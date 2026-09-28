# Verifying claims: a guide

The V-guide: a checklist for checking whether a claim holds, in your own writing or anyone else's, and the steps of a claims audit. Cite sections as "V-guide §1 (Fluency is not authority)". For the reasoning, see *On Verifying Claims*, which is a principles outline for now; the essay isn't written yet. The `Essay:` line under each section cites the outline's principles by number.

A claim is anything a piece of writing asserts that could be true or false. A source is the work a claim rests on. A claims audit is the full check in §11: an independent reader assigns each claim a verdict, and the author works each finding. The [`claims-verifier`](../skills/claims-verifier/SKILL.md) skill is one agent form of it; the steps here don't depend on the skill.

## 1. Fluency is not authority

Essay: *On Verifying Claims* P1.

- How well a claim is put, and how confident its source sounds, is not evidence that it's true.
- This holds for every claimant: a model, a colleague, a published author and yourself.
- Your own agreement isn't evidence either. A claim that seems obviously right still needs what §4 asks of it.
- When you check someone else's claims, set aside what you already believe. Belief neither passes a claim nor fails it: without support from its sources or a valid derivation (§6), the claim is unsupported even if you think it's true, and present support stands even if you doubt it.

## 2. Match the check to the stakes

Essay: *On Verifying Claims*, none. This is a guide rule, not a principle: the rules in §1 and §3 to §10 always hold; the stakes decide how much of the procedure a piece of work gets.

| The work | The check |
| --- | --- |
| Published writing, or anything high-stakes, that carries facts, figures or an argument | The full claims audit (§11). |
| Writing that makes claims but isn't published or high-stakes, including narrative pieces such as a retrospective or a diary | The lighter check: check your own sources (§4, §5) and flag what you couldn't check (§8), then have someone else read the claims the piece depends on (§9). |
| Code, and the claims in a PR body | Code review, which treats the ticket and the PR body as claims to verify: R-guide §4 (Reading order). For code you write, W-guide §10 (Code that goes out under your name). |
| Pure opinion, preference or a value judgement that asserts nothing checkable | No check; there is no claim to verify (§3). |

- Where a piece fits more than one row, the first row that fits wins. A published diary gets the full audit.
- A full audit of a narrative piece is loud by design, because it flags every unsourced claim. Expect that noise when a narrative piece is published.
- What a full audit costs depends on how it's run. Weigh the stakes, not the cost of one tool.

## 3. Find the claims

Essay: *On Verifying Claims* P2.

- List every factual or logical assertion the writing makes, not only the ones stated outright. What makes something a claim is its checkable content, not how it's phrased.
- Walk these kinds over the text.

| Kind | Example of what it carries |
| --- | --- |
| **Stated** | A figure, a causal claim, a derivation, a prediction, a statement about how a term is used elsewhere. |
| **Presupposed** | "When throughput doubled, we…" asserts that throughput doubled. |
| **Relational** | "X rose while Y fell" asserts that they happened together. |
| **Invited** | Two facts placed side by side so the reader draws the inference: "We shipped the fix in May. Churn fell in June." A thesis sentence or a takeaway line does the same. |
| **Quoted** | A quotation the argument leans on. If later claims depend on the quoted content being true, it's a claim, not just a report of what someone said. |
| **Wrapped** | A rhetorical question, or figures in a code block used as evidence. |
| **Cross-reference** | "See §4" or a pointer to another document asserts that the target says what the pointer claims. |

- A quotation doesn't launder a claim. Putting a load-bearing assertion in someone else's mouth still makes it the writing's claim.
- Leave out value judgements, preferences and pleasantries with nothing checkable in them, and the byline, date and version line. A checkable assertion inside a bio or a changelog line is still a claim.
- Split a sentence that makes several independently checkable claims, and check each.

## 4. Every claim needs a source or a derivation

Essay: *On Verifying Claims* P2; P8 for derivations.

