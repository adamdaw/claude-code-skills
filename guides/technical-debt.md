# Technical debt: sorting, recording and assessing it

A checklist for what you find in existing code: sort it, weigh it, record it, and put the
decision to its owner. It also covers assessing a codebase, including work you are asked to
accept from someone else. It assumes you already hold the principles; the reasoning is in
*On Technical Debt*. Cite a line as "D-guide §N".

Changing the code, including paying debt down, is in the F-guide. This guide points there
rather than restating it.

## 1. Sort it before you call it debt

Essay: *On Technical Debt* P2, P7; §3.

Find the agreement first: the requirement, the spec (SRS or SDD), the ticket's acceptance
criteria, or the contract and statement of work. Classify against what it says, not against
what you'd have wanted.

| It is | When | Where it goes |
| --- | --- | --- |
| **Defect** | It fails what was agreed. | To whoever owes the fix under that agreement. |
| **Deferred work** | It was agreed and isn't done yet. | The plan, recorded against the agreement if it isn't already. |
| **Debt** | It works, and it costs more to change than it should. | Weigh it (§3), then record it (§4). |
| **Preference** | You'd have done it differently and can't show a cost. | Nowhere (§2). |

- **Missing tests and a missing build pipeline are debt, unless the agreement required
  them.** Then they are defects, owed under that agreement.
- **Don't file a defect as debt.** It makes the fix sound optional and hides who owes it.
- **Something nobody agreed is a new requirement, not a finding against the work.** Route it
  as a change request.
- **Something you couldn't verify either way is an evidence gap.** Log it with its impact.
  Don't classify it until you can.
- **The class doesn't decide who pays.** In a handover, record the classification and a
  proposed responsibility (supplier, you, shared or pending) as separate fields. The contract
  owner decides responsibility; the assessment supplies the evidence.

## 2. A finding needs evidence

Essay: *On Technical Debt* P1, P7.

- **A debt finding names where it is, what it costs and what shows it.** Without the third
  part it isn't a finding yet. Look for the evidence, and keep the finding open while you do.
- **Evidence comes from** the change history, incidents, the code, the agreement, a published
  advisory, or a question about why the code is this way that nobody can answer.
- **Try to recover the reason before you call something debt.** Read the history, the commit
  that introduced it and the ticket it names; ask someone who was there. For the full
  procedure, use F-guide §1 (Explain before you edit).
  - An adequate reason that still holds: write it where the next reader will look, per
    W-guide §8 (Writing it up). It isn't debt.
  - No reason, an unchecked assumption, or a reason that no longer applies: it's debt. Say
    which part of the reason is missing.
