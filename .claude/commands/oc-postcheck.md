Review already-translated sections without retranslating or rewriting prose.

**Argument:** section identifier.
Examples: `printcrime` | `i-robot` | `after-the-siege` | `all`

**Instructions:**
1. Read `.claude/skills/oc-postcheck/SKILL.md` for the full procedure.
2. Run `python3 scripts/check_translation_batch.py <target>`.
3. Run `python3 scripts/validate_links.py`.
4. Do **not** edit translated sections unless the user explicitly asks.
5. Report findings in **English**, grouped by severity (must fix / should fix / optional).
