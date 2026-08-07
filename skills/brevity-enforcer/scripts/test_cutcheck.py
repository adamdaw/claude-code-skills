#!/usr/bin/env python3
"""Self-check for cutcheck.py. No framework, no network.

    python3 test_cutcheck.py

cutcheck exists to catch a brevity pass that quietly deletes a requirement, so
every case here is a way it could report "clean" on real damage, or report
damage on a correct edit. Both failure directions cost trust equally: a false
alarm on the prescribed split-to-sibling workflow trains the reader to ignore
the census that protects the contract.
"""
import contextlib
import io
import os
import sys
import tempfile
import types

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "cutcheck.py")

# Compiled from source text rather than imported: importlib honours __pycache__,
# and a stale .pyc silently tests code that is no longer on disk.
cc = types.ModuleType("cc")
cc.__file__ = SOURCE
with open(SOURCE) as fh:
    exec(compile(fh.read(), SOURCE, "exec"), cc.__dict__)

FAILED = []


def check(label, got, want):
    if got != want:
        FAILED.append(f"{label}\n    got:  {got!r}\n    want: {want!r}")


def run_report(orig, edited, *appendices):
    """cutcheck's stdout for these contents."""
    with tempfile.TemporaryDirectory() as td:
        paths = []
        for name, body in [("orig.md", orig), ("edited.md", edited)] + [
                (f"app{i}.md", a) for i, a in enumerate(appendices)]:
            p = os.path.join(td, name)
            with open(p, "w") as fh:
                fh.write(body)
            paths.append(p)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            cc.report(paths[0], paths[1], paths[2:])
        return buf.getvalue()


def section(out, title):
    """The lines of one report section."""
    lines, grab = [], False
    for line in out.splitlines():
        if line.startswith(title):
            grab = True
            continue
        if grab:
            if line.startswith("=") or not line.strip():
                if lines:
                    break
                continue
            lines.append(line.rstrip())
    return lines


# -- section splitting ------------------------------------------------------
check("splits on ## only",
      sorted(cc.sections("pre\n## A\nx\n### A.1\ny\n## B\nz")),
      ["(preamble)", "A", "B"])
check("subsection rolls into parent",
      cc.sections("## A\nx\n### A.1\ny")["A"].split(), ["x", "###", "A.1", "y"])
check("words counts whitespace-separated", cc.words("a  b\nc"), 3)

# -- heading level is detected, not assumed ---------------------------------
# ADRs section on "##"; the house GitHub work-item skeleton sections on "###".
# Hardcoding "## " collapsed a 4,280-word issue body into one "(preamble)" row.
check("h2 doc detected as level 2", cc.heading_level("# T\n## A\nx\n## B\ny"), 2)
check("h3-only doc detected as level 3",
      cc.heading_level("# T\n### A\nx\n### B\ny"), 3)
check("shallowest wins when both present",
      cc.heading_level("# T\n## A\n### A1\n## B"), 2)
check("no headings falls back to 2", cc.heading_level("just prose"), 2)
check("h1 alone does not count", cc.heading_level("# Title\nprose"), 2)
check("hash without a space is not a heading",
      cc.heading_level("# T\n##notaheading\n### Real\nx"), 3)

ISSUE = "### Linear Ticket\nABC-1\n### Description\nwords here\n### Acceptance Criteria\nmore\n"
check("h3 skeleton splits into its real sections",
      sorted(cc.sections(ISSUE)),
      ["(preamble)", "Acceptance Criteria", "Description", "Linear Ticket"])
issue_out = run_report(ISSUE, ISSUE)
check("per-section report is not one preamble row",
      "Description" in issue_out.split("PER-SECTION")[1].split("=" * 72)[1], True)

# Both sides must be split at the ORIGINAL's level. Detecting each side
# separately makes a renamed section read as one deleted plus one invented,
# which is a different and much louder claim than "it was renamed".
depth_change = run_report("# T\n## A\nx\n", "# T\n### B\ny\n")
check("edited side is split at the original's level",
      "SECTION ADDED" in depth_change, False)
