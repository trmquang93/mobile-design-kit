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

### Step 3: Generate the HTML Mockup

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

### Step 4: Review

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
