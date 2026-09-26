# Test writing: craft principles

The T-guide: a checklist for writing tests, and the rules a self-review or code review checks tests against. Cite sections as "T-guide §1 (Start at the outside)". For the reasoning, see *On Testing Code*; for sources, see [`references.md`](references.md).

## 1. Start at the outside

- Start a feature with one failing acceptance test at the outside of the system. Choose the smallest useful behaviour from the requirement or spec.
- Run it against the walking skeleton: the thinnest path through the assembled system. Confirm it fails because the behaviour is missing.
- Use unit tests to drive the implementation. Watch each fail for the intended reason, make it pass, then refactor against green tests.

## 2. Choose the kind of test

These kinds describe scope or purpose; a regression test can also be a unit test. Keep unit, acceptance and integration tests distinct.

| Kind | What to check |
| --- | --- |
| **Unit** | One unit of behaviour, with fast, deterministic feedback. Use real collaborators where practical; a unit need not be a single class. |
| **Acceptance** | A requirement through the system's outside interface. Use it to define when the feature is done. |
| **Integration** | A real connection between components or with a dependency: a database, filesystem, service or framework. Check the contract that a double cannot prove. |
| **Regression** | A known defect. Write the test before the fix and confirm red; apply the fix and confirm green; revert only the fix and confirm red again. Restore the fix and rerun to green. |
| **Characterization** | Existing behaviour before changing code. Observe what it does and record that result. The test is green by construction; it preserves behaviour without claiming that behaviour is correct. See F-guide §4 (Capture existing behaviour). |
| **Mutation** | Whether tests detect a deliberate defect. Use the procedure in [`mutation-testing.md`](mutation-testing.md). |

Older guidance called tests added after green "regression tests". Use *characterization* for tests that record existing behaviour. If the fix already exists, revert it to see red before restoring it.

## 3. A test tells a story; tell it with real things

- Give each test one behaviour to explain: arrange the situation, act, assert the observable outcome. Several assertions can describe that one outcome.
- Double things that act; build things that are. Use real values, records and collections. Use factories to make those fixtures readable.
- Prefer real collaborators. Use a double when a collaborator is slow, unavailable or not yet built; do not substitute one merely to avoid setup.
- Test a query's fields or a collection's shape where the real data is produced. A downstream stub returning the expected shape cannot check that contract.
- When designing outside-in, a double can describe an unbuilt collaborator. Exercise the real collaborator when it exists.
- Before writing a stand-in for a third-party client, make one real call and read the actual response. Then wrap the client in an interface you own and double that interface; a double cannot verify the vendor contract.
- Keep tests deterministic and independent of run order. Clean up what each test creates and avoid shared mutable fixtures.

## 4. Name the double; verify at most one interaction

Use the Fowler/Meszaros names for the role the double plays.

| Double | Role |
| --- | --- |
| **Dummy** | Fills a parameter slot and is never used. |
| **Fake** | A working implementation with a shortcut, such as an in-memory store. |
| **Stub** | Returns canned answers. |
| **Spy** | Records calls for later inspection. |
| **Mock** | Carries call expectations and fails when they are not met. |

- Assert observable outcomes: returned data, stored state, rendered output or emitted events. Do not assert internals such as private fields or use method spies to check internal calls.
- Assert a call only when it is the outcome: a side effect leaving the system, such as sending an email. Never assert calls between your own objects.
- Assert a call count only when that count is the requirement.
- Verify one interaction per test, at most. Use as many input stubs as the behaviour needs; those are not additional interactions to verify.

## 5. Keep the story straight

- Keep logic out of assertions and expected values. Write the expected result explicitly; do not calculate it with the production algorithm.
- Use loops only in setup or to run a table of independent cases. Give each case an explicit input and expected result; do not branch to decide what to assert.
- Make every failing assertion explain what was checked, what was expected and what actually happened from the library's output and any message you add. Add a message only where the library leaves that information out.

## 6. Check the edges

Walk these four families over each new behaviour or branch.

| Family | Cases |
| --- | --- |
| **Zero, one, many** | Empty, single and multiple elements in collections or repeated work. |
| **Boundaries** | The boundary and both sides: for "up to 10", check 9, 10 and 11. |
| **Absent, empty, zero** | A missing value, a present but empty value, and `0` or `false`. Keep their meanings distinct. |
| **The refusal** | Both the allowed and rejected paths of every guard, permission check or feature gate. |

- Check inverse relationships where they apply, such as decoding an encoded value. State the expected relationship explicitly.
- Cross-check against an independent source of truth: known examples, a trusted implementation or independently established results.
- Coverage is a floor, not a target: a green number over untested branches is worse than an honest gap. Use coverage to find unexecuted paths; a percentage does not show whether an assertion checks the behaviour.
- Keep longer case catalogues in the appendix to *On Testing Code*.

## 7. A bug is a symptom

- Find the misunderstanding behind the reported failure.
- Write a regression test that reproduces the defect before fixing it.
- Trace where else that misunderstanding acted: sibling callers, nearby branches and related inputs. Test those cases too.
- Compare patterns across failures before treating each as a separate defect.

## 8. Hard to test means entangled

- Ask whether a well-designed version would be easy to test.
- Undo chosen ties: pass in fetched dependencies, separate a second job, and make a hidden result observable through the public behaviour.
- Accept given ties: when the behaviour depends on a real database, framework or external service, keep that check in an integration test.
- Use a seam where behaviour can be substituted. See F-guide §6 (Open a seam). Do not add elaborate test setup to preserve an avoidable tie.

## 9. A skipped test is an open question

- Resolve what the skipped test leaves unanswered: fix it, delete it if the behaviour no longer applies, or link the ticket that tracks the question.
- Treat quarantine as temporary. A flaky test needs the same explicit follow-up.
