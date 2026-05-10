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

Usage:
    python3 add_tabbar.py <screen.html> \\
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


# ---------- styles ----------

def _icon_circle(items, active, dark, light, accent, badges):
    css = f"""
        /* Floating icon-circle tab bar */
        .float-tab-bar {{
            position: absolute;
            bottom: 46px; left: 50%;
            transform: translateX(-50%);
            width: calc(100% - 40px); max-width: 350px; height: 60px;
            display: flex; justify-content: space-around; align-items: center;
            padding: 0 4px;
            background: {light}; border-radius: 30px;
            box-shadow: 0 8px 24px rgba(0,0,0,.08), 0 2px 6px rgba(0,0,0,.04);
            z-index: 50;
            pointer-events: none; /* let scroll/touch fall through to .device-content */
        }}
        .float-tab-item {{
            pointer-events: auto;
            flex: 1; height: 52px; border: none; background: none; cursor: pointer;
            display: flex; align-items: center; justify-content: center;
            border-radius: 50%; color: {dark};
            transition: background .2s ease, color .2s ease, transform .2s ease;
            -webkit-tap-highlight-color: transparent;
        }}
        .float-tab-item:active {{ transform: scale(.94); }}
        .float-tab-item.active {{
            background: {dark}; color: {light};
            max-width: 52px; flex: 0 0 52px;
        }}
        .float-tab-item .float-tab-icon {{
            width: 24px; height: 24px; background-color: currentColor;
            -webkit-mask: var(--icon) no-repeat center / contain;
            mask: var(--icon) no-repeat center / contain;
        }}
"""
    rows = []
    for i, (ic, title) in enumerate(items):
        rows.append(
            f'            <button class="float-tab-item{" active" if i == active else ""}" '
            f'aria-label="{title}" style="--icon: url(\'{icon_url(ic)}\');">\n'
            f'                <span class="float-tab-icon"></span>\n'
            f'            </button>'
        )
    html = (
        '\n        <!-- Tab Bar (icon-circle, added by add_tabbar.py) -->\n'
        '        <nav class="float-tab-bar" aria-label="Primary">\n'
        + "\n".join(rows) + "\n        </nav>\n"
    )
    return css, html


def _pill(items, active, dark, light, accent, *, filled: bool):
    variant = "pill-filled" if filled else "pill-outline"
    active_decoration = (
        f"background: color-mix(in srgb, {accent} 18%, transparent); border: 0 solid transparent;"
        if filled
        else f"background: transparent; border: 2px solid {accent};"
    )
    css = f"""
        /* Floating {variant} tab bar */
        .float-tab-bar {{
            position: absolute;
            bottom: 46px; left: 50%;
            transform: translateX(-50%);
            width: calc(100% - 32px); max-width: 360px; height: 60px;
            display: flex; align-items: center; gap: 4px;
            padding: 0 12px;
            background: {light}; border-radius: 30px;
            box-shadow: 0 8px 24px rgba(0,0,0,.08), 0 2px 6px rgba(0,0,0,.04);
            z-index: 50;
            pointer-events: none; /* let scroll/touch fall through to .device-content */
        }}
        .float-tab-item {{
            pointer-events: auto;
            flex: 0 0 auto; height: 44px; min-width: 44px;
            border: none; background: none; cursor: pointer;
            display: flex; align-items: center; justify-content: center;
            border-radius: 22px; color: {dark}; padding: 0 10px; gap: 8px;
            transition: background .2s ease, color .2s ease, flex .25s ease, transform .2s ease;
            -webkit-tap-highlight-color: transparent;
        }}
        .float-tab-item:active {{ transform: scale(.96); }}
        .float-tab-item .float-tab-icon {{
            width: 24px; height: 24px; background-color: currentColor; flex: 0 0 24px;
            -webkit-mask: var(--icon) no-repeat center / contain;
            mask: var(--icon) no-repeat center / contain;
        }}
        .float-tab-item .float-tab-label {{
            display: none; font-size: 14px; font-weight: 600; white-space: nowrap;
            font-family: inherit;
        }}
        .float-tab-item.active {{
            flex: 1 1 auto; color: {accent}; {active_decoration}
        }}
        .float-tab-item.active .float-tab-label {{ display: inline; }}
"""
    rows = []
    for i, (ic, title) in enumerate(items):
        rows.append(
            f'            <button class="float-tab-item{" active" if i == active else ""}" '
            f'aria-label="{title}" style="--icon: url(\'{icon_url(ic)}\');">\n'
            f'                <span class="float-tab-icon"></span>\n'
            f'                <span class="float-tab-label">{title}</span>\n'
            f'            </button>'
        )
    html = (
        f'\n        <!-- Tab Bar ({variant}, added by add_tabbar.py) -->\n'
        '        <nav class="float-tab-bar" aria-label="Primary">\n'
        + "\n".join(rows) + "\n        </nav>\n"
    )
    return css, html


