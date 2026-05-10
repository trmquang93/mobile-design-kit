---
name: make-mobile-design
description: Design mobile app screens as HTML mockups with a reusable design system. Use when the user asks to "design a screen", "create a mobile mockup", "make mobile design", "build a mobile UI", or wants to convert a description/screenshot into an interactive HTML prototype.
argument-hint: "[screen-name or description]"
---

# Mobile Design Skill

Generate production-quality, mobile-first HTML mockups for app screens. Maintain a reusable design system and produce interactive prototypes that look and feel like real mobile apps.

## Components Library

Components are split into smaller files under [components/](components/). The index at [components.md](components.md) lists all files and when to load each one.

**IMPORTANT:** Before generating any screen:
1. **Always** read [components/01-base-tokens.md](components/01-base-tokens.md) and [components/02-status-bar.md](components/02-status-bar.md)
2. Read additional component files based on what the screen needs (nav bar, cards, buttons, etc.)
3. Do NOT load all files at once -- only load what the screen requires

You MUST use components exactly as defined to ensure visual consistency. Do not reinvent components that already exist in the library.

## Design Aesthetics & Differentiation

Before applying platform rules, commit to a **bold aesthetic direction**. Generic, interchangeable mockups are the failure mode -- every screen should feel intentionally designed for its context.

### Aesthetic Thinking

Before coding, decide:
- **Purpose**: What problem does this screen solve? Who is the user?
- **Tone**: Pick an extreme and commit. Examples: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian. Use these as inspiration, then tailor one to the product.
- **Differentiation**: What is the one thing a user will remember about this screen?

Bold maximalism and refined minimalism both work. The failure mode is the timid middle.

### Avoid AI-Slop Aesthetics

NEVER default to:
- Overused font families: Inter, Roboto, Arial, generic system stacks (on non-iOS), Space Grotesk-by-default.
- Cliched palettes: purple gradients on white, washed-out pastel-everywhere, evenly-distributed rainbow accents.
- Predictable layouts: stacked card lists with no rhythm, identical hero patterns, cookie-cutter dashboard grids.
- Decorative emoji as a substitute for real iconography.

Vary between generations: light vs dark, serif vs grotesque vs mono display, dense vs airy. No two mockups in a session should converge on the same aesthetic unless the user is iterating on one.

### Aesthetic Levers

- **Typography**: Pair a distinctive display font with a refined body font. Pull from Google Fonts when on non-iOS targets (e.g. Fraunces, Instrument Serif, Bricolage Grotesque, JetBrains Mono, IBM Plex, Redaction, Migra, Söhne-feel sans). Use weight, tracking, and size contrast as design tools.
- **Color**: Dominant colors with sharp accents beat timid balanced palettes. Use CSS variables. Commit to a temperature (warm earth, cool tech, acidic neon, etc.).
- **Motion**: Concentrate motion at high-impact moments -- one orchestrated page-load with staggered reveals (CSS `animation-delay`) lands harder than scattered micro-interactions. Use `scroll-snap`, hover surprises, and bouncy springs sparingly but precisely.
- **Spatial Composition**: Asymmetry, overlap, diagonal flow, grid-breaking elements. Generous negative space OR controlled density -- not lukewarm middle.
- **Backgrounds & Texture**: Don't default to flat fills. Layer gradient meshes, noise/grain overlays, geometric patterns, dramatic shadows, decorative rules, custom cursors, soft inner-glows. Match texture to the chosen tone.

### Reconciliation with Platform Rules

When the target is iOS, the iOS Design Rules below **constrain** the aesthetic levers:
- The system font stack stays mandatory; aesthetic differentiation comes from weight, scale, color, and layout instead of webfont swaps.
- The no-purple rule is absolute -- pick a different bold accent.
- Glass goes on the navigation layer only; for content drama use texture, gradient, or photography.

For Android or platform-agnostic mockups, the levers above are unconstrained -- push them harder. Implementation complexity should match the aesthetic vision: maximalism needs elaborate code; minimalism needs precision.

## iOS Design Rules

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

Liquid Glass is Apple's translucent material for the navigation layer floating above content. In HTML mockups, simulate it with `backdrop-filter`:

