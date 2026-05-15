# Android Design Rules

Load this file when the target platform is Android. Mirrors `ios.md` in shape. Apply Material 3 (the **Material 3 Expressive** language as of 2024+) — these rules override stylistic preferences for Android mockups.

## Core Principles (Material 3 Expressive)

1. **Personal** — Dynamic color, brand-driven palettes. The UI reflects a user/brand identity through color roles, not chrome.
2. **Bold** — Strong typography (display scales up to 57px), expressive shape variety (none → full-pill).
3. **Productive** — Surface roles and elevation overlays communicate hierarchy clearly without ornament.
4. **Consistent** — Use MD3 components as defined. Do not reinvent the switch, FAB, or bottom nav.

## Typography

Default to **Roboto Flex** (loaded via Google Fonts in the scaffold). Roboto Mono is the default mono companion. Brand-suggestion flow may swap these — keep the CSS variable name, just change its value.

- Font stack: `"Roboto Flex", "Roboto", "Google Sans", system-ui, -apple-system, sans-serif`
- Unlike iOS, custom Google webfonts are encouraged on Android.

### MD3 Type Scale

**Body is 16px on Android** (vs iOS body at 17px). Use the tokens from `components/android/01-base-tokens.md`:

| Token | Size / Weight | Use |
|---|---|---|
| `--md-sys-typescale-display-large` | 57/400 | Marketing hero only |
| `--md-sys-typescale-display-medium` | 45/400 | Onboarding heroes |
| `--md-sys-typescale-display-small` | 36/400 | Empty-state heroes |
| `--md-sys-typescale-headline-large` | 32/400 | Large-screen headlines |
| `--md-sys-typescale-headline-medium` | 28/400 | Section headlines, large top app bar title |
| `--md-sys-typescale-headline-small` | 24/400 | Medium top app bar title, dialog title |
| `--md-sys-typescale-title-large` | 22/400 | Small top app bar title, card title |
| `--md-sys-typescale-title-medium` | 16/500 | List-item primary, dialog headings |
| `--md-sys-typescale-title-small` | 14/500 | Tabs, dense labels |
| `--md-sys-typescale-body-large` | **16/400** | **Body, default** |
| `--md-sys-typescale-body-medium` | 14/400 | Supporting text, list-item secondary |
| `--md-sys-typescale-body-small` | 12/400 | Captions, metadata |
| `--md-sys-typescale-label-large` | 14/500 | Button labels |
| `--md-sys-typescale-label-medium` | 12/500 | Bottom-nav labels, chip text |
| `--md-sys-typescale-label-small` | 11/500 | Tiny status labels |

Never set body or list-row text below 14px. Bottom-nav labels are 12px; never go smaller.

## Density & Layout

- **Default content insets:** 16dp horizontal, 16–24dp between sections.
- **Top app bar** is the canonical top chrome. Pick small (64dp), center (64dp), medium (112dp), or large (152dp) per `03-navigation.md`.
- **Bottom navigation bar** for primary destinations (3–5 items, 80dp tall). The active item shows a pill-shaped `secondary-container` indicator behind its icon — this is the signature MD3 pattern.
- **Cards** are 12dp corner by default. Pick one variant per group (elevated / filled / outlined).
- **Lists** use 56dp (one-line), 72dp (two-line), or 88dp (three-line) heights. Leading slot is 24dp icon or 40dp avatar.
- **Buttons** are 40dp tall (filled / tonal / outlined / elevated / text). Icon buttons are 40dp circles.
- **Touch targets:** minimum **48×48dp** (vs iOS 44×44).

## Color

MD3 baseline palette is purple-violet — that's the default and a defining MD3 trait. **Purple is allowed on Android** (unlike iOS, where it's forbidden). Override the palette via `design-system.html` when the brand calls for it.

