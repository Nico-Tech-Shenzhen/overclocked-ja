# CHARACTERS.md — Overclocked Voice Guide

**Status: Initial skeleton. No story has been translated yet.**

This file guides narrator and character voice, per story, in dialogue and narration.
*Overclocked* is a short story collection with **no single narrator voice across the
book**. Each story has its own narrator, register, and cast, and must be treated
independently.

Entries marked PLACEHOLDER have not yet been confirmed by source text evidence. Do not
invent detailed voice rules, pronouns, ages, genders, family relationships, or identity
details beyond what the source text actually establishes. Determine voice separately for
every story from its source text; do not carry a pronoun or register decision from one
story into another.

**Never consult, quote, or imitate any existing published Japanese translation** when
determining voice, especially for I, Robot; When Sysadmins Ruled the Earth; and Anda's
Game.

## Updating this file

Use `/oc-rule-update` to add voice rules as you encounter narrators and characters in the
text. Do NOT edit translated story files when updating this file.

---

## Cory Doctorow — story introduction voice

Each story is preceded by a short introduction written by Cory Doctorow in his own voice
(not any story's narrator or characters). This is an adult, personal, direct essay voice.

**First-person pronoun:** 「私」, or subject omission where natural — do not force 「僕」
or 「俺」 in these introductions.
**Voice:** Personal, direct, conversational nonfiction essay register.
**Notes:** Confirm details from each story's actual introduction text; do not assume the
same anecdotal content or tone Doctorow used in other works (e.g. *Little Brother*).

---

## Printcrime

**Narrator / voice:** First-person narrator, a young woman (name Lanie/レイニー, addressed
by her father). Retrospective narration recalling childhood trauma (a police raid) and a
later reunion with her father after his release from prison. Voice is direct, plainspoken,
working-class British diction ("coppers," "Da," "Ma," "newsies," "manky estate," "minicab").
Confirmed from `source/sections/01-printcrime.txt`; the source never states the narrator's
age at time of narration or explicit gender markers beyond the name "Lanie" — do not add
gender-specific description beyond what a natural Japanese first-person narration implies.
**First-person pronoun:** 「わたし」（ひらがな）— chosen as a natural, not overtly
gender-marked, retrospective narration register.
**Register:** Plain, direct, unsentimental about violence and loss; short declarative
sentences mixed with a few long run-on sentences at moments of emotional intensity.
**Cast / names:** Narrator = レイニー (Lanie); her father addressed as "Da" → rendered
consistently as 父さん; her mother referenced once as "Ma" → 母さん (she has died before the
story's later scenes; no other detail about her is established).
**Notes:** This is the opening, and shortest, story in the collection. Retranslated in full
from `source/sections/01-printcrime.txt` (2026-08-02), status: draft. Resolved: source
phrase "The ipolice paid in high-grade pharmaceuticals" — "ipolice" read as a scanning
artifact for "the police" (the sentence describes the police paying an informant, Da's
customer, in pharmaceuticals as a reward for the tip). Translated as 警察 with the payment
made explicit ("その密告への見返りとして"); no TODO remains.

---

## When Sysadmins Ruled the Earth

**Narrator / voice:** Third-person limited, close to Felix throughout (not a first-person
narrator, unlike Printcrime). Confirmed from `source/sections/02-when-sysadmins-ruled-the-earth.txt`.
Rendered in plain narrative Japanese without a narrator pronoun; dialogue carries the
character voices instead.
**First-person pronoun (in dialogue):** Felix uses 俺 (casual, blue-collar-adjacent IT-guy
register); Kelly uses あんた/わたし in dialogue with Felix (direct, familiar-married-couple
register); Van uses 俺; Will Sario uses 俺, clipped and confrontational; Popovich uses 俺;
Queen Kong's chat-log dialogue uses casual/blunt phrasing without gendered pronoun markers
beyond the fact she is established as a woman; Rosa uses わたし.
**Register:** Sysadmin/IT workplace jargon and profanity-heavy banter between Felix and Van;
IRC/newsgroup posts rendered as plain unpunctuated-feeling chat lines, lowercase-flavored in
Japanese where the English source is lowercase/typo-casual (Queen Kong's and Sario's chat
lines). Preserve tech terms (BGP, DNS, IRC, root, PEBKAC, port 1337/"leet") per
`glossary.tsv`. Preserve profanity intensity in dialogue (くそ, クソ, etc.) without softening.
**Cast / names:** Felix Tremont（フェリックス・トレモント）— protagonist, sysadmin, later
"Prime Minister of Cyberspace." Kelly（ケリー）— his wife. Their son William, nicknamed
2.0（2.0）, referred to by that nickname throughout except when his birth-certificate name
"Will" briefly causes confusion with Will Sario. Van（ヴァン）— Felix's colleague and
friend, a type-two admin. Will Sario（ウィル・サリオ）— confrontational admin who argues for
deliberately killing the Internet; distinct character from Felix's dead son "Will," a
deliberate source-text confusion preserved in translation. Uri Popovich（ウリ・ポポヴィッチ）
and Diego Rosenbaum（ディエゴ・ローゼンバウム）— the "Bastard Operators From Hell" who
organize the building. Queen Kong（クイーン・コング）— a woman sysadmin running Google's
data center, known only by this handle. Rosa（ローザ）— a former RN turned web designer,
encountered after the group disperses.
**Notes:** A published Japanese translation of this story exists elsewhere. It was not
consulted at any point. Preserve 2006-era computing/networking references (IRC, Usenet,
newsgroups, BGP routers, IPv6, Blackberry, Flickr, Blogger/Typepad/LiveJournal, Google's
handmade-PC origin story) without modernizing. The "Will"/"Will Sario" name collision (§ line
149 vs. § line 309 of the source) is intentional in the English text and preserved as-is in
Japanese — 「ウィル」 for the son, 「ウィル・サリオ」 or 「サリオ」 for the sysadmin, to keep the
reader's momentary confusion intact without over-clarifying.

**"Felix's Law" (source: "Law of Infinite Universal Perversity -- AKA Felix's Law"):**
This is not a real named law; it is a mock-formal joke Felix (or the narrator, in his
voice) coined for himself after noticing he can never fix anything remotely after 1AM.
Render it so the Japanese explicitly shows Felix naming/calling it that himself (e.g.
「彼はそれを『森羅万象意地悪の法則』、略して『フェリックスの法則』と呼んでいた」), not as an
opaque literal compound (avoid a bare, uncontextualized calque like
「無限宇宙的意地悪の法則」) and not as if it were a famous external law the reader should
already recognize. Preserve the source order: the observed pattern (nothing gets fixed
remotely after 1AM) comes first, the joke name comes as the punch line after.

---

## Anda's Game

**Narrator / voice:** Third-person limited, close to Anda throughout (same narrative mode as
"When Sysadmins Ruled the Earth" — not a first-person narrator). Confirmed from
`source/sections/03-andas-game.txt`. Rendered in plain narrative Japanese without a narrator
pronoun; dialogue carries character voice.
**First-person pronoun (in dialogue):** Anda uses あたし (casual British schoolgirl register,
slightly bratty/sassy with her father, more vulnerable/earnest with Lucy and Raymond); Lucy
("Sarge") uses あたし with blunter, more American-teen phrasing (だよ/でしょ-heavy, confident,
occasionally dismissive); Raymond speaks formally and gently, private わたし implied rather
than stated (his lines are almost entirely in-game chat text, kept terse and grammatical,
reflecting a careful non-native-English speaker who is nonetheless highly articulate); Liza
the Organiza uses あたし with a brash, coach-like Australian-inflected register ("ひよっこ"
for "chicken(s)" as her address term); Anda's Da uses おれ/パパ in dialogue with her,
blustery-but-affectionate working father register; Anda's Mum is warm/fussing, minimal direct
dialogue.
**Register:** Contemporary (2004-era) British schoolgirl slang mixed with MMORPG/gamer chat
culture. In-game chat lines (marked with `>` in source) are rendered as terse, often
unpunctuated Japanese chat-text to preserve the typed/casual feel, matching the source's use
of lowercase and dropped punctuation for excited or careless typing (e.g. Anda's
"!!!!!!!!!!" chat line, the "u cn have my gold sorry!!!11!" begging noob). Preserve UK-specific
vocabulary and idiom sense (podge, chav, PE, hockey pitch, "Miss Pot"/"Mr Kettle" callback to
"pot calling the kettle black") — some of these are rendered by natural equivalent register
rather than literal gloss; the Pot/Kettle nicknames are kept as カタカナ nicknames
（ポットちゃん／ケトルさん）without a full idiom explanation, since the source itself does not
explain the idiom either — flagged here, not as a visible in-text note, per the guide's rule
against over-explaining what the source leaves implicit.
**Cast / names:** Anda（アンダ）— 12-year-old British protagonist, in-game handle
"Kali"（カリ）. Lucy（ルーシー）/ "Sarge"（サージ）— Anda's American platoon-leader friend and
mission partner, based in the US Midwest. Liza the Organiza（オーガナイザのライザ）— adult
professional gamer/organizer, Australian-accented, leader of Clan Fahrenheit, visits girls'
schools recruiting members; addresses girls as "chickens" → ひよっこ. Clan
Fahrenheit（クラン・ファーレンハイト）— the in-game guild/clan both girls belong to. Raymond
（レイモンド）— Mexican labor organizer trying to unionize the gold-farming child laborers,
speaks to Anda in-game under his real name. Anda's parents are referred to only as Da/Mum in
source, rendered as 父さん／母さん (no proper names given in source; do not invent any).
**Notes:** A published Japanese translation of this story exists elsewhere. It was not
consulted at any point. Preserve 2004-era MMORPG culture (BFG/"Big Friendly Gun" as a generic
superweapon term, PayPal, PC バン／PC Baang as a Korean-style internet café, respawn gates,
scrying scrolls, eBay gold-selling) without modernizing. The story contains sustained,
unsanitized fat-shaming dialogue (Anda's own body image distress, the bullying scene at the
PC café) and one scene of a boy punching and verbally abusing Anda — per
`TRANSLATION_GUIDE.md` rule 6, this intensity is preserved rather than softened. The Spanish
chat-line "no porfa necesito mi plata" (broken-Spanish begging, spoken by a child gold-farmer)
is preserved untranslated in the Spanish in one instance (matching the source's own
in-story English gloss/paraphrase of it elsewhere) — kept as Latin-alphabet text embedded in
the Japanese, per "verbatim-preserve items" in the checklist.

---

## I, Robot

**Narrator / voice:** PLACEHOLDER — determine from `source/sections/04-i-robot.txt`.
**First-person pronoun:** PLACEHOLDER.
**Register:** PLACEHOLDER.
**Cast / names:** PLACEHOLDER.
**Notes:** A published Japanese translation of this story exists elsewhere. Do not consult it under any circumstance. Title wordplay against Asimov's "I, Robot" is provisional; do not finalize the Japanese title without user approval.

---

## I, Row-Boat

**Narrator / voice:** PLACEHOLDER — determine from `source/sections/05-i-row-boat.txt`.
**First-person pronoun:** PLACEHOLDER.
**Register:** PLACEHOLDER.
**Cast / names:** PLACEHOLDER.
**Notes:** Title is a pun (companion piece to "I, Robot"); preserve the wordplay function rather than translating literally. Japanese title candidate is provisional until user approval.

---

## After the Siege

**Narrator / voice:** PLACEHOLDER — determine from `source/sections/06-after-the-siege.txt`.
**First-person pronoun:** PLACEHOLDER.
**Register:** PLACEHOLDER.
**Cast / names:** PLACEHOLDER.
**Notes:** Closing story in the collection.

---

## Name conventions

| English | Japanese rendering | Note |
|---------|-------------------|------|
| (none confirmed yet) | | Add entries here only after translating the relevant story from its source text. |
