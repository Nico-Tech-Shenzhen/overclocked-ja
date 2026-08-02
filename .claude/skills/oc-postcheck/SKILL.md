# Skill: oc-postcheck

Review already-translated sections. Read-only — do not rewrite prose.

## Steps

1. **Read current rules**
   Read `TRANSLATION_GUIDE.md`, `CHARACTERS.md`, and `glossary.tsv` (or the sections
   relevant to the target story, if already read earlier this session and unchanged).
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
   - Per `TRANSLATION_GUIDE.md § Reader orientation for technical and culture-specific
     terms`: no unexplained specialist term left opaque at first use; no explanation
     lagging behind a term's first use without a literary reason; no invented/joking
     name (e.g. a character-coined "law") reading as a real external reference; no
     unclear technical agency or network/UPS topology from carried-over English pronoun
     attachment

4. **Report (English only)**
   Keep it compact: quote only the short excerpt needed to justify each finding, never
   full paragraphs or whole files. Group by file and severity:
   - **Must fix**: errors that violate core rules (omissions, wrong register, broken footer)
   - **Should fix**: style deviations, terminology mismatches
   - **Optional**: minor style improvements

   Do NOT rewrite prose. List issues only.
   If user wants fixes applied, they must request a separate fix task.
