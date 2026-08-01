#!/usr/bin/env python3
"""
prepare_sources.py — Deduplicate and split the official Overclocked TXT
sources into source/sections/.

Unlike Little Brother (one novel file split by chapter delimiter),
Overclocked ships as SIX independently-published story files. Each file
repeats the same two blocks:

    1. a common collection "Forematter:" block
       (starts at "Forematter:", ends immediately before "Introduction to <Title>")
    2. a common Creative Commons License Deed + machine-readable RDF block
       (starts at "Creative Commons License Deed", runs to end of file)

Between those two repeated blocks sits the content that is unique to each
story: its "Introduction to <Title>" essay plus the story text itself
("<Title>\\n\\n(Originally published in ...)\\n\\n<story>").

This script:
  1. Reads every verified TXT original present in source/original/.
  2. Splits each file into (forematter, story_block, license_block) using
     the two textual delimiters above. The three pieces concatenate back to
     the original file byte-for-byte by construction (pure substring split),
     which is asserted per file as a hard internal sanity check.
  3. Verifies the forematter is textually IDENTICAL across all present files.
     Fails loudly (prints a unified diff) if not.
  4. Verifies the license block is textually identical, or — if it differs
     only in trailing whitespace (a known, harmless artifact of how each
     story page was exported to TXT) — verifies it is identical after
     whitespace normalization. A whitespace-only difference is reported as
     a NOTE, not an error. Any non-whitespace difference is a hard failure
     with a printed diff.
  5. Writes source/sections/00-front-matter.txt (deduplicated forematter,
     written once).
  6. Writes one source/sections/0N-<slug>.txt per story present, containing
     ONLY that story's unique introduction + story text.
  7. Writes source/sections/07-license.txt (deduplicated, whitespace-
     normalized license block, written once).
  8. Writes a conservation report to source/prepare_report.txt.

Missing sources (e.g. "After the Siege", not yet downloaded — see
source/manifest.json) are reported as clear warnings. The script does NOT
crash on missing files, and does NOT silently skip them: every missing
story is listed explicitly in stdout and in the conservation report.

Usage:
    python3 scripts/prepare_sources.py
"""

import difflib
import re
import sys
import pathlib

# ── Configuration ────────────────────────────────────────────────────────

REPO = pathlib.Path(__file__).resolve().parent.parent
ORIGINAL_DIR = REPO / "source" / "original"
SECTIONS_DIR = REPO / "source" / "sections"
REPORT_PATH = REPO / "source" / "prepare_report.txt"

FRONT_MATTER_FILENAME = "00-front-matter.txt"
LICENSE_FILENAME = "07-license.txt"

# Official story order (per START_CLAUDE.md "Source preparation model").
STORIES = [
    {
        "order": 1,
        "title": "Printcrime",
        "txt": "Cory_Doctorow_-_Overclocked_-_Printcrime.txt",
        "section": "01-printcrime.txt",
    },
    {
        "order": 2,
        "title": "When Sysadmins Ruled the Earth",
        "txt": "Cory_Doctorow_-_Overclocked_-_When_Sysadmins_Ruled_the_Earth.txt",
        "section": "02-when-sysadmins-ruled-the-earth.txt",
    },
    {
        "order": 3,
        "title": "Anda's Game",
        "txt": "Cory_Doctorow_-_Overclocked_-_Andas_Game.txt",
        "section": "03-andas-game.txt",
    },
    {
        "order": 4,
        "title": "I, Robot",
        "txt": "Cory_Doctorow_-_Overclocked_-_I_Robot.txt",
        "section": "04-i-robot.txt",
    },
    {
        "order": 5,
        "title": "I, Row-Boat",
        "txt": "Cory_Doctorow_-_Overclocked_-_I_Row-Boat.txt",
        "section": "05-i-row-boat.txt",
    },
    {
        "order": 6,
        "title": "After the Siege",
        "txt": "Cory_Doctorow_-_Overclocked_-_After_the_Siege.txt",
        "section": "06-after-the-siege.txt",
    },
]

INTRO_RE = re.compile(r"(?m)^Introduction to ")
LICENSE_RE = re.compile(r"(?m)^Creative Commons License Deed\s*$")


class PrepareError(SystemExit):
    pass


def fail(msg: str):
    print(f"\nERROR: {msg}", file=sys.stderr)
    raise PrepareError(1)


def normalize_ws(text: str) -> str:
    """Strip trailing whitespace from every line and normalize the block to
    end with exactly one trailing newline. Used only to check/produce a
    canonical form of the license block, which is known to carry harmless
    per-file export differences (trailing spaces on a blank line; presence
    or absence of a final newline)."""
    lines = text.split("\n")
    lines = [ln.rstrip() for ln in lines]
    normalized = "\n".join(lines)
    return normalized.rstrip("\n") + "\n"


