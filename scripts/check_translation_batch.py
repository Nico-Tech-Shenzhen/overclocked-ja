#!/usr/bin/env python3
"""
check_translation_batch.py — Read-only validation harness for Overclocked
Japanese translation sections.

Translation status levels (in ascending order of completeness):
  not_started   File is a placeholder; no content checks are applied.
  pilot         Early trial translation; light checks only (status + footer).
  draft         Full translation in progress; all checks applied.
  reviewed      Translation reviewed; all checks applied.
  complete      Translation finalised; all checks applied.

Usage:
    python3 scripts/check_translation_batch.py printcrime
    python3 scripts/check_translation_batch.py printcrime i-robot
    python3 scripts/check_translation_batch.py all

Book structure — Overclocked is a SIX-STORY collection, not a single novel
split into numbered chapters:
    front-matter                     →  docs/ja/front-matter.md
    printcrime                       →  docs/ja/printcrime.md
    when-sysadmins-ruled-the-earth   →  docs/ja/when-sysadmins-ruled-the-earth.md
    andas-game                       →  docs/ja/andas-game.md
    i-robot                          →  docs/ja/i-robot.md
    i-row-boat                       →  docs/ja/i-row-boat.md
    after-the-siege                  →  docs/ja/after-the-siege.md
"""

import re
import sys
import pathlib
from dataclasses import dataclass
from typing import List, Optional, Tuple

REPO = pathlib.Path(__file__).resolve().parent.parent
DOCS_JA = REPO / "docs" / "ja"
CHARACTERS = REPO / "CHARACTERS.md"

# Story slugs, in official collection order. "front-matter" is the common
# collection forematter, not a story, and has no narrator voice of its own —
# it is checked structurally but skipped for the pronoun check.
STORY_SLUGS = [
    "front-matter",
    "printcrime",
    "when-sysadmins-ruled-the-earth",
    "andas-game",
    "i-robot",
    "i-row-boat",
    "after-the-siege",
]

# Maps a story slug to its "## <Heading>" title in CHARACTERS.md, so the
# pronoun check can look up the per-story voice rule recorded there instead
# of hardcoding any one character's name or pronoun.
SLUG_TO_CHARACTERS_HEADING = {
    "printcrime": "Printcrime",
    "when-sysadmins-ruled-the-earth": "When Sysadmins Ruled the Earth",
    "andas-game": "Anda's Game",
    "i-robot": "I, Robot",
    "i-row-boat": "I, Row-Boat",
    "after-the-siege": "After the Siege",
}

# Status levels — lower index = less complete
STATUS_LEVELS = ["not_started", "pilot", "draft", "reviewed", "complete"]


@dataclass
class Target:
    slug: str

    @property
    def tag(self):
        return self.slug

    @property
    def path(self):
        return DOCS_JA / f"{self.slug}.md"


def parse_args(argv: List[str]) -> List[Target]:
    args = argv[1:]
    if not args or args == ["all"]:
        return [Target(s) for s in STORY_SLUGS]

    targets: List[Target] = []
    for tok in args:
        if tok in STORY_SLUGS:
            targets.append(Target(tok))
        else:
            print(f"WARNING: unrecognised argument {tok!r} — skipped "
                  f"(valid: {', '.join(STORY_SLUGS)}, or 'all')", file=sys.stderr)

    return targets


# ── CHARACTERS.md pronoun lookup ────────────────────────────────────────────

# First-person pronouns tracked for the per-story narrator-consistency check.
CANDIDATE_PRONOUNS = ["わたし", "私", "僕", "俺"]


def _load_characters_sections() -> dict:
    """Split CHARACTERS.md into {heading_text: body_text} by '## ' headings."""
    if not CHARACTERS.exists():
        return {}
    text = CHARACTERS.read_text(encoding="utf-8")
    sections: dict = {}
    current_heading = None
    current_lines: List[str] = []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+)$", line)
        if m:
            if current_heading is not None:
                sections[current_heading] = "\n".join(current_lines)
            current_heading = m.group(1).strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_heading is not None:
        sections[current_heading] = "\n".join(current_lines)
    return sections


def _expected_pronoun_for_slug(slug: str, sections: dict) -> Optional[str]:
    """Return the expected first-person pronoun for a story slug, as recorded
    in CHARACTERS.md, or None if not yet determined (PLACEHOLDER) or the slug
    has no narrator voice entry (e.g. front-matter)."""
    heading = SLUG_TO_CHARACTERS_HEADING.get(slug)
    if heading is None:
        return None
    body = sections.get(heading)
    if body is None:
        return None
    m = re.search(r"\*\*First-person pronoun:\*\*\s*(.+)", body)
    if not m:
        return None
    pronoun_line = m.group(1)
    if "PLACEHOLDER" in pronoun_line:
        return None
    quoted = re.findall(r"「(.+?)」", pronoun_line)
    for q in quoted:
        if q in CANDIDATE_PRONOUNS:
            return q
    return None


# ── check patterns ─────────────────────────────────────────────────────────

