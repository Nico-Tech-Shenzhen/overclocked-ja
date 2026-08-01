# Overclocked 日本語訳

Japanese translation project for *Overclocked: Stories of the Future Present* by Cory Doctorow.

- **Repository**: https://github.com/Nico-Tech-Shenzhen/overclocked-ja
- **Site**: https://takasumasakazu.net/overclocked-ja/
- **Translator**: 高須正和 / TAKASU Masakazu (@tks)

## About this project

*Overclocked: Stories of the Future Present* is a 2007 short story collection by Cory
Doctorow, published by Thunder's Mouth Press (a division of Avalon Books). It collects
six stories about technology, freedom, and the near future: Printcrime, When Sysadmins
Ruled the Earth, Anda's Game, I, Robot, I, Row-Boat, and After the Siege.

This project covers the original six-story collection only. It does not include the
later expanded edition, *Overclocked: More Stories of the Future Present*.

The collection is distributed under Creative Commons Attribution-NonCommercial-ShareAlike 2.5.
This Japanese translation uses the same license.

This is a fan translation project based on the CC-licensed English edition, translated
by 高須正和 (TAKASU Masakazu). **This is not an officially published Japanese edition.**

Published Japanese translations of some stories in this collection already exist
elsewhere. This project does not consult, quote, or imitate those translations; it is
produced independently from the official CC-licensed English source.

## License

- **Book-derived content** (translations): CC BY-NC-SA 2.5
- **Scripts and site configuration**: MIT License

See `CONTENT-LICENSE.md` for full details.

## Source

The original English text is distributed free by Cory Doctorow:

- Download page: https://craphound.com/overclocked/download/
- Six stories, each as plain text and HTML (see `source/manifest.json` for exact URLs)

Source files must be placed in `source/original/` before running the source
preparation script. See `source/manifest.json` for checksums and download instructions.

## Repository structure

```
overclocked-ja/
├── CLAUDE.md                    # Claude Code operational rules
├── TRANSLATION_GUIDE.md         # Translation rules and style guide
├── CHARACTERS.md                # Per-story voice guide
├── glossary.tsv                 # Term dictionary (source_term / ja_term / note)
├── CONTENT-LICENSE.md           # License information
├── README.md                    # This file
├── package.json                 # VitePress build config
├── source/
│   ├── original/                # Official source files (TXT + HTML, six stories)
│   ├── sections/                # Extracted sections (output of prepare_sources.py)
│   └── manifest.json            # URLs, checksums, download instructions
├── docs/
│   ├── index.md                 # Japanese site homepage
│   ├── credits.md               # Credits page
│   ├── license.md               # License page
│   ├── ja/                      # Translated story files
│   └── .vitepress/
│       └── config.mts           # VitePress configuration
├── scripts/
│   ├── prepare_sources.py       # Extract common forematter/license and per-story sections
│   ├── validate_sections.py     # Verify all sections exist and are valid
│   └── validate_links.py        # Check internal links in docs/ja/
├── .claude/
│   ├── commands/                # Claude Code slash command wrappers
│   └── skills/                  # Full skill procedure files
└── .github/
    └── workflows/
        └── deploy.yml           # GitHub Pages deployment
```

## Getting started (for translators)

1. Download the six official source files (see `source/manifest.json` for instructions)
2. Run `python scripts/prepare_sources.py` to extract the source into sections
3. Run `python scripts/validate_sections.py` to confirm all sections are present
4. Install dependencies: `npm install`
5. Read `TRANSLATION_GUIDE.md` and `CHARACTERS.md` before translating
6. Use `/oc-translate printcrime` to begin translating the first story

## Getting started (for site build)

```bash
npm install
npm run docs:dev      # local preview
npm run docs:build    # production build
```

## Translation status

No stories translated yet. Repository is in initial setup state.
