#!/usr/bin/env python3
"""Mechanical loss-detector for a brevity pass.

Usage: cutcheck.py ORIGINAL.md EDITED.md [APPENDIX.md ...]

Everything here is decidable without judgement. Anything it flags is a *candidate*
loss -- a human or model still decides whether the loss mattered. Anything it does
not flag is genuinely not lost, which is the point: it keeps the model reviewers
focused on load-bearing-ness rather than on inventory.
"""
import os
import re
import sys
from collections import Counter

KEYWORDS = r"MUST NOT|MUST|SHALL NOT|SHALL|SHOULD NOT|SHOULD|REQUIRED|RECOMMENDED|MAY|OPTIONAL"
MODALS = r"\b(?:must not|must|shall not|shall|should not|should|may|required|recommended|optional)\b"
# Salesforce API names, class names, metadata types, fields -- tokens a reader copies.
TOKENS = r"\b\w+__(?:c|mdt|e|r)\b|\b[A-Z][a-zA-Z]+(?:Repo|Controller|Service|Resolver|Factory)\b|\bCXS-\d+|\bSAL-\d+|\bADR-\d{4}-\d{3}\b|\bPS[G]?_\w+\b"
# Figures: bare numbers with optional unit suffix. Facts hide in numbers.
NUMBERS = r"\b\d+(?:[.,:]\d+)?\s*(?:k|%|s|seconds|minutes|hours|days|rows|queries|teams|metrics|pages|words)?\b"


def read(path):
    with open(path) as fh:
        return fh.read()


def heading_level(text):
    """Shallowest heading level at or below h2 that the document actually uses.

    ADRs section on `##`; the house GitHub work-item skeleton sections on `###`.
    Hardcoding `## ` collapsed every issue body into a single "(preamble)" row,
    which silently disabled the per-section report on a document type this skill
    explicitly accepts.
    """
    levels = {len(m) for m in re.findall(r"^(#{2,6}) \S", text, re.M)}
    return min(levels) if levels else 2


def sections(text, level=None):
    if level is None:
        level = heading_level(text)
    marker = "#" * level + " "
    out, cur = {}, "(preamble)"
    out[cur] = []
    for line in text.splitlines():
        if line.startswith(marker):
            cur = line[len(marker):].strip()
            out.setdefault(cur, [])
        else:
            out[cur].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def words(text):
    return len(text.split())


def census(text, pattern, flags=0):
    return Counter(re.findall(pattern, text, flags))


def soft_modals(text):
    """Modals that are NOT the ALL-CAPS protected form.

    A case-insensitive census counts MUST as a lowercase modal, so protected
    keywords were listed in the promotion-candidate section -- as candidates for
    promotion to themselves. RFC 8174 makes capitalisation the whole signal, so
    the two censuses have to disagree about case or they measure the same thing.
    """
    found = re.findall(MODALS, text, re.I)
    return Counter(m for m in found if m != m.upper())


