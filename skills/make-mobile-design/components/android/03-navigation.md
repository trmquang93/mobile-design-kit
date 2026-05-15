# A3. Top App Bar + A4. Bottom Navigation Bar

Material 3 navigation surfaces. **Pick one top app bar variant and at most one bottom nav per screen.** Never combine `add_ios_tabbar.py`'s output with these — that script is iOS-only.

## A3. Top App Bar (four variants)

All variants are sticky under the 24px status bar. The first child of `.device-content` MUST be the top app bar (or a hero) to own the status-bar safe area.

### A3.a — Small top app bar (default)

64dp tall. Title on the left next to a leading icon, trailing icon row on the right.

```html
<header class="top-app-bar top-app-bar--small">
    <button class="icon-btn" aria-label="Open navigation">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M3 6h18v2H3zm0 5h18v2H3zm0 5h18v2H3z"/></svg>
    </button>
    <h1 class="top-app-bar__title">Inbox</h1>
    <div class="top-app-bar__actions">
        <button class="icon-btn" aria-label="Search">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M15.5 14h-.79l-.28-.27A6.5 6.5 0 1 0 13 15.5l.27.28v.79l5 5L19.49 20l-5-5zm-6 0a4.5 4.5 0 1 1 4.5-4.5 4.5 4.5 0 0 1-4.5 4.5z"/></svg>
        </button>
        <button class="icon-btn" aria-label="More">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="5" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="12" cy="19" r="2"/></svg>
        </button>
    </div>
</header>
```

```css
.top-app-bar {
    position: sticky;
    top: 0;
    z-index: 10;
    display: flex;
    align-items: center;
    gap: 4px;
    padding: calc(24px + 8px) 4px 8px 4px;  /* 24px status-bar safe area + 8dp */
    background: var(--md-sys-color-surface);
    color: var(--md-sys-color-on-surface);
    transition: background-color var(--md-sys-motion-duration-short4) var(--md-sys-motion-easing-standard),
                box-shadow var(--md-sys-motion-duration-short4) var(--md-sys-motion-easing-standard);
}
/* When content scrolls beneath, switch to surface-container tone + level2 shadow */
.top-app-bar.is-scrolled {
    background: var(--md-sys-color-surface-container);
    box-shadow: var(--md-sys-elevation-level2);
}
.top-app-bar__title {
    flex: 1;
    font-size: var(--md-sys-typescale-title-large);  /* 22px */
    font-weight: 400;
    letter-spacing: 0;
    margin-left: 12px;
}
.top-app-bar__actions { display: flex; gap: 0; }
.icon-btn {
    width: 48px;
    height: 48px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border: none;
    background: transparent;
    color: inherit;
    border-radius: var(--md-sys-shape-corner-full);
    cursor: pointer;
    transition: background-color var(--md-sys-motion-duration-short2) var(--md-sys-motion-easing-standard);
}
.icon-btn:hover  { background: color-mix(in srgb, currentColor 8%, transparent); }
.icon-btn:active { background: color-mix(in srgb, currentColor 12%, transparent); }
```

### A3.b — Center-aligned top app bar

64dp tall. Title centered. Use for sub-pages (with a back button) or modal-feeling screens.

```html
<header class="top-app-bar top-app-bar--center">
    <button class="icon-btn" aria-label="Back">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>
    </button>
    <h1 class="top-app-bar__title top-app-bar__title--center">Settings</h1>
    <button class="icon-btn" aria-label="More">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="5" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="12" cy="19" r="2"/></svg>
    </button>
</header>
```

```css
.top-app-bar--center .top-app-bar__title--center {
    flex: 1;
    text-align: center;
    margin: 0;
    font-size: var(--md-sys-typescale-title-large);
}
```

### A3.c — Medium top app bar (two-line, collapsible)

112dp tall at rest. Title sits on its own line below a 64dp top row. Collapses to small on scroll (apply `.is-scrolled` class via JS).

```html
<header class="top-app-bar top-app-bar--medium">
    <div class="top-app-bar__top-row">
        <button class="icon-btn" aria-label="Back">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>
        </button>
        <div class="top-app-bar__actions">
            <button class="icon-btn" aria-label="Favorite">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
            </button>
        </div>
    </div>
    <h1 class="top-app-bar__title top-app-bar__title--large">Photos</h1>
</header>
```

