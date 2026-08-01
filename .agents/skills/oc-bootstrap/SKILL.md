# Skill: oc-bootstrap

Verify the Overclocked translation repository is correctly set up.

## Steps

1. **Check project files exist**
   Confirm these files are present. Report any missing:
   - `CLAUDE.md`
   - `TRANSLATION_GUIDE.md`
   - `CHARACTERS.md`
   - `glossary.tsv`
   - `CONTENT-LICENSE.md`
   - `source/manifest.json`
   - `scripts/prepare_sources.py`
   - `scripts/validate_sections.py`
   - `scripts/validate_links.py`
   - `scripts/check_translation_batch.py`
   - `docs/.vitepress/config.mts`
   - `.github/workflows/deploy.yml`
   - `package.json`

2. **Check source files**
   - Confirm all six official story TXT files exist in `source/original/`:
     Printcrime, When Sysadmins Ruled the Earth, Anda's Game, I Robot, I Row-Boat, After the Siege.
   - Confirm the matching six HTML files also exist in `source/original/`.
   - Report file sizes for all twelve files. Warn if any file looks truncated relative to `source/manifest.json`.
   - Check `source/manifest.json` for recorded SHA-256 hashes and byte sizes; flag any mismatch or `partial_download: true` entry.

3. **Check sections**
   - If `source/sections/` is empty or missing, run:
     ```bash
     python3 scripts/prepare_sources.py
     ```
   - Run:
     ```bash
     python3 scripts/validate_sections.py
     ```
   - Confirm all eight section files exist:
     `00-front-matter.txt`, `01-printcrime.txt`, `02-when-sysadmins-ruled-the-earth.txt`,
     `03-andas-game.txt`, `04-i-robot.txt`, `05-i-row-boat.txt`, `06-after-the-siege.txt`, `07-license.txt`.
   - Report full output.

4. **Check links**
   ```bash
   python3 scripts/validate_links.py
   ```
   Report full output.

5. **Report**
   - List of project files: present / missing
   - Source file status: size, hash-mismatch warning if applicable
   - prepare_sources.py output (if run)
   - validate_sections.py output
   - validate_links.py output
   - Suggested next step (e.g. download missing originals, run `/oc-translate printcrime`)
