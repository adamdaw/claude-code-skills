#!/usr/bin/env python3
"""Self-check for pr_neighbors.py. No framework, no network, no GitNexus.

    python3 test_pr_neighbors.py

Covers the pure logic: text parsing, symbol resolution, stack topology, date
resolution, and evidence ranking. Every case here is one that a wrong answer
would silently corrupt a report rather than crash it.
"""
import datetime
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "pr_neighbors.py")

# Compile from source text rather than importing. `importlib` honours
# __pycache__, and a stale .pyc left by an earlier `py_compile` silently made
# this file test code that was no longer on disk -- two mutation-test rounds
# reported the wrong result before that was spotted.
pn = types.ModuleType("pn")
pn.__file__ = SOURCE
with open(SOURCE) as fh:
    exec(compile(fh.read(), SOURCE, "exec"), pn.__dict__)

# Stubs below replace pn.run. Capture the real one first: an earlier version of
# this file tested run() *after* a stub had replaced it, so the check passed
# while exercising the stub -- a green suite testing nothing.
REAL_RUN = pn.run

FAILED = []


def check(label, got, want):
    if got != want:
        FAILED.append(f"{label}\n    got:  {got!r}\n    want: {want!r}")


# -- symbol resolution ------------------------------------------------------
# A wrong stem queries a symbol that does not exist, which returns an empty
# blast radius -- indistinguishable from "nothing is related".
check("Apex class", pn.symbol_of("pkgs/a/main/default/classes/Foo.cls"), "Foo")
check("trigger", pn.symbol_of("x/FooTrigger.trigger"), "FooTrigger")
check("jest test", pn.symbol_of("x/lwc/foo/__tests__/foo.test.js"), "foo")
check("ts spec", pn.symbol_of("x/bar.spec.ts"), "bar")
check("dotted name", pn.symbol_of("x/My.Thing.cls"), "My.Thing")
check("non-code untouched", pn.symbol_of("d/notes.md"), "notes.md")
check("meta.xml is not code",
      pn.symbols_from({"a/Foo.cls-meta.xml", "a/Foo.cls"}), {"Foo"})
check("metadata-only PR yields no symbols",
      pn.symbols_from({"a/x.permissionset-meta.xml", "b/y.md"}), set())

# -- Cypher quoting ---------------------------------------------------------
# An unescaped quote turns a query into a syntax error, which is reported as a
# failed layer rather than a wrong answer -- but a double-escaped backslash
# silently matches nothing.
check("plain", pn.quote(["A", "B"]), "'A','B'")
check("apostrophe", pn.quote(["O'Brien"]), "'O\\'Brien'")
check("backslash first", pn.quote(["a\\b"]), "'a\\\\b'")

# -- `gitnexus list` parser -------------------------------------------------
# This replaced a call to a flag that does not exist. If it silently returns {},
# the index guard goes quiet again -- the exact regression it was written for.
LIST_FIXTURE = """
  Indexed Repositories (2)

  main-repo
    Path:    /repo/main-repo
    Indexed: 2026-08-07, 9:05:29 a.m.
    Commit:  526838b
    Branch:  main
    Stats:   9520 files, 43221 symbols, 107445 edges
    Clusters:   1539
    Processes:  300

  main-repo-pr1278
    Path:    /repo/wt-pr1278
    Indexed: 2026-08-07, 6:12:00 p.m.
    Commit:  abc1234
    Branch:  HEAD
"""
# index_info shells out, so its parsing is exercised via a stubbed run().
pn.run = lambda cmd, **kw: (0, LIST_FIXTURE, "")
parsed = pn.index_info()
check("parses both indexes", sorted(parsed), ["main-repo", "main-repo-pr1278"])
check("captures commit", parsed["main-repo"]["commit"], "526838b")
check("captures path", parsed["main-repo-pr1278"]["path"], "/repo/wt-pr1278")
check("stats line is not a repo name", "Stats" in parsed, False)
check("lookup by name", sorted(pn.index_info("main-repo-pr1278")),
      ["main-repo-pr1278"])
