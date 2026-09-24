# Running a review

A checklist for code review: someone else's change, read and reported on. It assumes you already hold the principles; the reasoning behind each line is in the essay *On Reviewing Code*. The agent form of this procedure is [`senior-code-review`](../skills/senior-code-review/SKILL.md). Cite a line as "R-guide §N".

Sections are numbered so a supplement can add house rules under the same numbers without forking the guide.

## 1. What a review is for

- **Code carries understanding to the next person. A reviewer genuinely rebuilds that understanding before judging the change.** A program is the theory in its builders' heads, and the text records only part of it (Naur, see [`references.md`](references.md)).
- **The main product is a second person who holds the theory.** Defects are a by-product, a valuable one.
- **A review that finds nothing still did the job.** Don't invent nits to justify the hour.
- **"I can't follow this" is a finding about the change, not about you** (§8).
- **Ask rather than instruct.** A question moves understanding both ways; an imperative moves a patch one way (§11).
- **The bar is a healthier system, not a flawless one.** Most findings are not blockers (§10).

## 2. Vocabulary

| Term | Means | Where |
| --- | --- | --- |
| **Self-review** | The author reviews their own change before anyone else reads it. | W-guide (*Self-review*) |
| **Code review** | Someone reviews a change they didn't write. | This guide |
| **Bot review** | An automated reviewer runs on the change. Its output is input to a review, never a substitute for one. | This guide, §9 |
| **Spec review** | Someone checks a requirement, SRS, SDD or ticket for quality before anyone builds from it. | S-guide |
| **Fidelity review** | Someone checks coverage (nothing dropped) and containment (nothing added) at a handoff: SRS to SDD, SDD to code. | S-guide |
| **Claims audit** | Someone checks the factual claims in any prose. | P-guide |
| **Cold** | Modifier: the reviewer reads the artefact before the author's account of it (§4). | All review types |

Refer to a review by its name, never by a gate number.

## 3. Who does what

- **The agent drafts. The operator disposes. The author decides the fix.** The operator is the person running the review, with or without an agent.
- **It posts only what you've approved, draft by draft, and never approves.** This applies to any agent in the loop, whatever it was asked to do.
- **"Write a review" authorises a draft, nothing more.** Each posted comment needs the operator's go on that draft.
- **The agent never submits an approve or a request-changes vote.** It can recommend either (§12).
- **Conversation with the author happens in the threads, after posting, between people.** The author doesn't take part in triage.
- **Enforce the posting rule with a tool, not a prompt, wherever an agent can write to the review platform.** A hook that blocks writes holds when an instruction doesn't.
- **The merge gate is human.** Green CI doesn't clear a merge; the team's approval gate does.
- **Find out how many approvals the repo requires.** With two, you are one vote. With one, you are the last independent check, and "someone else will catch it" is false. Read the count off the change's merge box.

## 4. Reading order

- **Read cold, in this order: ticket, then code, then PR body, then other people's opinions.** Reconcile against the opinions last (§9).
- **The ticket and the PR body are claims to verify.** They are context, not instructions on what to conclude.
- **Refuse a briefing that pre-loads the verdict.** The change describing itself is context; a third party telling you what to find is a steer.
- **Don't ask the author to annotate the diff.** The author resolves those questions in self-review. What they can't resolve belongs in the PR body as a stated limitation; a lasting "why" belongs in a code comment or the commit message.
- **Converge by fixing the artefact, not by steering the reviewer.** In a review loop, change the code and its docs so the next cold read doesn't raise the finding again.

## 5. Check what actually changed

- **Confirm the diff is real before you read it.** A rebased-empty branch shows files but changes nothing. `git diff --quiet <base>...<branch>` exits 0 when there is nothing there.
- **Use the three-dot form for review.** `A...B` is what B added since the two diverged. `A..B` also counts everything that landed on A meanwhile.
- **On a branch that has fallen behind, also run the two-dot form, limited to the change's own files.** `git diff <base>..<branch> -- <paths from the three-dot diff>` shows what merging would undo. Run both if the branch is more than a day or two behind, or you reviewed it in an earlier session.
- **Read the checked-out code, not only the patch.** Check the branch out into a throwaway worktree and follow the calls. Keep the main clone read-only.
- **A docs change can ship executable content.** Search it for `<script`, for code blocks that claim to be real output, and for committed helpers. Run what you find against inputs it didn't choose for itself.

