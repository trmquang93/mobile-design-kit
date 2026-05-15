# A2. Android Status Bar

**Rule:** The status bar is provided by the device-frame scaffold (`scripts/create_android_template.py`) and is pinned with `position:absolute; top:0; z-index:50`. Do not redefine these properties, do not rewrite the status-bar HTML/CSS by hand, and never place the status bar inside a scrolling container (`.device-content`, body-level scroll, or any nested overflow region). The status bar must never scroll with content.

## Geometry

- **Height:** 24px (smaller than iOS's 59px).
- **Hole-punch camera:** a 14×14 circle centered horizontally at `top: 10px`, sits on top of the status bar via `z-index: 100`.
- **Content:** time on the left, signal/Wi-Fi/battery icons on the right. Font size = `--md-sys-typescale-label-medium` (12px), weight 500.
- **Color:** inherits `--md-sys-color-on-surface`. Inverts automatically in dark mode via the scaffold's `prefers-color-scheme: dark` block.

## Canonical Form (provided by scaffold)

```css
.status-bar {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4px 20px 0;
    font-size: var(--md-sys-typescale-label-medium);
    font-weight: 500;
    color: var(--md-sys-color-on-surface);
    z-index: 50;
    pointer-events: none;
}
```

## Status-Bar Safe Area (24px)

The scaffold sets `.device-content { padding-top: 0 }`. The 24px safe area belongs to the **first child** of `.device-content`, never to `.device-content` itself. This lets a top app bar's background fill behind the status bar to the very top edge — correct Android edge-to-edge behavior.

Pick one of these patterns for the first child:

1. **Top app bar (`.top-app-bar`)** — uses `padding-top: calc(24px + 8px)` so its background fills behind the status bar. See `03-navigation.md` §A3.
2. **Plain content** — first section adds 24px to its top padding.
3. **Full-bleed hero / photo** — no padding; image bleeds behind the status bar.

Do NOT add `padding-top: 24px` to `.device-content`. Do NOT use `margin-top: -24px` on the top app bar (breaks sticky pinning).

## Do / Don't

| Do | Don't |
|---|---|
| Leave the scaffold's `.status-bar` element alone. | Move it inside `.device-content`. |
| Let the first child own the 24px safe area. | Add 24px padding to `.device-content`. |
| Honor `pointer-events: none` so taps pass through. | Make the status bar interactive. |
| Use 12px / weight 500 type for the clock. | Use 17px (that's iOS). |
