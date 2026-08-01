# Skill: oc-translate

Translate a section of *Overclocked: Stories of the Future Present* into Japanese end-to-end.

## Arguments

Accepts any of:
- `front-matter` — common collection forematter (READ THIS FIRST / license notice)
- `printcrime` — Cory Doctorow's introduction to the story, plus the complete story
- `when-sysadmins-ruled-the-earth`
- `andas-game`
- `i-robot`
- `i-row-boat`
- `after-the-siege`
- `license` — complete Creative Commons legal code (not translated; reference only)

**Six stories only.** Never add stories from the expanded "More Stories of the Future
Present" edition. Never consult any existing published Japanese translation — this
applies with special force to I, Robot; When Sysadmins Ruled the Earth; and Anda's Game.

## Steps

**Step 1 — Verify repo state**
```bash
git status && git log --oneline -3
```
Confirm clean working tree.

**Step 2 — Read project files (required before any translation)**
Read in this order:
1. `CLAUDE.md`
2. `TRANSLATION_GUIDE.md`
3. `CHARACTERS.md`
4. `glossary.tsv`
5. `docs/.vitepress/config.mts` (check existing sidebar entries)

**Step 3 — Locate and read the source section**
Find the relevant file in `source/sections/`:
- front-matter → `source/sections/00-front-matter.txt`
- printcrime → `source/sections/01-printcrime.txt`
- when-sysadmins-ruled-the-earth → `source/sections/02-when-sysadmins-ruled-the-earth.txt`
- andas-game → `source/sections/03-andas-game.txt`
- i-robot → `source/sections/04-i-robot.txt`
- i-row-boat → `source/sections/05-i-row-boat.txt`
- after-the-siege → `source/sections/06-after-the-siege.txt`
- license → `source/sections/07-license.txt` (not translated)

If the section file is empty, the source is likely truncated or extraction failed. Alert the user and stop.

**Step 4 — Translate**
Write `docs/ja/<slug>.md`. Always use Python `write_bytes(text.encode('utf-8'))`.

Frontmatter for a story:
```yaml
---
title: 'Story Title'
translation_status: draft
---
```

Each story section includes Cory Doctorow's introduction to that story plus the complete
story text — preserve both.

Apply all rules from `TRANSLATION_GUIDE.md` and `CHARACTERS.md`:
- Determine narrator pronoun and voice per story from the source text; do not force one
  pronoun across the collection
- Do not summarize, condense, or omit any content, including the story introduction
- Preserve period computing/gaming/sysadmin slang and cultural references without modernizing
- Include `<small>` attribution footer at bottom
- Do not consult any existing Japanese translation of the story

**Step 5 — Update navigation**
Add entry to the appropriate sidebar group (前書き / 短編 / 情報) in `docs/.vitepress/config.mts`.
Update reading list and translation status in `docs/index.md`.
Use Python `write_bytes(content.encode('utf-8'))` for both files.

**Step 6 — Validate**
```bash
python3 scripts/check_translation_batch.py <target>
python3 scripts/validate_links.py
```
Zero errors required.

**Step 7 — Report (English only)**
Include:
- Files created/modified + byte counts
- Source section used
- Full validation output
- Any deviations, TODOs, or unresolved issues
- Confirmation that no existing Japanese translation was consulted
- PowerShell commit command:
  ```powershell
  git add docs/ja/<slug>.md docs/.vitepress/config.mts docs/index.md
  git commit -m "trans: translate <section> (draft)"
  ```