```css
.glass {
    background: rgba(255, 255, 255, 0.55);
    backdrop-filter: saturate(180%) blur(20px);
    -webkit-backdrop-filter: saturate(180%) blur(20px);
    border: 0.5px solid rgba(255, 255, 255, 0.18);
    border-radius: 9999px; /* capsule */
}

@media (prefers-color-scheme: dark) {
    .glass {
        background: rgba(28, 28, 30, 0.55);
        border-color: rgba(255, 255, 255, 0.08);
    }
}
```

Glass rules:
- Apply glass to **navigation layer only** (tab bars, nav headers, floating toolbars, FABs). Never on content cards, list rows, or media tiles.
- Glass elements **float above** content; never stack glass on glass.
- Capsule (`border-radius: 9999px`) or fully rounded (16--24px) shapes only.
- Tint subtly using accent color at low opacity (e.g. `rgba(0, 122, 255, 0.18)`). Never purple.
- For media-rich backgrounds, drop the white fill and rely on `backdrop-filter` alone (the "clear" variant).

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
- [ ] System font stack used for typography.
- [ ] Glass only on nav layer, not on content.
- [ ] All touch targets >= 44x44px.
- [ ] Light/dark mode tokens, not hardcoded colors.
- [ ] Animations respect `prefers-reduced-motion`.

For Android mockups or platform-agnostic prototypes, these rules are advisory rather than mandatory -- but the no-purple guideline still applies unless the user explicitly requests purple.

## Workflow

### Step 1: Load Components & Design System

Before generating any screen:

1. **Read [components.md](components.md)** to see the component index, then load the specific component files needed
2. Look for `design-system.html` in the current working directory
3. If `design-system.html` exists, read it and use those token values to override the default `:root` variables from components.md
4. If it does NOT exist, ask the user about their preferred style:
   - Visual style (clean/minimal, bold/expressive, dark mode, glassmorphism, etc.)
   - Primary brand color
   - Font preference (Inter, SF Pro, system default, etc.)
   - Corner radius preference (sharp, rounded, pill)
   - Then generate `design-system.html` with the agreed tokens before proceeding

### Step 2: Gather Screen Requirements

Ask the user (if not already clear from arguments or context):
- What screen to design (e.g., "login", "dashboard", "profile", "settings")
- Key content and data to display
- Any specific interactions (modals, bottom sheets, swipe actions)
- Whether to include a status bar, navigation bar, or tab bar

If the user provides a screenshot, analyze it and reproduce the layout faithfully.

### Step 3: Scaffold the Device Frame (Recommended)

