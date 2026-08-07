# Test writing: craft principles

Portable principles for writing tests well. Each has a house form in your own stack (a test framework, an assertion library, a fixtures convention); this guide states the principle and leaves the house form to you. Sources are in [`references.md`](references.md). Terse by design: read it as a checklist, not an essay.

## Tests come first

- **Write the failing test before the code, then make it pass, then refactor (red, green, refactor).** The failing test proves the test can fail, so a later green means something. Show the red before the green.
- **A test written after the fact tests what you built, not what you meant.** Prefer the order that pressures the design.

## Test behaviour, not implementation

- **Assert observable outcomes, not internals.** Private fields and method spies couple the test to the shape of the code and break on honest refactors. Assert returned data, side effects, rendered output, and emitted events.
- **One concept per test, named as a sentence.** Arrange, act, assert; a clear test name and assertion usually beat a custom message on every line.

## Cover what matters, not what's easy

- **The negative paths are the point.** Null and empty inputs, the error branch, both sides of every permission or feature gate. Exercise the branch, not just the happy path.
- **Coverage is a floor, not a target.** A percentage bar is a floor to clear, not the goal; a green number laid over untested branches is worse than an honest gap.

## Mocks hide reality

- **Mock to isolate a unit, but a mock only returns what you told it to.** When the behaviour under test is the real shape (a query's fields, a collection's contents), exercise the real thing. Guard the shape in the test that owns it, not in a downstream consumer's mock, because a mock hides a dropped field the consumer would fail on at runtime. Injecting a substitutable seam is what makes a mock possible, but prefer the real collaborator when its shape is the thing under test; mock to isolate the genuinely external or slow.
- **Assert the outcome, not the mock, unless the call is the outcome.** Verifying "the method was called" is usually a weak proxy for what it produced, so prefer the produced result. The exception is a side-effect-only collaborator (an email sent, a gateway charged exactly once): there the call *is* the observable behaviour, so asserting it is the right thing to do.

## Tests are design pressure

- **Hard to test is a design smell.** Reach for a seam (inject the collaborator) before reaching for heavier setup. If a test needs elaborate scaffolding, the code wants restructuring, not the test.

## Keep them trustworthy

- **Fast, deterministic, isolated.** No order dependence, no shared mutable state, clean up what you create. Build data through factories, not a shared global fixture.
- **A flaky test is a broken test.** Fix it or delete it (quarantine is a stopgap, not a parking spot); a test you learn to ignore protects nothing.

See also: [`code-writing`](code-writing.md) (design for test) and [`references.md`](references.md) for the sources behind each principle.
