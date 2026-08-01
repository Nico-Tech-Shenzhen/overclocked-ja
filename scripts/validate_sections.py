#!/usr/bin/env python3
"""
validate_sections.py — Fail-closed validation of Overclocked source
sections and (informationally) translation status.

Unlike Little Brother (single novel, 29 fixed sections), Overclocked is
six independently-published story files whose repeated forematter/license
blocks were deduplicated by scripts/prepare_sources.py. This script
validates the RESULT of that process.

Checks (each documented inline below):
  - all eight section files exist (00-front-matter, six stories, 07-license)
    — currently seven are expected to exist; "After the Siege" is a KNOWN,
      reported gap until its source is downloaded (see source/manifest.json)
  - all six originals exist in TXT *and* HTML form (missing ones reported)
  - TXT originals' byte sizes and SHA-256 match source/manifest.json
  - section extraction is reproducible: re-running prepare_sources.py in a
    scratch copy produces byte-identical section files
  - every unique paragraph of source content is accounted for (no section
    is empty; no story is truncated relative to its original)
  - forematter/license dedup only happened after equivalence checks passed
    (re-derives forematter/license from each original and compares against
    the checked-in deduplicated section files)
  - translation_status: for each of the six stories (+ front-matter), report
    whether docs/ja/<slug>.md exists and its frontmatter translation_status

Exit code 0 means all HARD checks passed. Warnings (including the expected
"After the Siege" gap) are printed but do not affect the exit code, unless
noted otherwise below.

Usage:
    python3 scripts/validate_sections.py
"""

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent
ORIGINAL_DIR = REPO / "source" / "original"
SECTIONS_DIR = REPO / "source" / "sections"
MANIFEST = REPO / "source" / "manifest.json"
DOCS_JA = REPO / "docs" / "ja"
PREPARE_SCRIPT = REPO / "scripts" / "prepare_sources.py"

FRONT_MATTER_SECTION = "00-front-matter.txt"
LICENSE_SECTION = "07-license.txt"

# order, title, txt basename, html basename, section filename, docs/ja slug
STORIES = [
    (1, "Printcrime",
     "Cory_Doctorow_-_Overclocked_-_Printcrime.txt",
     "Cory_Doctorow_-_Overclocked_-_Printcrime.html",
     "01-printcrime.txt", "printcrime"),
    (2, "When Sysadmins Ruled the Earth",
     "Cory_Doctorow_-_Overclocked_-_When_Sysadmins_Ruled_the_Earth.txt",
     "Cory_Doctorow_-_Overclocked_-_When_Sysadmins_Ruled_the_Earth.html",
     "02-when-sysadmins-ruled-the-earth.txt", "when-sysadmins-ruled-the-earth"),
    (3, "Anda's Game",
     "Cory_Doctorow_-_Overclocked_-_Andas_Game.txt",
     "Cory_Doctorow_-_Overclocked_-_Andas_Game.html",
     "03-andas-game.txt", "andas-game"),
    (4, "I, Robot",
     "Cory_Doctorow_-_Overclocked_-_I_Robot.txt",
     "Cory_Doctorow_-_Overclocked_-_I_Robot.html",
     "04-i-robot.txt", "i-robot"),
    (5, "I, Row-Boat",
     "Cory_Doctorow_-_Overclocked_-_I_Row-Boat.txt",
     "Cory_Doctorow_-_Overclocked_-_I_Row-Boat.html",
     "05-i-row-boat.txt", "i-row-boat"),
    (6, "After the Siege",
     "Cory_Doctorow_-_Overclocked_-_After_the_Siege.txt",
     "Cory_Doctorow_-_Overclocked_-_After_the_Siege.html",
     "06-after-the-siege.txt", "after-the-siege"),
]

EXPECTED_SECTIONS = (
    [FRONT_MATTER_SECTION] + [s[4] for s in STORIES] + [LICENSE_SECTION]
)

STATUS_LEVELS = ["not_started", "pilot", "draft", "reviewed", "complete"]

errors: list[str] = []
warnings: list[str] = []
gaps: list[str] = []  # known, expected incompleteness (e.g. After the Siege)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ── Check 0: originals present (TXT + HTML) ──────────────────────────────