For new screens, start by generating a realistic iPhone frame (Dynamic Island + status bar + home indicator) using the bundled script:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/make-mobile-design/scripts/create_device_template.py" my-screen.html --title "My Screen"
```

This produces a self-contained HTML file with:
- Centered Dynamic Island pill at the top
- Status bar (9:41, signal/wifi/battery icons) — same as components Section 2
- Empty `<main class="device-content">` slot for your screen content
- Home indicator bar at the bottom

After scaffolding, fill `.device-content` with components from [components.md](components.md). Do not redesign the device chrome — leave the island, status bar, and home indicator as-is.

### Step 4: Generate the HTML Mockup

For iOS-targeted screens, re-read the **iOS Design Rules** section above and apply every item in the Compliance Check before writing the file.

Create a single self-contained HTML file following these rules:

#### File Structure
- Single HTML file, no external dependencies (except Google Fonts CDN and Iconify SVG API for icons)
- All CSS inline in a `<style>` tag
- Minimal JS for interactions (toggles, tabs, modals) in a `<script>` tag at the end
- Name the file descriptively: `[screen-name].html`

#### Mobile-First Constraints
- `max-width: 430px` on body, centered with `margin: 0 auto`
- Viewport meta tag: `width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no`
- ALWAYS include the Status Bar component from components.md (Section 2)
- Use `-webkit-font-smoothing: antialiased`
- All touch targets minimum 44x44px

#### CSS Architecture
- Start with the Base Layout & Design Tokens from components.md (Section 1) -- this is the `:root` block and CSS reset
- Use the exact CSS variable names defined in components.md (`--color-primary`, `--space-4`, `--radius-md`, etc.)
- No utility class frameworks -- write semantic CSS
- Use `flexbox` and `grid` for layout
- Use `scroll-snap` for horizontal carousels
- Smooth transitions on interactive elements (0.15s-0.2s)
- Hide scrollbars with `-webkit-scrollbar: none` and `scrollbar-width: none`

#### Component Usage Rules
- **ALWAYS** copy component HTML and CSS exactly from components.md -- do not rewrite or restyle them
- When a screen needs a navigation header, use the Nav Header component (Section 3)
- When a screen needs bottom navigation, use the Tab Bar component (Section 4)
- When a screen needs search, use the Search Bar component (Section 5)
- Use the Section Header component (Section 8) for all section dividers
- Use the List Item component (Section 10) for all row-based content
- Use icons from the Common SVG Icons set (Section 25) for standard UI icons (chevrons, close, home, search, etc.)
- For domain-specific or additional icons not in Section 25, use the **Iconify API** (Section 26) -- see icon usage guide below
- If a needed component does not exist in the library, create it following the same CSS variable and naming patterns

#### Interactivity
- Copy JS snippets from components.md where provided (checkbox toggle, tab switching)
- Cards/rows that highlight on tap
- Bottom sheets using the Bottom Sheet component (Section 18)
- Floating action buttons using the FAB component (Section 17)

#### Content
- Use realistic sample data relevant to the app context
- If the app is Vietnamese-localized, use Vietnamese content
- Include enough items to show scroll behavior (not just 1-2 items)

### Step 5: Review

After generating, suggest:
- Opening the file in a browser to preview
- Any variations or states to consider (empty state, error state, loading state)

## Design System File Format

When creating `design-system.html`, structure it as a living reference page that displays all tokens visually:

```
design-system.html
- Color palette swatches (primary, secondary, semantic colors, grays)
- Typography scale (headings, body, captions with actual rendered examples)
- Spacing scale (visual blocks)
- Border radius examples
- Shadow examples
- Component library (buttons, cards, inputs, badges, chips, avatars, list items)
- Icon set (commonly used SVG icons)
```

This file serves as both documentation and a visual reference the user can open alongside mockups.

## Iconify API Integration

When a screen needs icons beyond the built-in SVG set (Section 25 of components.md), use the **Iconify API** to access 275,000+ open-source icons.

### Using Iconify icons in HTML mockups

Two methods, depending on context:

**Method 1: Inline `<img>` tag (simplest, for mockups)**
```html
<img src="https://api.iconify.design/mdi/receipt-text-outline.svg?width=24&height=24&color=%23currentColor" alt="receipt">
```

**Method 2: CSS background (for buttons, list items)**
```css
.icon-receipt {
    width: 24px; height: 24px;
    background: url('https://api.iconify.design/mdi/receipt-text-outline.svg?width=24&height=24&color=%236B7280') no-repeat center/contain;
}
```

Replace the color hex (URL-encoded: `%23` = `#`) to match your design tokens.

### Finding icons

Before generating a mockup, use the `/ios-icon-gen` skill to search for icons:

```
/ios-icon-gen search <keyword>
/ios-icon-gen search <keyword> --prefix mdi
```

### Recommended collections for mobile designs

| Collection | Prefix | Style | Best for |
|-----------|--------|-------|----------|
| Material Design | `mdi` | Filled + outline | General-purpose, Android-style |
| Phosphor | `ph` | 6 weights | Versatile, clean |
| Lucide | `lucide` | Thin stroke | Minimal, iOS-like |
| Tabler | `tabler` | Consistent stroke | Dashboard, tools |
| Heroicons | `heroicons` | Outline + solid | Tailwind-style |

### URL format

```
https://api.iconify.design/{collection}/{icon-name}.svg?width={px}&height={px}&color=%23{hex}
```

Examples:
```
https://api.iconify.design/mdi/receipt-text-outline.svg?width=24&height=24&color=%232563EB
https://api.iconify.design/lucide/scan.svg?width=20&height=20&color=%236B7280
https://api.iconify.design/ph/address-book.svg?width=32&height=32&color=%23ffffff
```

## Exporting Icons for iOS Development

After a mockup is approved, use the `/ios-icon-gen` skill to export icons as Xcode asset imagesets:

```
/ios-icon-gen mdi:receipt-text-outline myIconAsset --color 8E8E93 --output ./Assets.xcassets/icons
```

This bridges the design-to-code gap: icons chosen during mockup design can be directly exported as production-ready Xcode assets.

## Output

- Save the HTML file in the current working directory
- Provide a brief summary of what was built
- Note any design decisions made
- Suggest next screens or variations to design
