# Refactoring: changing existing code

A checklist for changing structure while preserving behaviour, and for getting
untested code ready to change. For the reasoning, see *On Refactoring Code*.

## 1. Explain before you edit

- **On code you didn't build, start with `explain`.** This includes code accepted
  from a model or copied from a snippet. Use its five parts even without the skill:

  | Part | What to establish |
  | --- | --- |
  | What it does | Trace inputs, outputs, state changes and side effects through the real callers. |
  | Why it's shaped this way | Read the code, tests and history. Say “can't tell” where the reason remains unknown. |
  | What it assumes | Name invariants, dependency contracts, ordering and assumptions about existing data. |
  | What would break it | Walk Requirement, Existing behaviour, Tests, Failure, Trust boundary, Scale, Structure and Legibility. |
  | What you must do to own it | Name concrete checks or questions that would close the gaps in your understanding. |

- Compare observed behaviour with the requirement and any spec, SRS or SDD.
  Keep observations, intended behaviour and unanswered questions distinct.
- Turn observed behaviour into characterization tests; turn dependency questions
  into seam checks; trace possible breakage through effects and pinch points.
- For difficult code, use Feathers' **Scratch Refactoring** to explore its shape
  in a disposable change. Discard those edits; redo any useful change under tests.

## 2. Build, ask, defer, don't

Apply this table when you discover work beyond the task's wording.

| Choice | When | Action |
| --- | --- | --- |
| **Build** | Correctness requires it: a guard, a known error path, or a fix in shared code that every caller needs. | Include the necessary code and tests. Check every affected caller. |
| **Ask** | Someone else owns the decision: unspecified behaviour, an architectural choice, or a reduction in the requirement. | State the missing decision and its consequence. Resolve it with that owner before implementing the dependent work. |
| **Defer** | Real work unrelated to this change: a defect, or debt that matters. | Record a follow-up ticket and link it from the PR. |
| **Don't** | Speculative structure, a rewrite of code you only passed, a fixture refactor for appearance alone, or a cosmetic preference. | Leave it alone. |

- Debt matters when it sits in code that changes often or is business-critical,
  or when it carries a risk or a hard deadline, such as an end-of-life runtime,
  an unpatched dependency or a security exposure. Deferring it does not mean
  fixing it now.
- An unspecified failure or missing-value meaning is **Ask**. Handling a
  missing value with an already established meaning is **Build**.
- If part of the requirement is harder than expected, ask; don't silently omit it.
- For small structural improvements in the code you are changing, use
  F-guide §3 (Tidy only what you touch).

## 3. Tidy only what you touch

- **“Leave it cleaner” means tidy the code you are already changing.** Improve a
  name, extract a coherent operation, or remove local duplication when that makes
  this change easier to understand. It does not authorise a surrounding rewrite.
- **Keep tidying in a separate commit from the behaviour change.** Each commit
  must build and pass its relevant tests. Put preparatory tidying first when the
  behaviour change depends on it.
- **Project rules requiring structural change on touch take precedence.** Follow
  that requirement even when it exceeds a local tidy; preserve the commit split.
- Refactor against green tests. If dependencies prevent testing, make only the
  careful change needed to establish a seam, then capture behaviour before doing
  broader restructuring. See F-guide §6 (Open a seam).

## 4. Capture existing behaviour

- **Characterization tests are green by construction.** Observe the existing
  implementation, inspect the result, and record that result as the expectation.
  An initial guess may fail; resolve it by learning what the code does.
- Preserve observable results, state changes and external effects around the
  planned edit. Include relevant boundaries and failure paths.
- Keep expectations independent of the implementation: record concrete results;
  don't call the production calculation to generate the expected value.
- A characterization test records what happens; it does not establish that the
  behaviour is correct. Name surprising behaviour and resolve any proposed change
  through F-guide §2 (Build, ask, defer, don't).
- For a bug fix, add a **regression test** for the intended behaviour: see it fail
  before the fix, pass after it, and fail when the fix is temporarily reverted.
  Restore the fix and confirm green. Keep the behaviour change separate from refactoring.
- Check that the characterization assertions detect a deliberate change to the
  behaviour they preserve. Restore the code and rerun; initial green alone is
  not evidence that the test detects a regression. For the mutation test kind, see
  T-guide §2 (Choose the kind of test).

## 5. Trace effects and choose test points

- Use Feathers' **effect sketch**: trace how an edited value or operation can
  affect returned values, shared state, callers and external systems.
- Choose **interception points**, places where tests can observe those effects.
  Account for effects that leave by another path, including delayed work.
- Look for a **pinch point**, where effects from several planned edits converge.
  A test there can protect the area without a separate test for every private
  method. Check for effects that bypass it before relying on that protection.
- Exercise the real affected paths. A passing test at one point does not cover
  an unobserved write, another caller or a dependency replaced by a double.

## 6. Open a seam

- A **seam** lets you substitute behaviour without editing the code at the point
  of use. Find its **enabling point**, where the implementation is selected;
  check both the test substitution and the production selection.
- Prefer an existing seam. When none works, break the dependency that blocks
  construction, execution or observation with the smallest reviewable change.
- Use Feathers' **Parameterize Constructor** or **Parameterize Method** when a
  caller can supply the dependency. **Extract Interface** can isolate a needed
  role; **Extract and Override Factory Method** can isolate object creation.
  Choose a technique that fits the language and dependency, not a blanket rewrite.
- Keep business decisions apart from library and platform calls. Put the calls
  behind an interface you own; retain integration tests against the real boundary.
- For a monster method, identify a small operation and its inputs, outputs and
  side effects before extracting it. Preserve evaluation order and shared state;
  don't combine extraction with a correction to the algorithm.

## 7. Sprout or wrap when adding behaviour

- **Sprout Method / Sprout Class:** put new behaviour in a tested method or class,
  then make the small change that calls it from the existing code.
- **Wrap Method / Wrap Class:** retain the existing operation and add behaviour
  around it through a wrapper. Check ordering, failure handling and callers that
  might bypass the wrapper.
- Test the connection as well as the new behaviour. Neither technique proves
  the old code correct or removes the need to characterize what the change affects.
- Treat the addition as a behaviour change. Keep any preparatory refactoring in
  its own commit, and defer wider cleanup through F-guide §2 (Build, ask, defer, don't).

## 8. Verify each step

- Establish the baseline before editing. Run the focused tests after each small
  transformation; when one fails unexpectedly, undo or diagnose that step before
  adding another.
- Use automated refactoring where available, then inspect the diff. Check callers,
  signatures, evaluation order and effects; a successful tool run is not proof.
- Run the relevant build, lint, type checks and broader tests before handing off.
  Record commands, results and any untested paths in the PR. If no test framework
  exists, state that gap and the checks you could perform.
- In self-review, check that the structural commit preserves behaviour and that
  the functional commit meets the requirement. Record unresolved limitations
  as known limitations in the PR description; retain lasting reasons in comments
  or commit messages.

The named legacy-code techniques come from Michael Feathers,
[*Working Effectively with Legacy Code*](https://www.informit.com/store/working-effectively-with-legacy-code-9780132931779).
Read by problem: characterization (Ch. 13); safe edits and feedback (23, 2);
sprout and wrap (6); effects and pinch points (11–12); dependency breaking
(9–10, 25); seams (4); monster methods (22); understanding (16); and library
boundaries (14–15). For other sources, see [References](references.md).
