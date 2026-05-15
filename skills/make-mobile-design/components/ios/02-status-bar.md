## 2. Status Bar (iOS)

Always include at the top of every screen.

**Rule:** The status bar is provided by the device-frame scaffold (`scripts/create_ios_template.py`) and is pinned with `position:absolute; top:0; z-index:50`. Do not redefine these properties, do not rewrite the status bar HTML/CSS by hand, and never place the status bar inside a scrolling container (e.g. `.device-content`, body-level scroll, or any nested overflow region). The status bar must never scroll with content.

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
        <svg width="20" height="13" viewBox="0 0 20 13" fill="currentColor"><path fill-rule="evenodd" clip-rule="evenodd" d="M19.3466 1.625C19.3466 1.00368 18.8654 0.5 18.2718 0.5H17.1969C16.6033 0.5 16.1221 1.00368 16.1221 1.625V11.375C16.1221 11.9963 16.6033 12.5 17.1969 12.5H18.2718C18.8654 12.5 19.3466 11.9963 19.3466 11.375V1.625ZM11.8565 2.9H12.9313C13.5249 2.9 14.0061 3.41577 14.0061 4.052V11.348C14.0061 11.9842 13.5249 12.5 12.9313 12.5H11.8565C11.2629 12.5 10.7817 11.9842 10.7817 11.348V4.052C10.7817 3.41577 11.2629 2.9 11.8565 2.9ZM7.49008 5.5H6.41527C5.82167 5.5 5.34046 6.02233 5.34046 6.66667V11.3333C5.34046 11.9777 5.82167 12.5 6.41527 12.5H7.49008C8.08368 12.5 8.56489 11.9777 8.56489 11.3333V6.66667C8.56489 6.02233 8.08368 5.5 7.49008 5.5ZM2.14962 7.9H1.07481C0.481208 7.9 0 8.41487 0 9.05V11.35C0 11.9851 0.481208 12.5 1.07481 12.5H2.14962C2.74322 12.5 3.22443 11.9851 3.22443 11.35V9.05C3.22443 8.41487 2.74322 7.9 2.14962 7.9Z"/></svg>
        <svg width="18" height="13" viewBox="26.9 0 17.3 13" fill="currentColor"><path fill-rule="evenodd" clip-rule="evenodd" d="M35.5408 3.02062C38.0469 3.02072 40.4571 3.92573 42.2734 5.54859C42.4102 5.67388 42.6288 5.6723 42.7635 5.54504L44.0709 4.30497C44.1391 4.24043 44.1771 4.153 44.1766 4.06204C44.176 3.97107 44.1369 3.88407 44.0679 3.82028C39.3008 -0.47342 31.7801 -0.47342 27.0129 3.82028C26.9439 3.88402 26.9047 3.971 26.9041 4.06197C26.9034 4.15293 26.9414 4.24038 27.0095 4.30497L28.3173 5.54504C28.4519 5.67249 28.6707 5.67407 28.8074 5.54859C30.6239 3.92562 33.0344 3.02061 35.5408 3.02062ZM35.539 7.16274C36.9067 7.16265 38.2255 7.66492 39.2393 8.57193C39.3765 8.70066 39.5925 8.69787 39.7261 8.56564L41.0232 7.27077C41.0915 7.20285 41.1294 7.11071 41.1285 7.01496C41.1275 6.91922 41.0877 6.82786 41.018 6.76132C37.9308 3.92401 33.1498 3.92401 30.0626 6.76132C29.9929 6.82786 29.9531 6.91926 29.9522 7.01504C29.9512 7.11081 29.9893 7.20294 30.0577 7.27077L31.3545 8.56564C31.4881 8.69787 31.7041 8.70066 31.8413 8.57193C32.8544 7.66552 34.1722 7.1633 35.539 7.16274ZM38.0803 9.90455C38.0823 10.008 38.0449 10.1076 37.9771 10.1801L35.7838 12.5894C35.7195 12.6602 35.6319 12.7 35.5404 12.7C35.4489 12.7 35.3613 12.6602 35.297 12.5894L33.1033 10.1801C33.0356 10.1076 32.9983 10.0079 33.0003 9.90447C33.0023 9.80107 33.0434 9.70315 33.114 9.63384C34.5147 8.34428 36.5661 8.34428 37.9669 9.63384C38.0373 9.70321 38.0784 9.80115 38.0803 9.90455Z"/></svg>
        <svg width="27" height="13" viewBox="52.5 0 27 13" fill="none"><rect opacity="0.35" x="52.5474" y="0.5" width="24" height="12" rx="3.8" stroke="currentColor"/><path opacity="0.4" d="M77.9473 4.66666V8.66666C78.752 8.32788 79.2753 7.53979 79.2753 6.66666C79.2753 5.79352 78.752 5.00543 77.9473 4.66666Z" fill="currentColor"/><rect x="53.8474" y="2" width="21" height="9" rx="2.5" fill="currentColor"/></svg>
    </div>
</div>
```

```css
/* CSS — canonical pinned form (provided by create_ios_template.py) */
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
