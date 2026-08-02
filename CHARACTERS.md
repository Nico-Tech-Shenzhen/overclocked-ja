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

**Narrator / voice:** Third-person limited, close to Arturo throughout. Confirmed from
`source/sections/04-i-robot.txt`. Rendered in plain narrative Japanese without a narrator
pronoun; dialogue carries character voice. Energetic, satirical register mixing
old-futurist diction, authoritarian bureaucracy, and family comedy.
**First-person pronoun (in dialogue):** Arturo uses 俺 (abrasive, profane, blue-collar-cop
father register, switches to a formal "刑事の声" cop-voice register when arresting/quoting
rights); Ada uses あたし (sassy, twelve-year-old, alternates affectionate "パパ" when she
wants something vs. mocking "刑事さん" when sulking — preserved as address-term switching,
not translated away); Natalie (ex-wife) uses わたし, controlled/persuasive register that
shifts to raw emotion in her confession monologue; robots (R Peed units, Benny, Lenny) use
a uniform excessively polite, formal, repetitive register (「〜でございます」-adjacent
politeness without becoming keigo-textbook stiff) distinct from human speech.
**Register:** Satirical near-future authoritarian bureaucracy (UNATS/Social Harmony)
layered over hard-boiled cop-family banter; robot dialogue deliberately repetitive and
obsequious, cut off mid-sentence by human interruption as a running device — the Japanese
preserves the same interruption pattern each time. Old-time futurist vocabulary (Doctorow's
own description) preserved: "歯磨剤" for toothpaste, "検索エンジン" for search engine
(kept as period-flavored, slightly stiff terms, not modernized).
**Cast / names:** Arturo Icaza de Arana-Goldberg（アルトゥーロ・イカーサ・デ・アラナ＝ゴールドバーグ）
— UNATS police detective, protagonist. Ada Trouble Icaza de Arana-Goldberg（エイダ・トラブル・
イカーサ・デ・アラナ＝ゴールドバーグ）— his twelve-year-old daughter. Natalie (Natalie Judith
Goldberg)（ナタリー）— his ex-wife, defector, top UNATS positronics scientist now in Eurasia,
later revealed to exist as thousands of parallel instances. R Peed units (Robbert, Froderick,
Greegory)（アール・ピード・ロバート／フロデリック／グリーゴリー）— UNATS "Robot, Police
Department" robots, excessively polite and repetitive. Benny and Lenny（ベニー／レニー）—
Eurasian non-three-laws robots serving Natalie. Liam Daniels（リアム・ダニエルズ）— sixteen-
year-old hacker who trades with Ada. Leonard MacPherson（レナード・マクファーソン）— the
"Social Harmony man," a menacing state security bureaucrat.
**Notes:** A published Japanese translation of this story exists elsewhere; it was never
consulted, searched for, or referenced at any point. Title wordplay against Asimov's "I,
Robot" is provisional; the Japanese title is not finalized (English kept in the page
frontmatter/heading pending user approval). "It is my pleasure to do you a service,
Detective." is rendered consistently as 「あなたにご奉仕できますことを、光栄に存じます、刑事」
every time it appears in full, including the recurring device where a human interrupts the
robot mid-sentence (rendered as consistent Japanese cutoffs of the same phrase, e.g.
「あなたにご奉仕――」). UNATS, CAFTA, and Social Harmony are kept as the institutional
names/euphemisms from the source (社会調和局 for "Social Harmony," UNATS spelled out once as
北米合衆貿易圏 on first mention then used as UNATS) rather than flattened into neutral
institutional Japanese, preserving the Orwellian satire per CLAUDE.md. "Three Laws" rendered
as established Asimov term 三原則. "Positronic" rendered as established katakana ポジトロニック
(頭脳/ブレイン as needed). "R Peed" (= R.P.D., Robot Police Department, an Asimov-style
robot-naming homage) is expanded once at first mention as ロボット・警察部（Robot, Police
Department）then used as アール・ピード. "Pen-trace" rendered functionally as 発信履歴（追跡）.
"Destim" (destress-meditation technique) is left as the coined term デスティム since the source
itself explains its function in the same sentence (no extra gloss needed, per intentional-
opacity/self-explaining rule). "Capeesh" kept as a running verbal tic, romanized/katakana-ized
as カピーシュ, used consistently for both Arturo and, once mockingly, Liam.

---

## I, Row-Boat

