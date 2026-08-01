# Skill: oc-postcheck

Review already-translated sections. Read-only — do not rewrite prose.

## Steps

1. **Read current rules**
   Read `TRANSLATION_GUIDE.md`, `CHARACTERS.md`, and `glossary.tsv`.
   Ignore prior chat history — evaluate only against the current rules.

2. **Run validation**
   ```bash
   python3 scripts/check_translation_batch.py <target>
   python3 scripts/validate_links.py
   ```
   Report full output.

3. **Qualitative review**
   For each target file, read `docs/ja/<slug>.md` and check:
   - Narrator pronoun/voice matches what `CHARACTERS.md` records for that specific story
     (voice is not shared across stories)
   - No paragraphs, sentences, or the story's author introduction omitted
   - Technical terms match `glossary.tsv`
   - Period computing/gaming/political references not modernized
   - `<small>` attribution footer present
   - No "公式日本語版", "公認翻訳", or similar official-translation claims anywhere
   - No sign that an existing published Japanese translation was consulted

4. **Report (English only)**
   Group by file and severity:
   - **Must fix**: errors that violate core rules (omissions, wrong register, broken footer)
   - **Should fix**: style deviations, terminology mismatches
   - **Optional**: minor style improvements

   Do NOT rewrite prose. List issues only.
   If user wants fixes applied, they must request a separate fix task.
