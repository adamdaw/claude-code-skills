# Runnable examples

The three cases in [`mutation-testing.md`](../guides/mutation-testing.md), as code you can run. Every figure quoted on that page comes from the run recorded below. Nothing there is illustrative.

## Reproduce it

```
npm ci
npm test                    # baseline: 9 tests, all green
npm run coverage            # the coverage table below
npm run mutation            # the full operator set
npm run mutation:reduced    # the equality operator alone
```

Those last three produce every figure quoted in [`mutation-testing.md`](../guides/mutation-testing.md) between them: coverage from the first, the full-set scores from the second, and the reduced-set score from the third.

Node's built-in test runner does the testing, so the mutation tool is the only dependency.

## Recorded results

Recorded 2026-08-19 with Node v24.18.0 and Stryker 10.0.0, `coverageAnalysis: "off"`, `mutate: ["src/**/*.js"]`.

Coverage first, from `npm run coverage`, because it is the thing mutation testing is meant to be read against:

| File | Line % | Branch % | Func % |
| --- | --- | --- | --- |
| `src/alerts.js` | 100.00 | 100.00 | 100.00 |
| `src/dates.js` | 100.00 | 100.00 | 100.00 |
| `src/discount.js` | 100.00 | 100.00 | 100.00 |

Full operator set (`npm run mutation`):

| File | Mutants | Killed | Survived | Score |
| --- | --- | --- | --- | --- |
| `src/alerts.js` | 10 | 0 | 10 | 0.00% |
| `src/dates.js` | 11 | 9 | 2 | 81.82% |
| `src/discount.js` | 9 | 6 | 3 | 66.67% |
| **total** | **30** | **15** | **15** | **50.00%** |

Equality operator alone (`npm run mutation:reduced`). `stryker.reduced.conf.json` excludes sixteen of the seventeen mutators Stryker 10.0.0 installs, which leaves `EqualityOperator`:

| File | Mutants | Killed | Survived | Score |
| --- | --- | --- | --- | --- |
| `src/alerts.js` | 1 | 0 | 1 | 0.00% |
| `src/dates.js` | 4 | 2 | 2 | 50.00% |
| `src/discount.js` | 2 | 1 | 1 | 50.00% |
| **total** | **7** | **3** | **4** | **42.86%** |

Every mutant that ran there is an `EqualityOperator` mutant. That is checked against the mutator list the installed instrumenter declares, not assumed from the config: sixteen excluded names, seventeen installed, one left over.

Complete coverage on every file, and mutation scores of 0.00%, 81.82% and 66.67% on those same three files.

Wall clock, median of three consecutive runs on an Apple M5 Pro:

| Command | Mutants run | Wall clock |
| --- | --- | --- |
| `npm run coverage` | not applicable | 0.17s |
| `npm run mutation` | 30 | 0.94s |
| `npm run mutation:reduced` | 7 | 0.74s |

Those are whole-command times with npm and Stryker startup included, and they are the figures most specific to this machine. They are this low because none of the three files has any shared setup to pay for: the tests call pure functions, plus one hand-written test double at `test/helpers/mailer.js`. There is no database, no build step and no fixture to construct, so the per-mutant cost is close to the cost of starting the runner.

### Two things that will confuse you if you recompute from the raw JSON

**The mutant counts above are what Stryker ran, not what it generated.** Excluding an operator does not drop its mutants from the report; they are recorded with status `Ignored` and left out of the score. `reports/mutation-reduced/report.json` lists eleven mutants for `src/dates.js`, seven ignored and four run, and its 50.00% is 2 killed over those 4. Recompute a score as killed plus survived plus timeout, never as the length of the array.

**The generated population is not fixed either.** `src/alerts.js` yields ten mutants under the full operator set and eleven under the reduced one. Stryker's `CallExpression` mutator carries `filter(mutantsInScope) { return mutantsInScope.length === 1 }`, so it fires only when it is the only mutant in scope: the `ArrowFunction` mutant at line 8 suppresses it in the full run, and excluding `ArrowFunction` lets it through. Narrowing an operator set can add a mutant. This is why two scores from different operator sets are not comparable even in principle, and not merely hard to compare.

## What each file is for

One line of purpose each, then the survivors from the full run as the report records them. The reading of those survivors is on [`mutation-testing.md`](../guides/mutation-testing.md); what is here is the evidence that page reads.

**`src/discount.js`** — a percentage cap the two tests execute without exercising. Nine mutants, three survivors:

| Mutator | Line | Replacement |
| --- | --- | --- |
| `EqualityOperator` | 4 | `pct >= 50` |
| `BlockStatement` | 4 | `{}` |
| `ConditionalExpression` | 4 | `false` |

**`src/dates.js`** — a two-guard clamp whose tests pin both boundaries. Eleven mutants, nine killed, two survivors, both of them guard comparisons:

| Mutator | Line | Replacement |
| --- | --- | --- |
| `EqualityOperator` | 4 | `day >= 31` |
| `EqualityOperator` | 7 | `day <= 1` |

**`src/alerts.js`** — a severity guard and a deferred send, against the test double at `test/helpers/mailer.js`. Ten mutants, ten survivors, nothing killed:

| Mutator | Line | Replacement |
| --- | --- | --- |
| `BlockStatement` | 4 | `{}` |
| `ConditionalExpression` | 5 | `true` |
| `ConditionalExpression` | 5 | `false` |
| `EqualityOperator` | 5 | `event.severity === 'critical'` |
| `StringLiteral` | 5 | `""` |
| `BlockStatement` | 5 | `{}` |
| `BooleanLiteral` | 6 | `true` |
| `ArrowFunction` | 8 | `() => undefined` |
| `StringLiteral` | 8 | <code>``</code> |
| `BooleanLiteral` | 9 | `false` |

The two tests assert `sentCount() === 0` and pass. Delivery is deferred to a microtask, so that count reads 0 whether or not anything was sent, which is why every row above survives.

## Why the score moves with the operator set

The same file, the same tests, two operator sets:

| `src/dates.js` | Mutants run | Killed | Survived | Score |
| --- | --- | --- | --- | --- |
| Full operator set | 11 | 9 | 2 | 81.82% |
| Equality operator alone | 4 | 2 | 2 | 50.00% |

The survivors are the same two mutants in both rows: `day >= 31` and `day <= 1`. Only the denominator moved, from 2 unkilled out of 11 to 2 out of 4.

## A caveat on these numbers

They are exact for the versions pinned above and they are not a promise about yours. Stryker's operator set changes between majors, so a later version may generate a different number of mutants on this same unchanged code and report a different score. The count of installed mutators quoted above is the count for 10.0.0. If your run disagrees, compare mutant counts before concluding anything went wrong.