Use semantic MD3 color roles (`--md-sys-color-primary`, `--md-sys-color-surface-container`, etc. from `components/android/01-base-tokens.md`). Do NOT hardcode hex values.

Honor `prefers-color-scheme: dark` — the scaffold ships a complete dark palette under that media query.

## Shape

MD3 uses corner-shape tokens (none / extra-small / small / medium / large / extra-large / full). Defaults:

- Cards: `corner-medium` (12dp)
- Top of bottom sheets, drawers: `corner-large` (16dp)
- Dialogs, large FAB: `corner-extra-large` (28dp)
- Chips, pills, full FAB extended: `corner-full`

Do not mix shapes randomly. Pick a corner family per component class and stick to it.

## Elevation

MD3 expresses depth through **tonal surface overlays** (a surface-tint blended in at increasing opacity per level) combined with a soft shadow. Use:

- `surface-container-lowest` → `surface-container-highest` for the **color** part.
- `--md-sys-elevation-level0..5` for the **shadow** part.

**No frosted glass.** MD3 does not use `backdrop-filter`. Do not import the iOS Liquid Glass recipe on Android — it'll look wrong.

## Motion

| Curve | Duration | Use |
|---|---|---|
| `easing-standard` | `duration-short3..short4` (150–200ms) | Default property changes (button hover, ripple). |
| `easing-emphasized` | `duration-medium2..medium4` (300–400ms) | Container transforms, sheet open/close. |
| `easing-emphasized-decelerate` | `duration-medium2..medium4` | Items arriving on screen. |
| `easing-emphasized-accelerate` | `duration-short3..short4` | Items leaving the screen. |

Respect `prefers-reduced-motion` — wrap non-essential animations.

## Forbidden Patterns

NEVER produce Android mockups with:

- iOS large-title nav pattern (34px headline above pinned status bar). Use MD3 top app bar variants instead.
- Apple system font stack (`-apple-system`). Use Roboto Flex.
- Liquid Glass / `backdrop-filter` recipes. Use MD3 surface-container tones.
- iOS switch geometry (small thumb, narrow track). Use the wide-track MD3 switch.
- iOS-style 11px tab-bar labels. MD3 nav-bar labels are 12px.
- 44×44 touch targets. Android requires 48×48.
- Inset-grouped list cards. MD3 uses full-bleed list items inside a surface.

## Accessibility

- Body text contrast ratio >= 4.5:1; large text >= 3:1.
- Every interactive element gets a visible focus / pressed state (color-mix overlays at 8%/12% opacity per MD3 state layer spec).
- Use `aria-label` on icon-only buttons.
- Honor `prefers-color-scheme` and `prefers-reduced-motion`.
- 48dp minimum tap target.

## Compliance Check

Before delivering an Android mockup, verify:

- [ ] Screen was generated by running `create_android_template.py`; content lives inside `.device-content`; status bar is pinned at 24dp and does not scroll with content.
- [ ] Roboto Flex loaded from Google Fonts; no `-apple-system` in the font stack.
- [ ] Body, list rows render at 16px (`--md-sys-typescale-body-large`); section headers at 14px (`title-small`); bottom-nav labels at 12px (`label-medium`).
- [ ] Touch targets ≥ 48×48dp.
- [ ] No `backdrop-filter` / glass surfaces — depth comes from `surface-container-*` tones + elevation shadows.
- [ ] Bottom navigation bar (if present) uses the pill `secondary-container` active indicator with always-visible labels.
- [ ] Top app bar is one of the four MD3 variants (small / center / medium / large) and is `position: sticky; top: 0` under the status bar.
- [ ] MD3 corner tokens used per component family (12dp cards, 28dp dialogs, full pills for chips/FAB-extended).
- [ ] Light/dark mode tokens (`--md-sys-color-*`), not hardcoded colors.
- [ ] Animations respect `prefers-reduced-motion`.
- [ ] `.device-content { padding-top: 0 }` (scaffold default — never overridden to 24px). The first child owns the 24dp status-bar safe area via its own `padding-top: calc(24px + …)`.
- [ ] Any floating overlay over `.device-content` (custom bottom nav, FAB, snackbar) uses `pointer-events: none` on the wrapper with `pointer-events: auto` on interactive children.

