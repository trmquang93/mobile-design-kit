# A24. Tablet Layout Wrappers (MD3 Expanded Window Class)

Layout wrappers for Pixel Tablet and other Android tablets at the
**expanded** window-size class (≥840dp). **Only load when form-factor =
tablet.** These are *wrappers* — fill cells with the existing Android
components (top app bar, list items, cards) unchanged.

MD3 patterns at expanded class:
- **Navigation rail** (80dp) replaces bottom navigation for global nav.
- **List-detail** is the canonical two-pane content layout (360dp list,
  flex detail).
- **Screen margins** bump to **24dp** at expanded class (from 16dp on
  compact phones).
- **Standard navigation drawer** is an option for 5+ destinations; modal
  drawer is also OK over a scrim.

Reference: `m3.material.io/foundations/layout/canonical-layouts/list-detail`.

---

## A24a. `.tablet-shell` — Nav Rail + Content

```html
<!-- First child of .device-content. -->
<div class="tablet-shell">
    <!-- Navigation rail from components/android/09-navigation-drawer.md §A23.
         Apply the 24dp top safe area via the rail's first inner element. -->
    <aside class="nav-rail" aria-label="Primary navigation">
        <!-- ... nav-rail items ... -->
    </aside>
    <main class="tablet-content">
        <!-- Top app bar + content -->
    </main>
</div>
```

```css
.tablet-shell {
    display: flex;
    height: 100%;
}

.tablet-content {
    flex: 1;
    min-width: 0;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    background: var(--md-sys-color-surface);
}

.tablet-content::-webkit-scrollbar { display: none; }
.tablet-content { scrollbar-width: none; }
```

**Notes:**
- The nav rail from §A23 is 80dp wide with the MD3 active-indicator pill.
- Apply `padding-top: calc(24px + 12px)` to the rail's first item so it
  clears the status bar.
- If the app has 5+ destinations, use a **standard navigation drawer**
  (360dp wide, always visible) in place of the rail.

---

## A24b. `.list-detail` — Two-Pane Content

```html
<main class="tablet-content">
    <!-- Top app bar (small/medium) from components/android/03-navigation.md -->
    <div class="list-detail">
        <section class="list-pane" aria-label="Items">
            <!-- Reuse .list-item rows -->
        </section>
        <section class="detail-pane-md" aria-label="Detail">
            <!-- Cards, content, etc. -->
        </section>
    </div>
</main>
```

```css
.list-detail {
    display: flex;
    gap: 24px;
    padding: 24px;
    height: 100%;
    box-sizing: border-box;
}

.list-pane {
    width: 360px;
    flex-shrink: 0;
    background: var(--md-sys-color-surface-container-low);
    border-radius: var(--md-sys-shape-corner-large);
    overflow-y: auto;
}

.detail-pane-md {
    flex: 1;
    min-width: 0;
    background: var(--md-sys-color-surface-container-lowest);
    border-radius: var(--md-sys-shape-corner-large);
    overflow-y: auto;
    padding: 24px;
}

.list-pane::-webkit-scrollbar,
.detail-pane-md::-webkit-scrollbar { display: none; }
.list-pane, .detail-pane-md { scrollbar-width: none; }
```

**Use when:** list-driven content with selectable rows and a detail view
(mail, settings, file browser).

---

## A24c. `.three-column` — Expanded Three-Column

For apps with three hierarchical levels (account → folder → message):

```html
<main class="tablet-content">
    <div class="three-column-md">
        <section class="list-pane list-pane--narrow">...</section>
        <section class="list-pane">...</section>
        <section class="detail-pane-md">...</section>
    </div>
</main>
```

```css
.three-column-md {
    display: flex;
    gap: 24px;
    padding: 24px;
    height: 100%;
    box-sizing: border-box;
}
.list-pane--narrow { width: 240px; }
```

Use sparingly — three columns only make sense when the middle column
holds real content, not just a header.

---

## Touch Targets

- 48×48dp minimum applies to tablet too. Nav-rail items are already
  56×56dp.
- Sidebar/drawer rows: keep `min-height: 56dp` (the MD3 list-item
  default).

---

## Do / Don't

- **Do** reuse the existing top app bar, list-item, card, FAB
  components inside both panes — they work unchanged at tablet widths.
- **Do** use 24dp screen padding (vs 16dp on phones) — encoded in the
  `.list-detail` snippet above.
- **Do** prefer `surface-container-low` for the list pane and
  `surface-container-lowest` for the detail pane (or invert if your
  brand calls for it) — the two-tone treatment is the MD3 hint that
  these are separate scroll regions.
- **Don't** use `backdrop-filter` / frosted glass — MD3 depth is tonal,
  not blurred. This applies to tablet identically to phone.
- **Don't** stack a bottom navigation bar with a nav rail. Pick one.
  Bottom nav at expanded class is allowed by MD3 but discouraged when
  rail/drawer can absorb the destinations.
- **Don't** drop the top app bar — even tablet content panes keep the
  MD3 top app bar pinned at the top of `.tablet-content`.
