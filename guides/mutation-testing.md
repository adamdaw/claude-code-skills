# Mutation testing, in five minutes

What it is, why it is worth the time, and how to run one by hand with no tooling to install. The vocabulary and the manual loop are portable; the operators, the tool, and the cost of a test run belong to your stack, so translate those. Sources are in [`references.md`](references.md).

The examples are ours rather than borrowed from somebody's real codebase, but they are real code, not illustrations. They live in [`examples/`](../examples/), and every number on this page comes from a recorded run. Three commands produce them between them, one for coverage and two for the two operator sets; [`examples/README.md`](../examples/README.md) lists all three against the figures each one produces.

## The one-sentence version

Break the code on purpose and see whether any test complains.

## A worked example

A discount helper with a cap:

```js
export function applyDiscount(amount, pct) {
  if (pct > 50) {
    pct = 50;
  }
  return amount - (amount * pct) / 100;
}
```

And two tests:

```js
test('applies ten percent', () => {
  assert.equal(applyDiscount(100, 10), 90, 'ten percent off 100');
});

test('handles a large percentage', () => {
  assert.notEqual(applyDiscount(100, 80), null, 'returns a value');
});
```

Every line of the method runs, and so do both branches of the guard. Measured, that is 100% of lines, 100% of branches and 100% of functions, which is every dimension the runner reports.

Now delete the cap:

```js
export function applyDiscount(amount, pct) {
  return amount - (amount * pct) / 100;
}
```

Both tests still pass. The first never sends a percentage above 50, and the second only checks that *something* came back. The cap, the only interesting logic in the method, is executed by the suite and verified by nothing.

That deletion is a **mutant**: one small deliberate defect. Because the tests stayed green, the mutant **survived**. Had a test failed, the mutant would have been **killed**, which is the outcome you want. It is a survivor in the recorded run too, reported as `BlockStatement` at line 4 with the cap body emptied, one of three survivors out of nine mutants on that file.

## Why coverage cannot tell you this

Coverage measures which lines ran. It has no opinion on whether anything checked the result. A test with no assertion still produces full coverage of everything it touches, and so does a test whose only assertion is `assertNotNull(result)`.

Mutation testing measures something different. Take a change to this code and ask whether some test notices. That is the question you care about, whether the suite would catch a regression. Note what it is not: the changes that get tried are not every change you could make. A tool works from a fixed set of operators, over the files you point it at. Both bounds come up further down, and both matter when you read a score.

The number it produces is the **mutation score**, mutants killed divided by mutants attempted. That is what a tool reports, and it is not the only definition in use. The standard survey of the field puts *non-equivalent* mutants in the denominator instead, and on that definition a perfect score is both attainable and the goal. A tool cannot compute that denominator, because deciding whether a mutant is equivalent is undecidable, so it leaves the unkillable ones in and its score cannot reach 100%. Two definitions, one word: treat the number as the least portable thing on this page. The date helper in `examples/` scores 81.82% across eleven mutants under the full operator set, and 50.00% across four when only the equality operator runs. Same code, same tests, a swing of nearly 32 points. Narrowing the operators did not make the suite worse, it shrank the denominator, and the two unkillable mutants in it went from a fifth of the total to half. A score is comparable only against another score from the same operator set, so read the mutant count before you read the score.

## Why it is worth the time

**It turns a review opinion into a fact.** "That assertion looks thin" is something the author can reasonably argue with. "Delete this line and nothing in the suite goes red" is not.

**It names the assertion you are missing.** Coverage tells you a line is untested, which leaves you to work out what to write. A survivor tells you the exact change nobody detects, which is usually the content of the assertion you need. Sometimes it tells you no assertion would help. Two survivor shapes are worked below, and telling them apart is the reading that matters: in one, no assertion could have helped, and in the other the suite could assert its way to a kill and does not.

**It gives acceptance criteria a checkable form.** "When the delimiter changes, this test fails" can be verified. "Tests verify the parsing behaviour" cannot.

**Done by hand it is two test runs**, on the one line you already doubt. You need no tooling and nobody's permission.

## Not every survivor is a bug

Change `pct > 50` to `pct >= 50` in the original method. At exactly 50 the cap now fires and sets `pct` to 50, which it already was. No test can tell the difference, because there is no difference. That is an **equivalent mutant**, and it is unkillable by construction. It is one of the three survivors on that file.

They are common enough that the field named the problem and built a literature on detecting them, and undecidability means that literature is about heuristics rather than answers. This is why a tool-reported 100% is not the goal, and why the score is the least interesting output. Read the list of survivors instead. Each one is a sentence of the form "you can change this and nobody notices", and you decide case by case whether that matters.

