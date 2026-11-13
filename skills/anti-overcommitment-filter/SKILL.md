---
name: anti-overcommitment-filter
description: Use when refining a business request, a bug report, or derived work into an actionable ticket, before the ticket is approved (triggers "anti-overcommitment filter", "overcommitment filter", "are we promising too much", "scope check", "gold-plating"). Checks that each commitment in the draft is needed, knowable now, bounded, and within the owner's control, and proposes cutting, narrowing, spiking or parking the rest. Reports; never edits the tracker.
license: MIT
---

# Anti-overcommitment filter

Every line in a ticket is a promise somebody will be held to. This filter reads a draft and
asks of each commitment: is it needed, is it knowable now, is it bounded, and is it ours to
deliver? A commitment that fails any of these gets cut, narrowed, split into discovery work
or parked.

The default is to commit to less. A ticket that promises the smallest thing that meets the
need can be delivered, checked and closed. A ticket that promises more turns into a negotiation
at acceptance time. ([S-guide §4](../../guides/specifying.md#4-the-sdd-is-the-smallest-contract-that-makes-the-srs-checkable) applies the same idea to the SDD: every line is attack
surface.)

## Where it sits

It's the third of three refinement filters, run on each piece after the
[single responsibility](../single-responsibility-filter/SKILL.md) and
[separation of concerns](../separation-of-concerns-filter/SKILL.md) filters, before the ticket is approved and before [`spec-review`](../spec-review/SKILL.md).

## Input

- The draft work item, already split and separated.
- Its source: the original ask, bug report or parent ticket. This filter depends on the
  source, because "needed" means "traceable to what was asked".

## The tests

Apply them to every commitment in the draft (acceptance criteria, scope statements and the
implicit commitments described below), in this order:
Needed, Ours, Knowable, Bounded. Report a line under the first test it fails, and give the
outcome that test leads to. A line that isn't needed doesn't need bounding. If it fails a
later test too, name that test in the finding's observation.

Some content belongs to another filter. An open question written as a criterion is a
separation of concerns finding, not a Knowable one. See *Which filter owns what* in the
[single responsibility filter](../single-responsibility-filter/SKILL.md).

1. **Needed.** Does it trace to something the source asked for? Extra polish, extra options,
   configurability "for later", future-proofing and "while we're at it" fail this test.
   Trace each criterion, not just its topic. A criterion that serves a traced need but adds a
   capability the source didn't ask for (a new format, a new access path, a new audience) is
   untraced for that addition.
   A bug ticket commits to fixing the observed defect. A wider rewrite is a separate request
   that somebody has to make.
2. **Ours.** Can the team that owns this ticket deliver it alone? A criterion that's met only
   if another team ships, a vendor responds or a stakeholder approves is a dependency, not a
   commitment. Name it as one.
3. **Knowable.** Could someone tell today whether it's achievable, and roughly what it costs?
   If the answer depends on an investigation nobody has done (an unknown root cause, an
   untested integration, an unmeasured baseline), the investigation is the work. Commit to
   that, not to its result.
4. **Bounded.** Is there a stated edge? Look for unbounded words: *all*, *any*, *every*,
   *always*, *never*, *fully*, *seamless*, *real-time*, *robust*, *support*, *handle*,
   *integrate with*, *improve*. Each needs a named set, a number or an observable outcome.
   "Support all browsers" commits to nothing checkable. "Works in the browsers on the
   supported-browsers list" can be checked.

Also check what the draft commits to *implicitly*. A date, an estimate, a performance number
or a compatibility promise in the title or description binds just as much as one in the
criteria, and often nobody has agreed to it. Test it like any other commitment: it's a finding
with an outcome, and it counts toward the verdict.

## Outcomes

Give each finding exactly one outcome:

- **Cut** (from Needed): not needed, and nothing in it is worth keeping. Remove it.
- **Narrow** (from Bounded): needed but unbounded. Propose the bound, phrased as a question to the owner
  if the bound is a business decision.
- **Spike** (from Knowable): not knowable yet. Propose a separate, time-boxed discovery ticket that answers a
  named question. This ticket waits on the answer or commits only to what doesn't depend on it.
- **Depend** (from Ours): not ours. Restate it as a named dependency with an owner.
- **Park** (from Needed): not needed for this ask, but a real idea someone may want. Use
  *Park*, not *Cut*, whenever the line describes something a user or owner could plausibly ask
  for on its own. Propose a follow-up ticket, unfiled,
  for the owner to decide on.

## Output

1. **Verdict**: *committable* or *findings*.
2. **Findings**: for each, quote the sentence or criterion verbatim, name the test it fails,
   give the outcome and the proposed replacement wording if there is one, and write the
   finding: an observation and a question. Name any later test it also fails in the
   observation.
3. **Implicit commitments**: the findings above that sit outside the criteria, listed again
   with who appears to have made each one.
4. **Proposed spikes and parked items**: one line each, unfiled.
5. **Questions for the owner**: every bound or cut that is a business decision.

The labelled fields above (the quote, the test or pair, the outcome, the proposals) are this
filter's report structure. The finding itself is written the way [R-guide §11 (Writing a finding)](../../guides/running-a-review.md#11-writing-a-finding)
shapes one: an observation and a question, with the quote as the pointer. It doesn't explain
or argue. §11's rules govern that text, not the headings or the proposals.

On a clean draft, give the verdict and write "None." under every other heading, so a
reader can tell each section was checked rather than skipped.

## Rules

- Report; don't act. Never edit or approve a ticket in the tracker, or commit to a date on anyone's behalf.
- Cutting scope is a proposal, not a decision. The owner decides what's needed; the filter
  shows them what each line costs in commitment.
- Don't invent work. Replacement wording, spikes and parked items may only use what the draft
  and its source contain. A new idea goes under questions.
- Don't replace an overcommitment with a different one. A narrowed criterion must still be
  something the team can check and deliver.
- Doing less is a legitimate result. A draft that comes out of this filter as a smaller ticket
  plus a spike, or as "not yet", has been refined, not failed.
