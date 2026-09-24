# Code writing

**Code carries your understanding to the next person, and most of what you know never reaches the code.** Write so the reader can recover it: as simple as possible, but no simpler. The reasoning is in *On Writing Code*.

A checklist for someone who already holds the principles. Each line has a house form in your own stack (an API, a framework convention, a rule file); the guide states the principle and leaves the house form to you. Sources are in [`references.md`](references.md). Changing existing code, including leaving it cleaner, is in the F-guide: F-guide §2 (Build, ask, defer, don't), F-guide §3 (Tidy only what you touch), F-guide §4 (Capture existing behaviour).

## 1. Start with the whole path

- **Build the walking skeleton first.** The thinnest version that runs end to end through every layer, before any part is elaborated. It includes what makes the feature reachable (configuration, permissions, deployment, navigation), not only the code. Exercise it as an ordinary user, not an administrator.
- **Its first passenger is one failing test at the outside.** See T-guide §1 (Start at the outside).
- **Estimate before you build.** Work out the order of magnitude (rows, calls, bytes, time) before choosing the approach. When the estimate is inconclusive, assume the collection is large: the realistic worst case. Estimating chooses the design; it isn't optimising. Optimise only what you have measured.
- **Reach for the least code that works, after you understand the problem.** Trace the real flow end to end, then take the lowest rung that holds: nothing, existing code, the standard library or platform, an installed dependency, one line, then the minimum. Deletion over addition, boring over clever, fewest files.

## 2. Manage complexity

- **Every change adds or removes complexity. Default to removing it.** The measure of a design is how much you have to hold in your head to change it safely.
- **Prefer deep modules: a small interface over a substantial implementation.** A module that exposes a lot to save a little inside is shallow, and the cost reaches every caller.
- **Hide how, show what.** A module hides its implementation decisions; callers never need its internals. What it does stays visible: its effects, its failures, its costs. No hidden work, no silent fallback, nothing a caller has to discover in production.
- **Depend on the narrowest thing that works:** an interface or a small port, not a whole object graph. Hand collaborators in rather than letting the code reach out for them.
- **Talk to your immediate collaborators (Law of Demeter).** Ask an object to do something; don't navigate through it to reach a third. This is about behaviour: walking a data structure, a standard-library collection or a fluent builder isn't a violation.
- **Compose by default; inherit with care.** A child class is everything its parent is and everything the parent becomes later, and it must work anywhere the parent does (Liskov). Inherit where a framework requires it, or where that contract is what you mean.
- **Keep it flexible.** Small pieces that do one thing and combine, rather than one piece that does everything. Flexibility and simplicity pull against each other: get flexibility from composition, not from options nobody asked for (§4).
- **Build on solid ground.** Prefer mature, well-understood technology with open standards to a fast-moving framework. A hard dependency on an ecosystem that changes quickly is a liability.
- **Data outlives its software.** Store it in open, documented formats under a schema you own, so the next system can read it without this one.
- **Hard to test means entangled.** See T-guide §8 (Hard to test means entangled).

## 3. Say what you mean

- **One level of abstraction per function.** The reader follows the reasoning step by step without dropping into detail and climbing out again. Aim for clarity, not brevity.
- **Name non-obvious conditions.** A compound or surprising boolean becomes a named function or variable that says what it means (`isRenewalEligible`, not three clauses inline).
- **A name admits what the function does, side effects included.** `getCustomer` that also creates one is `getOrCreateCustomer`. A name that hides a write is a defect.
- **Use the domain's language.** No magic numbers, no abbreviations that only make sense today.
- **Comments explain why, not what.** The code already says what. A comment carries the reasoning, the constraint, or the thing that would surprise the next reader.
- **Small, obvious units.** Guard clauses over deep nesting, one responsibility per function, a function you can describe in one sentence without "and".

## 4. Duplication and speculation

- **Don't repeat knowledge.** The duplication that hurts is two places that must change together. Extract those.
- **Leave look-alike code alone.** Coincidental similarity isn't duplication; merging it couples things that change for different reasons.
- **Abstract on the third copy (rule of three).** Write it, notice it the second time, abstract on the third. Two call sites rarely tell you what varies.
- **A wrong abstraction costs more than a duplicate.** Abstract early only at a boundary you must swap or a published interface others depend on.
- **Build for the requirement in front of you (YAGNI).** Every speculative abstraction is a guess about what will vary, made when you know least. Delete a dead option rather than keeping it for a someday.

## 5. Know why it's correct

- **Know why it works.** Predict a change's effect before you keep it. If it started working and you can't say why, you haven't finished.
- **State invariants in code.** Assert your own assumptions (a total is never negative, a list is sorted by now) where they are relied on. This is for your own code's assumptions; input from outside is validated at the edge (§6), not asserted.
- **Fix the root cause, not the symptom.** Find every caller of the function you touch and fix the shared function once. Patching only the reported path leaves the sibling callers broken.
- **Minimalism never cuts the guardrails.** Input validation at trust boundaries, error handling that prevents data loss, security and accessibility aren't where you save lines. Non-trivial logic leaves one runnable check behind. Mark a deliberate corner-cut with a comment naming the limit and the upgrade path.

## 6. Fail loudly, at the boundary

- **Never swallow an error.** No empty catch, no catch that hides the cause.
- **Catch only to handle it, or to add context and rethrow.** Catch the specific failure you expect, not everything.
- **Log once, where the error is finally handled,** through the application's logging path. Inner layers enrich the error with context; they don't log it on the way up.
- **Normalize absence, surface errors.** Turn an expected-absent value into an empty collection at the edge. A failure is not an absent value: don't turn it into a default.
- **Validate inputs at the edge, against an allowlist.** Enumerate what is permitted and reject the rest. A denylist needs you to have thought of every bad input in advance.

## 7. Respect the machine

- **Batch the work.** Do it for the set, not with a call or query per element (the N+1 trap). Keep results bounded, and stay inside the limits the runtime enforces. Realistic volume is a requirement (§1), not the speculation YAGNI warns against.
- **What's inside the loop matters more than the loop.** An in-memory operation, a local database round trip and a network call are orders of magnitude apart. Big-O is worth one question, whether a loop is nested over the same data; for I/O the constant it discards is the whole cost.

## 8. Writing it up

A repo's own commit and PR conventions win over these.

- **Put each piece of reasoning where it will be read.** Intent in a name; a local why in a comment; the reasoning for the change in the PR body; a constraint that outlives the code in the ticket.
- **Name the rejected alternative in the commit message only when it prevents an undo.**
- **Commit message: what and why, present tense.** One logical change per commit. Tidying: F-guide §3 (Tidy only what you touch).
- **The PR body is a contract about the diff.** What it does, what it deliberately doesn't do, and where you're unsure.
- **Say what you decided that the requirement didn't.** Each such decision is one the reviewer would otherwise re-derive.
- **Say what you didn't do.** Silence reads as coverage. "Not tested at production volume" is honest.
- **Link the deferred tickets.**
- **State limitations as facts, not annotations.** A limitation you couldn't resolve goes in the PR body as state. No comments on your own diff to guide the reviewer (§9).
- **Leave the journey out.** How you got there lives in git history and the review thread.
- **Describe the work, not the people.** No "as discussed with", no credit for who suggested what, no note about which tool helped. Provenance lives in commit metadata.
- **Don't defend it pre-emptively.** Explaining why something is fine before anyone asks usually means you doubt it: act on that instead.
- **Keep it reviewable: aim under 200 lines, never past 400.** Past that, reviewers stop finding defects.

## 9. Self-review

Your own change, before anyone else reads it. Self-review is not cold: you hold the theory, so it finds what is visible from inside it. It never replaces code review: R-guide §1 (What a review is for).

- **Code you didn't build line by line (from a model, a snippet, a similar class): explain it first.** What it does, why it's shaped this way ("I can't tell" is a valid answer), what it assumes, what would break it, and what you must do to own it. The procedure is F-guide §1 (Explain before you edit).
- **Walk the eight dimensions.** The same eight a code reviewer checks: R-guide §7 (What to look for: the eight dimensions).
- **List every candidate, then decide.** Write down each candidate, name the dimensions that came up clean, and decide each one yourself. When an agent runs the pass, it lists and you decide.
- **Hold your own standard, which is higher than the team's.** Include analyzer findings below the team's threshold.
- **Resolve what you'd have annotated.** Find out, test it, fix it, or rename it. What stays unresolved goes in the PR body as state (§8); a lasting why goes in a code comment or the commit message.
- **Refactor-type fixes follow the F-guide:** F-guide §8 (Verify each step).

| # | Dimension | The question | Sub-checks |
| --- | --- | --- | --- |
| 1 | Requirement | Did I build what was asked, or what I assumed? | Every branch the requirement names and the ones it doesn't: what absent means per field, the boundary, what to refuse. Each decision it didn't make is in the PR body. |
| 2 | Existing behaviour | What else routes through what I changed? | Every caller read. Existing data considered, including rows written under older rules. The fix is in the shared function (§5). |
| 3 | Tests | Would these go red if I broke it? | New-behaviour and regression tests seen red; characterization tests are green by construction, per T-guide §2 (Choose the kind of test). Both sides of every gate. Hard to test means entangled: T-guide §8 (Hard to test means entangled). |
| 4 | Failure | What happens when this doesn't work? | Each failure point handled, propagated with context, or refused. Nothing swallowed; logged once (§6). No later write assuming an earlier one worked. |
| 5 | Trust boundary | Where did this value come from, and who controls it? | Trust established on the side you own. Anything reaching a query, a file path or a permission checked against an allowlist (§6). |
| 6 | Scale | What happens at ten thousand instead of ten? | Estimated (§1). No per-item call where a batch exists. Results bounded (§7). |
| 7 | Structure | Is this simpler or more complicated than what was here? | One responsibility and one level of abstraction (§3). Coupling (§2); no hidden ordering between calls. Duplicated knowledge (§4); values that always travel together grouped as one concept. Few arguments, no flag arguments, no output arguments, no dead code. The least-code ladder (§1); no new dependency for something small; dependencies point toward more stable modules. |
| 8 | Legibility | Can the next person change it without asking me? | Names say intent and side effects; no `data` or `temp`; similar things named alike; nothing clever at the cost of reading (§3). No magic numbers. Comments say why; no commented-out code; no stale comment. Standards: analyzer findings triaged, formatting automated, public interfaces documented. |

## 10. Code that goes out under your name

- **You own every line you ship.** If you can't explain why it's shaped this way without the tool that wrote it, you don't own it yet (§9).
- **The tool implements your reasoning; it doesn't replace it.** Design decisions, trade-offs and what the requirement means stay yours.
- **Check behaviour against primary sources.** An API's contract, a library's semantics or a platform limit comes from its documentation or a real call, not from a model's summary or memory. Say in the PR body what you couldn't verify.
- **Fluency is not authority.** Code that reads well, a green run and a confident explanation aren't evidence it's right. Don't ask the model that wrote it to confirm it.

The prose version of these rules is in the P-guide (*Writing*).

## 11. When you're stuck

- **Diagnose before you add.** Find out why it fails before changing anything else. No layered workarounds, retries, delays or fallbacks over a problem you don't understand.
- **Predict before you change.** If you can't say what a change will do, you are guessing, and a guess that works ends the investigation without answering it (§5).
- **Fix where the bad value comes from, not where it surfaced.**
- **Three failed attempts means you're solving the wrong problem.** Stop. Go back to the requirement and check it says what you think, or describe the problem (not your attempts) to someone who knows the system.
- **Spend fifteen minutes before you ask.** Read the code being called, where it's called from, its tests and its history.
- **Then ask specifically:** what you're trying to do, what you tried, what happened.

See also: [`test-writing`](test-writing.md) and [`references.md`](references.md).
