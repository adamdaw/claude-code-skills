# Specifying: writing and reviewing SRS, SDD and tickets

A checklist for writing a spec and for reviewing one. It assumes you already hold the principles; the reasoning is in *On Specifying Software*. Cite a line as "S-guide §N".

Vocabulary used throughout:

- **Requirement**: one thing the system must do, stated so it can be checked.
- **SRS** (software requirements specification): the requirements for one piece of work, and what the person who asked agreed to.
- **SDD** (software design description): the contract a build is checked against.
- **Spec**: either of these, or a ticket that plays either role.
- **Spec review**: judges whether a spec is fit to build from. **Fidelity review**: checks one layer against the one before it (SRS→SDD, SDD→code).

## 1. Write requirements with SHALL, stated positively

- Use SHALL only in requirements and SDD contract lines. SHALL binds; *should*, *will* and *may* bind nothing, so keep them out of anything normative.
- State each requirement positively. Turn a prohibition into an allowlist: "The system shall log only the request ID and status", not "shall not log personal data".
- Use "shall not" only when no positive form exists.
- One requirement per sentence, one reading per requirement.
- State the need, not the design. How it is built belongs in the code; the SDD holds only traced, checkable commitments (§4).
- Write acceptance criteria as observed outcomes in the plain present tense: "The export contains one row per active account."
- Two requirements that contradict each other are a finding, however far apart they sit.

## 2. Use canonical EARS

- Write every requirement in one of the six EARS forms. Source: Alistair Mavin, Philip Wilkinson, Adrian Harwood and Mark Novak, "Easy Approach to Requirements Syntax (EARS)", IEEE International Requirements Engineering Conference, 2009.
  - **Ubiquitous**: The \<system\> shall \<response\>.
  - **Event-driven**: When \<trigger\>, the \<system\> shall \<response\>.
  - **State-driven**: While \<state\>, the \<system\> shall \<response\>.
  - **Unwanted behaviour**: If \<condition\>, then the \<system\> shall \<response\>.
  - **Optional feature**: Where \<feature is included\>, the \<system\> shall \<response\>.
  - **Complex**: a combination of the preceding keywords, such as "While \<state\>, when \<trigger\>, the \<system\> shall \<response\>."
- Write each refusal in the unwanted-behaviour form: the condition the system refuses, and what it does instead.
- A local variant of EARS folds into the canonical forms. If a variant seems to express something the six forms can't, raise it as a question; don't keep the variant.

## 3. Say what a missing value means

- For every value that can be missing, the spec states what missing means. A spec that doesn't is a spec-review finding.
- Keep absent, empty and zero apart. They are three states, and each needs its own stated meaning.
- If you don't know what a missing value is supposed to mean, ask. It's a decision nobody made yet, and it isn't yours to make.
- Ask the other questions the requirement doesn't answer: what it refuses, how many it handles realistically, and what happens when it fails. (*On Writing Code* has the reasoning.)

## 4. The SDD is the smallest contract that makes the SRS checkable

