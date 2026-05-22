#!/usr/bin/env python3
"""Inject a Material 3 bottom navigation bar into an Android screen HTML file
(edits the file in place).

The bottom nav has 3-5 destinations. The active item gets a pill-shaped
`secondary-container`-tinted active indicator behind its icon — this is the
single most recognizable Android-vs-iOS giveaway.

Two styles:

    standard  Flat bottom nav using `surface-container` color. (Default.)

    elevated  Adds level-2 elevation shadow plus surface-tint overlay. Use
              when the nav sits over rich content/photography.

The bottom-nav CSS lives in skills/make-mobile-design/assets/device-android.css
(already linked by create_android_template.py / create_android_tablet_template.py).
This script emits markup only.

Usage:
    python3 add_android_navbar.py <screen.html> \\
        --item home:Home \\
        --item search:Search \\
        --item bookmark:Saved \\
        --item user:Profile \\
        --active 0
"""

import argparse
import re
import sys
from pathlib import Path

ICON_ALIASES = {
    "home":      "material-symbols:home-outline",
    "home-fill": "material-symbols:home",
    "search":    "material-symbols:search",
    "mail":      "material-symbols:mail-outline",
    "user":      "material-symbols:person-outline",
    "person":    "material-symbols:person-outline",
    "settings":  "material-symbols:settings-outline",
    "heart":     "material-symbols:favorite-outline",
    "bell":      "material-symbols:notifications-outline",
    "bookmark":  "material-symbols:bookmark-outline",
    "calendar":  "material-symbols:calendar-today-outline",
    "chat":      "material-symbols:chat-outline",
    "compass":   "material-symbols:explore-outline",
    "star":      "material-symbols:star-outline",
    "clock":     "material-symbols:schedule-outline",
    "phone":     "material-symbols:phone-outline",
    "grid":      "material-symbols:apps",
    "menu":      "material-symbols:menu",
    "plus":      "material-symbols:add",
    "library":   "material-symbols:library-books-outline",
    "video":     "material-symbols:videocam-outline",
    "music":     "material-symbols:music-note",
    "shop":      "material-symbols:storefront-outline",
    "cart":      "material-symbols:shopping-cart-outline",
}

STYLES = ("standard", "elevated")


def parse_item(raw: str) -> tuple[str, str]:
    if ":" not in raw:
        raise ValueError(
            f"--item must be '<icon>:<title>' (got {raw!r}). "
            "Use a colon to separate, e.g. 'home:Home' or 'mdi:home:Home'."
        )
    icon, title = raw.rsplit(":", 1)
    icon = ICON_ALIASES.get(icon, icon)
    if "/" in icon or icon.endswith(".svg"):
        raise ValueError(f"Icon must be an Iconify name, not a URL: {icon!r}")
    if ":" not in icon:
        raise ValueError(
            f"Icon {icon!r} is not a known alias and is not in 'collection:name' form."
        )
    title = title.strip()
    if not title:
        raise ValueError(f"Title is empty in --item {raw!r}")
    return icon, title


def parse_badge(raw: str) -> tuple[int, str]:
    if ":" not in raw:
        raise ValueError(f"--badge must be 'INDEX:COUNT' (got {raw!r})")
    idx_str, count = raw.split(":", 1)
    return int(idx_str), count.strip()


def icon_url(icon: str) -> str:
    return f"https://api.iconify.design/{icon.replace(':', '/', 1)}.svg"


def build(style: str, items, active: int, badges: dict[int, str]) -> str:
    """Build the bottom-nav HTML markup. No CSS — that lives in
    assets/device-android.css. The .bottom-nav--elevated modifier toggles
    the level-2 shadow."""

    style_class = " bottom-nav--elevated" if style == "elevated" else ""

    nav_items = []
    for idx, (icon, title) in enumerate(items):
        is_active = idx == active
        active_cls = " is-active" if is_active else ""
        active_attr = ' aria-current="page"' if is_active else ""
        badge_html = ""
        if idx in badges:
            count = badges[idx]
            display = count if len(count) <= 2 else "99+"
            badge_html = f'<span class="bottom-nav__badge" aria-label="{count} notifications">{display}</span>'
        nav_items.append(
            f'    <button class="bottom-nav__item{active_cls}"{active_attr} aria-label="{title}">\n'
            f"        <span class=\"bottom-nav__indicator\" style=\"--icon: url('{icon_url(icon)}');\">\n"
            f'            <span class="bottom-nav__icon" aria-hidden="true"></span>\n'
            f'        </span>\n'
            f'        <span class="bottom-nav__label">{title}</span>\n'
            f'        {badge_html}\n'
            f'    </button>'
        )

    return (
        f'\n        <!-- Bottom Navigation ({style}, added by add_android_navbar.py) -->\n'
        f'        <nav class="bottom-nav{style_class}" aria-label="Primary">\n'
        + "\n".join(nav_items)
        + '\n        </nav>\n'
    )


def inject(html: str, nav_html: str) -> str:
    if 'class="bottom-nav"' in html or 'class="bottom-nav ' in html:
        raise RuntimeError(
            "A bottom navigation bar is already present in this file. "
            "Remove it first or edit the existing markup."
        )

    marker = re.search(r"[ \t]*<!--\s*Gesture-navigation pill\s*-->", html)
    if marker:
        idx = marker.start()
        return html[:idx] + nav_html + html[idx:]

    device_close = html.rfind("</div>\n</body>")
    if device_close == -1:
        raise RuntimeError(
            "Could not find an injection point for the bottom nav. "
            "Re-scaffold the screen with create_android_template.py."
        )
    return html[:device_close] + nav_html + html[device_close:]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inject a Material 3 bottom navigation bar into an Android screen HTML file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("file", help="Path to the screen HTML file (edited in place)")
    parser.add_argument("--style", choices=STYLES, default="standard")
    parser.add_argument(
        "--item", action="append", required=True, metavar="ICON:TITLE",
        help="Bottom-nav destination. Repeat for each (3-5 recommended).",
    )
    parser.add_argument("--active", type=int, default=0)
    parser.add_argument(
        "--badge", action="append", default=[], metavar="IDX:COUNT",
        help="Notification badge on item IDX. Repeatable.",
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

    if not 3 <= len(items) <= 5:
        print(
            f"Warning: {len(items)} items — MD3 bottom nav supports 3 to 5 destinations.",
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

    nav_html = build(args.style, items, args.active, badges)

    html = target.read_text(encoding="utf-8")
    try:
        new_html = inject(html, nav_html)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    target.write_text(new_html, encoding="utf-8")
    print(
        f"Added {args.style} bottom nav with {len(items)} destinations to {target} "
        f"(active: {args.active}{', badges: ' + str(len(badges)) if badges else ''})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
