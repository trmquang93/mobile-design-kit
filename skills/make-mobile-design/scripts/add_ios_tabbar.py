#!/usr/bin/env python3
"""Inject a tab bar into a mobile screen HTML file (edits the file in place).

Six styles, all driven by --style:

    icon-circle   White floating capsule, icon-only. Active item wears a
                  dark filled circle behind a light icon. (Default.)

    pill-outline  White floating capsule. Active item expands into an
                  outlined pill that shows icon + label; others icon-only.

    pill-filled   Like pill-outline but the active pill is filled with a
                  light accent tint instead of an outline.

    classic       Flat full-width tab bar pinned above the home indicator
                  (no capsule). Every item shows icon + label stacked.
                  Use --badge IDX:COUNT to add a notification badge.

    glass         Translucent liquid-glass capsule (backdrop blur). Active
                  item gets a soft glass tint. Per Apple HIG: glass on the
                  navigation layer only.

    glass-split   Liquid-glass capsule for items 0..N-2, plus a separate
                  liquid-glass circle for the last item (use it for a
                  trailing action like search).

The CSS for every style lives in skills/make-mobile-design/assets/device-ios.css
(already linked by create_ios_template.py / create_ipad_template.py). This
script emits markup only, plus the per-screen color overrides as inline
CSS variables (--tab-dark / --tab-light / --tab-accent) on the <nav>.

Usage:
    python3 add_ios_tabbar.py <screen.html> \\
        --style pill-outline \\
        --item home:Home \\
        --item search:Search \\
        --item bookmark:Saved \\
        --item user:Profile \\
        --active 0

Each --item is "<icon>:<title>". <icon> is a built-in alias (home, menu,
plus, mail, user, search, settings, heart, bell, bookmark, calendar, chat,
compass, star, clock, phone, grid, mic) or any Iconify name like
"mdi:home-outline" or "lucide:plus". Title is the label / aria-label.

    --active IDX            0-based active index (default 0).
    --badge IDX:COUNT       (classic only, repeatable) red badge on item IDX.
    --dark-color HEX        Inactive icon color / circle fill (default #25282C).
    --light-color HEX       Bar background / active icon color (default #FFFFFF).
    --accent-color HEX      Active accent (default #1194AA for pill styles,
                            #007AFF for classic).
"""

import argparse
import re
import sys
from pathlib import Path

ICON_ALIASES = {
    "home": "lucide:home",
    "menu": "lucide:menu",
    "plus": "lucide:plus-circle",
    "mail": "lucide:mail",
    "user": "lucide:user",
    "search": "lucide:search",
    "settings": "lucide:settings",
    "heart": "lucide:heart",
    "bell": "lucide:bell",
    "bookmark": "lucide:bookmark",
    "calendar": "lucide:calendar",
    "chat": "lucide:message-circle",
    "compass": "lucide:compass",
    "star": "lucide:star",
    "clock": "lucide:clock",
    "phone": "lucide:phone",
    "grid": "lucide:grid-3x3",
    "mic": "lucide:mic",
}

STYLES = (
    "icon-circle",
    "pill-outline",
    "pill-filled",
    "classic",
    "glass",
    "glass-split",
)

PILL_STYLES = {"pill-outline", "pill-filled"}
GLASS_STYLES = {"glass", "glass-split"}


def parse_item(raw: str) -> tuple[str, str]:
    if ":" not in raw:
        raise ValueError(
            f"--item must be '<icon>:<title>' (got {raw!r}). "
            "Use a colon to separate, e.g. 'home:Home' or 'mdi:home-outline:Home'."
        )
    icon, title = raw.rsplit(":", 1)
    icon = ICON_ALIASES.get(icon, icon)
    if "/" in icon or icon.endswith(".svg"):
        raise ValueError(f"Icon must be an Iconify name, not a URL or path: {icon!r}")
    if ":" not in icon:
        raise ValueError(
            f"Icon {icon!r} is not a known alias and is not in 'collection:name' Iconify form."
        )
    title = title.strip()
    if not title:
        raise ValueError(f"Title is empty in --item {raw!r}")
    return icon, title


def parse_badge(raw: str) -> tuple[int, str]:
    if ":" not in raw:
        raise ValueError(f"--badge must be 'INDEX:COUNT' (got {raw!r})")
    idx_str, count = raw.split(":", 1)
    idx = int(idx_str)
    count = count.strip()
    if not count:
        raise ValueError(f"--badge count is empty in {raw!r}")
    return idx, count


