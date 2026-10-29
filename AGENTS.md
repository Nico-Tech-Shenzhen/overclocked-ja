# AGENTS.md — Overclocked Japanese translation

## Start here

1. Read `translation-project.yaml` before project work.
2. Use the shared Codex skills `translation-bootstrap`,
   `translation-translate`, `translation-review`, `translation-rule-update`,
   `translation-rule-audit`, and `translation-finalize` as appropriate.
3. Read the local sources of truth required for the task:
   `TRANSLATION_GUIDE.md`, `CHARACTERS.md`, and `glossary.tsv`. Current
   explicit user instructions take precedence over stored rules.
4. Use the source paths and validators configured in
   `translation-project.yaml`.

Generic translation procedure lives in the shared skills. This file keeps the
Overclocked-specific contract and safety constraints.

## Operational and authorization rules

- Work and report in English. Japanese is required for translated book content
  in `docs/ja/*.md` and Japanese reader-facing pages such as `docs/index.md`.
- Commit messages, branch names, PR titles, and PR descriptions must be in
  English.
- Never commit or push unless the user explicitly authorizes that action.
- Do not restate full rule files in reports. Report deviations, TODOs, errors,
  changed-file metrics, and complete validator output.
- Never add `noindex`, `nofollow`, or other search-engine blocking directives
  to the site.

## Source integrity and scope

- Translate only from section files in `source/sections/` produced by
  `scripts/prepare_sources.py`. The official downloaded files remain in
  `source/original/`; do not re-download them during translation work. Report a
  missing or corrupt source file instead.
- Never consult, search for, quote, or imitate an existing published Japanese
  translation of any story in this collection. This restriction applies with
  particular force to *I, Robot*, *When Sysadmins Ruled the Earth*, and
  *Anda's Game*, for which published Japanese translations are known to exist.
- The project covers only the six-story 2007 collection in this order. Do not
  add stories from *Overclocked: More Stories of the Future Present*.

| Source section | Japanese output |
|---|---|
| `source/sections/00-front-matter.txt` | `docs/ja/front-matter.md` |
| `source/sections/01-printcrime.txt` | `docs/ja/printcrime.md` |
| `source/sections/02-when-sysadmins-ruled-the-earth.txt` | `docs/ja/when-sysadmins-ruled-the-earth.md` |
| `source/sections/03-andas-game.txt` | `docs/ja/andas-game.md` |
| `source/sections/04-i-robot.txt` | `docs/ja/i-robot.md` |
| `source/sections/05-i-row-boat.txt` | `docs/ja/i-row-boat.md` |
| `source/sections/06-after-the-siege.txt` | `docs/ja/after-the-siege.md` |

`source/sections/07-license.txt` contains the complete legal code and is not a
translation unit.

Each story page includes both Cory Doctorow's author introduction and the full
story. Collection-specific introduction voice, narrator decisions, character
voices, terminology, attribution, license wording, title policy, and period
context rules remain in the local guide, character file, and glossary.

## Completion gates

Do not call a section complete unless:

- its configured source section exists and was produced by the source
  preparation script;
- the Japanese was translated from that section rather than memory,
  assumptions, or an existing Japanese translation;
- required introduction, story text, structure, and attribution are present;
- frontmatter `translation_status` is accurate; and
- all applicable configured validators pass with zero errors.

Run the Windows VitePress build when required by the configured workflow. Do
not generate or publish PDF/EPUB unless the local publication policy and an
explicit user instruction authorize it.

## Rule and review boundaries

- A rule-update task may edit only `TRANSLATION_GUIDE.md`, `CHARACTERS.md`,
  `glossary.tsv`, `translation-project.yaml`, and/or `AGENTS.md` as required by
  the classified feedback. It must not retranslate prose unless explicitly
  requested.
- A rule audit must not edit `docs/ja/*.md`.
- Translation review is read-only unless the user explicitly requests a
  separate fix task.
- Do not silently generalize one-off corrections. For a recurring issue that
  may deserve a durable rule, report a Rule Candidate with the problem,
  proposed rule, rationale, expected scope, and possible risks. The human
  translator decides whether to adopt it.

## Claude Code compatibility

Preserve `CLAUDE.md`, `.claude/`, and the existing `oc-*` commands and skills.
They remain the Claude Code interface and need not duplicate the Codex shared
skill implementation. Do not rename, delete, or destructively migrate them.
