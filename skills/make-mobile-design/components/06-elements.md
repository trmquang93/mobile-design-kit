## 11. Avatar

```html
<!-- HTML -->
<!-- Text avatar -->
<div class="avatar avatar-blue">HA</div>

<!-- Image avatar -->
<img class="avatar" src="photo.jpg" alt="Name">
```

```css
/* CSS */
.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: var(--text-base);
    font-weight: 600;
    color: white;
    flex-shrink: 0;
    object-fit: cover;
}

.avatar-sm { width: 32px; height: 32px; font-size: var(--text-sm); }
.avatar-lg { width: 48px; height: 48px; font-size: var(--text-lg); }

.avatar-blue { background: var(--color-primary); }
.avatar-green { background: var(--color-success); }
.avatar-purple { background: var(--color-info); }
.avatar-orange { background: var(--color-warning); }
```

---

## 12. Badge

```html
<!-- HTML -->
<span class="badge badge-success">Completed</span>
<span class="badge badge-warning">Pending</span>
<span class="badge badge-info">PRO</span>
<span class="badge badge-error">Overdue</span>
```

```css
/* CSS */
.badge {
    font-size: var(--text-xs);
    font-weight: 600;
    padding: 3px 8px;
    border-radius: var(--radius-full);
    display: inline-flex;
    align-items: center;
    gap: var(--space-1);
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

.badge-success { background: var(--color-success-light); color: var(--color-success); }
.badge-warning { background: var(--color-warning-light); color: var(--color-warning); }
.badge-info { background: var(--color-info-light); color: var(--color-info); }
.badge-error { background: var(--color-error-light); color: var(--color-error); }
.badge-primary { background: var(--color-primary-light); color: var(--color-primary); }
```

---

## 13. Chip / Tag

```html
<!-- HTML -->
<div class="chip-group">
    <span class="chip">Label <span class="chip-count">3</span></span>
    <span class="chip">Another</span>
</div>
```

```css
/* CSS */
.chip-group {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-2);
}

.chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: var(--space-2) var(--space-3);
    border-radius: var(--radius-full);
    background: var(--gray-50);
    border: 1px solid var(--gray-200);
    font-size: 13px;
    color: var(--gray-700);
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}

.chip:hover {
    background: var(--color-primary-light);
    border-color: var(--color-primary);
    color: var(--color-primary);
}

.chip-count {
    font-size: var(--text-xs);
    font-weight: 600;
    color: white;
    background: var(--color-primary);
    border-radius: 10px;
    min-width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 6px;
}
```

---

## 14. Buttons

```html
<!-- HTML -->
<button class="btn btn-primary">Primary Button</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-outline">Outline</button>
<button class="btn btn-ghost">Ghost</button>
```

```css
/* CSS */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-2);
    padding: var(--space-3) var(--space-5);
    border-radius: var(--radius-sm);
    font-family: var(--font-family);
    font-size: var(--text-base);
    font-weight: 600;
    cursor: pointer;
    border: none;
    transition: all 0.2s;
    min-height: 44px;
}

.btn svg {
    width: 18px;
    height: 18px;
}

.btn-primary {
    background: var(--color-primary);
    color: white;
}

.btn-primary:hover {
    background: #1D4ED8;
}

.btn-secondary {
    background: var(--color-primary-light);
    color: var(--color-primary);
}

.btn-outline {
    background: white;
    color: var(--gray-700);
    border: 1px solid var(--gray-200);
}

.btn-ghost {
    background: none;
    color: var(--color-primary);
}

.btn-full {
    width: 100%;
}

.btn-sm {
    padding: var(--space-2) var(--space-3);
    font-size: var(--text-sm);
    min-height: 36px;
    border-radius: var(--radius-xs);
}
```
