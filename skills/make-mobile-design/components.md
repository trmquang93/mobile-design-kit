# Mobile Design Components Library

Reusable HTML/CSS components for mobile app mockups. Copy these exactly when generating screens to ensure consistency. Every component uses CSS custom properties from the design tokens -- always include the tokens block first.

Components are split by platform. **Load only the files for the platform you're targeting.** Cross-platform files (icons, the Iconify API guide) live at the top of `components/`.

## iOS Component Files (`components/ios/`)

| File | Sections | When to load |
|------|----------|-------------|
| [ios/00-liquid-glass.md](components/ios/00-liquid-glass.md) | 0. Liquid Glass — Shared Recipe | Whenever a nav header / tab bar / toolbar / FAB / sheet uses the `.glass` class |
| [ios/01-base-tokens.md](components/ios/01-base-tokens.md) | 1. Base Layout & Design Tokens (iOS HIG type ramp) | **Always for iOS** |
| [ios/02-status-bar.md](components/ios/02-status-bar.md) | 2. Status Bar (iOS, 59px, Dynamic Island) | **Always for iOS** |
| [ios/03-navigation.md](components/ios/03-navigation.md) | 3. Navigation Header, 4. Bottom Tab Bar | When iOS screen has nav bar or tab bar |
| [ios/04-search-filters.md](components/ios/04-search-filters.md) | 5. Search Bar, 6. Segmented Control, 7. Filter Tabs | When iOS screen has search or filtering |
| [ios/05-content.md](components/ios/05-content.md) | 8. Section Header, 9. Content Card, 10. List Item | When iOS screen shows content lists or cards |
| [ios/06-elements.md](components/ios/06-elements.md) | 11. Avatar, 12. Badge, 13. Chip/Tag, 14. Buttons | When iOS screen needs these UI elements |
| [ios/07-interactive.md](components/ios/07-interactive.md) | 15. Checkbox/Task Row, 16. Progress Bar, 17. FAB | When iOS screen has interactive controls |
| [ios/08-overlays.md](components/ios/08-overlays.md) | 18. Bottom Sheet, 19. Action Menu | When iOS screen has modal overlays |
| [ios/09-cards-banners.md](components/ios/09-cards-banners.md) | 20. Stats Carousel, 21. Promo Banner, 22. Paywall | When iOS screen has promotional content |
| [ios/10-media-states.md](components/ios/10-media-states.md) | 23. Audio Player, 24. Empty State | When iOS screen has media playback or empty states |
| [ios/12-toolbars.md](components/ios/12-toolbars.md) | 27. Bottom Toolbar (Icon Only), 28. Bottom Toolbar (Icon+Label), 29. Bottom Toolbar with Overflow Menu, 30. Header Toolbar | When iOS screen has a contextual action bar, an overflow menu, or multiple header trailing actions |
| [ios/13-tablet-layouts.md](components/ios/13-tablet-layouts.md) | 31. Tablet Layout Wrappers (split-view, sidebar, supplemental pane, detail pane, three-column, sidebar rows) | **Load when form-factor = tablet** and the iPad screen has a sidebar, split view, or three-column layout |

## Android Component Files (`components/android/`)

| File | Sections | When to load |
|------|----------|-------------|
| [android/01-base-tokens.md](components/android/01-base-tokens.md) | A1. MD3 Design Tokens (color roles, type scale, shape, elevation, motion) | **Always for Android** |
| [android/02-status-bar.md](components/android/02-status-bar.md) | A2. Status Bar (24dp, hole-punch camera) | **Always for Android** |
| [android/03-navigation.md](components/android/03-navigation.md) | A3. Top App Bar (small / center / medium / large), A4. Bottom Navigation Bar | When Android screen has top app bar or bottom nav |
| [android/04-search-filters.md](components/android/04-search-filters.md) | A5. Search Bar, A6. Segmented Buttons, A7. Chips (assist / filter / input / suggestion) | When Android screen has search or filtering |
| [android/05-content.md](components/android/05-content.md) | A8. Section Header, A9. Cards (elevated / filled / outlined), A10. List Items | When Android screen shows content lists or cards |
| [android/06-elements.md](components/android/06-elements.md) | A11. Avatar, A12. Badge, A13. Chip, A14. Buttons (filled / tonal / outlined / elevated / text + icon buttons) | When Android screen needs these UI elements |
| [android/07-interactive.md](components/android/07-interactive.md) | A15. Switch / Checkbox / Radio, A16. Slider, A17. Progress, A18. FAB (regular / small / large / extended) | When Android screen has interactive controls |
| [android/08-overlays.md](components/android/08-overlays.md) | A19. Bottom Sheet (modal + standard), A20. Dialog, A21. Menu | When Android screen has modal overlays |
| [android/09-navigation-drawer.md](components/android/09-navigation-drawer.md) | A22. Navigation Drawer (modal + standard), A23. Navigation Rail | When Android screen has a side drawer or rail |
| [android/10-tablet-layouts.md](components/android/10-tablet-layouts.md) | A24. Tablet Layout Wrappers (`.tablet-shell`, `.list-detail`, `.list-pane`, `.detail-pane-md`, `.three-column-md`) | **Load when form-factor = tablet** and the Android screen uses nav rail / list-detail / three-column |

## Cross-Platform Files

| File | Sections | When to load |
|------|----------|-------------|
| [11-icons.md](components/11-icons.md) | 25. Common SVG Icons, 26. Iconify API | When you need icon references (both platforms) |

Also available: [iconify-icons.md](iconify-icons.md) -- full Iconify API guide with 275k+ icons (platform-agnostic).

## Quick Start (iOS)

For a typical iOS screen, load these files:

1. `components/ios/01-base-tokens.md` (required)
2. `components/ios/02-status-bar.md` (required)
3. `components/ios/03-navigation.md` (if nav bar / tab bar)
4. Pick additional iOS files based on the screen's content needs
5. `components/11-icons.md` (if you need specific icons)

## Quick Start (Android)

For a typical Android screen, load these files:

1. `components/android/01-base-tokens.md` (required)
2. `components/android/02-status-bar.md` (required)
3. `components/android/03-navigation.md` (if top app bar / bottom nav)
4. Pick additional Android files based on the screen's content needs
5. `components/11-icons.md` (if you need specific icons; prefer `mdi` or `material-symbols` collections for Android)
