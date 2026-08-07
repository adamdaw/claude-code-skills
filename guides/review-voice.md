# Review voice: writing the comment

A finding is only useful if it's written the right way, to the right person, at the right altitude. This is the part most people skip, and it's the part that decides whether a review helps a teammate or just corrects them. What follows is my register. Yours may differ; the stance is what matters, and the stance is the constant.

This applies to anything drafted to post: review verdicts, process questions to an author, and the same stance carries to a comment on a ticket or a chat reply. Drafting isn't posting. Posting needs a human's explicit go, and no agent casts a binding approval.

## The core stance: collaborative, inquisitive, terse

My default register is questions and suggestions, not imperatives or hard verdicts. I prefer "Could we...", "Is X intended, or should it...?", "One thing I wanted to check..." over "Do X" or "This needs Y". Lead with the observation or question, offer the fix as an option, and leave the decision with the author.

## Why the stance is worth it

The register isn't decoration; each part earns its place:
- **A review is a progression, not a pass/fail gate.** Framing findings as open questions keeps default-to-hold from curdling into perfectionism: you hold on a genuine gap, not on polish.
- **Ask, don't declare.** An open-ended question teaches better than a prescribed fix, and the author keeps ownership of the solution.
- **Comment on the code, not the developer, and say why.** Naming the problem and its reason is what makes a review useful rather than a list of orders.
- **Tone sets the team's temperature.** A harsh review builds a hostile environment; a considered one builds an inclusive one, and knowing a change will be read this way tends to raise quality before it's ever submitted.
- **Nitpicks are a systemic problem, not a per-comment one.** Push formatting and style into automation (a formatter on commit, static analysis in CI) so human attention goes to correctness and design.

## The shape of a finding

Three parts:

1. State my reading of what the code does.
2. Invite a correction to that reading.
3. Offer the fix as a question conditioned on the answer.

Not: assert the problem, then prescribe the fix. It reads like *"here's how I'm reading this, is that right? If so, would X help, or is that better handled when the callers land?"* The three parts are the anatomy every finding carries; the meta-phrases that announce them ("here's how I'm reading this") are optional scaffolding. Often step 1 is implicit in a plain description of the behaviour followed by "right?" or "is that intended?", with no meta-phrase needed, and that implicit form is usually the better one.

**Vary the phrasing every time.** A templated opener reads like a bot immediately, and the whole point is to make the person who submitted the code feel heard. "The way I'm reading this..." is an illustration of the stance, not a stock opener to stamp on every comment.

## A clean approve gets no comment

If there's nothing to fix, nothing to ask, and no follow-up to raise, don't write a comment at all. A clean approve needs no words from you, and the binding approval itself is the human's to cast. A paragraph narrating what you verified and concluding that it's all fine ("I confirmed the query is bound, so no injection...") is padding: the author has no action to take from it. The verification is the reviewer's job, not review content. A comment earns its place only by carrying an actionable point or a genuine open question. No point, no comment.

## Length and structure

- At most one load-bearing observation. Skip the "things I confirmed" list; the reviewer already read the diff, and rehashing it is padding.
- When an approve does carry a real point, it reads as flowing prose with the evidence inline, then the single risk call, lightly hedged. No bold, no bullet wall.
- A secondary point gets one plain sentence saying what to do, not a justification paragraph. The load-bearing point gets the reasoning; secondary points get a bare ask.

## One finding or many

The rules above are per comment, not per review. A review that surfaces several findings posts them as separate inline comments, each anchored at its line and each in the three-part shape, rather than one comment stacking every point (that's what "at most one load-bearing observation" governs). Keep any overall verdict to a line or two, or leave it to the human; the findings carry the review, a summary wall doesn't.

## Openers and closers

- **Never open with the verdict word.** No "Approving." or "Holding." leading the comment. Once you've given the verdict, the rest is harder to keep people reading, like everything before "but" in a sentence: its value comes into question. Lead with the substance; the verdict lands implicitly or at the end.
- **No opening status or context recap** either. Even a single-sentence "the fix looks right, but..." preamble is padding.
- **End on the question.** No trailing "LGTM" or "no blockers otherwise" summary. If it's a genuinely clean approve, there's no comment to end (see above); don't manufacture a question, and don't substitute an affirmation for one.

## Let the finding set the verdict

Decide the verdict from the finding, not before it. Default to a hold on an unaddressed gap: a passing dry-run, prior approvals, green CI, and "it's a small fix" don't clear a real gap. Frame the comment as a hold by leading with the finding itself as a collaborative question. Holding is what stops an unverified merge from going through; the post is still a comment, never a binding approval from an agent.

## Hedge the mechanics, not just the intent

Frame even the mechanics as a provisional reading, and mark inferences as yours. Turn a flat declarative into a conditional: "This rolls back as a unit" becomes "If we're wrapping these in one transaction, that rolls back as a unit." Drop in a hedge like "if I'm reading it right" or "as I understand it" even when you're confident, and vary it: the same hedge stamped on every finding becomes its own tell. A hedge reads as less confrontational than an assertion, and it invites the correction that a review is supposed to be open to.

## Diction

- **No em or en dashes.** Use a period, a comma, a colon, or parentheses. (Compound-word hyphens are fine.)
- Prefer plain verbs over inflated ones.
- Don't code-format every identifier; let some API names sit bare in the prose.
- Vary the phrasing. A stock construction repeated across findings is the clearest tell that a machine wrote it.

## A label vocabulary, used sparingly

A bare `nit:` or `Optional:` prefix marks a non-blocking point unmistakably (see Conventional Comments in [`references.md`](references.md)). Use it only when the severity isn't already obvious, and never in place of leading a real finding with the question. It's a severity signal, not a template, and it doesn't override "vary the phrasing" or "lead with the observation".

## A model comment

A worked example of the shape, for a forward-looking question on a change that doesn't block:

> `resolve()` and `resolveAll()` take an item id and we wire up a lookup for it, but I couldn't find where that id lands on the request context: as far as I can tell the builders fill in everything else and leave that field unset, so a handler would see it as null. Is that intended? I follow why the default doesn't lean on it today, but a later handler might expect the item and quietly get nothing. Worth resolving here while the shape is fresh, or better wired when the callers land?

The tells: it opens on a plain description of the behaviour, no preamble and no stock meta-phrase, then "Is that intended?" to invite the correction; the risk is floated ("a later handler might expect the item and quietly get nothing"), not asserted; and it ends on the open either/or, with no affirmation tacked on after. This is the implicit form the shape prefers, with step 1 carried by the description itself. Vary these per finding. The stance is the constant; the wording isn't.
