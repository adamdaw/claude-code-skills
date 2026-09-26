# References

The outside sources behind the guides here. Most lines note the principle taken and where it shows up; a couple are general background. Books are by title and author; confirm the current edition when buying. Links verified 2026-09-26; the Jia & Harman entry links to the ACM record and the McKinsey entry to mckinsey.com, and both refuse automated requests, so check them in a browser rather than a script.

## Code quality and design

- **A Philosophy of Software Design, 2nd ed.**, John Ousterhout (2021). Complexity is the core problem; prefer deep modules to shallow ones. Behind W-guide §2 (Manage complexity).
- **Working Effectively with Legacy Code**, Michael Feathers (2004). Seams and testability; hard-to-test is a design signal. Behind the named techniques in F-guide §4 (Capture existing behaviour) through F-guide §7 (Sprout or wrap when adding behaviour), and T-guide §8 (Hard to test means entangled).
- **Refactoring, 2nd ed.**, Martin Fowler (2018). The code-smell catalogue and safe transformations. Behind the Structure dimension in R-guide §7 (What to look for: the eight dimensions); naming a specific refactoring gives author and reviewer a shared vocabulary.
- **The Pragmatic Programmer, 20th Anniversary ed.**, Hunt & Thomas (2019). Broad craft foundations, most centrally DRY (coined here) and orthogonality. DRY is behind W-guide §4 (Duplication and speculation). (YAGNI comes from Extreme Programming, not this book.)
- **Tidy First?**, Kent Beck (2023). The economics of small structural cleanups and when to defer them. Behind separating tidying from behaviour change in F-guide §3 (Tidy only what you touch).
- **Code Complete, 2nd ed.**, Steve McConnell (2004). General background rather than the source for any single rule here: the exhaustive construction reference, kept as a lookup.

## Testing

- **Test-Driven Development by Example**, Kent Beck (2002). Red, green, refactor. Behind T-guide §1 (Start at the outside).
- **Growing Object-Oriented Software, Guided by Tests**, Freeman & Pryce (2009). Tests as design pressure: hard-to-test is a design signal, and the tests drive the object design. Behind T-guide §8 (Hard to test means entangled). (It makes the mockist / London-school case, outside-in; the prefer-a-real-collaborator stance here is the classicist counterview, not GOOS's own.)
- **Mocks Aren't Stubs**, Martin Fowler (2007, martinfowler.com, free). Meszaros's double taxonomy (dummy, fake, stub, spy, mock), state verification against behaviour verification, and the classical / mockist split with its real tradeoffs. Behind T-guide §4 (Name the double; verify at most one interaction), including the classical default and the instruction to name the double rather than calling everything a mock.

## Mutation testing

- **An Analysis and Survey of the Development of Mutation Testing**, Jia & Harman (IEEE TSE 37(5), 2011). The standard survey: operator families, the equivalent-mutant problem, and the cost-reduction strategies. Source of the vocabulary in `mutation-testing`: a mutant is killed when it gives a different output, and "otherwise it is said to have survived". It defines the mutation score over *non-equivalent* mutants, so on its definition a score of 1 is the goal, and it cites Budd and Angluin for the proof that deciding equivalence is undecidable. Both halves are behind this page's two-definitions paragraph.
- **State of Mutation Testing at Google**, Petrović & Ivanković (ICSE-SEIP 2018; free PDF). Mutation analysis made affordable on a very large repo by mutating only changed lines, omitting lines without statement coverage, and suppressing "arid" lines that yield uninteresting mutants. They define the mutation score over the total number of mutants, which is the tool-reported form this page uses, and then decline to surface it: computing it across the repo is infeasible and they "were also unable to find a good way to surface it to the engineers in an actionable way". Survivors go to code review instead, where a developer can dismiss one as not useful in a click. Behind `mutation-testing`'s "read the survivors, not the score."
- **PIT** (pitest.org). The long-established mutation tool for the JVM, and the reference implementation of the tool-driven form.

## Code review

- **Programming as Theory Building**, Peter Naur (1985, 14pp, free). A program is not its text but a theory held by the people who built it, covering what the world is assumed to be like and why the code has the shape it does; a program whose team has dispersed is dead, and documentation cannot revive it, being text too. Behind R-guide §1 (What a review is for): if the theory only moves between people, review is how it reaches a second head, which is why a review that finds nothing still worked and why "why is it done this way?" outranks most defects. Also behind D-guide §2 (A finding needs evidence), where a reason nobody can recover is debt. Short but not light, and worth a second reading.
- **Google's Code Review Developer Guide** (google.github.io/eng-practices). The approve standard: improve the overall health of the system, not chase perfection. Behind the verdict rule in R-guide §12 (Verdict). (The collaborative, inquisitive register in R-guide §11 (Writing a finding) is my own, not Google's.) Discount for context: Google has a monorepo, heavy tooling and a readability-certification process, so the approve standard transfers everywhere and some of the machinery doesn't.
- **Best Kept Secrets of Peer Code Review**, Jason Cohen / SmartBear (2006; the Cisco case-study chapter is free online). Annotate first, keep reviews to 200 to 400 lines and under an hour. Behind R-guide §6 (Size, pace, scope). Read the figures as order-of-magnitude rather than gospel: 2006, C and C++, a pre-GitHub tool. Its least-quoted finding deserves more use than its most, with a caveat: authors who annotate their own change before review are associated with markedly fewer defects. Cohen offers two explanations that, in his words, "lead to opposite conclusions about whether author preparation should be mandatory" — that explaining the change makes the author find defects themselves, or that annotation primes the reviewer to read along with the author's account and look less hard. He judges the first more tenable from a manual survey of the reviews, but does not demonstrate it.
- **Conventional Comments** (conventionalcomments.org). A label vocabulary (`nit:`, `issue:`, `suggestion:`) that makes the blocking-versus-non-blocking distinction unmistakable. Behind the labels in R-guide §11 (Writing a finding).

