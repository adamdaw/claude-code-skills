# Code writing: craft principles

Portable principles for writing code well. Each has a house form in your own stack (an API, a framework convention, a rule file); this guide states the principle and leaves the house form to you. Sources are in [`references.md`](references.md). Terse by design: read it as a checklist, not an essay.

## Complexity is what you're managing

- **Every change either adds or removes complexity. Default to removing it.** The measure of a design is how much you have to hold in your head to change it safely.
- **Prefer deep modules: a small, simple interface over a substantial implementation.** A class or function that exposes a lot to save a little inside is shallow, and the cost leaks to every caller.
- **Hide information, don't broadcast it.** A module owns its decisions; callers shouldn't need its internals to use it correctly. Tell, don't ask.

## Design for change and for test

- **If it's hard to test in isolation, that's a design signal, not a testing problem.** Wire collaborators through a seam you can substitute, rather than hard-wiring a concrete dependency or reaching for global state.
- **Depend on the narrowest thing that works** (an interface or a small port, not a whole object graph), so a change stays contained.

## Say what you mean

- **Names carry intent. Spend them in the domain's language.** No magic numbers, no abbreviations that only make sense today.
- **Comments explain why, not what.** The code already says what. Use comments for the reasoning, the constraint, or the thing that would otherwise surprise the next reader.
- **Small, obvious units.** Guard clauses over deep nesting, one responsibility per function, a function you can describe in a sentence.

## Don't repeat, don't speculate

- **DRY the knowledge, not just the text.** The duplication that hurts is two places that must change together. Extract those; leave coincidental similarity alone.
- **YAGNI: build for the requirement in front of you.** Speculative generality is complexity you pay for now and rarely use. Delete a dead option rather than keeping it against a someday.
- **Reach for the least code that works, once you understand the problem.** Read the task and trace the real flow end to end, then take the lowest rung that holds: does it need to exist at all (YAGNI), is it already in the codebase (reuse the helper or pattern, don't rewrite), does the standard library or platform do it, does an installed dependency, can it be one line, and only then the minimum that works. Deletion over addition, boring over clever, fewest files. A small diff in the wrong place isn't lazy, it's a second bug.
- **Fix the root cause, not the symptom.** A report names a symptom. Find every caller of the function you touch and fix the shared function once; patching only the path the ticket names leaves a sibling caller broken.

- **Minimalism never cuts the guardrails.** Input validation at trust boundaries, error handling that prevents data loss, security, and accessibility aren't where you save lines, and non-trivial logic still leaves one runnable check behind (see [`test-writing`](test-writing.md)). Mark a deliberate corner-cut with a comment naming the ceiling and the upgrade path.

## Fail loudly, at the boundary

- **Never swallow an error.** Surface it, or propagate it to a boundary that will. Log it once, at that boundary, through the application's logging path, not with an ad-hoc print and not re-logged at every frame as it unwinds. No bare catch that hides the cause.
- **Validate inputs at the edge.** Normalize an expected-absent value early (a null to an empty collection) so it doesn't propagate downstream. An actual error is not an absent value, though: surface it rather than papering over it with a default, per "never swallow an error" above.

## Leave it cleaner

- **Tidy on touch, in a commit separate from the behaviour change.** Small structural cleanups where you're already working, kept apart from the functional diff so the review stays legible.
- **Refactor against green tests.** When the code isn't testable yet, the first careful move is the minimal seam that lets you get a test around it (Feathers), then refactor green. You don't restructure working logic blind.

## Respect the machine

- **Batch the work; assume the collection is large.** Do the work in a set rather than a call or query per element in a loop (the N+1 trap), keep queries bounded, and stay inside whatever limits the runtime enforces. Realistic data volume is a requirement in front of you, not the speculative someday YAGNI warns against.

See also: [`test-writing`](test-writing.md) (tests as design pressure) and [`references.md`](references.md) for the sources behind each principle.
