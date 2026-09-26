# Running a review

A checklist for code review: someone else's change, read and reported on. It assumes you already hold the principles; the reasoning behind each line is in the essay *On Reviewing Code*. The agent form of this procedure is [`senior-code-review`](../skills/senior-code-review/SKILL.md). Cite a line as "R-guide §N".

Sections are numbered so a supplement can add house rules under the same numbers without forking the guide.

## 1. What a review is for

Essay: *On Reviewing Code*, R-essay §1, principle 1; R-essay §6.

- **Code carries understanding to the next person. A reviewer genuinely rebuilds that understanding before judging the change.** A program is the theory in its builders' heads, and the text records only part of it (Naur, see [`references.md`](references.md)).
- **The main product is a second person who holds the theory.** Defects are a by-product, a valuable one.
- **Finish able to say, in one sentence, what the change does and why it has this shape.** Saying the first but not the second is a finding (§8).
- **A review that finds nothing still did the job.** Don't invent nits to justify the hour.
- **"I can't follow this" is a finding about the change, not about you** (§8).
- **Ask rather than instruct.** A question moves understanding both ways; an imperative moves a patch one way (§11).
- **The bar is a healthier system, not a flawless one.** Most findings are not blockers (§10).

## 2. Vocabulary

Essay: *On Reviewing Code*, none. The vocabulary is decided for all guides, not taken from the essay.