- A claim holds when a source carries it, or when it follows validly from premises that are themselves supported (§6). Otherwise flag it.
- Flag it even when it's common knowledge. The claim carries the burden; a reader's familiarity with it doesn't.
- The writing's own bare assertions are not evidence for its other claims. Restating a claim in a table or a summary doesn't support it.
- A citation supports the claims in the block it sits in: the paragraph, list item, table cell or caption. A footnote attaches to the block that holds its marker, not to the note.
- Where the writing sets a different scope, follow it. "Sources for this section" covers the section; a citation the writing ties to one sentence covers only that sentence.
- Support doesn't travel past that scope. A later passage that echoes the claim without the citation isn't covered by it. Don't infer a citation the writing doesn't make, and don't widen a narrow one.

## 5. Read the primary source yourself

Essay: *On Verifying Claims* P3.

- Check a claim against the work it rests on, not against a summary of it: a model's, a search tool's, or another author's citation.
- For code, the primary source is the documentation or a real call. For prose, it's the work itself, in a copy you can check.
- Match each quotation word for word against a copy of the work, not a remembered wording.
- Read the whole source, including its own limits. A line the source qualifies or retracts elsewhere supports only the qualified form.
- The source must itself report something: evidence, a derivation, or a first-hand account. A first-hand account supports only claims about the person's own experience. A source that only restates the claim, or only cites another work for it, supports nothing; follow the citation to the work that reports.
- Confirm that what you're reading is the work cited. A file that quotes the cited work in its bibliography is not that work.
- If you wrote the claim, this check is still yours to do. It isn't the confirmation §9 asks for.

## 6. Some claims are checked by reasoning

Essay: *On Verifying Claims* P8.

- Some claims are verified by deriving them: a proof, a valid inference from premises you accept, a calculation, or a check anyone can rerun, such as a test or a real call. They need no appeal to a source.
- Each premise the derivation depends on is itself a claim, and needs its own grounds under §4.
- Write out the steps so a reader can follow and check them. An unexplained jump doesn't count as a derivation.
- If the argument only goes through with an unstated premise, the conclusion is unsupported until that premise is named and supported.
- Watch for scope slipping between steps: a "some" that becomes "all", or a bounded claim later used without its bound.
- A conclusion is no stronger than its weakest premise. If a premise is only suggested by the evidence, the conclusion can be at most a suggestion, unless a stated step makes the stronger conclusion follow.
- Recompute every figure you can derive from figures in the writing or its sources.
- A chain of claims that leads back to itself supports nothing.
- A rerunnable check counts only if it could have failed. A test you have never seen fail proves nothing; see *On Testing Code* P1 and T-guide §2 (Choose the kind of test).
- Know the limits. A valid argument from a false premise proves nothing about the world, and a correct proof of the wrong statement proves the wrong thing. Check that the statement proved is the claim made.

## 7. Shrink the claim to fit the source

Essay: *On Verifying Claims* P4.

- A source supports a claim only as far as it goes. Where it supports a weaker or narrower claim, the claim shrinks to fit; never stretch the source.
- Match the kind of evidence before its strength. Correlation doesn't carry a causal claim. In one of the examples below, a simulation was cited as evidence about how people behave: the wrong kind of evidence for that claim. Hedging a causal claim ("the data suggest the cache caused it") doesn't change its kind.
- Tell the two kinds of hedge apart. "I believe" or "I suspect" states the writer's attitude: check the claim underneath. "Suggests", "probably" or "almost certainly" states the strength of the evidence: the source must carry that strength and no less.
- Read a figure at the precision it's written. "47%" isn't carried by 42%; "20 engineers" means 20. A loosened figure ("about 50%") still has limits, and "never" or "all" is a figure too.
- Where the source supports a weaker claim, the author writes the weaker claim. A reviewer quotes what the source does say and stops there.
- Examples of the drift this catches, from real cases with the details removed:
  - An early survey of an idea was cited as its origin.
  - A paper was cited for a claim it never made; another was credited to one of its two authors, and its simulation cited as evidence about people.
  - A writer argued a point for one kind of work, and the draft cited the writer for all kinds. The fix stated the wider use as the draft's own extension.
  - An analogy was credited to a writer who never draws it; it was the essayist's own.

## 8. Say what you verified and what you're assuming

Essay: *On Verifying Claims* P5.