def report(orig_path, edit_path, appendix_paths):
    orig = read(orig_path)
    edited = read(edit_path)
    appendix = "\n".join(read(p) for p in appendix_paths)
    kept = edited + "\n" + appendix  # content that survived *somewhere*

    print("=" * 72)
    print("BUDGET")
    print("=" * 72)
    ow, ew, aw = words(orig), words(edited), words(appendix)
    print(f"original  {ow:6d} words  ~{ow/500:5.1f} pages")
    print(f"edited    {ew:6d} words  ~{ew/500:5.1f} pages   {'UNDER' if ew <= 6000 else 'OVER'} the 6,000-word / 12-page ceiling")
    if appendix_paths:
        print(f"appendix  {aw:6d} words  ~{aw/500:5.1f} pages   ({', '.join(appendix_paths)})")
    if ow:
        print(f"delta     {ew-ow:+6d} words  ({(ew-ow)/ow*100:+.1f}%)   "
              f"retained overall: {(ew+aw)/ow*100:.0f}%")
    else:
        print("delta     original is empty; no ratio to report")

    print()
    print("=" * 72)
    print("PER-SECTION")
    print("=" * 72)
    # One level for both sides: a pass that changed heading depth would
    # otherwise report every section as simultaneously missing and added.
    level = heading_level(orig)
    so, se = sections(orig, level), sections(edited, level)
    for name in so:
        a, b = words(so[name]), words(se.get(name, ""))
        flag = "  <-- SECTION MISSING" if name not in se else ""
        print(f"{name[:44]:46s} {a:5d} -> {b:5d}  ({b/500:4.1f}p){flag}")
    for name in se:
        if name not in so:
            print(f"{name[:44]:46s}     - -> {words(se[name]):5d}  <-- SECTION ADDED")

    print()
    print("=" * 72)
    print("NORMATIVE KEYWORDS (ALL-CAPS, RFC 2119/8174)")
    print("=" * 72)
    # Compared against `kept`, not `edited`: a keyword that moved intact into a
    # sibling design doc -- the escape hatch this skill prescribes -- was
    # otherwise reported as a lost requirement on every correct split.
    ko, ke = census(orig, KEYWORDS), census(kept, KEYWORDS)
    if not ko and not ke:
        print("none in either file -- guard passed trivially, protected nothing.")
        print("(pre-adoption doc; see lowercase modals below)")
    for k in sorted(set(ko) | set(ke)):
        mark = "  <-- CHANGED" if ko[k] != ke[k] else ""
        print(f"{k:14s} {ko[k]:3d} -> {ke[k]:3d}{mark}")

    print()
    print("=" * 72)
    print("LOWERCASE MODALS (candidate unpromoted requirements)")
    print("=" * 72)
    mo, me = soft_modals(orig), soft_modals(kept)
    for k in sorted(set(mo) | set(me)):
        delta = me[k] - mo[k]
        # Both directions matter. A drop may be a deleted requirement; an ADD may be a
        # requirement the pass invented, which is the same defect facing the other way.
        mark = ""
        if delta < 0:
            mark = f"  <-- {-delta} DROPPED (check for a deleted requirement)"
        elif delta > 0:
            mark = f"  <-- {delta} ADDED (check the pass did not invent binding force)"
        print(f"{k:14s} {mo[k]:3d} -> {me[k]:3d}{mark}")

    print()
    print("=" * 72)
    print("EXACT TOKENS PRESENT IN ORIGINAL, ABSENT FROM EDITED+APPENDIX")
    print("=" * 72)
    to, tk = set(re.findall(TOKENS, orig)), set(re.findall(TOKENS, kept))
    missing = sorted(to - tk)
    print(f"{len(missing)} missing of {len(to)} distinct")
    for t in missing:
        print(f"  {t}")

    print()
    print("=" * 72)
    print("FIGURES PRESENT IN ORIGINAL, ABSENT FROM EDITED+APPENDIX")
    print("=" * 72)
    no = set(x.strip() for x in re.findall(NUMBERS, orig))
    nk = set(x.strip() for x in re.findall(NUMBERS, kept))
    missing_n = sorted(no - nk)
    print(f"{len(missing_n)} missing of {len(no)} distinct")
    if missing_n:
        print("  " + ", ".join(missing_n))

    print()
    print("=" * 72)
    print("REGISTER: first-person / named-subject leakage into the edit")
    print("=" * 72)
    # Set CUTCHECK_NAMES to a |-separated list of teammate names to catch those too.
    names = os.environ.get("CUTCHECK_NAMES", "").strip()
    # Case-insensitive for everything except the pronoun "I", where a lowercase
    # match would hit stray list markers and algebra. This census used to be
    # fully case-sensitive, which missed "We sliced the epic" -- sentence-initial
    # first person, and the very example the guide gives as the register
    # violation to avoid.
    soft = "we|our|you|your" + (f"|{names}" if names else "")
    leak_i = rf"\b(?:{soft})\b"
    def leaks(text):
        # Fold case so "We" and "we" are one row. Summed, not dict-comprehended:
        # a comprehension keyed on k.lower() overwrites rather than adds, so a
        # doc using both spellings would under-count.
        folded = Counter()
        for word, n in census(text, leak_i, re.I).items():
            folded[word.lower()] += n
        folded.update(census(text, r"\bI\b"))
        return folded

    lo, le = leaks(orig), leaks(kept)
    for k in sorted(set(lo) | set(le)):
        mark = "  <-- INTRODUCED BY THE EDIT" if le[k] > lo[k] else ""
        print(f"{k:10s} {lo[k]:3d} -> {le[k]:3d}{mark}")
    if not le:
        print("clean -- no first-person or named-subject constructions in the edit")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    for path in sys.argv[1:]:
        if not os.path.isfile(path):
            sys.exit(f"cutcheck: no such file: {path}")
    report(sys.argv[1], sys.argv[2], sys.argv[3:])
