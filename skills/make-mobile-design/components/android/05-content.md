# A8. Section Header + A9. Cards + A10. List Items

## A8. Section Header

```html
<h2 class="section-header">Recently saved</h2>
```

```css
.section-header {
    margin: 24px 16px 8px;
    font: 500 var(--md-sys-typescale-title-small) / 1.43 var(--font-roboto);
    color: var(--md-sys-color-on-surface-variant);
    letter-spacing: 0.1px;
}
```

## A9. Cards (three variants)

### Elevated card (default)

```html
<article class="card card--elevated">
    <img class="card__media" src="https://picsum.photos/seed/a/400/200" alt="">
    <div class="card__body">
        <h3 class="card__title">Yosemite Valley</h3>
        <p class="card__support">Eastern California. 5 saved photos.</p>
    </div>
    <div class="card__actions">
        <button class="btn btn--text">Share</button>
        <button class="btn btn--text">Open</button>
    </div>
</article>
```

```css
.card {
    margin: 8px 16px;
    border-radius: var(--md-sys-shape-corner-medium);
    overflow: hidden;
    background: var(--md-sys-color-surface-container-low);
    color: var(--md-sys-color-on-surface);
}
.card--elevated {
    background: var(--md-sys-color-surface-container-low);
    box-shadow: var(--md-sys-elevation-level1);
}
.card--filled    { background: var(--md-sys-color-surface-container-highest); }
.card--outlined  { background: var(--md-sys-color-surface); border: 1px solid var(--md-sys-color-outline-variant); }
.card__media { width: 100%; height: 160px; object-fit: cover; display: block; }
.card__body  { padding: 16px; }
.card__title {
    font: 500 var(--md-sys-typescale-title-medium) / 1.5 var(--font-roboto);
    margin-bottom: 4px;
}
.card__support {
    font: 400 var(--md-sys-typescale-body-medium) / 1.43 var(--font-roboto);
    color: var(--md-sys-color-on-surface-variant);
}
.card__actions { display: flex; gap: 8px; padding: 0 8px 8px; justify-content: flex-end; }
```

## A10. List Item

MD3 list items support one, two, or three lines. Leading slot (avatar / icon), trailing slot (icon / switch / chevron / meta).

### One-line list item

```html
<ul class="list">
    <li class="list-item">
        <span class="list-item__leading">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
        </span>
        <span class="list-item__text">Account</span>
        <span class="list-item__trailing">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M9 6 7.6 7.4 12.2 12l-4.6 4.6L9 18l6-6z"/></svg>
        </span>
    </li>
</ul>
```

### Two-line list item

```html
<li class="list-item list-item--two-line">
    <span class="list-item__leading list-item__leading--avatar">AB</span>
    <span class="list-item__text">
        <span class="list-item__primary">Anna Becker</span>
        <span class="list-item__secondary">Sent you the trip itinerary</span>
    </span>
    <span class="list-item__trailing list-item__trailing--meta">Mon</span>
</li>
```

```css
.list { list-style: none; padding: 0; margin: 0; }
.list-item {
    display: flex;
    align-items: center;
    gap: 16px;
    min-height: 56px;
    padding: 8px 16px;
    color: var(--md-sys-color-on-surface);
    cursor: pointer;
    transition: background-color 150ms var(--md-sys-motion-easing-standard);
}
.list-item:hover  { background: color-mix(in srgb, var(--md-sys-color-on-surface) 4%, transparent); }
.list-item:active { background: color-mix(in srgb, var(--md-sys-color-on-surface) 8%, transparent); }
.list-item--two-line   { min-height: 72px; }
.list-item--three-line { min-height: 88px; align-items: flex-start; padding-top: 12px; }
.list-item__leading {
    width: 24px; height: 24px;
    display: inline-flex; align-items: center; justify-content: center;
    color: var(--md-sys-color-on-surface-variant);
    flex-shrink: 0;
}
.list-item__leading--avatar {
    width: 40px; height: 40px;
    border-radius: 50%;
    background: var(--md-sys-color-primary-container);
    color: var(--md-sys-color-on-primary-container);
    font: 500 var(--md-sys-typescale-title-medium) / 1 var(--font-roboto);
}
.list-item__text { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
.list-item__primary {
    font: 400 var(--md-sys-typescale-body-large) / 1.5 var(--font-roboto);
}
.list-item__secondary {
    font: 400 var(--md-sys-typescale-body-medium) / 1.43 var(--font-roboto);
    color: var(--md-sys-color-on-surface-variant);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.list-item__trailing {
    color: var(--md-sys-color-on-surface-variant);
    flex-shrink: 0;
}
.list-item__trailing--meta {
    font: 400 var(--md-sys-typescale-label-small) / 1 var(--font-roboto);
}
```

## Do / Don't

| Do | Don't |
|---|---|
| Use `surface-container-low` for elevated card fill (provides tonal overlay automatically). | Use a flat `surface` background and expect MD3 elevation to read. |
| Pick ONE card variant per group. | Mix elevated and filled cards in the same list. |
| Use 56dp min height for one-line list items (40dp content + 8dp top/bottom). | Use 44dp (that's iOS). |
| Keep secondary text to one ellipsized line. | Wrap to multiple lines — switch to a three-line item if needed. |
