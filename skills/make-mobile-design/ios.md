# iOS Design Rules

Load this file when the target platform is iOS. Mirrors `android.md` in shape. Content was extracted from `SKILL.md` during the iOS/Android split.


When the target platform is iOS (or unspecified, since this skill is mobile-first), apply Apple Human Interface Guidelines. These rules override stylistic preferences -- treat them as non-negotiable for iOS mockups.

### Core Principles (Apple HIG)

1. **Clarity**: Every element is easily understood. Minimalist layout, straightforward navigation.
2. **Deference**: UI minimizes distractions. Content takes center stage, chrome recedes.
3. **Depth**: Visual layers communicate hierarchy through translucency, blur, and motion.
4. **Consistency**: Familiar patterns -- don't reinvent native controls.

### Typography

Default to the San Francisco family on iOS mockups:
- Use `font-family: -apple-system, "SF Pro Text", "SF Pro Display", system-ui, sans-serif;`
- Body and labels at 13--19px use SF Pro Text proportions; titles at 20px+ use SF Pro Display proportions (the system font handles this automatically via `-apple-system`).
- Avoid custom webfonts unless brand-critical. If a custom font is required, pair it with `-apple-system` as fallback.
- Respect Dynamic Type spirit: do not lock font sizes in absolute `px` for body text where `rem`/`em` can scale.

#### iOS HIG Type Ramp (use these tokens, not web-style sizes)

**Body is 17px on iOS.** Web defaults of 14--15px will make the screen feel like a webpage. Use the tokens from `01-base-tokens.md`:

| Token | Size | Use |
|---|---|---|
| `--text-largetitle` | 34px | Large title at top of scroll (primary screens) |
| `--text-title1` | 28px | Title 1 |
| `--text-title2` | 22px | Title 2 (sheet headers) |
| `--text-title3` | 20px | Title 3 (card titles) |
| `--text-body` | **17px** | Body, list rows, button labels — **default** |
| `--text-callout` | 16px | Callout |
| `--text-subheadline` | 15px | Subheadline |
| `--text-footnote` | 13px | Footnote, list meta, grouped-list section headers |
| `--text-caption1` | 12px | Caption |
| `--text-caption2` | 11px | Tab bar labels, fine print |

Anything below 13px is for legal copy, captions, or tab-bar labels only. Never set body or list-row text below 15px.

### iOS Density & Layout

iOS screens favour **content-first hierarchy and whitespace**. The most common failure mode is treating the device frame like a webpage and packing it with sections, rows, and CTAs.

- **One screen, one job.** Aim for **3–5 distinct sections** above the fold. If a screen has more, split it.
- **Default content insets:** `16px` horizontal, `24–32px` between sections.
- **Large-title nav pattern** for primary tabs/screens: a 34pt title sits at the top of the scroll region (not pinned), with a single search bar or short subtitle underneath.
- **Lists are grouped or inset-grouped:** wrap row groups in one rounded card with 16px outer margin and dividers between rows. Do not put a card around every individual row.
- **Whitespace is a feature, not a gap to fill.** Do **not** add filler rows just so the content scrolls.
- **Buttons:** primary action is a 50px-tall pill or 44px filled rect; label at 17pt semibold.
- **Touch targets:** minimum 44×44px.

### Color Palette

**CRITICAL: Never use purple as a primary, accent, or gradient color. No purple gradients. No purple tints on glass.**

Preferred accent colors:
- **Blue** -- trust, productivity, communication (default iOS accent)
- **Green** -- health, success, nature
- **Orange** -- energy, creativity, warmth
- **Red** -- alerts, importance (use sparingly)
- **Teal / Cyan** -- modern, fresh, technical
- **Indigo** -- depth without purple (use carefully, never drift toward violet)

Use semantic tokens that adapt to light/dark mode (`--color-text-primary`, `--color-bg-secondary`, etc. from `01-base-tokens.md`). Avoid hardcoded greys.

### Liquid Glass (iOS 26)

Liquid Glass is Apple's translucent material for the navigation layer floating above content. **The full recipe — SVG `<defs>`, CSS, dark mode, reduced-transparency fallback — lives in [components/ios/00-liquid-glass.md](components/ios/00-liquid-glass.md). Always load that file before emitting any `.glass` element.** Every glass surface in this skill uses that recipe; do not invent ad-hoc `backdrop-filter` formulas.

Glass rules:
- Apply glass to **navigation layer only** (tab bars, nav headers, floating toolbars, FABs). Never on content cards, list rows, or media tiles.
- Glass elements **float above** content; never stack glass on glass.
- Capsule (`border-radius: 9999px`) or fully rounded (16--24px) shapes only.
- Tint subtly using accent color at low opacity (e.g. `rgba(0, 122, 255, 0.18)`). Never purple.
- For media-rich backgrounds, drop the white fill and rely on the filter alone (the "clear" variant).

### Motion

- Spring-feel transitions: 0.3--0.45s with `cubic-bezier(0.34, 1.56, 0.64, 1)` for bouncy, or `cubic-bezier(0.25, 0.1, 0.25, 1)` for smooth.
- Micro-interactions (hover, tap, toggle) under 0.2s.
- Respect reduced motion: wrap non-essential animations in `@media (prefers-reduced-motion: no-preference)`.

### Forbidden Patterns

