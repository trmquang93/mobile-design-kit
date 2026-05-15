## 27. Bottom Contextual Toolbar — Icon Only

Ephemeral, task-scoped action bar pinned to the bottom of the screen. Use for selection / edit / detail modes (Mail's archive/move/delete, Safari's back/forward/share, Photos' edit toolbar). **Distinct from a tab bar** — a tab bar is structural primary navigation that's always visible; a toolbar appears only while a contextual mode is active.

DO NOT use this on a screen that already has a bottom tab bar from `add_ios_tabbar.py` or `03-navigation.md`. Pick one bottom layer.

Two layouts share the same Liquid Glass recipe used by `scripts/add_ios_tabbar.py` (`glass` / `glass-split`) so contextual toolbars match the look of glass tab bars in the same app:

- **Single pill** — one floating capsule containing every action.
- **Split** — primary capsule on the left + a separate glass circle on the right for a destructive or trailing action (Mail/Photos pattern). Default below.

```html
<!-- HTML — split layout: primary pill + trailing destructive circle. -->
<div class="toolbar toolbar--bottom" role="toolbar" aria-label="Message actions">
    <div class="toolbar__group glass">
        <button class="toolbar__btn" aria-label="Archive">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 8v13H3V8"/><path d="M1 3h22v5H1z"/><line x1="10" y1="12" x2="14" y2="12"/></svg>
        </button>
        <button class="toolbar__btn" aria-label="Flag">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/></svg>
        </button>
        <button class="toolbar__btn" aria-label="Move to folder">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
        </button>
    </div>
    <div class="toolbar__group toolbar__group--trailing glass">
        <button class="toolbar__btn toolbar__btn--destructive" aria-label="Delete">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
        </button>
    </div>
</div>
```

For a single-pill layout, drop `.toolbar__group--trailing` and put every button inside one `.toolbar__group`.

```css
/* CSS */
.toolbar--bottom {
    /* Outer rail is transparent — the .toolbar__group(s) carry the glass. */
    position: absolute;
    left: 0;
    right: 0;
    bottom: 46px;                           /* clear the home-indicator area */
    height: 60px;
    padding: 0 16px;
    padding-bottom: env(safe-area-inset-bottom, 0px);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-3);
    z-index: 50;

    /* CRITICAL: do not block scroll on the bar's footprint. */
    pointer-events: none;
}

.toolbar--bottom > * { pointer-events: auto; }

.toolbar__group {
    /* Liquid Glass — apply the shared `.glass` class alongside this one
       in markup: <div class="toolbar__group glass">. The recipe lives
       in components/ios/00-liquid-glass.md (always load it).
       This rule only sets toolbar-specific layout. */
    display: inline-flex;
    align-items: center;
    gap: var(--space-1);
    height: 60px;
    padding: 0 6px;
    border-radius: 30px;
    box-shadow:
        0 12px 32px rgba(0, 0, 0, 0.18),
        0 1px 0 rgba(255, 255, 255, 0.45) inset;
}

.toolbar__group--trailing {
    width: 60px;
    padding: 0;
    justify-content: center;
    border-radius: 50%;
}

.toolbar__btn {
    /* 52x52 hit target inside the 60px capsule (>=44 minimum). */
    min-width: 52px;
    height: 52px;
    padding: 0;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border: 0;
    color: var(--color-primary);
    cursor: pointer;
    border-radius: 50%;
    transition: transform 80ms ease-out, background 0.15s ease, color 0.15s ease;
    font-family: var(--font-family);
}

.toolbar__btn svg { width: 22px; height: 22px; }
.toolbar__group--trailing .toolbar__btn { width: 60px; height: 60px; }

.toolbar__btn:active {
    transform: scale(0.94);
    background: color-mix(in srgb, currentColor 12%, transparent);
}

.toolbar__btn--destructive { color: var(--color-error); }
.toolbar__btn[disabled] { opacity: 0.35; pointer-events: none; }

.toolbar__spacer { flex: 1 1 auto; }

@media (prefers-color-scheme: dark) {
    .toolbar__group {
        background: color-mix(in srgb, #1C1C1E 50%, transparent);
        border-color: color-mix(in srgb, #FFFFFF 12%, transparent);
        box-shadow:
            0 12px 32px rgba(0, 0, 0, 0.40),
            0 1px 0 rgba(255, 255, 255, 0.06) inset;
    }
}

/* IMPORTANT: do NOT add CSS animations on `.toolbar--bottom` or any
   ancestor of a `.glass` element. ANY CSS animation (even opacity-only)
   promotes the element to a separate compositor layer, and
   `backdrop-filter: url(#glass-distortion)` with `feDisplacementMap`
   silently fails to identity output across compositor layers. The pill
   still renders with its sheen + rim highlight, but the backdrop passes
   through unwarped. See components/ios/00-liquid-glass.md for details.

   If you need an entrance animation, animate a non-glass WRAPPER around
   the toolbar (the wrapper takes the layer promotion; the glass pills
   inside stay in the parent compositor and warp correctly). */
```

To dismiss the toolbar, fade a non-glass wrapper (e.g. via JS toggling
`opacity` and `display: none` after a CSS `transition`) — never
animate `.toolbar--bottom` itself or you'll re-trigger the displacement
identity-fallback bug.

---

## 28. Bottom Toolbar — Icon + Label

Variant of section 27. Single glass capsule, taller, each button stacks an icon over a small label. Use when actions are less obvious than archive/share (e.g. "Markup", "Crop", "Adjust").

```html
<!-- HTML — single pill, no trailing split. -->
<div class="toolbar toolbar--bottom toolbar--labels" role="toolbar" aria-label="Photo edit actions">
    <div class="toolbar__group toolbar__group--full glass">
        <button class="toolbar__btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            <span class="toolbar__label">Markup</span>
        </button>
        <button class="toolbar__btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2v14a2 2 0 0 0 2 2h14"/><path d="M18 22V8a2 2 0 0 0-2-2H2"/></svg>
            <span class="toolbar__label">Crop</span>
        </button>
        <button class="toolbar__btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2v20"/></svg>
            <span class="toolbar__label">Adjust</span>
        </button>
        <button class="toolbar__btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="9"/></svg>
            <span class="toolbar__label">Filters</span>
        </button>
    </div>
</div>
```

```css
/* CSS — extends section 27. The pill stretches edge-to-edge and items distribute evenly. */
.toolbar--labels { height: 72px; }

.toolbar__group--full {
    flex: 1 1 auto;
    height: 72px;
    padding: 6px var(--space-2);
    border-radius: 36px;
}

.toolbar--labels .toolbar__btn {
    flex: 1 1 0;
    flex-direction: column;
    gap: 2px;
    height: 100%;
    border-radius: 24px;
}

.toolbar__label {
    font-size: var(--text-caption2);   /* 11px — matches HIG tab bar labels */
    font-weight: 500;
    letter-spacing: 0.01em;
    line-height: 1;
}
```

---

## 29. Bottom Toolbar — With Overflow Menu

Variant of section 27. Adds an ellipsis (`•••`) button on the right that toggles a popover anchored bottom-right. The popover reuses the action-menu styles from `08-overlays.md` — copy section 19 onto the screen and reference `.action-menu` here.

```html
<!-- HTML — popover sits inside the menu host group so it inherits pointer-events isolation. -->
<div class="toolbar toolbar--bottom" role="toolbar" aria-label="Document actions">
    <div class="toolbar__group toolbar__menu-host glass" data-menu-open="false">
        <button class="toolbar__btn" aria-label="Share">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>
        </button>
        <button class="toolbar__btn" aria-label="Bookmark">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
        </button>
        <button class="toolbar__btn toolbar__menu-trigger" aria-label="More" aria-haspopup="menu" aria-expanded="false"
                onclick="(function(b){var h=b.closest('.toolbar__menu-host');var o=h.dataset.menuOpen!=='true';h.dataset.menuOpen=o;b.setAttribute('aria-expanded',o);})(this)">
            <svg viewBox="0 0 24 24" fill="currentColor"><circle cx="6" cy="12" r="1.6"/><circle cx="12" cy="12" r="1.6"/><circle cx="18" cy="12" r="1.6"/></svg>
        </button>

        <!-- Popover — uses .action-menu from 08-overlays.md (section 19). Anchored bottom-right above the pill. -->
        <div class="toolbar__menu action-menu" role="menu">
            <div class="action-menu-item" role="menuitem">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3h18v18H3z"/><path d="M12 8v8"/><path d="M8 12h8"/></svg>
                <span>Move to folder</span>
            </div>
            <div class="action-menu-item" role="menuitem">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z"/></svg>
                <span>Translate</span>
            </div>
            <div class="action-menu-divider"></div>
            <div class="action-menu-item destructive" role="menuitem">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/></svg>
                <span>Delete</span>
            </div>
        </div>
    </div>
</div>
```

```css
/* CSS — extends section 27. Anchors the popover and animates open/close. */
.toolbar__menu-host { position: relative; }

.toolbar__menu {
    position: absolute;
    right: 0;
    bottom: calc(100% + var(--space-2));
    transform-origin: bottom right;
    opacity: 0;
    transform: scale(0.92) translateY(8px);
    pointer-events: none;
    transition: opacity 0.18s ease, transform 0.18s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.toolbar__menu-host[data-menu-open="true"] .toolbar__menu {
    opacity: 1;
    transform: scale(1) translateY(0);
    pointer-events: auto;
}

@media (prefers-reduced-motion: reduce) {
    .toolbar__menu { transition: opacity 0.12s linear; transform: none; }
    .toolbar__menu-host[data-menu-open="true"] .toolbar__menu { transform: none; }
}
```

---

## 30. Header Toolbar — Leading / Trailing

Use only when the nav header needs **more than one trailing action** (e.g. share + edit + ⋯). For a single trailing action, stick with the standard nav header in `03-navigation.md`. Do not stack this on top of the standard nav header — replace the action slot.

```html
<!-- HTML — drop into the existing .nav-header from 03-navigation.md as the trailing slot. -->
<div class="nav-toolbar" role="toolbar" aria-label="Document header actions">
    <button class="nav-toolbar__btn" aria-label="Share">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>
    </button>
    <button class="nav-toolbar__btn" aria-label="Edit">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
    </button>
    <button class="nav-toolbar__btn" aria-label="More">
        <svg viewBox="0 0 24 24" fill="currentColor"><circle cx="6" cy="12" r="1.6"/><circle cx="12" cy="12" r="1.6"/><circle cx="18" cy="12" r="1.6"/></svg>
    </button>
</div>
```

```css
/* CSS */
.nav-toolbar {
    display: inline-flex;
    align-items: center;
    gap: var(--space-1);
}

.nav-toolbar__btn {
    width: 44px;
    height: 44px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border: 0;
    color: var(--color-primary);
    cursor: pointer;
    border-radius: var(--radius-xs);
    transition: transform 80ms ease-out, background 0.15s ease;
}

.nav-toolbar__btn svg { width: 22px; height: 22px; }

.nav-toolbar__btn:active {
    transform: scale(0.94);
    background: rgba(60, 60, 67, 0.08);
}

@media (prefers-color-scheme: dark) {
    .nav-toolbar__btn:active { background: rgba(255, 255, 255, 0.08); }
}
```

---

## Platform mapping

These class names map 1:1 onto the iOS-native and Expo Router APIs the user is likely targeting:

| Mockup class | Expo Router | UIKit | SwiftUI |
|---|---|---|---|
| `.toolbar--bottom` | `<Stack.Toolbar placement="bottom">` | `UIToolbar` | `.toolbar { ToolbarItemGroup(placement: .bottomBar) { … } }` |
| `.toolbar__group` / `.toolbar__group--trailing` | `Stack.Toolbar.Group` | `UIToolbar` segments | `ToolbarItemGroup` (multiple groups in `.bottomBar`) |
| `.toolbar__btn` | `Stack.Toolbar.Button` | `UIBarButtonItem` | `Button { … }` inside `ToolbarItem` |
| `.toolbar__spacer` | `Stack.Toolbar.Spacer` | `UIBarButtonItem.flexibleSpace` | `Spacer()` |
| `.toolbar__menu-trigger` + `.toolbar__menu` | `Stack.Toolbar.Menu` | `UIBarButtonItem` with `UIMenu` | `Menu { … }` |
| `.nav-toolbar` | `<Stack.Toolbar placement="right">` (or `"left"`) | `UINavigationItem.rightBarButtonItems` | `.toolbar { ToolbarItemGroup(placement: .topBarTrailing) { … } }` |

**HARD RULES** (copy into every toolbar mockup):
- Wrapper is `pointer-events: none`; children re-enable with `pointer-events: auto`.
- Bottom variants pad with `env(safe-area-inset-bottom, 0px)`.
- Buttons hit 44×44 minimum even when the glyph is 22px.
- Tint uses `--color-primary` (blue/green/orange/teal/indigo only — NEVER purple).
- Reuse the shared `.glass` recipe from [components/ios/00-liquid-glass.md](00-liquid-glass.md) (SVG-displacement refractive glass with flat-blur fallback). Do not invent a different glass formula.
- All entry/exit animations live inside `@media (prefers-reduced-motion: no-preference)`; the bar must render in its final state when motion is reduced.
