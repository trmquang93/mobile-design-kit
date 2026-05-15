# A22. Navigation Drawer + A23. Navigation Rail

## A22. Navigation Drawer (modal)

Slides in from the left over a scrim. Used when the app has more destinations than a bottom nav can hold (typically 5+).

```html
<div class="scrim"></div>
<aside class="nav-drawer" aria-label="Primary navigation">
    <header class="nav-drawer__header">
        <h2 class="nav-drawer__title">Mail</h2>
        <p class="nav-drawer__subtitle">anna@example.com</p>
    </header>

    <h3 class="nav-drawer__section-header">Mailboxes</h3>

    <button class="nav-drawer__item is-active">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4-8 5-8-5V6l8 5 8-5v2z"/></svg>
        <span>Inbox</span>
        <span class="nav-drawer__count">128</span>
    </button>
    <button class="nav-drawer__item">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2 1 21h22L12 2zm1 14h-2v-2h2v2zm0-4h-2V8h2v4z"/></svg>
        <span>Starred</span>
        <span class="nav-drawer__count">4</span>
    </button>
    <button class="nav-drawer__item">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>
        <span>Drafts</span>
    </button>
    <button class="nav-drawer__item">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="m2.01 21 21-9-21-9v7l15 2-15 2z"/></svg>
        <span>Sent</span>
    </button>

    <hr class="nav-drawer__divider">

    <h3 class="nav-drawer__section-header">Labels</h3>
    <button class="nav-drawer__item">
        <span class="nav-drawer__swatch" style="background: #4F378B"></span>
        <span>Personal</span>
    </button>
    <button class="nav-drawer__item">
        <span class="nav-drawer__swatch" style="background: #B3261E"></span>
        <span>Urgent</span>
    </button>
</aside>
```

```css
.nav-drawer {
    position: absolute;
    top: 0; left: 0; bottom: 0;
    width: 360px;
    max-width: calc(100% - 56px);
    padding: 12px 12px 16px;
    background: var(--md-sys-color-surface-container-low);
    color: var(--md-sys-color-on-surface);
    border-top-right-radius: var(--md-sys-shape-corner-large);
    border-bottom-right-radius: var(--md-sys-shape-corner-large);
    box-shadow: var(--md-sys-elevation-level1);
    z-index: 70;
    overflow-y: auto;
    animation: drawer-slide 350ms var(--md-sys-motion-easing-emphasized-decelerate);
}
@keyframes drawer-slide {
    from { transform: translateX(-100%); }
    to   { transform: translateX(0); }
}
.nav-drawer__header {
    padding: calc(24px + 16px) 16px 16px;  /* status-bar safe area + 16dp */
}
.nav-drawer__title {
    font: 400 var(--md-sys-typescale-title-large) / 1.27 var(--font-roboto);
}
.nav-drawer__subtitle {
    font: 400 var(--md-sys-typescale-body-medium) / 1.43 var(--font-roboto);
    color: var(--md-sys-color-on-surface-variant);
}
.nav-drawer__section-header {
    padding: 16px 16px 8px;
    font: 500 var(--md-sys-typescale-title-small) / 1.43 var(--font-roboto);
    color: var(--md-sys-color-on-surface-variant);
    letter-spacing: 0.1px;
}
.nav-drawer__item {
    display: flex;
    align-items: center;
    gap: 12px;
    width: 100%;
    min-height: 56px;
    padding: 0 16px;
    border: none;
    background: transparent;
    color: var(--md-sys-color-on-surface-variant);
    font: 500 var(--md-sys-typescale-label-large) / 1 var(--font-roboto);
    border-radius: var(--md-sys-shape-corner-full);
    cursor: pointer;
    transition: background-color 150ms var(--md-sys-motion-easing-standard);
}
.nav-drawer__item:hover { background: color-mix(in srgb, var(--md-sys-color-on-surface) 8%, transparent); }
.nav-drawer__item.is-active {
    background: var(--md-sys-color-secondary-container);
    color: var(--md-sys-color-on-secondary-container);
    font-weight: 700;
}
.nav-drawer__item > span:not([class]),
.nav-drawer__item > span.nav-drawer__swatch + span {
    flex: 1;
    text-align: left;
}
.nav-drawer__count {
    font: 500 var(--md-sys-typescale-label-medium) / 1 var(--font-roboto);
}
.nav-drawer__swatch {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    flex-shrink: 0;
}
.nav-drawer__divider {
    margin: 8px 16px;
    border: 0;
    border-top: 1px solid var(--md-sys-color-outline-variant);
}
```

### Standard navigation drawer

Same markup, no `.scrim`, and pin the drawer to the left side of the screen permanently (only useful on tablet / foldable / wide layouts — not the default phone target).

## A23. Navigation Rail

A compact vertical alternative — used on tablets, foldables, or wide phone landscape. Not common on Pixel 8 portrait; document for completeness.

```html
<aside class="nav-rail" aria-label="Primary navigation">
    <button class="nav-rail__fab" aria-label="Compose">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25z"/></svg>
    </button>
    <button class="nav-rail__item is-active">
        <span class="bottom-nav__indicator">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
        </span>
        Home
    </button>
    <button class="nav-rail__item">
        <span class="bottom-nav__indicator">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M15.5 14h-.79l-.28-.27A6.5 6.5 0 1 0 13 15.5l.27.28v.79l5 5L19.49 20l-5-5z"/></svg>
        </span>
        Search
    </button>
</aside>
```

```css
.nav-rail {
    position: absolute;
    top: 24px; left: 0; bottom: 24px;
    width: 80px;
    padding: 8px 0;
    background: var(--md-sys-color-surface);
    color: var(--md-sys-color-on-surface);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    z-index: 40;
}
.nav-rail__fab {
    width: 56px; height: 56px;
    border: none;
    background: var(--md-sys-color-primary-container);
    color: var(--md-sys-color-on-primary-container);
    border-radius: var(--md-sys-shape-corner-large);
    box-shadow: var(--md-sys-elevation-level1);
    margin: 8px 0 16px;
    cursor: pointer;
    display: inline-flex; align-items: center; justify-content: center;
}
.nav-rail__item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    width: 64px;
    border: none;
    background: transparent;
    color: var(--md-sys-color-on-surface-variant);
    font: 500 var(--md-sys-typescale-label-medium) / 1.33 var(--font-roboto);
    cursor: pointer;
    padding: 0;
}
.nav-rail__item.is-active { color: var(--md-sys-color-on-surface); }
```

## Do / Don't

| Do | Don't |
|---|---|
| Use a drawer when you have more than 5 top-level destinations. | Combine drawer + bottom nav on the same screen for the SAME destinations. |
| Use the pill `secondary-container` highlight for active drawer item. | A vertical accent bar on the left (that's M2). |
| Keep drawer width 360dp or less. | Full-screen drawer — that's a different pattern. |
| Use the rail only on tablet / wide layouts. | Force the rail on a Pixel-portrait mockup. |