MARKDOWN_FOOTNOTE_RE = re.compile(r"\[\^")
TOP_CREDIT_RE = re.compile(
    r"^\s*\*?(?:原著|著者|著作権|出版|本翻訳|日本語訳)[::：]",
    re.MULTILINE,
)
BARE_URL_JP_RE = re.compile(
    r"https?://[^\s\)\]>\"\']+[　-鿿＀-￯]"
)


def _read_frontmatter_status(lines: List[str]) -> Optional[str]:
    """Extract translation_status value from YAML frontmatter. Returns None if absent."""
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
                return m.group(1).strip()
    return None


def check_target(t: Target, issues: List[Tuple], summary: List[Tuple],
                  characters_sections: dict):
    tag = t.tag
    path = t.path

    if not path.exists():
        issues.append((tag, "MISSING", f"File not found: {path}"))
        return

    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        issues.append((tag, "MOJIBAKE", f"UTF-8 decode error: {e}"))
        return

    lines = text.splitlines()

    # ── Determine translation status ─────────────────────────────────────────
    status = _read_frontmatter_status(lines)

    if status is None:
        issues.append((tag, "NO-STATUS", "No translation_status field in frontmatter"))
        # Cannot determine skip level; fall through with all checks
        status = "draft"  # treat as needing full check
    elif status not in STATUS_LEVELS:
        issues.append((tag, "BAD-STATUS",
                       f"Unknown translation_status: {status!r} "
                       f"(valid: {', '.join(STATUS_LEVELS)})"))
        status = "draft"

    summary.append((tag, status))

    # not_started: file is a placeholder — skip ALL content checks
    if status == "not_started":
        return

    # ── Checks that apply to pilot and above ─────────────────────────────────

    # footer
    if "<small>" not in text:
        issues.append((tag, "NO-FOOTER", "Missing <small> attribution footer"))

    # ── Checks that apply to draft and above ─────────────────────────────────

    if status in ("draft", "reviewed", "complete"):

        # top credit block in first 30 lines of body (after frontmatter)
        head = "\n".join(lines[:30])
        for mm in TOP_CREDIT_RE.finditer(head):
            lineno = head[:mm.start()].count("\n") + 1
            issues.append((tag, "TOP-CREDIT",
                           f"Line ~{lineno}: credit block in first 30 lines — "
                           f"{mm.group().strip()[:60]}"))

        # Markdown footnote syntax
        for i, line in enumerate(lines, 1):
            if MARKDOWN_FOOTNOTE_RE.search(line):
                issues.append((tag, "MD-FOOTNOTE",
                               f"Line {i}: Markdown footnote [^ — {line[:80]}"))

        # bare URL followed by Japanese
        for i, line in enumerate(lines, 1):
            if BARE_URL_JP_RE.search(line):
                issues.append((tag, "BARE-URL",
                               f"Line {i}: bare URL + Japanese — {line[:100]}"))

        # Per-story narrator pronoun consistency check, driven by the
        # per-story voice rule recorded in CHARACTERS.md (not a hardcoded
        # character name/pronoun — Overclocked has no single narrator voice
        # across the collection).
        expected = _expected_pronoun_for_slug(t.slug, characters_sections)
        if expected is not None:
            expected_count = text.count(expected + "は")
            for other in CANDIDATE_PRONOUNS:
                if other == expected:
                    continue
                other_count = text.count(other + "は")
                if other_count > 3 and other_count > expected_count:
                    issues.append((tag, "PRONOUN",
                                   f"「{other}は」 ({other_count}×) outnumbers "
                                   f"「{expected}は」 ({expected_count}×) — "
                                   f"CHARACTERS.md records 「{expected}」 as this "
                                   "story's narrator pronoun"))


def main():
    argv = sys.argv
    if len(argv) < 2 or argv[1:] == ["all"]:
        targets = parse_args(["script", "all"])
    else:
        targets = parse_args(argv)

    if not targets:
        print("No targets to check.")
        sys.exit(0)

    characters_sections = _load_characters_sections()

    issues: List[Tuple] = []
    summary: List[Tuple] = []

    print(f"Checking {len(targets)} section(s): {', '.join(t.tag for t in targets)}...\n")

    for t in targets:
        check_target(t, issues, summary, characters_sections)

    # ── Status summary ────────────────────────────────────────────────────────
    counts = {s: 0 for s in STATUS_LEVELS}
    for _tag, st in summary:
        if st in counts:
            counts[st] += 1

    print("Translation status summary:")
    for level in STATUS_LEVELS:
        if counts[level] or level in ("not_started", "draft", "complete"):
            print(f"  {level:12s}: {counts[level]}")
    print()

    if issues:
        print("=" * 60)
        print("ISSUES FOUND")
        print("=" * 60)
        for tag, kind, msg in issues:
            print(f"  [{kind}] {tag}: {msg}")
        print()

    if not issues:
        print("✓ All checks passed.")
    else:
        serious = [i for i in issues if i[1] not in ("NO-STATUS",)]
        print(f"Total issues: {len(issues)}  ({len(serious)} serious)")

    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
