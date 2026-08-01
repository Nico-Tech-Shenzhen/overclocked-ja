# AGENTS.md — Overclocked 日本語訳

## Operational rules

1. **Always read `TRANSLATION_GUIDE.md` before any translation work.**
2. **Always consult `glossary.tsv` before translating technical or recurring terms.**
3. **Work and report in English** to reduce token usage. Japanese is required only for
   translated book content and public-facing Japanese pages (`docs/ja/`, `docs/index.md`).
   See **§ Operational language** below for the full rule.
4. **Never commit or push** to any remote unless explicitly instructed by the user.
5. **Do not call a section complete** unless all of the following are done:
   - Source section file exists in `source/sections/` and was produced by `scripts/prepare_sources.py`
   - Translation written from the section source text (not from memory, assumptions, or any
     existing published Japanese translation)
   - `python scripts/validate_sections.py` passes with zero errors
   - Frontmatter field `translation_status` is accurate
6. **Do not re-state the full guide in reports.** Only report deviations, TODOs, errors,
   and quantitative results (word counts, validation output).
7. **Source files are in `source/original/`.** Never attempt to re-download them from the
   internet during a translation session. If a file is missing or corrupt, alert the user.
8. **`/oc-rule-update` edits only `TRANSLATION_GUIDE.md`, `CHARACTERS.md`, and/or `glossary.tsv`.**
   It must not edit translated section files or retranslate content unless explicitly instructed.
9. **`/oc-rule-audit` edits only `TRANSLATION_GUIDE.md`, `CHARACTERS.md`, and/or `glossary.tsv`.**
   It must not edit translated section files or retranslate content.
10. **`/oc-postcheck` and `/oc-full-recheck` are review-only.** They must not rewrite translated
    prose unless the user explicitly requests a separate fix task.
11. **Never consult, search for, quote, or imitate any existing published Japanese translation**
    of any story in this collection, even as a comparison or review aid. This applies with
    special force to *I, Robot*, *When Sysadmins Ruled the Earth*, and *Anda's Game*, for which
    published Japanese translations are known to exist.

## Operational language

Use **English** for all workflow and development operations.

**Always English:**
- Codex reports, progress summaries, and explanations of changed files
- Validation and build result summaries
- Suggested commit messages and actual git commit messages
- Branch names, PR titles, and PR descriptions
- TODO comments that are not reader-facing
- Internal notes about source sections, validation, and build results

**Always Japanese:**
- Translated book content (`docs/ja/*.md`)
- Japanese reader-facing site text (homepage, credits, nav labels)
- Japanese headings and body text inside translated pages
- Japanese examples that intentionally belong in the translation

**Commit messages must be in English.**

Good:
```
trans: add Printcrime Japanese translation (draft)
fix: standardize narrator pronoun in i-robot
guide: update Anda's Game voice rules
docs: update site index links
```

Bad (do not use Japanese in commit messages):
```
プリントクライムの日本語訳を追加
アンダの語りを修正
```

## Book structure

*Overclocked: Stories of the Future Present* (2007) collects six short stories. Each
official source file repeats the same collection forematter and the same Creative
Commons license deed around a story-specific author introduction and story text.
Translate in order, one section at a time.

| File | Section |
|------|---------|
| `source/sections/00-front-matter.txt` | Common collection forematter (READ THIS FIRST / license notice) |
| `source/sections/01-printcrime.txt` | Printcrime — author introduction + story |
| `source/sections/02-when-sysadmins-ruled-the-earth.txt` | When Sysadmins Ruled the Earth — author introduction + story |
| `source/sections/03-andas-game.txt` | Anda's Game — author introduction + story |
| `source/sections/04-i-robot.txt` | I, Robot — author introduction + story |
| `source/sections/05-i-row-boat.txt` | I, Row-Boat — author introduction + story |
| `source/sections/06-after-the-siege.txt` | After the Siege — author introduction + story |
| `source/sections/07-license.txt` | Complete Creative Commons legal code (not translated) |

**There are six stories, in this order. Do not add stories from the later expanded
edition "Overclocked: More Stories of the Future Present."**
Each story maps to `docs/ja/<slug>.md` (e.g. `docs/ja/printcrime.md`,
`docs/ja/when-sysadmins-ruled-the-earth.md`). The forematter maps to
`docs/ja/front-matter.md`.

## Standard section translation workflow

Use this sequence for every section. Vary only if the user specifies otherwise.

**Step 1 — Verify repo state**
```
cd D:\translate\overclocked-ja && git status && git log --oneline -3
```
Confirm clean working tree and correct HEAD before touching any file.