def icon_url(icon: str) -> str:
    return f"https://api.iconify.design/{icon.replace(':', '/', 1)}.svg"


def _item_html(icon: str, title: str, *, active: bool, with_label: bool, badge: str | None = None) -> str:
    """Render a single <button> tab item."""
    active_cls = " active" if active else ""
    badge_html = ""
    icon_wrap_open = ""
    icon_wrap_close = ""
    if badge is not None:
        # classic style wraps the icon for badge positioning
        icon_wrap_open = '<span class="float-tab-icon-wrap">'
        icon_wrap_close = f'<span class="float-tab-badge">{badge}</span></span>'
    label_html = f'<span class="float-tab-label">{title}</span>' if with_label else ""
    return (
        f'            <button class="float-tab-item{active_cls}" '
        f'aria-label="{title}" style="--icon: url(\'{icon_url(icon)}\');">\n'
        f'                {icon_wrap_open}<span class="float-tab-icon"></span>{icon_wrap_close}\n'
        f'                {label_html}\n'
        f'            </button>'
    )


def build(style: str, items, active: int, dark: str, light: str, accent: str, badges: dict[int, str]):
    """Build the tab-bar HTML markup. No CSS — that lives in the shared
    stylesheet. The <nav> carries inline CSS variables for per-screen
    colors."""

    if style == "glass-split" and len(items) < 2:
        raise ValueError("glass-split requires at least 2 items (one splits off)")

    style_vars = f"--tab-dark: {dark}; --tab-light: {light}; --tab-accent: {accent};"
    glass_class = " float-tab-glass" if style in GLASS_STYLES else ""

    with_label = style in PILL_STYLES

    if style == "glass-split":
        main_items = items[:-1]
        trailing_icon, trailing_title = items[-1]
        trailing_idx = len(items) - 1
        rows = [
            _item_html(ic, t, active=(i == active), with_label=False)
            for i, (ic, t) in enumerate(main_items)
        ]
        trailing_active = active == trailing_idx
        return (
            f'\n        <!-- Tab Bar (glass-split, added by add_ios_tabbar.py) -->\n'
            f'        <nav class="float-tab-bar float-tab-bar--glass-split{glass_class}" '
            f'aria-label="Primary" style="{style_vars}">\n'
            + "\n".join(rows) + "\n        </nav>\n"
            f'        <div class="float-tab-trailing float-tab-glass" style="{style_vars}">\n'
            + _item_html(trailing_icon, trailing_title, active=trailing_active, with_label=False)
            + "\n        </div>\n"
        )

    rows = []
    for i, (ic, title) in enumerate(items):
        badge_val = badges.get(i) if style == "classic" else None
        rows.append(_item_html(
            ic, title,
            active=(i == active),
            with_label=with_label,
            badge=badge_val,
        ))
    return (
        f'\n        <!-- Tab Bar ({style}, added by add_ios_tabbar.py) -->\n'
        f'        <nav class="float-tab-bar float-tab-bar--{style}{glass_class}" '
        f'aria-label="Primary" style="{style_vars}">\n'
        + "\n".join(rows) + "\n        </nav>\n"
    )


# ---------- injection ----------

GLASS_SVG_DEFS = (
    '    <!-- Liquid Glass distortion filter (see components/ios/00-liquid-glass.md) -->\n'
    '    <svg width="0" height="0" style="position:absolute" aria-hidden="true">\n'
    '      <filter id="glass-distortion" x="0%" y="0%" width="100%" height="100%">\n'
    '        <feImage preserveAspectRatio="none" result="map"\n'
    '          href=\'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" preserveAspectRatio="none"><defs>\n'
    '            <linearGradient id="x" x1="0" y1="0.5" x2="1" y2="0.5">\n'
    '                <stop offset="0" stop-color="rgb(255,0,0)"/>\n'
    '                <stop offset="0.15" stop-color="rgb(128,0,0)"/>\n'
    '                <stop offset="0.85" stop-color="rgb(128,0,0)"/>\n'
    '                <stop offset="1" stop-color="rgb(255,0,0)"/>\n'
    '            </linearGradient>\n'
    '            <linearGradient id="y" x1="0.5" y1="0" x2="0.5" y2="1">\n'
    '                <stop offset="0" stop-color="rgb(0,255,0)"/>\n'
    '                <stop offset="0.15" stop-color="rgb(0,128,0)"/>\n'
    '                <stop offset="0.85" stop-color="rgb(0,128,0)"/>\n'
    '                <stop offset="1" stop-color="rgb(0,255,0)"/>\n'
    '            </linearGradient>\n'
    '        </defs><rect width="100" height="100" fill="url(%23x)"/><rect width="100" height="100" fill="url(%23y)" style="mix-blend-mode:screen"/></svg>\'/>\n'
    '        <feGaussianBlur in="map" stdDeviation="2" result="smoothed"/>\n'
    '        <feDisplacementMap in="SourceGraphic" in2="smoothed" scale="40" xChannelSelector="R" yChannelSelector="G"/>\n'
    '      </filter>\n'
    '    </svg>\n'
)


