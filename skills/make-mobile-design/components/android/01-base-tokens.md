# A1. Material 3 Design Tokens

The canonical source of MD3 tokens for Android mockups. The Android scaffold (`scripts/create_android_template.py`) inlines these into every generated file; redefine them via `design-system.html` to apply a brand palette.

**Always load this file when target = Android.** Mirrors `components/ios/01-base-tokens.md` in role.

## Color (MD3 Baseline — Light)

| Token | Hex | Use |
|---|---|---|
| `--md-sys-color-primary` | `#6750A4` | Primary actions (filled buttons, FAB, active indicators). |
| `--md-sys-color-on-primary` | `#FFFFFF` | Content drawn on top of `primary`. |
| `--md-sys-color-primary-container` | `#EADDFF` | Tonal container backgrounds (tonal buttons, nav-bar pill). |
| `--md-sys-color-on-primary-container` | `#4F378B` | Content on `primary-container`. |
| `--md-sys-color-secondary` | `#625B71` | Secondary accents. |
| `--md-sys-color-secondary-container` | `#E8DEF8` | Bottom-nav active pill background. |
| `--md-sys-color-tertiary` | `#7D5260` | Tertiary accent (rare). |
| `--md-sys-color-error` | `#B3261E` | Errors. |
| `--md-sys-color-background` | `#FEF7FF` | Screen base. |
| `--md-sys-color-surface` | `#FEF7FF` | Default surface (cards, sheets). |
| `--md-sys-color-surface-variant` | `#E7E0EC` | Lower-emphasis surfaces (chips, dividers). |
| `--md-sys-color-on-surface` | `#1D1B20` | Body text. |
| `--md-sys-color-on-surface-variant` | `#49454F` | Secondary text, inactive icons. |
| `--md-sys-color-outline` | `#79747E` | Borders for outlined buttons / cards. |
| `--md-sys-color-outline-variant` | `#CAC4D0` | Subtle dividers. |
| `--md-sys-color-surface-container-lowest` | `#FFFFFF` | Lowest tonal step. |
| `--md-sys-color-surface-container-low` | `#F7F2FA` | |
| `--md-sys-color-surface-container` | `#F3EDF7` | Default elevated container fill. |
| `--md-sys-color-surface-container-high` | `#ECE6F0` | Dialogs, menus. |
| `--md-sys-color-surface-container-highest` | `#E6E0E9` | Top app bar (scrolled state). |
| `--md-sys-color-surface-tint` | same as primary | Tonal overlay layered onto elevated surfaces. |

Dark variants are defined in the scaffold under `@media (prefers-color-scheme: dark)`. Honor `prefers-color-scheme` — do not hardcode colors.

**MD3 uses purple-violet by default.** Unlike iOS, purple is allowed (in fact, central) on Android. Override the palette via `design-system.html` when the brand says otherwise.

## Typography — MD3 Type Scale

Roboto Flex is the default font (loaded from Google Fonts in the scaffold). Use Roboto Mono for code/numerics; pair with another Google font if the brand calls for it.

| Token | Size | Weight (default) | Use |
|---|---|---|---|
| `--md-sys-typescale-display-large` | 57px | 400 | Marketing hero text only (rarely used in-app). |
| `--md-sys-typescale-display-medium` | 45px | 400 | Onboarding heroes. |
| `--md-sys-typescale-display-small` | 36px | 400 | Empty-state heroes. |
| `--md-sys-typescale-headline-large` | 32px | 400 | Large screen headlines. |
| `--md-sys-typescale-headline-medium` | 28px | 400 | Section headlines, large top app bar title. |
| `--md-sys-typescale-headline-small` | 24px | 400 | Medium top app bar title. |
| `--md-sys-typescale-title-large` | 22px | 400 | Small top app bar title, card titles. |
| `--md-sys-typescale-title-medium` | 16px | 500 | List-item primary, dialog title. |
| `--md-sys-typescale-title-small` | 14px | 500 | Tabs, dense labels. |
| `--md-sys-typescale-body-large` | 16px | 400 | **Default body.** |
| `--md-sys-typescale-body-medium` | 14px | 400 | Supporting text, list-item secondary. |
| `--md-sys-typescale-body-small` | 12px | 400 | Captions, metadata. |
| `--md-sys-typescale-label-large` | 14px | 500 | Button labels. |
| `--md-sys-typescale-label-medium` | 12px | 500 | Bottom-nav labels, chip text. |
| `--md-sys-typescale-label-small` | 11px | 500 | Tiny status indicators. |

