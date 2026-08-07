#!/usr/bin/env python3
"""Find the pull requests that impact, or are impacted by, one PR.

Usage: pr_neighbors.py <pr-number> [options]

Four layers:

  1. File overlap        which other PRs edit a file this PR edits.
  2. Blast radius        which other PRs edit a file that calls into, or is
                         called by, a symbol this PR changed. Needs a GitNexus
                         index built from THIS PR's branch -- a symbol the PR
                         introduces does not exist in a main index.
  3. Merged history      which already-merged PRs touched the same ground, split
                         by whether this branch contains them yet.
  4. New references      (--new-callers) which other PRs add a reference to a
                         blast-radius symbol. No graph can see this: the edge
                         lives in the other PR's diff, not in any index.

Layers 1-3 are close to free. Layer 4 costs one API call per candidate PR.

Every failure path is loud. A layer that could not run says so rather than
reporting zero results, because "nothing related" and "I could not check" look
identical in output and mean opposite things.
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from collections import defaultdict

# Extensions that resolve to a symbol name. Anything else (metadata XML, docs,
# permission sets) participates in file overlap only.
CODE_EXT = (".cls", ".trigger", ".js", ".ts")
EDGE_TYPES = "['CALLS','EXTENDS','IMPLEMENTS','IMPORTS','METHOD_OVERRIDES']"
# Files referenced by at least this many distinct other files are hubs: matching
# one is a property of the file, not a relationship between two PRs. The number
# is a heuristic, not a measurement -- override with --hub-degree.
HUB_DEGREE = 12
# Symbols queried per Cypher batch. Batching matters enormously: each `gitnexus`
# invocation costs ~0.8s of process startup regardless of query size, so a
# per-symbol loop over a 90-class PR takes minutes while one batched query takes
# under a second.
BATCH = 200

# Ordered set with occurrence counts: one Cypher failure per batch would
# otherwise print the same line dozens of times on a large PR.
WARNINGS = {}


def warn(msg):
    WARNINGS[msg] = WARNINGS.get(msg, 0) + 1


def flush_warnings():
    for msg, n in WARNINGS.items():
        times = f"  (×{n})" if n > 1 else ""
        print(f"  ⚠  {msg}{times}")
    WARNINGS.clear()


def run(cmd, **kw):
    """(returncode, stdout, stderr). Never raises.

    A missing binary makes subprocess.run raise rather than return non-zero, so
    an uninstalled `gh` or `gitnexus` produced a raw traceback instead of the
    explained failure every other path gives.
    """
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, **kw)
    except FileNotFoundError:
        return 127, "", f"{cmd[0]}: command not found"
    except OSError as e:
        return 126, "", f"{cmd[0]}: {e}"
    return p.returncode, p.stdout, p.stderr


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def quote(values):
    """Cypher string list. Backslash first, or the quote escape is re-escaped."""
    out = []
    for v in values:
        out.append("'" + v.replace("\\", "\\\\").replace("'", "\\'") + "'")
    return ",".join(out)


# --------------------------------------------------------------------------
# GitNexus
# --------------------------------------------------------------------------

def cypher(query, index=None):
    """Run one Cypher query, returning rows as dicts. [] on any failure."""
    cmd = ["gitnexus", "cypher", query]
    if index:
        cmd += ["--repo", index]
    code, out, err = run(cmd)
    if code != 0:
        warn(f"Cypher call failed ({err.strip()[:120] or 'no stderr'}). "
             f"Layer 2 results are incomplete.")
        return []
    try:
        payload = json.loads(out)
    except json.JSONDecodeError:
        warn("Cypher returned unparseable output. Layer 2 is incomplete.")
        return []
    # An empty result set is a bare `[]`, not an object with a `markdown` key.
    if not isinstance(payload, dict):
        return []
    lines = [l for l in payload.get("markdown", "").splitlines()
             if l.startswith("|")]
    if len(lines) < 3:
        return []
    header = [c.strip() for c in lines[0].strip("|").split("|")]
    rows = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) == len(header):
            rows.append(dict(zip(header, cells)))
    return rows


def index_info(name=None):
    """Parse `gitnexus list` into {name: {path, commit, branch, indexed}}.

    There is no `--json` on `list`, so the human output is parsed. An earlier
    version of this script called `gitnexus list --json`, silently got an
    "unknown option" error, and therefore never once emitted the staleness
    warning it existed to emit.
    """
    code, out, _ = run(["gitnexus", "list"])
    if code != 0:
        return {}
    repos, cur = {}, None
    for raw in out.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = re.match(r"^(Path|Indexed|Commit|Branch):\s+(.*)$", line)
        if m and cur:
            repos[cur][m.group(1).lower()] = m.group(2).strip()
        elif not line.startswith(("Indexed Repositories", "Stats:", "Clusters:",
                                  "Processes:")) and ":" not in line:
            cur = line
            repos[cur] = {}
    if name:
        for key, val in repos.items():
            if name in (key, val.get("path")):
                return {key: val}
        return {}
    return repos


def resolve_index(index, repo_path):
    """Pick the index to query, or die explaining the choice.

    GitNexus makes `--repo` mandatory the moment a second index is registered,
    and every query fails without it. Since one worktree index is exactly what
    this skill tells you to build, that state is the normal case rather than the
    exception -- so the index whose path matches the checkout is selected
    automatically instead of failing.
    """
    if index:
        return index
    repos = index_info()
    if len(repos) <= 1:
        return index
    want = os.path.realpath(repo_path)
    for name, meta in repos.items():
        if meta.get("path") and os.path.realpath(meta["path"]) == want:
            warn(f"{len(repos)} indexes registered; using '{name}' because its "
                 f"path matches --repo-path. Pass --index to override.")
            return name
    die("several GitNexus indexes are registered and none matches "
        f"--repo-path {repo_path}. Pass --index with one of: "
        f"{', '.join(sorted(repos))}")


def check_index(index, pr_head, repo_path):
    """Verify the index can actually answer questions about this PR's code.

    Staleness in commits is the weaker signal. The one that matters is whether
    the indexed commit contains the PR head at all: an index built from main
    cannot see a class the PR introduces, so layer 2 returns an empty radius
    that reads exactly like "nothing is related".
    """
    info = index_info(index)
    if not info:
        warn("Could not read the GitNexus index list. Layer 2 is unverified — "
             "treat an empty blast radius as 'not checked', not as 'nothing found'.")
        return
    name, meta = next(iter(info.items()))
    commit, path = meta.get("commit", ""), meta.get("path", "")
    if not commit:
        warn(f"Index '{name}' reports no indexed commit. Layer 2 is unverified.")
        return

    code, _, _ = run(["git", "-C", repo_path, "cat-file", "-e", commit])
    if code != 0:
        warn(f"Index '{name}' is at commit {commit}, which is not in "
             f"{repo_path}. Layer 2 may describe a different tree.")
        return

    code, out, _ = run(["git", "-C", repo_path, "merge-base",
                        "--is-ancestor", pr_head, commit])
    if code != 0:
        _, behind, _ = run(["git", "-C", repo_path, "rev-list", "--count",
                            f"{commit}..{pr_head}"])
        n = behind.strip() or "?"
        warn(f"Index '{name}' (commit {commit}, {meta.get('indexed', '?')}) does "
             f"NOT contain this PR's head — {n} commits of this PR are missing "
             f"from it.\n     Layer 2 cannot see symbols the PR introduces. "
             f"Build an index from the PR's branch:\n"
             f"       git worktree add --detach ../wt-pr FETCH_HEAD && "
             f"gitnexus analyze ../wt-pr")


def blast_radius(symbols, index=None, depth=1):
    """Files that reference, or are referenced by, any of these symbols.

    Depth is walked as repeated *batched* single hops. A variable-length
    `ALL(x IN r WHERE x.type IN [...])` predicate returns zero rows on this
    engine (LadybugDB/Kuzu) without erroring, which reads as "nothing is
    affected" -- so it is not used.
    """
    files, seen = set(), set()
    frontier = set(s for s in symbols if s)
    for _ in range(max(1, depth)):
        batch = sorted(frontier - seen)
        if not batch:
            break
        nxt = set()
        for i in range(0, len(batch), BATCH):
            chunk = batch[i:i + BATCH]
            seen |= set(chunk)
            names = quote(chunk)
            for near, far in (("b", "a"), ("a", "b")):
                q = (f"MATCH (a)-[r:CodeRelation]->(b) "
                     f"WHERE {near}.name IN [{names}] AND r.type IN {EDGE_TYPES} "
                     f"RETURN DISTINCT {far}.filePath AS f, {far}.name AS n")
                for row in cypher(q, index):
                    if row.get("f", "").count("/"):
                        files.add(row["f"])
                    if row.get("n"):
                        nxt.add(row["n"])
        frontier = nxt
    return files, seen


def dependents(paths, index=None):
    """Distinct referencing-file count per path, in one batched query.

    Matched on exact path rather than a `.*Name.cls` regex. The regex form would
    also match any file whose name merely *ends* with the target's name --
    `ContractBaseRepo.cls` for a `BaseRepo.cls` target. No such collision exists
    in this repo today, so this is a latent correctness fix, not an observed
    one: both forms currently return the same counts.
    """
    out = {p: 0 for p in paths}
    paths = sorted(paths)
    for i in range(0, len(paths), BATCH):
        chunk = paths[i:i + BATCH]
        q = (f"MATCH (a)-[r:CodeRelation]->(b) "
             f"WHERE b.filePath IN [{quote(chunk)}] AND r.type IN {EDGE_TYPES} "
             f"RETURN b.filePath AS f, count(DISTINCT a.filePath) AS n")
        for row in cypher(q, index):
            try:
                out[row["f"]] = int(row["n"])
            except (KeyError, ValueError):
                pass
    return out


# --------------------------------------------------------------------------
# GitHub / git
# --------------------------------------------------------------------------

def gh_json(args, what):
    code, out, err = run(["gh"] + args)
    if code != 0:
        die(f"`gh` failed reading {what}: {err.strip()[:200]}")
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        die(f"`gh` returned unparseable JSON for {what}")


def pr_meta(num, repo):
    fields = ("number,title,author,headRefName,baseRefName,headRefOid,files,"
              "isDraft,state")
    return gh_json(["pr", "view", str(num), "--repo", repo, "--json", fields],
                   f"PR {num}")


def list_prs(repo, state, limit=100):
    fields = ("number,title,author,headRefName,baseRefName,files,isDraft,"
              "mergedAt,closedAt")
    return gh_json(["pr", "list", "--repo", repo, "--state", state,
                    "--limit", str(limit), "--json", fields],
                   f"{state} PR list")


def stack_members(prs, target):
    """PRs reachable from target by base/head chaining, in both directions.

    A stacked child contains its parent's commits, so every member of a stack
    shares files with every other member. Unsuppressed, a nine-deep stack
    reports eight false conflicts.
    """
    by_head = {p["headRefName"]: p for p in prs}
    by_base = defaultdict(list)
    for p in prs:
        by_base[p["baseRefName"]].append(p)
    seen, queue = set(), [target]
    while queue:
        cur = queue.pop()
        if cur["number"] in seen:
            continue
        seen.add(cur["number"])
        parent = by_head.get(cur["baseRefName"])
        if parent:
            queue.append(parent)
        queue.extend(by_base.get(cur["headRefName"], []))
    return seen


def stack_groups(prs):
    groups, assigned = [], set()
    for p in prs:
        if p["number"] in assigned:
            continue
        members = stack_members(prs, p)
        assigned |= members
        groups.append(sorted(members))
    return groups


def merged_commits(repo_path, base_ref, since=None):
    """[(sha, date, pr|None, subject, [files])], newest first, from git log."""
    cmd = ["git", "-C", repo_path, "log", base_ref]
    if since:
        cmd.append(f"--since={since}")
    cmd += ["--name-only", "--pretty=format:@@%H\t%cs\t%s"]
    code, out, err = run(cmd)
    if code != 0:
        warn(f"Could not read history from '{base_ref}' in {repo_path} "
             f"({err.strip()[:100]}). Layer 3 did not run.")
        return None
    commits, cur, files = [], None, []
    for line in out.splitlines():
        if line.startswith("@@"):
            if cur:
                commits.append((*cur, files))
            sha, date, subj = line[2:].split("\t", 2)
            m = re.search(r"\(#(\d+)\)", subj)
            cur, files = (sha, date, int(m.group(1)) if m else None, subj), []
        elif line.strip():
            files.append(line.strip())
    if cur:
        commits.append((*cur, files))
    return commits


def resolve_base(repo_path):
    for ref in ("origin/HEAD", "origin/main", "origin/master"):
        code, _, _ = run(["git", "-C", repo_path, "rev-parse", "--verify", "-q", ref])
        if code == 0:
            return ref
    return None


def ancestry(repo_path, shas, head):
    """{sha: bool} -- does `head` contain each sha. One process per sha."""
    out = {}
    for sha in shas:
        code, _, _ = run(["git", "-C", repo_path, "merge-base",
                          "--is-ancestor", sha, head])
        out[sha] = code == 0
    return out


def diff_symbol_refs(num, repo, names):
    """Blast-radius symbols this PR references from *code* it adds.

    Two filters that the first version of this lacked:

      * only added lines inside code files count. Without this, a design doc
        naming a class in prose reads as a new call -- and this repo commits
        plan and design docs alongside code by policy, so that is systematic
        rather than incidental.
      * a file that *defines* the symbol is reported separately from one that
        *calls* it. Editing FooService.cls is not "adding a reference to Foo".
    """
    code, diff, _ = run(["gh", "pr", "diff", str(num), "--repo", repo])
    if code != 0:
        warn(f"Could not read the diff for #{num}; layer 4 skipped it.")
        return set(), set()
    refs, defs, path = set(), set(), ""
    for line in diff.splitlines():
        if line.startswith("diff --git"):
            parts = line.split()
            path = parts[-1][2:] if len(parts) >= 4 else ""
            continue
        if not line.startswith("+") or line.startswith("+++"):
            continue
        if not path.endswith(CODE_EXT):
            continue
        stem = symbol_of(path)
        for n in names:
            if re.search(rf"\b{re.escape(n)}\b", line):
                (defs if n == stem else refs).add(n)
    return refs, defs


# --------------------------------------------------------------------------

def since_cutoff(since):
    """`--since` as a YYYY-MM-DD string, or None if it cannot be resolved.

    `git log --since` accepts relative strings natively; the GitHub PR list does
    not, so the same value has to be resolved to a date for the closed-PR
    filter. Resolution is delegated to git rather than reimplemented, so both
    layers agree on what "30 days ago" means.
    """
    if not since:
        return None
    text = since.strip()
    if re.match(r"^\d{4}-\d{2}-\d{2}$", text):
        return text
    m = re.match(r"^(\d+)\s+(day|week|month|year)s?(\s+ago)?$", text)
    if m:
        n, unit = int(m.group(1)), m.group(2)
        days = {"day": 1, "week": 7, "month": 30, "year": 365}[unit] * n
        return (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    warn(f"Could not resolve --since '{since}' to a date, so the closed-PR "
         f"section is unfiltered. `git log --since` still honours it, so the "
         f"merged sections are filtered. Use 'N days ago' or YYYY-MM-DD.")
    return None


def abandoned_prs(prs, cutoff=None):
    """Closed-without-merging PRs, optionally newer than `cutoff`.

    `gh pr list --state closed` includes merged PRs, so the null-`mergedAt`
    filter is what makes this section mean "attempted and abandoned" rather than
    "closed somehow".
    """
    out = []
    for p in prs:
        if p.get("mergedAt"):
            continue
        if cutoff and (p.get("closedAt") or "")[:10] < cutoff:
            continue
        out.append(p)
    return out


def symbol_of(path):
    """Symbol name for a code path. `Foo.cls` -> Foo; `foo.test.js` -> foo."""
    base = os.path.basename(path)
    for ext in CODE_EXT:
        if base.endswith(ext):
            base = base[: -len(ext)]
            break
    # Strip a trailing test/spec qualifier so foo.test.js resolves to foo
    # rather than to the non-existent symbol "foo.test".
    return re.sub(r"\.(test|spec)$", "", base)


def symbols_from(paths):
    return {symbol_of(p) for p in paths if p.endswith(CODE_EXT)}


def show_files(files, shared, hub, fanout, cap=4):
    """Strongest evidence first, since `cap` truncates.

    Sorting the union alphabetically lets a weak hub hit crowd out every shared
    file, so the ranked list reads as if the PRs merely share a base class.
    """
    ranked = sorted(files, key=lambda f: (f not in shared, f in hub, f))
    for f in ranked[:cap]:
        mark = "=" if f in shared else "~"
        note = f"  (hub: {fanout[f]} files depend on it)" if f in hub else ""
        print(f"      {mark} {os.path.basename(f)}{note}")
    if len(ranked) > cap:
        print(f"      … and {len(ranked) - cap} more")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pr", type=int)
    ap.add_argument("--repo", required=True, help="GitHub owner/name")
    ap.add_argument("--repo-path", default=".", help="local checkout for git history")
    ap.add_argument("--index", help="GitNexus index name (omit if only one)")
    ap.add_argument("--base-ref", help="history ref for layer 3 "
                                       "(default: origin/HEAD, then origin/main)")
    ap.add_argument("--state", default="open,merged",
                    help="open,merged,closed or all (default: open,merged)")
    ap.add_argument("--since", help="age filter for merged and closed, e.g. "
                                    "'30 days ago'. No default: per-subsystem "
                                    "activity is bursty, so a fixed window "
                                    "hides more than it saves.")
    ap.add_argument("--limit", type=int, default=15, help="max hits per section")
    ap.add_argument("--depth", type=int, default=1, choices=range(1, 4),
                    metavar="1-3", help="graph hops (default 1)")
    ap.add_argument("--hub-degree", type=int, default=HUB_DEGREE,
                    help=f"dependent-file count above which a file is a hub "
                         f"(default {HUB_DEGREE}, a heuristic)")
    ap.add_argument("--new-callers", action="store_true",
                    help="layer 4: scan candidate diffs for added references. "
                         "One API call per candidate PR.")
    ap.add_argument("--show-stack", action="store_true",
                    help="do not suppress same-stack PRs")
    args = ap.parse_args()

    states = {s.strip() for s in args.state.split(",")}
    if "all" in states:
        states = {"open", "merged", "closed"}
    unknown = states - {"open", "merged", "closed"}
    if unknown:
        die(f"unknown --state value(s): {', '.join(sorted(unknown))}")

    target = pr_meta(args.pr, args.repo)
    changed = {f["path"] for f in target["files"]}
    symbols = symbols_from(changed)

    print(f"PR {args.pr} — {target['title']}")
    print(f"  {target['headRefName']} → {target['baseRefName']} · "
          f"{len(changed)} files · {len(symbols)} code symbols")

    run(["git", "-C", args.repo_path, "fetch", "origin", "-q",
         f"pull/{args.pr}/head"])
    head = target["headRefOid"]
    code, _, _ = run(["git", "-C", args.repo_path, "cat-file", "-e", head])
    if code != 0:
        warn(f"PR head {head[:8]} is not in {args.repo_path}; the "
             f"merged-vs-stale split cannot be computed.")
        head = None

    index = resolve_index(args.index, args.repo_path)
    radius, reached = set(), set()
    if symbols:
        if head:
            check_index(index, head, args.repo_path)
        radius, reached = blast_radius(symbols, index, args.depth)
        radius -= changed
    else:
        warn("This PR changes no code files, so layer 2 does not apply. "
             "File overlap still does.")
    if symbols and not radius:
        warn("Blast radius is empty. Either the change is a genuine leaf or its "
             "symbols are absent from the index — read this as 'not checked'.")
    print(f"  blast radius: {len(radius)} files, {len(reached)} symbols")

    if WARNINGS:
        print()
        flush_warnings()
    print()

    fanout = dependents(radius, index) if radius else {}
    hub = {f for f, n in fanout.items() if n >= args.hub_degree}
    reported = set()

    # ---- layer 1 + 2 : open ---------------------------------------------
    if "open" in states:
        prs = list_prs(args.repo, "open")
        stack = stack_members(prs, target) if not args.show_stack else {args.pr}
        rows, suppressed = [], 0
        for p in prs:
            if p["number"] == args.pr:
                continue
            files = {f["path"] for f in p["files"]}
            shared, reach = files & changed, files & radius
            if not (shared or reach):
                continue
            if p["number"] in stack:
                suppressed += 1
                continue
            rows.append((p, shared, reach))
        rows.sort(key=lambda r: (-len(r[1]), -len(r[2] - hub), -len(r[2])))

        print(f"OPEN — concurrent work ({len(rows)} related)")
        if not rows:
            print("  none")
        for p, shared, reach in rows[:args.limit]:
            reported.add(p["number"])
            kind = ("shared file" if shared
                    else "blast radius" if reach - hub else "hub only — weak")
            draft = " [draft]" if p["isDraft"] else ""
            print(f"  #{p['number']}{draft}  {p['author']['login']}  ({kind})")
            print(f"      {p['title'][:70]}")
            show_files(shared | reach, shared, hub, fanout)
        if len(rows) > args.limit:
            print(f"  ({len(rows) - args.limit} more above --limit {args.limit})")
        if suppressed:
            print(f"  ({suppressed} same-stack PRs suppressed; --show-stack "
                  f"to include)")

    # ---- layer 3 : merged history ---------------------------------------
    if "merged" in states:
        base = args.base_ref or resolve_base(args.repo_path)
        commits = merged_commits(args.repo_path, base, args.since) if base else None
        if base is None:
            warn(f"No origin/HEAD, origin/main or origin/master in "
                 f"{args.repo_path}. Layer 3 did not run — pass --base-ref.")
        if commits is None:
            print("\nMERGED — not checked (see warnings)")
        else:
            hits = [(sha, date, num, subj,
                     (set(files) & changed, set(files) & radius))
                    for sha, date, num, subj, files in commits
                    if (set(files) & changed) or (set(files) & radius)]
            contains = ancestry(args.repo_path, [h[0] for h in hits], head) \
                if head else {}
            stale = [h for h in hits if not contains.get(h[0], True)]
            ctx = [h for h in hits if contains.get(h[0], True)]

            label = ("MERGED, NOT IN YOUR BRANCH — you are stale against these"
                     if head else
                     "MERGED — ancestry unknown, PR head unavailable")
            print(f"\n{label} ({len(stale)})")
            if not stale:
                print("  none")
            for sha, date, num, subj, (shared, reach) in stale[:args.limit]:
                tag = f"#{num}" if num else sha[:8]
                print(f"  {date}  {tag:8s} {subj[:62]}")
                show_files(shared | reach, shared, hub, fanout, cap=3)

            print(f"\nMERGED, ALREADY IN YOUR BRANCH — context ({len(ctx)})")
            if not ctx:
                print("  none")
            for sha, date, num, subj, _ in ctx[:args.limit]:
                tag = f"#{num}" if num else sha[:8]
                print(f"  {date}  {tag:8s} {subj[:62]}")

    # ---- layer 3b : closed unmerged --------------------------------------
    if "closed" in states:
        # `gh pr list --state closed` includes merged PRs, so filter on mergedAt.
        abandoned = abandoned_prs(list_prs(args.repo, "closed", 200),
                                  since_cutoff(args.since))
        rows = []
        for p in abandoned:
            files = {f["path"] for f in p["files"]}
            shared, reach = files & changed, files & radius
            if shared or reach:
                rows.append((p, shared, reach))
        rows.sort(key=lambda r: -r[0]["number"])
        print(f"\nCLOSED WITHOUT MERGING — attempted here before ({len(rows)})")
        if not rows:
            print("  none")
        for p, shared, reach in rows[:args.limit]:
            when = (p.get("closedAt") or "")[:10]
            print(f"  {when}  #{p['number']}  {p['author']['login']}")
            print(f"      {p['title'][:70]}")
            show_files(shared | reach, shared, hub, fanout, cap=3)

    # ---- layer 4 : new references ----------------------------------------
    if args.new_callers:
        print("\nNEW REFERENCES — calls being added that no index can see")
        if not reached:
            print("  skipped: no blast-radius symbols to look for")
        else:
            prs = list_prs(args.repo, "open")
            candidates = [p for p in prs
                          if p["number"] != args.pr and p["number"] not in reported]
            skipped = len(prs) - 1 - len(candidates)
            found = False
            for members in stack_groups(prs):
                hits = {}
                for num in members:
                    if not any(p["number"] == num for p in candidates):
                        continue
                    refs, _ = diff_symbol_refs(num, args.repo, reached)
                    if refs:
                        hits[num] = refs
                if not hits:
                    continue
                found = True
                syms = sorted(set().union(*hits.values()))
                where = (f"#{next(iter(hits))}" if len(hits) == 1
                         else f"#{min(hits)}–#{max(hits)} "
                              f"({len(hits)} PRs in one stack)")
                print(f"  {where}  adds: {', '.join(syms[:5])}")
            if not found:
                print("  none")
            if skipped:
                print(f"  ({skipped} already reported above, not re-scanned)")

    if WARNINGS:
        print()
        flush_warnings()
    print("\n  =  edits a file this PR edits    ~  edits a file in the blast radius")


if __name__ == "__main__":
    main()