```css
.top-app-bar--medium {
    flex-direction: column;
    align-items: stretch;
    gap: 0;
    padding: calc(24px + 8px) 4px 20px 4px;
}
.top-app-bar--medium .top-app-bar__top-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 32px;
}
.top-app-bar__title--large {
    font-size: var(--md-sys-typescale-headline-small);  /* 24px for medium variant */
    font-weight: 400;
    padding: 8px 16px 0;
    margin: 0;
}
```

### A3.d — Large top app bar

152dp tall. Hero variant. Same markup as medium but the title uses `headline-medium` (28px).

```css
.top-app-bar--large { padding-bottom: 28px; }
.top-app-bar--large .top-app-bar__title--large {
    font-size: var(--md-sys-typescale-headline-medium);  /* 28px */
    padding: 20px 16px 0;
}
```

## A4. Bottom Navigation Bar

80dp tall. 3–5 destinations. Each destination has a 32×64 pill-shaped **active indicator** behind the icon when active. Labels are always visible (MD3 default).

Use `scripts/add_android_navbar.py` to inject this into a scaffolded file — do not hand-write the markup unless extending it.

```html
<nav class="bottom-nav" aria-label="Primary">
    <button class="bottom-nav__item is-active" aria-current="page">
        <span class="bottom-nav__indicator">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
        </span>
        <span class="bottom-nav__label">Home</span>
    </button>
    <button class="bottom-nav__item">
        <span class="bottom-nav__indicator">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M15.5 14h-.79l-.28-.27A6.5 6.5 0 1 0 13 15.5l.27.28v.79l5 5L19.49 20l-5-5zm-6 0a4.5 4.5 0 1 1 4.5-4.5 4.5 4.5 0 0 1-4.5 4.5z"/></svg>
        </span>
        <span class="bottom-nav__label">Search</span>
    </button>
    <button class="bottom-nav__item">
        <span class="bottom-nav__indicator">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
        </span>
        <span class="bottom-nav__label">Saved</span>
    </button>
    <button class="bottom-nav__item">
        <span class="bottom-nav__indicator">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
        </span>
        <span class="bottom-nav__label">Profile</span>
    </button>
</nav>
```

```css
.bottom-nav {
    position: absolute;
    bottom: 24px;        /* clearance above gesture-nav pill */
    left: 0; right: 0;
    height: 80px;
    display: flex;
    justify-content: space-around;
    align-items: flex-start;
    padding: 12px 8px 16px;
    background: var(--md-sys-color-surface-container);
    z-index: 40;
    pointer-events: none;  /* wrapper passes scroll through; children opt-in */
}
.bottom-nav__item {
    pointer-events: auto;
    flex: 1;
    max-width: 80px;
    min-height: 48px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    border: none;
    background: transparent;
    color: var(--md-sys-color-on-surface-variant);
    cursor: pointer;
    padding: 0;
}
.bottom-nav__indicator {
    width: 64px;
    height: 32px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--md-sys-shape-corner-full);
    transition: background-color var(--md-sys-motion-duration-short4) var(--md-sys-motion-easing-emphasized),
                color var(--md-sys-motion-duration-short4) var(--md-sys-motion-easing-emphasized);
}
.bottom-nav__item.is-active .bottom-nav__indicator {
    background: var(--md-sys-color-secondary-container);
    color: var(--md-sys-color-on-secondary-container);
}
.bottom-nav__item.is-active { color: var(--md-sys-color-on-surface); }
.bottom-nav__label {
    font-size: var(--md-sys-typescale-label-medium);  /* 12px */
    font-weight: 500;
    line-height: 1.33;
    letter-spacing: 0.5px;
}
.bottom-nav__item.is-active .bottom-nav__label { font-weight: 700; }
```

**Why the pill-indicator pattern matters:** it's the single most recognizable Android-vs-iOS giveaway in MD3. The active item gets a `secondary-container` pill behind its icon; the icon itself swaps from outlined to filled when active (do this in your SVG choice). Don't change the icon position or omit the pill.

## Do / Don't

| Do | Don't |
|---|---|
| Use `.is-scrolled` toggle for surface-container tone on scroll. | Layer `backdrop-filter` (that's iOS). |
| Pin the top app bar via `position: sticky; top: 0`. | Make it `position: fixed` (breaks the scroll context). |
| Keep bottom-nav labels at 12px / weight 500. | Drop labels — MD3 nav-bar labels are always visible. |
| 3–5 bottom-nav items. | Fewer than 3 or more than 5. |
| Apply pill indicator to active item only. | Apply it to every item. |
| Use 48dp minimum tap target. | Use 44px (that's iOS). |