**Body is 16px on Android** (vs 17px on iOS). Bottom-nav labels are 12sp/12px — never go below that for primary navigation.

## Shape — Corner Tokens

| Token | Value | Used by |
|---|---|---|
| `--md-sys-shape-corner-none` | 0 | Edge-to-edge media. |
| `--md-sys-shape-corner-extra-small` | 4px | Snackbars. |
| `--md-sys-shape-corner-small` | 8px | Small components (chip, switch track). |
| `--md-sys-shape-corner-medium` | 12px | Cards (default), text fields. |
| `--md-sys-shape-corner-large` | 16px | Top of bottom sheets, navigation drawer. |
| `--md-sys-shape-corner-extra-large` | 28px | Dialogs, large FAB, M3-Expressive cards. |
| `--md-sys-shape-corner-full` | 9999px | Pills (chips, search bar, FAB extended, nav-bar active indicator). |

## Elevation — Tonal Overlay + Shadow

MD3 expresses depth through **tonal surface overlays** (a surface tint applied at increasing opacity) combined with a soft shadow. Use these tokens for `box-shadow`; layer surface-tint via `background-color` set to one of the `surface-container-*` steps that matches the level.

| Token | Use |
|---|---|
| `--md-sys-elevation-level0` | Resting surfaces, content. |
| `--md-sys-elevation-level1` | Elevated cards at rest, search bar. |
| `--md-sys-elevation-level2` | Top app bar (scrolled), elevated bottom nav. |
| `--md-sys-elevation-level3` | FAB, menus. |
| `--md-sys-elevation-level4` | Picked-up draggable items. |
| `--md-sys-elevation-level5` | Modal dialogs. |

**Do not use frosted-glass `backdrop-filter` on Android.** MD3 does not use Apple-style glass. Express depth via tonal containers + the elevation tokens above.

## Motion

| Token | Curve / Duration | Use |
|---|---|---|
| `--md-sys-motion-easing-standard` | `cubic-bezier(0.2, 0, 0, 1)` | Default for property changes. |
| `--md-sys-motion-easing-emphasized` | `cubic-bezier(0.2, 0, 0, 1)` | Hero transitions. |
| `--md-sys-motion-easing-emphasized-decelerate` | `cubic-bezier(0.05, 0.7, 0.1, 1)` | Enter (items arriving). |
| `--md-sys-motion-easing-emphasized-accelerate` | `cubic-bezier(0.3, 0, 0.8, 0.15)` | Exit (items leaving). |
| `--md-sys-motion-duration-short2..short4` | 100/150/200ms | Micro-interactions (ripple, state change). |
| `--md-sys-motion-duration-medium2..medium4` | 300/350/400ms | Container transforms, sheet open/close. |
| `--md-sys-motion-duration-long1..long2` | 450/500ms | Cross-screen hero transitions. |

Respect `prefers-reduced-motion` — wrap non-essential animations in `@media (prefers-reduced-motion: no-preference)`.

## Font Stack

```css
--font-roboto: "Roboto Flex", "Roboto", "Google Sans", system-ui, -apple-system, sans-serif;
--font-mono:   "Roboto Mono", ui-monospace, "SF Mono", Menlo, monospace;
```

Scaffold loads Roboto Flex + Roboto Mono via Google Fonts. The brand-suggestion flow may swap these — keep the variable name; just change its value.

## Do / Don't

| Do | Don't |
|---|---|
| Load this file before any Android component. | Mix iOS HIG tokens (`--text-body`, `--color-bg`) on Android. |
| Reference tokens by name in every component. | Hardcode hex colors or px sizes. |
| Use `surface-container-*` for elevated fills. | Apply `backdrop-filter` to fake MD3 elevation. |
| Honor `prefers-color-scheme`. | Hardcode dark-mode colors. |
| Use 48dp minimum touch targets. | Use 44px (that's iOS). |
