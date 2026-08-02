# Skill: oc-review-introduction

Focused voice review and revision of Cory Doctorow's author introduction for one story.
Edits only the introduction — never the story body — unless the user explicitly asks
for more.

## Steps

1. **Read minimum required context**
   - `TRANSLATION_GUIDE.md` § "Cory Doctorow's author introductions" (the durable rule
     for this review; skip the rest of the guide if already read this session and
     unchanged)
   - The story's source section file in `source/sections/`
   - The current `docs/ja/<slug>.md`
   - Only the `glossary.tsv` entries relevant to terms actually appearing in the
     introduction

2. **Identify the introduction boundary from the verified source**
   Do not guess from approximate line numbers. Each source section file contains the
   collection forematter, Doctorow's introduction to that specific story, then the
   story text. Locate the exact point in the source where the introduction ends and the
   story narrative begins (e.g. a scene-setting opening line, a change from Doctorow's
   own voice to the story's narrator). Confirm the same boundary in the existing
   `docs/ja/<slug>.md`.

3. **Paragraph-by-paragraph comparison**
   Map each English source paragraph of the introduction to its current Japanese
   paragraph. For each pair, check for:
   - English clause order carried over into Japanese
   - Stacked/nested relative clauses
   - Bureaucratic nominalization or report-like phrasing (e.g. 「〜との見解を示した」
     「〜であると感じた」「〜に対する統制力」「〜ということを意味する」)
   - Sentence boundaries that exist only because the English sentence boundary does
   - Loss of sarcasm, exaggeration, repetition, short punchy sentences, or metaphor
     setup/landing

4. **Rebuild flagged paragraphs**
   Translate independently from the English source under the current rule — do not
   mechanically apply a previously suggested rewrite, and never consult any existing
   published Japanese translation of the story. Preserve:
   - all source information and paragraph order
   - technical accuracy and named things (products, coined terms, proper nouns)
   - rhetorical structure: irony, exaggeration, deliberate repetition, sudden short
     sentences, metaphor setup and landing, delayed judgments/punch lines
   Do not make the Japanese calmer, more neutral, more polite, or more formal than the
   English.

5. **Scope discipline**
   Edit only the introduction paragraphs. Leave the story body, frontmatter, and
   `<small>` attribution footer untouched unless the user explicitly instructs
   otherwise. Write the file with `path.write_bytes(text.encode('utf-8'))`, never the
   Edit tool.

6. **Validate**
   ```bash
   python3 scripts/check_translation_batch.py <slug>
   ```
   Confirm zero errors. (Full-collection link/build validation is run once after all
   target stories are done, not per-story — see the calling workflow.)

7. **Report (English only)**
   Compact report, no pasted full prose (short representative excerpts only):
   - Introduction boundary used (brief description, not full text)
   - Number of paragraphs revised vs. left unchanged, with a one-line reason each for
     revised ones (e.g. "stacked relative clause → split into two sentences")
   - Any technical terms or coined phrases handled specially
   - Validation output
   - Confirmation that no existing published Japanese translation was consulted
   - Confirmation that only the introduction was edited (story body untouched)