def check_originals_present():
    print("Checking source/original/ ...")
    for order, title, txt, html, section, slug in STORIES:
        txt_path = ORIGINAL_DIR / txt
        html_path = ORIGINAL_DIR / html
        txt_ok = txt_path.exists()
        html_ok = html_path.exists()
        if txt_ok and html_ok:
            print(f"  [OK]      {title}: TXT + HTML present")
        elif not txt_ok and not html_ok:
            gaps.append(f"{title}: neither TXT nor HTML original is present "
                        f"(expected — see source/manifest.json)")
            print(f"  [MISSING] {title}: TXT and HTML both absent")
        else:
            missing_kind = "HTML" if txt_ok else "TXT"
            warnings.append(f"{title}: {missing_kind} original is missing while "
                             f"the other format is present — inconsistent, check manifest")
            print(f"  [PARTIAL] {title}: {'TXT' if txt_ok else 'HTML'} present, "
                  f"{missing_kind} missing")


# ── Check 1: manifest present; byte size / SHA-256 match ─────────────────

def check_manifest():
    print("\nChecking source/manifest.json ...")
    if not MANIFEST.exists():
        errors.append("MANIFEST MISSING: source/manifest.json not found")
        return

    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"MANIFEST PARSE ERROR: {e}")
        return

    entries_by_filename = {e.get("filename"): e for e in manifest.get("files", [])}
    if not entries_by_filename:
        errors.append("MANIFEST: no 'files' entries found")
        return

    for order, title, txt, html, section, slug in STORIES:
        for fname in (txt, html):
            entry = entries_by_filename.get(fname)
            if entry is None:
                warnings.append(f"MANIFEST: no entry for {fname}")
                continue
            path = ORIGINAL_DIR / fname
            if not path.exists():
                # Already reported by check_originals_present(); manifest
                # itself may legitimately record a FAILED/not-retrieved status.
                if entry.get("status"):
                    print(f"  [SKIP]  {fname}: manifest records status "
                          f"{entry['status']!r} — matches local absence")
                continue
            data = path.read_bytes()
            actual_size = len(data)
            actual_sha = sha256_bytes(data)
            expected_size = entry.get("byte_size")
            expected_sha = entry.get("sha256")
            if expected_size is not None and expected_size != actual_size:
                errors.append(
                    f"SIZE MISMATCH: {fname}: manifest={expected_size} actual={actual_size}"
                )
            if expected_sha is not None and expected_sha != actual_sha:
                errors.append(
                    f"CHECKSUM MISMATCH: {fname}\n"
                    f"  manifest : {expected_sha}\n"
                    f"  actual   : {actual_sha}"
                )
            if expected_size is not None and expected_sha is not None:
                print(f"  [OK]    {fname}: size and SHA-256 match manifest")


# ── Check 2: all section files exist ──────────────────────────────────────

def check_sections_exist():
    print("\nChecking source/sections/ ...")
    if not SECTIONS_DIR.exists():
        errors.append(f"SECTIONS DIRECTORY MISSING: {SECTIONS_DIR}. "
                       f"Run: python scripts/prepare_sources.py")
        return

    for fname in EXPECTED_SECTIONS:
        p = SECTIONS_DIR / fname
        if p.exists():
            print(f"  [OK]      {fname} ({p.stat().st_size:,} bytes)")
        else:
            # Only treat as a hard error if the corresponding original TXT
            # is actually present — otherwise this is the known/expected gap.
            story = next((s for s in STORIES if s[4] == fname), None)
            if story and not (ORIGINAL_DIR / story[2]).exists():
                gaps.append(f"{fname} not produced — source original for "
                            f"'{story[1]}' is not yet downloaded")
                print(f"  [GAP]     {fname} — expected, source not yet available")
            else:
                errors.append(f"MISSING SECTION: {fname} (source original IS present — "
                               f"run scripts/prepare_sources.py)")
                print(f"  [MISSING] {fname}")


# ── Check 3: no section is empty; no story truncated ──────────────────────

def check_non_empty_and_untruncated():
    print("\nChecking section content (non-empty, untruncated) ...")
    for fname in EXPECTED_SECTIONS:
        p = SECTIONS_DIR / fname
        if not p.exists():
            continue
        size = p.stat().st_size
        if size == 0:
            errors.append(f"EMPTY SECTION: {fname}")
            continue
        if fname in (FRONT_MATTER_SECTION, LICENSE_SECTION):
            continue
        story = next((s for s in STORIES if s[4] == fname), None)
        if not story:
            continue
        _, title, txt, _html, _section, _slug = story
        orig_path = ORIGINAL_DIR / txt
        if not orig_path.exists():
            continue
        orig_size = orig_path.stat().st_size
        # A sane lower bound: the story's own section must not be smaller
        # than a tiny fraction of the original file (which also contains
        # the now-removed forematter/license — so exact equality isn't
        # expected, but a story section can never legitimately be tiny
        # relative to its source).
        if size < orig_size * 0.20:
            errors.append(
                f"POSSIBLE TRUNCATION: {fname} is {size:,} bytes but its source "
                f"original ({txt}) is {orig_size:,} bytes — story content looks "
                f"disproportionately small."
            )
        else:
            print(f"  [OK]      {fname}: {size:,} bytes (source {orig_size:,} bytes)")