For iOS mockups, load `ios.md` instead.

---

## Tablet (MD3 Expanded Window Class)

Apply this section **in addition to** the phone rules above when
form-factor = tablet. Phone rules (Roboto Flex, MD3 surface roles, 48dp
touch targets, no `backdrop-filter`) still hold — tablet adds the
expanded-class layout and chrome expectations.

Reference: `m3.material.io/foundations/layout/applying-layout/window-size-classes`.

### Window Size Class & Orientation

- Pixel Tablet scaffold defaults to **1280×800 dp landscape** (expanded
  window class). `--orientation portrait` flips to 800×1280 dp.
- Design for landscape first — that's how the docked Pixel Tablet is
  used most.

### Navigation

- **Navigation rail** (`components/android/09-navigation-drawer.md` §A23)
  replaces the bottom navigation bar at expanded class when global nav
  has 3–7 destinations.
- **Standard navigation drawer** (always visible, 360dp wide) replaces
  the rail when destinations exceed 7 or the app needs section headers
  inside the nav.
- **Modal navigation drawer** is OK on tablet too, but reserve it for
  rarely-accessed secondary nav.
- Bottom navigation bar / `add_android_navbar.py` is **not blocked** on
  tablet, but it is discouraged. Rail / drawer is the idiomatic choice
  per MD3.

### Layout Patterns

- **`.list-detail`** (`components/android/10-tablet-layouts.md` §A24b)
  is the canonical two-pane layout: 360dp list pane + flex detail pane,
  separated by 24dp gap, sitting on 24dp screen padding.
- **`.three-column-md`** for hierarchical content (e.g. accounts →
  folders → messages). Use only when each column has real content.
- The top app bar (any of small/center/medium/large) sits **inside**
  `.tablet-content`, above the panes — not above the nav rail.

### Density & Layout

- **Screen margins:** 24dp on expanded class (vs 16dp on compact/phone).
- **Pane gap:** 24dp between list and detail.
- **Pane radius:** large (16dp) corner radius via
  `--md-sys-shape-corner-large` — the two panes are visually distinct
  surface containers, not a flat split.

### Type Scale

- Same Roboto Flex stack and MD3 type tokens as phone.
- Large-screen headlines may bump from `headline-medium` (28) to
  `headline-large` (32) when the screen has a Large top app bar — MD3
  permits this at expanded class.
- Body, list rows remain 16px (`body-large`).

### Surface Roles

- List pane: `surface-container-low`.
- Detail pane: `surface-container-lowest` (or invert).
- Nav rail: `surface` with no fill (transparent over the page surface).
- Always-visible drawer: `surface-container-low`.

The two-tone treatment is the MD3 hint that panes are independent scroll
regions — keep it. Do **not** use `backdrop-filter` to differentiate
them.

### Compliance Check (Tablet additions)

Append to the phone checklist:

- [ ] Screen was generated by `create_android_tablet_template.py` (not
      the Pixel 8 phone scaffold). Frame is 1280×800 landscape (or
      800×1280 portrait).
- [ ] When global nav is present, a navigation rail or standard
      navigation drawer is used — not a bottom navigation bar.
- [ ] Screen padding is 24dp; pane gap is 24dp; list pane is 360dp.
- [ ] List and detail panes use distinct `surface-container-*` tones,
      not `backdrop-filter`.
- [ ] Status-bar safe area (24dp) is absorbed by the first child of each
      scrolling pane, never by `.device-content`.
- [ ] Generated tablet file's Copy-to-Figma button has been smoke-tested
      and produces an SVG that pastes into Figma without serializer
      errors.
