#!/usr/bin/env python3
"""Generate a standalone HTML Pixel 8 device template with a top hole-punch
camera, 24dp status bar, and gesture-navigation pill — ready to be filled
with Material 3 screen content.

Usage:
    python3 create_android_template.py <output.html> [--title "Screen Name"]

Notes:
- 412 x 915 viewport (Pixel 8 logical density).
- MD3 baseline tokens inlined in :root; keep in sync with
  components/android/01-base-tokens.md.
- Roboto Flex loaded from Google Fonts.
- .device-content uses padding-top: 0 so the FIRST CHILD owns the 24px
  status-bar safe area, matching the iOS scaffold convention (lets a top
  app bar's background fill behind the status bar).
"""

import argparse
import sys
from pathlib import Path
from string import Template

TEMPLATE = Template(r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>$title</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Flex:opsz,wght@8..144,300..900&family=Roboto+Mono:wght@400;500&display=swap">
    <style>
        :root {
            /* Material 3 — baseline LIGHT scheme.
               Keep in sync with components/android/01-base-tokens.md. */
            --md-sys-color-primary:                #6750A4;
            --md-sys-color-on-primary:             #FFFFFF;
            --md-sys-color-primary-container:      #EADDFF;
            --md-sys-color-on-primary-container:   #4F378B;
            --md-sys-color-secondary:              #625B71;
            --md-sys-color-on-secondary:           #FFFFFF;
            --md-sys-color-secondary-container:    #E8DEF8;
            --md-sys-color-on-secondary-container: #1D192B;
            --md-sys-color-tertiary:               #7D5260;
            --md-sys-color-on-tertiary:            #FFFFFF;
            --md-sys-color-tertiary-container:     #FFD8E4;
            --md-sys-color-on-tertiary-container:  #31111D;
            --md-sys-color-error:                  #B3261E;
            --md-sys-color-on-error:               #FFFFFF;
            --md-sys-color-error-container:        #F9DEDC;
            --md-sys-color-on-error-container:     #410E0B;
            --md-sys-color-background:             #FEF7FF;
            --md-sys-color-on-background:          #1D1B20;
            --md-sys-color-surface:                #FEF7FF;
            --md-sys-color-on-surface:             #1D1B20;
            --md-sys-color-surface-variant:        #E7E0EC;
            --md-sys-color-on-surface-variant:     #49454F;
            --md-sys-color-outline:                #79747E;
            --md-sys-color-outline-variant:        #CAC4D0;
            --md-sys-color-surface-container-lowest:  #FFFFFF;
            --md-sys-color-surface-container-low:     #F7F2FA;
            --md-sys-color-surface-container:         #F3EDF7;
            --md-sys-color-surface-container-high:    #ECE6F0;
            --md-sys-color-surface-container-highest: #E6E0E9;
            --md-sys-color-surface-tint:           var(--md-sys-color-primary);
            --md-sys-color-inverse-surface:        #322F35;
            --md-sys-color-inverse-on-surface:     #F5EFF7;
            --md-sys-color-scrim:                  #000000;

            /* MD3 type scale (size / line-height in px). Use Roboto Flex. */
            --md-sys-typescale-display-large:    57px;
            --md-sys-typescale-display-medium:   45px;
            --md-sys-typescale-display-small:    36px;
            --md-sys-typescale-headline-large:   32px;
            --md-sys-typescale-headline-medium:  28px;
            --md-sys-typescale-headline-small:   24px;
            --md-sys-typescale-title-large:      22px;
            --md-sys-typescale-title-medium:     16px;
            --md-sys-typescale-title-small:      14px;
            --md-sys-typescale-body-large:       16px;
            --md-sys-typescale-body-medium:      14px;
            --md-sys-typescale-body-small:       12px;
            --md-sys-typescale-label-large:      14px;
            --md-sys-typescale-label-medium:     12px;
            --md-sys-typescale-label-small:      11px;

            /* MD3 corner shape tokens */
            --md-sys-shape-corner-none:        0px;
            --md-sys-shape-corner-extra-small: 4px;
            --md-sys-shape-corner-small:       8px;
            --md-sys-shape-corner-medium:      12px;
            --md-sys-shape-corner-large:       16px;
            --md-sys-shape-corner-extra-large: 28px;
            --md-sys-shape-corner-full:        9999px;

            /* MD3 tonal elevation — combine box-shadow with surface-tint
               overlay for full effect (see android.md "Elevation"). */
            --md-sys-elevation-level0: none;
            --md-sys-elevation-level1: 0 1px 2px rgba(0,0,0,0.30), 0 1px 3px 1px rgba(0,0,0,0.15);
            --md-sys-elevation-level2: 0 1px 2px rgba(0,0,0,0.30), 0 2px 6px 2px rgba(0,0,0,0.15);
            --md-sys-elevation-level3: 0 4px 8px 3px rgba(0,0,0,0.15), 0 1px 3px rgba(0,0,0,0.30);
            --md-sys-elevation-level4: 0 6px 10px 4px rgba(0,0,0,0.15), 0 2px 3px rgba(0,0,0,0.30);
            --md-sys-elevation-level5: 0 8px 12px 6px rgba(0,0,0,0.15), 0 4px 4px rgba(0,0,0,0.30);

            /* MD3 motion easing */
            --md-sys-motion-easing-standard:               cubic-bezier(0.2, 0.0, 0, 1.0);
            --md-sys-motion-easing-emphasized:             cubic-bezier(0.2, 0.0, 0, 1.0);
            --md-sys-motion-easing-emphasized-decelerate:  cubic-bezier(0.05, 0.7, 0.1, 1.0);
            --md-sys-motion-easing-emphasized-accelerate:  cubic-bezier(0.3, 0.0, 0.8, 0.15);
            --md-sys-motion-easing-linear:                 linear;

            /* MD3 motion durations */
            --md-sys-motion-duration-short1:  50ms;
            --md-sys-motion-duration-short2: 100ms;
            --md-sys-motion-duration-short3: 150ms;
            --md-sys-motion-duration-short4: 200ms;
            --md-sys-motion-duration-medium1: 250ms;
            --md-sys-motion-duration-medium2: 300ms;
            --md-sys-motion-duration-medium3: 350ms;
            --md-sys-motion-duration-medium4: 400ms;
            --md-sys-motion-duration-long1:  450ms;
            --md-sys-motion-duration-long2:  500ms;

            --font-roboto: "Roboto Flex", "Roboto", "Google Sans", system-ui, -apple-system, sans-serif;
            --font-mono:   "Roboto Mono", ui-monospace, "SF Mono", Menlo, monospace;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --md-sys-color-primary:                #D0BCFF;
                --md-sys-color-on-primary:             #381E72;
                --md-sys-color-primary-container:      #4F378B;
                --md-sys-color-on-primary-container:   #EADDFF;
                --md-sys-color-secondary:              #CCC2DC;
                --md-sys-color-on-secondary:           #332D41;
                --md-sys-color-secondary-container:    #4A4458;
                --md-sys-color-on-secondary-container: #E8DEF8;
                --md-sys-color-tertiary:               #EFB8C8;
                --md-sys-color-on-tertiary:            #492532;
                --md-sys-color-tertiary-container:     #633B48;
                --md-sys-color-on-tertiary-container:  #FFD8E4;
                --md-sys-color-error:                  #F2B8B5;
                --md-sys-color-on-error:               #601410;
                --md-sys-color-error-container:        #8C1D18;
                --md-sys-color-on-error-container:     #F9DEDC;
                --md-sys-color-background:             #141218;
                --md-sys-color-on-background:          #E6E0E9;
                --md-sys-color-surface:                #141218;
                --md-sys-color-on-surface:             #E6E0E9;
                --md-sys-color-surface-variant:        #49454F;
                --md-sys-color-on-surface-variant:     #CAC4D0;
                --md-sys-color-outline:                #938F99;
                --md-sys-color-outline-variant:        #49454F;
                --md-sys-color-surface-container-lowest:  #0F0D13;
                --md-sys-color-surface-container-low:     #1D1B20;
                --md-sys-color-surface-container:         #211F26;
                --md-sys-color-surface-container-high:    #2B2930;
                --md-sys-color-surface-container-highest: #36343B;
                --md-sys-color-inverse-surface:        #E6E0E9;
                --md-sys-color-inverse-on-surface:     #322F35;
            }
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        html, body {
            background: #1a1a1a;
            font-family: var(--font-roboto);
            font-size: var(--md-sys-typescale-body-large);
            line-height: 1.5;
            color: var(--md-sys-color-on-surface);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            min-height: 100vh;
        }

        body {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px 0;
        }

        /* Pixel 8 frame: 412 x 915 logical px, ~36px corner radius */
        .device {
            position: relative;
            width: 412px;
            height: 915px;
            min-width: 412px;
            min-height: 915px;
            flex-shrink: 0;
            background: var(--md-sys-color-background);
            border-radius: 44px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            overflow: hidden;
        }

        /* Hole-punch camera — centered, top */
        .hole-punch {
            position: absolute;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            width: 14px;
            height: 14px;
            background: #000;
            border-radius: 50%;
            z-index: 100;
            pointer-events: none;
        }

        /* Status bar (matches components/android/02-status-bar.md) — 24px,
           pinned via position:absolute; top:0; z-index:50.
           pointer-events: none so taps fall through to scrolling content. */
        .status-bar {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 4px 20px 0;
            font-size: var(--md-sys-typescale-label-medium);
            font-weight: 500;
            color: var(--md-sys-color-on-surface);
            z-index: 50;
            pointer-events: none;
        }

        .status-bar-time { letter-spacing: 0.02em; }
        .status-bar-icons { display: flex; gap: 4px; align-items: center; }

        /* Scrollable content. Same convention as the iOS scaffold:
           padding-top is 0 — the FIRST CHILD inside .device-content owns the
           24px status-bar safe area via its own padding-top:
              .top-app-bar  → padding-top: calc(24px + 8px)
              .page-content → padding-top: 24px
              full-bleed    → 0 (image/hero bleeds behind status bar)

           Any floating overlay over .device-content (custom bottom nav, FAB,
           snackbar) MUST set `pointer-events: none` on its wrapper and
           `pointer-events: auto` on its interactive children, otherwise the
           overlay swallows scroll over its footprint. */
        .device-content {
            position: absolute;
            inset: 0;
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
            padding-top: 0;          /* status-bar offset belongs on first child */
            padding-bottom: 24px;    /* clearance above gesture-nav pill */
            background: var(--md-sys-color-background);
        }
        .device-content::-webkit-scrollbar { display: none; }
        .device-content { scrollbar-width: none; }

        /* Gesture-nav pill — overlay, never scrolls */
        .gesture-nav-area {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 24px;
            display: flex;
            justify-content: center;
            align-items: flex-end;
            padding-bottom: 10px;
            pointer-events: none;
            z-index: 50;
        }
        .gesture-nav-pill {
            width: 108px;
            height: 4px;
            background: var(--md-sys-color-on-surface);
            border-radius: 2px;
            opacity: 0.85;
        }
    </style>
</head>
<body>
    <div class="device" data-platform="android">
        <!-- Hole-punch camera (always on top) -->
        <div class="hole-punch"></div>

        <!-- Status bar -->
        <div class="status-bar">
            <span class="status-bar-time">9:41</span>
            <div class="status-bar-icons">
                <!-- Signal -->
                <svg width="14" height="10" viewBox="0 0 14 10" fill="currentColor" aria-hidden="true"><rect x="0" y="7" width="2" height="3" rx="0.5"/><rect x="3" y="5" width="2" height="5" rx="0.5"/><rect x="6" y="3" width="2" height="7" rx="0.5"/><rect x="9" y="0" width="2" height="10" rx="0.5"/></svg>
                <!-- Wi-Fi -->
                <svg width="14" height="10" viewBox="0 0 14 10" fill="currentColor" aria-hidden="true"><path d="M7 2.5c1.9 0 3.6.7 4.9 1.9l1.1-1.1C11.4 1.7 9.3 1 7 1S2.6 1.7 1 3.3l1.1 1.1C3.4 3.2 5.1 2.5 7 2.5Z"/><path d="M7 5c1.1 0 2.1.4 2.8 1.1l1.1-1.1C9.9 4 8.5 3.5 7 3.5S4.1 4 3.1 5l1.1 1.1C4.9 5.4 5.9 5 7 5Z"/><circle cx="7" cy="8.5" r="1.3"/></svg>
                <!-- Battery -->
                <svg width="22" height="10" viewBox="0 0 22 10" fill="none" aria-hidden="true"><rect x="0.5" y="0.5" width="19" height="9" rx="1.5" stroke="currentColor" stroke-width="1"/><rect x="20" y="3" width="1.5" height="4" rx="0.5" fill="currentColor"/><rect x="2" y="2" width="14" height="6" rx="0.5" fill="currentColor"/></svg>
            </div>
        </div>

        <!-- Screen content goes here -->
        <main class="device-content">
            <!-- Fill with Android (Material 3) components -->
        </main>

        <!-- Gesture-navigation pill -->
        <div class="gesture-nav-area">
            <div class="gesture-nav-pill"></div>
        </div>
    </div>
</body>
</html>
""")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a Pixel 8 (Android, Material 3) device template HTML file."
    )
    parser.add_argument("output", help="Output HTML file path")
    parser.add_argument("--title", default="Android Screen", help="Page title (default: 'Android Screen')")
    args = parser.parse_args()

    out_path = Path(args.output)
    if not out_path.parent.exists():
        print(f"Error: parent directory does not exist: {out_path.parent}", file=sys.stderr)
        return 1

    html = TEMPLATE.substitute(title=args.title)
    out_path.write_text(html, encoding="utf-8")
    print(f"Created Android device template: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
