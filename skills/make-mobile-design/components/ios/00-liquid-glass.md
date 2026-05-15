# 0. Liquid Glass — Shared Recipe

Single source of truth for the Liquid Glass material used on the navigation
layer (nav header, bottom tab bar, contextual toolbars, FAB, sheets).
Every glass surface in this skill MUST use this recipe — no ad-hoc
`backdrop-filter` formulas elsewhere.

The effect is an SVG-displacement refractive glass adapted from
[lucasromerodb/liquid-glass-effect-macos](https://github.com/lucasromerodb/liquid-glass-effect-macos),
tuned for capsule-shaped iOS chrome.

## Placement rules (HIG)

- Glass is allowed on the **navigation layer only**: nav header, bottom
  tab bar, floating toolbars, FAB, modal sheets, alerts, segmented
  controls.
- Never on content surfaces — lists, cards, media tiles, modal bodies.
- Never stack glass on glass.
- Capsule (`border-radius: 9999px`) or fully rounded (16–24px) shapes only.
- Tint subtly with the accent color at low opacity. Never purple.

## SVG filter defs

Add this once per HTML page, immediately inside `<body>`. The filter id
`glass-distortion` is global — do not rename.

```html
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <filter id="glass-distortion" x="0%" y="0%" width="100%" height="100%">
    <feImage preserveAspectRatio="none" result="map"
      href='data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" preserveAspectRatio="none"><defs>
        <linearGradient id="x" x1="0" y1="0.5" x2="1" y2="0.5">
            <stop offset="0" stop-color="rgb(255,0,0)"/>
            <stop offset="0.15" stop-color="rgb(128,0,0)"/>
            <stop offset="0.85" stop-color="rgb(128,0,0)"/>
            <stop offset="1" stop-color="rgb(255,0,0)"/>
        </linearGradient>
        <linearGradient id="y" x1="0.5" y1="0" x2="0.5" y2="1">
            <stop offset="0" stop-color="rgb(0,255,0)"/>
            <stop offset="0.15" stop-color="rgb(0,128,0)"/>
            <stop offset="0.85" stop-color="rgb(0,128,0)"/>
            <stop offset="1" stop-color="rgb(0,255,0)"/>
        </linearGradient>
    </defs><rect width="100" height="100" fill="url(%23x)"/><rect width="100" height="100" fill="url(%23y)" style="mix-blend-mode:screen"/></svg>'/>
    <feGaussianBlur in="map" stdDeviation="2" result="smoothed"/>
    <feDisplacementMap in="SourceGraphic" in2="smoothed"
                       scale="40" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
</svg>
```

## CSS

```css
.glass {
    position: relative;
    /* Diagonal sheen baked into the fill so the pill reads as glass
       even when the backdrop is uniform (white, solid, etc.). */
    background:
        linear-gradient(135deg,
            rgba(255, 255, 255, 0.22) 0%,
            rgba(255, 255, 255, 0.06) 28%,
            rgba(255, 255, 255, 0.04) 72%,
            rgba(255, 255, 255, 0.28) 100%);
    border: 1px solid rgba(255, 255, 255, 0.4);
    border-radius: 9999px; /* capsule */
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.85),
        inset 0 -1px 1px rgba(255, 255, 255, 0.30),
        inset 0 0 0 1px rgba(255, 255, 255, 0.05),
        0 10px 28px rgba(0, 0, 0, 0.18),
        0 2px 6px rgba(0, 0, 0, 0.10);
    backdrop-filter: url(#glass-distortion) saturate(140%);
    -webkit-backdrop-filter: saturate(180%) blur(20px); /* iOS Safari fallback */
}

/* Browsers that can't run url() inside backdrop-filter
   (iOS Safari, older Chromium) keep the original flat-blur look. */
@supports not (backdrop-filter: url(#glass-distortion)) {
    .glass {
        background: rgba(255, 255, 255, 0.55);
        backdrop-filter: saturate(180%) blur(20px);
        -webkit-backdrop-filter: saturate(180%) blur(20px);
    }
}

@media (prefers-color-scheme: dark) {
    .glass {
        background: rgba(28, 28, 30, 0.55);
        border-color: rgba(255, 255, 255, 0.08);
    }
}

@media (prefers-reduced-transparency: reduce) {
    .glass {
        backdrop-filter: none;
        -webkit-backdrop-filter: none;
        background: rgba(255, 255, 255, 0.92);
    }
    @media (prefers-color-scheme: dark) {
        .glass { background: rgba(28, 28, 30, 0.96); }
    }
}
```

## Tuning notes

- The displacement map is a **gradient image**, not fractal noise. Two
  crossed linear gradients (red horizontal, green vertical via
  `mix-blend-mode: screen`) produce the lens shape: bright→dim→bright
  ramps along each axis push pixels outward at the capsule's rim and
  leave the centre nearly identity. That rim-only warp is what reads
  as "glass" on small pills.
- `scale="40"` is tuned for capsule-shaped chrome (44–60px tall). Lower
  it if the warp eats text on a particular surface; raise it for hero
  glass over photography.
- `feGaussianBlur stdDeviation="2"` on the map only — this softens the
  gradient steps so the refraction reads as curved, not banded. The
  default recipe does not blur `SourceGraphic`; the displacement alone
  is the effect, and a heavy blur on top washes it back to flat glass.
  If you specifically want a *frosted* glass surface (blur on top of
  the refraction), use the `glass-distortion-frosted` variant below —
  do NOT chain `blur()` in CSS `backdrop-filter` next to `url(...)`,
  because the order across SVG and CSS filters is implementation-
  dependent and the blur typically ends up being warped by the
  displacement instead of layered on top of it.
- The diagonal `linear-gradient` sheen + bright top-rim inset highlight
  is what reads as "glass body" when the fill is mostly transparent.

## CRITICAL: do not animate transforms on glass ancestors

`backdrop-filter: url(#filter)` with `feDisplacementMap` requires the
filtered element to share a compositor layer with the backdrop content.
**Any `transform`, `will-change: transform`, `filter`, or `opacity < 1`
on the glass element OR any of its ancestors promotes it to a separate
compositor layer — and `feDisplacementMap` silently fails to identity
output (no warp, the backdrop passes through unchanged).** Other
backdrop-filter functions (`blur`, `saturate`) keep working because
they use a simpler GPU path; only the SVG `url()` path breaks.

Symptoms: pill renders, sheen and rim highlight visible, but the
backdrop content under the pill is identical to outside it.

Common offenders, all triggered the same identity-fallback bug in this
codebase:

```css
/* ❌ Breaks the displacement (translateY → compositor layer): */
.toolbar { animation: slide-in 320ms ease-out both; }
@keyframes slide-in {
    from { transform: translateY(120%); opacity: 0; }
    to   { transform: translateY(0);    opacity: 1; }
}

/* ✅ Opacity-only entrance is safe: */
.toolbar { animation: fade-in 320ms ease-out both; }
@keyframes fade-in {
    from { opacity: 0; }
    to   { opacity: 1; }
}
```

If you need a translate-style entrance, animate a **non-glass wrapper**
that contains the glass element, so the wrapper takes the layer
promotion and the glass element stays in the parent compositor.

## Variants

- **Tinted glass** (active state): add `background: rgba(<accent>, 0.18)`.
  The tab-bar emitter in `scripts/add_ios_tabbar.py` does this for the
  active item.
- **Clear glass** (over photography): drop the white fill, keep only
  the filter and border.
- **Frosted glass** (refraction + soft blur): use when the surface sits
  over busy/text-heavy content and the rim-only displacement isn't
  enough to keep foreground elements legible — e.g. a contextual
  toolbar over a scrolling list. See recipe below.

### Frosted glass recipe

The blur MUST run *inside* the SVG filter chain, taking
`feDisplacementMap`'s output as input. That guarantees the pipeline
order: backdrop → displace → blur → composite. Chaining
`blur()` in the CSS `backdrop-filter` next to `url(#glass-distortion)`
does NOT do this reliably — the displacement ends up warping the
already-blurred image (or the blur smears the displacement waves), and
the result varies by engine.

Add a second filter id alongside the default one (do not modify
`glass-distortion` — keep the rim-only look as the codebase default):

```html
<filter id="glass-distortion-frosted" x="0%" y="0%" width="100%" height="100%">
  <!-- Same gradient map as glass-distortion: -->
  <feImage preserveAspectRatio="none" result="map" href='...same data URL...'/>
  <feGaussianBlur in="map" stdDeviation="2" result="smoothed"/>
  <feDisplacementMap in="SourceGraphic" in2="smoothed"
                     scale="40" xChannelSelector="R" yChannelSelector="G"
                     result="displaced"/>
  <!-- Post-displacement blur. Tune stdDeviation per surface (1.5–3
       reads as frosted; >4 starts to look like flat blur and loses
       the refraction). -->
  <feGaussianBlur in="displaced" stdDeviation="1.5"/>
</filter>
```

Then on the surface:

```css
.glass--frosted {
    /* same as .glass, but: */
    backdrop-filter: url(#glass-distortion-frosted) saturate(140%);
}
```

Do NOT add a CSS `blur()` on top — the SVG filter already produced
the final blurred-displaced image. Stacking another blur on top of
that wastes a layer and risks promoting the element to a separate
compositor (which kills the displacement, see next section).

## Browser support

| Engine | Refractive look | Fallback |
|---|---|---|
| Chromium desktop (Chrome / Edge / Brave) | ✅ | — |
| Safari macOS 17+ | ⚠️ partial | — |
| iOS Safari | ❌ | flat blur |
| Firefox | ❌ | flat blur |

These mockups are designed for desktop Chromium rendering (Playwright
in `examples/capture.mjs`). Anyone opening the HTML directly on an
iPhone sees the flat-blur fallback — that is intentional.

## Don'ts

- Don't apply `.glass` to content cards, list rows, or media tiles.
- Don't stack a glass tab bar over a glass nav header without a clear
  spatial gap.
- Don't invent a different `backdrop-filter` formula in a new
  component — extend this recipe or add a variant here.
- Don't tint with purple.
