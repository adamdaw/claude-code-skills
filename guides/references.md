# References

The outside sources behind the code, test, and review guides here. Most lines note the principle taken and where it shows up; a couple are general background. Books are by title and author; confirm the current edition when buying. Links verified 2026-08-19; the Jia & Harman entry links to the ACM record, which refuses automated requests, so check it in a browser rather than a script.

## Code quality and design

- **A Philosophy of Software Design, 2nd ed.**, John Ousterhout (2021). Complexity is the core problem; prefer deep modules to shallow ones. Behind `code-writing`'s "complexity is what you are managing."
- **Working Effectively with Legacy Code**, Michael Feathers (2004). Seams and testability; hard-to-test is a design signal. Behind the dependency-injection and design-for-test principles.
- **Refactoring, 2nd ed.**, Martin Fowler (2018). The code-smell catalogue and safe transformations. Behind the structural-craft pass; naming a specific refactoring gives author and reviewer a shared vocabulary.
- **The Pragmatic Programmer, 20th Anniversary ed.**, Hunt & Thomas (2019). Broad craft foundations, most centrally DRY (coined here) and orthogonality. (YAGNI comes from Extreme Programming, not this book.)
- **Tidy First?**, Kent Beck (2023). The economics of small structural cleanups and when to defer them. Behind separating tidying from behaviour change.
- **Code Complete, 2nd ed.**, Steve McConnell (2004). General background rather than the source for any single rule here: the exhaustive construction reference, kept as a lookup.

## Testing

- **Test-Driven Development by Example**, Kent Beck (2002). Red, green, refactor. Behind `test-writing`'s tests-first.
- **Growing Object-Oriented Software, Guided by Tests**, Freeman & Pryce (2009). Tests as design pressure: hard-to-test is a design signal, and the tests drive the object design. Behind `test-writing`'s "tests are design pressure." (It makes the mockist / London-school case, outside-in; the prefer-a-real-collaborator stance here is the classicist counterview, not GOOS's own.)
- **Mocks Aren't Stubs**, Martin Fowler (2007, martinfowler.com, free). Meszaros's double taxonomy (dummy, fake, stub, spy, mock), state verification against behaviour verification, and the classical / mockist split with its real tradeoffs. Behind `test-writing`'s Test doubles section, including the classical default and the instruction to name the double rather than calling everything a mock.

## Mutation testing

- **An Analysis and Survey of the Development of Mutation Testing**, Jia & Harman (IEEE TSE 37(5), 2011). The standard survey: operator families, the equivalent-mutant problem, and the cost-reduction strategies. Source of the vocabulary in `mutation-testing`: a mutant is killed when it gives a different output, and "otherwise it is said to have survived". It defines the mutation score over *non-equivalent* mutants, so on its definition a score of 1 is the goal, and it cites Budd and Angluin for the proof that deciding equivalence is undecidable. Both halves are behind this page's two-definitions paragraph.
- **State of Mutation Testing at Google**, Petrović & Ivanković (ICSE-SEIP 2018; free PDF). Mutation analysis made affordable on a very large repo by mutating only changed lines, omitting lines without statement coverage, and suppressing "arid" lines that yield uninteresting mutants. They define the mutation score over the total number of mutants, which is the tool-reported form this page uses, and then decline to surface it: computing it across the repo is infeasible and they "were also unable to find a good way to surface it to the engineers in an actionable way". Survivors go to code review instead, where a developer can dismiss one as not useful in a click. Behind `mutation-testing`'s "read the survivors, not the score."
- **PIT** (pitest.org). The long-established mutation tool for the JVM, and the reference implementation of the tool-driven form.

## Code review

- **Programming as Theory Building**, Peter Naur (1985, 14pp, free). A program is not its text but a theory held by the people who built it, covering what the world is assumed to be like and why the code has the shape it does; a program whose team has dispersed is dead, and documentation cannot revive it, being text too. Behind `running-a-review`'s "what a review is for": if the theory only moves between people, review is how it reaches a second head, which is why a review that finds nothing still worked and why "why is it done this way?" outranks most defects. Short but not light, and worth a second reading.
- **Google's Code Review Developer Guide** (google.github.io/eng-practices). The approve standard: improve the overall health of the system, not chase perfection. Behind the verdict rule. (The collaborative, inquisitive register in `review-voice` is my own, not Google's.) Discount for context: Google has a monorepo, heavy tooling and a readability-certification process, so the approve standard transfers everywhere and some of the machinery doesn't.
- **Best Kept Secrets of Peer Code Review**, Jason Cohen / SmartBear (2006; the Cisco case-study chapter is free online). Annotate first, keep reviews to 200 to 400 lines and under an hour. Behind the size-and-pace section. Read the figures as order-of-magnitude rather than gospel: 2006, C and C++, a pre-GitHub tool, though the shape of the curve has held up better than the exact numbers. Its least-quoted finding deserves more use than its most: authors who annotate their own change before review find defects themselves, in the act of explaining it.
- **Conventional Comments** (conventionalcomments.org). A label vocabulary (`nit:`, `issue:`, `suggestion:`) that makes the blocking-versus-non-blocking distinction unmistakable.

## Links

[A Philosophy of Software Design, 2nd ed.](https://www.amazon.com/Philosophy-Software-Design-2nd/dp/173210221X) · [Programming as Theory Building (PDF)](https://pages.cs.wisc.edu/~remzi/Naur.pdf) · [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html) · [State of Mutation Testing at Google (PDF)](https://research.google.com/pubs/archive/46584.pdf) · [Jia & Harman survey](https://dl.acm.org/doi/10.1109/TSE.2010.62) · [PIT](https://pitest.org/) · [Google eng-practices (reviewer)](https://google.github.io/eng-practices/review/reviewer/) · [Best Kept Secrets of Peer Code Review (free PDF chapter)](https://static0.smartbear.co/support/media/resources/cc/book/code-review-cisco-case-study.pdf) · [Conventional Comments](https://conventionalcomments.org/)
