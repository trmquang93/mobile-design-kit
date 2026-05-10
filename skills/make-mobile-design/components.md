# Mobile Design Components Library

Reusable HTML/CSS components for mobile app mockups. Copy these exactly when generating screens to ensure consistency. Every component uses CSS custom properties from the design tokens -- always include the tokens block first.

## Component Files

Load the relevant file(s) before generating a screen. **Always load base tokens first.**

| File | Sections | When to load |
|------|----------|-------------|
| [01-base-tokens.md](components/01-base-tokens.md) | 1. Base Layout & Design Tokens | **Always** -- every screen needs this |
| [02-status-bar.md](components/02-status-bar.md) | 2. Status Bar (iOS) | **Always** -- every screen needs this |
| [03-navigation.md](components/03-navigation.md) | 3. Navigation Header, 4. Bottom Tab Bar | When screen has nav bar or tab bar |
| [04-search-filters.md](components/04-search-filters.md) | 5. Search Bar, 6. Segmented Control, 7. Filter Tabs | When screen has search or filtering |
| [05-content.md](components/05-content.md) | 8. Section Header, 9. Content Card, 10. List Item | When screen shows content lists or cards |
| [06-elements.md](components/06-elements.md) | 11. Avatar, 12. Badge, 13. Chip/Tag, 14. Buttons | When screen needs these UI elements |
| [07-interactive.md](components/07-interactive.md) | 15. Checkbox/Task Row, 16. Progress Bar, 17. FAB | When screen has interactive controls |
| [08-overlays.md](components/08-overlays.md) | 18. Bottom Sheet, 19. Action Menu | When screen has modal overlays |
| [09-cards-banners.md](components/09-cards-banners.md) | 20. Stats Carousel, 21. Promo Banner, 22. Paywall | When screen has promotional content |
| [10-media-states.md](components/10-media-states.md) | 23. Audio Player, 24. Empty State | When screen has media playback or empty states |
| [11-icons.md](components/11-icons.md) | 25. Common SVG Icons, 26. Iconify API | When you need icon references |
| [12-toolbars.md](components/12-toolbars.md) | 27. Bottom Toolbar (Icon Only), 28. Bottom Toolbar (Icon+Label), 29. Bottom Toolbar with Overflow Menu, 30. Header Toolbar | When screen has a contextual action bar (edit/share/delete), an overflow menu, or multiple header trailing actions |

Also available: [iconify-icons.md](iconify-icons.md) -- full Iconify API guide with 275k+ icons.

## Quick Start

For a typical screen, load these files:

1. `components/01-base-tokens.md` (required)
2. `components/02-status-bar.md` (required)
3. `components/03-navigation.md` (if nav bar / tab bar)
4. Pick additional files based on the screen's content needs
5. `components/11-icons.md` (if you need specific icons)
