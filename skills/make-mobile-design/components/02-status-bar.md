## 2. Status Bar (iOS)

Always include at the top of every screen.

**Rule:** The status bar is provided by the device-frame scaffold (`scripts/create_device_template.py`) and is pinned with `position:absolute; top:0; z-index:50`. Do not redefine these properties, do not rewrite the status bar HTML/CSS by hand, and never place the status bar inside a scrolling container (e.g. `.device-content`, body-level scroll, or any nested overflow region). The status bar must never scroll with content.

### Status-bar safe area (59px)

The scaffold's `.device-content` has `padding-top: 0`. The 59px reserved for the status bar is the **first child's** responsibility, not the container's. This is so a nav header / glass top bar / hero image can render its background behind the status bar to the very top edge — correct iOS behavior.

Three legal patterns for the first child:

1. **`.nav-header` (back/title/actions)** — uses `padding-top: calc(59px + var(--space-2))`, background fills behind status bar. See §3a in `03-navigation.md`.
2. **`.page-header` (large title) or any first content section** — add `padding-top: calc(59px + <design-spacing>)` to its existing top padding. The page background continues behind the status bar naturally.
3. **Full-bleed hero / photo / map** — let the media start at y=0 and bleed behind the status bar. Add a transparent `.nav-header.transparent` on top if you need back/action buttons. See §3a-i in `03-navigation.md`.

Never set `padding-top: 59px` back on `.device-content` — it breaks the top-edge fill for nav headers and reintroduces the status-bar seam bug.

```html
<!-- HTML -->
<div class="status-bar">
    <span class="status-bar-time">9:41</span>
    <div class="status-bar-icons">
        <svg width="16" height="12" viewBox="0 0 16 12" fill="currentColor"><rect x="0" y="3" width="3" height="9" rx="1"/><rect x="4.5" y="2" width="3" height="10" rx="1"/><rect x="9" y="0" width="3" height="12" rx="1"/><rect x="13" y="1" width="3" height="11" rx="1"/></svg>
        <svg width="16" height="12" viewBox="0 0 16 12" fill="currentColor"><path d="M8 3C10.7 3 13.1 4.2 14.7 6.1L16 4.8C14 2.5 11.2 1 8 1S2 2.5 0 4.8L1.3 6.1C2.9 4.2 5.3 3 8 3Z"/><path d="M8 7C9.5 7 10.9 7.6 11.9 8.6L13.2 7.3C11.8 5.9 10 5 8 5S4.2 5.9 2.8 7.3L4.1 8.6C5.1 7.6 6.5 7 8 7Z"/><circle cx="8" cy="11" r="1.5"/></svg>
        <svg width="25" height="12" viewBox="0 0 25 12" fill="currentColor"><rect x="0" y="1" width="21" height="10" rx="2" stroke="currentColor" stroke-width="1" fill="none"/><rect x="22" y="4" width="2" height="4" rx="1"/><rect x="2" y="3" width="17" height="6" rx="1"/></svg>
    </div>
</div>
```

```css
/* CSS — canonical pinned form (provided by create_device_template.py) */
.status-bar {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 59px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 24px 8px;
    z-index: 50;
    pointer-events: none;
}

.status-bar-time {
    font-size: var(--text-md);
    font-weight: 600;
}

.status-bar-icons {
    display: flex;
    gap: 6px;
    align-items: center;
}
```
