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

        /* Figma export chrome — host page only, not part of the design payload */
        .figma-export-toolbar {
            position: fixed;
            top: 16px;
            right: 16px;
            display: flex;
            gap: 8px;
            align-items: center;
            z-index: 1000;
            font-family: var(--font-roboto);
        }
        .figma-export-btn {
            appearance: none;
            border: 1px solid rgba(255,255,255,0.18);
            background: rgba(28,28,30,0.72);
            backdrop-filter: blur(20px) saturate(160%);
            -webkit-backdrop-filter: blur(20px) saturate(160%);
            color: #fff;
            font: 500 13px var(--font-roboto);
            padding: 8px 14px;
            border-radius: 999px;
            cursor: pointer;
        }
        .figma-export-btn:hover { background: rgba(44,44,46,0.85); }
        .figma-export-btn:active { transform: scale(0.98); }
        .figma-export-toast {
            color: #fff;
            font-size: 12px;
            opacity: 0.9;
            background: rgba(28,28,30,0.72);
            padding: 6px 10px;
            border-radius: 999px;
            backdrop-filter: blur(20px) saturate(160%);
            -webkit-backdrop-filter: blur(20px) saturate(160%);
        }
        .figma-export-toast[hidden] { display: none; }
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
                <svg width="13" height="13" viewBox="73.6 9.47 36.1 36.06" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" clip-rule="evenodd" d="M109.695 12.2225C109.695 10.7038 108.464 9.47253 106.945 9.47253C105.426 9.47253 104.195 10.7038 104.195 12.2225V42.7781C104.195 44.2969 105.426 45.5281 106.945 45.5281C108.464 45.5281 109.695 44.2969 109.695 42.7781V12.2225ZM89.2219 28.4164C89.2219 26.8976 87.9907 25.6664 86.4719 25.6664C84.9532 25.6664 83.7219 26.8976 83.7219 28.4164V42.7775C83.7219 44.2963 84.9532 45.5275 86.4719 45.5275C87.9907 45.5275 89.2219 44.2963 89.2219 42.7775V28.4164ZM76.3892 33.917C77.908 33.917 79.1392 35.1482 79.1392 36.667V42.7781C79.1392 44.2969 77.908 45.5281 76.3892 45.5281C74.8704 45.5281 73.6392 44.2969 73.6392 42.7781V36.667C73.6392 35.1482 74.8704 33.917 76.3892 33.917ZM99.6113 20.4724C99.6113 18.9536 98.3801 17.7224 96.8613 17.7224C95.3425 17.7224 94.1113 18.9536 94.1113 20.4724V42.7779C94.1113 44.2967 95.3425 45.5279 96.8613 45.5279C98.3801 45.5279 99.6113 44.2967 99.6113 42.7779V20.4724Z"/></svg>
                <!-- Wi-Fi -->
                <svg width="18" height="13" viewBox="3.4 9 46.7 34.4" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" clip-rule="evenodd" d="M16.7266 15.9883C20.0518 14.6069 23.6178 13.898 27.2186 13.9027L27.2218 13.9027C34.7956 13.9027 41.6459 16.9777 46.6005 21.9533C47.5531 22.9099 49.1008 22.9132 50.0574 21.9606C51.0141 21.008 51.0174 19.4603 50.0648 18.5037C44.2305 12.6446 36.1489 9.01425 27.2234 9.01382C22.9773 9.0085 18.7722 9.84448 14.851 11.4735C10.9293 13.1027 7.36927 15.4929 4.37663 18.5059C3.42526 19.4637 3.4305 21.0114 4.38835 21.9628C5.34619 22.9142 6.89392 22.9089 7.8453 21.9511C10.3828 19.3963 13.4013 17.3697 16.7266 15.9883ZM27.2234 9.01382L27.2218 9.01382V11.4583L27.225 9.01382L27.2234 9.01382ZM20.0813 24.5246C22.3374 23.5614 24.7656 23.0663 27.2188 23.0694H27.2248C29.678 23.0663 32.1062 23.5614 34.3623 24.5246C36.6185 25.4878 38.6556 26.8991 40.3501 28.6729C41.2827 29.649 42.83 29.6844 43.8062 28.7518C44.7824 27.8192 44.8177 26.2719 43.8851 25.2957C41.7334 23.0434 39.1467 21.2514 36.2819 20.0283C33.418 18.8057 30.3357 18.177 27.2218 18.1805C24.1078 18.177 21.0256 18.8057 18.1617 20.0283C15.2969 21.2514 12.7102 23.0434 10.5585 25.2957C9.62589 26.2719 9.66124 27.8192 10.6374 28.7518C11.6136 29.6844 13.1609 29.649 14.0935 28.6729C15.788 26.8991 17.8251 25.4878 20.0813 24.5246ZM27.2218 18.1805L27.2188 18.1805L27.2218 20.6249L27.2248 18.1805L27.2218 18.1805ZM23.4996 33.0373C24.668 32.5078 25.9362 32.2346 27.2191 32.236H27.2218C29.9236 32.236 32.346 33.4225 34.001 35.3088C34.8914 36.3236 36.4358 36.4244 37.4506 35.534C38.4654 34.6437 38.5663 33.0992 37.6759 32.0844C35.1328 29.186 31.3912 27.3476 27.2232 27.3471L27.2245 27.3472L27.2218 29.7916V27.3471H27.2232C25.2429 27.3451 23.2852 27.767 21.4815 28.5844C19.6774 29.402 18.0693 30.5964 16.7652 32.0872C15.8764 33.1034 15.9796 34.6477 16.9958 35.5365C18.0119 36.4253 19.5562 36.3221 20.445 35.306C21.2896 34.3404 22.3311 33.5669 23.4996 33.0373ZM30.5556 40.3332C30.5556 42.0208 29.1875 43.3888 27.5 43.3888C25.8125 43.3888 24.4444 42.0208 24.4444 40.3332C24.4444 38.6457 25.8125 37.2777 27.5 37.2777C29.1875 37.2777 30.5556 38.6457 30.5556 40.3332Z"/></svg>
                <!-- Battery -->
                <svg width="19" height="13" viewBox="132.9 11.4 45.85 32.1" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" clip-rule="evenodd" d="M134.93 13.472C136.22 12.1827 137.968 11.4584 139.792 11.4584H167.292C169.115 11.4584 170.864 12.1827 172.153 13.472C173.442 14.7613 174.167 16.51 174.167 18.3334V18.7266C175.124 19.0652 176.004 19.615 176.736 20.347C178.026 21.6363 178.75 23.385 178.75 25.2084V29.7917C178.75 31.6151 178.026 33.3638 176.736 34.6531C176.004 35.385 175.124 35.9349 174.167 36.2735V36.6667C174.167 38.4901 173.442 40.2388 172.153 41.5281C170.864 42.8174 169.115 43.5417 167.292 43.5417H139.792C137.968 43.5417 136.22 42.8174 134.93 41.5281C133.641 40.2388 132.917 38.4901 132.917 36.6667V18.3334C132.917 16.51 133.641 14.7613 134.93 13.472ZM139.792 16.0417C139.184 16.0417 138.601 16.2832 138.171 16.7129C137.741 17.1427 137.5 17.7256 137.5 18.3334V36.6667C137.5 37.2745 137.741 37.8574 138.171 38.2872C138.601 38.7169 139.184 38.9584 139.792 38.9584H167.292C167.899 38.9584 168.482 38.7169 168.912 38.2872C169.342 37.8574 169.583 37.2745 169.583 36.6667V34.375C169.583 33.1094 170.609 32.0834 171.875 32.0834C172.483 32.0834 173.066 31.8419 173.495 31.4122C173.925 30.9824 174.167 30.3995 174.167 29.7917V25.2084C174.167 24.6006 173.925 24.0177 173.495 23.5879C173.066 23.1582 172.483 22.9167 171.875 22.9167C170.609 22.9167 169.583 21.8907 169.583 20.625V18.3334C169.583 17.7256 169.342 17.1427 168.912 16.7129C168.482 16.2832 167.899 16.0417 167.292 16.0417H139.792ZM144.375 20.625C145.641 20.625 146.667 21.6511 146.667 22.9167V32.0834C146.667 33.349 145.641 34.375 144.375 34.375C143.109 34.375 142.083 33.349 142.083 32.0834V22.9167C142.083 21.6511 143.109 20.625 144.375 20.625ZM153.542 20.625C154.807 20.625 155.833 21.6511 155.833 22.9167V32.0834C155.833 33.349 154.807 34.375 153.542 34.375C152.276 34.375 151.25 33.349 151.25 32.0834V22.9167C151.25 21.6511 152.276 20.625 153.542 20.625ZM162.708 20.625C163.974 20.625 165 21.6511 165 22.9167V32.0834C165 33.349 163.974 34.375 162.708 34.375C161.443 34.375 160.417 33.349 160.417 32.0834V22.9167C160.417 21.6511 161.443 20.625 162.708 20.625Z"/></svg>
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

    <!-- Figma export chrome (host page only; not serialized into the payload) -->
    <div class="figma-export-toolbar" data-figma-export-ignore>
        <span class="figma-export-toast" hidden></span>
        <button type="button" class="figma-export-btn" onclick="window.__copyDesignToFigma()">
            Copy to Figma
        </button>
    </div>

    <script>
    /*
     * Figma-ready SVG export
     *
     * Walks .device and emits real SVG primitives (rect, text, image, nested
     * <svg>, linearGradient, clipPath). Result is copied to the clipboard as
     * plain text — Figma's onPaste handler detects an SVG string and converts
     * it to editable vector layers (text stays text, shapes stay shapes).
     *
     * Coverage:
     *   - solid fills, linear gradients, borders, border-radius, opacity
     *   - text (multi-line via Range.getClientRects per line)
     *   - inline <svg> icons (embedded as nested <svg>, color inherited)
     *   - <img> (emitted as <image href="..."> — Figma may refuse remote URLs)
     *   - overflow clipping via <clipPath>
     * Not exported:
     *   - box-shadow, backdrop-filter, CSS filters, transforms
     *   - background-image (non-gradient), pseudo-elements (::before/::after)
     */
    (function () {
      var SVG_NS = 'http://www.w3.org/2000/svg';
      var defs = [];
      var defCounter = 0;

      function esc(s) {
        return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
      }

      function parseRgb(str) {
        if (!str || str === 'transparent' || str === 'rgba(0, 0, 0, 0)') return null;
        var m = str.match(/rgba?\(([^)]+)\)/);
        if (!m) return null;
        var p = m[1].split(',').map(function (s) { return parseFloat(s.trim()); });
        return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
      }

      function colorAttr(c) {
        return c ? 'rgb(' + Math.round(c.r) + ',' + Math.round(c.g) + ',' + Math.round(c.b) + ')' : 'none';
      }

      function num(v) { return Math.round(v * 100) / 100; }

      function gradientDef(bgImage) {
        if (!bgImage || bgImage === 'none') return null;
        var m = bgImage.match(/linear-gradient\(([\s\S]+)\)\s*$$/);
        if (!m) return null;
        var inner = m[1];
        var parts = [], depth = 0, start = 0;
        for (var i = 0; i <= inner.length; i++) {
          var ch = inner[i];
          if (ch === '(') depth++;
          else if (ch === ')') depth--;
          else if ((ch === ',' && depth === 0) || i === inner.length) {
            parts.push(inner.slice(start, i).trim());
            start = i + 1;
          }
        }
        var angle = 180;
        var stopParts = parts;
        var degMatch = parts[0] && parts[0].match(/^(-?\d+(?:\.\d+)?)deg$$/);
        if (degMatch) { angle = parseFloat(degMatch[1]); stopParts = parts.slice(1); }
        else if (parts[0] && /^to\s+/.test(parts[0])) {
          var dirs = { top: 0, right: 90, bottom: 180, left: 270,
                       'top right': 45, 'bottom right': 135, 'bottom left': 225, 'top left': 315 };
          var key = parts[0].replace(/^to\s+/, '').trim();
          angle = dirs[key] !== undefined ? dirs[key] : 180;
          stopParts = parts.slice(1);
        }
        var stops = stopParts.map(function (s, idx, arr) {
          var cm = s.match(/rgba?\([^)]+\)|#[0-9a-f]+|[a-z]+/i);
          var pm = s.match(/(\d+(?:\.\d+)?)%/);
          return {
            color: parseRgb(cm ? cm[0] : '#000') || { r: 0, g: 0, b: 0, a: 1 },
            pos: pm ? parseFloat(pm[1]) / 100 : (arr.length > 1 ? idx / (arr.length - 1) : 0)
          };
        });
        var rad = (angle - 90) * Math.PI / 180;
        var dx = Math.cos(rad) * 0.5, dy = Math.sin(rad) * 0.5;
        var id = 'fgmg' + (++defCounter);
        var stopXml = stops.map(function (s) {
          return '<stop offset="' + num(s.pos) + '" stop-color="' + colorAttr(s.color) + '" stop-opacity="' + s.color.a + '"/>';
        }).join('');
        defs.push('<linearGradient id="' + id + '" x1="' + num(0.5 - dx) + '" y1="' + num(0.5 - dy) +
                  '" x2="' + num(0.5 + dx) + '" y2="' + num(0.5 + dy) + '">' + stopXml + '</linearGradient>');
        return 'url(#' + id + ')';
      }

      function clipDef(x, y, w, h, rx) {
        var id = 'fgmc' + (++defCounter);
        defs.push('<clipPath id="' + id + '"><rect x="' + num(x) + '" y="' + num(y) +
                  '" width="' + num(w) + '" height="' + num(h) +
                  '" rx="' + num(rx) + '" ry="' + num(rx) + '"/></clipPath>');
        return id;
      }

      function lineRectsForText(textNode) {
        var text = textNode.textContent;
        if (!text.trim()) return [];
        var range = document.createRange();
        range.selectNodeContents(textNode);
        var rects = Array.prototype.slice.call(range.getClientRects());
        if (rects.length === 0) return [];
        if (rects.length === 1) return [{ text: text, rect: rects[0] }];
        var lines = [];
        var len = text.length;
        var offset = 0;
        for (var li = 0; li < rects.length; li++) {
          var targetTop = rects[li].top;
          while (offset < len && /\s/.test(text[offset])) offset++;
          var lo = offset, hi = len;
          while (lo < hi) {
            var mid = (lo + hi + 1) >> 1;
            range.setStart(textNode, offset);
            range.setEnd(textNode, mid);
            var rs = range.getClientRects();
            var lastTop = rs.length ? rs[rs.length - 1].top : targetTop;
            if (Math.abs(lastTop - targetTop) < 1) lo = mid;
            else hi = mid - 1;
          }
          var lineEnd = lo > offset ? lo : Math.min(offset + 1, len);
          var lineText = text.slice(offset, lineEnd);
          if (lineText.trim().length) lines.push({ text: lineText, rect: rects[li] });
          offset = lineEnd;
        }
        return lines;
      }

      function emitTextNode(textNode, ox, oy, out) {
        var parent = textNode.parentElement;
        if (!parent) return;
        var cs = getComputedStyle(parent);
        var color = parseRgb(cs.color);
        var family = (cs.fontFamily || '').replace(/"/g, "'");
        var size = parseFloat(cs.fontSize);
        var weight = cs.fontWeight;
        var align = cs.textAlign;
        var lines = lineRectsForText(textNode);
        for (var i = 0; i < lines.length; i++) {
          var ln = lines[i];
          var lx = ln.rect.left - ox;
          var ly = ln.rect.top - oy;
          var ty = ly + (ln.rect.height - size) / 2 + size * 0.82;
          var tx = lx;
          var anchor = 'start';
          if (align === 'center') { anchor = 'middle'; tx = lx + ln.rect.width / 2; }
          else if (align === 'right' || align === 'end') { anchor = 'end'; tx = lx + ln.rect.width; }
          out.push('<text x="' + num(tx) + '" y="' + num(ty) +
                   '" font-family="' + esc(family) +
                   '" font-size="' + num(size) +
                   '" font-weight="' + weight +
                   '" fill="' + colorAttr(color) +
                   (color && color.a < 1 ? '" fill-opacity="' + color.a : '') +
                   '" text-anchor="' + anchor +
                   '" xml:space="preserve">' + esc(ln.text) + '</text>');
        }
      }

      function emit(node, ox, oy, out) {
        if (node.nodeType === 3) { emitTextNode(node, ox, oy, out); return; }
        if (node.nodeType !== 1) return;
        if (node.dataset && 'figmaExportIgnore' in node.dataset) return;
        var cs = getComputedStyle(node);
        if (cs.display === 'none' || cs.visibility === 'hidden') return;
        var op = parseFloat(cs.opacity);
        if (op === 0) return;
        var tag = node.tagName.toLowerCase();
        var r = node.getBoundingClientRect();
        var x = r.left - ox, y = r.top - oy, w = r.width, h = r.height;
        if (w <= 0 || h <= 0) return;

        // CSS mask icon (e.g. Iconify SVG used as `mask` with a
        // `background-color` tint — the Android bottom nav uses this).
        // Figma's SVG paste can't read CSS `mask`, so without this the icon
        // appears as a solid filled rectangle. Pre-fetched SVG markup is
        // recolored with the element's background-color and inlined.
        var maskImg = (cs.maskImage && cs.maskImage !== 'none') ? cs.maskImage : cs.webkitMaskImage;
        var maskMatch = maskImg && maskImg.match(/url\((['"]?)([^'")]+)\1\)/);
        if (maskMatch && window.__figmaMaskCache && window.__figmaMaskCache[maskMatch[2]]) {
          var maskSvg = window.__figmaMaskCache[maskMatch[2]];
          var maskColor = parseRgb(cs.backgroundColor) || parseRgb(cs.color) || { r: 0, g: 0, b: 0, a: 1 };
          var maskColorVal = colorAttr(maskColor);
          var vbm = maskSvg.match(/viewBox\s*=\s*"([^"]+)"/i);
          var vb = vbm ? vbm[1].split(/\s+/).map(parseFloat) : [0, 0, 24, 24];
          var inner = maskSvg.replace(/^[\s\S]*?<svg[^>]*>/i, '').replace(/<\/svg>\s*$$/i, '');
          inner = inner.replace(/currentColor/g, maskColorVal);
          var msx = w / (vb[2] || 24), msy = h / (vb[3] || 24);
          if (op < 1) out.push('<g opacity="' + op + '">');
          out.push('<g transform="translate(' + num(x - vb[0] * msx) + ',' + num(y - vb[1] * msy) +
                   ') scale(' + num(msx) + ',' + num(msy) + ')" fill="' + maskColorVal +
                   '" fill-opacity="' + maskColor.a + '">' + inner + '</g>');
          if (op < 1) out.push('</g>');
          return;
        }

        if (tag === 'svg') {
          var color = parseRgb(cs.color);
          var colorVal = color ? colorAttr(color) : 'black';
          var markup = node.outerHTML.replace(
            /^<svg\b([^>]*)>/i,
            function (_m, attrs) {
              var stripped = attrs.replace(/\s(?:width|height)\s*=\s*"[^"]*"/gi, '');
              return '<svg width="' + num(w) + '" height="' + num(h) + '"' + stripped + '>';
            }
          ).replace(/currentColor/g, colorVal);
          if (op < 1) out.push('<g opacity="' + op + '">');
          out.push('<g transform="translate(' + num(x) + ',' + num(y) + ')">' + markup + '</g>');
          if (op < 1) out.push('</g>');
          return;
        }

        if (tag === 'img') {
          var src = node.currentSrc || node.src;
          out.push('<image x="' + num(x) + '" y="' + num(y) +
                   '" width="' + num(w) + '" height="' + num(h) +
                   '" href="' + esc(src) + '" preserveAspectRatio="xMidYMid slice"/>');
          return;
        }

        if (op < 1) out.push('<g opacity="' + op + '">');

        var bg = parseRgb(cs.backgroundColor);
        var grad = gradientDef(cs.backgroundImage);
        var borderW = parseFloat(cs.borderTopWidth) || 0;
        var borderC = borderW > 0 ? parseRgb(cs.borderTopColor) : null;
        var rx = parseFloat(cs.borderTopLeftRadius) || 0;
        rx = Math.min(rx, Math.min(w, h) / 2);
        if (grad || bg || (borderW && borderC)) {
          var fillVal = grad || (bg ? colorAttr(bg) : 'none');
          var fillOp = (!grad && bg) ? bg.a : 1;
          var strokeAttr = (borderW && borderC)
            ? ' stroke="' + colorAttr(borderC) + '" stroke-opacity="' + borderC.a + '" stroke-width="' + num(borderW) + '"'
            : '';
          out.push('<rect x="' + num(x) + '" y="' + num(y) +
                   '" width="' + num(w) + '" height="' + num(h) +
                   '" rx="' + num(rx) + '" ry="' + num(rx) +
                   '" fill="' + fillVal + '" fill-opacity="' + fillOp + '"' + strokeAttr + '/>');
        }

        var kids = Array.prototype.slice.call(node.childNodes);
        var ordered = kids.map(function (c, idx) {
          var z = 0;
          if (c.nodeType === 1) {
            var zs = getComputedStyle(c).zIndex;
            if (zs && zs !== 'auto') { var zn = parseInt(zs, 10); if (!isNaN(zn)) z = zn; }
          }
          return { node: c, idx: idx, z: z };
        });
        ordered.sort(function (a, b) { return (a.z - b.z) || (a.idx - b.idx); });
        var childOut = [];
        for (var i = 0; i < ordered.length; i++) {
          emit(ordered[i].node, ox, oy, childOut);
        }
        var needsClip = (cs.overflow === 'hidden' || cs.overflow === 'auto' || cs.overflow === 'scroll' || cs.overflowX === 'hidden' || cs.overflowY === 'hidden');
        if (needsClip && childOut.length) {
          var cid = clipDef(x, y, w, h, rx);
          out.push('<g clip-path="url(#' + cid + ')">');
          out.push(childOut.join(''));
          out.push('</g>');
        } else {
          out.push(childOut.join(''));
        }

        if (op < 1) out.push('</g>');
      }

      function showToast(msg, isError) {
        var t = document.querySelector('.figma-export-toast');
        if (!t) return;
        t.textContent = msg;
        t.hidden = false;
        t.style.color = isError ? '#ff9f9f' : '#fff';
        clearTimeout(showToast._timer);
        showToast._timer = setTimeout(function () { t.hidden = true; }, 2500);
      }

      window.__copyDesignToFigma = async function () {
        try {
          defs = [];
          defCounter = 0;
          var root = document.querySelector('.device');
          if (!root) { showToast('No .device frame found', true); return; }
          // Pre-fetch CSS mask SVG icons so emit() can inline them
          // synchronously. Each cached entry maps mask url -> raw SVG text.
          var maskUrls = {};
          root.querySelectorAll('*').forEach(function (n) {
            var s = getComputedStyle(n);
            var mi = (s.maskImage && s.maskImage !== 'none') ? s.maskImage : s.webkitMaskImage;
            var m = mi && mi.match(/url\((['"]?)([^'")]+)\1\)/);
            if (m) maskUrls[m[2]] = true;
          });
          var maskCache = {};
          await Promise.all(Object.keys(maskUrls).map(function (u) {
            return fetch(u).then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
              .then(function (t) { maskCache[u] = t; })
              .catch(function () { maskCache[u] = null; });
          }));
          window.__figmaMaskCache = maskCache;
          var r = root.getBoundingClientRect();
          var out = [];
          emit(root, r.left, r.top, out);
          var svg = '<svg xmlns="' + SVG_NS + '" width="' + num(r.width) + '" height="' + num(r.height) +
                    '" viewBox="0 0 ' + num(r.width) + ' ' + num(r.height) + '">' +
                    (defs.length ? '<defs>' + defs.join('') + '</defs>' : '') +
                    out.join('') +
                    '</svg>';
          await navigator.clipboard.writeText(svg);
          showToast('Copied — paste into Figma (Cmd+V)');
        } catch (err) {
          console.error('[figma-export]', err);
          showToast('Clipboard blocked — serve over http(s) or grant permission', true);
        }
      };
    })();
    </script>
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
