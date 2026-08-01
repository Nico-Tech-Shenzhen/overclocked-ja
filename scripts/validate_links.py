#!/usr/bin/env python3
"""
validate_links.py
Check that internal links resolve to files that actually exist, matching
VitePress's own dead-link checking (VitePress fails the production build on
any dead internal link; this script gives the same signal earlier, in CI and
locally, without weakening that check).

Checks:
  - Image references in docs/**/*.md must point to files that exist.
    VitePress convention: /images/foo.png => docs/public/images/foo.png
  - Internal markdown links ([text](/path)) in docs/**/*.md must resolve to
    an existing page.
  - Internal sidebar links (link: '/path') in docs/.vitepress/config.mts must
    resolve to an existing page.

An untranslated story that is listed as plain text (not a markdown link) is
not something this script can see, by design — plain text never matches the
link regex, so it never produces a warning or an error. That is the correct,
intentional state for stories that don't have a docs/ja/*.md file yet: don't
link to a page that doesn't exist; list it as plain text instead.

Usage: python3 scripts/validate_links.py
"""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DOCS_DIR = REPO_ROOT / "docs"
PUBLIC_DIR = DOCS_DIR / "public"
CONFIG_MTS = DOCS_DIR / ".vitepress" / "config.mts"

IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\((/[^)#\s]+)")
SIDEBAR_LINK_RE = re.compile(r"link:\s*'(/[^']+)'")

errors: list[str] = []


def resolve_vitepress_path(src: str) -> Path:
    """Resolve a VitePress URL path to a filesystem path."""
    stripped = src.lstrip("/")
    public_candidate = PUBLIC_DIR / stripped
    if public_candidate.exists():
        return public_candidate
    docs_candidate = DOCS_DIR / stripped
    if docs_candidate.exists():
        return docs_candidate
    docs_md = (DOCS_DIR / stripped).with_suffix(".md")
    if docs_md.exists():
        return docs_md
    return public_candidate


def check_file(md_path: Path):
    text = md_path.read_text(encoding="utf-8")
    rel = md_path.relative_to(REPO_ROOT)

    # Image refs
    for alt, src in IMG_RE.findall(text):
        if src.startswith("http"):
            continue
        if src.startswith("/"):
            resolved = resolve_vitepress_path(src)
        else:
            resolved = (md_path.parent / src).resolve()

        if not resolved.exists():
            errors.append(
                f"{rel}: broken image '{src}' "
                f"(expected at {resolved.relative_to(REPO_ROOT)})"
            )

    # Internal markdown links (absolute paths only). A missing local page is
    # a real dead link — VitePress will fail the production build on this,
    # so this must be an error here too, not a warning.
    for text_content, href in LINK_RE.findall(text):
        href_path = href.split("#")[0]
        if not href_path or href_path.startswith("http"):
            continue
        resolved = resolve_vitepress_path(href_path)
        if not resolved.exists():
            errors.append(
                f"{rel}: dead link '{href}' -> no page at "
                f"'{resolved.relative_to(REPO_ROOT)}'"
            )


def check_sidebar(config_path: Path):
    """Check docs/.vitepress/config.mts sidebar link: '/path' entries.

    Only checks internal ('/'-prefixed) links inside the sidebar/nav config
    (nav/editLink entries pointing at external URLs like GitHub are skipped
    automatically since they don't match the leading-'/' pattern this
    regex requires — well, editLink patterns and some nav entries use
    full https:// URLs which don't match `link: '/...'` at all).
    """
    if not config_path.exists():
        return
    text = config_path.read_text(encoding="utf-8")
    rel = config_path.relative_to(REPO_ROOT)

    for href in SIDEBAR_LINK_RE.findall(text):
        href_path = href.split("#")[0]
        resolved = resolve_vitepress_path(href_path)
        if not resolved.exists():
            errors.append(
                f"{rel}: dead sidebar/nav link '{href}' -> no page at "
                f"'{resolved.relative_to(REPO_ROOT)}'"
            )


def main():
    md_files = list(DOCS_DIR.rglob("*.md"))
    print(f"Checking {len(md_files)} markdown files + sidebar config ...\n")

    for f in sorted(md_files):
        check_file(f)

    check_sidebar(CONFIG_MTS)

    if errors:
        print("ERRORS:")
        for e in errors:
            print(f"  ✗  {e}")
        print(f"\n{len(errors)} error(s) found.")
        sys.exit(1)
    else:
        print("✓ All links OK — no dead links found.")


if __name__ == "__main__":
    main()
