---
name: separation-of-concerns-filter
description: Use when refining a business request, a bug report, or derived work into an actionable ticket, before the ticket is approved, and the draft mixes kinds of content (triggers "separation of concerns filter", "SoC filter", "this ticket is tangled", "need vs design"). Checks that need is kept apart from design, requirement from rationale, commitment from open question, and one owner's work from another's. Proposes where each misplaced piece belongs. Reports; never edits the tracker.
license: MIT
---

# Separation of concerns filter

The [single responsibility filter](../single-responsibility-filter/SKILL.md) asks how many
pieces of work a draft holds. This filter asks a different question: within one piece, are
different kinds of thing kept apart? A ticket can have exactly one outcome and still be
tangled. It might mix the need with a guessed design, bury an open question inside an
acceptance criterion, or carry another team's work as if it were its own.

Tangling matters because each kind of content is judged by different people at different
times. If they're mixed, a reviewer can't tell which lines are binding.

## Where it sits

It's the second of three refinement filters. Run it after the single responsibility filter,
on each piece separately, and before the
[anti-overcommitment filter](../anti-overcommitment-filter/SKILL.md). All three run before the ticket is
approved, and before [`spec-review`](../spec-review/SKILL.md).

When content could belong to more than one filter, see *Which filter owns what* in the
[single responsibility filter](../single-responsibility-filter/SKILL.md).

## Input

- The draft work item, already through the single responsibility filter.
- Its source: the original ask, bug report or parent ticket.

## The concerns to keep apart

Check each pair. Content on the wrong side of a pair is a finding.

1. **Need vs design.** The ticket states what must be true, not how to build it. "Users can
   export their invoices" is a need. "Add a CSV button that calls the reports API" is a design.
   A design detail is fine if it's a real constraint the owner imposed. A constraint that
   already names who imposed it is not a finding. One that doesn't is a finding with the
   outcome *Ask*. Otherwise it goes to design. ([S-guide §1](../../guides/specifying.md#1-write-requirements-with-shall-stated-positively):
   state the need, not the design.)
2. **Requirement vs rationale.** Why the work matters, how the problem was found and what was
   tried before are useful, but they don't bind anything. Keep them in a clearly non-binding
   section or in the elicitation record and decision register
   ([S-guide §6](../../guides/specifying.md#6-the-elicitation-record-and-the-decision-register)), not inside the
   requirements or acceptance criteria.
3. **Commitment vs open question.** An acceptance criterion states an observed outcome. "TBD",
   "probably", "ideally" and "to be confirmed with X" mark a question, and a question can't be
   accepted. Move it to an open-questions list with someone named to answer it.
4. **This owner vs another.** Work that another team, system or vendor must do isn't this
   ticket's to commit. Name it as a dependency with its owner, or route it as its own ticket.
5. **Behaviour vs operations.** Data backfills, migrations, configuration changes, feature
   flags, rollout, monitoring and user communication are often real work that someone has to
   do. Each one is either explicitly in scope with its own criterion or explicitly elsewhere.
   Don't leave it implied.
6. **Policy vs mechanism.** A business rule (who qualifies, what the limit is) belongs to the
   business owner. The mechanism that enforces it belongs to the builders. When a draft
   states a rule only through its mechanism, the rule can't be reviewed by the person who
   owns it.

For a bug, add one more: **symptom vs diagnosis.** The report states what was observed, where
and how to reproduce it. A suspected cause is a hypothesis; label it as one, and keep it out
of the acceptance criteria. The criterion is that the symptom no longer occurs.

## Outcomes

Give each finding exactly one outcome:

- **Move**: the content belongs in this ticket but in a different section (rationale,
  open questions, dependencies, constraints).
- **Route**: the content is another owner's work. Name the owner and say whether this ticket
  depends on it.
- **Defer to design**: the content is a how, and it belongs in the SDD or the code, not the
  ticket.
- **Ask**: you can't tell which side of the pair the content is on, usually a design detail
  that might be an owner's constraint. Put the question to the owner under *Questions for the
  owner*. Don't defer it or keep it until they answer.

## Output

1. **Verdict**: *separated* or *findings*.
2. **Findings**: for each, quote the line, name the pair it crosses, give the outcome, and say
   where the content goes.
3. **Dependencies**: every piece of another owner's work the ticket relies on, with that
   owner named.
4. **Questions for the owner**: open questions pulled out of the criteria, each with who
   should answer it.

The output headings above are the report's structure, and the proposals they ask for are
this filter's job. The register of [R-guide §11 (Writing a finding)](../../guides/running-a-review.md#11-writing-a-finding) governs only how each finding's
"why" is worded: an observation and a question, collaborative and terse. It doesn't
remove the headings or the proposals.

On a clean draft, give the verdict and write "None." under every other heading, so a
reader can tell each section was checked rather than skipped.

## Rules

- Report; don't act. Never edit or approve a ticket in the tracker.
- Moving content must not change its meaning. If separating a line would change what it
  commits to, ask the owner rather than rewording it.
- A design choice the owner made deliberately isn't a finding just because it's a how. If
  the draft doesn't say whether it's a constraint, the outcome is *Ask*, not *Defer to design*.
