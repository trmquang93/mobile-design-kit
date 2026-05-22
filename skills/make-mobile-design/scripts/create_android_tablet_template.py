#!/usr/bin/env python3
"""Generate a standalone HTML Pixel Tablet device template — Material 3
expanded window class. 24dp status bar, gesture-navigation pill, no
hole-punch camera (the Pixel Tablet has a bezel camera).

Usage:
    python3 create_android_tablet_template.py <output.html>
        [--title "Screen Name"] [--orientation landscape|portrait]

Defaults:
    landscape (1280 x 800 dp). --orientation portrait flips to 800 x 1280 dp.

The device chrome and Copy-to-Figma serializer come from shared asset
files referenced via absolute file:// URLs (see ../assets/).
"""

import argparse
import sys
from pathlib import Path
from string import Template

from _shared_template import asset_link, asset_script

TEMPLATE = Template(r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>$title</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Flex:opsz,wght@8..144,300..900&family=Roboto+Mono:wght@400;500&display=swap">
    $chrome_css
    $platform_css
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

            /* MD3 type scale */
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

            /* MD3 tonal elevation */
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
    </style>
</head>
<body>
    <div class="device" data-platform="android" data-form-factor="tablet"
         style="--device-w: ${width}px; --device-h: ${height}px; --device-radius: 28px;">
        <!-- Pixel Tablet camera lives in the bezel — no on-surface hole-punch. -->

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

    $figma_script
</body>
</html>
""")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a Pixel Tablet (Android Material 3, expanded window class) device template HTML file."
    )
    parser.add_argument("output", help="Output HTML file path")
    parser.add_argument("--title", default="Tablet Screen", help="Page title (default: 'Tablet Screen')")
    parser.add_argument(
        "--orientation", choices=("landscape", "portrait"), default="landscape",
        help="Frame orientation (default: landscape, 1280×800 dp)",
    )
    args = parser.parse_args()

    out_path = Path(args.output)
    if not out_path.parent.exists():
        print(f"Error: parent directory does not exist: {out_path.parent}", file=sys.stderr)
        return 1

    width, height = (1280, 800) if args.orientation == "landscape" else (800, 1280)

    html = TEMPLATE.substitute(
        title=args.title,
        width=width,
        height=height,
        chrome_css=asset_link("device-chrome.css", out_path),
        platform_css=asset_link("device-android.css", out_path),
        figma_script=asset_script("figma-export.js", out_path),
    )
    out_path.write_text(html, encoding="utf-8")
    print(f"Created Pixel Tablet device template ({args.orientation}, {width}×{height} dp): {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
