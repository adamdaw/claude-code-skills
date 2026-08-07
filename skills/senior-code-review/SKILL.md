---
name: senior-code-review
description: Use when reviewing a pull request, a diff, or a code change (triggers "review this PR", "code review", "senior review", "review the change"). Runs four complementary passes over the change (correctness, structural craft, minimalism, house standards), reads the actual checked-out code rather than just the diff, reconciles with the live PR thread, and works findings one at a time toward a hold-or-approve recommendation. It drafts and recommends; it never posts a binding approval.
license: MIT
---

# Senior code review

One review that runs several complementary passes over a change, then applies judgement and stops at the human gate. The point is an independent read, as honest as you can make it, that informs the human's call without ever substituting for it. This is the operational companion to [`running-a-review`](../../guides/running-a-review.md) and [`review-voice`](../../guides/review-voice.md); the never-approve rule and the human gate are the whole point, not a nicety.

**The one idea to start with:** the reviewer reads cold and reports. It doesn't approve. A human posts, and the team's approval gate clears a merge.

## Run it in this order

1. **Read cold.** Form the read with nobody's findings in front of you and no conclusion pre-loaded, no statement of what you're supposed to confirm. The change's own description and ticket are fair to read, since they're claims to verify; what you refuse is a briefing that tells you the verdict to reach. Brief a reviewer with a conclusion and all you get back is that conclusion.
2. **Read the checked-out code, not just the diff.** First confirm what actually changed against the base (the live diff), so you aren't reviewing already-merged or phantom content (a rebased-empty branch reads as real files but is a no-op diff). Then check the branch out into a throwaway worktree and read the real files for context. The load-bearing facts are usually invisible in the patch: a default that silently coerces a missing value to zero, an access grant the change leans on, a dependency version that shifted under it. The main clone is a read-only reference; never mutate it.
3. **Walk the four passes below** to gather candidate findings.
4. **Reconcile against the live thread.** Re-fetch the head (the author may have pushed, even fixed the thing) and read the existing comments. Check the commit each approval and each automated finding was made against: an approval that predates the current head is stale, so flag it; a bot finding computed on an older commit may be moot, so verify it against the live diff before repeating it. Already raised and open? Add weight only if you have something new. Already fixed on a newer commit? Drop it. Already dispositioned as by-design? Engage the reasoning or accept it. "Do nothing" is a valid outcome.
5. **Work it finding by finding, with the human running the review.** Surface each finding as it clears: what it is, the evidence, whether it blocks. Size it and decide together (drop / nit / follow-up ticket / hold / fold in), then the next. The agent proposes and the operator disposes; any back-and-forth with the author is the human's, downstream of this.
6. **Assemble the survivors** into one review, then re-voice it into the posting reviewer's register before it goes out (see [`review-voice`](../../guides/review-voice.md)); the raw findings as gathered aren't postable as-is. If nothing survives, add nothing, just recommend approval.
7. **Stop at the gate.** Recommend hold or approve; the human posts and holds the binding approval.

## The four passes

Run all four. Passes 1 to 3 apply craft principles as review lenses; pass 4 applies your house standards. Each pass names what it looks for and points to the guide that holds the detail; hold a change to both the craft and the house rule. This skill is the procedure, not the rulebook.

### 1. Correctness & tests
Does the change prove its own behaviour, the negative and gate branches included, against the real shape rather than a mock that only returns what you fed it? The test-craft to hold it to, from what to assert through to the one case where asserting a call is right, lives in [`test-writing`](../../guides/test-writing.md).

### 2. Structural craft
Is the change simple to change safely, or does it add coupling, duplication, unclear names, or over-wide interfaces? Walk the smell catalogue: feature envy, transitive navigation (`a.getB().getC()`), tell-don't-ask, hidden temporal coupling, data clumps, magic numbers, a function doing more than one job, more than three arguments (reach for a parameter object), flag arguments, output arguments, dead code. Name the specific refactoring when one applies (Extract Method, Introduce Parameter Object, Move Method) so the author has shared vocabulary; hard to construct for a test is a design signal, not a test problem. The principles behind the smells are in [`code-writing`](../../guides/code-writing.md).

### 3. Minimalism (the ladder)
Once you understand the change, run each new thing up the ladder and flag what doesn't need to be there. Tags: `delete` (dead code, speculative feature; replaces with nothing), `stdlib` (a hand-rolled thing the platform ships; name it), `native` (a dependency or code the platform already covers), `yagni` (an abstraction with one implementation, config nobody sets, a layer with one caller), `shrink` (same logic, fewer lines; show the shorter form). One line per finding: location, what to cut, what replaces it. `net: -N lines` is a real, valuable result.
- **Boundary:** minimalism is over-engineering only. It never flags correctness, security, or performance for deletion, and never the one smoke test or self-check that proves the logic. Those belong to the other passes.
- **Scope check:** does the diff match the change's stated scope, or bundle unrelated work? Bundled-beyond-scope work is a split candidate (the Size, pace, scope section in [`running-a-review`](../../guides/running-a-review.md) has the full rationale); it also moots any prior approval on the smaller change.

### 4. House standards
Apply the full dimension checklist in [`running-a-review`](../../guides/running-a-review.md); it is the single source for the house standards. The four passes here and the checklist's dimensions are two cuts of the same review, not a one-to-one map: passes 1 to 3 are the craft lenses, and this pass runs the checklist in full so the stack-specific dimensions (security, error handling, performance, dependencies, standards and docs) and anything the lenses did not already cover all get their pass. Apply its rows, don't restate them, and fill in your own codebase's concrete APIs and conventions there.

## Verdict

Decide approve-versus-hold *from* the finding, not before it. Default to a **hold** on an unaddressed gap; a clean change with only nits ships with those nits noted. The full verdict rule (why green CI and prior approvals don't clear a real gap, and why the bar is a healthier system rather than a flawless one) lives in [`running-a-review`](../../guides/running-a-review.md).

## Register

Findings go out as questions and suggestions, not imperatives: state your reading, invite a correction, offer the fix conditioned on the answer, and vary the phrasing so it doesn't read like a bot. Lead with the substance, never the verdict word; end on the question; a clean approve gets no comment at all. The full register, how a finding is shaped and why the stance is worth the effort, lives in [`review-voice`](../../guides/review-voice.md). Apply it when re-voicing at step 6 rather than restating it here.

## Guardrails

- **Never post a binding approval.** "Write a code review" isn't authority to approve. Posting even a comment needs the reviewer's explicit per-draft go; the binding approval is a human's.
- **Count approvals, not green CI.** The team's approval gate clears a merge. This read is one vote informing that decision; it never satisfies it.
- **An independent read is one perspective.** It'll sometimes miss what a human or another tool catches, and sometimes re-derive what the thread already settled. The reconcile step is what turns it into a contribution rather than a repeat.