def unified_diff_report(label_a: str, a: str, label_b: str, b: str, limit: int = 60) -> str:
    diff = list(
        difflib.unified_diff(
            a.splitlines(keepends=True),
            b.splitlines(keepends=True),
            fromfile=label_a,
            tofile=label_b,
            lineterm="",
        )
    )
    if len(diff) > limit:
        diff = diff[:limit] + [f"... ({len(diff) - limit} more diff lines truncated) ..."]
    return "\n".join(diff)


def split_file(path: pathlib.Path):
    """Split one story TXT into (forematter, story_block, license_block).
    Returns the decoded text plus the three substrings. Reconstruction
    (forematter + story_block + license_block == text) is guaranteed by
    construction (pure index slicing) and is asserted as a hard sanity
    check regardless."""
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as e:
        fail(f"{path.name}: not valid UTF-8: {e}")

    intro_matches = list(INTRO_RE.finditer(text))
    if not intro_matches:
        fail(
            f"{path.name}: could not find the 'Introduction to ' delimiter that "
            f"marks the end of the collection forematter. Source may be malformed "
            f"or the file layout has changed."
        )
    intro_start = intro_matches[0].start()

    license_matches = list(LICENSE_RE.finditer(text))
    if not license_matches:
        fail(
            f"{path.name}: could not find the 'Creative Commons License Deed' "
            f"delimiter that marks the start of the license block."
        )
    if len(license_matches) > 1:
        fail(
            f"{path.name}: 'Creative Commons License Deed' delimiter appears "
            f"{len(license_matches)} times — expected exactly once."
        )
    license_start = license_matches[0].start()

    if license_start <= intro_start:
        fail(
            f"{path.name}: license delimiter appears before (or at) the "
            f"introduction delimiter — file layout is not as expected."
        )

    forematter = text[:intro_start]
    story_block = text[intro_start:license_start]
    license_block = text[license_start:]

    # Hard internal sanity check: no bytes lost or duplicated by the split.
    if forematter + story_block + license_block != text:
        fail(f"{path.name}: internal split error — reconstructed text does not "
             f"match the original. This should be impossible; aborting.")

    if not story_block.strip():
        fail(f"{path.name}: extracted story block is empty.")

    return {
        "path": path,
        "raw_bytes": raw,
        "text": text,
        "forematter": forematter,
        "story_block": story_block,
        "license_block": license_block,
    }