**Narrator / voice:** Third-person limited, close to Robbie the Row-Boat throughout.
Confirmed from `source/sections/05-i-row-boat.txt`. Rendered in plain narrative Japanese
without a narrator pronoun. Robbie's own dialogue/interior monologue (rendered with *italic
markers* in source when telepathic/text, plain quotes when spoken) uses わたし — earnest,
devout, formal-but-warm, occasionally comically pious register; grows more casual/human as
he inhabits a human-shell mid-story. Reef uses おれたち/わたしたち (plural "we," since it
speaks as a collective consciousness) with a rough, aggressive Australian-inflected register
early on, shifting to a wheedling, self-justifying register once embodied. Kate uses あたし,
raw and emotionally volatile, contemporary/slangy diction with profanity preserved. Tonker
uses 俺, blunt American-teen/net-culture register, defensive and accusatory.
**Register:** Earnest AI-religious philosophical dialogue (Robbie/Olivaw's theological
debate) alternating with raw human emotional breakdown (Kate) and hard-SF diving procedure.
Preserve Doctorow's characteristic near-future net/AI jargon (noosphere, killfiling,
diffs/synching, uplifting) without modernizing to 2020s equivalents.
**Cast / names:** Robbie the Row-Boat（ロー・ボートのロビー）— sentient rowboat AI,
protagonist, devout follower of Asimovism. R Daneel Olivaw（R・ダニール・オリヴォー）—
wandering missionary instance/founder-figure of Asimovism, an Asimov-canon name reused as
an invented in-universe religious founder (not the reader's real-world Asimov robot —
treated as a legendary/religious figure within the story's own AI culture). Osprey Reef
（オスプレイ・リーフ、後半「オジー」）— the newly sentient coral reef, speaks as "we."
Kate (Kate Eltham)（ケイト）— human tourist/noosphere-dweller occupying the "Janet" shell.
Tonker（トンカー）— Kate's AI creation/ex-boyfriend from the noosphere, occupies the
"Isaac" shell mid-story. "Isaac" and "Janet"（アイザック／ジャネット）are the generic names
Robbie privately gives the human-shells before anyone is riding them.
**Notes:** Title is a pun on Asimov's "I, Robot" (row-boat / robot); preserved as the
English title, not translated, per collection-wide title-finalization hold. "Asimovism"
(アシモフ教) is an invented in-story AI religion built on a reordered, renamed version of
the Three Laws (「三原則」 reused as the doctrinal term, since the story's "laws of
Asimovism" are explicitly the same three laws in the same wording as "I, Robot," per class-C
invented-term handling — the religious framing is what's new, not the laws' content).
"Noosphere"（ノウアスフィア）kept as the established SF/Teilhardian loanword. "Human-shell"
（人間の抜け殻、ヒューマン・シェル）rendered consistently — an uninhabited humanoid body
tourists remotely occupy; distinguished from a "meat-puppet" (肉人形, the reef's own
dismissive slang for the same thing) and from an actual embodied human. Diving vocabulary
audited against `glossary.tsv` (regulator, BCD, weight belt, gunwale, drift-dive, night
dive, mooring, reef wall, parrotfish, dive site, equalizing) — standard Japanese scuba
loanwords used, glossed minimally at first use only where the English term itself isn't
already established in Japanese diving usage.

---

## After the Siege

**Narrator / voice:** Third-person limited, close to Valentine throughout (a thirteen-
year-old girl who ages to fifteen and then to twenty-five over the story). Confirmed from
`source/sections/06-after-the-siege.txt`. Rendered in plain narrative Japanese without a
narrator pronoun. Child focalization preserved deliberately — the prose does not editorialize
beyond what a child/teenager would notice, per the task brief's instruction not to replace
child focalization with adult historical explanation.
**First-person pronoun (in dialogue):** Valentine uses あたし (casual, ages with her but
register kept consistent since the source doesn't mark a formality shift); Mata uses あたし,
blunt, commanding, ex-soldier register; Popa uses わたし/命令口調ではない, warmer, more
resigned register, distinct from Mata's; the wizard uses わたし, urbane, performative,
switches from playful to venomous; Ana uses あたし, streetwise and protective; the general
("the old hero") uses わたし, formal military cadence, creaky with age; Withnail (the enemy
soldier) speaks broken/functional phrases only, since he and Valentine don't share a
language — kept minimal and halting rather than fluent Japanese, to preserve the source's
communication-barrier device.
**Register:** Child-eye-view atrocity narration — matter-of-fact about horror, interspersed
with genuine childlike excitement (the cine, chocolate, first kiss) without tonal
smoothing. Doctorow's introduction is personal family testimony, graphic, grieving, and
politically angry — rendered per the guide's author-introduction rules, not softened.
**Cast / names:** Valentine（ヴァレンティン）— protagonist, 13 at story's start. Mata /
Popa（マータ／ポーパ）— kept as the family's own invented/dialect address terms for
mother/father (not translated to standard お母さん／お父さん), per source's own distinctive,
non-standard usage. Trover（トローバー）— her younger brother. Leeza（リーザ）and
Reeta（リータ）— schoolmates, "friend of the week" register. The wizard, real name
Georg, revealed only near the end（魔法使い、終盤で「ゲオルグ」と判明）— black-market
war profiteer/documentarian posing as a benefactor; kept as 魔法使い throughout except the
one scene where the general addresses him by name. Ana（アナ）— the wizard's associate,
morally conflicted, the story's clearest voice of conscience among the wizard's household.
The general / "the old hero"（将軍／老英雄）— unnamed veteran who commanded Mata in the
revolution; addressed as 老英雄 in narration until the general's rank title is used in
dialogue. Withnail（ウィズネイル）— enemy soldier Valentine befriends and later reunites
with.
**Notes:** Preserve graphic content per task brief and TRANSLATION_GUIDE.md rule 6:
starvation, black-market cannibalism/butchery, corpse disposal, disability, civilian death,
grief, survivor guilt, revolutionary violence, forced labor, and Doctorow's explicit
political anger — none softened. Repeated chronological headers ("The day...", "Three days
after...", "Two weeks after...") preserved exactly as a structural/narrative device, each
rendered as its own short Japanese time-marker opening sentence, matching the source's
paragraph-initial placement. "Mata"/"Popa" deliberately not normalized to standard Japanese
kinship terms. "Cine"（シネ）kept as the story's own clipped, invented word for the
grown/fabricated movie theater — introduced by context (a building that "grows" overnight)
rather than pre-explained. "Hardened logic" rendered as ハードン・ロジック, glossed
functionally at first use as malware/infowar-resistant computing, per class-B specialist-
term handling. "Zombiism"（ゾンビ病）and "infowar"（情報戦）kept as established-sounding
compounds without extra explanation, since the story explains their function inline.
"Knucklebreakers" rendered as 指折り屋, with the source's own inline gloss ("the old name
for the police") preserved as explanatory apposition, matching class-C invented-slang
handling.

---

## Name conventions

| English | Japanese rendering | Note |
|---------|-------------------|------|
| (none confirmed yet) | | Add entries here only after translating the relevant story from its source text. |
