---
name: spec-review
description: Run a cold Gate-1 spec review against a GitHub work-item issue. Use when a GH issue body needs reviewing AS A SPEC (not as code, not as a build request) — "spec review", "Gate 1", "review the issue as a spec", "/spec-review <issue>". Spawns a fresh subagent that reads only the published issue, reports findings, and never implements.
allowed-tools: Bash, Read, Grep, Glob, Write, Agent
license: MIT
---

# Spec review (Gate 1)

Runs one cold pass over a GitHub work-item issue treated as the Software Design
Document. The reviewer is a fresh subagent invocation; it reads the published
issue body and reports findings. Nothing is built.

Throughout, **the Architect** means the human who owns the spec and declares the
gate green.

## Why a subagent and not this session

The session that authored the spec cannot review it. A fresh invocation is the
structural independence reset — a fresh window resets memory, but a separate
invocation is what establishes production independence. Never review a spec you
wrote in the same context.

## Inputs the reviewer gets, and nothing else

1. The issue number and the repo (`owner/name`).
2. **The tracker ticket ID, so it can read the SRS.** This gate checks that the
   SDD faithfully encodes the SRS, so withholding the SRS makes that
   uncheckable — and invites the reviewer to demand a Requirements section the
   house SDD skeleton deliberately does not have. The SRS is a source artifact,
   not deliberation.
3. The path to `CONSTITUTION.md` in the local checkout. If that checkout is a
   stale mirror, tell the reviewer to read it from `origin/main` instead.
4. The prompt below, verbatim.

It fetches both bodies itself. Do not paste them in, do not summarise them, and
do not mention what you think is wrong with either.

**Never pass prior-pass findings, your own reasoning, or the ticket's internal
rationale.** Those are the deliberation record. Feeding any of them back means
the pass returns your own conclusions instead of an independent read.

## Where the record lives

Keep two files per ticket, wherever your team keeps its work-item records:

- `work-item.md` — the spec body. The authoring surface.
- `spec-review.md` — every pass appended under a `## Pass N` heading, with the
  disposition written under each finding.

**Edit `work-item.md`, then push it. Never edit the issue body on GitHub
directly.** One direction only is what keeps the two from drifting.

```bash
gh issue edit <N> --repo <owner>/<name> --body-file <path>/work-item.md
```

## The loop

1. Run a pass (below). Append the raw output to `spec-review.md` under the next
   `## Pass N`.
2. Work the findings **one at a time with the Architect** — fix / accept with a
   stated reason / below the altitude fence. Write each disposition under its
   finding. Never revise the spec off a batch of findings unilaterally.
3. Apply the survivors to `work-item.md`, push to GitHub, run the next pass cold.
4. Converged when a pass returns zero findings against a body unchanged since a
   distinct reviewer last cleared it. Findings at this gate get **fixed**, not
   waived. The Architect declares green; never propose calling it green.

Do not post the review to the issue without the Architect's per-draft approval.

## Running a pass

Spawn one subagent with `run_in_background: false`. Restrict it to **read-only
tools**: `Bash(gh issue view:*)`, `Read`, `Grep`, `Glob`. No `Write`, no `Edit`.
With no write tool at all, an implementation attempt is structurally impossible
rather than merely forbidden, and no stray file lands in the repo. The review
comes back as the subagent's return text; you append it to `spec-review.md`.

Prompt, verbatim, substituting the issue number, repo, ticket ID, and
Constitution path:

---

You are reviewing GitHub issue #<N> in <repo> **as a specification**. You are not
a code reviewer and you are not the implementer. Nothing is built in this pass.

Fetch both artifacts yourself:
`gh issue view <N> --repo <repo>` — the SDD under review
the tracker ticket `<TICKET>` — the SRS it must faithfully encode

## What you are reviewing

The issue body is the Software Design Document: the technical contract a future
PR will implement. The house skeleton sections on `###`, not `##`: `Linear
Ticket Number`, `Work Type`, `Description`, `Architectural Notes`, and
`Acceptance Criteria`. There is deliberately no Requirements section — the
tracker ticket is the Software Requirements Specification, and requirements in
EARS form live there. Check that every SRS requirement is encoded and that no
acceptance criterion is ungoverned; do not ask the SDD to restate the SRS. Read it against `<constitution-path>` and
any ADR or design doc it links. You may read repository source **only** to verify
a factual claim the spec makes — that a named precedent class exists, that a
cited section says what the spec says it says, that a planned class name fits the
40-character limit. You may not read source to plan an implementation.