def _classic(items, active, dark, light, accent, badges):
    css = f"""
        /* Classic iOS tab bar */
        .float-tab-bar {{
            position: absolute;
            bottom: 34px; left: 0; right: 0;
            display: flex; align-items: stretch;
            padding: 6px 0 4px;
            background: color-mix(in srgb, {light} 92%, transparent);
            backdrop-filter: saturate(180%) blur(20px);
            -webkit-backdrop-filter: saturate(180%) blur(20px);
            border-top: 0.5px solid color-mix(in srgb, {dark} 12%, transparent);
            z-index: 50;
            pointer-events: none; /* let scroll/touch fall through to .device-content */
        }}
        .float-tab-item {{
            pointer-events: auto;
            flex: 1; min-height: 44px;
            border: none; background: none; cursor: pointer;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            gap: 2px; padding: 4px 2px;
            color: color-mix(in srgb, {dark} 60%, transparent);
            font-family: inherit;
            transition: color .15s ease, transform .15s ease;
            -webkit-tap-highlight-color: transparent;
            position: relative;
        }}
        .float-tab-item:active {{ transform: scale(.95); }}
        .float-tab-item.active {{ color: {accent}; }}
        .float-tab-item .float-tab-icon-wrap {{
            position: relative; width: 28px; height: 28px;
            display: flex; align-items: center; justify-content: center;
        }}
        .float-tab-item .float-tab-icon {{
            width: 26px; height: 26px; background-color: currentColor;
            -webkit-mask: var(--icon) no-repeat center / contain;
            mask: var(--icon) no-repeat center / contain;
        }}
        .float-tab-item .float-tab-label {{
            font-size: 10px; font-weight: 500; letter-spacing: .1px;
        }}
        .float-tab-badge {{
            position: absolute; top: -2px; right: -8px;
            min-width: 16px; height: 16px; padding: 0 4px;
            border-radius: 8px; background: #FF3B30; color: #FFFFFF;
            font-size: 11px; font-weight: 600; line-height: 16px; text-align: center;
        }}
"""
    rows = []
    for i, (ic, title) in enumerate(items):
        badge_html = ""
        if i in badges:
            badge_html = f'                    <span class="float-tab-badge">{badges[i]}</span>\n'
        rows.append(
            f'            <button class="float-tab-item{" active" if i == active else ""}" '
            f'aria-label="{title}" style="--icon: url(\'{icon_url(ic)}\');">\n'
            f'                <span class="float-tab-icon-wrap">\n'
            f'                    <span class="float-tab-icon"></span>\n'
            f'{badge_html}'
            f'                </span>\n'
            f'                <span class="float-tab-label">{title}</span>\n'
            f'            </button>'
        )
    html = (
        '\n        <!-- Tab Bar (classic, added by add_tabbar.py) -->\n'
        '        <nav class="float-tab-bar" aria-label="Primary">\n'
        + "\n".join(rows) + "\n        </nav>\n"
    )
    return css, html


def _glass_base_css(dark, light, accent):
    # Refractive Liquid Glass — see components/00-liquid-glass.md.
    # Requires the SVG #glass-distortion <defs> block (injected separately).
    return f"""
        /* Liquid-glass tab bar (refractive; falls back to flat blur). */
        .float-tab-glass {{
            background:
                linear-gradient(135deg,
                    color-mix(in srgb, {light} 22%, transparent) 0%,
                    color-mix(in srgb, {light} 6%, transparent) 28%,
                    color-mix(in srgb, {light} 4%, transparent) 72%,
                    color-mix(in srgb, {light} 28%, transparent) 100%);
            backdrop-filter: url(#glass-distortion) saturate(140%);
            -webkit-backdrop-filter: saturate(180%) blur(24px);
            border: 1px solid color-mix(in srgb, {light} 40%, transparent);
            box-shadow:
                0 10px 28px rgba(0,0,0,.20),
                0 2px 6px rgba(0,0,0,.10),
                0 1px 0 rgba(255,255,255,.85) inset,
                0 -1px 1px rgba(255,255,255,.30) inset;
        }}
        @supports not (backdrop-filter: url(#glass-distortion)) {{
            .float-tab-glass {{
                background: color-mix(in srgb, {light} 32%, transparent);
                backdrop-filter: saturate(180%) blur(24px);
                -webkit-backdrop-filter: saturate(180%) blur(24px);
            }}
        }}
        @media (prefers-reduced-transparency: reduce) {{
            .float-tab-glass {{
                backdrop-filter: none;
                -webkit-backdrop-filter: none;
                background: color-mix(in srgb, {light} 92%, transparent);
            }}
        }}
        .float-tab-item {{
            pointer-events: auto;
            flex: 1; height: 52px; min-width: 52px;
            border: none; background: none; cursor: pointer;
            display: flex; align-items: center; justify-content: center;
            border-radius: 50%; color: {dark};
            transition: background .2s ease, color .2s ease, transform .2s ease;
            -webkit-tap-highlight-color: transparent;
        }}
        .float-tab-item:active {{ transform: scale(.94); }}
        .float-tab-item.active {{
            background: color-mix(in srgb, {accent} 22%, transparent);
            color: {accent};
            max-width: 52px; flex: 0 0 52px;
        }}
        .float-tab-item .float-tab-icon {{
            width: 24px; height: 24px; background-color: currentColor;
            -webkit-mask: var(--icon) no-repeat center / contain;
            mask: var(--icon) no-repeat center / contain;
        }}
"""