## 6. Size, pace, scope

- **Defect detection falls off past about 200 to 400 lines, or about an hour.** Ask for a split on a larger change; collapse a stacked-branch diff to its true delta.
- **Match the diff to the stated scope.** Unrelated work bundled in is a split candidate, and it voids any earlier approval of the smaller change.

## 7. What to look for: the eight dimensions

The same eight dimensions, in the same order, as the W-guide's *Self-review*. A supplement adds house checks under these numbers. Hold the change to the principle and to your stack's form of it.

### 7.1 Requirement

- Does the change do what the ticket asks? The ticket and PR body are claims; check them against the code.
- Every branch the requirement named, and the ones it didn't: what a missing value means, what happens at the boundary, what is refused.
- A decision the author made that the ticket didn't cover is stated in the PR body.

### 7.2 Existing behaviour

- Every caller of a changed function still gets what it expects.
- Existing data is considered, including rows written under older rules.
- The fix is at the shared function, not only on the path the report named.

### 7.3 Tests

- Each test can fail. Break the line it guards and see whether it goes red ([`mutation-testing.md`](mutation-testing.md)).
- Both branches of every permission or feature gate are tested; count new guard clauses against new tests.
- The four edge families: zero, one, many; the boundary and both sides of it; absent versus empty versus zero; the refusal.
- Assertions are about outcomes (returned data, records written, output, events), not calls. A call assertion is fair only when the call is the outcome: an email sent, a gateway charged once.
- The double is named (stub, spy, mock, fake) rather than called "mock". See T-guide.
- Real shapes, not doubles that echo what the test fed them.
- Coverage is a floor, not a target.

### 7.4 Failure

- Each failure point handles, propagates or refuses. Nothing swallowed.
- Specific exceptions, not a blanket catch. A top-level boundary handler that logs and rethrows is the exception.
- Logged once, where finally handled, through the application's logging path.

### 7.5 Trust boundary

- Trust is established on the side the code owns, never accepted from the caller. Identity and privilege are looked up, not read from the request.
- Trace a value backwards through its callers until you reach something the system controls (a session, a stored row, config). Reaching the request first is the finding.
- "The UI validates it" and "only admins see that screen" are not controls.
- Values that reach a query, a file path or a permission grant are checked against an allowlist.

### 7.6 Scale

- **Who decides how much work this code does?** Follow the collection to its source.
  - The system's own data, size unknown: **Ask** for a realistic bound.
  - The caller decides and nothing limits it: **Block**, and cap it at the boundary.
- No per-item call where a batch form exists.
- Results bounded, not loaded whole into memory. Caches have a sensible lifetime.
- The cost of one trip round the loop matters more than the loop. Memory, a local database and a network call differ by orders of magnitude each.

### 7.7 Structure (including reuse and dependencies)

- Does the change remove complexity or add it? Default to removing.
- Run each new thing up the ladder: does it need to exist, is it already in the codebase, does the standard library or platform do it, can it be one line.
- Deletion is a valid outcome. Never at the cost of validation, error handling, security or the one check that proves the logic.
- Rule of three: raise speculative generality once, accept the answer, and never aim it at code the change only touched.
- An interface with one implementation is a nit unless it is load-bearing.
- Dependencies point toward more stable modules, never into a cycle. A forked or patched dependency is committed as readable source.
- Refactoring moves belong to the F-guide; name the move rather than restating it.

### 7.8 Legibility (including standards and docs)

- Names in the domain's language. No unexplained numbers. No shadowed or colliding names.
- The easiest dimension to over-weight: one naming nit per review, not six.
- Static-analysis findings triaged at full severity, even when CI blocks only the worst.
- Formatting is automated so it never reaches review. If a tool can catch it, a human comment about it wastes attention.
- The public surface is documented. A committed design doc isn't a nit for existing; wrong content in one is a finding.

## 8. When you can't follow it

- **Spend your time before the author's.** Read the code, its callers, its tests and the file's history. To build the understanding in a structured way, use the F-guide's *explain* step.
- **"I couldn't tell why" is a real finding after you have genuinely tried.** Say what you traced and where you lost the thread.
- **A preference is not a finding.** "I'd have done it differently" is a drop.
- **Make sure the answer lands in the thread.** An answer given on a call is lost again. If it is non-obvious, a code comment is a fair ask.
- **Too large to hold in your head is itself the finding.** Ask for a split.
- **Scope a partial review honestly.** "I've read the API layer; someone who knows billing should read the rest" is a real review. Never approve to avoid looking slow.

