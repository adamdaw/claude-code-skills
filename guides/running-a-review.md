# Running a review

How I run a review of a change. This is the human companion to [`senior-code-review.skill.md`](../skills/senior-code-review/SKILL.md); it covers *how the review runs* and *what it looks for*. The register findings get written in lives in [`review-voice.md`](review-voice.md), and the craft the review holds a change to lives in [`code-writing`](code-writing.md) and [`test-writing`](test-writing.md).

The whole thing serves one goal: an honest, independent read that feeds the human decision without standing in for it. The reviewer reads cold and reports. It never casts a binding approval. The team's approval gate is what clears a merge.

## Read cold (independence)

- **The review is independent.** I form the read with nobody else's findings in front of me and no conclusion pre-loaded, no statement of what I'm supposed to confirm. Hand the reviewer a conclusion and the conclusion is all it hands back.
- **The context lives in the artefact, not the ask.** The reviewer reads the diff and the checked-out code cold. Understanding comes from the code and from what the change says about itself, its description and ticket included. The author's own statement of intent, acceptance criteria and all, is fair to read: it is a claim to verify, not an instruction on what to conclude. What the reviewer refuses is a separate briefing that pre-loads the verdict. The line is who is talking: the change describing itself is context; a third party telling the reviewer what to find is a steer.
- **Converge by revising the artefact, not steering the reviewer.** In a review loop I want the code and its docs fixed so the *next* cold read doesn't surface the finding again. I don't tune the prompt to get a cleaner result; that just launders my own assumptions back to me.

## Read the checked-out code, not the diff

- **Anchor on the live diff first.** Confirm what actually changed against the base before reading, so you aren't reviewing already-merged or phantom content. A rebased-empty branch reads as real files but is a no-op diff.
- **Then read the change in context.** Check the branch out into a throwaway worktree beside your main clone and read the real files, not just the patch. The load-bearing facts are usually invisible in a diff: a default that turns a missing value into zero, an access grant the change depends on, a dependency version that quietly moved. The diff shows what changed; the working tree shows what it means in context. Keep the main clone a read-only reference; never mutate it for a review.

## The finding lifecycle

1. **Reconcile each candidate against the live thread.** Once you have candidate findings from the checklist below, re-fetch the head (the author may have pushed, even fixed the thing) and read the existing comments and reviews. Check the commit each approval and each automated finding was made against: an approval that predates the current head is stale, so flag it, and a bot finding computed on an older commit may be moot, so verify it against the live diff before repeating it. Already raised and open? Add weight only if you have something new. Already fixed on a newer commit? Drop it. Already dispositioned by the author as by-design? Engage the specific reasoning or accept it; don't re-post it as if it were unanswered. **"Do nothing" is a valid verdict** when the thread already covers the findings.
2. **Work it finding by finding, not as a finished solo draft.** Surface each finding as it clears the checklist: what it is, the evidence, whether it blocks. Size it there and then (drop, note as a nit or a follow-up ticket, hold, or fold into what gets posted), then the next. Do this with whoever runs the review with you, a co-reviewer or the agent's operator; the author meets it through the posted comments, downstream of this, not in the triage.
3. **Assemble the survivors** into one consolidated read, then re-voice it in the posting reviewer's register (see [`review-voice`](review-voice.md)) before anything goes out; a neutral or machine-produced draft isn't postable as-is. By then nothing in it is new to me. If nothing survives, add nothing.

## Verdict

- **Let the finding set the verdict; default to a hold on an unaddressed gap.** Decide approve-versus-hold *from* the finding, not before it. Green CI, a passing dry-run, and prior approvals don't clear a real gap. Withholding approval is the lever that stops an unverified merge.
- **A review is a progression, not a pass/fail gate.** There's no perfect code, only healthier code. The bar for approval is "does this improve the overall health of the system", not "is this flawless". That's what keeps default-to-hold from turning into perfectionism: hold on a genuine gap, not on polish, and let a clean change ship with its nits noted.
- **A clean approve gets no comment.** No paragraph narrating what you verified. The verification is the reviewer's job, not review content. Full phrasing rules in [`review-voice`](review-voice.md).

## What to look for, in your terms

Start from the standard dimensions. Each is the local form of a portable principle (see [`code-writing`](code-writing.md), [`test-writing`](test-writing.md)) applied through your stack's rules; hold a change to both the principle and its house rule. The house form below is written generically; fill in the concrete API and convention from your own codebase.