def _glass(items, active, dark, light, accent, badges):
    css = _glass_base_css(dark, light, accent) + f"""
        .float-tab-bar {{
            position: absolute;
            bottom: 46px; left: 50%;
            transform: translateX(-50%);
            width: calc(100% - 40px); max-width: 360px; height: 60px;
            display: flex; justify-content: space-around; align-items: center;
            padding: 0 6px; border-radius: 30px;
            z-index: 50;
            pointer-events: none; /* let scroll/touch fall through to .device-content */
        }}
"""
    rows = []
    for i, (ic, title) in enumerate(items):
        rows.append(
            f'            <button class="float-tab-item{" active" if i == active else ""}" '
            f'aria-label="{title}" style="--icon: url(\'{icon_url(ic)}\');">\n'
            f'                <span class="float-tab-icon"></span>\n'
            f'            </button>'
        )
    html = (
        '\n        <!-- Tab Bar (glass, added by add_tabbar.py) -->\n'
        '        <nav class="float-tab-bar float-tab-glass" aria-label="Primary">\n'
        + "\n".join(rows) + "\n        </nav>\n"
    )
    return css, html


def _glass_split(items, active, dark, light, accent, badges):
    if len(items) < 2:
        raise ValueError("glass-split requires at least 2 items (one splits off)")
    main_items = items[:-1]
    trailing = items[-1]
    trailing_idx = len(items) - 1

    css = _glass_base_css(dark, light, accent) + f"""
        .float-tab-bar {{
            position: absolute;
            bottom: 46px; left: 16px;
            right: calc(60px + 24px);
            height: 60px;
            display: flex; justify-content: space-around; align-items: center;
            padding: 0 6px; border-radius: 30px;
            z-index: 50;
            pointer-events: none; /* let scroll/touch fall through to .device-content */
        }}
        .float-tab-trailing {{
            position: absolute;
            bottom: 46px; right: 16px;
            width: 60px; height: 60px;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            z-index: 50;
            pointer-events: none;
        }}
        .float-tab-trailing .float-tab-item {{ height: 60px; flex: 1; }}
"""
    rows = []
    for i, (ic, title) in enumerate(main_items):
        rows.append(
            f'            <button class="float-tab-item{" active" if i == active else ""}" '
            f'aria-label="{title}" style="--icon: url(\'{icon_url(ic)}\');">\n'
            f'                <span class="float-tab-icon"></span>\n'
            f'            </button>'
        )
    trailing_active = " active" if active == trailing_idx else ""
    html = (
        '\n        <!-- Tab Bar (glass-split, added by add_tabbar.py) -->\n'
        '        <nav class="float-tab-bar float-tab-glass" aria-label="Primary">\n'
        + "\n".join(rows) + "\n        </nav>\n"
        '        <div class="float-tab-trailing float-tab-glass">\n'
        f'            <button class="float-tab-item{trailing_active}" '
        f'aria-label="{trailing[1]}" style="--icon: url(\'{icon_url(trailing[0])}\');">\n'
        '                <span class="float-tab-icon"></span>\n'
        '            </button>\n'
        '        </div>\n'
    )
    return css, html


STYLE_BUILDERS = {
    "icon-circle": _icon_circle,
    "classic": _classic,
    "glass": _glass,
    "glass-split": _glass_split,
}


def build(style, items, active, dark, light, accent, badges):
    if style == "pill-outline":
        return _pill(items, active, dark, light, accent, filled=False)
    if style == "pill-filled":
        return _pill(items, active, dark, light, accent, filled=True)
    return STYLE_BUILDERS[style](items, active, dark, light, accent, badges)


# ---------- injection ----------

GLASS_SVG_DEFS = (
    '    <!-- Liquid Glass distortion filter (see components/00-liquid-glass.md) -->\n'
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


def inject(html: str, css_block: str, tabbar_html: str, *, needs_glass_defs: bool) -> str:
    if 'class="float-tab-bar"' in html or 'class="float-tab-bar ' in html:
        raise RuntimeError(
            "A floating tab bar is already present in this file. "
            "Remove it first or edit the existing markup."
        )
    if "</style>" not in html:
        raise RuntimeError("Could not find </style> in the file; not a scaffolded screen?")
    html = html.replace("</style>", css_block + "    </style>", 1)

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
            "Re-scaffold the screen with create_device_template.py."
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
        css_block, tabbar_html = build(
            args.style, items, args.active, args.dark_color, args.light_color, accent, badges,
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    html = target.read_text(encoding="utf-8")
    try:
        new_html = inject(
            html, css_block, tabbar_html,
            needs_glass_defs=args.style in ("glass", "glass-split"),
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
