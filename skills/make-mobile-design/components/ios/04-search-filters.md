## 5. Search Bar

```html
<!-- HTML -->
<div class="search-bar">
    <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
    <input type="text" class="search-input" placeholder="Search for files">
</div>
```

```css
/* CSS */
.search-bar {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    margin: var(--space-4) var(--space-5);
    padding: var(--space-3) var(--space-4);
    background: var(--gray-50);
    border: 1px solid var(--gray-200);
    border-radius: var(--radius-sm);
}

.search-icon {
    width: 18px;
    height: 18px;
    color: var(--gray-400);
    flex-shrink: 0;
}

.search-input {
    flex: 1;
    border: none;
    background: none;
    outline: none;
    font-family: var(--font-family);
    font-size: var(--text-base);
    color: var(--gray-900);
}

.search-input::placeholder {
    color: var(--gray-400);
}
```

---

## 6. Segmented Control (Tabs)

```html
<!-- HTML -->
<div class="segment-control">
    <button class="segment-item active">Summary</button>
    <button class="segment-item">Transcript</button>
    <button class="segment-item">Chat AI</button>
</div>
```

```css
/* CSS */
.segment-control {
    display: flex;
    gap: 0;
    margin: var(--space-5) var(--space-5) 0;
    border-bottom: 1px solid var(--gray-200);
}

.segment-item {
    flex: 1;
    padding: var(--space-3) var(--space-4);
    border: none;
    background: none;
    font-family: var(--font-family);
    font-size: var(--text-base);
    font-weight: 500;
    color: var(--gray-400);
    cursor: pointer;
    position: relative;
    transition: color 0.2s;
}

.segment-item.active {
    color: var(--color-primary);
    font-weight: 600;
}

.segment-item.active::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    right: 0;
    height: 2px;
    background: var(--color-primary);
    border-radius: 1px;
}
```

**JS for interactivity:**
```javascript
document.querySelectorAll('.segment-item').forEach(item => {
    item.addEventListener('click', function() {
        this.parentElement.querySelectorAll('.segment-item').forEach(s => s.classList.remove('active'));
        this.classList.add('active');
    });
});
```

---

## 7. Filter Tabs (Pill style)

```html
<!-- HTML -->
<div class="filter-tabs">
    <button class="filter-tab active">All</button>
    <button class="filter-tab">Favourite</button>
    <button class="filter-tab">Folder</button>
</div>
```

```css
/* CSS */
.filter-tabs {
    display: flex;
    gap: var(--space-2);
    padding: var(--space-4) var(--space-5);
}

.filter-tab {
    padding: var(--space-2) var(--space-5);
    border-radius: var(--radius-full);
    border: 1px solid var(--gray-200);
    background: white;
    font-family: var(--font-family);
    font-size: var(--text-base);
    font-weight: 500;
    color: var(--gray-500);
    cursor: pointer;
    transition: all 0.2s;
}

.filter-tab.active {
    background: var(--color-primary);
    border-color: var(--color-primary);
    color: white;
}
```
