# Claude Code skills

Agent skills and the guides behind them, written down so they can be reused. The skills
live in [`skills/`](skills/), one directory each, in the Agent Skills format any harness
that loads Markdown skills can read. The guides they defer to live in
[`guides/`](guides/), listed [below](#the-guides).

Take the repo whole rather than lifting a single skill directory out of it. The skills
link into `guides/` by relative path, and the guides link into `examples/`, so a skill
installed on its own loses the material it defers to.

| Skill | What it does |
| --- | --- |
| [`senior-code-review`](skills/senior-code-review/SKILL.md) | Reviews a PR, a diff, or a change. Reads cold, reads the checked-out code rather than the patch, walks four passes, reconciles against the live thread, works it finding by finding to a hold-or-approve recommendation. Never posts a binding approval. |
| [`spec-review`](skills/spec-review/SKILL.md) | Reviews a GitHub work-item issue **as a spec**, before anyone builds it. Spawns a fresh read-only subagent that reads only the published issue and its tracker ticket, reports findings, and cannot implement. |
| [`brevity-enforcer`](skills/brevity-enforcer/SKILL.md) | Cuts a durable doc (ADR, spec, plan, design doc, issue body) down to length without softening an RFC 2119 keyword or flipping the register. Ships `cutcheck.py` so the check is mechanical rather than eyeballed. |
| [`pr-neighbors`](skills/pr-neighbors/SKILL.md) | Finds the open PRs that impact, or are impacted by, the one you're about to review or merge. |
| [`claims-verifier`](skills/claims-verifier/SKILL.md) | Reviews a document's claims adversarially, before it ships. Spawns a fresh read-only subagent that attempts to refute every factual and logical claim against the document's own evidence, verdicts each (supported / unsupported / overclaimed / contradicted / unverifiable), and loops until two distinct cold passes come back clean over identical bytes. The partner to `senior-code-review`, for prose. |

`pr-neighbors` was a team-mate's idea.

## The guides

Each guide is a numbered checklist with a one-letter prefix, so a line can be cited as "X-guide §N (Title)", for example "R-guide §11 (Writing a finding)".

| Prefix | Guide | What it covers |
| --- | --- | --- |
| W | [`code-writing.md`](guides/code-writing.md) | Writing a change: the whole path first, complexity, naming, correctness, failure, writing it up, and self-review over the eight dimensions. |
| F | [`refactoring.md`](guides/refactoring.md) | Changing existing code: explain before you edit; build, ask, defer, don't; tidying; characterization tests, seams, sprout and wrap. |
| T | [`test-writing.md`](guides/test-writing.md) | Writing and reviewing tests: the six kinds of test, doubles, edge families, and what hard to test means. |
| R | [`running-a-review.md`](guides/running-a-review.md) | Code review: reading order, the eight dimensions, triage, weighing a finding, writing it, and the verdict. |
| S | [`specifying.md`](guides/specifying.md) | Writing and reviewing an SRS, an SDD or a ticket: SHALL and EARS, the registers, spec review and fidelity review. |
| P | [`writing.md`](guides/writing.md) | Professional, technical and personal writing: editing order, lexicon, registers, editorial conventions, accessibility, and the preservation check. |
| D | [`technical-debt.md`](guides/technical-debt.md) | Technical debt: sorting it from defects and preference, evidence, weighing, the debt ticket, assessments, and accepting inherited work. |

Two more files sit beside them without a prefix: [`mutation-testing.md`](guides/mutation-testing.md), a five-minute explainer, and [`references.md`](guides/references.md), the outside sources behind the guides.

Most of what follows is about the first one, because the review method is the part with
the most written down.

## A code review method

This is how I run code review, written down so it can be reused. It's a stance and a procedure, not a linter: the reviewer, human or model, reads the change and reports, and a human weighs whether to merge. The principles are portable across stacks, though the examples lean on common object-oriented and git-based conventions, so translate them where yours differ. Where your stack has a concrete form of a rule, that's where you apply it.

The method comes out of everyday practice and the better writing on the subject (see [`references.md`](guides/references.md)). It's opinionated, and I've tried to say why at each turn rather than just hand down rules.

### The one idea

The reviewer, whether it's a person or a model, reads the change cold and reports. It doesn't approve. A human posts the review, and the team's approval gate (an approval plus a required team review, in my case) is what clears a merge. Find out what your own gate is before you lean on this, because it changes what an approval means: where one is required, yours is the last independent check and "someone else will catch it" is false. Everything else follows from that: the goal is to get the most honest, independent read possible *into* a human decision, never to replace it.

And one idea underneath that one, about what the read is for. A program is not its text, it's the theory in the builders' heads (Naur), so the primary product of a review is a second person who holds that theory, and the defects are a valuable by-product. That's why a review that finds nothing still worked, why "I can't follow this" is a finding about the change rather than about you, and why the register in [R-guide §11 (Writing a finding)](guides/running-a-review.md#11-writing-a-finding) asks instead of instructing.

If you take those two from this repo, take them. The rest is just how to make the read honest, how to keep the output kind, and how to stop at the gate.

### The pieces

- **[`skills/senior-code-review`](skills/senior-code-review/SKILL.md)**, the procedure as an agent skill: read cold, read the checked-out code in a worktree, walk four passes, reconcile against the live thread, work it finding by finding, stop at the human gate. Drop it into an agent harness that loads Markdown skills in the Agent Skills format, or just read it as a checklist.
- **[`running-a-review.md`](guides/running-a-review.md)**, the R-guide: the same procedure for a human, plus the checklist of what a review looks for over the eight dimensions. Each dimension is a portable principle you fill in with your own stack's rules. R-guide §11 (Writing a finding) is how a finding gets written: collaborative, inquisitive, terse. The register is the part most people skip, and it's what separates a review that helps from one that merely corrects.
- **[`code-writing.md`](guides/code-writing.md)** / **[`test-writing.md`](guides/test-writing.md)**, the W-guide and T-guide a review holds a change to. The author's self-review, W-guide §9 (Self-review), walks the same eight dimensions a code review does.
- **[`mutation-testing.md`](guides/mutation-testing.md)**, how to check that a test would actually catch a regression: break the line on purpose and see whether anything goes red. A five-minute explainer with a worked example and a five-step manual loop you can run without installing anything. It's what turns "that assertion looks thin" from an opinion into a fact. Its figures come from [`examples/`](examples/), three small files you can run yourself; they carry 100% line and branch coverage and mutation scores of 0%, 81.82% and 66.67%.
- **[`references.md`](guides/references.md)**, the outside sources behind all of it, with what each one contributes.

### Using it

Two ways, and they share one spine.

- **As an agent skill.** Point your coding agent at `skills/senior-code-review/SKILL.md`. It runs the procedure and hands you back a recommendation and a draft. It never posts and never approves; those stay yours.
- **As human guides.** Read `guides/running-a-review.md` before a review and its §11 before writing the comment, as working references you return to, not essays to read once.

Either way the line is firm: no model casts a binding approval, and a human holds the merge gate.

Two caveats. The operational spine assumes a git and pull-request workflow (a worktree checkout, a live review thread, a merge gate). The craft principles don't, but the procedure does, so translate the mechanics if your version control or review tool differs. And the files are meant to travel together: the skill carries the procedure and defers to the guides for the house checklist and the register, so keep them side by side.

### Adapting it to your stack

The dimensions and principles are portable; the *house form* of each is yours to fill in. Where a guide says "enforce access control at the data layer" or "inject collaborators through a substitutable seam", the concrete API, framework, and convention are specific to your codebase. Keep those specifics in your own rules files and let these guides point at them. That separation is on purpose: the principle is stable, the house rule changes with the stack.

### License

MIT. See [`LICENSE`](LICENSE).
