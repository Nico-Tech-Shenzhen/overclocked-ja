# Skill: oc-full-recheck

Revalidate all translated sections against the latest rules. Read-only — do not rewrite.

## Steps

1. **Read current rules**
   Read `CLAUDE.md`, `TRANSLATION_GUIDE.md`, `CHARACTERS.md`, `glossary.tsv` (skip
   re-reading any already loaded earlier this session and unchanged).
   Ignore prior chat history.

2. **Find all translated files**
   List all `.md` files in `docs/ja/`.

3. **Run full validation**
   ```bash
   python3 scripts/check_translation_batch.py all
   python3 scripts/validate_links.py
   ```
   Report full output.

4. **Qualitative review**
   For each translated file, apply the full checklist from `TRANSLATION_GUIDE.md §LLM translation checklist`.
   Note rule violations, pattern inconsistencies, per-story voice inconsistencies, and glossary mismatches.

5. **Report (English only)**
   Keep it compact: grouped summary by file and severity, short excerpts only where
   needed to justify a finding — never full files or full diffs.
   Do NOT rewrite prose. This is a review-only command.
   If the user wants fixes applied, they must request a separate fix task after reviewing this report.