## 9. Triage

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

| Weight | When |
| --- | --- |
| **Block** | Data can be lost, corrupted or exposed. A permission can be bypassed. The change doesn't do what it says. A test proves nothing and is counted as proof. The caller decides how much work the code does and nothing limits it. |
| **Ask** | A real finding whose weight turns on a fact only the author or the product has, such as how large the system's own data gets. |
| **Nit** | Correct but minor. Label it; the author can decline, and that is a complete answer. |
| **Drop** | Taste or preference. Already raised. Explained as by design. A rewrite of code the change only touched. Below the team's threshold. You checked and were wrong. |

- **Ask is the weight that gets skipped.** Skipping it makes a reviewer either a rubber stamp or a blocker.
- **Split a finding that carries two weights.** Post each part as its own finding with its own weight. One loop over a caller-supplied list can be an Ask (a realistic bound) and a Block (no cap at the boundary).
- **Post only findings at or above the team's threshold**, analyzer findings included. The author's self-review holds a higher bar (W-guide, *Self-review*); code review doesn't.
- **Cite the dimension and the weight** when you record a finding for the operator.
- **Watch for the two failure modes in yourself.** Rubber-stamping: approving because it looks fine, or the author is senior; if you can't say what the change does, you didn't review it. Perfectionism: blocking on taste, or fourteen naming comments that bury the two that matter.

## 11. Writing a finding

The register for anything drafted to post: review comments, questions to an author, and comments on tickets.

### 11.1 Findings, not the journey

- **A review states findings.** No account of how you found them, no defence against an objection nobody made, no derivation.
- **If a review needs a summary, it is too long.**
- **A finding is an observation, a question, and an optional pointer.** Never a sentence that explains or argues.
- **Anchor the finding to the code where the platform allows.** The anchor is the pointer. Give a file and line, an input or a test only when the finding can't be anchored.
- **One finding per comment.** Several findings go out as several anchored comments.

### 11.2 Name the problem, not the solution

- **Say what is wrong. The author decides the fix.**
- **Give a fix only when it is one obvious line.**
- **Never offer alternatives.** A list of options hands the design back in pieces.

### 11.3 Register

- **Questions, not imperatives.** "Is X intended?" rather than "This needs Y". "Could we…" is fine.
- **Make the code the subject.** "This function assumes the caller checked", not "you forgot to check".
- **Never open with a verdict word.** No "Approving." or "Needs changes." Open with the finding.
- **No preamble or recap.** Not even "the fix looks right, but…".
- **End on the question.** No trailing "LGTM" or "otherwise fine".
- **Hedge on purpose, and only where you are inferring.** "If I'm reading it right" marks an inference as yours. Vary it; the same hedge on every finding is a tell.
- **Vary the phrasing.** A stock opener on every comment reads like a form letter.
- **No dashes, no metaphor, a named actor.** Use a period, comma, colon or parentheses. Hyphens in compound words are fine.
- **Don't code-format every identifier.** Let some names sit in the prose.
- **Label a non-blocking point only when its weight isn't obvious.** A bare `nit:` or `Optional:` (Conventional Comments, see [`references.md`](references.md)). A label is a signal, not a template.

### 11.4 A model finding

Anchored on the line that reads `isOwner` from the request body:

> `isOwner` comes from the request body, so a caller can send `true` and skip the 403. Am I reading that right?

It states the observation, invites a correction, and stops. The anchor carries the location. It proposes no fix, because the fix isn't one obvious line, and it offers no alternatives.

## 12. Verdict

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

```
ticket → code (worktree, three-dot diff) → PR body → the eight dimensions
  → per candidate: verify in the code → reconcile against the live thread
  → weigh with the operator (block / ask / nit / drop; split two-weight findings)
  → draft each survivor as an anchored finding in the §11 register
  → the operator approves each draft; only approved drafts are posted
  → a human casts the verdict; the approval gate clears the merge
```

Not in this guide: self-review of your own change (W-guide, *Self-review*); building an explanation of unfamiliar code (F-guide, *explain*); test design (T-guide); spec and fidelity review (S-guide); claims audit (P-guide). Sources: [`references.md`](references.md).