## Hard prohibitions

- Do NOT write, modify, or delete any repository file. Your single write is the
  review file named at the end.
- Do NOT write code, pseudo-code, method bodies, SOQL, or metadata XML anywhere,
  including inside a finding as an illustration.
- Do NOT open a pull request, push a branch, or post a comment.
- Do NOT propose an implementation approach. Where the spec has decided
  something, test whether the decision is stated well enough to build from. Do
  not offer a different decision.

## Hold the altitude

Many work-item issues open with a `Review scope / altitude` blockquote naming
the build-time mechanics held out of scope. **If one is present, honour it as
written** — findings below that fence are out of scope and must not be raised.

**If there is no such blockquote, apply the default fence below and say in your
Observations that the issue carries no explicit altitude statement.** Do not
infer a fence from the issue's contents, and do not treat its absence as
licence to review build mechanics. Most issues do not carry one, so this is the
common case, not the exception.

Fenced, so not review material: query-build paths, DML call shapes, assertion
helper choices, cron string internals, exact XML element form, and any other
coding of an already-decided contract.

In scope regardless of the fence: the behavioural contract, method signatures
and return types, security context, flag and state lifecycles, the acceptance
criteria, and the named deliverables.

One narrow exception. When a genuine deliverable is dressed as a mechanic ("the
Default CMDT record must carry explicit values or production reads null"), keep
the requirement and drop the mechanic. State it as a requirement the spec is
missing, never as the XML that would satisfy it.

## What to check

**Requirements.** Modally conformant: every requirement carries a capitalised
RFC 2119 keyword as clarified by RFC 8174 — MUST for an absolute requirement,
SHOULD where a justified deviation is possible, MAY where it is genuinely
discretionary. Prefer MUST over SHALL; they bind identically and MUST is the
plainer word. A lowercase *should*, *may*, *could*, or *might* binds nothing and
is a finding. Each requirement semantically unambiguous, testable without reading
code, and describing WHAT the system does rather than HOW it is built. No two
contradict each other.

**Completeness.** No missing stakeholder, non-functional requirement, or edge
case. A requirement the acceptance criteria do not cover, and an acceptance
criterion with no governing requirement, are both findings.

**Acceptance criteria.** Given / When / Then scenarios, not declarative
checkboxes. Grouped under the three confirmation categories, each in the right
one: a scenario a test proves does not belong under manual validation, and one
needing a human does not belong under automated. Each mechanically verifiable by
an engineer without interpretation.

**Architectural Notes.** Decisions, not restated requirements. Deep rationale
cited to the ADR rather than reproduced. A note that only repeats a requirement
is a finding; so is a note that has quietly become a draft implementation.

**External behaviour is flagged, not pinned.** Where the spec relies on the
behaviour of something not visible from the repo — a managed package, a host
API, a platform quirk — it must be marked as a reliance to verify against
reality, not asserted as a design pin. You cannot validate such a claim, so do
not reason about whether it is true. Flag any stated as settled fact.

**Non-contradiction with the Constitution.** The spec may not silently violate a
rule; if it must, the Constitution is amended first. A deliberate, explicitly
named deviation with a stated reason is not a finding. An unnamed one is.

**Housekeeping.** Planned class names within 40 characters. No tracker ID
destined to ship in committed code, comments, strings, or tests.

## Output

Return your review as your final message. Markdown, no wrapper tags. Write no
files.

**Verdict**: one of `Green — no findings` or `Findings to clear`

### Findings

Numbered. Each names the section of the issue it applies to, states the gap in
one or two sentences, and says what the spec would need to say instead. No code.
If none, write `_None_`.

### Observations

Non-blocking, same form. If none, write `_None_`.

Findings at this gate get fixed, not waived. Do not offer a verdict on whether
to proceed — that decision is the Architect's.

---

## Related

The cold-read independence rule, the finding lifecycle, and the rule against
tuning a trigger for a cleaner result are shared with the `senior-code-review`
skill in this plugin. What a compliant SDD contains, and the altitude fence the
reviewer honours, come from the team's SDD authoring guide.
