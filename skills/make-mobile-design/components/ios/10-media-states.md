## 23. Audio Player (Persistent)

```html
<!-- HTML -->
<div class="audio-player">
    <div class="player-progress">
        <span class="player-time">0:06</span>
        <div class="player-track">
            <div class="player-track-fill" style="width: 5%;"></div>
            <div class="player-thumb"></div>
        </div>
        <span class="player-time">15:16</span>
    </div>
    <div class="player-controls">
        <span class="player-speed">1.0x</span>
        <button class="player-btn-sm">
            <svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12.5 8c-2.65 0-5.05 1.04-6.83 2.73L3 8v8h8l-2.81-2.81C9.83 11.83 11.1 11 12.5 11c2.33 0 4.31 1.46 5.11 3.5l2.38-.79C18.87 10.47 15.92 8 12.5 8z"/><text x="6" y="20" font-size="8" font-weight="700">15</text></svg>
        </button>
        <button class="player-btn-main">
            <svg viewBox="0 0 24 24" fill="white"><polygon points="5 3 19 12 5 21 5 3"/></svg>
        </button>
        <button class="player-btn-sm">
            <svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M11.5 8c2.65 0 5.05 1.04 6.83 2.73L21 8v8h-8l2.81-2.81C14.17 11.83 12.9 11 11.5 11c-2.33 0-4.31 1.46-5.11 3.5L4.01 13.71C5.13 10.47 8.08 8 11.5 8z"/><text x="10" y="20" font-size="8" font-weight="700">15</text></svg>
        </button>
        <button class="player-btn-sm">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
        </button>
    </div>
</div>
```

```css
/* CSS */
.audio-player {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 430px;
    background: white;
    border-top: 1px solid var(--gray-200);
    padding: var(--space-3) var(--space-5) calc(var(--space-4) + env(safe-area-inset-bottom, 0px));
    z-index: 90;
}

.player-progress {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    margin-bottom: var(--space-3);
}

.player-time {
    font-size: var(--text-sm);
    color: var(--gray-500);
    font-weight: 500;
    min-width: 36px;
}

.player-track {
    flex: 1;
    height: 4px;
    background: var(--gray-200);
    border-radius: 2px;
    position: relative;
}

.player-track-fill {
    height: 100%;
    background: var(--color-primary);
    border-radius: 2px;
}

.player-thumb {
    width: 12px;
    height: 12px;
    background: var(--color-primary);
    border-radius: 50%;
    position: absolute;
    top: -4px;
    left: 5%;
}

.player-controls {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-4);
}

.player-speed {
    font-size: var(--text-sm);
    font-weight: 600;
    color: var(--gray-600);
    min-width: 36px;
}

.player-btn-sm {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    background: none;
    cursor: pointer;
    color: var(--gray-600);
}

.player-btn-sm svg {
    width: 22px;
    height: 22px;
}

.player-btn-main {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: var(--color-primary);
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

.player-btn-main svg {
    width: 22px;
    height: 22px;
}
```

---

## 24. Empty State

```html
<!-- HTML -->
<div class="empty-state">
    <div class="empty-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>
    </div>
    <h3 class="empty-title">No recordings yet</h3>
    <p class="empty-text">Start your first recording to see it appear here.</p>
    <button class="btn btn-primary">Record now</button>
</div>
```

```css
/* CSS */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: var(--space-8) var(--space-5);
}

.empty-icon {
    width: 64px;
    height: 64px;
    background: var(--gray-100);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: var(--space-5);
    color: var(--gray-400);
}

.empty-icon svg {
    width: 28px;
    height: 28px;
}

.empty-title {
    font-size: var(--text-lg);
    font-weight: 600;
    margin-bottom: var(--space-2);
}

.empty-text {
    font-size: var(--text-base);
    color: var(--gray-500);
    line-height: 1.5;
    margin-bottom: var(--space-5);
    max-width: 260px;
}
```