| Term | Means | Where |
| --- | --- | --- |
| **Self-review** | The author reviews their own change before anyone else reads it. | W-guide §9 (Self-review) |
| **Code review** | Someone reviews a change they didn't write. | This guide |
| **Bot review** | An automated reviewer runs on the change. Its output is input to a review, never a substitute for one. | This guide, §9 |
| **Spec review** | Someone checks a requirement, SRS, SDD or ticket for quality before anyone builds from it. | S-guide §10 (Spec review) |
| **Fidelity review** | Someone checks coverage (nothing dropped) and containment (nothing added) at a handoff: SRS to SDD, SDD to code. | S-guide §11 (Fidelity review) |
| **Claims audit** | Someone checks the factual claims in any prose. | P-guide §1 (Writing under Adam's name) |
| **Cold** | Modifier: the reviewer reads the artefact before the author's account of it (§4). | All review types |

Refer to a review by its name, never by a gate number.

## 3. Who does what

Essay: *On Reviewing Code*, R-essay §3.7; R-essay App. C.

- **The agent drafts. The operator disposes. The author decides the fix.** The operator is the person running the review, with or without an agent.
- **It posts only what you've approved, draft by draft, and never approves.** This applies to any agent in the loop, whatever it was asked to do.
- **"Write a review" authorises a draft, nothing more.** Each posted comment needs the operator's go on that draft.
- **The agent never submits an approve or a request-changes vote.** It can recommend either (§12).
- **Conversation with the author happens in the threads, after posting, between people.** The author doesn't take part in triage.
- **Enforce the posting rule with a tool, not a prompt, wherever an agent can write to the review platform.** A hook that blocks writes holds when an instruction doesn't.
- **The merge gate is human.** Green CI doesn't clear a merge; the team's approval gate does.
- **Find out how many approvals the repo requires.** With two, you are one vote. With one, you are the last independent check, and "someone else will catch it" is false. Read the count off the change's merge box.

## 4. Reading order

Essay: *On Reviewing Code*, R-essay §3.1.

- **Read cold, in this order: ticket, then code, then PR body, then other people's opinions.** Reconcile against the opinions last (§9).
- **The ticket and the PR body are claims to verify.** They are context, not instructions on what to conclude.
- **Refuse a briefing that pre-loads the verdict.** The change describing itself is context; a third party telling you what to find is a steer.
- **Don't ask the author to annotate the diff.** The author resolves those questions in self-review. What they can't resolve belongs in the PR body as a stated limitation; a lasting "why" belongs in a code comment or the commit message.
- **Converge by fixing the artefact, not by steering the reviewer.** In a review loop, change the code and its docs so the next cold read doesn't raise the finding again.

## 5. Check what actually changed

Essay: *On Reviewing Code*, R-essay §3.2, §3.3; R-essay App. A.

- **Confirm the diff is real before you read it.** A rebased-empty branch shows files but changes nothing. `git diff --quiet <base>...<branch>` exits 0 when there is nothing there.
- **Use the three-dot form for review.** `A...B` is what B added since the two diverged. `A..B` also counts everything that landed on A meanwhile.
- **On a branch that has fallen behind, also run the two-dot form, limited to the change's own files.** `git diff <base>..<branch> -- <paths from the three-dot diff>` shows what merging would undo. Run both if the branch is more than a day or two behind, or you reviewed it in an earlier session.
- **Read the checked-out code, not only the patch.** Check the branch out into a throwaway worktree and follow the calls. Keep the main clone read-only.
- **A docs change can ship executable content.** Search it for `<script`, for code blocks that claim to be real output, and for committed helpers. Run what you find against inputs it didn't choose for itself.

## 6. Size, pace, scope

Essay: *On Reviewing Code*, R-essay §3.4, §6, §7.

- **Defect detection falls off past about 200 to 400 lines, or about an hour.** Ask for a split on a larger change; collapse a stacked-branch diff to its true delta.
- **Match the diff to the stated scope.** Unrelated work bundled in is a split candidate, and the added scope needs a fresh review. Whether an earlier approval still counts is repository policy (§9).

## 7. What to look for: the eight dimensions

Essay: *On Reviewing Code*, R-essay §4, reorganised into the eight dimensions.

The same eight dimensions, in the same order, as W-guide §9 (Self-review). A supplement adds house checks under these numbers. Hold the change to the principle and to your stack's form of it.

### 7.1 Requirement

Essay: *On Reviewing Code*, R-essay §3.1; R-essay §6 (the change doesn't do what it says).

- Does the change do what the ticket asks? The ticket and PR body are claims; check them against the code.
- Every branch the requirement named, and the ones it didn't: what a missing value means, what happens at the boundary, what is refused.
- A decision the author made that the ticket didn't cover is stated in the PR body.
- A value that can be missing with no stated meaning is an Ask: what a missing discount means is a decision nobody has made yet, and it isn't the reviewer's to make.

### 7.2 Existing behaviour

Essay: *On Reviewing Code*, R-essay §3.3.

- Every caller of a changed function still gets what it expects.
- Existing data is considered, including rows written under older rules.
- The fix is at the shared function, not only on the path the report named.

### 7.3 Tests

Essay: *On Reviewing Code*, R-essay §4.1; R-essay §1, principles 2, 3 and 6.

- Each test can fail. Break the line it guards and see whether it goes red ([`mutation-testing.md`](mutation-testing.md)).
- Both branches of every permission or feature gate are tested; count new guard clauses against new tests.
- The four edge families: zero, one, many; the boundary and both sides of it; absent versus empty versus zero; the refusal.
- Assertions are about outcomes (returned data, records written, output, events), not calls. A call assertion is fair only when the call is the outcome: an email sent, a gateway charged once.
- The double is named (stub, spy, mock, fake) rather than called "mock".
- Nothing doubles a client the team doesn't own. See T-guide §4 (Name the double; verify at most one interaction) for the one-real-call rule.
- Real shapes, not doubles that echo what the test fed them.
- Every test carries its own assertion.
- A test selects things by a stable, intention-revealing identifier, not a generated one.
- Hard to test is a design signal: elaborate setup to reach one line, many collaborators to double, time, randomness or the filesystem read directly. Usually Ask or Nit, not a licence to redesign; it escalates when it leaves a risky path untested.
- Coverage is a minimum to clear, not a goal: a high percentage over untested branches is worse than an honest gap.
- T-guide §6 (Check the edges) and T-guide §4 (Name the double; verify at most one interaction) hold the full rules.

### 7.4 Failure

Essay: *On Reviewing Code*, R-essay §4.3.

- Each failure point handles, propagates or refuses. Nothing swallowed.
- Specific exceptions, not a blanket catch. A top-level boundary handler that logs and rethrows is the exception.
- Logged once, where finally handled, through the application's logging path.

### 7.5 Trust boundary

Essay: *On Reviewing Code*, R-essay §4.2; R-essay §1, principle 4.

- Trust is established on the side the code owns, never accepted from the caller. Identity and privilege are looked up, not read from the request.
- Trace a value backwards through its callers until you reach something the system controls (a session, a stored row, config). Reaching the request first is the finding.
- "The UI validates it" and "only admins see that screen" are not controls.
- Access goes through the checked path, not an unchecked direct read that someone can forget to guard.
- Values that reach a query, a file path or a permission grant are checked against an allowlist.

### 7.6 Scale

Essay: *On Reviewing Code*, R-essay §4.5; R-essay §1, principle 5.

- **Who decides how much work this code does?** Follow the collection to its source.
  - The system's own data, size unknown: **Ask** for a realistic bound.
  - The caller decides and nothing limits it: **Block**, and cap it at the boundary.
- No per-item call where a batch form exists.
- Results bounded, not loaded whole into memory. Caches have a sensible lifetime.
- The code stays inside the limits the runtime enforces. See W-guide §7 (Respect the machine).
- The cost of one trip round the loop matters more than the loop. Memory, a local database and a network call differ by orders of magnitude each.
- Growth: a scan of a collection inside a loop over the same data grows with the square of its size.
- Turn a scale suspicion into evidence: run the code with a large input when you can.

### 7.7 Structure (including reuse and dependencies)

Essay: *On Reviewing Code*, R-essay §4.4, §4.7; R-essay §1, principles 6 and 7.

- Does the change remove complexity or add it? Default to removing.
- Deep modules: a small interface over a substantial implementation, not a shallow wrapper. See W-guide §2 (Manage complexity).
- Collaborators come in through a substitutable seam, not a hard-wired static or singleton, where a test needs one. Raise it once as Ask or Nit (§7.3), not as a redesign.
- Logic stays out of framework entry points and glue code.
- A long, growing type switch becomes polymorphism. A two-case conditional is usually simpler left alone.
- Ask four questions of each new thing, in order: does it need to exist, is it already in the codebase, does the standard library or platform do it, can it be one line.
- Deletion is a valid outcome. Never at the cost of validation, error handling, security or the one check that proves the logic.
- Deduplicate knowledge (two places that must change together), not code that only looks alike. See W-guide §4 (Duplication and speculation).
- Rule of three: abstract on the third copy. Raise speculative generality once, accept the answer, and never aim it at code the change only touched.
- Two cases earn an abstraction early: a boundary you must substitute (a test double, a replaceable vendor, an isolated platform API) and a published interface others already depend on.
- An interface with one implementation is a nit unless it is load-bearing.
- Dependencies point toward more stable modules, never into a cycle. A forked or patched dependency is committed as readable source.
- Background for judging structure: F-guide §6 (Open a seam) and F-guide §7 (Sprout or wrap when adding behaviour). The finding names the structural problem; the author chooses the fix (§11.2).

### 7.8 Legibility (including standards and docs)

Essay: *On Reviewing Code*, R-essay §4.6, §4.8.

- Names in the domain's language. No unexplained numbers. No shadowed or colliding names.
- The easiest dimension to over-weight: one naming nit per review, not six.
- Static-analysis findings triaged at full severity, even when CI blocks only the worst.
- Formatting is automated so it never reaches review. If a tool can catch it, a human comment about it wastes attention.
- The public surface is documented. A committed design doc isn't a nit for existing; wrong content in one is a finding.

## 8. When you can't follow it

Essay: *On Reviewing Code*, R-essay §7.

- **Spend your time before the author's.** Read the code, its callers, its tests and the file's history. To build the understanding step by step, use F-guide §1 (Explain before you edit).
- **"I couldn't tell why" is a real finding after you have genuinely tried.** Say what you traced and the point where you stopped understanding it.
- **A preference is not a finding.** "I'd have done it differently" is a drop. For debt findings, see D-guide §2 (A finding needs evidence).
- **Make sure the answer lands in the thread.** An answer given only on a call leaves no record. If it is non-obvious, a code comment is a fair ask.
- **Too large to hold in your head is itself the finding.** Ask for a split.
- **Scope a partial review honestly.** "I've read the API layer; someone who knows billing should read the rest" is a real review. Never approve to avoid looking slow.

## 9. Triage

Essay: *On Reviewing Code*, R-essay §3.6; R-essay App. B.

- **Verify each candidate in the code before it becomes a finding.** An unverified finding is a guess. If you were wrong, drop it silently.
- **Tool output is evidence, never a finding by itself.** That includes bot review, analyzers, code graphs and lists of neighbouring changes.
- **Run a bot reviewer read-only.** It doesn't post and doesn't fix; you verify each thing it raises like any other candidate.
- **Reconcile the survivors against the live thread.** Re-fetch the head and read the existing comments.
  - Already raised and open: add weight only if you have something new.
  - Fixed on a newer commit: drop it.
  - Explained by the author as by design: engage that reasoning or accept it.
  - A bot finding made against an older commit: check it against the live diff before repeating it.
- **An approval belongs to a commit.** Whether it still counts is the repo's configuration, not a finding. A rework landing after an approval is worth raising; a rebase or merge commit isn't.
- **"Nothing to add" is a valid outcome** when the thread already covers the findings.
- **Work finding by finding with the operator.** For each: what it is, the evidence, its weight (§10).

## 10. Weighing a finding

Essay: *On Reviewing Code*, R-essay §6, and the Weight passage of each principle in R-essay §1.

| Weight | When |
| --- | --- |
| **Block** | Data can be lost, corrupted or exposed. A permission can be bypassed. The change doesn't do what it says. A test that proves nothing is the only proof behind a permission, a money path or data integrity. A permission or validation gate has no refusal test. The caller decides how much work the code does and nothing limits it. |
| **Ask** | A real finding whose weight turns on a fact only the author or the product has, such as how large the system's own data gets. A missing zero case in an internal helper is Ask or Nit. |
| **Nit** | Correct but minor, including a hollow test on a low-stakes path. Label it; the author can decline, and that is a complete answer. |
| **Drop** | Taste or preference. Already raised. Explained as by design. A rewrite of code the change only touched. Below the team's threshold. You checked and were wrong. |

- **Ask is the weight that gets skipped.** Without it, a reviewer either approves what they can't judge or blocks it.
- **Split a finding that carries two weights.** Post each part as its own finding with its own weight, so an answer to one can't read as settling the other. Example, one loop over a caller-supplied list:
  - Ask: what is a realistic size for this list? The answer sets whether per-item calls are acceptable.
  - Block: nothing caps the list at the boundary. A realistic-size answer doesn't fix this; only a cap does.
- **Post only findings at or above the team's threshold**, analyzer findings included. The author's self-review holds a higher bar, per W-guide §9 (Self-review); code review doesn't.
- **Cite the dimension and the weight** when you record a finding for the operator.
- **Watch for the two failure modes in yourself.** Approving without reviewing: approving because it looks fine, or the author is senior; if you can't say what the change does, you didn't review it. Perfectionism: blocking on taste, or fourteen naming comments posted alongside the two findings that matter, which makes those two harder to find.

## 11. Writing a finding

Essay: *On Reviewing Code*, R-essay §8.

The register for anything drafted to post: review comments, questions to an author, comments on tickets, and chat replies about a review.

### 11.1 Findings, not the journey

- **A review states findings.** No account of how you found them, no defence against an objection nobody made, no derivation.
- **If a review needs a summary, it is too long.**
- **A finding is an observation, a question, and an optional pointer.** Never a sentence that explains or argues.
- **Anchor the finding to the code where the platform allows.** The anchor is the pointer. Give a file and line, an input or a test only when the finding can't be anchored.
- **One finding per comment.** Several findings go out as several anchored comments.

### 11.2 Name the problem, not the solution

- **Say what is wrong. The author decides the fix.**
- **Give a fix only when it is one obvious line.**
- **Never offer alternatives.** A list of options leaves the author to compare designs the reviewer only sketched.

### 11.3 Register

- **Questions, not imperatives.** "Is X intended?" rather than "This needs Y". "Could we…" is fine.
- **Make the code the subject.** "This function assumes the caller checked", not "you forgot to check".
- **Never open with a verdict word.** No "Approving." or "Needs changes." Open with the finding.
- **No preamble or recap.** Not even "the fix looks right, but…".
- **End on the question.** No trailing "LGTM" or "otherwise fine".
- **Frame the mechanics as your reading, even when you are confident.** "If these share one transaction, they roll back together", not "This rolls back as a unit". Mark inferences as yours: "if I'm reading it right". Vary the hedge; the same one on every finding is a tell.
- **Vary the phrasing.** A stock opener on every comment reads like a form letter.
- **Prose, not formatting.** No bold, no wall of bullets; put the evidence inline.
- **Plain verbs.** "Use", not "leverage"; "check", not "validate the correctness of".
- **No dashes, no metaphor, a named actor.** Use a period, comma, colon or parentheses. Hyphens in compound words are fine.
- **Don't code-format every identifier.** Let some names sit in the prose.
- **Label a non-blocking point only when its weight isn't obvious.** A bare `nit:` or `Optional:` (Conventional Comments, see [`references.md`](references.md)). A label is a signal, not a template.

### 11.4 A model finding

Anchored on the line that reads `isOwner` from the request body:

> `isOwner` comes from the request body, so a caller can send `true` and skip the 403. Am I reading that right?

It states the observation, invites a correction, and stops. The anchor carries the location. It proposes no fix, because the fix isn't one obvious line, and it offers no alternatives.

## 12. Verdict

Essay: *On Reviewing Code*, R-essay §3.7, §5 (What you'd actually do), §6.

| Verdict | When | What goes with it |
| --- | --- | --- |
| **Not approved** | The default whenever there are findings. | The findings. No verdict word, no "hold". |
| **Request changes** | Rare: a critical blocker where someone else might approve first. It locks the merge. | The blocking finding. |
| **Approved** | No findings at or above the threshold. | Nothing. A clean approve gets no comment. |
| **Conditional approval** | Findings the author has agreed to address. | One line naming the agreed conditions. |

- **Let the findings set the verdict.** Green CI, a passing dry run and earlier approvals don't clear a real finding.
- **An agent recommends a verdict and never casts approve or request-changes.** Both are votes.
- **Clean areas go unmentioned.** A paragraph on what you verified is padding; checking was the job, not the output.

## 13. End to end

Essay: *On Reviewing Code*, R-essay §3; R-essay App. C.

```text
ticket → code (worktree, three-dot diff) → PR body → the eight dimensions
  → per candidate: verify in the code → reconcile against the live thread
  → weigh with the operator (block / ask / nit / drop; split two-weight findings)
  → draft each survivor as an anchored finding in the §11 register
  → the operator approves each draft; only approved drafts are posted
  → a human casts the verdict; the approval gate clears the merge
```

Not in this guide:

- Self-review of your own change: W-guide §9 (Self-review).
- Building an explanation of unfamiliar code: F-guide §1 (Explain before you edit).
- Choosing and designing tests: T-guide §2 (Choose the kind of test).
- Spec and fidelity review: S-guide §10 (Spec review), S-guide §11 (Fidelity review).
- Claims audit: P-guide §1 (Writing under Adam's name).

Sources: [`references.md`](references.md).
