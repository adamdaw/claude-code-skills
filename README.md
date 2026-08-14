# Claude Code skills

Agent skills and the guides behind them, written down so they can be reused. The skills
live in [`skills/`](skills/), one directory each, in the Agent Skills format any harness
that loads Markdown skills can read. The craft guides they defer to live in
[`guides/`](guides/).

| Skill | What it does |
| --- | --- |
| [`senior-code-review`](skills/senior-code-review/SKILL.md) | Reviews a PR, a diff, or a change. Reads cold, reads the checked-out code rather than the patch, walks four passes, reconciles against the live thread, works it finding by finding to a hold-or-approve recommendation. Never posts a binding approval. |
| [`spec-review`](skills/spec-review/SKILL.md) | Reviews a GitHub work-item issue **as a spec**, before anyone builds it. Spawns a fresh read-only subagent that reads only the published issue and its tracker ticket, reports findings, and cannot implement. |
| [`brevity-enforcer`](skills/brevity-enforcer/SKILL.md) | Cuts a durable doc (ADR, spec, plan, design doc, issue body) down to length without softening an RFC 2119 keyword or flipping the register. Ships `cutcheck.py` so the check is mechanical rather than eyeballed. |
| [`pr-neighbors`](skills/pr-neighbors/SKILL.md) | Finds the open PRs that impact, or are impacted by, the one you're about to review or merge. |
| [`claims-verifier`](skills/claims-verifier/SKILL.md) | Reviews a document's claims adversarially, before it ships. Spawns a fresh read-only subagent that attempts to refute every factual and logical claim against the document's own evidence, verdicts each (supported / unsupported / contradicted / unverifiable), and loops until a cold pass comes back clean. The partner to `senior-code-review`, for prose. |

`pr-neighbors` was a team-mate's idea.

Most of what follows is about the first one, because the review method is the part with
the most written down.

## A code review method

This is how I run code review, written down so it can be reused. It's a stance and a procedure, not a linter: the reviewer, human or model, reads the change and reports, and a human weighs whether to merge. The principles are portable across stacks, though the examples lean on common object-oriented and git-based conventions, so translate them where yours differ. Where your stack has a concrete form of a rule, that's where you apply it.

The method comes out of everyday practice and the better writing on the subject (see [`references.md`](guides/references.md)). It's opinionated, and I've tried to say why at each turn rather than just hand down rules.

### The one idea

The reviewer, whether it's a person or a model, reads the change cold and reports. It doesn't approve. A human posts the review, and the team's approval gate (two humans, in my case) is what clears a merge. Everything else follows from that: the goal is to get the most honest, independent read possible *into* a human decision, never to replace it.

If you take one thing from this repo, take that. The rest is just how to make the read honest, how to keep the output kind, and how to stop at the gate.

### The pieces

- **[`skills/senior-code-review`](skills/senior-code-review/SKILL.md)**, the procedure as an agent skill: read cold, read the checked-out code in a worktree, walk four passes, reconcile against the live thread, work it finding by finding, stop at the human gate. Drop it into an agent harness that loads Markdown skills in the Agent Skills format, or just read it as a checklist.
- **[`running-a-review.md`](guides/running-a-review.md)**, the same procedure for a human, plus the checklist of what a review looks for, dimension by dimension. Each dimension is a portable principle you fill in with your own stack's rules.
- **[`review-voice.md`](guides/review-voice.md)**, how a finding gets written: collaborative, inquisitive, terse. The register is the part most people skip, and it's what separates a review that helps from one that merely corrects.
- **[`code-writing.md`](guides/code-writing.md)** / **[`test-writing.md`](guides/test-writing.md)**, the craft principles a review holds a change to. The review checks the code against these, so they're worth stating on their own.
- **[`references.md`](guides/references.md)**, the outside sources behind all of it, with what each one contributes.

### Using it

Two ways, and they share one spine.

- **As an agent skill.** Point your coding agent at `skills/senior-code-review/SKILL.md`. It runs the procedure and hands you back a recommendation and a draft. It never posts and never approves; those stay yours.
- **As human guides.** Read `guides/running-a-review.md` before a review and `guides/review-voice.md` before writing the comment, as working references you return to, not essays to read once.

Either way the line is firm: no model casts a binding approval, and a human holds the merge gate.

Two caveats. The operational spine assumes a git and pull-request workflow (a worktree checkout, a live review thread, a merge gate). The craft principles don't, but the procedure does, so translate the mechanics if your version control or review tool differs. And the files are meant to travel together: the skill carries the procedure and defers to the guides for the house checklist and the register, so keep them side by side.

### Adapting it to your stack

The dimensions and principles are portable; the *house form* of each is yours to fill in. Where a guide says "enforce access control at the data layer" or "inject collaborators through a substitutable seam", the concrete API, framework, and convention are specific to your codebase. Keep those specifics in your own rules files and let these guides point at them. That separation is on purpose: the principle is stable, the house rule changes with the stack.

### License

MIT. See [`LICENSE`](LICENSE).
