# Test writing: craft principles

Portable principles for writing tests well. Each has a house form in your own stack (a test framework, an assertion library, a fixtures convention); this guide states the principle and leaves the house form to you. Sources are in [`references.md`](references.md). Terse by design: read it as a checklist, not an essay.

## Tests come first

- **Write the failing test before the code, then make it pass, then refactor (red, green, refactor).** The failing test proves the test can fail, so a later green means something. Show the red before the green.
- **A test written after the fact tests what you built, not what you meant.** Prefer the order that pressures the design.

## Test behaviour, not implementation

- **Assert observable outcomes, not internals.** Private fields and method spies couple the test to the shape of the code and break on honest refactors. Assert returned data, side effects, rendered output, and emitted events.
- **One concept per test, named as a sentence.** Arrange, act, assert; a clear test name and assertion usually beat a custom message on every line.

## Cover what matters, not what's easy

- **The negative paths are the point.** Null and empty inputs, the error branch, both sides of every permission or feature gate. Exercise the branch, not just the happy path. A gate with only its happy path tested is a gate nobody has ever watched close.
- **Four edge families, and naming them is most of spotting them.** *Zero, one, many*: the three cardinalities that behave differently, and most loops are written with many in mind and break quietly on zero. *Boundaries*: for a rule of "up to 10" the interesting inputs are 9, 10 and 11, never the comfortable middle. *Absent versus empty versus zero*: a missing field, a present but empty one, and one set to `0` or `false` are three states code routinely conflates, and `if (!discount)` treating "no discount recorded" the same as "a discount of zero" is a real bug with money behind it. *The refusal*: a new `if` that guards something wants two tests, not one.
- **Coverage is a floor, not a target.** A percentage bar is a floor to clear, not the goal; a green number laid over untested branches is worse than an honest gap.

## Test doubles: name it, then pick one

- **"Mock" is one of five doubles, and only one of them checks calls.** A *dummy* fills a parameter slot and is never used. A *fake* is a working implementation with a shortcut that makes it unfit for production, an in-memory store standing in for a database. A *stub* returns canned answers. A *spy* is a stub that records how it was called. A *mock* carries expectations and fails when the calls don't match them. Say which one you mean, in the test name and in review: "mock" used loosely hides whether a test asserts outcomes or call sequences, which is the distinction the next two bullets turn on.
- **Prefer state verification to behaviour verification.** Assert what the code produced, the returned data, the records written, the output rendered, rather than which methods it called. Checking calls pins the test to today's implementation, so an honest refactor reddens a correct change. The exception is a side-effect-only collaborator (an email sent, a gateway charged exactly once): there the call *is* the observable behaviour, so asserting it is the right thing to do. If your tooling offers a "all expected calls happened" assertion, treat it as bookkeeping and pair it with a real one.
- **Classical by default: use the real collaborator unless it is slow, unbuilt, or awkward to construct.** A double only returns what you told it to, so when the behaviour under test is the real shape (a query's fields, a collection's contents), exercise the real thing. Guard that shape in the test that owns it, not in a downstream consumer's double, because a double hides a dropped field the consumer would fail on at runtime.
- **Classical costs bigger fixtures. Pay that with factories, not with more doubles.** Reaching for a double to dodge setup trades a bug-catching test for a fast one.
- **The mockist style earns its keep designing outside-in.** When the collaborator does not exist yet, letting the test name the interface you wish you had is real design pressure. Swap in the actual collaborator once it exists; the scaffolding is not the permanent test.
- **Don't double what you don't own.** A hand-written stand-in for a third-party client encodes your belief about how that library behaves, and your belief is exactly what's wrong when the library surprises you. Wrap it in a thin interface of your own and fake that instead, so the thing you're pretending about is code you control.
- **Neither style proves the system works.** Both still need a coarser end-to-end pass over the assembled thing before you believe it.

## Tests are design pressure

- **Hard to test is a design smell.** Reach for a seam (inject the collaborator) before reaching for heavier setup. If a test needs elaborate scaffolding, the code wants restructuring, not the test.

## Keep them trustworthy

- **Fast, deterministic, isolated.** No order dependence, no shared mutable state, clean up what you create. Build data through factories, not a shared global fixture.
- **A flaky test is a broken test.** Fix it or delete it (quarantine is a stopgap, not a parking spot); a test you learn to ignore protects nothing.

See also: [`code-writing`](code-writing.md) (design for test) and [`references.md`](references.md) for the sources behind each principle.