| Dimension | What to hold the change to |
| --- | --- |
| **Correctness & test coverage** | Exercise the real shape, not just a mock that returns what you told it (a mock hides a field the data layer dropped that a consumer then fails on, so guard the shape in the test that owns it). Prove *both* branches of a permission or feature gate, the negative path included. Every test carries its own assertion. Assert observable behaviour (returned data, side effects, rendered output, emitted events) over internals; a call-count assertion is fair only when the call is the behaviour (an email sent, a gateway charged once). Coverage is a floor, not a target: a green percentage over untested branches is worse than an honest gap. Where a test selects a thing, bind it to a stable, intention-revealing identifier, not a volatile generated one. |
| **Security & access control** | Validate and enforce trust at the boundary you own; never assume the caller did it. A check the caller can skip or forge (a gate it can bypass, a privilege it asserts about itself) isn't a control; the trusted side re-checks before it acts. In a multi-user system that means server-side authorization; in a library or CLI it means validating inputs and privileges at your entry points rather than trusting what comes in. Route access through the checked path, not an unchecked direct read you can forget to guard, and gate a capability on the trusted side, not a flag the untrusted side can set. |
| **Error handling & logging** | Route errors through the application's error and logging path, not an ad-hoc print left in production. Catch the specific exception, not a blanket catch that hides the cause; a top-level boundary handler that logs and re-raises is the allowed exception. Fail loudly at the boundary, never swallow. |
| **Design & structure** | Does the change remove complexity or add it? Default to removing. Prefer a deep module (a narrow interface over a substantial implementation) to a shallow one, and resist speculative generality (YAGNI). Inject collaborators through a substitutable seam, not a hard-wired static or singleton. Keep logic out of framework entry points and glue code. Prefer polymorphism to a long, growing type switch, though a two-case conditional is usually simpler left alone (YAGNI). |
| **Performance & scale** | Assume inputs can be large: avoid per-element overhead when a batched form exists (a call or query per item, the N+1 trap being the database case), and don't hold an unbounded result in memory, bound it. Stay inside whatever limits the runtime enforces, and where you cache, set sensible lifetimes. |
| **Readability & naming** | Domain-language names, no magic numbers. Watch for identifier shadowing and collisions (a variable named for the type it shadows), and respect the language's naming and scoping rules. |
| **Reuse, dependencies & minimalism** | Run each new thing up the ladder: does it need to exist at all (YAGNI), is it already in the codebase (reuse, don't rewrite), does the standard library or platform do it, can it collapse to one line. Deletion is a valid review outcome (a `net: -N lines` result is a real one), but never cut validation, error handling, security, or the one self-check that proves the logic. DRY the knowledge, not coincidental similarity. Respect dependency direction: references point toward the more stable modules, never into a cycle. A forked or patched dependency is committed as source you can read in review, not applied opaquely by a build step. |
| **Standards & documentation** | Triage static-analysis findings at full severity even when CI only blocks the worst; fix the rest anyway. Run the formatter in a pre-commit hook so style never reaches review. Document the public surface. Committed plan and design docs are a feature; don't nit them for existing, though wrong content in one is a real finding. |

## Size, pace, scope

- **Hold to the minimal ask.** Defect detection falls off past roughly 200 to 400 lines or an hour of review. Split a sprawling change; collapse a stacked-branch diff to its true delta (merge the base in) so the reviewer reads the real change.
- **Match the diff to the stated scope.** Does the change stay within its ticket, or does it bundle unrelated work? Flag bundled-beyond-scope work as a split candidate; it inflates regression risk and the review surface, and it moots any prior approval on the smaller change.

## Guardrails

- **Drafting is not approving.** A request to "write a review" authorises a draft, nothing more. Every posted comment needs the reviewer's per-draft go, and the binding approval is always a human's to cast.
- **The gate is human, not green CI.** A merge clears on the team's approval gate (two humans, for me); a passing pipeline doesn't. This read is one vote into that gate, never a substitute for it.

## End to end

```
branch → worktree → read cold (full context) → walk the checklist
      → per finding: reconcile vs live thread, then size with your co-reviewer or operator (drop/nit/follow-up/hold/fold)
      → assemble survivors into one review in your voice (none survive → say nothing)
      → a human posts, the approval gate clears, merge
```

See also: [`review-voice`](review-voice.md) (the register findings are written in), [`code-writing`](code-writing.md) / [`test-writing`](test-writing.md) (the craft behind the checklist), [`references.md`](references.md).