# ── Check 4: dedup only happened after equivalence — re-derive and compare ─

INTRO_RE = re.compile(r"(?m)^Introduction to ")
LICENSE_RE = re.compile(r"(?m)^Creative Commons License Deed\s*$")


def normalize_ws(text: str) -> str:
    lines = text.split("\n")
    lines = [ln.rstrip() for ln in lines]
    normalized = "\n".join(lines)
    return normalized.rstrip("\n") + "\n"


def check_dedup_equivalence_and_conservation():
    """Re-derive forematter/story/license from each present original and
    confirm: (a) every original's forematter matches the checked-in
    00-front-matter.txt exactly; (b) every original's license matches
    07-license.txt after whitespace normalization; (c) every original's
    story block matches its own section file exactly. This proves the
    committed section files are a faithful, lossless, order-preserving
    decomposition of the originals — i.e. dedup happened only after (and
    consistent with) the equivalence checks in prepare_sources.py."""
    print("\nChecking dedup conservation (each original reconstructs from sections) ...")

    fm_section_path = SECTIONS_DIR / FRONT_MATTER_SECTION
    lic_section_path = SECTIONS_DIR / LICENSE_SECTION
    if not fm_section_path.exists() or not lic_section_path.exists():
        warnings.append("Skipping dedup-conservation check: front-matter or "
                         "license section file is missing")
        return

    canonical_forematter = fm_section_path.read_bytes().decode("utf-8")
    canonical_license = lic_section_path.read_bytes().decode("utf-8")

    for order, title, txt, html, section, slug in STORIES:
        orig_path = ORIGINAL_DIR / txt
        section_path = SECTIONS_DIR / section
        if not orig_path.exists() or not section_path.exists():
            continue

        text = orig_path.read_bytes().decode("utf-8-sig")
        intro_matches = list(INTRO_RE.finditer(text))
        license_matches = list(LICENSE_RE.finditer(text))
        if not intro_matches or not license_matches:
            errors.append(f"{txt}: delimiter(s) not found during re-validation")
            continue

        intro_start = intro_matches[0].start()
        license_start = license_matches[0].start()
        forematter = text[:intro_start]
        story_block = text[intro_start:license_start]
        license_block = text[license_start:]

        if forematter != canonical_forematter:
            errors.append(f"{txt}: re-derived forematter does not match "
                          f"{FRONT_MATTER_SECTION} — dedup may be stale, "
                          f"re-run scripts/prepare_sources.py")

        if normalize_ws(license_block) != canonical_license:
            errors.append(f"{txt}: re-derived license (normalized) does not match "
                          f"{LICENSE_SECTION} — dedup may be stale, "
                          f"re-run scripts/prepare_sources.py")

        section_text = section_path.read_bytes().decode("utf-8")
        if section_text != story_block:
            errors.append(f"{section}: does not match the story block re-derived "
                          f"from {txt} — section may be stale or was hand-edited; "
                          f"re-run scripts/prepare_sources.py")
        else:
            print(f"  [OK]      {section}: matches re-derived story block from {txt}")


# ── Check 5: reproducibility — re-run prepare_sources.py in a scratch copy ─

