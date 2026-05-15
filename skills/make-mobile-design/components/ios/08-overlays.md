## 18. Bottom Sheet

```html
<!-- HTML -->
<div class="sheet-overlay" id="sheet">
    <div class="sheet">
        <div class="sheet-handle"></div>
        <div class="sheet-header">
            <h3 class="sheet-title">Sheet Title</h3>
            <button class="sheet-done" onclick="document.getElementById('sheet').style.display='none'">Done</button>
        </div>
        <div class="sheet-body">
            <!-- Content here -->
        </div>
    </div>
</div>
```

```css
/* CSS */
.sheet-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.3);
    display: flex;
    align-items: flex-end;
    justify-content: center;
    z-index: 200;
}

.sheet {
    width: 100%;
    max-width: 430px;
    background: white;
    border-radius: var(--radius-md) var(--radius-md) 0 0;
    padding: 0 var(--space-5) var(--space-6);
    max-height: 70vh;
    overflow-y: auto;
}

.sheet-handle {
    width: 36px;
    height: 4px;
    background: var(--gray-300);
    border-radius: 2px;
    margin: var(--space-3) auto var(--space-4);
}

.sheet-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--space-4);
}

.sheet-title {
    font-size: var(--text-lg);
    font-weight: 600;
}

.sheet-done {
    font-size: var(--text-base);
    font-weight: 600;
    color: var(--color-primary);
    background: none;
    border: none;
    cursor: pointer;
    font-family: var(--font-family);
}

.sheet-body {
    padding-bottom: env(safe-area-inset-bottom, 0px);
}
```

---

## 19. Action Menu (Dropdown/Popover)

```html
<!-- HTML -->
<div class="action-menu">
    <div class="action-menu-item">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3h18v18H3z"/><path d="M12 8v8"/><path d="M8 12h8"/></svg>
        <span>Move to folder</span>
    </div>
    <div class="action-menu-item">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z"/></svg>
        <span>Translate</span>
    </div>
    <div class="action-menu-divider"></div>
    <div class="action-menu-item destructive">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
        <span>Delete</span>
    </div>
</div>
```

```css
/* CSS */
.action-menu {
    background: white;
    border-radius: var(--radius-sm);
    box-shadow: var(--shadow-lg);
    padding: var(--space-2) 0;
    min-width: 220px;
    border: 1px solid var(--gray-100);
}

.action-menu-item {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    padding: var(--space-3) var(--space-5);
    font-size: var(--text-base);
    color: var(--gray-800);
    cursor: pointer;
    transition: background 0.15s;
}

.action-menu-item:hover {
    background: var(--gray-50);
}

.action-menu-item svg {
    width: 20px;
    height: 20px;
    flex-shrink: 0;
}

.action-menu-item.destructive {
    color: var(--color-error);
}

.action-menu-divider {
    height: 1px;
    background: var(--gray-100);
    margin: var(--space-2) 0;
}
```
