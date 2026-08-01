#!/usr/bin/env python3
"""Build the full Japanese "Overclocked" collection as EPUB and PDF.

Pipeline (adapted from the Little Brother project's book-build workflow):

  1. `prepare` - clean each translated section (strip VitePress frontmatter,
     the repeated per-page <small> credit footer, and HTML comments) and
     write them, in book order, to build/book/. A generated colophon page
     (license + credits, once) is appended at the end.
  2. `epub`    - feed the cleaned sections to Pandoc (`-f markdown-citations`,
     so "@tks" is not parsed as a citation) to produce a reflowable Japanese
     EPUB3 with a linked TOC and one page-break per story.
  3. `pdf`     - convert the cleaned sections to Typst markup and compile a
     Japanese A4 PDF with Noto Serif CJK JP (falls back to a pandoc/xelatex
     or pandoc/wkhtmltopdf pipeline if Typst is unavailable).
  4. `all`     - run prepare, epub, and pdf in sequence.

Overclocked is a SIX-STORY collection, not a single novel split into
chapters. Book order is: front matter, then the six stories in their
official published order, then a generated colophon. Each story starts a
new page/section in both PDF and EPUB output (mirroring the Little Brother
per-chapter page-break behavior, applied per-story here instead).

`validate_story_order()` is a hard gate: both `epub` and `pdf` refuse to
build unless all six stories are present in `docs/ja/`, appear exactly
once, and are in the correct collection order. This script never publishes
or links a partial/incomplete "complete book" file — if any story is
missing, the build aborts loudly instead of producing a misleading output.

Usage:
    python scripts/build_book.py prepare
    python scripts/build_book.py epub
    python scripts/build_book.py pdf
    python scripts/build_book.py all
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_JA = ROOT / "docs" / "ja"
BUILD_DIR = ROOT / "build" / "book"
OUTPUT_DIR = ROOT / "docs" / "public" / "downloads"
CSS_PATH = ROOT / "scripts" / "book.css"

EPUB_OUTPUT = OUTPUT_DIR / "overclocked-ja.epub"
PDF_OUTPUT = OUTPUT_DIR / "overclocked-ja.pdf"

TITLE = "Overclocked 日本語訳"
AUTHOR = "Cory Doctorow"
TRANSLATOR = "日本語訳: 高須正和（@tks） / 協力: ニコ技深圳コミュニティ"
LANGUAGE = "ja-JP"
PROJECT_URL = "https://github.com/Nico-Tech-Shenzhen/overclocked-ja"
LICENSE_NOTICE = (
    "原著および本日本語訳は、クリエイティブ・コモンズ 表示 - 非営利 - 継承 2.5 "
    "（CC BY-NC-SA 2.5）ライセンスの条件で提供されます。"
    "https://creativecommons.org/licenses/by-nc-sa/2.5/"
)
UNOFFICIAL_NOTICE = (
    "本書は、著者 Cory Doctorow および原出版社 Thunder's Mouth Press による公式な"
    "日本語版ではありません。原著の CC ライセンス条件に基づき高須正和が公開する"
    "非公式の日本語訳プロジェクトです。DRM は使用していません。"
)

# Book order. Six stories in the official 2007 collection order.
# `colophon` is generated in this script, not read from docs/ja/.
STORIES = [
    ("printcrime", "Printcrime"),
    ("when-sysadmins-ruled-the-earth", "When Sysadmins Ruled the Earth"),
    ("andas-game", "Anda's Game"),
    ("i-robot", "I, Robot"),
    ("i-row-boat", "I, Row-Boat"),
    ("after-the-siege", "After the Siege"),
]

SECTIONS = [
    ("front-matter", "表紙・ライセンス表記"),
    *STORIES,
]

COLOPHON_SLUG = "colophon"
COLOPHON_LABEL = "ライセンスとクレジット"


# --------------------------------------------------------------------------
# Story-order validation (hard gate — never build/publish a partial book)
# --------------------------------------------------------------------------

def validate_story_order() -> None:
    """Confirm all six stories exist in docs/ja/, appear exactly once, and
    are listed in the correct collection order. Raises SystemExit with a
    clear message if not — callers must not proceed to build EPUB/PDF."""
    missing = [slug for slug, _ in STORIES if not (DOCS_JA / f"{slug}.md").is_file()]
    if missing:
        raise SystemExit(
            "Refusing to build: the following story section(s) are missing from "
            f"docs/ja/ — {', '.join(missing)}. A complete book cannot be built "
            "until a translation for every story exists. This script never "
            "publishes or links a partial/incomplete book file."
        )

    # STORIES is itself the single source of truth for order, and slugs are
    # unique literals within it — but re-derive and re-check explicitly so
    # a future edit to this list cannot silently introduce a duplicate.
    slugs = [slug for slug, _ in STORIES]
    seen = set()
    duplicates = set()
    for slug in slugs:
        if slug in seen:
            duplicates.add(slug)
        seen.add(slug)
    if duplicates:
        raise SystemExit(f"Refusing to build: duplicate story slug(s) in STORIES: {duplicates}")

    expected_order = [
        "printcrime",
        "when-sysadmins-ruled-the-earth",
        "andas-game",
        "i-robot",
        "i-row-boat",
        "after-the-siege",
    ]
    if slugs != expected_order:
        raise SystemExit(
            "Refusing to build: STORIES order does not match the official "
            f"collection order.\n  expected: {expected_order}\n  actual  : {slugs}"
        )

    print(f"Story order OK: all {len(STORIES)} stories present, unique, and in "
          "the correct order.")


# --------------------------------------------------------------------------
# Step 1: prepare
# --------------------------------------------------------------------------

def strip_source_wrappers(text: str) -> str:
    """Strip VitePress frontmatter, the repeated per-page <small> credit
    footer, and HTML comments (translator TODO notes) from a section file.
    This is also what keeps English source text/draft notes/TODOs out of
    the generated EPUB/PDF: everything outside the frontmatter/footer/
    comment wrappers is the translated Japanese prose itself."""
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S)
    text = re.sub(r"\n?<small>\s*.*?</small>\s*\Z", "\n", text, flags=re.S | re.I)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return text.strip() + "\n"


def colophon_markdown() -> str:
    return (
        f"# {COLOPHON_LABEL}\n\n"
        f"**{TITLE}**\n\n"
        f"原著: *Overclocked: Stories of the Future Present* (c) Cory Doctorow "
        f"/ Thunder's Mouth Press, 2007\n\n"
        f"{TRANSLATOR}\n\n"
        f"{LICENSE_NOTICE}\n\n"
        f"{UNOFFICIAL_NOTICE}\n\n"
        f"プロジェクトページ: {PROJECT_URL}\n"
    )


def prepare(build_dir: Path = BUILD_DIR) -> list[Path]:
    """Clean each translated section and write it to build/book/, in book
    order, plus a generated colophon file at the end. Returns the ordered
    list of prepared markdown file paths. Refuses to run unless all six
    stories are present, unique, and correctly ordered."""
    validate_story_order()

    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True)

    missing = [slug for slug, _ in SECTIONS if not (DOCS_JA / f"{slug}.md").is_file()]
    if missing:
        raise SystemExit("Missing Japanese section(s): " + ", ".join(missing))

    prepared: list[Path] = []
    for index, (slug, _label) in enumerate(SECTIONS, start=1):
        source = (DOCS_JA / f"{slug}.md").read_text(encoding="utf-8")
        cleaned = strip_source_wrappers(source)
        out_path = build_dir / f"{index:02d}-{slug}.md"
        out_path.write_bytes(cleaned.encode("utf-8"))
        prepared.append(out_path)

    colophon_path = build_dir / f"{len(SECTIONS) + 1:02d}-{COLOPHON_SLUG}.md"
    colophon_path.write_bytes(colophon_markdown().encode("utf-8"))
    prepared.append(colophon_path)

    print(f"Prepared {len(prepared)} section(s) in {build_dir}")
    return prepared


def prepared_files(build_dir: Path = BUILD_DIR) -> list[Path]:
    if not build_dir.exists():
        return prepare(build_dir)
    files = sorted(build_dir.glob("*.md"))
    if len(files) != len(SECTIONS) + 1:
        return prepare(build_dir)
    return files


# --------------------------------------------------------------------------
# Step 2: EPUB (Pandoc)
# --------------------------------------------------------------------------

def build_epub(files: list[Path], output: Path = EPUB_OUTPUT) -> None:
    validate_story_order()
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "pandoc",
        "-f", "markdown-citations",
        "-t", "epub3",
        "--metadata", f"title={TITLE}",
        "--metadata", f"creator={AUTHOR}",
        "--metadata", f"contributor={TRANSLATOR}",
        "--metadata", f"lang={LANGUAGE}",
        "--metadata", f"rights=CC BY-NC-SA 2.5 (unofficial translation, no DRM)",
        "--css", str(CSS_PATH),
        "--epub-chapter-level=1",
        "--toc",
        "--toc-depth=1",
        "-o", str(output),
        *[str(f) for f in files],
    ]
    subprocess.run(cmd, check=True, cwd=ROOT)
    errors = validate_epub(output)
    if errors:
        raise SystemExit("EPUB validation failed:\n- " + "\n- ".join(errors))
    print(f"EPUB built: {output} ({output.stat().st_size} bytes)")


def validate_epub(output: Path) -> list[str]:
    """Validate structure, leaked source text, and story order/uniqueness
    of the generated EPUB. Navigation must list each story exactly once,
    in the correct collection order (front matter, then the six stories)."""
    errors: list[str] = []
    with zipfile.ZipFile(output) as archive:
        names = archive.namelist()
        if not names or names[0] != "mimetype":
            errors.append("mimetype must be the first ZIP member")
        elif archive.getinfo("mimetype").compress_type != zipfile.ZIP_STORED:
            errors.append("mimetype must be stored uncompressed")
        if archive.read("mimetype") != b"application/epub+zip":
            errors.append("invalid mimetype content")
        opf_names = [n for n in names if n.endswith("content.opf")]
        if not opf_names:
            errors.append("missing content.opf")
        else:
            opf = archive.read(opf_names[0]).decode("utf-8")
            for required in (TITLE, AUTHOR):
                if required not in opf:
                    errors.append(f"OPF metadata missing: {required!r}")

        # Leaked source-text / draft-note detection.
        story_order_seen: list[str] = []
        for name in names:
            if name.endswith(".xhtml") or name.endswith(".html"):
                content = archive.read(name).decode("utf-8", errors="ignore")
                if "translation_status:" in content or "<small>" in content:
                    errors.append(f"source wrapper leaked into {name}")
                if "<!--" in content:
                    errors.append(f"HTML comment leaked into {name}")
                for slug, _label in STORIES:
                    if slug in name:
                        story_order_seen.append(slug)

        expected = [slug for slug, _ in STORIES]
        # Filter to first occurrence per file, preserving encounter order,
        # then compare against the expected sequence.
        seen_unique_in_order = list(dict.fromkeys(story_order_seen))
        counts = {s: story_order_seen.count(s) for s in expected}
        duplicated = {s: c for s, c in counts.items() if c > 1}
        if duplicated:
            errors.append(f"story appears more than once in EPUB output: {duplicated}")
        missing_in_output = [s for s in expected if s not in counts or counts[s] == 0]
        if missing_in_output:
            errors.append(f"story missing from EPUB output: {missing_in_output}")
        if not duplicated and not missing_in_output and seen_unique_in_order != expected:
            errors.append(
                f"stories are out of order in EPUB output: "
                f"expected {expected}, saw {seen_unique_in_order}"
            )
    return errors


# --------------------------------------------------------------------------
# Step 3: PDF (Typst, with pandoc fallback)
# --------------------------------------------------------------------------

def escape_typst(text: str) -> str:
    replacements = [
        ("\\", "\\\\"),
        ("#", "\\#"),
        ("$", "\\$"),
        ("@", "\\@"),
        ("<", "\\<"),
        (">", "\\>"),
        ("[", "\\["),
        ("]", "\\]"),
        ("~", "\\~"),
        ("_", "\\_"),
        ("*", "\\*"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def inline_typst(text: str) -> str:
    tokens: list[str] = []

    def hold(fragment: str) -> str:
        tokens.append(fragment)
        return f"\x00{len(tokens) - 1}\x00"

    text = re.sub(
        r"\[([^\]]+)\]\(([^\s)]+)(?:\s+[\"'][^\"']*[\"'])?\)",
        lambda m: hold(f'#link("{m.group(2)}")[{escape_typst(m.group(1))}]'),
        text,
    )
    text = re.sub(r"`([^`]+)`", lambda m: hold(f"`{m.group(1)}`"), text)
    text = re.sub(
        r"\*\*(.+?)\*\*|__(.+?)__",
        lambda m: hold(f"*{escape_typst(m.group(1) or m.group(2))}*"),
        text,
    )
    text = re.sub(
        r"(?<!\*)\*([^*\n]+?)\*(?!\*)|(?<!_)_([^_\n]+?)_(?!_)",
        lambda m: hold(f"_{escape_typst(m.group(1) or m.group(2))}_"),
        text,
    )
    text = escape_typst(text)
    for index, token in enumerate(tokens):
        text = text.replace(f"\x00{index}\x00", token)
    return text


def markdown_to_typst(markdown: str) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    quote: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            output.append(inline_typst("\n".join(paragraph)))
            output.append("")
            paragraph.clear()

    def flush_quote() -> None:
        if quote:
            body = " ".join(inline_typst(part) for part in quote)
            output.append(f"#quote(block: true)[{body}]")
            output.append("")
            quote.clear()

    for raw in lines + [""]:
        line = raw.rstrip()
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        item = re.match(r"^\s*([-+*]|\d+\.)\s+(.+)$", line)
        if line.startswith(">"):
            flush_paragraph()
            content = re.sub(r"^>\s?", "", line)
            if content:
                quote.append(content)
            continue
        flush_quote()
        if heading:
            flush_paragraph()
            level = len(heading.group(1))
            output.append(f"{'=' * level} {inline_typst(heading.group(2))}")
            output.append("")
        elif item:
            flush_paragraph()
            marker = "+" if item.group(1)[0].isdigit() else "-"
            output.append(f"{marker} {inline_typst(item.group(2))}")
        elif re.fullmatch(r"\s*([-*_])(?:\s*\1){2,}\s*", line):
            flush_paragraph()
            output.append("#line(length: 60%)")
            output.append("")
        elif not line.strip():
            flush_paragraph()
        else:
            paragraph.append(line)
    return "\n".join(output)


TYPST_PREAMBLE = '''
#set document(title: "%s", author: "%s")
#set page(paper: "a4", margin: (top: 2.5cm, bottom: 2.5cm, left: 2.2cm, right: 2.2cm), numbering: "1")
#set text(font: "Noto Serif CJK JP", lang: "ja", size: 10.5pt)
#set par(justify: true, leading: 0.95em, first-line-indent: 1em)
#set heading(numbering: none)
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  block(it)
}
#show link: underline
''' % (TITLE, AUTHOR)


def typst_title_page() -> str:
    # #outline() collects level-1 headings (each story's H1) into a linked
    # PDF table of contents whose entries jump to their destinations.
    return (
        "#align(center)[\n"
        "  #v(4cm)\n"
        f'  #text(size: 22pt, weight: "bold")[{escape_typst(TITLE)}]\n'
        "  #v(1em)\n"
        f"  #text(size: 14pt)[{escape_typst(AUTHOR)}]\n"
        "  #v(0.5em)\n"
        f"  #text(size: 11pt)[{escape_typst(TRANSLATOR)}]\n"
        "]\n"
        "#pagebreak()\n"
        '#outline(title: "目次", depth: 1)\n'
        "#pagebreak(weak: true)\n"
    )


def build_typst_source(files: list[Path]) -> str:
    parts = [TYPST_PREAMBLE, typst_title_page()]
    for path in files:
        parts.append(markdown_to_typst(path.read_text(encoding="utf-8")))
        parts.append("")
    return "\n".join(parts)


def compile_with_typst(typ_path: Path, output: Path) -> None:
    if shutil.which("typst"):
        subprocess.run(["typst", "compile", str(typ_path), str(output)], check=True, cwd=ROOT)
        return
    import typst as typst_pkg  # pip install typst

    typst_pkg.compile(str(typ_path), output=str(output), format="pdf")


def build_pdf_fallback(files: list[Path], output: Path) -> None:
    for engine in ("wkhtmltopdf", "weasyprint"):
        if shutil.which(engine):
            cmd = [
                "pandoc", "-f", "markdown-citations", "-t", "pdf",
                f"--pdf-engine={engine}", "--css", str(CSS_PATH),
                "-o", str(output), *[str(f) for f in files],
            ]
            subprocess.run(cmd, check=True, cwd=ROOT)
            print(f"PDF built (pandoc/{engine} fallback): {output} ({output.stat().st_size} bytes)")
            return
    if shutil.which("xelatex"):
        cmd = [
            "pandoc", "-f", "markdown-citations", "-t", "pdf",
            "--pdf-engine=xelatex",
            "-V", "CJKmainfont=Noto Serif CJK JP",
            "-V", "mainfont=Noto Serif CJK JP",
            "-o", str(output), *[str(f) for f in files],
        ]
        try:
            subprocess.run(cmd, check=True, cwd=ROOT)
        except subprocess.CalledProcessError as exc:
            raise SystemExit(
                "PDF build failed: Typst was unavailable and the xelatex fallback "
                f"also failed ({exc}). Install the 'typst' package "
                "(pip install typst) or a CJK-capable LaTeX toolchain."
            ) from exc
        print(f"PDF built (pandoc/xelatex fallback): {output} ({output.stat().st_size} bytes)")
        return
    raise SystemExit(
        "PDF build failed: no working PDF engine found. Install the 'typst' "
        "Python package (pip install typst) or the Typst CLI."
    )


def build_pdf(files: list[Path], output: Path = PDF_OUTPUT) -> None:
    validate_story_order()
    output.parent.mkdir(parents=True, exist_ok=True)
    typ_source = build_typst_source(files)
    typ_path = BUILD_DIR / "book.typ"
    typ_path.write_bytes(typ_source.encode("utf-8"))

    try:
        compile_with_typst(typ_path, output)
        print(f"PDF built (Typst): {output} ({output.stat().st_size} bytes)")
    except Exception as exc:  # noqa: BLE001 - deliberately broad, this is a build fallback trigger
        print(f"Typst PDF build failed ({exc}); trying fallback PDF engine...", file=sys.stderr)
        build_pdf_fallback(files, output)

    if not output.is_file() or output.stat().st_size == 0:
        raise SystemExit(f"PDF build failed: {output} was not created")
    with output.open("rb") as fh:
        if fh.read(5) != b"%PDF-":
            raise SystemExit(f"PDF build failed: {output} is not a valid PDF")


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["prepare", "epub", "pdf", "all"])
    args = parser.parse_args()

    if args.command == "prepare":
        prepare()
        return

    if args.command == "epub":
        build_epub(prepared_files())
        return

    if args.command == "pdf":
        build_pdf(prepared_files())
        return

    if args.command == "all":
        files = prepare()
        build_epub(files)
        build_pdf(files)
        return


if __name__ == "__main__":
    main()