- Mark what you checked, what you inferred, and what you couldn't check. Keep observations, inferences and unknowns distinct.
- Put the mark where the reader will see it: in the sentence, a footnote, or the PR body. A note in a comment that doesn't render flags nothing.
- Flag each claim where it sits. A blanket disclaimer at the top flags nothing.
- A hedge isn't a flag. "Probably" states strength (§7); "not yet measured" or "to verify" says the claim wasn't checked.
- Mark a source unverified until you've read it, and say when you've seen a work only through a summary.

## 9. Someone else confirms the claim

Essay: *On Verifying Claims* P6.

- Whoever made a claim can't be the one to confirm it. That holds for a person as much as for the model or session that drafted it. A model or session asked to check its own claims re-derives the reasoning that produced them and reports the re-derivation as confirmation.
- Get an independent read, by someone who hasn't been told what to conclude. For a model, that means a fresh session with no access to the drafting context.
- Give the reader the writing and its sources. Hold back the author's account of the claims, and never pre-load the verdict. Compare R-guide §4 (Reading order).
- The reader reports; they don't edit the writing or propose replacement wording. For a claim they can't support, they name the kind of evidence that would support it as written.
- The maker still checks their own sources (§5). That check comes before the independent read and doesn't replace it.

## 10. A finding is evidence; the author decides

Essay: *On Verifying Claims* P7.

- What a check reports, whether from a tool, a bot, a reviewer or an audit, is input to a judgement, not a verdict. The person who publishes decides what stands and answers for it.
- Work the findings one at a time, and record a disposition under each.

| Disposition | When |
| --- | --- |
| **Fix** | The finding is right. Revise the writing; the next read checks that the defect is gone, not only that the text changed. |
| **Accept with a stated reason** | The claim stands as written, for a reason you record. |
| **Reject as not a claim** | The line is a value judgement or illustration the writing doesn't assert. A line with figures in it needs a disclaimer the reader can see. |
| **Contest** | The reader misread the source, or didn't read it. Record the dispute and its evidence; the claim stays open until it ends in a fix, an acceptance, or vindication: a later independent read re-checks the claim against the disputed source and finds it carried, and that re-check is recorded under the finding. |

- An open contest means the audit isn't finished.
- For an unverifiable finding, fetch the source and read it; the claim is checked again once it's available.
- Know what the check can't catch. It catches carelessness and drift, not deliberate fabrication: an author who invents a source or a figure defeats a reader who can only read what they're given. The author's honesty is the root of trust, and checking primary sources stays the author's job.

## 11. Run a claims audit

Essay: *On Verifying Claims* P2 to P8.

The full check, for work §2 says needs one.

1. **Gather.** The author lists every source the writing cites and where to read it, marking any not available.
2. **Read cold.** An independent reader (§9) takes only the writing and its sources.
3. **List the claims.** Number every claim in order (§3), so none is skipped silently.
4. **Check each claim** against its sources (§4, §5), its reasoning (§6) and the writing's own qualifications. Look for contradictions between claims.
5. **Verdict each claim.** Counter-evidence outranks support. Otherwise, a cited source nobody has read keeps the claim unverifiable, however good the other evidence looks. Otherwise, one route that fully carries the claim, a source or a derivation, is enough: another route that supports less doesn't pull it down.

| Verdict | Means |
| --- | --- |
| **Supported** | The evidence carries the claim at its stated strength, and every source cited for it was read. |
| **Unsupported** | Evidence is needed and none holds: no source, a source that reports nothing, a missing premise, or a citation too vague to find. |
| **Overclaimed** | The source supports a weaker or narrower claim of the same kind (§7). If the kind differs, the claim is unsupported. A stated figure the source's figure doesn't round to, at the precision written, is contradicted, not overclaimed (§7). |
| **Contradicted** | Counter-evidence in the writing or a source, a contradiction between claims, an argument that doesn't follow, or a figure out of tolerance: "47%" against a source's 42%. |
| **Unverifiable** | A source that can be found (a DOI, a URL, or author, title and venue) hasn't been read yet. A citation that can't be found is unsupported, not unverifiable. |

6. **Work the findings** with the author (§10).
7. **Repeat** with a fresh reader after any fix. The audit is done when a cold read of the unchanged text raises no new finding and no contest is open.

- Verdicts at the boundary involve judgement, and two readers can differ. Working the findings absorbs that; the verdict list doesn't.
