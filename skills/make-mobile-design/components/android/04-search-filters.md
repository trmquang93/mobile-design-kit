# A5. Search Bar + A6. Segmented Buttons + A7. Chips

## A5. Search Bar (docked)

The MD3 docked search bar floats over the top of the screen, looking like a pill with leading + trailing icons.

```html
<form class="search-bar" role="search">
    <button type="button" class="icon-btn" aria-label="Open menu">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M3 6h18v2H3zm0 5h18v2H3zm0 5h18v2H3z"/></svg>
    </button>
    <input type="search" class="search-bar__input" placeholder="Search photos" aria-label="Search">
    <button type="button" class="icon-btn" aria-label="Voice search">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.3-3c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.48 6-3.3 6-6.72h-1.7z"/></svg>
    </button>
</form>
```

```css
.search-bar {
    display: flex;
    align-items: center;
    height: 56px;
    margin: 8px 16px;
    padding: 4px 8px;
    background: var(--md-sys-color-surface-container-high);
    border-radius: var(--md-sys-shape-corner-full);
    box-shadow: var(--md-sys-elevation-level1);
}
.search-bar__input {
    flex: 1;
    border: none;
    background: transparent;
    color: var(--md-sys-color-on-surface);
    font: 400 var(--md-sys-typescale-body-large) / 1.5 var(--font-roboto);
    outline: none;
    padding: 0 8px;
}
.search-bar__input::placeholder { color: var(--md-sys-color-on-surface-variant); }
```

## A6. Segmented Buttons

Two to five connected buttons. Used like iOS segmented control but with MD3 shape and check-icon-on-selected animation.

```html
<div class="segmented" role="group" aria-label="View mode">
    <button class="segmented__btn is-selected" aria-pressed="true">
        <svg class="segmented__check" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/></svg>
        Grid
    </button>
    <button class="segmented__btn" aria-pressed="false">List</button>
    <button class="segmented__btn" aria-pressed="false">Map</button>
</div>
```

```css
.segmented {
    display: inline-flex;
    border: 1px solid var(--md-sys-color-outline);
    border-radius: var(--md-sys-shape-corner-full);
    overflow: hidden;
}
.segmented__btn {
    min-height: 40px;
    padding: 0 16px;
    border: none;
    background: transparent;
    color: var(--md-sys-color-on-surface);
    font: 500 var(--md-sys-typescale-label-large) / 1 var(--font-roboto);
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    border-right: 1px solid var(--md-sys-color-outline);
    transition: background-color 150ms var(--md-sys-motion-easing-standard);
}
.segmented__btn:last-child { border-right: none; }
.segmented__btn.is-selected {
    background: var(--md-sys-color-secondary-container);
    color: var(--md-sys-color-on-secondary-container);
}
.segmented__check { display: none; }
.segmented__btn.is-selected .segmented__check { display: inline-block; }
```

## A7. Chips

Four MD3 variants: **assist**, **filter**, **input**, **suggestion**. All share the same chip shell; semantics differ.

```html
<div class="chip-row">
    <button class="chip">              <!-- assist -->
        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
        Add stop
    </button>
    <button class="chip is-selected">  <!-- filter, selected -->
        <svg class="chip__check" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/></svg>
        Today
    </button>
    <button class="chip">              <!-- filter, unselected -->
        This week
    </button>
    <span class="chip chip--input">    <!-- input -->
        <img class="chip__avatar" alt="" src="https://api.iconify.design/material-symbols/person.svg?color=%23FFFFFF">
        Anna
        <button class="chip__dismiss" aria-label="Remove">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M19 6.4 17.6 5 12 10.6 6.4 5 5 6.4 10.6 12 5 17.6 6.4 19 12 13.4 17.6 19 19 17.6 13.4 12z"/></svg>
        </button>
    </span>
</div>
```

```css
.chip-row { display: flex; gap: 8px; flex-wrap: wrap; padding: 8px 16px; }
.chip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    min-height: 32px;
    padding: 0 16px;
    border: 1px solid var(--md-sys-color-outline);
    background: transparent;
    color: var(--md-sys-color-on-surface-variant);
    font: 500 var(--md-sys-typescale-label-large) / 1 var(--font-roboto);
    border-radius: var(--md-sys-shape-corner-small);
    cursor: pointer;
    transition: background-color 150ms var(--md-sys-motion-easing-standard);
}
.chip:hover { background: color-mix(in srgb, var(--md-sys-color-on-surface-variant) 8%, transparent); }
.chip.is-selected {
    background: var(--md-sys-color-secondary-container);
    color: var(--md-sys-color-on-secondary-container);
    border-color: transparent;
}
.chip__check { display: none; }
.chip.is-selected .chip__check { display: inline-block; }
.chip--input {
    padding-left: 4px;
    padding-right: 4px;
    background: var(--md-sys-color-surface-container-high);
    border-color: transparent;
}
.chip__avatar { width: 24px; height: 24px; border-radius: 50%; background: var(--md-sys-color-primary); padding: 4px; }
.chip__dismiss {
    width: 18px; height: 18px;
    border: none; background: transparent;
    color: currentColor; cursor: pointer;
    display: inline-flex; align-items: center; justify-content: center;
}
```

## Do / Don't

| Do | Don't |
|---|---|
| Use `secondary-container` for selected chip/segment. | Use `primary` (reserved for filled buttons / FAB). |
| 8dp corner on chips (MD3 default). | Full-pill chips (that's M2 / older). |
| Show a leading check on selected filter/segment. | Use a trailing arrow icon (that's M2). |
| Wrap chip rows; let them flow horizontally. | Force them into a single line — they overflow on small screens. |