check("and the original section still reports as missing",
      "SECTION MISSING" in depth_change, True)

# -- the ALL-CAPS census honours moved content ------------------------------
# The documented escape hatch moves detail to a sibling design doc. Comparing
# against `edited` alone reported every correct split as a lost requirement.
MOVED_ORIG = "# A\n## Context\nThe job MUST run.\n## Decision\nIt MUST retry.\n"
MOVED_EDIT = "# A\n## Context\nThe job MUST run.\n## Decision\nSee appendix.\n"
MOVED_APP = "# Appendix\nIt MUST retry.\n"
kw = section(run_report(MOVED_ORIG, MOVED_EDIT, MOVED_APP), "NORMATIVE KEYWORDS")
check("moved keyword is not a loss", [l for l in kw if "CHANGED" in l], [])
kw_nomove = section(run_report(MOVED_ORIG, MOVED_EDIT), "NORMATIVE KEYWORDS")
check("dropped keyword with no appendix IS a loss",
      any("CHANGED" in l for l in kw_nomove), True)

# -- softening is the damage this tool exists to catch ----------------------
SOFT_ORIG = "# A\n## Context\nRecords SHOULD NOT be shared.\n"
SOFT_EDIT = "# A\n## Context\nAvoid sharing records.\n"
check("softened keyword is flagged",
      any("CHANGED" in l for l in
          section(run_report(SOFT_ORIG, SOFT_EDIT), "NORMATIVE KEYWORDS")), True)

DECAP_EDIT = "# A\n## Context\nRecords should not be shared.\n"
check("decapitalised keyword is flagged",
      any("CHANGED" in l for l in
          section(run_report(SOFT_ORIG, DECAP_EDIT), "NORMATIVE KEYWORDS")), True)

# -- ALL-CAPS keywords are not lowercase modals ----------------------------
# A case-insensitive modal census listed protected keywords as candidates for
# promotion to themselves.
check("MUST is not a soft modal", cc.soft_modals("The job MUST run."), {})
check("lowercase must is", dict(cc.soft_modals("the job must run")), {"must": 1})
check("sentence-initial Must is",
      dict(cc.soft_modals("Must the job run?")), {"Must": 1})
check("mixed case counted once each",
      dict(cc.soft_modals("MUST must Must")), {"must": 1, "Must": 1})
check("multiword modal", dict(cc.soft_modals("it must not run")), {"must not": 1})

soft_sec = section(run_report("# A\n## C\nThe job MUST run and may retry.\n",
                              "# A\n## C\nThe job MUST run.\n"), "LOWERCASE MODALS")
check("a dropped soft modal is flagged",
      any("DROPPED" in l for l in soft_sec), True)
check("the ALL-CAPS keyword stays out of that section",
      any(l.startswith("MUST") for l in soft_sec), False)

# -- invented binding force is the same defect, reversed --------------------
check("an added soft modal is flagged",
      any("ADDED" in l for l in
          section(run_report("# A\n## C\nThe job runs.\n",
                             "# A\n## C\nThe job must run.\n"), "LOWERCASE MODALS")),
      True)

# -- tokens and figures ----------------------------------------------------
tok = run_report("# A\n## C\n`Rollup__mdt` and AccountRepo at 300 seconds.\n",
                 "# A\n## C\nSomething else.\n")
check("lost token reported", "Rollup__mdt" in tok, True)
check("lost class token reported", "AccountRepo" in tok, True)
check("lost figure reported", "300 seconds" in tok, True)

kept_tok = run_report("# A\n## C\n`Rollup__mdt` at 300 seconds.\n",
                      "# A\n## C\nSee appendix.\n",
                      "# App\n`Rollup__mdt` at 300 seconds.\n")
check("token moved to appendix is not lost",
      "0 missing" in kept_tok.split("EXACT TOKENS")[1].split("=")[0] or
      "0 missing" in kept_tok.split("EXACT TOKENS")[1][:200], True)

# -- register leak ---------------------------------------------------------
reg = run_report("# A\n## C\nThe epic is decomposed.\n",
                 "# A\n## C\nWe sliced the epic.\n")
