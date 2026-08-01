Translate a section of *Overclocked: Stories of the Future Present* into Japanese.

**Argument:** section identifier passed after the command name.
Examples: `front-matter` | `printcrime` | `when-sysadmins-ruled-the-earth` | `andas-game` | `i-robot` | `i-row-boat` | `after-the-siege` | `license`

**Six stories only. Do not add stories from the expanded "More Stories of the Future Present" edition.**

**Instructions:**
1. Read `.claude/skills/oc-translate/SKILL.md` for the full procedure.
2. Follow `CLAUDE.md`, `TRANSLATION_GUIDE.md`, `CHARACTERS.md`, and `glossary.tsv`.
3. Use the standard section translation workflow in `CLAUDE.md`.
4. Use **English** for all reports, logs, TODOs, and commit messages.
5. Use **Japanese** only for translated reader-facing content in `docs/ja/`.
6. Never commit or push. Never consult any existing published Japanese translation.
7. Run `python scripts/check_translation_batch.py <target>` after translating.