check("lookup by path", sorted(pn.index_info("/repo/main-repo")),
      ["main-repo"])
check("unknown name yields nothing", pn.index_info("nope"), {})
pn.run = REAL_RUN

# -- index selection --------------------------------------------------------
# GitNexus makes --repo mandatory past the first index, so getting this wrong
# makes every layer-2 query fail -- and building a second index is exactly what
# the skill instructs.
pn.run = lambda cmd, **kw: (0, LIST_FIXTURE, "")
pn.WARNINGS.clear()
check("explicit index wins", pn.resolve_index("chosen", "/repo/main-repo"), "chosen")
check("explicit index needs no warning", len(pn.WARNINGS), 0)
check("picks the index matching --repo-path",
      pn.resolve_index(None, "/repo/wt-pr1278"), "main-repo-pr1278")
check("auto-pick is disclosed", len(pn.WARNINGS), 1)
pn.WARNINGS.clear()
import contextlib as _ctx
import io as _io
try:
    with _ctx.redirect_stderr(_io.StringIO()):   # die() is expected here
        pn.resolve_index(None, "/some/unrelated/checkout")
    check("no match must exit", "returned normally", "SystemExit")
except SystemExit:
    pass
pn.run = lambda cmd, **kw: (0, "\n  Indexed Repositories (1)\n\n  Solo\n    Path:    /repo/solo\n    Commit:  abc\n", "")
check("single index needs no --repo", pn.resolve_index(None, "/anywhere"), None)
pn.run = REAL_RUN
pn.WARNINGS.clear()

# -- Cypher result parser ---------------------------------------------------
pn.run = lambda cmd, **kw: (0, '{"markdown": "| f | n |\\n| --- | --- |\\n'
                               '| a/A.cls | A |\\n| b/B.cls | B |"}', "")
check("parses markdown rows", pn.cypher("q"),
      [{"f": "a/A.cls", "n": "A"}, {"f": "b/B.cls", "n": "B"}])
pn.run = lambda cmd, **kw: (0, "[]", "")
check("bare [] is empty, not an error", pn.cypher("q"), [])
pn.WARNINGS.clear()
pn.run = lambda cmd, **kw: (127, "", "gitnexus: command not found")
check("missing binary yields no rows", pn.cypher("q"), [])
check("missing binary warns", len(pn.WARNINGS), 1)
pn.WARNINGS.clear()
pn.run = REAL_RUN

# -- stack topology ---------------------------------------------------------
# Unsuppressed, every member of a stack reports as colliding with every other.
def pr(n, head, base):
    return {"number": n, "headRefName": head, "baseRefName": base}


STACK = [pr(1, "a", "main"), pr(2, "b", "a"), pr(3, "c", "b"),
         pr(9, "solo", "main"), pr(10, "other", "main")]
check("walks a stack in both directions",
      pn.stack_members(STACK, STACK[1]), {1, 2, 3})
check("from the bottom", pn.stack_members(STACK, STACK[0]), {1, 2, 3})
check("a lone PR is its own stack", pn.stack_members(STACK, STACK[3]), {9})
check("PRs sharing a base are not a stack",
      pn.stack_members(STACK, STACK[4]), {10})
check("groups partition every PR",
      sorted(pn.stack_groups(STACK)), [[1, 2, 3], [9], [10]])
check("groups cover all PRs once",
      sorted(n for g in pn.stack_groups(STACK) for n in g), [1, 2, 3, 9, 10])

# -- since resolution -------------------------------------------------------
today = datetime.date.today()
check("ISO passes through", pn.since_cutoff("2026-07-10"), "2026-07-10")
check("relative days", pn.since_cutoff("5 days ago"),
      (today - datetime.timedelta(days=5)).isoformat())
