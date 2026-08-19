---
name: pr-neighbors
description: Use when opening, reviewing, or rebasing a pull request and you want to know what else is in flight against the same code — "what else touches this", "what PRs relate to this one", "will anything conflict", "am I stale". Finds the PRs that impact or are impacted by one PR, including PRs that share no files with it, via a code graph. Splits merged hits into ones your branch lacks and ones that are context. Reports only; changes nothing.
allowed-tools: Bash, Read, Grep, Glob
license: MIT
---

# PR neighbours

Answers one question about a pull request: **what else is moving in the code this
PR touches?** Not just PRs editing the same files — that is the easy half — but
PRs editing code that calls into, or is called by, what this PR changed.

It reports. It does not rebase, comment, or change anything.

## Why file overlap is not enough

A PR that changes a method and a PR that changes the only caller of that method
share no files at all. They will merge cleanly and one of them will be wrong.
Nothing in the GitHub UI shows this. That gap is the reason this skill exists,
and it is why the graph layer is worth its cost.

Measured on a real pair: PR A changed `OwnerShareReconciler`, PR B changed
`OwnerShareReconciliationBatch`, which calls it. Zero shared files. Only the
graph found it.

## Run it

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/pr-neighbors/scripts/pr_neighbors.py" <pr-number> \
  --repo-path <local-checkout> [--index <gitnexus-index>] [options]
```

Four layers. The script runs 1–3 always; 4 is opt-in.

| Layer | Finds | Cost |
| --- | --- | --- |
| 1 · File overlap | Other PRs editing a file this PR edits | free |
| 2 · Blast radius | Other PRs editing a file that calls, or is called by, a symbol this PR changed | needs a GitNexus index |
| 3 · Merged history | Already-merged PRs on the same ground, split by whether this branch has them | free |
| 4 · New references (`--new-callers`) | Other PRs that *add* a reference to a blast-radius symbol | one API call per candidate |

Layer 4 exists because no graph can find it. If another PR adds the first-ever
call to a method this PR is changing, that edge does not exist in any index —
it lives only in the other PR's diff. It is off by default because it is the
only slow layer; turn it on when the PR changes a shared or public API.

Measured on a 9,000-file repo: a 100-file / 90-symbol PR runs layers 1–3 in
about **6s** at depth 1 and **11s** at depth 2. Layer 4 adds roughly a second
per candidate PR it has not already reported (~45s across 40 open PRs).

## Index the PR's branch, not main

**This is the step that makes or breaks layer 2.** A symbol the PR introduces
does not exist in an index built from `main`, so the blast radius comes back
empty and the skill reports a confident "nothing related."

```bash
git fetch origin pull/<N>/head
git worktree add --detach ../wt-pr<N> FETCH_HEAD
printf '{"name":"repo-pr<N>","defaultBranch":"main"}\n' > ../wt-pr<N>/.gitnexusrc
gitnexus analyze ../wt-pr<N>
```

Then pass `--index repo-pr<N>`. Roughly a minute on a 9,000-file repo — cheap
enough to do per review. Name the index in `.gitnexusrc`, because the registry is
keyed by path and two worktrees of one repo are otherwise indistinguishable.

Tear it down in this order, or the registry keeps a pointer to a deleted path:

```bash
cd ../wt-pr<N> && gitnexus clean
cd - && git worktree remove ../wt-pr<N>
```

The script checks whether the indexed commit **contains this PR's head**, and
says so when it does not:

```
⚠  Index 'main-repo' (commit 526838b, 2026-08-07) does NOT contain this PR's
   head — 17 commits of this PR are missing from it.
   Layer 2 cannot see symbols the PR introduces.