An equivalent mutant is also design information: a change that *cannot* alter behaviour is a change that does not matter, which is worth knowing next time somebody argues about that line. Mind the bound, though. A change nothing could observe is not the same as a change your suite happens to miss, and the second kind matters a great deal. There is one of those further down this page.

## How to run one, by hand

One mutant, one line, one named victim. Five steps:

1. **Pick the line that carries the logic.** The guard, the cap, the comparison, whatever you would be nervous to get backwards.
2. **Name the test you expect to fail, before you run anything.** Say it out loud or write it in the review comment. This step is the method: if you cannot name a victim, you already have your answer.
3. **Break the line.** Delete it, invert the comparison, or return null. One change, not two.
4. **Run the suite.** The test you named must fail. If a *different* test fails instead, read it, because the one you named may not check what its name says.
5. **Restore the line and re-run.** Back to the baseline you started from. A red that survives the restore is not your mutant; a flaky suite or a stale environment reds a run without any help from you.

**If your tests run against a built or deployed copy, restoring means rebuilding it.** Reverting the file in your working tree leaves the broken version live in whatever the test run actually reads. This one is easy to get caught by, and a mutant left in place across a break produces failures that read as real defects. Rebuild, then confirm the running code matches your tree before you believe any red. Where tests compile and run straight from the working tree there is nothing to go stale, but the mutation is still written to that tree, so step 5 still applies.

That is the whole technique. It is worth making a habit, because "all tests green" is not by itself proof that a new guard does anything.

## What it costs

By hand: two test runs, one mutated and one restored, plus the few seconds of thinking that step 2 takes.

By tool, the default cost model is one test run per mutant. Code producing 100 mutants costs 100 test runs unless the tool groups them, and where a run means deploying the mutated code and waiting, that should land hardest on suites with expensive shared setup, though I have not timed it. Do not read the second here as typical: 30 mutants across three tiny files finish in about a second, because there is nothing to set up. The manual form is targeted and cheap, the automated form broad and expensive. They do not compete, and you do not need the second one to start.

The examples here use Stryker, for JavaScript. PIT is the long-established one for the JVM, and most ecosystems now have an equivalent. They work the same way: parse the code, generate mutants across the files you point them at, run the suite against each one, and score the results. Coverage data, where a tool uses it, narrows which tests run per mutant rather than which lines get mutated, and the runs behind this page have that analysis switched off.

## What a survivor looks like

Two of the three files under [`examples/src/`](../examples/src) exist for this section, one of each shape. All three have 100% line and branch coverage.

**A score below 100 is not a defect list.** `dates.js` clamps a day number into the range 1 to 31 and scores 81.82%: eleven mutants, nine killed, two survivors. Both survivors are the same operator change, `day > 31` widened to `day >= 31` and `day < 1` to `day <= 1`, and both are equivalent mutants. At exactly 31 the mutated guard fires and assigns 31, which `day` already held. Correct result, nothing to fix.

Note the split of labour there. Stryker reported those two as *survived*. That they are *equivalent* is the reading you do afterwards, by arguing about the code. No mutation tool decides equivalence for you, which is most of why the survivor list matters more than the number does.

**A suite can assert, pass, and still detect nothing.** `alerts.js` hands an alert message to an injected mailer when a critical event arrives, and it scores 0%: ten mutants, ten survivors, nothing killed. Its two tests carry real equality assertions with messages, and they pass. Delivery is deferred to a microtask, so the mailer's sent count still reads 0 when the assertion runs, whether or not anything was sent, and asserting 0 was a deliberate choice to keep the test deterministic. Deleting the send outright, inverting the guard, emptying the guard body, blanking the alert string: all ten changes pass unnoticed.

That second shape is what this technique exists to find. Complete line coverage, complete branch coverage, real passing assertions, and a static analyzer sees nothing wrong, because nothing is missing. The assertion is right there.

## When not to bother

Mutating code with no logic in it wastes a few seconds. Getters, constructors, and pass-through wrappers produce mutants nobody should care about.

The technique earns its time on branching logic: guards, caps, validation, anything with a boundary. Ask "would a test catch it if I got this comparison backwards?" If you cannot answer straight away, mutate it. If the answer is obviously yes, do not.

## The one habit worth keeping

Before you say a test proves something, break the thing it proves and watch it go red.

See also: [`examples/`](../examples/) for the code and the recorded numbers, [`test-writing`](test-writing.md) for why coverage is a floor, and [`references.md`](references.md) for the sources behind this page.