check("singular unit", pn.since_cutoff("1 week ago"),
      (today - datetime.timedelta(days=7)).isoformat())
check("no window", pn.since_cutoff(None), None)
pn.WARNINGS.clear()
check("unparseable yields None", pn.since_cutoff("next tuesday"), None)
check("unparseable warns", len(pn.WARNINGS), 1)
pn.WARNINGS.clear()

# -- closed-PR filtering ----------------------------------------------------
# `gh pr list --state closed` includes merged PRs, so a missing mergedAt filter
# reports every merged PR as an abandoned attempt.
CLOSED = [
    {"number": 1, "mergedAt": "2026-08-01T00:00:00Z", "closedAt": "2026-08-01T00:00:00Z"},
    {"number": 2, "mergedAt": None, "closedAt": "2026-07-14T00:00:00Z"},
    {"number": 3, "mergedAt": None, "closedAt": "2026-07-08T00:00:00Z"},
    {"number": 4, "mergedAt": None, "closedAt": None},
]
check("merged PRs are excluded",
      [p["number"] for p in pn.abandoned_prs(CLOSED)], [2, 3, 4])
check("cutoff filters by closedAt",
      [p["number"] for p in pn.abandoned_prs(CLOSED, "2026-07-10")], [2])
check("cutoff drops a null closedAt",
      [p["number"] for p in pn.abandoned_prs(CLOSED, "2026-01-01")], [2, 3])
check("no cutoff keeps a null closedAt",
      4 in [p["number"] for p in pn.abandoned_prs(CLOSED)], True)

# -- run() never raises -----------------------------------------------------
# subprocess.run raises on a missing binary; letting that escape produced a raw
# traceback for the most ordinary failure there is (the tool is not installed).
code, out, err = REAL_RUN(["definitely-not-a-real-binary-xyz"])
check("missing binary returns 127", code, 127)
check("missing binary explains itself", "command not found" in err, True)

import tempfile
with tempfile.TemporaryDirectory() as td:
    noexec = os.path.join(td, "noexec")
    with open(noexec, "w") as fh:
        fh.write("#!/bin/sh\ntrue\n")
    os.chmod(noexec, 0o644)          # readable, not executable -> PermissionError
    code, out, err = REAL_RUN([noexec])
check("non-executable returns 126", code, 126)
check("non-executable explains itself", bool(err), True)

# -- warning dedupe ---------------------------------------------------------
pn.warn("same")
pn.warn("same")
pn.warn("other")
check("identical warnings collapse", pn.WARNINGS, {"same": 2, "other": 1})
pn.WARNINGS.clear()

# -- evidence ranking -------------------------------------------------------
# The per-hit list is truncated, so ordering decides what a reader sees. A weak
# hub match sorting above a shared file makes two PRs look merely co-located.
import io
import contextlib

shared = {"z/Shared.cls"}
hubfile = "a/Gateway.cls"
files = shared | {hubfile, "m/Mid.cls"}
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    pn.show_files(files, shared, {hubfile}, {hubfile: 196, "m/Mid.cls": 2}, cap=2)
lines = [l.strip() for l in buf.getvalue().splitlines() if l.strip()]
check("shared file ranks first", lines[0], "= Shared.cls")
check("non-hub outranks hub", lines[1], "~ Mid.cls")
check("truncation is disclosed", lines[-1], "… and 1 more")

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    pn.show_files({hubfile}, set(), {hubfile}, {hubfile: 196}, cap=4)
check("hub degree is shown", "hub: 196 files depend on it" in buf.getvalue(), True)

# -- no stub leaked into the module -----------------------------------------
check("pn.run restored after stubbing", pn.run is REAL_RUN, True)

# --------------------------------------------------------------------------
if FAILED:
    print(f"FAIL — {len(FAILED)} check(s)\n")
    for f in FAILED:
        print(f"  {f}\n")
    sys.exit(1)
print("ok — all checks passed")
