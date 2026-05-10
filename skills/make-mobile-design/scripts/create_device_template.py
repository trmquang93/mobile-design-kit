#!/usr/bin/env python3
"""Generate a standalone HTML iPhone device template with Dynamic Island
and home indicator, ready to be filled with screen content.

Usage:
    python create_device_template.py <output.html> [--title "Screen Name"]
"""

import argparse
import sys
from pathlib import Path
from string import Template

TEMPLATE = Template("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>$title</title>
    <style>
        :root {
            --color-bg: #FFFFFF;
            --color-text: #000000;
            --color-text-secondary: #6B7280;
            --color-island: #000000;
            --font-system: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", system-ui, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;

            /* iOS HIG type ramp — keep in sync with components/01-base-tokens.md */
            --text-caption2:    11px;
            --text-caption1:    12px;
            --text-footnote:    13px;
            --text-subheadline: 15px;
            --text-callout:     16px;
            --text-body:        17px;
            --text-title3:      20px;
            --text-title2:      22px;
            --text-title1:      28px;
            --text-largetitle:  34px;
            --text-md:          var(--text-body);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        html, body {
            background: #1a1a1a;
            font-family: var(--font-system);
            font-size: var(--text-body);
            line-height: 1.29;
            letter-spacing: -0.022em;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            color: var(--color-text);
            min-height: 100vh;
        }

        body {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px 0;
        }

        .device {
            position: relative;
            width: 430px;
            height: 932px;
            min-width: 430px;
            min-height: 932px;
            flex-shrink: 0;
            background: var(--color-bg);
            border-radius: 48px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            overflow: hidden;
        }

        /* Dynamic Island */
        .dynamic-island {
            position: absolute;
            top: 11px;
            left: 50%;
            transform: translateX(-50%);
            width: 126px;
            height: 37px;
            background: var(--color-island);
            border-radius: 19px;
            z-index: 100;
            pointer-events: none;
        }

        /* Status Bar (matches components/02-status-bar.md) — overlays content, stays fixed during scroll */
        .status-bar {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 59px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 24px 8px;
            z-index: 50;
            pointer-events: none;
        }

        .status-bar-time {
            font-size: var(--text-md);
            font-weight: 600;
        }

        .status-bar-icons {
            display: flex;
            gap: 6px;
            align-items: center;
        }

        /* Scrollable content — scrolls behind status bar and home indicator.
           Any floating overlay placed over .device-content (custom tab bar, FAB,
           banner, sheet handle) MUST set `pointer-events: none` on its wrapper
           and `pointer-events: auto` on its interactive children, otherwise the
           overlay swallows wheel/touch and the screen stops scrolling under it. */
        .device-content {
            position: absolute;
            inset: 0;
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
            padding-top: 59px;    /* space for status bar */
            padding-bottom: 34px; /* space for home indicator */
        }
        /* Block layout, NOT flex — flex-direction:column with overflow:auto
           lets browsers shrink children below their content size and the
           container then reports scrollHeight == clientHeight (no scroll). */

        .device-content::-webkit-scrollbar { display: none; }
        .device-content { scrollbar-width: none; }

        /* Home Indicator — overlays content, stays fixed during scroll */
        .home-indicator-area {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 34px;
            display: flex;
            justify-content: center;
            align-items: flex-end;
            padding-bottom: 8px;
            pointer-events: none;
            z-index: 50;
        }

        .home-indicator {
            width: 134px;
            height: 5px;
            background: var(--color-text);
            border-radius: 3px;
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <div class="device">
        <!-- Dynamic Island (always on top) -->
        <div class="dynamic-island"></div>

        <!-- Status Bar -->
        <div class="status-bar">
            <span class="status-bar-time">9:41</span>
            <div class="status-bar-icons">
                <svg width="16" height="12" viewBox="0 0 16 12" fill="currentColor"><rect x="0" y="3" width="3" height="9" rx="1"/><rect x="4.5" y="2" width="3" height="10" rx="1"/><rect x="9" y="0" width="3" height="12" rx="1"/><rect x="13" y="1" width="3" height="11" rx="1"/></svg>
                <svg width="16" height="12" viewBox="0 0 16 12" fill="currentColor"><path d="M8 3C10.7 3 13.1 4.2 14.7 6.1L16 4.8C14 2.5 11.2 1 8 1S2 2.5 0 4.8L1.3 6.1C2.9 4.2 5.3 3 8 3Z"/><path d="M8 7C9.5 7 10.9 7.6 11.9 8.6L13.2 7.3C11.8 5.9 10 5 8 5S4.2 5.9 2.8 7.3L4.1 8.6C5.1 7.6 6.5 7 8 7Z"/><circle cx="8" cy="11" r="1.5"/></svg>
                <svg width="25" height="12" viewBox="0 0 25 12" fill="currentColor"><rect x="0" y="1" width="21" height="10" rx="2" stroke="currentColor" stroke-width="1" fill="none"/><rect x="22" y="4" width="2" height="4" rx="1"/><rect x="2" y="3" width="17" height="6" rx="1"/></svg>
            </div>
        </div>

        <!-- Insert screen content here -->
        <main class="device-content">
            <!-- Screen content goes here -->
        </main>

        <!-- Home Indicator -->
        <div class="home-indicator-area">
            <div class="home-indicator"></div>
        </div>
    </div>
</body>
</html>
""")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate an iPhone device template HTML file with Dynamic Island and home indicator."
    )
    parser.add_argument("output", help="Output HTML file path")
    parser.add_argument("--title", default="Mobile Screen", help="Page title (default: 'Mobile Screen')")
    args = parser.parse_args()

    out_path = Path(args.output)
    if not out_path.parent.exists():
        print(f"Error: parent directory does not exist: {out_path.parent}", file=sys.stderr)
        return 1

    html = TEMPLATE.substitute(title=args.title)
    out_path.write_text(html, encoding="utf-8")
    print(f"Created device template: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
