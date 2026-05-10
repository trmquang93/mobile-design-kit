## 8. Section Header

```html
<!-- HTML -->
<div class="section-header">
    <span class="section-label">SECTION TITLE</span>
    <button class="section-link">View all</button> <!-- optional -->
</div>
```

```css
/* CSS */
.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-5) var(--space-5) var(--space-3);
}

.section-label {
    font-size: var(--text-footnote);
    font-weight: 400;
    color: var(--gray-500);
    /* iOS grouped-list section headers are sentence-case, not uppercase. */
}

.section-link {
    font-size: var(--text-body);
    font-weight: 400;
    color: var(--color-primary);
    cursor: pointer;
    background: none;
    border: none;
    font-family: var(--font-family);
}
```

---

## 9. Content Card

```html
<!-- HTML -->
<div class="card">
    <div class="card-header">
        <h3 class="card-title">Card Title</h3>
    </div>
    <div class="card-body">
        <p class="card-text">Card content goes here.</p>
    </div>
</div>
```

```css
/* CSS */
.card {
    background: white;
    border-radius: var(--radius-md);
    border: 1px solid var(--gray-200);
    margin: 0 var(--space-5);
    overflow: hidden;
}

.card-header {
    padding: var(--space-5) var(--space-5) 0;
}

.card-title {
    font-size: var(--text-title3);
    font-weight: 700;
    line-height: 1.2;
}

.card-body {
    padding: var(--space-4) var(--space-5) var(--space-5);
}

.card-text {
    font-size: var(--text-body);
    line-height: 1.4;
    color: var(--gray-700);
}
```

---

## 10. List Item (Recording/File row)

```html
<!-- HTML -->
<div class="list-item">
    <div class="list-item-icon blue">
        <!-- Insert icon SVG here -->
    </div>
    <div class="list-item-content">
        <div class="list-item-title">Item Title</div>
        <div class="list-item-meta">
            <span>45:12</span>
            <span>12/10/2023</span>
        </div>
    </div>
    <div class="list-item-trailing">
        <button class="icon-btn-sm">
            <svg viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="5" r="1.5"/><circle cx="12" cy="12" r="1.5"/><circle cx="12" cy="19" r="1.5"/></svg>
        </button>
    </div>
</div>
```

```css
/* CSS */
.list-item {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    padding: var(--space-3) var(--space-4);
    min-height: 44px;
    cursor: pointer;
    transition: background 0.15s;
}

.list-item:hover {
    background: var(--gray-50);
}

.list-item-icon {
    width: 44px;
    height: 44px;
    border-radius: var(--radius-xs);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.list-item-icon svg {
    width: 20px;
    height: 20px;
}

.list-item-icon.blue {
    background: var(--color-primary-light);
    color: var(--color-primary);
}

.list-item-icon.green {
    background: var(--color-success-light);
    color: var(--color-success);
}

.list-item-icon.orange {
    background: var(--color-warning-light);
    color: var(--color-warning);
}

.list-item-icon.purple {
    background: var(--color-info-light);
    color: var(--color-info);
}

.list-item-content {
    flex: 1;
    min-width: 0;
}

.list-item-title {
    font-size: var(--text-body);
    font-weight: 400;
    color: var(--gray-900);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.list-item-meta {
    font-size: var(--text-footnote);
    color: var(--gray-500);
    margin-top: 2px;
    display: flex;
    align-items: center;
    gap: var(--space-2);
}

.list-item-trailing {
    flex-shrink: 0;
}

.icon-btn-sm {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    background: none;
    cursor: pointer;
    color: var(--gray-400);
    border-radius: 50%;
}

.icon-btn-sm svg {
    width: 16px;
    height: 16px;
}
```
