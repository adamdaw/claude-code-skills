---
name: single-responsibility-filter
description: Use when refining a business request, a bug report, or derived work into an actionable ticket, before the ticket is approved, and the draft may be carrying more than one piece of work (triggers "single responsibility filter", "is this one ticket", "should this be split", "SRP filter"). Checks that the draft has one outcome, accepted by one owner, and proposes splits where it doesn't. Reports; never edits the tracker.
license: MIT
---

# Single responsibility filter

A ticket should have one reason to exist: one outcome that one owner accepts as done. This
filter reads a draft work item and reports where it carries more than one, then proposes a
split that leaves each piece independently deliverable.

The idea is adapted from the single responsibility principle for code. A module should have
one reason to change. A ticket should have one reason to be done.

## Where it sits

Run it while a request is being refined, before the ticket is approved. The draft may be text
that hasn't been filed yet or a ticket already in the tracker in a pre-approval state; either
way, approval is the gate these filters feed. It is the first of three filters:

1. **Single responsibility** (this one): how many pieces of work are here?
2. [**Separation of concerns**](../separation-of-concerns-filter/SKILL.md): within each piece,
   are different kinds of thing kept apart?
3. [**Anti-overcommitment**](../anti-overcommitment-filter/SKILL.md): does each piece promise
   only what is known, needed and deliverable?

Run them in that order. Splitting first means the later filters judge each piece on its own.

### Which filter owns what

Some content could be caught by more than one filter. Report it under the one that owns it:

- **Another internal owner's work that delivers value on its own** (a report another team
  accepts) is a split here.
- **Another owner's work this outcome needs** (a production rollout, a vendor action, a
  stakeholder's decision) isn't a split, because it fails the over-split check below. Nor is work an outside vendor
  or customer must do, even when it has its own timing: nobody outside can accept a ticket. The
  separation of concerns filter routes it. If the draft states it as a commitment, the
  anti-overcommitment filter also marks it as a dependency.
- **An open question written as a criterion** belongs to the separation of concerns filter,
  not to anti-overcommitment's Knowable test.
- **A draft that replaces the ask instead of adding to it** passes this filter, because it
  is still one outcome. The anti-overcommitment filter's Needed test catches it.
- **A second outcome added to the ask** is a split here. If the anti-overcommitment filter
  runs on the unsplit draft, its Needed test will also flag the added part. That overlap is
  expected; in the normal order the split has already happened.

None of them replaces [`spec-review`](../spec-review/SKILL.md), which comes later and judges
whether a finished spec is fit to build from.

## Input

- The draft: a business request, a bug report, or a derived work item (follow-up, debt,
  something a review or incident turned up).
- Its source, if there is one: the original ask, the incident, the parent ticket.

Read the source as well as the draft. A draft that has drifted from its source can look
coherent on its own.

## The tests

Apply each test to the draft. Any one that fails is a finding.

1. **One sentence.** Can "done" be stated in one sentence without *and*, *also* or *plus*? If
   the only honest statement needs a conjunction, there is probably more than one outcome.
2. **Independent value.** If one part were dropped or delayed, would the rest still deliver
   something the owner wants? If yes, the parts are separate tickets.
3. **One acceptor.** Who says it's done? Two different people, teams or roles accepting
   different parts means two tickets. *Different parts* means outcomes that could each be
   delivered alone. Several people signing off on aspects of one outcome (Design accepts the
   look, the product owner accepts the whole) is one outcome with a sign-off list, not a split.
4. **One work type.** A defect fix and a new capability are different work, judged
   differently. A bug ticket fixes the observed defect. A second defect it reveals, or the
   feature it suggests, is its own ticket.
5. **Acceptance criteria cluster.** Group the criteria by the outcome each one checks. More
   than one group is more than one ticket.

## Signals worth a closer look

These don't fail the filter by themselves, but they usually point at a test that does:

- "While we're in there…", "and also…", "as part of this…"
- A title that names two things.
- A derived refactor, migration or cleanup riding along with a request.
- A bug report whose steps to reproduce describe two different failures.
- Acceptance criteria that could be checked in any order by different people.

## Don't over-split

A split is only right if each piece passes on its own:

- Each piece is deliverable and verifiable by itself. A piece whose only test is "the other
  ticket works" isn't a ticket. It's a task inside one.
- Prefer slicing by outcome (a thin piece that works end to end) to slicing by layer
  (front end, back end, database). Layer slicing produces tickets nobody can accept alone.
- Necessary steps toward a single outcome stay together, however many there are.

If a draft fails test 1 but every candidate split fails these checks, it's one ticket with a
badly worded outcome. Report a rewording, not a split.

## Output

Report, in this order:

1. **Verdict**: *one ticket* or *split proposed*.
2. **Findings**: for each one, quote the sentence or criterion verbatim, name the test it fails, and say why in a
   sentence.
3. **Proposed shape**: one line per resulting ticket, giving its one-sentence outcome, its
   acceptor and its work type. Mark which piece is the original ask, and say what each other
   piece needs before it is worth filing.
4. **Questions for the owner**: anything the filter couldn't decide, such as who accepts a
   part or whether a part is wanted at all.

The output headings above are the report's structure, and the proposals they ask for are
this filter's job. The register of [R-guide §11 (Writing a finding)](../../guides/running-a-review.md#11-writing-a-finding) governs only how each finding's
"why" is worded: an observation and a question, collaborative and terse. It doesn't
remove the headings or the proposals.

On a clean draft, give the verdict and write "None." under every other heading, so a
reader can tell each section was checked rather than skipped.

## Rules

- Report; don't act. Never create, edit, close or approve a ticket in the tracker. The human
  does that.
- Don't invent work. A split may only redistribute what the draft and its source already
  contain. A new idea goes under questions, not into a proposed ticket.
- Whether a split piece is wanted at all is the owner's call. Ask; don't decide.
