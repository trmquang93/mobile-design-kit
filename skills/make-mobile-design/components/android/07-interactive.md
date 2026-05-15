# A15. Switch / Checkbox / Radio + A16. Slider + A17. Progress + A18. FAB

## A15. Switch (THE Android-vs-iOS giveaway control)

MD3 switches have a much wider track and a thumb that grows when ON. The geometry is the single clearest signal that a screen is Android, not iOS — get it right.

```html
<label class="switch">
    <input type="checkbox" class="switch__input" checked>
    <span class="switch__track">
        <span class="switch__thumb"></span>
    </span>
</label>
```

```css
.switch { display: inline-block; cursor: pointer; }
.switch__input { position: absolute; opacity: 0; pointer-events: none; }
.switch__track {
    display: block;
    width: 52px;
    height: 32px;
    border-radius: var(--md-sys-shape-corner-full);
    background: var(--md-sys-color-surface-container-highest);
    border: 2px solid var(--md-sys-color-outline);
    position: relative;
    transition: background-color 150ms var(--md-sys-motion-easing-standard),
                border-color 150ms var(--md-sys-motion-easing-standard);
}
.switch__thumb {
    position: absolute;
    top: 50%;
    left: 6px;
    transform: translateY(-50%);
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: var(--md-sys-color-outline);
    transition: transform 200ms var(--md-sys-motion-easing-emphasized),
                background-color 200ms var(--md-sys-motion-easing-emphasized),
                width 200ms var(--md-sys-motion-easing-emphasized),
                height 200ms var(--md-sys-motion-easing-emphasized),
                left 200ms var(--md-sys-motion-easing-emphasized);
}
.switch__input:checked + .switch__track {
    background: var(--md-sys-color-primary);
    border-color: var(--md-sys-color-primary);
}
.switch__input:checked + .switch__track .switch__thumb {
    width: 24px;
    height: 24px;
    left: 24px;
    background: var(--md-sys-color-on-primary);
}
```

## A15.b — Checkbox

```html
<label class="checkbox">
    <input type="checkbox" class="checkbox__input" checked>
    <span class="checkbox__box"></span>
    <span class="checkbox__label">I agree to the terms</span>
</label>
```

```css
.checkbox { display: inline-flex; align-items: center; gap: 12px; cursor: pointer; min-height: 48px; }
.checkbox__input { position: absolute; opacity: 0; pointer-events: none; }
.checkbox__box {
    width: 18px; height: 18px;
    border: 2px solid var(--md-sys-color-on-surface-variant);
    border-radius: 2px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: background-color 150ms, border-color 150ms;
}
.checkbox__input:checked + .checkbox__box {
    background: var(--md-sys-color-primary);
    border-color: var(--md-sys-color-primary);
}
.checkbox__input:checked + .checkbox__box::after {
    content: "";
    width: 12px; height: 6px;
    border-left: 2px solid var(--md-sys-color-on-primary);
    border-bottom: 2px solid var(--md-sys-color-on-primary);
    transform: rotate(-45deg) translate(1px, -1px);
}
.checkbox__label { font: 400 var(--md-sys-typescale-body-large) / 1.5 var(--font-roboto); }
```

## A15.c — Radio

```html
<label class="radio">
    <input type="radio" name="g" class="radio__input" checked>
    <span class="radio__dot"></span>
    Option A
</label>
```

```css
.radio { display: inline-flex; align-items: center; gap: 12px; cursor: pointer; min-height: 48px; }
.radio__input { position: absolute; opacity: 0; }
.radio__dot {
    width: 20px; height: 20px;
    border-radius: 50%;
    border: 2px solid var(--md-sys-color-on-surface-variant);
    display: inline-flex;
    align-items: center;
    justify-content: center;
}
.radio__input:checked + .radio__dot { border-color: var(--md-sys-color-primary); }
.radio__input:checked + .radio__dot::after {
    content: "";
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--md-sys-color-primary);
}
```

## A16. Slider

```html
<input type="range" class="slider" min="0" max="100" value="40">
```

```css
.slider {
    -webkit-appearance: none;
    appearance: none;
    width: 100%;
    height: 16px;
    background: transparent;
    cursor: pointer;
}
.slider::-webkit-slider-runnable-track {
    height: 4px;
    background: var(--md-sys-color-surface-container-highest);
    border-radius: var(--md-sys-shape-corner-full);
}
.slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 4px;
    height: 44px;
    background: var(--md-sys-color-primary);
    border-radius: var(--md-sys-shape-corner-full);
    margin-top: -20px;
}
.slider::-moz-range-track {
    height: 4px;
    background: var(--md-sys-color-surface-container-highest);
    border-radius: var(--md-sys-shape-corner-full);
}
.slider::-moz-range-thumb {
    width: 4px;
    height: 44px;
    background: var(--md-sys-color-primary);
    border: none;
    border-radius: var(--md-sys-shape-corner-full);
}
```