NEVER produce iOS mockups with:
- Purple as primary, accent, gradient, or glass tint.
- Custom navigation bars that replace the native large-title pattern when a native pattern fits.
- Skeuomorphic textures, heavy drop shadows, or beveled edges.
- Cluttered layouts that violate content-first hierarchy.
- Glass effects on content surfaces (lists, cards, media tiles, modals body).
- Animations longer than 0.5s for micro-interactions.
- Touch targets smaller than 44x44px.

### Accessibility

- Body text contrast ratio >= 4.5:1; large text >= 3:1.
- Every interactive element gets a visible focus / pressed state.
- Use `aria-label` on icon-only buttons.
- Honor `prefers-color-scheme` and `prefers-reduced-motion`.

### Compliance Check

Before delivering an iOS mockup, verify:
- [ ] No purple anywhere (text, accent, gradient, glass tint, illustration).
- [ ] System font stack used for typography (no Inter / Roboto / Google Fonts on iOS).
- [ ] Body, list rows, and button labels render at 17px (`--text-body`); section headers at 13px (`--text-footnote`); tab bar labels at 11px (`--text-caption2`).
- [ ] Screen has 3–5 sections max with generous whitespace; no filler rows added just to enable scrolling.
- [ ] Glass only on nav layer, not on content.
- [ ] All touch targets >= 44x44px.
- [ ] Light/dark mode tokens, not hardcoded colors.
- [ ] Animations respect `prefers-reduced-motion`.
- [ ] Screen was generated by running `create_ios_template.py`; content lives inside `.device-content`; status bar is pinned and does not scroll with content.
- [ ] Any floating overlay over `.device-content` (custom tab bar, FAB, banner) uses `pointer-events: none` on the wrapper with `pointer-events: auto` on interactive children; the screen scrolls anywhere inside the device frame, including over the overlay.
- [ ] `.device-content { padding-top: 0 }` (scaffold default — never overridden to 59px). The first child of `.device-content` owns the 59px status-bar safe area via its own `padding-top: calc(59px + …)`. Verified by scrolling — top nav (if any) stays pinned at y=0 and its background fills behind the status bar, OR for transparent/full-bleed first child, scrolled content reaches the top edge.

For Android mockups, load `android.md` instead — it carries the Material 3 equivalent of this ruleset. The no-purple guideline applies only to iOS; Android may use purple when the brand calls for it (MD3's default Baseline scheme is built around purple-violet).

---

## Tablet (iPadOS)

Apply this section **in addition to** the phone rules above when
form-factor = tablet. Phone rules (no purple, system font stack,
content-first layout, etc.) still hold — tablet adds layout and chrome
expectations specific to the regular size class.

### Size Class & Orientation

- **Regular-regular by default in landscape.** The iPad scaffold is
  1194×834 landscape; portrait (834×1194) is opt-in via
  `--orientation portrait`.
- Design for landscape first — most iPad apps are used in landscape with
  a Magic Keyboard / Smart Folio.
- A landscape iPad is a *regular-width* container: persistent sidebars,
  multi-column layouts, and pointer-friendly hover states all apply.

### Navigation

- **Persistent sidebar** is the canonical primary-nav pattern. Use the
  `.split-view` wrapper from `components/ios/13-tablet-layouts.md`. The
  sidebar replaces the iPhone tab bar — do **not** stack both on an iPad
  screen.
- **Top toolbar** (the `.nav-header` from `03-navigation.md`) lives
  inside the detail pane, not above the whole frame. The sidebar gets
  its own header (Mailboxes, Folders, Settings, …).
- **Three-column** (`sidebar + supplemental + detail`) is allowed for
  hierarchical content. Skip it when the middle column would be a
  near-empty list — collapse to two-pane.
- Bottom tab bar / `add_ios_tabbar.py` is **not blocked** on iPad, but
  it is discouraged. Sidebar is the idiomatic choice.

### Liquid Glass on iPad

Glass is sanctioned on iPad navigation chrome (sidebar background, top
toolbar). Reuse the recipe from `components/ios/00-liquid-glass.md` —
**do not invent iPad-specific variants**. Apply glass on the sidebar
only when the detail pane has full-bleed media; otherwise stay on
`--gray-50`.

### Type Ramp

- Same SF Pro stack and `--text-*` tokens as phone.
- Large-title may scale from 34pt to **40pt** in regular width when the
  screen has the room (Mail, Settings on iPad). This is the only
  HIG-sanctioned size deviation.
- Body, list rows, and button labels remain 17px.

### Density & Layout

- Sidebar width: **320pt** minimum, 375pt acceptable for content-rich
  sidebars. Supplemental column: 320pt.
- Outer content insets bump from 16pt (phone) to **24pt** on iPad detail
  panes for breathing room.
- Lists in the sidebar stay full-width (no inset cards). Lists in the
  detail pane keep the inset-grouped pattern.

### Compliance Check (Tablet additions)

Append to the phone checklist:

- [ ] Screen was generated by `create_ipad_template.py` (not the iPhone
      scaffold). Frame is 1194×834 landscape (or 834×1194 portrait).
- [ ] When primary nav has more than 4 destinations, a persistent
      sidebar (`.split-view`) is present. No bottom tab bar competes
      with it.
- [ ] Sidebar width is 320–375pt; supplemental column (if present) is
      320pt; detail pane is flex 1.
- [ ] Status-bar safe area (24px on iPad — not 59px) is absorbed by the
      first child of each scrolling pane, never by `.device-content`.
- [ ] No purple anywhere — the no-purple rule applies to iPad just as
      to iPhone.
- [ ] Generated tablet file's Copy-to-Figma button has been smoke-tested
      and produces an SVG that pastes into Figma without serializer
      errors.
