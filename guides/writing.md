# Writing: professional, technical and personal

P-guide. A checklist for drafting and editing; choose the register before writing.
Clarity outranks brevity. For the reasoning, see [How I Use AI](https://adamdaw.com/ai/)
and the future essay *On Writing*.

## 1. Writing under Adam's name

- Follow the standard in [How I Use AI](https://adamdaw.com/ai/): help Adam reason;
  don't reason for him. Express ideas he understands and positions he has formed.
- Everything that goes out under Adam's name must be something he can explain and defend
  without AI assistance.
  Surface missing reasoning as a question; don't supply an argument in his voice.
- Use primary sources only for factual claims. Locate the source, check the claim
  against it, and give Adam the source to read before publication.
- Flag unsourced claims explicitly. Keep observations, inferences and unknowns distinct.
- Fluency is not authority. A polished sentence and a model's agreement are not evidence.
  Use an independent claims audit when checking claims; author judgement remains necessary.

## 2. Edit in order: content → comprehension → voice

1. **Content:** establish the point, evidence, scope and intended action. Flag gaps.
2. **Comprehension:** order the explanation, define needed terms and make each inference
   follow from what the reader has already been told.
3. **Voice:** apply the chosen register without changing substance or severity.

- Voice never overrides comprehension. An edit must preserve the claim, its limits,
  the decision, the obligation and the weight of a finding.
- Choose the shape before drafting. Fit the material to the reader's task; a word-count
  target cannot decide which facts matter.
- `public-writing` applies these rules to colleague-facing text.

## 3. Keep the lexicon; explain it

- Keep official field terms and exact identifiers. Cut insider shorthand and unnecessary
  jargon. Don't remove a needed term to avoid defining it.
- Ask: would this reader have to look the term up to act? If so, gloss it once on first
  use, in a short clause: “idempotent, meaning that repeating the request has no extra effect”.
- Skip the gloss when the audience already knows the term, the text has already defined
  it, or its meaning is clear enough here for the reader to act. Reintroduce it in a
  section that readers use independently.
- Use one term per thing and one meaning per word. Repeat the term instead of changing
  synonyms for variety. Preserve search terms in durable writing.
- Keep requirement, spec, SRS (software requirements specification) and SDD (software
  design description) distinct. Don't turn descriptive prose into a requirement by editing.
- Name the review type: self-review, code review, bot review, spec review, fidelity review
  or claims audit. Use names, not gate numbers; “cold” describes an independent read
  without supplied findings or a preloaded conclusion.

## 4. Choose the register

Lead task writing with the answer in the form its reader needs. Choose the opening
and shape for each register from the following table.

| Register | Opening and shape |
| --- | --- |
| Claude's prose to Adam | Answer, then only context that changes the next action; follow P-guide §5 (Claude to Adam). |
| Vault notes | Outcome or state first. Name the actor and identifier every time; keep searchable lexicon. Preserve the note's required structure and metadata. |
| Reviews | Finding first, never a verdict word or status recap. Give the observation, invite correction, then ask about a possible fix. Keep one finding per comment. See R-guide §11 (Writing a finding). |
| PR descriptions | Concrete problem and resulting behaviour, then scope, verification and material limits. Scale detail to the change. |
| Technical docs | Answer or task first; prerequisites, ordered actions, expected result and recovery where needed. Separate explanation from instructions. |
| Specs and ADRs (architecture decision records) | Requirement or decision first, with scope, constraints and checkable consequences. Separate binding text from explanation. |
| Correspondence | For email and sensitive messages, put the purpose, request or acknowledgement first, with enough context for this recipient. For apologies, name the act and responsibility; for condolences, acknowledge the loss without inventing feelings or memories. Deliver hard news plainly and state a request with its timing. |
| Personal essays | A true scene first; never manufacture one. Develop Adam's argument from his material; follow P-guide §9 (Personal essays and fiction). |
| Fiction | Follow only the project's `bible/` for voice. |

These conventions differ by register. In the essays column, “Adam's” means keep his
choice unless it blocks comprehension.

| Rule | Claude to Adam | Reviews | Specs and ADRs | Personal essays |
| --- | --- | --- | --- | --- |
| “We” | Never; use “I” or “you” | “Could we…” is allowed | — | Inclusive “we” is allowed |
| Hedges | Cut | Deliberate, to invite correction | Cut | Adam's |
| Metaphor | None | None | None | Adam's |
| Passive | Name the actor | Name the actor | Allowed; preserve responsibility | Adam's |
| Em and en dashes | Allowed | None | Allowed | Adam's |

- In vault notes, PR descriptions and technical docs, use literal language and name the
  actor. Correspondence can retain courtesy and warmth suited to the recipient.
- In reviews, a hedge must not weaken the finding's severity. End on the real question;
  don't append a reassurance or invent a question when there is no finding.
- Use plain writing for nonfiction; apply the register's specific conventions where
  they differ. Do not apply chat's paragraph limit to every durable document.

## 5. Claude to Adam

1. Open with the answer.
2. End with the ask on its own line; if there is no ask, end with a one-line summary.
3. Use at most three sentences per paragraph.
4. Keep a response to a few short paragraphs. Use a table, a list or split the response
   when more material is needed.

## 6. Write plain sentences

- Give each sentence one idea and each paragraph one job. Keep subject and verb close.
- Name who acted. Use “I” for the agent's actions and “you” for Adam's; don't hide a
  mistake in passive voice. Passive is valid when the actor is unknown or immaterial.
- Put a condition before the instruction it limits. Use the imperative for instructions.
- Use present tense for how something works and past tense for what happened. Keep
  other tenses when the meaning needs them; replace vague timing with a date or version.
- Prefer familiar words: “use”, “start”, “because”. Remove filler such as “just”,
  “obviously” and “please note”; don't tell a reader that their task is easy.
- Preserve precision. Use “can” for ability or permission, “might” for possibility and
  “must” for a requirement. Avoid “should” and “may” in ordinary prose; never soften
  or reinterpret a contractual keyword.
- Avoid mannered contrasts, personified documents, decorative closers and emphasis for
  rhythm. Vary sentence openings without changing terms for the same thing.
- Keep helper words and deliberate repetition when they prevent a reread or a wrong
  inference. Break a style rule when following it would make the writing less clear.

## 7. Apply editorial conventions

Use these defaults for task writing; preserve exact literals, quotations and contractual
notation. See the linked Google style pages for detailed conventions.

- **Numbers:** spell out zero through nine in ordinary prose; use numerals for 10 and
  higher, measurements and comparable data. Keep precision consistent; don't round away
  a boundary. See [Numbers](https://developers.google.com/style/numbers).
- **Dates and times:** spell out the month in prose, such as September 24, 2026; use
  `YYYY-MM-DD` for sortable dates. Include the time zone when timing matters; avoid
  ambiguous numeric dates and relative dates in durable instructions.
  See [Dates and times](https://developers.google.com/style/dates-times).
- **Units:** give the unit with the number, separated by a nonbreaking space where
  supported, such as 20 ms. Repeat units at both ends of a range; distinguish MB from
  MiB and identify ambiguous currencies.
  See [Units of measurement](https://developers.google.com/style/units-of-measure).
- **Links:** use descriptive text that makes sense alone; link directly to the source
  or relevant section. Explain unexpected downloads or navigation. Check relative links.
  See [Cross-references and linking](https://developers.google.com/style/cross-references).
- **Lists:** number ordered steps; use bullets for unordered items and tables for
  comparisons. Keep items grammatically parallel and punctuate complete sentences.
  See [Lists](https://developers.google.com/style/lists).
- **Headings:** use descriptive sentence case and a logical hierarchy without skipped
  levels. Number guide sections so they can be cited as “P-guide §7 (Apply editorial
  conventions)”. See [Headings and titles](https://developers.google.com/style/headings).
- **Code font:** mark exact commands, paths, identifiers and literal values. Use fenced
  blocks for multiline examples; distinguish placeholders from runnable input. Don't use
  code font for ordinary concepts or emphasis.
  See [Code in text](https://developers.google.com/style/code-in-text).
- **Abbreviations:** expand unfamiliar abbreviations at first use; avoid introducing one
  used only once. Keep exact product names and identifiers intact.
  See [Abbreviations](https://developers.google.com/style/abbreviations).

## 8. Make the writing accessible

- Use real headings, lists and text. Keep the reading order meaningful when styling is absent.
- Give informative images useful alt text and complex diagrams a text explanation.
  Use empty alt text for decoration; keep code and instructions available as text.
- Supply captions or transcripts for audio and video.
- Identify controls by label. Never make colour, position, shape or sound the only way
  to identify something or understand a result.
- Give tables headers and keep their structure simple. Use a list when comparison adds
  nothing. Use inclusive language without assuming a reader's abilities.
- Check the rendered document with zoom, keyboard navigation and a screen reader where
  applicable. Confirm links and instructions still make sense outside the visual layout.

Adapted from Google's [Write accessible documentation](https://developers.google.com/style/accessibility).

## 9. Personal essays and fiction

- Start an essay with a scene from Adam's material. If the material has no true scene,
  ask for one; don't invent an event, memory, detail or quotation.
- Develop one point per paragraph with the evidence or example it needs. Make the
  connection to the next point explicit; retain qualifications and answer real objections.
- Preserve Adam's flourishes, rhythm and British/Canadian spelling when editing.
  His metaphors, hedges and passive constructions can stay when readers can follow them.
- For fiction, use only the project's `bible/`. Treat the general fiction profile as
  historical; don't import it as a competing voice authority.
- For fuller paragraph and argument development, see the future essay *On Writing*.

## 10. Check preservation before sending

- Check documents automatically; check review comments and chat on request. Treat
  `brevity-enforcer` as a preservation check, not a cutter. Simplifying an explanation
  (`eli5`) is a separate task from shortening it.
- Read the result cold against the chosen register's shape, without the editor's account
  of what the revision was meant to preserve.
- Compare claims, evidence, qualifications, owners, actions, severity and obligations.
  Restore any cut needed to bound a claim or prevent a wrong inference.
- Preserve exact identifiers, figures, units and normative keywords, including their
  force. Don't promote, soften or delete a requirement during a prose edit.
- After cutting an existing draft, use
  [cutcheck.py](../skills/brevity-enforcer/scripts/cutcheck.py) to compare original and
  edited text, including any destination documents for moved material. Investigate each
  flagged loss; compare the meaning yourself to establish semantic preservation.
- Confirm that sources support the claims, needed terms are explained, links resolve
  and the final wording still says what the author intended. A zero-edit check is valid.