```

That is the check that matters, not commits-behind. An index built from main is
"fresh" by any staleness measure and still blind to every class the PR adds.

Read every warning as **"this layer did not run"**, never as "nothing found".
The two are indistinguishable in output and mean opposite things, which is why
warnings print twice — once before the results and once after.

## Reading the output

Five sections, and the distinction between the two merged ones is the point.

**OPEN — concurrent work.** Someone is editing this code right now. Risk is
conflict, duplicated work, or two designs that disagree. `=` marks a shared
file, `~` a blast-radius file.

**MERGED, NOT IN YOUR BRANCH.** Already on the main line, absent from this
branch. The branch is built on ground that moved. Usually means rebase, and
sometimes means a decision this PR encodes was already overtaken.

**MERGED, ALREADY IN YOUR BRANCH.** Context, not risk. How this code got to be
the way it is. Worth reading before reviewing an unfamiliar subsystem.

**CLOSED WITHOUT MERGING.** Someone attempted work here and abandoned it. Rare,
occasionally the most useful section in the report — it can mean the approach
this PR is taking was already tried. `gh pr list --state closed` includes merged
PRs, so these are filtered on a null `mergedAt`.

**NEW REFERENCES.** Layer 4. A PR is about to depend on something being changed
here. PRs already named in the sections above are not re-scanned.

Same ancestry test drives the two merged sections — `git merge-base
--is-ancestor` against the PR head. Same fact, opposite meanings, so they are
never merged into one list.

## Two kinds of noise it suppresses, and why

**Same-stack PRs.** A stacked PR contains its parent's commits, so every member
of a stack shares files with every other member. That is the stack working as
designed, not a collision. Without suppression a nine-deep stack reports eight
false conflicts on its first run — measured, not hypothetical. Suppressed by
default with a count; `--show-stack` to include them.

**Hub files.** A base class two hundred classes extend matches nearly every PR.
Hub-ness is a property of the graph, not of this week's PR traffic, so it is
measured as in-degree (`--hub-degree`, default 12 distinct dependent files)
rather than by how many PRs happen to touch the file. **The threshold itself is
a guess** — 12 was chosen because it puts a 196-dependent base class on the
right side of the line, and nothing validates where the boundary belongs. Tune
it per repo.

Hub-only hits are labelled `hub only — weak`, annotated with the degree, and
sorted last. They are shown, not dropped: a PR *deleting* a hub class is
extremely relevant to a PR that extends it. Within each hit, shared files are
listed before blast-radius ones, because the per-hit list is truncated and
alphabetical order otherwise lets a weak hub match crowd out every strong one.

## Options

| Option | Default | Notes |
| --- | --- | --- |
| `--repo` | *(required)* | GitHub `owner/name` |
| `--repo-path` | `.` | Local checkout, used for git history and the ancestry test |
| `--index` | auto | GitNexus index name; required when more than one is registered |
| `--state` | `open,merged` | `open`, `merged`, `closed`, or `all` |
| `--since` | none | Age filter for merged and closed |
| `--limit` | 15 | Max hits per section |
| `--depth` | 1 | Graph hops, capped at 3 |
| `--hub-degree` | 12 | Dependent-file count above which a file counts as a hub. A heuristic, not a measurement — tune it if the `hub only — weak` label is landing wrongly |
| `--base-ref` | `origin/HEAD`, then `origin/main` | History ref for layer 3 |
| `--new-callers` | off | Layer 4 |
| `--show-stack` | off | Do not suppress same-stack PRs |

## On `--since`, and why there is no default window

There is no default age window, deliberately. Per-subsystem activity is bursty,
so a fixed window hides more than it saves. Measured on one real blast radius:

```
  7d: 0 merged PRs        21d: 6        60d: 6
 14d: 0                   30d: 6        90d: 6
```

A 14-day default would have reported "nothing related" on a subsystem with six
related merges three weeks earlier. The cliff sits wherever that subsystem's
burst happened, which no default can know.

Scanning all history is not the expensive part — 2,673 commits with full file
lists takes about 0.2s, because merged PRs come out of `git log` rather than the
API (squash-merge subjects carry the `(#N)` suffix). So the whole history is
read, results are ranked by recency, and `--limit` caps the output. `--since`
stays available for when the question really is "what landed since I branched."

## Engine gotchas worth knowing

- **`ALL(x IN r WHERE x.type IN [...])` over a variable-length relationship list
  returns zero rows** on LadybugDB/Kùzu, without erroring. That reads as
  "nothing is affected", which is the worst possible failure mode here. Depth is
  therefore walked as repeated single hops. An untyped `*1..N` does work but
  drags in folder nodes through `CONTAINS`.
- **Every `gitnexus` invocation costs ~0.8s of process startup regardless of
  query size.** Batch with `IN [...]`: one query over 200 symbols costs the same
  as one query over one. A per-symbol loop over a 90-class PR takes minutes;
  batched, under a second. This is the single biggest performance decision in
  the script.
- **An empty Cypher result is a bare `[]`**, not an object with a `markdown`
  key. Treating that as a parse failure turns "nothing references this" into
  "the query broke".
- **`gitnexus list` has no `--json`.** It exits 0 and prints `error: unknown
  option '--json'` to stdout, so a script that parses it gets silence rather
  than a failure. The human output is parsed instead.
- Exact `filePath` equality works fine and is preferred over a `.*Name.cls`
  regex, which also matches any file whose name merely ends with the target's.

## Self-check

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/pr-neighbors/scripts/test_pr_neighbors.py"
```

No framework, no network, no GitNexus. Covers the pure logic: symbol
resolution, Cypher quoting and result parsing, the `gitnexus list` parser,
stack topology, `--since` resolution, closed-PR filtering, warning dedupe,
subprocess failure handling, index selection, and evidence ranking.

It is mutation-tested: sixteen deliberate single-line breakages, all sixteen
caught. Two findings came out of writing it, and both are the reason it exists:

- A stale `__pycache__/*.pyc` made the suite test code that was no longer on
  disk, so two mutation rounds reported the wrong result. The loader now
  compiles from source text rather than importing.
- The `run()` test was placed after a stub had replaced `pn.run`, so it
  exercised the stub. A green check testing nothing. The real function is now
  captured before any stubbing, restored after each stubbed section, and a final
  assertion confirms no stub leaked.

## Limits

- Symbol resolution is by filename, so it is accurate for Apex (one top-level
  class per file) and coarse for JavaScript.
- Layer 2 sees the PR's branch and the index it was built from. A symbol
  introduced by a *different* open PR is invisible to it — that is layer 3's job.
- Metadata-only PRs (permission sets, custom metadata, flows) have no symbols, so
  only layers 1 and 3 apply. That is not a failure; the output says so.
- Layer 4 matches symbol names textually in added lines of **code files only**,
  and separates a file that *defines* the symbol from one that *references* it.
  It still cannot tell a real call from a name inside a comment or string. An
  earlier version omitted the code-file filter entirely, so every design doc
  naming a class read as a new call — and this repo commits plan and design docs
  alongside code by policy, which made that systematic rather than incidental.
- Ancestry needs the PR head as a local object. The script fetches
  `pull/<N>/head` first; if that fails it says the merged/stale split could not
  be computed rather than guessing.
