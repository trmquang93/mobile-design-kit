## 3. Navigation Header

### 3a. Back + Title + Actions (Detail screens)

```html
<!-- HTML -->
<div class="nav-header">
    <button class="nav-back">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg>
    </button>
    <h1 class="nav-title">Screen Title</h1>
    <div class="nav-actions">
        <button class="nav-action-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>
        </button>
        <button class="nav-action-btn">
            <svg viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="5" r="1.5"/><circle cx="12" cy="12" r="1.5"/><circle cx="12" cy="19" r="1.5"/></svg>
        </button>
    </div>
</div>
```

```css
/* CSS */
.nav-header {
    display: flex;
    align-items: center;
    padding: var(--space-2) var(--space-5);
    gap: var(--space-3);
}

.nav-back {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    border: none;
    background: none;
    cursor: pointer;
    color: var(--gray-900);
}

.nav-back svg {
    width: 22px;
    height: 22px;
}

.nav-title {
    flex: 1;
    font-size: var(--text-lg);
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.nav-actions {
    display: flex;
    gap: var(--space-1);
}

.nav-action-btn {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    border: none;
    background: none;
    cursor: pointer;
    color: var(--gray-600);
    transition: background 0.2s;
}

.nav-action-btn:hover {
    background: var(--gray-100);
}

.nav-action-btn svg {
    width: 20px;
    height: 20px;
}
```

### 3b. Large Title Header (Top-level screens)

```html
<!-- HTML -->
<div class="page-header">
    <h1 class="page-title">Page Title</h1>
    <p class="page-subtitle">Description text</p>
</div>
```

```css
/* CSS */
.page-header {
    padding: var(--space-4) var(--space-5) 0;
}

.page-title {
    font-size: var(--text-3xl);
    font-weight: 700;
    line-height: 1.2;
    color: var(--gray-900);
}

.page-subtitle {
    font-size: var(--text-base);
    color: var(--gray-500);
    margin-top: var(--space-1);
}
```

---

## 4. Bottom Tab Bar

```html
<!-- HTML -->
<div class="tab-bar">
    <button class="tab-item active">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>
        <span>Home</span>
    </button>
    <button class="tab-item">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13 2 13 9 20 9"/></svg>
        <span>Files</span>
    </button>
    <button class="tab-item">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
        <span>Setting</span>
    </button>
</div>
```

```css
/* CSS */
.tab-bar {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 430px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding: var(--space-2) 0 calc(var(--space-5) + env(safe-area-inset-bottom, 0px));
    background: white;
    border-top: 1px solid var(--gray-200);
    z-index: 50;
}

.tab-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-1);
    padding: var(--space-2) var(--space-4);
    border: none;
    background: none;
    cursor: pointer;
    color: var(--gray-400);
    font-family: var(--font-family);
    transition: color 0.2s;
}

.tab-item svg {
    width: 22px;
    height: 22px;
}

.tab-item span {
    font-size: var(--text-xs);
    font-weight: 500;
}

.tab-item.active {
    color: var(--color-primary);
}
```

**Usage note:** When a screen has a tab bar, add `padding-bottom: 80px` to `body` to prevent content from being hidden behind it.