- **A preference is a drop.** The rule is R-guide §8 (When you can't follow it) and R-guide
  §10 (Weighing a finding); it holds for an assessment as it does for a code review. A list
  padded with taste buries the debt that matters.
- **Duplication isn't debt by default; a wrong abstraction often is.** The rule is W-guide §4
  (Duplication and speculation).
  - Look-alike code whose copies each changed for their own reasons: not debt.
  - Shared code where changes for one caller keep forcing edits to the shared part, and some
    of them break another caller: a lead, not proof. Read those changes.
  - Shared code that ties together rules that vary independently: a wrong abstraction.
    Coupling alone doesn't make it one.
- **Tool output is evidence, never a finding by itself.** Verify each item from a scanner,
  linter or analyzer, as in R-guide §9 (Triage). Rank by impact, not by warning count.

## 3. Weigh it: debt that matters

Essay: *On Technical Debt* P4.

Debt compounds through change, so where it sits matters as much as what it is. Debt that
matters meets at least one of these weights. This is the bar F-guide §2 (Build, ask, defer,
don't) uses for its Defer row.

| Weight | The question | How to check |
| --- | --- | --- |
| **Change frequency** | How often does this code change? | Hotspots: complexity combined with change frequency, from version history (Tornhill). Count changes over a recent window, and how many were fixes. |
| **Business criticality** | What depends on this working? | Ask the business owner what fails when this fails. |
| **Risk and hard deadlines** | Is something coming for it, whether or not anyone edits it? | Runtime and platform support dates, advisories against pinned dependencies, known security exposures. |

- **Read the history before the style.** A first churn count from git:

  ```sh
  git log --since="12 months ago" --name-only --format= | sort | uniq -c | sort -rn | head -20
  ```

  Set the counts beside a complexity measure your stack provides. The files high on both are
  where to read first.
- **Hotspots direct the investigation; they don't replace it.** A file that changes often is
  a place to look, not a finding.
- **Check risk and deadlines in quiet code too.** A service nobody edits still loses security
  support on the date its runtime reaches end of life.
- **Give each risk its own clock.** A published advisory needs assessing now, even when the
  runtime beside it has a support date months away.
- **A renewal on a known date, such as a certificate or a contract, is usually planned work.**
  If renewing it is hard because of how the code is built, that difficulty might be debt.
- **If the history is missing or unreliable, say so.** Use the best proxy you have, such as a
  deployment log, an audit trail or the ticket history, and lower your confidence in the
  weight.
- **Lead time and incident rate are indicators, not measures of debt.** They show where to
  look and help test an estimate; other causes move them too.
- **Priority follows the weights.** State which weight applies. Debt that meets none of them
  is below the bar.

## 4. Record it: the debt ticket

Essay: *On Technical Debt* P3, P6.

Debt you don't pay now gets a ticket with an owner. Where you found it decides whether it
gets one. Keep the cases apart:

| Where you found it | Debt that matters (§3) | Below the bar |
| --- | --- | --- |
| **In an assessment** (§7, §8) | Ticket with an owner, priority from §3. | Ticket with an owner, at low priority. |
| **Mid-change, in code you only passed** | Defer: a ticket, linked from the PR, per F-guide §2 (Build, ask, defer, don't). | Leave it alone. No ticket. |
| **Mid-change, in code your change edits** | A small improvement that helps this change: F-guide §3 (Tidy only what you touch). Anything larger: F-guide §2. | The same. |

A debt ticket holds:

| Field | What it holds |
| --- | --- |
| **Where** | A file, a module or a boundary. "The export code" isn't a place. |
| **Cost of keeping it** | The extra work each change needs, or the risk or deadline it carries. Name the §3 weight. |
| **Evidence** | What shows it (§2): commits, incidents, the change that took three days, the advisory. Link each one. |
| **Owner** | A named person who will make the §5 decision. |
| **Priority** | From §3; low when the debt is below the bar. |
| **Fix cost** | A low and high estimate, not a single figure. |
| **Deadline** | The date, where a risk or deadline applies. |
| **Found in** | The PR or assessment it came from, linked both ways. |
| **Decision** | Filled in at §5: who decided, what they chose, the reason, and when to revisit it. |

- **The first four are the minimum.** A ticket without them can't be weighed without redoing
  your work.
- **Write it while the evidence is in front of you.** Link it from the PR, per W-guide §8
  (Writing it up).
- **An owner is someone who will decide, not only someone who noticed.** When the debt sits in
  another team's code, route it there with an owner there, as S-guide §13 (The four
  dispositions) does for any finding.
- **A `TODO` with no ticket isn't a record.** A comment explains the debt to the next reader;
  it doesn't queue the work or give it an owner.

## 5. Decide: pay it down or accept it

Essay: *On Technical Debt* P5.

- **Accepting debt can be the right call, if the person who owns the trade-off makes it.**
  Find that person first. It's often not whoever found the debt.
- **Put both costs to the owner:** the fix cost now, and the cost of keeping it (§3). Then let
  them choose: pay it now, schedule it, or accept it.
- **Decide before the shortcut ships.** After that, the choice has been made by default.
- **In code your change edits, an architectural choice is Ask:** F-guide §2 (Build, ask, defer,
  don't).
- **Record the decision on the ticket** (§4): who decided, what they chose, the reason, and a
  review date or the event that reopens it.
- **Accepted debt keeps its ticket and its owner.** The review date is when the choice gets
  made again.
- **The tell:** "we'll clean it up later", said by someone who doesn't own the schedule.

## 6. Pay it down

Essay: *On Technical Debt* P6.

- **Paying down debt is changing existing code.** The F-guide governs it in full.
- **Incremental paydown is the bounded tidy in F-guide §3 (Tidy only what you touch):** small
  improvements in code your change already edits, in a separate commit.
- **Anything larger is sorted with F-guide §2 (Build, ask, defer, don't)**, not folded into
  the change. Debt you only pass is sorted by §4, not fixed.
- **Paying down missing tests:** for untested code, start with F-guide §4 (Capture existing
  behaviour). Which tests to add is in the T-guide.

## 7. Run a debt assessment

Essay: *On Technical Debt* P3, P4, P7; §2.

1. **Frame.** State the scope, the decision the assessment supports, and the standard you judge
   against: the agreement (§1), then the team's own standards. Go deep where the business risk
   is and skim the rest.
2. **Baseline.** Fix the version you assess: a commit, a tag or a snapshot of code and
   configuration. Every finding refers to it. A target that moves while you assess it makes
   every finding disputable.
3. **Gather evidence.**
   - Change history and hotspots (§3).
   - Reading the code, per F-guide §1 (Explain before you edit).
   - Automated scans, as leads (§2).
   - Incident and delivery data.
   - The people who built it, while they can still be asked.
4. **Run practical tests.** Behaviour is stronger evidence than documents.
   - **Rebuild:** build and deploy it from its own instructions in a clean environment. Log
     every manual step.
   - **Change:** make one realistic change end to end. Time it and list every place you had to
     touch.
   - **Correctness:** check the rules that matter most against expected results agreed with
     the business owner.
   - **Volume:** run realistic volumes through it and watch the limits.
   - **Failure:** send bad input and interrupt a job. Check that the failure is visible and
     that recovery works.

   Run them in an isolated environment with synthetic or masked data.
5. **Keep a findings register.** One row per finding: an ID, where, the class (§1), the
   evidence (§2), the weight (§3), the fix cost, the cost of keeping it, any deadline, your
   confidence, and an owner. Include debt below the bar at low priority (§4). Log evidence gaps
   separately, each with its impact.
6. **Check the top findings independently.** A second reviewer checks the evidence for every
   high-priority or blocking finding. Anything used to negotiate must be reproducible by
   someone else.
7. **Report.**
   - A one-page summary: the recommendation, a remediation range for the assessed scope with
     your confidence and exclusions, and the top risks.
   - The findings register.
   - The debt tickets (§4), with the decisions still to make and who makes them (§5).

- **Drop preferences before the report.** They don't appear in it (§2).
- **Where a reader needs scale, two surveys give it, with caveats.** Both are self-reported;
  treat them as directional, not as a benchmark for your system.
  - Stripe and Harris Poll, *The Developer Coefficient* (2018): developers estimate 13.5 hours
    of a 41.1-hour week go on technical debt. Vendor-commissioned.
  - McKinsey Digital, "Tech debt: Reclaiming tech equity" (2020): 50 CIOs estimate tech debt at
    20–40% of the value of their technology estate, before depreciation.

## 8. Accept inherited or third-party work

Essay: *On Technical Debt* P2, P7; §2.

Accepting someone else's work is a debt assessment (§7) with an agreement attached. Run it
before sign-off, while you have leverage and the builders can still answer.

- **Collect the agreement:** the contract, the statement of work, the acceptance criteria,
  change requests and every delivered document.
- **Freeze the delivered state.** Ask in writing, with a named owner, that the delivered
  environment isn't changed during the assessment. On day one, snapshot the delivered code and
  configuration into a repository you control.
  - Record what identifies the snapshot: source, version, timestamps, item counts and anything
    you couldn't retrieve. A checksum proves integrity, not completeness.
  - Keep personal and sensitive data out of the repository.
- **Treat their documents as claims to verify.** Where a document and the delivered system
  disagree, the gap is a finding.
- **Rebuild from their documents only**, in an environment you control. Log every manual step.
  - "Environment unavailable" is a different result from "can't be reproduced".
  - Many manual steps don't prove it can't be reproduced; the documented procedure failing
    does.
- **Check conformance.** Walk every acceptance criterion against the running system: met,
  partly met, not met or not assessed, with evidence and confidence.
- **Classify against the agreement** (§1). A defect goes back against the handover, not into
  your backlog.
- **When you can reach the builders, ask the why questions now** (§2), and record each answer
  beside the code it explains.
- **When you can't reach them, ask in writing** through the contract owner, so there's a
  record.
  - Make each question specific and answerable, and ask for a deliverable: "Provide the
    deployment procedure, including manual steps."
  - Build the questions from gaps the assessment finds, and send them in batches.
  - Always ask for the known shortcuts, workarounds and deferred work, and for the test plan
    and results against the acceptance criteria.
  - Log an unanswered or vague reply as an evidence gap and assess its impact. Don't make the
    assessment wait on replies.
- **Recommend one of three outcomes:**

  | Outcome | When |
  | --- | --- |
  | **Accept** | The issues are modest and understood. Budget for them. |
  | **Accept with conditions** | Named issues are fixed before sign-off or under whatever warranty the contract provides. The rest is accepted knowingly. |
  | **Reject or withhold** | Blocking issues: it can't be rebuilt, it isn't secure, or core requirements aren't met. |

- **Each condition names** the acceptance criterion, the owner, the deadline, the retest and the
  evidence that closes it.
- **Make acceptance conditional on production matching the assessed baseline**, with any
  approved differences listed.
- **The business and contract owners decide acceptance** (§5). The assessment recommends.
- **Debt you accept with the work gets tickets with owners** (§4), including debt below the bar.

---

Hotspots come from Adam Tornhill, *Your Code as a Crime Scene* (Pragmatic Bookshelf, 2015;
2nd edition 2024). For other sources, see [References](references.md).
