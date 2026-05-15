## 15. Checkbox / Task Row

```html
<!-- HTML -->
<div class="task-row">
    <div class="checkbox"></div>
    <div class="task-info">
        <div class="task-name">Task description</div>
        <div class="task-deadline">Due: Tomorrow</div>
    </div>
    <span class="task-priority">!</span> <!-- optional -->
</div>
```

```css
/* CSS */
.task-row {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    padding: var(--space-3) 0;
    border-bottom: 1px solid var(--gray-100);
}

.task-row:last-child {
    border-bottom: none;
}

.checkbox {
    width: 22px;
    height: 22px;
    border-radius: 6px;
    border: 2px solid var(--gray-300);
    flex-shrink: 0;
    cursor: pointer;
    transition: all 0.2s;
}

.checkbox:hover {
    border-color: var(--color-primary);
}

.checkbox.checked {
    background: var(--color-primary);
    border-color: var(--color-primary);
    position: relative;
}

.checkbox.checked::after {
    content: '';
    position: absolute;
    top: 3px;
    left: 6px;
    width: 5px;
    height: 9px;
    border: solid white;
    border-width: 0 2px 2px 0;
    transform: rotate(45deg);
}

.task-info { flex: 1; }

.task-name {
    font-size: var(--text-base);
    color: var(--gray-800);
}

.task-name.completed {
    text-decoration: line-through;
    color: var(--gray-400);
}

.task-deadline {
    font-size: var(--text-sm);
    color: var(--gray-500);
    margin-top: 2px;
}

.task-deadline.overdue {
    color: var(--color-error);
    font-weight: 500;
}

.task-priority {
    font-size: var(--text-lg);
    font-weight: 700;
    color: var(--color-error);
}
```

**JS for interactivity:**
```javascript
document.querySelectorAll('.checkbox').forEach(cb => {
    cb.addEventListener('click', function() {
        this.classList.toggle('checked');
        const name = this.nextElementSibling?.querySelector('.task-name');
        if (name) name.classList.toggle('completed');
    });
});
```

---

## 16. Progress Bar

```html
<!-- HTML -->
<div class="progress-wrap">
    <div class="progress-header">
        <span class="progress-label">Task progress</span>
        <span class="progress-value">8/12</span>
    </div>
    <div class="progress-track">
        <div class="progress-fill" style="width: 67%;"></div>
    </div>
    <span class="progress-percent">67% completed</span>
</div>
```

```css
/* CSS */
.progress-wrap { margin-bottom: var(--space-4); }

.progress-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--space-2);
}

.progress-label {
    font-size: var(--text-lg);
    font-weight: 600;
}

.progress-value {
    font-size: var(--text-base);
    font-weight: 600;
    color: var(--color-primary);
}

.progress-track {
    width: 100%;
    height: 8px;
    background: var(--gray-100);
    border-radius: 4px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--color-primary), #3B82F6);
    border-radius: 4px;
    transition: width 0.6s ease;
}

.progress-percent {
    font-size: var(--text-sm);
    color: var(--gray-500);
    display: block;
    margin-top: var(--space-1);
}
```

---

## 17. Floating Action Button

```html
<!-- HTML -->
<button class="fab">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
    Button Label
</button>
```

```css
/* CSS */
.fab {
    position: fixed;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%);
    max-width: 390px;
    width: calc(100% - 40px);
    padding: var(--space-4) var(--space-6);
    background: var(--color-primary);
    color: white;
    border: none;
    border-radius: var(--radius-md);
    font-family: var(--font-family);
    font-size: var(--text-md);
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-3);
    box-shadow: 0 8px 32px rgba(37, 99, 235, 0.35);
    transition: all 0.2s;
    z-index: 100;
}

.fab:hover {
    transform: translateX(-50%) translateY(-2px);
    box-shadow: 0 12px 40px rgba(37, 99, 235, 0.45);
}

.fab svg {
    width: 20px;
    height: 20px;
}
```

**Usage note:** When a screen has a FAB, add `padding-bottom: 100px` to `body`. If it also has a tab bar, increase to `padding-bottom: 160px`.