## Specifying

- **Easy Approach to Requirements Syntax (EARS)**, Alistair Mavin, Philip Wilkinson, Adrian Harwood and Mark Novak (IEEE International Requirements Engineering Conference, 2009). The six requirement forms. Behind S-guide §2 (Use canonical EARS).

## Technical debt

- **The WyCash Portfolio Management System**, Ward Cunningham (OOPSLA '92 Experience Report, 1992). The debt metaphor: "Every minute spent on not-quite-right code counts as interest on that debt." Behind D-guide §3 (Weigh it: debt that matters), where debt compounds through change.
- **Technical Debt Quadrant**, Martin Fowler (2009, martinfowler.com, free). Reckless or prudent, deliberate or inadvertent: a way to name where debt came from without blame. Background for *On Technical Debt*.
- **Your Code as a Crime Scene**, Adam Tornhill (Pragmatic Bookshelf, 2015; 2nd edition 2024). Hotspots: code complexity combined with change frequency, from version history. Behind D-guide §3 (Weigh it: debt that matters).
- **The Developer Coefficient**, Stripe and Harris Poll (2018). Developers estimate 13.5 hours of a 41.1-hour week go on technical debt. Self-reported and vendor-commissioned: directional, not a benchmark. Cited in D-guide §7 (Run a debt assessment).
- **Tech debt: Reclaiming tech equity**, Dalal, Krishnakanthan, Münstermann and Patenge, McKinsey Digital (2020). CIOs estimate tech debt at 20 to 40% of the value of their technology estate, before depreciation. Self-reported, 50 CIOs: directional, not a benchmark. Cited in D-guide §7 (Run a debt assessment).

## Links

[A Philosophy of Software Design, 2nd ed.](https://www.amazon.com/Philosophy-Software-Design-2nd/dp/173210221X) · [Programming as Theory Building (PDF)](https://pages.cs.wisc.edu/~remzi/Naur.pdf) · [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html) · [State of Mutation Testing at Google (PDF)](https://research.google.com/pubs/archive/46584.pdf) · [Jia & Harman survey](https://dl.acm.org/doi/10.1109/TSE.2010.62) · [PIT](https://pitest.org/) · [Google eng-practices (reviewer)](https://google.github.io/eng-practices/review/reviewer/) · [Best Kept Secrets of Peer Code Review (free PDF chapter)](https://static0.smartbear.co/support/media/resources/cc/book/code-review-cisco-case-study.pdf) · [Conventional Comments](https://conventionalcomments.org/) · [The WyCash Portfolio Management System](http://c2.com/doc/oopsla92.html) · [Technical Debt Quadrant](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html) · [The Developer Coefficient (PDF)](https://d37ugbyn3rpeym.cloudfront.net/newsroom/the-developer-coefficient.pdf) · [Tech debt: Reclaiming tech equity](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/tech-debt-reclaiming-tech-equity)