def inject(html: str, tabbar_html: str, *, needs_glass_defs: bool) -> str:
    if 'class="float-tab-bar"' in html or 'class="float-tab-bar ' in html:
        raise RuntimeError(
            "A floating tab bar is already present in this file. "
            "Remove it first or edit the existing markup."
        )

    if needs_glass_defs and 'id="glass-distortion"' not in html:
        if "<body" in html:
            html = re.sub(
                r"(<body[^>]*>\n?)",
                lambda m: m.group(1) + GLASS_SVG_DEFS,
                html,
                count=1,
            )
        else:
            raise RuntimeError("Could not find <body> to inject the glass-distortion <defs>.")

    home_marker = re.search(r"[ \t]*<!--\s*Home Indicator\s*-->", html)
    if home_marker:
        idx = home_marker.start()
        return html[:idx] + tabbar_html + html[idx:]

    device_close = html.rfind("</div>\n</body>")
    if device_close == -1:
        raise RuntimeError(
            "Could not find an injection point for the tab bar. "
            "Re-scaffold the screen with create_ios_template.py."
        )
    return html[:device_close] + tabbar_html + html[device_close:]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inject a tab bar into a mobile screen HTML file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("file", help="Path to the screen HTML file (edited in place)")
    parser.add_argument(
        "--style",
        choices=STYLES,
        default="icon-circle",
        help="Visual style (default: icon-circle)",
    )
    parser.add_argument(
        "--item", action="append", required=True, metavar="ICON:TITLE",
        help="Tab bar item. Repeat for each item (3-5 recommended).",
    )
    parser.add_argument(
        "--active", type=int, default=0,
        help="0-based index of the active item (default: 0)",
    )
    parser.add_argument(
        "--badge", action="append", default=[], metavar="IDX:COUNT",
        help="Notification badge on item IDX (classic style only). Repeatable.",
    )
    parser.add_argument("--dark-color", default="#25282C")
    parser.add_argument("--light-color", default="#FFFFFF")
    parser.add_argument(
        "--accent-color", default=None,
        help="Active accent color (default: #1194AA for pills/glass, #007AFF for classic)",
    )
    args = parser.parse_args()

    target = Path(args.file)
    if not target.is_file():
        print(f"Error: file not found: {target}", file=sys.stderr)
        return 1

    try:
        items = [parse_item(raw) for raw in args.item]
        badges_list = [parse_badge(raw) for raw in args.badge]
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not 2 <= len(items) <= 6:
        print(
            f"Warning: {len(items)} items — tab bars work best with 3 to 5 items.",
            file=sys.stderr,
        )

    if not 0 <= args.active < len(items):
        print(f"Error: --active {args.active} out of range (0..{len(items) - 1})", file=sys.stderr)
        return 1

    badges = {}
    for idx, count in badges_list:
        if not 0 <= idx < len(items):
            print(f"Error: --badge index {idx} out of range", file=sys.stderr)
            return 1
        badges[idx] = count
    if badges and args.style != "classic":
        print(
            f"Warning: --badge is only rendered for --style classic (got {args.style}); ignored.",
            file=sys.stderr,
        )
        badges = {}

    accent = args.accent_color or ("#007AFF" if args.style == "classic" else "#1194AA")

    try:
        tabbar_html = build(
            args.style, items, args.active, args.dark_color, args.light_color, accent, badges,
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    html = target.read_text(encoding="utf-8")
    try:
        new_html = inject(
            html, tabbar_html,
            needs_glass_defs=args.style in GLASS_STYLES,
        )
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    target.write_text(new_html, encoding="utf-8")
    print(
        f"Added {args.style} tab bar with {len(items)} items to {target} "
        f"(active: {args.active}{', badges: ' + str(len(badges)) if badges else ''})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
