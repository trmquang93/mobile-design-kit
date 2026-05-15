# 31. Tablet Layout Wrappers (iPadOS)

iPad layout wrappers. **Only load when form-factor = tablet.** These are
*wrappers* — fill cells with the existing iOS components (list items, nav
headers, search bars, cards) unchanged. Tablet adds no new content
primitives, only layout shells.

Apple HIG patterns: iPad uses persistent sidebars on regular-width windows.
Two-pane split view (sidebar + detail) is the default for list-driven apps
(Mail, Notes, Settings). Three-column (sidebar + supplemental + detail) is
the canonical pattern for hierarchical content (Mail with mailbox →
thread list → message).

Sidebar widths follow HIG: 320pt minimum on iPad Pro 11", 375pt acceptable
for content-rich sidebars. The supplemental column (when present) is also
320pt. The detail pane is flex 1.

---

## 31a. `.split-view` — Two-Pane (Sidebar + Detail)

```html
<!-- Lives directly inside .device-content as the first child. -->
<div class="split-view">
    <aside class="sidebar-ipad" aria-label="Primary navigation">
        <!-- Section headers + list items from components/ios/05-content.md.
             Status-bar safe area belongs on the FIRST CHILD of the sidebar
             (or on the sidebar's own padding-top), per the iOS scaffold rule. -->
        <div class="sidebar-ipad__top">
            <h1 class="sidebar-ipad__title">Mailboxes</h1>
        </div>
        <!-- Reuse .list-item rows here -->
    </aside>
    <main class="detail-pane">
        <!-- Reuse .nav-header from 03-navigation.md, plus content. -->
    </main>
</div>
```

```css
.split-view {
    display: flex;
    height: 100%;
    min-height: 100%;
}

.sidebar-ipad {
    width: 320px;
    flex-shrink: 0;
    border-right: 1px solid var(--gray-200);
    background: var(--gray-50);
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
}

/* Sidebar internal padding-top absorbs the 24px iPad status-bar safe area. */
.sidebar-ipad__top {
    padding: calc(24px + var(--space-3)) var(--space-4) var(--space-3);
}

.sidebar-ipad__title {
    font-size: var(--text-largetitle);
    font-weight: 700;
    letter-spacing: -0.02em;
}

.detail-pane {
    flex: 1;
    min-width: 0;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    background: var(--color-bg);
}

.detail-pane::-webkit-scrollbar,
.sidebar-ipad::-webkit-scrollbar { display: none; }
.detail-pane, .sidebar-ipad { scrollbar-width: none; }
```

**Use when:** primary navigation has 4+ destinations and the user benefits
from seeing context while drilling into detail (mail, notes, settings).

**Don't:** stack a bottom tab bar with a sidebar — pick one navigation
metaphor per screen. HIG: tab bar on iPhone, sidebar on iPad.

---

## 31b. `.three-column` — Sidebar + Supplemental + Detail

```html
<div class="three-column">
    <aside class="sidebar-ipad sidebar-ipad--narrow" aria-label="Mailboxes">
        <!-- Top-level navigation (folders, accounts) -->
    </aside>
    <section class="supplemental-pane" aria-label="Thread list">
        <!-- Mid-level list (threads, items) -->
    </section>
    <main class="detail-pane">
        <!-- Selected item detail -->
    </main>
</div>
```

```css
.three-column {
    display: flex;
    height: 100%;
}

.sidebar-ipad--narrow { width: 280px; }

.supplemental-pane {
    width: 360px;
    flex-shrink: 0;
    border-right: 1px solid var(--gray-200);
    background: var(--color-bg);
    overflow-y: auto;
}
.supplemental-pane::-webkit-scrollbar { display: none; }
.supplemental-pane { scrollbar-width: none; }
```

**Use when:** content is hierarchical with three meaningful levels. Skip
if the middle column would just hold a header + a single list — collapse
to two-pane in that case.

---

## 31c. Single-Pane Tablet

A tablet screen that doesn't need split navigation (a focused editor,
onboarding flow, presentation view) skips `.split-view` entirely. Use the
existing iOS page structure inside `.device-content` as you would on
phone, just at the larger viewport. The scaffold's `.device-content`
already fills the iPad frame; no additional wrapper is needed.

For a landscape immersive view, set `padding: 0 max(40px, env(safe-area-inset-left))`
on the first child so content tracks the iPad's wider canvas without
edge-hugging.

---

## Liquid Glass on iPad Sidebars

Per HIG, the sidebar background may use the Liquid Glass material on
iPadOS when stacked over photographic content (Photos app pattern). Apply
the recipe from `00-liquid-glass.md` to `.sidebar-ipad` only when the
detail pane has full-bleed media behind it. Otherwise keep the sidebar on
the standard `--gray-50` surface.

**Copy-to-Figma caveat:** glass surfaces paste as opaque rects. The
sidebar's 1px right border survives. If exporting to Figma matters, skip
the glass variant.

---

## Sidebar Row Pattern

When sidebar rows are `<button>` elements (the recommended HIG pattern for
keyboard / VoiceOver), reset the default UA button chrome — otherwise
each row paints as a rounded gray rectangle with a border, which is not
what HIG wants:

```css
.sidebar-row {
    display: flex; align-items: center; gap: 12px;
    width: 100%;
    padding: 10px 24px; min-height: 44px;
    color: var(--gray-800);
    font-size: var(--text-body);
    font-family: inherit;
    text-align: left;
    background: transparent;
    border: none;
    appearance: none;
    -webkit-appearance: none;
    cursor: pointer;
}
.sidebar-row:hover { background: rgba(0,0,0,0.04); }
.sidebar-row.is-active { background: var(--color-primary-light); color: var(--color-primary); }
```

Forgetting the reset is the most common iPad-sidebar bug — verify rows
look flat (no border, no UA gray fill) before shipping.

## Touch & Pointer Targets

- Sidebar row min-height stays at 44px (HIG iPad touch target).
- Three-column screens get an implicit pointer-hover state since iPadOS
  supports trackpad/Magic Keyboard — keep `.list-item:hover` styles in
  place.

---

## Do / Don't

- **Do** reuse `.nav-header`, `.list-item`, `.section-header`, `.search-bar`
  inside both panes — they work unchanged at iPad widths.
- **Do** keep `.sidebar-ipad` and `.detail-pane` as siblings of each
  other under a single `.split-view` wrapper that is itself the first
  child of `.device-content`.
- **Don't** introduce a separate `.device-content` per pane — the
  scaffold's single scroll container handles outer device chrome; the
  panes own their own scroll regions via `overflow-y: auto`.
- **Don't** use a top tab bar across the whole iPad frame. Use sidebar
  navigation for primary destinations.
