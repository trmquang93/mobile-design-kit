## 20. Horizontal Scroll Cards (Stats Carousel)

```html
<!-- HTML -->
<div class="h-scroll">
    <div class="h-scroll-spacer"></div>
    <div class="stat-card" style="background: var(--color-primary-light);">
        <div class="stat-icon" style="background: var(--color-primary);">
            <!-- icon SVG -->
        </div>
        <div class="stat-value" style="color: var(--color-primary);">8</div>
        <div class="stat-label">Label</div>
    </div>
    <!-- more cards... -->
    <div class="h-scroll-spacer"></div>
</div>
```

```css
/* CSS */
.h-scroll {
    display: flex;
    gap: var(--space-3);
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
}

.h-scroll::-webkit-scrollbar { display: none; }

.h-scroll-spacer {
    width: var(--space-5);
    flex-shrink: 0;
}

.stat-card {
    flex: 0 0 auto;
    width: 130px;
    padding: var(--space-4);
    border-radius: var(--radius-sm);
    scroll-snap-align: start;
}

.stat-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: var(--space-3);
    color: white;
}

.stat-icon svg {
    width: 18px;
    height: 18px;
}

.stat-value {
    font-size: var(--text-2xl);
    font-weight: 700;
    margin-bottom: 2px;
}

.stat-label {
    font-size: var(--text-sm);
    color: var(--gray-500);
    font-weight: 500;
}
```

---

## 21. Promo / CTA Banner

```html
<!-- HTML -->
<div class="promo-banner">
    <h3 class="promo-title">Weekly summary</h3>
    <p class="promo-text">You recorded 12 hours of meetings. AI is ready to summarize the key points.</p>
    <button class="btn btn-sm" style="background: white; color: var(--color-primary);">View summary</button>
</div>
```

```css
/* CSS */
.promo-banner {
    margin: var(--space-4) var(--space-5);
    padding: var(--space-5);
    background: var(--color-primary);
    border-radius: var(--radius-md);
    color: white;
}

.promo-title {
    font-size: var(--text-lg);
    font-weight: 700;
    margin-bottom: var(--space-2);
}

.promo-text {
    font-size: var(--text-base);
    line-height: 1.5;
    opacity: 0.9;
    margin-bottom: var(--space-4);
}
```

---

## 22. Paywall Banner

```html
<!-- HTML -->
<div class="paywall-banner">
    <p class="paywall-title">Continue reading your recorded version</p>
    <button class="paywall-btn">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="18" height="18"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
        Try PRO for free
    </button>
    <p class="paywall-text">Create, save, and share unlimited notes. Get full access to all advanced note-taking tools.</p>
</div>
```

```css
/* CSS */
.paywall-banner {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 430px;
    background: var(--gray-800);
    color: white;
    padding: var(--space-6) var(--space-5) calc(var(--space-6) + env(safe-area-inset-bottom, 0px));
    border-radius: var(--radius-md) var(--radius-md) 0 0;
    text-align: center;
    z-index: 100;
}

.paywall-title {
    font-size: var(--text-lg);
    font-weight: 600;
    margin-bottom: var(--space-4);
}

.paywall-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-2);
    width: 100%;
    padding: var(--space-4);
    background: white;
    color: var(--gray-900);
    border: none;
    border-radius: var(--radius-sm);
    font-family: var(--font-family);
    font-size: var(--text-md);
    font-weight: 600;
    cursor: pointer;
    margin-bottom: var(--space-3);
}

.paywall-text {
    font-size: var(--text-sm);
    color: var(--gray-400);
    line-height: 1.5;
}
```