## A17. Progress

### Linear progress

```html
<div class="progress-linear" role="progressbar" aria-valuenow="65" aria-valuemin="0" aria-valuemax="100">
    <span class="progress-linear__bar" style="width: 65%"></span>
</div>
```

```css
.progress-linear {
    height: 4px;
    background: var(--md-sys-color-surface-container-highest);
    border-radius: var(--md-sys-shape-corner-full);
    overflow: hidden;
}
.progress-linear__bar {
    display: block;
    height: 100%;
    background: var(--md-sys-color-primary);
    border-radius: inherit;
    transition: width 250ms var(--md-sys-motion-easing-standard);
}
```

### Circular progress (indeterminate)

```html
<svg class="progress-circular" viewBox="0 0 32 32" aria-label="Loading">
    <circle cx="16" cy="16" r="13" fill="none" stroke-width="3.5" stroke-linecap="round"/>
</svg>
```

```css
.progress-circular {
    width: 40px; height: 40px;
    color: var(--md-sys-color-primary);
    animation: pc-rotate 1.4s linear infinite;
}
.progress-circular circle {
    stroke: currentColor;
    stroke-dasharray: 80;
    stroke-dashoffset: 60;
    animation: pc-dash 1.4s ease-in-out infinite;
}
@keyframes pc-rotate { to { transform: rotate(360deg); } }
@keyframes pc-dash {
    0% { stroke-dashoffset: 80; }
    50% { stroke-dashoffset: 20; }
    100% { stroke-dashoffset: 80; }
}
@media (prefers-reduced-motion: reduce) {
    .progress-circular, .progress-circular circle { animation: none; }
}
```

## A18. FAB (four variants)

```html
<button class="fab" aria-label="Compose">                         <!-- regular -->
    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04a1 1 0 0 0 0-1.41l-2.34-2.34a1 1 0 0 0-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>
</button>

<button class="fab fab--small" aria-label="Add">                   <!-- small -->
    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
</button>

<button class="fab fab--large" aria-label="Compose">               <!-- large -->
    <svg width="36" height="36" viewBox="0 0 24 24" fill="currentColor"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04a1 1 0 0 0 0-1.41l-2.34-2.34a1 1 0 0 0-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>
</button>

<button class="fab fab--extended">                                  <!-- extended -->
    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
    Compose
</button>
```

```css
.fab {
    position: absolute;
    right: 16px;
    bottom: calc(80px + 24px + 16px);   /* above bottom-nav (80px) + gesture-nav clearance (24px) + 16px gap */
    width: 56px;
    height: 56px;
    border-radius: var(--md-sys-shape-corner-large);
    background: var(--md-sys-color-primary-container);
    color: var(--md-sys-color-on-primary-container);
    border: none;
    cursor: pointer;
    box-shadow: var(--md-sys-elevation-level3);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    z-index: 30;
    transition: box-shadow 150ms var(--md-sys-motion-easing-standard);
}
.fab:hover  { box-shadow: var(--md-sys-elevation-level4); }
.fab:active { box-shadow: var(--md-sys-elevation-level3); }
.fab--small  { width: 40px; height: 40px; border-radius: var(--md-sys-shape-corner-medium); }
.fab--large  { width: 96px; height: 96px; border-radius: var(--md-sys-shape-corner-extra-large); }
.fab--extended {
    width: auto;
    height: 56px;
    padding: 0 16px 0 16px;
    border-radius: var(--md-sys-shape-corner-large);
    gap: 12px;
    font: 500 var(--md-sys-typescale-label-large) / 1 var(--font-roboto);
}
```

## Do / Don't

| Do | Don't |
|---|---|
| Use the wide-track MD3 switch geometry. | Reuse an iOS-style switch (smaller track, equal thumb). |
| Place one FAB max per screen. | Multiple FABs competing for attention. |
| Use `primary-container` for FAB (MD3 default). | Use `primary` directly — that's higher emphasis than FAB warrants. |
| 48dp minimum tap target for switch / checkbox / radio. | 44px (iOS). |
| Use indeterminate spinner for unknown durations. | Show a fake-progress determinate bar. |
