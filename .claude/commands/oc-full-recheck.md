Revalidate all existing translated Japanese sections against the latest rules.

**The collection has six stories. Do not add stories from the expanded edition.**

**Argument (optional):** `all`, a story name, or a list of story names.
Examples: *(no argument)* | `all` | `printcrime` | `i-robot i-row-boat`

**Instructions:**
1. Read `.claude/skills/oc-full-recheck/SKILL.md` for the full procedure.
2. Read the current `CLAUDE.md`, `TRANSLATION_GUIDE.md`, `CHARACTERS.md`, and `glossary.tsv` — ignore prior chat history.
3. Run `python3 scripts/check_translation_batch.py all` (or the requested range).
4. Run `python3 scripts/validate_links.py`.
5. Perform qualitative review against `TRANSLATION_GUIDE.md` and `CHARACTERS.md`.
6. **Review only.** Do **not** retranslate or edit `docs/ja/*.md` unless the user explicitly requests a separate fix task.
7. Report in **English**, grouped by file and severity.
