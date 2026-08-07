# References

The outside sources behind the code, test, and review guides here. Most lines note the principle taken and where it shows up; a couple are general background. Books are by title and author; confirm the current edition when buying. Links verified 2026-07-30.

## Code quality and design

- **A Philosophy of Software Design, 2nd ed.**, John Ousterhout (2021). Complexity is the core problem; prefer deep modules to shallow ones. Behind `code-writing`'s "complexity is what you are managing."
- **Working Effectively with Legacy Code**, Michael Feathers (2004). Seams and testability; hard-to-test is a design signal. Behind the dependency-injection and design-for-test principles.
- **Refactoring, 2nd ed.**, Martin Fowler (2018). The code-smell catalogue and safe transformations. Behind the structural-craft pass; naming a specific refactoring gives author and reviewer a shared vocabulary.
- **The Pragmatic Programmer, 20th Anniversary ed.**, Hunt & Thomas (2019). Broad craft foundations, most centrally DRY (coined here) and orthogonality. (YAGNI comes from Extreme Programming, not this book.)
- **Tidy First?**, Kent Beck (2023). The economics of small structural cleanups and when to defer them. Behind separating tidying from behaviour change.
- **Code Complete, 2nd ed.**, Steve McConnell (2004). General background rather than the source for any single rule here: the exhaustive construction reference, kept as a lookup.

## Testing

- **Test-Driven Development by Example**, Kent Beck (2002). Red, green, refactor. Behind `test-writing`'s tests-first.
- **Growing Object-Oriented Software, Guided by Tests**, Freeman & Pryce (2009). Tests as design pressure: hard-to-test is a design signal, and the tests drive the object design. Behind `test-writing`'s "tests are design pressure." (It makes the mockist / London-school case; the prefer-a-real-collaborator stance here is the classicist counterview, not GOOS's own.)

## Code review

- **Google's Code Review Developer Guide** (google.github.io/eng-practices). The approve standard: improve the overall health of the system, not chase perfection. Behind the verdict rule. (The collaborative, inquisitive register in `review-voice` is my own, not Google's.)
- **Best Kept Secrets of Peer Code Review**, Jason Cohen / SmartBear (2006; the Cisco case-study chapter is free online). Annotate first, keep reviews to 200 to 400 lines and under an hour. Behind the size-and-pace section.
- **Conventional Comments** (conventionalcomments.org). A label vocabulary (`nit:`, `issue:`, `suggestion:`) that makes the blocking-versus-non-blocking distinction unmistakable.

## Links

[A Philosophy of Software Design, 2nd ed.](https://www.amazon.com/Philosophy-Software-Design-2nd/dp/173210221X) · [Google eng-practices (reviewer)](https://google.github.io/eng-practices/review/reviewer/) · [Best Kept Secrets of Peer Code Review (free PDF chapter)](https://static0.smartbear.co/support/media/resources/cc/book/code-review-cisco-case-study.pdf) · [Conventional Comments](https://conventionalcomments.org/)