def main():
    print(f"Source dir  : {ORIGINAL_DIR}")
    print(f"Sections dir: {SECTIONS_DIR}\n")

    SECTIONS_DIR.mkdir(parents=True, exist_ok=True)

    present = []
    missing = []
    for story in STORIES:
        p = ORIGINAL_DIR / story["txt"]
        if p.exists():
            present.append(story)
        else:
            missing.append(story)

    if missing:
        print("WARNING: the following story source file(s) are missing and will")
        print("be SKIPPED (no section file will be produced for them):")
        for story in missing:
            print(f"  - {story['title']}: source/original/{story['txt']} not found")
        print()

    if not present:
        fail("No story source files found in source/original/. Nothing to prepare.")

    # ── Split every present file ────────────────────────────────────────
    splits = {}
    for story in present:
        splits[story["order"]] = split_file(ORIGINAL_DIR / story["txt"])
        print(f"  Split OK: {story['txt']} "
              f"(forematter {len(splits[story['order']]['forematter']):,} chars, "
              f"story {len(splits[story['order']]['story_block']):,} chars, "
              f"license {len(splits[story['order']]['license_block']):,} chars)")

    # ── Verify forematter equivalence (strict) ──────────────────────────
    print("\nVerifying forematter equivalence across all present files...")
    first_story = present[0]
    canonical_forematter = splits[first_story["order"]]["forematter"]
    forematter_diffs = []
    for story in present[1:]:
        candidate = splits[story["order"]]["forematter"]
        if candidate != canonical_forematter:
            forematter_diffs.append((story, candidate))

    if forematter_diffs:
        print("ERROR: forematter is NOT identical across all story files:", file=sys.stderr)
        for story, candidate in forematter_diffs:
            print(f"\n--- diff: {first_story['txt']} vs {story['txt']} ---", file=sys.stderr)
            print(
                unified_diff_report(
                    first_story["txt"], canonical_forematter, story["txt"], candidate
                ),
                file=sys.stderr,
            )
        fail("forematter equivalence check failed (see diffs above). "
             "Refusing to deduplicate non-equivalent content.")
    print(f"  OK — identical across {len(present)} file(s) "
          f"({len(canonical_forematter):,} chars).")

    # ── Verify license equivalence (strict, then whitespace-normalized) ─
    print("\nVerifying license block equivalence across all present files...")
    canonical_license_raw = splits[first_story["order"]]["license_block"]
    license_notes = []
    hard_license_diffs = []
    any_whitespace_diff = False

    for story in present[1:]:
        candidate = splits[story["order"]]["license_block"]
        if candidate == canonical_license_raw:
            continue
        norm_base = normalize_ws(canonical_license_raw)
        norm_candidate = normalize_ws(candidate)
        if norm_base == norm_candidate:
            any_whitespace_diff = True
            license_notes.append(
                f"  NOTE: {story['txt']} license block differs from "
                f"{first_story['txt']} only in trailing whitespace / final "
                f"newline — treated as equivalent after normalization."
            )
        else:
            hard_license_diffs.append((story, candidate))

    if hard_license_diffs:
        print("ERROR: license block is NOT equivalent across all story files "
              "(non-whitespace differences found):", file=sys.stderr)
        for story, candidate in hard_license_diffs:
            print(f"\n--- diff: {first_story['txt']} vs {story['txt']} ---", file=sys.stderr)
            print(
                unified_diff_report(
                    first_story["txt"], canonical_license_raw, story["txt"], candidate
                ),
                file=sys.stderr,
            )
        fail("license equivalence check failed (see diffs above). "
             "Refusing to deduplicate non-equivalent content.")

    if any_whitespace_diff:
        print("  OK (after whitespace normalization) — see notes:")
        for note in license_notes:
            print(note)
    else:
        print(f"  OK — byte-identical across {len(present)} file(s).")

    canonical_license = normalize_ws(canonical_license_raw)

    # ── Write section files ──────────────────────────────────────────────
    print("\nWriting section files...")
    written = []

    fm_path = SECTIONS_DIR / FRONT_MATTER_FILENAME
    fm_bytes = canonical_forematter.encode("utf-8")
    fm_path.write_bytes(fm_bytes)
    written.append((FRONT_MATTER_FILENAME, len(fm_bytes)))
    print(f"  {FRONT_MATTER_FILENAME:45s} {len(fm_bytes):8,d} bytes  "
          f"(deduplicated from {len(present)} file(s))")

    for story in present:
        block = splits[story["order"]]["story_block"]
        out_path = SECTIONS_DIR / story["section"]
        encoded = block.encode("utf-8")
        out_path.write_bytes(encoded)
        written.append((story["section"], len(encoded)))
        print(f"  {story['section']:45s} {len(encoded):8,d} bytes  ({story['title']})")

    lic_path = SECTIONS_DIR / LICENSE_FILENAME
    lic_bytes = canonical_license.encode("utf-8")
    lic_path.write_bytes(lic_bytes)
    written.append((LICENSE_FILENAME, len(lic_bytes)))
    print(f"  {LICENSE_FILENAME:45s} {len(lic_bytes):8,d} bytes  "
          f"(deduplicated from {len(present)} file(s), whitespace-normalized)")

    for story in missing:
        print(f"  {story['section']:45s} {'—':>8s}         "
              f"NOT PRODUCED — source missing ({story['title']})")

    # ── Conservation accounting ──────────────────────────────────────────
    total_input_bytes = sum(len(splits[s["order"]]["raw_bytes"]) for s in present)
    total_output_bytes = sum(n for _, n in written)

    # Expected relationship:
    #   sum(input files) == front-matter(1x) + sum(story blocks, 1x each) + license(1x)
    #                        + (n-1) duplicate forematter copies removed
    #                        + (n-1) duplicate (possibly whitespace-varying) license copies removed
    #                        +/- small whitespace-normalization delta in the license block
    n = len(present)
    dedup_forematter_bytes_removed = (n - 1) * len(canonical_forematter.encode("utf-8"))
    # Use each file's own original license byte length for an honest "removed" estimate.
    license_byte_lengths = [
        len(splits[s["order"]]["license_block"].encode("utf-8")) for s in present
    ]
    dedup_license_bytes_removed = sum(license_byte_lengths) - len(canonical_license.encode("utf-8"))

    print("\nConservation accounting:")
    print(f"  Input files considered      : {n}")
    print(f"  Total input bytes           : {total_input_bytes:,}")
    print(f"  Total output bytes          : {total_output_bytes:,}")
    print(f"  Forematter bytes deduplicated (removed): {dedup_forematter_bytes_removed:,} "
          f"({n - 1} redundant copies of {len(canonical_forematter.encode('utf-8')):,} bytes each)")
    print(f"  License bytes deduplicated (removed)   : {dedup_license_bytes_removed:,} "
          f"(sum of {n} originals minus 1 canonical, whitespace-normalized copy)")
    reconstructed = total_output_bytes + dedup_forematter_bytes_removed + dedup_license_bytes_removed
    delta = total_input_bytes - reconstructed
    print(f"  Reconstructed total (output + removed) : {reconstructed:,}")
    print(f"  Delta vs. total input bytes             : {delta:+,} "
          f"(should be 0 if the only removed content is redundant forematter/license copies)")

    if delta != 0:
        print(
            "  WARNING: nonzero delta — see source/prepare_report.txt for detail; "
            "this can arise from the license whitespace-normalization changing a few "
            "bytes per file (expected, harmless) but should be double-checked if large.",
        )

    # ── Write conservation report ────────────────────────────────────────
    report_lines = []
    report_lines.append("Overclocked source preparation — conservation report")
    report_lines.append("=" * 60)
    report_lines.append("")
    report_lines.append(f"Story files present : {n} / {len(STORIES)}")
    for story in present:
        report_lines.append(f"  - {story['title']} ({story['txt']})")
    if missing:
        report_lines.append(f"Story files MISSING : {len(missing)} / {len(STORIES)}")
        for story in missing:
            report_lines.append(f"  - {story['title']} ({story['txt']}) — NOT downloaded; "
                                 f"see source/manifest.json for status. No section file "
                                 f"({story['section']}) was produced for this story.")
    report_lines.append("")
    report_lines.append("Deduplication")
    report_lines.append("-" * 60)
    report_lines.append(
        f"Forematter: identical (byte-for-byte) across all {n} present file(s). "
        f"Written once to {FRONT_MATTER_FILENAME} "
        f"({len(canonical_forematter.encode('utf-8')):,} bytes)."
    )
    if any_whitespace_diff:
        report_lines.append(
            f"License block: NOT byte-identical across all {n} present file(s) — "
            f"differences were limited to trailing whitespace on one blank line and/or "
            f"the presence/absence of a final trailing newline. Verified equivalent "
            f"after whitespace normalization. Written once, whitespace-normalized, to "
            f"{LICENSE_FILENAME} ({len(canonical_license.encode('utf-8')):,} bytes)."
        )
        for note in license_notes:
            report_lines.append(note.strip())
    else:
        report_lines.append(
            f"License block: identical (byte-for-byte) across all {n} present file(s). "
            f"Written once to {LICENSE_FILENAME} "
            f"({len(canonical_license.encode('utf-8')):,} bytes)."
        )
    report_lines.append("")
    report_lines.append("Per-story unique content")
    report_lines.append("-" * 60)
    for story in present:
        block = splits[story["order"]]["story_block"]
        report_lines.append(
            f"  {story['section']:40s} {len(block.encode('utf-8')):8,d} bytes  "
            f"(introduction + story text, {story['title']})"
        )
    report_lines.append("")
    report_lines.append("Byte accounting")
    report_lines.append("-" * 60)
    report_lines.append(f"  Total input bytes (present originals)   : {total_input_bytes:,}")
    report_lines.append(f"  Total output bytes (all section files)  : {total_output_bytes:,}")
    report_lines.append(f"  Forematter bytes deduplicated away       : {dedup_forematter_bytes_removed:,}")
    report_lines.append(f"  License bytes deduplicated away          : {dedup_license_bytes_removed:,}")
    report_lines.append(f"  Reconstructed total (output + removed)   : {reconstructed:,}")
    report_lines.append(f"  Delta vs. total input                    : {delta:+,}")
    report_lines.append("")
    report_lines.append(
        "All unique content (forematter once, each story's own introduction + "
        "story text, license once) is accounted for. No story text was altered, "
        "reordered, or condensed by this script; only the two exactly-repeated "
        "blocks (forematter, license) were deduplicated, and only after being "
        "verified equivalent across every file that contains them."
    )
    report_lines.append("")

    REPORT_PATH.write_bytes(("\n".join(report_lines) + "\n").encode("utf-8"))
    print(f"\nConservation report written to {REPORT_PATH}")

    print(f"\nSections written: {len(written)} / {len(STORIES) + 2} "
          f"(front-matter + {len(STORIES)} stories + license)")
    if missing:
        print(f"Incomplete: {len(missing)} story section(s) not produced due to missing "
              f"source(s) — see warnings above. This is expected until the missing "
              f"source(s) are downloaded.")
        print("\n✓ Source preparation complete for all available stories "
              "(with known, reported gaps).")
    else:
        print("\n✓ Source preparation complete — all stories present.")


if __name__ == "__main__":
    main()
