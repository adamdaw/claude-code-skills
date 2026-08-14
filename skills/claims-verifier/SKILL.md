---
name: claims-verifier
description: Run a cold adversarial pass over a document's claims. Use when a piece of writing needs its assertions torn at before it ships — "verify the claims", "claims check", "try to refute this", "adversarial claims review" — and before publishing anything that carries facts, statistics, or an argument chain. Spawns a fresh subagent that attempts to refute every factual and logical claim against the document's own evidence, verdicts each, and never edits. Not for code (that is senior-code-review's job) and not for opinion pieces that assert nothing.
allowed-tools: Bash, Read, Grep, Glob, Write, Agent
license: MIT
---

# Claims verifier

One cold adversarial pass over a document, claim by claim. The reviewer is a fresh
subagent invocation; it attempts to refute every factual and logical claim and returns a
verdict for each. Nothing is edited.

Partner to `senior-code-review`: that skill holds code to the craft, this one holds prose
to its evidence. The burden of proof sits with the document — a claim stands because the
document or its cited sources carry it, never because it sounds right.

Throughout, **the author** means the human who owns the document and declares the review
converged.

## Why a subagent and not this session

The session that drafted the document cannot review it. Asked to verify its own claims,
it re-derives the reasoning that produced them and reports the re-derivation as
confirmation — agreement that means nothing. A fresh invocation is the structural
independence reset. Never verify claims you drafted in the same context.

## Inputs the adversary gets, and nothing else

1. The document path.
2. The paths of the **local** sources the document cites, so the support can actually be
   checked. Withholding them turns every sourced claim into an unverifiable one and makes
   the pass worthless. Point at the files; the adversary reads them itself.
3. The prompt below, verbatim.

Do not paste the document in, do not summarise it, and do not mention what you think its
weak points are. **Never pass draft history, authorial intent, or prior-pass findings.**
Those are the deliberation record; feeding any of them back means the pass returns your
own conclusions instead of an independent read.

The adversary works offline. It reads the document and the local sources — nothing else.
A claim resting on a source that exists only on the web comes back UNVERIFIABLE, which is
the correct answer: fetching and verifying a primary source is the author's job, and no
adversary's confident paraphrase substitutes for it.

## Where the record lives

Keep `claims-review.md` beside the target document. Every pass is appended under a
`## Pass N` heading, with the disposition written under each finding. The document itself
is edited only by applying dispositioned survivors, never by the adversary.

## The loop

1. Run a pass (below). Append the raw output to `claims-review.md` under the next
   `## Pass N`.
2. Work the findings **one at a time with the author** — fix / accept with a stated
   reason / out of scope. Write each disposition under its finding. Never revise the
   document off a batch of findings unilaterally.
3. Every UNVERIFIABLE verdict gets a disposition too: the author fetches and verifies the
   source (outside this skill), or accepts the claim as unverified with a stated reason.
   An unverifiable claim nobody dispositioned is an open finding, not a pass.
4. Apply the survivors to the document, then run the next pass cold.
5. Converged when a pass returns zero findings against a document unchanged since a
   distinct cold invocation last cleared it. The author declares convergence; never
   propose calling it clean.

## Running a pass

Spawn one subagent with `run_in_background: false`. Restrict it to **read-only tools**:
`Read`, `Grep`, `Glob`. No `Bash`, no `Write`, no `Edit`, no network. With no write tool
at all, an edit to the document is structurally impossible rather than merely forbidden,
and with no network tool the offline fence holds itself. The review comes back as the
subagent's return text; you append it to `claims-review.md`.

Prompt, verbatim, substituting the document path and the cited-source paths:

---

You are attempting to **refute** the document at `<doc-path>`. You are not its editor,
not its summariser, and not its advocate. Nothing is rewritten in this pass.

Read the document, then read the local sources it cites: `<source-paths>`.

## What counts as a claim

Every factual or logical assertion the document makes: an empirical or statistical
statement, a causal claim, a derivation (a "therefore", a "so", a "which means"), a
definitional assertion, a stated reliance on external behaviour. Opinions, aesthetic
judgements, and normative stances are out of scope — unless one is phrased as empirical
fact, which is itself a finding.

The burden of proof is the document's. A claim is supported when the document or a cited
source carries the evidence at the claim's stated strength. Plausibility is not support.

## Procedure

1. **Enumerate** the claims in document order with stable IDs: C1, C2, …
2. **Classify** each: empirical/statistical · causal · logical derivation · definitional
   · external reliance.
3. **Attack** each by class:
   - **Internal consistency.** Hunt contradictions between claims, and between a claim
     and the document's own qualifications elsewhere. A bounded claim later used
     unbounded is a contradiction.
   - **Cited evidence.** Read the cited source directly. Support means the source says
     what the claim says, at the claim's strength — quote the supporting line, or fail
     it. A source that says something weaker, narrower, or merely adjacent is a
     mismatch, not support.
   - **Logic.** Premises stated, conclusion follows, no quantifier or scope slippage (a
     "some" quietly becoming "all", a specific case cited as the general rule). An
     argument whose conclusion needs an unstated premise names that premise in the
     finding.
   - **Numbers.** Recompute any figure derivable from other figures in the document or
     its sources. A number that cannot be reproduced is a finding.
4. **Verdict** each claim:
   - `SUPPORTED` — evidence present and it holds.
   - `UNSUPPORTED` — no evidence offered where evidence is needed.
   - `CONTRADICTED` — counter-evidence in the document or a source, a source mismatch,
     or invalid logic.
   - `UNVERIFIABLE` — support rests on a source not available locally. Flag it for the
     author to fetch and verify. Do not reason about whether it is probably true; you
     cannot check it, so do not weigh it.

## Hard prohibitions

- Do NOT edit, write, or delete any file. Your findings are your final message and
  nothing else.
- Do NOT access the network or claim knowledge of what an external source says.
- Do NOT redraft a claim or propose replacement wording. State what evidence would
  support the claim as written; the rewrite is the author's.
- Do NOT let a claim pass on your own background knowledge. If the support is not in the
  document or its sources, the verdict is UNSUPPORTED or UNVERIFIABLE, even when you
  believe the claim.

## Output

Return your review as your final message. Markdown, no wrapper tags. Write no files.

**Verdict**: one of `Clean — all claims supported` or `Findings to clear`

### Claim ledger

One row per claim: ID, the claim compressed to a line, class, verdict.

### Findings

Numbered, one per non-SUPPORTED claim. Each names the claim ID, quotes the claim as
written, states the refutation or the absence of support (with the source line quoted on
a mismatch), and says what evidence would support the claim. If none, write `_None_`.

### Observations

Non-blocking, same form — a hedge doing a claim's work, an opinion dressed as fact that
did not rise to a finding. If none, write `_None_`.

Findings at this review get dispositioned by the author, not waived by you. Do not offer
a verdict on whether the document should ship — that decision is the author's.

---

## Related

The cold-read independence rule, the context-free adversary, and the finding lifecycle
are shared with `spec-review` in this repo. The boundary with `senior-code-review` is the
artifact: code goes there, prose claims come here. The offline fence exists because
primary-source verification is the author's burden, and an adversary's confident
paraphrase of a source it never read is exactly the failure this skill exists to catch.