- Every SDD line is attack surface. Write only what a fidelity review or a test will hold the code to.
- Each line must be **traced**: it serves a named SRS requirement.
- Each line must be **checkable**: an interface, a precondition or postcondition, an invariant, a boundary behaviour, or an error the caller can see.
- A line that fails either test is a finding. A checkable line with no trace is still inflation; a traced line that can't be checked is still exposition or design:
  - **Inflation** (untraced: a new commitment the SRS doesn't make): cut it, or take it back to the SRS through its owner and SRS review. Never keep it in place.
  - **Derivation, justification or exposition**: cut it. The reason goes in the decision register (§6).
  - **Design or implementation** (the how): cut it. It belongs in the code.
- Don't restate the SRS in the SDD. Trace to it by ID.

## 5. Normative and non-normative documents

Normative documents are what reviewers see and what gets built. Non-normative documents are used only at reconciliation (§12).

| Normative (reviewed, built from) | Non-normative (reconciliation only) |
| --- | --- |
| Constitution: repo-wide rules | ADRs: the why behind a constraint |
| Constraints register: C-n entries | Elicitation record: F-n entries |
| SRS | Decision register: D-n entries |
| SDD | |

- A cold spec review or fidelity review gets the normative column only. Filter the constraints register by scope; that is a lookup, not a judgement.
- Nobody reviews a non-normative document as contract, and nobody builds from one.
- Keep ADRs for cross-cutting, long-lived decisions. Other rationale goes in the decision register, in a commit body (a rejected alternative only when it prevents someone undoing the change), or nowhere.

## 6. The elicitation record and the decision register

- **Elicitation record** (sits beside the SRS): facts. Each F-entry has an ID, the fact, its source and a date. A stakeholder's decision is recorded as a fact: who decided what, and when.
- **Decision register** (sits beside the SDD): choices. Each D-entry has an ID, the choice, an owner and a one-line reason.
- Link the specs to the registers by ID (F-n, D-n). A stale fact flags every line that cites it.
- Record a term change as a D-entry.
- Elicit live one question at a time. Asynchronously, ask all the questions at once, in writing, where the answers stay.
- Every answer becomes an F-entry.

## 7. The constraints register

- Each C-entry has an ID, a scope, one positive SHALL line, and a link to the ADR that holds its reason.
- A constraint binds every spec in its scope. Reviewers receive the entries whose scope covers the spec.
- Change a constraint through an ADR decision, never through a workaround in the SDD.

## 8. A spec never contains a deviation

- If a spec conflicts with the constitution or a constraint, don't write the deviation into the spec.
- Resolve it one of two ways: amend the constitution, or add a scoped exception to the constraints register with its ADR.
- Until one of those happens, the conflict is an open finding.
- If the rule belongs to someone else (a team's constitution, say), the conflict is a question to them, with a D-entry while it stays open.

## 9. A new edge case found while writing the SDD

- Record it as a D-entry, and send a question to the person who asked. Batch it with the others, in writing.
- Record their answer as an F-entry.
- Then either amend the SRS through SRS review, or defer the case by their decision.
- Don't add the case to the SDD without the requester's decision, and don't hold the SDD indefinitely waiting for it.
- Going back to SRS review is costly. Do it anyway, and count it.

## 10. Spec review

- A spec review is cold: the reviewer is not the author and has not seen the author's reasoning.
- Hand the reviewer its inputs: the spec under review, the spec it must encode (the SRS, for an SDD), the constitution, and the constraints in scope. The reviewer fetches nothing and has no tracker or repository-hosting access.
- Never hand in the non-normative documents, earlier findings or your own opinion of the spec.
- The reviewer returns findings and writes no files. Recording happens at reconciliation (§12).
- It checks:
  - Each requirement against §1–§3: SHALL, positive, one reading, EARS, missing values stated.
  - The SDD against §4: every line traced and checkable.
  - No deviation from the constitution or a constraint in scope (§8).
  - Each acceptance criterion observable without reading the code.
  - Reliance on outside behaviour (a vendor API, a platform quirk) marked as a reliance to verify, not stated as settled.
- It judges whether the spec is fit to build from. It doesn't propose a design.
- Spec review is judgement work. Give it a strong model or an experienced reader.

## 11. Fidelity review

- Fidelity = **coverage** (nothing dropped) + **containment** (nothing added).
- Run it at each handoff: SRS→SDD, then SDD→code.
- Same inputs rule as §10: handed in, normative only, findings returned, no files written.
- Start with ID matching, which is cheap and mechanical:
  - Every requirement ID in the upstream layer has at least one downstream line that traces to it. A requirement with no trace is a coverage finding.
  - Every downstream line traces to an upstream ID. A line with no trace is a containment finding (inflation, §4).
- Hand only what the matching can't settle to a strong model or a person: a line that traces but doesn't say what the requirement says, or code that doesn't do what the line says.
- A script or a cheap model does the matching; save judgement for the non-matches.

## 12. Reconciliation

- Reconcile the candidate findings from a cold pass against the decision register and the glossary before anyone acts on them.
- Drop re-raises of settled decisions and reversions of settled choices. Log each drop against its D-entry: "re-raised ×12; stands".
- A candidate that keeps coming back gets one look. Either the decision stands, or you fix it by editing or removing a line. Never fix it by adding spec text.
- Reconciliation is mostly matching, so a script or a cheap model can do most of it.
- **Done** = a cold pass whose candidates, after reconciliation, leave no new finding, on a spec body unchanged since that pass.
- If passes stop converging on genuinely new findings, escalate to the person who asked.

## 13. The four dispositions

Every finding that survives reconciliation gets exactly one disposition.

- **Fix**: change or remove a line. A cut idea can be parked as a follow-up.
- **Reject**: not a real finding. Record a D-entry; reconciliation drops it from then on.
- **Escalate**: real, and this spec's problem, but the decision belongs to someone else. Their answer becomes an F-entry.
- **Route**: real, but not this spec's responsibility. Send it where it belongs, with an owner there. If this spec depends on it, escalate instead.
- No waivers. A finding nobody fixes is rejected with a reason, escalated or routed.

## 14. Names, not numbers

- Name each review in prose and in stored state: SRS review, SDD review, fidelity review SRS→SDD, fidelity review SDD→code. Never "Gate 1" or "Gate 3".
- Where a tool needs the order, derive an index from one ordered list of names and use it only for comparisons. Store names; show people names.

## 15. Formats apply forward

- These formats apply to specs written or substantively revised after you adopt them.
- An older spec isn't a finding for its format alone. Review it for content.
- When a format is your own practice and not the team's, review other people's tickets for content, never for format.
