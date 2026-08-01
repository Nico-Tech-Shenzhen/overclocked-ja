# Translation Guide — Overclocked 日本語訳

See `CLAUDE.md` for operational rules. This guide covers substance.

## Project scope

Japanese translation of:

> *Overclocked: Stories of the Future Present*
> Author: Cory Doctorow
> Original publisher: Thunder's Mouth Press, a division of Avalon Books (2007)
> License: Creative Commons Attribution-NonCommercial-ShareAlike 2.5
> Free download: https://craphound.com/overclocked/download/

This project covers the original six-story collection only: Printcrime, When Sysadmins
Ruled the Earth, Anda's Game, I, Robot, I, Row-Boat, and After the Siege. It does not
include the later expanded edition, *Overclocked: More Stories of the Future Present*,
and no stories from that edition should be added.

The Japanese translation is also released under **CC BY-NC-SA 2.5**.

Published Japanese translations of some stories in this collection (at least I, Robot;
When Sysadmins Ruled the Earth; and Anda's Game) exist elsewhere. **They must never be
consulted, searched for, quoted, or imitated** — not as a translation source, not as a
comparison text, not as phrasing reference, not as review material. This translation is
produced solely and independently from the official CC-licensed English source.

## Attribution requirements (mandatory in every story file)

Every `docs/ja/*.md` file must include the following visible footer `<small>` block,
adapted naturally for the page:

```html
<small>
*原著*: *Overclocked: Stories of the Future Present* © Cory Doctorow<br>
*出版*: Thunder's Mouth Press, 2007<br>
*日本語訳*: 高須正和（@tks） — [https://takasumasakazu.net](https://takasumasakazu.net)<br>
*協力*: ニコ技深圳コミュニティ<br>
*ライセンス*: CC BY-NC-SA 2.5<br>
*注記*: 本翻訳は、原著の Creative Commons ライセンス条件に従って公開する高須正和による日本語訳であり、出版社による公式日本語版ではありません。
</small>
```

Confirm the most accurate copyright-year wording from the official source before
finalizing the footer. Do not invent a year range.

Never use the phrases "公式日本語版", "公認翻訳", or "正規翻訳" anywhere in translated content.

## Translation priorities

Apply in order when rules conflict.

**1. Japanese reader clarity comes first.**
Translate so a Japanese reader can follow without decoding English-shaped prose. If a
technical concept needs explanation, explain the function first, then give the formal term.

**2. Translate meaning and voice, not English syntax.**
Rebuild sentences in natural Japanese. Do not carry over English noun chains, passive
abstractions, or hedged constructions when they obscure the point.

**3. Preserve rhetorical information timing.**
Surface English clause order does not need to be preserved, but distinguish between
surface syntax (freely rebuildable) and an ordering that creates characterization,
humor, emphasis, suspense, interruption, or a punch line (preserve the sequence).

**4. Preserve every paragraph and structural element.**
Do not summarize, condense, skip, or invent text. Translate every paragraph, including
each story's author introduction.

**5. Verify agency after rebuilding sentences.**
When rebuilding English sentences in Japanese, check who acts on whom — do not let
English surface grammar silently change agency, possession, or control. Recheck
transitive/intransitive and active/passive relationships after every rebuild.

**6. Preserve vivid metaphor without Japanese tautology.**
Preserve vivid, grotesque, humorous, or excessive metaphors rather than softening or
abstracting them. After preserving the image, remove any semantic redundancy introduced
in Japanese.

**7. Technical accuracy still matters.**
Do not simplify by changing meaning. Preserve technical facts, protocol names, product
names, hacker/gaming slang (when identifiable), and source order.

## Core translation rules

- **Faithful**: Translate every paragraph. Do not summarize, condense, or skip content.
- **Complete**: Do not omit paragraphs, sentences, dialogue, author introductions, or any
  structural element.
- **No invented text**: If source text is unclear, mark with `<!-- TODO: verify: [desc] -->`.
- **Preserve order**: Keep all paragraphs in original order. Do not reorganize.
- **Consult glossary.tsv** before translating technical or recurring terms.
- **Katakana** for established loanwords; kanji compounds where natural.

## Collection-specific rules

1. **There is no single narrator voice across the collection.** Each of the six stories
   has its own narrator and register.
2. **Determine voice separately for every story from the source.** Read the story before
   assigning a pronoun, register, or tone in `CHARACTERS.md`.
3. **Do not globally force `僕`, `私`, or `俺`.** The correct first-person pronoun (or
   omission) is decided per story, per narrator, from source evidence.
4. **Cory Doctorow's story introductions use an adult, personal, direct essay voice**;
   normally use `私` or omit the pronoun naturally. This voice is distinct from any
   story's narrator.
5. **Preserve early- and mid-2000s computing language, online-game culture, sysadmin
   slang, political assumptions, and science-fiction terminology.** Do not modernize
   technology, platforms, or cultural references to a 2020s equivalent.
6. **Do not sanitize profanity, violence, grief, grotesque imagery, or political anger.**
   Preserve the intensity of the source.
7. **Preserve jokes, puns, delayed judgments, technical wordplay, and title wordplay.**
   Rebuild the Japanese freely to keep the comedic or rhetorical function intact.
8. **Title translations are provisional until approved by the user.** Do not finalize a
   Japanese story title in public-facing content; a candidate may appear as an internal
   note only.
9. **Never infer gender, age, family order, identity, or relationship details that the
   source does not establish.**
10. **Each story gets its own character and voice section in `CHARACTERS.md`.** Do not
    merge or share voice rules across stories.
11. **Add glossary terms only after reading them in context.** Do not pre-populate
    `glossary.tsv` with guessed terms before the relevant story has been read.
12. **Existing Japanese translations must never be consulted.** This applies to every
    story, and with particular force to I, Robot; When Sysadmins Ruled the Earth; and
    Anda's Game, for which published Japanese translations are known to exist.

## Sentence construction

**Rebuild sentences; do not mirror English syntax.**

- Split long English sentences at natural pauses.
- "and / but / since / while / hence" chains → separate Japanese sentences.
- Resolve ambiguous pronouns from context.
- Do not omit an explicit subject when a long sentence becomes ambiguous about who is acting.
- Put context/topic before predicate.
- Cause/effect: put reason first when it aids readability.

## Surface syntax versus rhetorical information timing

English surface clause order does not need to be preserved. Reorder subjects, modifiers,
reasons, and clauses freely when doing so produces immediately understandable Japanese.

However, distinguish between:
- **Surface syntax** — English grammatical scaffolding that may be freely rebuilt.
- **Rhetorical information sequence** — an ordering that creates characterization, humor,
  emphasis, suspense, interruption, or a punch line.

Preserve the sequence when the original order performs a literary function; rebuild
freely otherwise.

Structures that typically carry rhetorical function and must retain their sequence:
- setup → reason → conclusion
- observation → explanation → sarcastic judgment
- proper noun or event → afterthought evaluation
- list of traits → dismissive conclusion
- action → parenthetical interruption → continuation

**Rule-boundary clarification:**
- Clarity over literal English syntax — always.
- Rhetorical sequence over merely tidy Japanese — when it carries voice or humor.
- Not every English clause order has rhetorical significance; identify the function
  before deciding.
- Technical explanations may be reordered more aggressively for comprehension.
- Jokes, delayed evaluations, interruptions, and punch lines require more caution.
- Do not mechanically preserve every dash or every sentence boundary.
- Preserve function, not word order.

## Verify agency after rebuilding sentences

When rebuilding English sentences in Japanese, verify who acts on whom:
- Do not preserve English surface grammar when it changes agency, possession, or control.
- Check transitive/intransitive and active/passive relationships after every rebuild.
- After rebuild, recheck: does the Japanese subject do what the English subject does?

## Do not infer sibling age or birth order

English `brother` and `sister` are not age-marked. Rules:
- Never add 「兄」「弟」「姉」「妹」 unless the source text or established context confirms
  age order.
- Default to 「兄弟」「姉妹」 or restructure the sentence.
- 「家族」 may be used only when the exact sibling relationship is not important and
  Japanese reads more naturally; report the loss of specificity when it matters.
- Do not infer age, rank, gender, family order, or any relationship detail beyond the
  source.

## Parse compressed coordination and idioms before translating

When a sentence contains compressed or humorous coordination, identify the grammatical
role of each element before translating:
- Do not invent groups of people when the source coordinates two reasons, standards, or
  judgments.
- Translate the intended proposition, not the apparent English noun sequence.
- Recheck parallel constructions for scope and attachment.

## Preserve vivid metaphor without Japanese tautology

- Preserve vivid, grotesque, humorous, or excessive metaphors rather than softening or
  abstracting them.
- After preserving the image, remove any semantic redundancy introduced in Japanese.
- Preserve insult or intensity strength unless Japanese comprehension genuinely requires
  adjustment.

## Translate perception expressions by function, not word-by-word

- For visual conspicuousness: 「嫌でも目につく」「いやでも目に入る」
- For cognitive obviousness: 「いやでもわかる」
- Avoid unnatural collocations that mix sensory registers.
- Split overloaded descriptions when Japanese rhythm improves from doing so.
- Confirm whether the source phrase is about vision, cognition, or social awareness
  before choosing a rendering.

## Translate states and textures as sensory language

Do not translate an English state adjective as a completed physical action merely
because the same word can also function as a verb. Choose natural Japanese sensory
language for texture, smell, fluidity, and physical condition. Preserve grotesque or
low-register comparisons that are part of a narrator's voice; do not sanitize them.

## Avoid redundant synonym glosses

- Do not write parenthetical glosses that repeat the same meaning in different words
  (e.g. 「ハンドル（ハンドルネーム）」).
- Parentheses should add information (the English original, an abbreviation expansion,
  or a context note), not repeat the same meaning.
- On first mention, use the term from `glossary.tsv`; add the English form in
  parentheses only when the English itself carries meaning for the reader.

## Preserve afterthoughts and delayed evaluations; limit noun repetition

When the source repeats a proper noun because of English sentence structure, Japanese
may replace the second occurrence with 「これ」「それ」 or a local restructuring.

Do not remove an afterthought, boast, judgment, or punch line merely to avoid
repetition. Preserve the timing of the evaluation even when the noun itself is not
repeated.

See also **Surface syntax versus rhetorical information timing** above.

## Locative precision

- Distinguish 「〜で」 (at/inside a location) from 「〜周辺で」 (in a location's vicinity/neighborhood).
- Resolve English prepositions and broad locative phrases according to the actual scope
  described in the source.

## Technical vocabulary policy

Always check `glossary.tsv` first. If a term is missing, add it only after reading it in
context in the story being translated — see Collection-specific rule 11.

**Decision rules:**
- Prefer the Japanese term from `glossary.tsv`.
- Security/networking/gaming terms: expand abbreviation on first mention, use
  abbreviation after.
- Hacker/sysadmin/gamer culture terms: check whether the English term itself is part of
  the meaning. If so, keep English in parentheses on first use.
- Do not overload sentences with parenthetical glosses.

**First mention pattern:** Japanese term（English term）
**After first mention:** Japanese term alone

## Setting preservation rule

Each story is set in its own early- or mid-2000s near-future context. Do not silently
modernize:
- Technology, platforms, and services referenced in the story
- Online game culture and sysadmin/IT workplace culture
- Political assumptions embedded in the story
- Terminology from the period

If a period reference is confusing for a 2020s Japanese reader, add a short translator's
note in a clearly marked HTML comment, but preserve the original text.

## Translator notes

Keep translator notes **rare and clearly marked**.

Use HTML comment for internal TODO:
```html
<!-- TODO: TN — [reason for note] -->
```

Use visible note block only when the reader genuinely needs context:
```markdown
> [!NOTE]
> 訳注：[短い説明]
```

Do not add translator notes for technology, culture, or vocabulary that a Japanese
reader familiar with tech and internet culture would already know.

## Technology and cultural explanation policy

Do not automatically add translator explanations for every real technology or cultural
concept.

- If the narrator immediately explains it, do not explain it in advance.
- If the concept is essential and the source does not explain it, add a short natural
  clarification on first mention.
- If it is not necessary to follow the scene, leave it unexplained.
- Do not duplicate a narrator's own technical explanation.
- Do not turn an explanation into textbook prose.
- Preserve the voice established by the story's own narrator.

## Rule Candidates

If you identify a recurring translation issue that may be worth generalizing across
stories, do not silently modify this guide, `CHARACTERS.md`, or `glossary.tsv`. Propose
it as a **Rule Candidate** (Problem / Proposed Rule / Rationale / Expected Scope /
Possible Risks) per `CLAUDE.md § Rule Proposal Policy`. The human translator decides
whether to adopt it. Local, story-specific decisions should remain local fixes and not
become project-wide rules.

## Review-only commands

`/oc-postcheck` and `/oc-full-recheck` are review-only and must not rewrite translated
prose. `/oc-rule-update` and `/oc-rule-audit` edit only `TRANSLATION_GUIDE.md`,
`CHARACTERS.md`, and/or `glossary.tsv`, and must not edit `docs/ja/*.md` or retranslate
content.

## LLM translation checklist

Before marking any section complete, verify all items:

1. Narrator voice for this specific story matches the confirmed entry in `CHARACTERS.md`
   (or is newly determined from source evidence, not assumed from another story).
2. No paragraphs, sentences, dialogue lines, or author introduction omitted.
3. No text invented; unclear source marked with TODO comment.
4. Technical terms follow `glossary.tsv`; expand on first use.
5. No unnecessary katakana jargon; use natural Japanese equivalents.
6. Ambiguous pronouns resolved to explicit nouns.
7. Verbatim-preserve items (handles, URLs, protocol names, brand names) preserved exactly.
8. Setting is not modernized; period technology and culture preserved.
9. `<small>` attribution footer present at bottom.
10. No "公式日本語版", "公認翻訳", "正規翻訳" in any text.
11. No indication that an existing published Japanese translation was consulted.
12. `python scripts/validate_sections.py` passes zero errors.
13. `python scripts/validate_links.py` passes zero errors.
14. Frontmatter title and translation_status are accurate.
15. No credit/license block under the story title; attribution is footer-only.
16. UTF-8 encoding with no mojibake or replacement characters.
