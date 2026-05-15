# A11. Avatar + A12. Badge + A13. Chip + A14. Buttons

## A11. Avatar

```html
<span class="avatar">AB</span>
<img class="avatar" src="..." alt="Anna Becker">
```

```css
.avatar {
    width: 40px; height: 40px;
    border-radius: 50%;
    background: var(--md-sys-color-primary-container);
    color: var(--md-sys-color-on-primary-container);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font: 500 var(--md-sys-typescale-title-medium) / 1 var(--font-roboto);
    overflow: hidden;
    object-fit: cover;
}
.avatar--sm { width: 24px; height: 24px; font-size: var(--md-sys-typescale-label-medium); }
.avatar--lg { width: 56px; height: 56px; font-size: var(--md-sys-typescale-title-large); }
```

## A12. Badge

Small dot or count badge. Goes on icon buttons in the top app bar or bottom nav.

```html
<span class="badge">3</span>
<span class="badge badge--dot" aria-label="Unread"></span>
```

```css
.badge {
    min-width: 16px;
    height: 16px;
    padding: 0 4px;
    border-radius: 8px;
    background: var(--md-sys-color-error);
    color: var(--md-sys-color-on-error);
    font: 500 10px / 1 var(--font-roboto);
    display: inline-flex;
    align-items: center;
    justify-content: center;
}
.badge--dot { width: 6px; height: 6px; padding: 0; border-radius: 50%; }
```

## A13. Chip

Full chip docs in [04-search-filters.md](04-search-filters.md) §A7. Quick reference:

```html
<button class="chip">Assist</button>
<button class="chip is-selected">Filter</button>
```

## A14. Buttons (five MD3 styles)

```html
<button class="btn btn--filled">Send</button>
<button class="btn btn--tonal">Save</button>
<button class="btn btn--outlined">Cancel</button>
<button class="btn btn--elevated">Edit</button>
<button class="btn btn--text">Learn more</button>
```

```css
.btn {
    height: 40px;
    padding: 0 24px;
    border: none;
    border-radius: var(--md-sys-shape-corner-full);
    font: 500 var(--md-sys-typescale-label-large) / 1 var(--font-roboto);
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: background-color 150ms var(--md-sys-motion-easing-standard),
                box-shadow 150ms var(--md-sys-motion-easing-standard);
}
.btn--filled {
    background: var(--md-sys-color-primary);
    color: var(--md-sys-color-on-primary);
}
.btn--filled:hover  { box-shadow: var(--md-sys-elevation-level1); background: color-mix(in srgb, var(--md-sys-color-primary) 92%, var(--md-sys-color-on-primary)); }
.btn--filled:active { box-shadow: none; }
.btn--tonal {
    background: var(--md-sys-color-secondary-container);
    color: var(--md-sys-color-on-secondary-container);
}
.btn--outlined {
    background: transparent;
    color: var(--md-sys-color-primary);
    border: 1px solid var(--md-sys-color-outline);
}
.btn--elevated {
    background: var(--md-sys-color-surface-container-low);
    color: var(--md-sys-color-primary);
    box-shadow: var(--md-sys-elevation-level1);
}
.btn--text {
    background: transparent;
    color: var(--md-sys-color-primary);
    padding: 0 12px;
}
.btn[disabled] {
    background: color-mix(in srgb, var(--md-sys-color-on-surface) 12%, transparent);
    color: color-mix(in srgb, var(--md-sys-color-on-surface) 38%, transparent);
    cursor: not-allowed;
    box-shadow: none;
}

/* Icon buttons — 48dp tap target, 24dp icon */
.icon-btn--filled {
    width: 40px; height: 40px;
    background: var(--md-sys-color-primary);
    color: var(--md-sys-color-on-primary);
    border-radius: var(--md-sys-shape-corner-full);
    border: none;
    cursor: pointer;
}
.icon-btn--tonal {
    width: 40px; height: 40px;
    background: var(--md-sys-color-secondary-container);
    color: var(--md-sys-color-on-secondary-container);
    border-radius: var(--md-sys-shape-corner-full);
    border: none;
    cursor: pointer;
}
.icon-btn--outlined {
    width: 40px; height: 40px;
    background: transparent;
    border: 1px solid var(--md-sys-color-outline);
    color: var(--md-sys-color-on-surface-variant);
    border-radius: var(--md-sys-shape-corner-full);
    cursor: pointer;
}
```

## Hierarchy

When stacking buttons on a screen, follow MD3 emphasis order:

1. **Filled** — highest emphasis. One per screen, for the primary action.
2. **Tonal** — second-highest. Use when filled would be too aggressive (e.g. "Save draft" alongside primary "Publish").
3. **Outlined** — secondary actions, mostly destructive or neutral counterparts.
4. **Elevated** — when the button sits on a busy/colored surface and needs lift.
5. **Text** — lowest emphasis. Card actions, snackbar actions, inline links.

## Do / Don't

| Do | Don't |
|---|---|
| One filled button per screen. | Two filled buttons competing for attention. |
| Use tonal for "save / draft / secondary commit" actions. | Use outlined where tonal fits better. |
| 40dp button height (24dp + 16dp vertical inset). | 50dp pill (that's iOS). |
| Use `label-large` (14px/500) for button text. | Use 17px (that's iOS body). |