**Step 2 — Read project files**
Read in this order (required before any translation):
1. `TRANSLATION_GUIDE.md` — rules, style, checklist
2. `CHARACTERS.md` — per-story voice notes and name conventions
3. `glossary.tsv` — term dictionary
4. `docs/.vitepress/config.mts` — sidebar (to see existing entries)

**Step 3 — Read the source section**
```
source/sections/NN-<name>.txt
```
Translate **only from the section source file**, never from memory and never from any
existing published Japanese translation.

**Step 4 — Translate**
Write `docs/ja/<slug>.md`:
- Frontmatter: `title`, `translation_status: draft`
- Content translated per `TRANSLATION_GUIDE.md` and `CHARACTERS.md`
- Preserve the story's author introduction as well as the story itself
- `<small>` attribution footer at the bottom of every page
- Always write Japanese files with `path.write_bytes(text.encode('utf-8'))` — never the Edit tool

**Step 5 — Update navigation**
Add the new page to the appropriate sidebar group (前書き / 短編 / 情報) in
`docs/.vitepress/config.mts` and to the reading list in `docs/index.md`.
Write both with `write_bytes(content.encode('utf-8'))`.

**Step 6 — Validate**
```
python scripts/validate_sections.py
python scripts/validate_links.py
```
Zero errors required before marking a section complete.
Run `npm run docs:build` on Windows to check the VitePress build.

**Step 7 — Report**
Report in English only. Include:
- Files changed + line/byte counts
- Source section used
- validate_sections.py and validate_links.py output (full)
- Any deviations from TRANSLATION_GUIDE.md, TODOs, or unresolved issues
- Confirmation that no existing Japanese translation was consulted
- PowerShell commit command (do not commit yourself):
  ```powershell
  git add docs/ja/<slug>.md docs/.vitepress/config.mts docs/index.md
  git commit -m "trans: translate <story> — Story Title (draft)"
  ```

## Codex commands and skills

Slash commands are registered as thin wrappers in `.Codex/commands/*.md`.
Each wrapper delegates to the matching `.Codex/skills/oc-*/SKILL.md` for the full procedure.

| Command | Purpose |
|---------|---------|
| `/oc-bootstrap` | Verify setup: source files, sections, scripts, VitePress build |
| `/oc-translate <section>` | Translate a section end-to-end |
| `/oc-postcheck <section>` | Review a translated section without rewriting |
| `/oc-full-recheck` | Revalidate all translated sections against latest rules |
| `/oc-rule-update <description>` | Incorporate new feedback and update TRANSLATION_GUIDE.md / CHARACTERS.md / glossary.tsv |
| `/oc-rule-audit [all\|terminology\|voice]` | Audit, consolidate, and de-conflict translation rules without editing translated prose |

**`/oc-rule-update` is rule/glossary-only.** Incorporates new user feedback and performs a
focused audit of the rules it touches. It must not edit translated section files or retranslate.  
**`/oc-rule-audit` is rule/glossary-only.** Performs periodic project-wide rule maintenance
without requiring new feedback. Default scope is `all`. It must not edit `docs/ja/*.md`.  
**Both skills confirm** `No docs/ja/*.md files were edited` at the end of every run.  
**`/oc-postcheck` and `/oc-full-recheck` are review-only.** They must not rewrite prose.

### Rule Proposal Policy

If you identify a recurring translation issue that may be worth generalizing, do not silently modify the translation guide, character guide, or glossary. Propose it as a **Rule Candidate** using:

- **Problem:** What recurring issue was observed?
- **Proposed Rule:** The rule in concise, reusable language.
- **Rationale:** Why should this become a persistent rule?
- **Expected Scope:** Where should this rule apply?
- **Possible Risks:** Where might it overgeneralize, conflict with existing rules, or require exceptions?

Propose candidates only for issues likely to recur. Local wording corrections, isolated mistranslations, and story-specific decisions should remain local fixes. Keep the number of candidates small and prioritize only high-value reusable rules.

The human translator decides whether to adopt, revise, or reject each candidate. Never modify `TRANSLATION_GUIDE.md`, `CHARACTERS.md`, or `glossary.tsv` without explicit approval.

### Validation harness

```bash
python scripts/prepare_sources.py           # (re-)extract source into sections
python scripts/validate_sections.py         # confirm all sections present + checksums
python scripts/validate_links.py            # check internal links in docs/ja/
```

`npm run docs:build` must be run on Windows (cannot run in Linux sandbox).

## Potential future hooks

- **PreToolUse hook**: block `git push` from Codex.
- **Stop hook**: suggest running `/oc-postcheck` or `/oc-full-recheck` after a
  translation session completes.

## Imported Claude Cowork project instructions