def check_reproducibility():
    print("\nChecking section extraction is reproducible ...")
    if not PREPARE_SCRIPT.exists():
        warnings.append("Skipping reproducibility check: scripts/prepare_sources.py not found")
        return

    with tempfile.TemporaryDirectory(prefix="oc-prepare-repro-") as tmp:
        tmp_path = pathlib.Path(tmp)
        scratch_repo = tmp_path / "repo"
        (scratch_repo / "source" / "original").mkdir(parents=True)
        (scratch_repo / "scripts").mkdir(parents=True)
        shutil.copy(PREPARE_SCRIPT, scratch_repo / "scripts" / "prepare_sources.py")
        for f in ORIGINAL_DIR.glob("*.txt"):
            shutil.copy(f, scratch_repo / "source" / "original" / f.name)

        proc = subprocess.run(
            [sys.executable, str(scratch_repo / "scripts" / "prepare_sources.py")],
            cwd=scratch_repo,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            errors.append(
                "REPRODUCIBILITY: prepare_sources.py failed when re-run in a "
                f"scratch copy (exit {proc.returncode}):\n{proc.stderr[-2000:]}"
            )
            return

        scratch_sections = scratch_repo / "source" / "sections"
        mismatches = []
        for fname in EXPECTED_SECTIONS:
            real = SECTIONS_DIR / fname
            scratch = scratch_sections / fname
            if not real.exists() and not scratch.exists():
                continue
            if real.exists() != scratch.exists():
                mismatches.append(f"{fname}: existence differs (committed={real.exists()}, "
                                  f"reproduced={scratch.exists()})")
                continue
            if real.read_bytes() != scratch.read_bytes():
                mismatches.append(f"{fname}: byte content differs from a fresh re-run")

        if mismatches:
            errors.append("REPRODUCIBILITY: re-running prepare_sources.py does not "
                          "reproduce the committed section files:\n  " +
                          "\n  ".join(mismatches))
        else:
            print(f"  [OK]      re-running prepare_sources.py reproduces all "
                  f"{len(EXPECTED_SECTIONS)} expected section files byte-for-byte")


# ── Check 6: UTF-8 validity ────────────────────────────────────────────────

def check_utf8():
    print("\nChecking UTF-8 validity of section files ...")
    for fname in EXPECTED_SECTIONS:
        p = SECTIONS_DIR / fname
        if not p.exists() or p.stat().st_size == 0:
            continue
        try:
            p.read_bytes().decode("utf-8")
        except UnicodeDecodeError as e:
            errors.append(f"UTF-8 ERROR in {fname}: {e}")


# ── Check 7 (informational): translation_status per story ─────────────────

def read_frontmatter_status(lines: list[str]):
    in_fm = False
    for i, line in enumerate(lines[:30]):
        if i == 0 and line.strip() == "---":
            in_fm = True
            continue
        if in_fm and line.strip() == "---":
            break
        if in_fm:
            m = re.match(r"translation_status:\s*(\S+)", line)
            if m:
                return m.group(1).strip().strip('"\'')
    return None


def check_translation_status():
    print("\nTranslation status (docs/ja/) ...")
    targets = [("front-matter", "Front matter")] + [(s[5], s[1]) for s in STORIES]
    for slug, title in targets:
        path = DOCS_JA / f"{slug}.md"
        if not path.exists():
            print(f"  [NONE]    {title:35s} docs/ja/{slug}.md not found")
            continue
        try:
            text = path.read_bytes().decode("utf-8")
        except UnicodeDecodeError as e:
            warnings.append(f"docs/ja/{slug}.md: UTF-8 decode error: {e}")
            continue
        status = read_frontmatter_status(text.splitlines())
        if status is None:
            warnings.append(f"docs/ja/{slug}.md: no translation_status field in frontmatter")
            print(f"  [??]      {title:35s} no translation_status field")
        elif status not in STATUS_LEVELS:
            warnings.append(f"docs/ja/{slug}.md: unknown translation_status {status!r}")
            print(f"  [??]      {title:35s} unknown status: {status!r}")
        else:
            print(f"  [{status:8s}] {title:35s} docs/ja/{slug}.md")


# ── Main ────────────────────────────────────────────────────────────────

def main():
    print(f"Validating Overclocked source sections\n")

    check_originals_present()
    check_manifest()
    check_sections_exist()
    check_non_empty_and_untruncated()
    check_dedup_equivalence_and_conservation()
    check_reproducibility()
    check_utf8()
    check_translation_status()

    if gaps:
        print("\nKNOWN GAPS (expected, non-fatal):")
        for g in gaps:
            print(f"  ○  {g}")

    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print(f"  ⚠  {w}")

    if errors:
        print("\nERRORS:")
        for e in errors:
            print(f"  ✗  {e}")
        print(f"\n{len(errors)} error(s) — validation FAILED.")
        sys.exit(1)

    print("\n✓ All hard checks passed with zero errors "
          f"({len(gaps)} known gap(s), {len(warnings)} warning(s)).")


if __name__ == "__main__":
    main()
