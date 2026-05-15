# A19. Bottom Sheet + A20. Dialog + A21. Menu

## A19. Bottom Sheet (modal)

Slides up from the bottom over a scrim. Drag handle at the top is the MD3 default.

```html
<div class="scrim" aria-hidden="false"></div>
<aside class="bottom-sheet" role="dialog" aria-modal="true" aria-labelledby="bs-title">
    <div class="bottom-sheet__handle" aria-hidden="true"></div>
    <h2 id="bs-title" class="bottom-sheet__title">Sort by</h2>
    <ul class="list">
        <li class="list-item"><span class="list-item__text">Most recent</span></li>
        <li class="list-item"><span class="list-item__text">Most popular</span></li>
        <li class="list-item"><span class="list-item__text">Trending</span></li>
    </ul>
</aside>
```

```css
.scrim {
    position: absolute;
    inset: 0;
    background: var(--md-sys-color-scrim);
    opacity: 0.32;
    z-index: 60;
    pointer-events: auto;
}
.bottom-sheet {
    position: absolute;
    bottom: 0;
    left: 0; right: 0;
    background: var(--md-sys-color-surface-container-low);
    color: var(--md-sys-color-on-surface);
    border-top-left-radius: var(--md-sys-shape-corner-extra-large);
    border-top-right-radius: var(--md-sys-shape-corner-extra-large);
    padding: 0 0 32px;
    z-index: 70;
    box-shadow: var(--md-sys-elevation-level3);
    animation: bs-rise 350ms var(--md-sys-motion-easing-emphasized-decelerate);
}
.bottom-sheet__handle {
    width: 32px;
    height: 4px;
    background: var(--md-sys-color-on-surface-variant);
    opacity: 0.4;
    border-radius: var(--md-sys-shape-corner-full);
    margin: 16px auto 8px;
}
.bottom-sheet__title {
    font: 400 var(--md-sys-typescale-title-large) / 1.27 var(--font-roboto);
    padding: 12px 16px 16px;
}
@keyframes bs-rise {
    from { transform: translateY(100%); }
    to   { transform: translateY(0); }
}
@media (prefers-reduced-motion: reduce) {
    .bottom-sheet { animation: none; }
}
```

### Standard bottom sheet

Same markup, drop the `.scrim`, and keep the sheet docked at the bottom edge of the screen — used like a persistent panel.

## A20. Dialog (basic)

```html
<div class="scrim"></div>
<div class="dialog" role="dialog" aria-modal="true" aria-labelledby="dlg-title">
    <span class="dialog__icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/></svg>
    </span>
    <h2 id="dlg-title" class="dialog__title">Discard draft?</h2>
    <p class="dialog__body">You will lose your changes if you don't save. This action can't be undone.</p>
    <div class="dialog__actions">
        <button class="btn btn--text">Cancel</button>
        <button class="btn btn--text">Discard</button>
    </div>
</div>
```

```css
.dialog {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: calc(100% - 48px);
    max-width: 360px;
    padding: 24px;
    background: var(--md-sys-color-surface-container-high);
    color: var(--md-sys-color-on-surface);
    border-radius: var(--md-sys-shape-corner-extra-large);
    box-shadow: var(--md-sys-elevation-level3);
    z-index: 80;
    text-align: left;
}
.dialog__icon {
    display: inline-flex;
    color: var(--md-sys-color-secondary);
    margin-bottom: 16px;
}
.dialog__title {
    font: 400 var(--md-sys-typescale-headline-small) / 1.33 var(--font-roboto);
    margin-bottom: 16px;
}
.dialog__body {
    font: 400 var(--md-sys-typescale-body-medium) / 1.43 var(--font-roboto);
    color: var(--md-sys-color-on-surface-variant);
    margin-bottom: 24px;
}
.dialog__actions {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
}
```

### Full-screen dialog

```html
<div class="dialog dialog--fullscreen">
    <header class="top-app-bar top-app-bar--small">
        <button class="icon-btn" aria-label="Close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M19 6.4 17.6 5 12 10.6 6.4 5 5 6.4 10.6 12 5 17.6 6.4 19 12 13.4 17.6 19 19 17.6 13.4 12z"/></svg>
        </button>
        <h1 class="top-app-bar__title">New event</h1>
        <div class="top-app-bar__actions">
            <button class="btn btn--text">Save</button>
        </div>
    </header>
    <!-- form contents -->
</div>
```

```css
.dialog--fullscreen {
    position: absolute;
    inset: 0;
    transform: none;
    width: auto;
    max-width: none;
    padding: 0;
    background: var(--md-sys-color-surface);
    border-radius: 0;
    box-shadow: none;
}
```

## A21. Menu (dropdown)

```html
<div class="menu" role="menu">
    <button class="menu__item" role="menuitem">Edit</button>
    <button class="menu__item" role="menuitem">Share</button>
    <hr class="menu__divider">
    <button class="menu__item menu__item--destructive" role="menuitem">Delete</button>
</div>
```

```css
.menu {
    position: absolute;
    min-width: 112px;
    padding: 8px 0;
    background: var(--md-sys-color-surface-container);
    border-radius: var(--md-sys-shape-corner-extra-small);
    box-shadow: var(--md-sys-elevation-level2);
    z-index: 75;
}
.menu__item {
    display: block;
    width: 100%;
    padding: 0 12px;
    height: 48px;
    border: none;
    background: transparent;
    text-align: left;
    color: var(--md-sys-color-on-surface);
    font: 400 var(--md-sys-typescale-label-large) / 1 var(--font-roboto);
    cursor: pointer;
}
.menu__item:hover { background: color-mix(in srgb, var(--md-sys-color-on-surface) 8%, transparent); }
.menu__item--destructive { color: var(--md-sys-color-error); }
.menu__divider { margin: 4px 0; border: 0; border-top: 1px solid var(--md-sys-color-outline-variant); }
```

## Do / Don't

| Do | Don't |
|---|---|
| Use `surface-container-low` for bottom sheet (matches MD3 elevation overlay). | Use `surface` flat — it'll look unelevated. |
| Always show the drag handle on modal bottom sheets. | Omit it — Android users tap/drag it. |
| Use `corner-extra-large` (28dp) on dialogs and the top of bottom sheets. | Use sharper corners — that's M2. |
| Dialog actions stay text buttons (lowest emphasis). | Use filled buttons in dialog footer. |
| Scrim at 32% opacity. | 50%+ — too dark for MD3. |
