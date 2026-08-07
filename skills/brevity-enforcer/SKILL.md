---
name: brevity-enforcer
description: Use when someone points at a named durable doc (ADR, spec, plan, design doc, runbook, GH issue body) and says it is too long, over the page cap, bloated, or asks to cut it down, trim it, or fit it in 12 pages — and before publishing any ADR, so the length check happens ahead of review. Enforces the 12-page ceiling and per-section targets without softening an RFC 2119 keyword or flipping the register. Not for PR review comments or chat replies, and not for docs nobody asked about.
allowed-tools: Bash, Read, Edit, Grep, Glob
license: MIT
---

# Brevity enforcer

Shortens one named durable doc. It removes words, not decisions. Every pass has to survive
one question: after the cut, can a reviewer still sign off on the same thing?

This skill is self-contained — the standards it enforces are stated here rather than
delegated to a doc elsewhere. Where a repository carries its own ADR authoring guide, that
guide wins and this file is the working procedure under it.

## Invoked deliberately, on a named doc

Committed plan and design docs are a feature, and doc volume is never a review finding. This
skill runs when someone points at a specific file and asks for a cut. It is not a roving
critic and it does not go looking for long docs to trim.

If the doc is already inside budget and every section is inside its target, say so and cut
nothing. A zero-edit pass is a valid, honest result. If it is inside budget but a section is
over target, tighten that section in place and read the ceiling rule below before
restructuring anything.

## Two things a cut must never break

### 1. Register is set by doc type, not by the brevity advice

Generic brevity advice says "prefer the active voice." Durable governance docs are
deliberately the opposite, and flipping them is worse damage than the length ever was.

| Doc type                                      | Register                                                                                   |
| --------------------------------------------- | ------------------------------------------------------------------------------------------ |
| ADRs, durable specs, design docs, slice plans | Formal, technical, **passive, impersonal**. No personal name as the subject of a decision. |
| How-tos, runbooks, reference docs, guides     | Direct and active. Imperative for instructions.                                            |
| Chat, PR and ticket comments                  | Active.                                                                                     |

Decide the register from the doc type before the first edit, and hold it for the whole pass.
Shortening a sentence is not license to rewrite it into a different voice.

Right — shorter, still passive:

> It is worth noting that the rollup engine, as it is currently configured, does not support cursor resumption.

> The rollup engine does not support cursor resumption.

Wrong — shorter, register flipped:

> The epic is decomposed into 13 slices.

> ✗ We sliced the epic into 13 pieces.

Provenance and attribution belong in metadata or a dedicated provenance note, not woven
through the prose. Reserve names for genuine role assignments the doc needs, such as a
sign-off owner, and never for narrating who chose what.

### 2. Normative keywords are protected tokens

Requirements are written with the RFC 2119 keywords as clarified by RFC 8174, capitalised,
across ADRs, specs, plans, and issues. The ALL-CAPS forms — MUST, MUST NOT, REQUIRED, SHALL,
SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY, OPTIONAL — carry the
contract. They are the reason the doc is enforceable at all, so a brevity pass copies them
through untouched.

| Keyword | Meaning |
| --- | --- |
| MUST / REQUIRED | An absolute requirement. Non-compliance is a defect. |
| MUST NOT | An absolute prohibition. |
| SHOULD / RECOMMENDED | A valid reason to deviate may exist; the full implications must be weighed and the deviation justified. |
| SHOULD NOT / NOT RECOMMENDED | Likewise, in the negative. |
| MAY / OPTIONAL | Genuinely discretionary. An implementer choosing either way is compliant. |

Never soften, paraphrase, downgrade, or delete one. Never "simplify" SHALL to *will* or to a
lowercase *must* — RFC 8174 makes the capitalisation the thing that signals normativity, so
decapitalising a keyword silently converts a requirement into prose. Never merge two
requirements that use different keywords into one sentence; MUST and SHOULD are different
promises.

Wrong, and this is the failure mode that does real damage:

> Records SHOULD NOT be shared to the Retail Manager role.

> ✗ Avoid sharing records to the Retail Manager role.

That cut destroyed a normative keyword *and* flipped the register in six words.

**Prefer MUST over SHALL when introducing or converting a keyword.** They bind identically
under RFC 2119, and MUST is the plainer word, so it satisfies the Simplified Technical
English rule below at the same time. This is a preference for new text, not a licence to
rewrite: an existing SHALL is a protected token like any other and stays put unless the pass
is explicitly a keyword-conversion pass.

Any doc that uses the keywords carries the RFC 8174 boilerplate verbatim, once, near the top
— in an ADR, immediately under the metadata table and above `## Context`. It is quoted
verbatim and never edited, so it keeps SHALL regardless. Never cut it for length:

> The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
> "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document
> are to be interpreted as described in BCP 14 [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
> [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174) when, and only when, they appear in
> all capitals, as shown here.

Consequences, Risks, and Alternatives sections are descriptive rather than normative. They
record what follows from a decision, not what an implementer must do, so they generally carry
no keywords. The Decision section is where the contract lives.

### Lowercase modals are not automatically fair game

RFC 8174 makes capitalisation the signal, so a lowercase *must* / *should* / *may* is not
protected the way the keyword is. That does not make it free to delete. Plenty of docs predate
keyword adoption and carry their requirements in ordinary prose, so a lowercase modal is
sometimes a hedge and sometimes a contract wearing normal clothes.

Classify each one before touching it:

- **Descriptive** — narrates what can happen. "A straggler *can* land minutes after the last
  call." Cut, reword, or keep on brevity grounds like any other prose.
- **Requirement in disguise** — binds an implementer or constrains the build. "Prune and
  backfill *must not* fight." Leave the sentence intact and list it in the report as a
  promotion candidate with the ALL-CAPS form it would take.

Propose the promotion; do not apply it. A brevity pass earns trust by changing length and
nothing else — promoting a modal changes the doc's binding force, and that is an authoring
decision for the doc's owner, not a side effect of a trim. The report makes the candidates
easy to accept in a follow-up edit.

The test for "requirement in disguise": if an implementer could ignore the sentence and still
claim compliance, it is descriptive. If ignoring it would breach the decision, it is a
requirement and the doc is currently under-specifying it.

## What to hunt

Read a section, ask what the reviewer actually needs from it, then cut in this order:

- **Throat-clearing.** "It is worth noting that", "As mentioned above", "It should be
  emphasised that", "In order to". The sentence almost always starts at the verb.
- **Adverbs and intensifiers.** significantly, notably, fairly, quite, very, essentially,
  ultimately, simply. If the claim needs the adverb, the claim needs a number instead.
- **Hedges** that are not normative keywords and not requirements in disguise: arguably,
  generally speaking, it seems, in most cases. Either the doc knows or it does not; say which.
  Check a lowercase modal against the classification above before cutting it — the
  hedge-hunting instinct is exactly what deletes an unpromoted requirement.
- **Restatement.** Prose that narrates a table, a code block, or the section above it. Delete
  the prose, keep the table.
- **The long word.** utilize → use, prior to → before, at this point in time → now, in the
  event that → if, is able to → can, commence → start.
- **The two-comma sentence.** One idea per paragraph, one job per sentence. Split it.
- **The long noun cluster.** Three words maximum. "Scratch org definition feature flag"
  becomes "the feature flag in the scratch org definition" — longer in words, shorter to
  parse, and it forces the relationship to be stated rather than guessed.
- **The elaborate tense.** Simple present or simple past unless the meaning needs otherwise.
  "Will have been deployed" is almost always "is deployed".
- **The synonym drift.** One term per thing, every time. A doc that says "the record", then
  "the row", then "the entry" reads as three things and costs the reader a reconciliation on
  every switch. Pick the doc's own term and make it uniform; note the substitutions in the
  report, because a term change can look like a semantic change.
- **Decision archaeology.** How the decision was reached, who raised what, which draft came
  first. Provenance belongs in metadata or the session log, not the prose.

The hunt list above is the working reading of **ASD-STE100 (Simplified Technical English)**,
which is the house standard for all prose and does not apply to code. Two carve-outs matter
here. STE's active-voice default is scoped by doc type, per §1 above — durable governance docs
stay passive. And technical names, proper nouns, and code identifiers are never plain-worded:
`RollupControl__mdt`, `Territory2` and ASD-STE100 itself are protected tokens in the same way
normative keywords are.

Then delete the favourite paragraph. The passage the author is proudest of is the first
suspect precisely because it survived earlier edits on affection rather than load.

Target at least a 10% word cut on any pass — that much is nearly always available without
losing a fact. When the doc is over budget, cut until it is under, and use the escape hatch
below rather than compressing a section past the point where it still decides something.

## What looks cuttable but isn't

Every item in the hunt list above has a lookalike that carries weight. These are the cuts that
survive a careful pass and still do damage, because the sentence genuinely reads like filler
right up until you ask what stops being true without it.

- **A sentence that bounds a claim made elsewhere.** "The DST-correctness claim applies to the
  hourly path and to rows computed under their effective-dated hours." It scans as
  restatement. It is the only thing stopping an unqualified guarantee two sections away from
  covering rows the doc elsewhere admits are wrong. Before cutting a sentence that starts
  *this applies to* / *this holds for* / *this is limited to*, find the claim it bounds and
  check whether that claim is still safe unbounded.
- **The generalisation a specific rule instantiates.** "A ratio is never shown over a window
  where one side has no coverage" alongside the concrete rule that implements it. The concrete
  rule reads sufficient. It isn't: the generalisation is what extends to the next ratio nobody
  has built yet.
- **The second half of a two-part reason.** "…because it would re-inflate the row count the
  horizon bounds (and would be silently re-pruned again)." The first reason justifies the
  rule; the second is what defeats the person arguing for an exception.
- **Enumerated cases that read as a doublet.** "absent **or zero** handled counts" → the guard
  written from the shortened version handles null and still divides by zero. Two nouns joined
  by *or* are usually two cases, not one idea said twice.
- **A scope word inside a compound.** "Migration/rollback" → "rollback" quietly drops forward
  migration from the rule. "Drop the object/rows" → "drop the rows" removes the sanction to
  drop the object. Compounds are cheap to trim and expensive to be wrong about.
- **The negative half of a contrast.** "Bounded only by how far presence records are retained,
  **not by the team-key stamp**." "Verified against the seeded metric rows, **not the wider
  `Aggregation_Function__c` picklist**." Keeping only the positive half leaves a sentence that
  reads complete, which is why this one survives careful passes. But the "not Y" half is
  usually the whole reason the sentence exists: it pre-empts one specific wrong inference the
  reader was about to make. Ask what mistake the negative is blocking. If a reasonable
  implementer would make that mistake without it, it stays.
- **Where a displaced decision lives.** "The current channel ID is a config value recorded in
  the digest slice, not in this ADR." "The refinement should reconcile this separately." These
  read as slice-ownership boilerplate and are the opposite: they are the pointers that keep a
  deferred item owned. An open item whose owner is deleted does not become closed, it becomes
  lost — and this skill's own escape hatch depends on exactly this kind of sentence surviving.

The common test: ask what becomes *unknowable* or *arguable* if the sentence goes. If the
answer is "nothing, it was said better above," cut it. If the answer names a person who would
now decide differently, keep it.

## What never gets cut

- Any ALL-CAPS normative keyword, the requirement it governs, and the RFC 8174 boilerplate.
- **Consequences and Risks reasoning.** Those tables are where the load-bearing decisions end
  up after adversarial teardown. Length there is not bloat. Tighten the wording of a cell; do
  not drop a row, and do not collapse two risks into one.
- Acceptance criteria, contract matrices, field and API names, exact tokens the reader copies.
- Anything the doc is the only record of. If deleting it loses the fact, it moves — see below
  — it does not disappear.

## The ceiling decides how far restructuring goes

Two different things can be wrong with a doc, and they license different amounts of work.

**Over the ceiling.** Cut until it is under, and split out a sibling design doc where the
detail needs somewhere to go. The doc has to shrink and there is no way around it.

**Under the ceiling but breaching per-section targets.** Tighten in place — throat-clearing,
restatement, adverbs, the compression of a 24-sentence subsection into fewer, denser
sentences. That is pure gain and produces no new file. But do **not** create a sibling design
doc to hit a per-section target on a doc that is already compliant. Report the breach, size
the move ("bringing Decision §3 inside its target means relocating ~1,400 words"), and let the
author call it.

The reason is that a split is not free the way a trim is. If the ceiling exists to bound what
a reviewer reads before signing off, splitting a compliant doc raises the total: a 9.7-page
ADR becomes a 5.4-page ADR plus a 5.1-page design doc, and the reviewer now reads 10.5 pages
across two files instead of 9.7 across one. That can still be the right call — a sprawling
Decision section is genuinely harder to review than a long one — but it is a structural change
to how the work is documented, which is the author's decision and not a side effect of asking
for a trim.

Same instinct as the promotion candidates: propose the change that alters shape, apply only
the change that removes words.

## Where displaced content goes

Cutting is not discarding. Detail that must survive moves to a sibling design doc the ADR
references.

Do the move in the same pass. Write the sibling doc, put the displaced content in it whole,
and add a bare link under References. A cut that leaves a dangling reference to a doc nobody
wrote is worse than the original length.

The sibling lands wherever the parent doc lives — beside it, sharing its path convention. In
the SalesforceDX repo that means specs at `docs/specs/YYYY-MM-DD-<topic>-design.md` and plans
at `docs/plans/YYYY-MM-DD-<feature>.md`. A doc drafted outside the repo gets a sibling beside
it and a bare filename in References; note in the report that the reference needs the repo
prefix if the pair later moves into the repo, since a link that resolves in one location and
not the other is the failure this causes.

## Budget and per-section targets

ADRs have a hard ceiling of **12 pages**. Markdown is not paginated, so the check uses a
word-count proxy of **~500 words per page → 6,000 words**. Measure with `wc -w`, note that
tables and code blocks inflate the count a little, and report the number rather than arguing
with it.

| Section                    | Target                                              |
| -------------------------- | --------------------------------------------------- |
| Context                    | ~150–250 words, only facts the Decision binds to     |
| Decision (each subsection) | ~3–5 sentences; implementation detail moves out      |
| Positive / Negative        | one-line bullets, no "this means that…" expansion    |
| Risks and Mitigations      | table, one row per risk, no prose                    |
| Alternatives Considered    | one line each + "Rejected because…"                  |
| References                 | bare paths and links                                 |

Measure per section:

```bash
awk '/^## /{s=$0; order[++n]=s; next} s!=""{c[s]+=NF} END{for(i=1;i<=n;i++) printf "%-42s %5d words  ~%.1f pages\n", order[i], c[order[i]], c[order[i]]/500}' FILE.md
```

## Run the checker — do not eyeball this

`scripts/cutcheck.py` does the measuring, the keyword census, the modal diff, and the
token/figure inventory in one pass. Run it after the cut, before writing the report:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/brevity-enforcer/scripts/cutcheck.py" ORIGINAL.md EDITED.md [SIBLING-DESIGN-DOC.md ...]
```

It compares against edited **plus** every sibling doc you passed, so content that legitimately
moved does not read as a loss. Everything it flags is a candidate; you still decide whether
the loss mattered. Everything it does not flag is genuinely not lost.

Run it even when you are confident, and especially then. A pass that watches for modal
flattening while cutting will still miss one — the attention that is shortening a sentence is
not the attention that notices its verb stopped binding. On the run that produced this
guidance the editor caught and restored nine flattened modals by hand and missed a tenth; the
count came out of the script, not the vigilance. Treat the modal-diff line as a gate: every
dropped modal needs an explanation in the report or a restoration in the text.

An empty ALL-CAPS census plus a long lowercase list is the signature of a doc written before
keyword adoption. Say so in the report — the keyword guard passed trivially on that doc and
protected nothing, which is worth knowing.

The register check greps for first-person and named-subject leakage, case-insensitively
except for the pronoun "I". It defaults to pronouns only; set `CUTCHECK_NAMES` to a
`|`-separated list of your team's names to catch those too. It reads the sibling docs as well
as the edit, because first person introduced in displaced content is the same violation.

Verify the checker itself with `python3 scripts/test_cutcheck.py` — no framework, no network.
It is mutation-tested: seventeen deliberate breakages, all seventeen caught. Three real
defects came out of writing it, all of which had been shipping silently:

- The ALL-CAPS keyword census compared against the edit alone, ignoring the sibling docs. So
  every correct use of the escape hatch below reported a **lost requirement** — the one
  finding the tool exists to produce, fired on the workflow this guide prescribes.
- `MUST` was counted as a lowercase modal, because the modal census was case-insensitive.
  Protected keywords appeared in the promotion-candidate list as candidates for promotion to
  themselves.
- The register census was case-sensitive, so "We sliced the epic" — the exact register
  violation shown as wrong in §1 above — was invisible to it.

## Sequence

1. Confirm which file. Identify the doc type and therefore the register.
2. Read any ADR authoring guide the repository carries, then the whole doc.
3. Measure: run `scripts/cutcheck.py` against the untouched file (pass it twice) to bank the
   starting numbers. Pass every sibling doc you create to the final run, or content that
   legitimately moved reads as lost.
4. Cut section by section against the targets. Move, do not drop, anything load-bearing.
   Classify each lowercase modal before cutting it; collect the promotion candidates.
5. Re-run `scripts/cutcheck.py` with the edit and any sibling docs. Account for every dropped
   modal and every missing token or figure before reporting — restore, or explain.
6. Report, show the diff, and stop. Do not commit. Landing the cut is the doc owner's call,
   and so is accepting any promotion candidate.

## Report format

Use this shape:

```markdown
## Brevity pass — <file>

**Budget:** 7,400 → 5,600 words (~14.8 → ~11.2 pages). Under the 12-page ceiling. ✅

| Section      | Before | After | Target      | Status |
| ------------ | ------ | ----- | ----------- | ------ |
| Context      | 640    | 220   | 150–250     | ✅     |
| Decision     | 2,100  | 1,450 | 3–5 sent/ss | ✅     |
| Consequences | 1,900  | 1,780 | bullets     | ✅     |
| ...          |        |       |             |        |

**Cut:** throat-clearing openers across Context and Decision; the narration duplicating
the risk table; adverbs throughout; the three-paragraph justification in Alternatives.

**Moved out:** the SOQL and cron detail from Decision §3 → `docs/specs/2026-08-06-...-design.md`,
linked under References.

**Register:** passive impersonal throughout, unchanged.

**Normative keywords:** census identical before and after —
MUST 7, MUST NOT 2, SHALL 1, SHOULD 4, MAY 3. No keyword softened, moved, or deleted. ✅

**Promotion candidates — not applied (3).** Lowercase modals that read as requirements
rather than description. Left exactly as written; promoting them is a separate call.

| Quoted as written | Would become | Location |
| ----------------- | ------------ | -------- |
| "prune and backfill must not fight either" | MUST NOT | Decision §Retention |
| "a metric later seeded with either shape needs a component added here first" | REQUIRED | Decision §Spine |
| "the per-team abandon figure is either omitted or annotated as non-summable" | MUST | Digest |

Descriptive lowercase modals left as prose (9): "could fall on the adjacent civil date",
"can land minutes after the last call", …
```

If a section could not be brought inside its target without losing a decision, say so
explicitly and name what is holding the words. An honest overage beats a quiet gutting.