check("first-person introduced by the edit is flagged",
      "INTRODUCED BY THE EDIT" in reg, True)
clean = run_report("# A\n## C\nThe epic is decomposed.\n",
                   "# A\n## C\nThe epic has 13 slices.\n")
check("passive edit reports clean", "clean --" in clean, True)

os.environ["CUTCHECK_NAMES"] = "Ada|Grace"
named = run_report("# A\n## C\nThe decision stands.\n",
                   "# A\n## C\nAda decided this.\n")
check("configured name is flagged", "INTRODUCED BY THE EDIT" in named, True)
del os.environ["CUTCHECK_NAMES"]
unnamed = run_report("# A\n## C\nThe decision stands.\n",
                     "# A\n## C\nAda decided this.\n")
check("names are not flagged unless configured",
      "INTRODUCED BY THE EDIT" in unnamed, False)

# -- register census details -----------------------------------------------
# Each of these survived a mutation run: verified once by hand, never pinned.
mixed = run_report("# A\n## C\nThe work stands.\n",
                   "# A\n## C\nWe did it and we agreed and WE shipped.\n")
import re as _re


def census_row(out, word):
    """(before, after) for one census row, ignoring any trailing marker."""
    for line in out.splitlines():
        m = _re.match(rf"^{_re.escape(word)}\s+(\d+)\s*->\s*(\d+)", line)
        if m:
            return int(m.group(1)), int(m.group(2))
    return None


check("case variants sum rather than overwrite",
      census_row(mixed, "we"), (0, 3))

check("first-person 'I' is counted",
      "INTRODUCED BY THE EDIT" in run_report("# A\n## C\nThe work stands.\n",
                                             "# A\n## C\nI decided this.\n"), True)

# Content that moved to a sibling doc is not a new register leak.
moved_reg = run_report("# A\n## C\nWe agreed the plan.\n",
                       "# A\n## C\nSee appendix.\n",
                       "# App\nWe agreed the plan.\n")
check("register leak already in the original is not 'introduced'",
      "INTRODUCED BY THE EDIT" in moved_reg, False)

# The sibling doc is part of the pass's output, so first person introduced
# *there* is the same violation. Scoping this census to `edited` alone would
# miss it -- and that is where displaced content lands.
app_leak = run_report("# A\n## C\nThe plan is agreed.\n",
                      "# A\n## C\nSee appendix.\n",
                      "# App\nWe agreed the plan.\n")
check("first person introduced in the appendix is flagged",
      "INTRODUCED BY THE EDIT" in app_leak, True)
check("and it is counted there", census_row(app_leak, "we"), (0, 1))

# -- budget line -----------------------------------------------------------
budget = run_report("# A\n## C\n" + "word " * 100, "# A\n## C\n" + "word " * 50)
check("delta percentage is reported", "delta" in budget and "%" in budget, True)
check("retention is reported", "retained overall" in budget, True)
check("ceiling verdict is reported",
      "UNDER the 6,000-word" in budget, True)
over = run_report("# A\n## C\nx\n", "# A\n## C\n" + "word " * 6100)
check("over-ceiling is reported", "OVER the 6,000-word" in over, True)

# -- section movement ------------------------------------------------------
moved = run_report("# A\n## Keep\nx\n## Gone\ny\n", "# A\n## Keep\nx\n## New\nz\n")
check("removed section reported", "SECTION MISSING" in moved, True)
check("added section reported", "SECTION ADDED" in moved, True)

# -- crash paths -----------------------------------------------------------
# An empty original divided by zero; a missing file raised before reporting.
check("empty original does not crash",
      "no ratio to report" in run_report("", "# A\n## C\nx\n"), True)
check("pre-adoption doc says the guard protected nothing",
      "protected nothing" in run_report("# A\n## C\nx\n", "# A\n## C\ny\n"), True)

# --------------------------------------------------------------------------
if FAILED:
    print(f"FAIL — {len(FAILED)} check(s)\n")
    for f in FAILED:
        print(f"  {f}\n")
    sys.exit(1)
print("ok — all checks passed")
