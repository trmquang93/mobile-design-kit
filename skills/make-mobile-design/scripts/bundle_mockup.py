#!/usr/bin/env python3
"""Inline shared plugin assets back into a make-mobile-design mockup so the
HTML becomes self-contained and portable.

Scaffolded mockups reference three shared assets (device-chrome.css, the
per-platform device CSS, and figma-export.js) through `<link>` /
`<script src>` tags. Those references resolve only on the machine that
has the mobile-design-kit plugin installed at the original path. When
the mockup is emailed or zipped to someone else, the chrome and the
Copy-to-Figma button vanish.

This script reads such a mockup, replaces each shared-asset reference
with an inline `<style>` / `<script>` block holding the asset's verbatim
contents, and writes a new HTML file. External refs (Google Fonts,
Iconify, any https:// URL) are left alone.

Usage:
    python3 bundle_mockup.py path/to/screen.html
        # → writes path/to/screen.standalone.html

    python3 bundle_mockup.py path/to/screen.html out/screen.html
        # → explicit output path

    python3 bundle_mockup.py screen.html --no-figma
        # → skip inlining figma-export.js and strip the toolbar element

See shared-device-chrome-plan.md §0.1 for the full handoff spec.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

from _shared_template import plugin_root


ASSETS_SUBDIR = ("skills", "make-mobile-design", "assets")

# Asset filenames we're willing to inline from a project's .design/ folder.
# Anything else under .design/ is left alone defensively (we don't blindly
# inline arbitrary files just because the path matches the convention).
KNOWN_ASSETS = frozenset({
    "device-chrome.css",
    "device-ios.css",
    "device-android.css",
    "figma-export.js",
})

LINK_RE = re.compile(
    r'<link\b[^>]*\brel\s*=\s*"stylesheet"[^>]*\bhref\s*=\s*"([^"]+)"[^>]*>',
    re.IGNORECASE,
)
SCRIPT_RE = re.compile(
    r'<script\b[^>]*\bsrc\s*=\s*"([^"]+)"[^>]*>\s*</script>',
    re.IGNORECASE,
)
TOOLBAR_RE = re.compile(
    r'\s*<div\b[^>]*\bdata-figma-export-ignore\b[^>]*>.*?</div>',
    re.DOTALL | re.IGNORECASE,
)


def resolve_asset_ref(href: str, html_dir: Path, assets_dir: Path) -> Path | None:
    """Return the resolved Path if `href` points at an inline-able asset.

    Two acceptable sources:
    1. A file directly under the plugin's canonical assets dir
       (in-plugin mockups under `examples/`).
    2. A known asset filename inside a `.design/` directory anywhere on
       disk (user-project mockups, the normal case).

    Anything else — external URLs, files outside both locations, unknown
    filenames inside `.design/` — returns None and is left untouched.
    """
    parsed = urlparse(href)
    if parsed.scheme in ("http", "https", "data"):
        return None

    if parsed.scheme == "file":
        candidate = Path(unquote(parsed.path))
    elif parsed.scheme == "":
        path = unquote(parsed.path)
        candidate = Path(path)
        if not candidate.is_absolute():
            candidate = html_dir / candidate
    else:
        return None

    try:
        resolved = candidate.resolve()
    except OSError:
        return None

    if not resolved.is_file():
        return None

    try:
        resolved.relative_to(assets_dir)
        return resolved
    except ValueError:
        pass

    if resolved.parent.name == ".design" and resolved.name in KNOWN_ASSETS:
        return resolved

    return None


def inline_link(match: re.Match, html_dir: Path, assets_dir: Path) -> str:
    href = match.group(1)
    resolved = resolve_asset_ref(href, html_dir, assets_dir)
    if resolved is None:
        return match.group(0)
    contents = resolved.read_text(encoding="utf-8")
    rel = resolved.name
    return (
        f"<style>\n/* inlined from {rel} */\n"
        f"{contents}\n</style>"
    )


def inline_script(
    match: re.Match, html_dir: Path, assets_dir: Path, skip_figma: bool
) -> str:
    href = match.group(1)
    resolved = resolve_asset_ref(href, html_dir, assets_dir)
    if resolved is None:
        return match.group(0)
    if skip_figma and resolved.name == "figma-export.js":
        return ""
    contents = resolved.read_text(encoding="utf-8")
    rel = resolved.name
    return (
        f"<script>\n/* inlined from {rel} */\n"
        f"{contents}\n</script>"
    )


def bundle(html: str, html_dir: Path, assets_dir: Path, no_figma: bool) -> str:
    out = LINK_RE.sub(lambda m: inline_link(m, html_dir, assets_dir), html)
    out = SCRIPT_RE.sub(
        lambda m: inline_script(m, html_dir, assets_dir, no_figma), out
    )
    if no_figma:
        out = TOOLBAR_RE.sub("", out)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Inline shared plugin assets into a mockup HTML so it renders "
            "standalone on any machine."
        )
    )
    parser.add_argument("input", help="Path to the mockup HTML to bundle.")
    parser.add_argument(
        "output",
        nargs="?",
        default=None,
        help=(
            "Output path. Defaults to <input>.standalone.html next to the "
            "input file. Refusing to overwrite the input in place."
        ),
    )
    parser.add_argument(
        "--no-figma",
        action="store_true",
        help=(
            "Skip inlining figma-export.js and remove the Copy-to-Figma "
            "toolbar element from the body."
        ),
    )
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.is_file():
        print(f"Error: input file does not exist: {input_path}", file=sys.stderr)
        return 1

    if args.output is None:
        output_path = input_path.with_suffix(".standalone.html")
    else:
        output_path = Path(args.output).resolve()

    if output_path == input_path:
        print(
            "Error: refusing to overwrite the input file in place. "
            "Provide a different output path.",
            file=sys.stderr,
        )
        return 1

    if not output_path.parent.exists():
        print(
            f"Error: output directory does not exist: {output_path.parent}",
            file=sys.stderr,
        )
        return 1

    root = plugin_root()
    assets_dir = (root.joinpath(*ASSETS_SUBDIR)).resolve()
    if not assets_dir.is_dir():
        print(f"Error: plugin asset directory missing: {assets_dir}", file=sys.stderr)
        return 1

    html = input_path.read_text(encoding="utf-8")
    bundled = bundle(html, input_path.parent, assets_dir, args.no_figma)
    output_path.write_text(bundled, encoding="utf-8")
    print(f"Bundled mockup written to: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
