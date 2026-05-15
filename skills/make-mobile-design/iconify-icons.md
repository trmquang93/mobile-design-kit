# Iconify API Icons (275,000+ icons)

When the built-in SVG set (Section 25 of components.md) doesn't have what you need, use the **Iconify API** to access 275k+ open-source icons from 200+ collections. No downloads required -- icons load via URL.

## API URL format

```
https://api.iconify.design/{collection}/{icon-name}.svg?width={px}&height={px}&color=%23{hex}
```

Note: `%23` is the URL-encoded `#` for hex colors.

## Usage in HTML mockups

**As `<img>` tag (recommended for most cases):**
```html
<!-- 24px gray icon -->
<img src="https://api.iconify.design/mdi/receipt-text-outline.svg?width=24&height=24&color=%236B7280"
     width="24" height="24" alt="receipt">

<!-- 32px primary-colored icon -->
<img src="https://api.iconify.design/lucide/scan.svg?width=32&height=32&color=%232563EB"
     width="32" height="32" alt="scan">
```

> **Copy-to-Figma note:** `<img>` is the most Figma-export-friendly choice — it round-trips as an `<image>` reference. The CSS-mask variant below is also supported (the serializer pre-fetches and inlines the SVG tinted by `background-color`). The plain "CSS background" variant is NOT — Figma sees only the element's `background-color` rect, not the icon — avoid it for anything you intend to paste into Figma.

**As CSS background (for buttons, pseudo-elements):**
```css
.icon-receipt {
    width: 24px;
    height: 24px;
    background: url('https://api.iconify.design/mdi/receipt-text-outline.svg?width=24&height=24&color=%236B7280') no-repeat center/contain;
}
```

**As inline CSS with mask (supports currentColor):**
```css
.icon {
    width: 24px;
    height: 24px;
    background-color: currentColor;
    -webkit-mask-image: url('https://api.iconify.design/mdi/receipt-text-outline.svg');
    mask-image: url('https://api.iconify.design/mdi/receipt-text-outline.svg');
    -webkit-mask-size: contain;
    mask-size: contain;
}
```

## Quick reference: common app icons

```
Scanner / Document:
  mdi:document-scanner          mdi:file-document-outline
  lucide:scan                   lucide:file-scan
  ph:scan                       ph:file-text

Receipt / Expense:
  mdi:receipt-text-outline      mdi:receipt-outline
  lucide:receipt                ph:receipt

Business Card / Contact:
  mdi:business-card-outline     mdi:account-box-outline
  lucide:contact                ph:address-book
  ph:identification-card

Camera:
  mdi:camera-outline            lucide:camera
  ph:camera                     tabler:camera

OCR / Text Recognition:
  mdi:text-recognition          mdi:ocr
  lucide:text-search            ph:text-aa

Cloud / Sync:
  mdi:cloud-upload-outline      mdi:cloud-sync-outline
  lucide:cloud-upload           ph:cloud-arrow-up

Signature:
  mdi:signature-freehand        mdi:draw-pen
  lucide:pen-tool               ph:signature

Stamp:
  mdi:stamper                   mdi:rubber-stamp

Export / Share:
  mdi:export-variant            mdi:share-variant-outline
  lucide:share-2                ph:export

QR Code:
  mdi:qrcode-scan               lucide:qr-code
  ph:qr-code                    tabler:qr-code

Settings:
  mdi:cog-outline               lucide:settings
  ph:gear                       tabler:settings

Premium / Crown:
  mdi:crown-outline             lucide:crown
  ph:crown                      tabler:crown
```

## Popular collections

| Collection | Prefix | Count | Style |
|-----------|--------|-------|-------|
| Material Design | `mdi` | 7400+ | Filled + outline variants |
| Phosphor | `ph` | 9000+ | 6 weights per icon |
| Solar | `solar` | 7400+ | Bold, linear, outline |
| Tabler | `tabler` | 6000+ | Consistent stroke width |
| Lucide | `lucide` | 1700+ | Clean, minimal |
| Remix Icon | `ri` | 3100+ | Filled + line variants |
| Heroicons | `heroicons` | 1200+ | Tailwind CSS companion |

## Finding more icons

Use the `/ios-icon-gen` skill to search:
```
/ios-icon-gen search <keyword>
/ios-icon-gen search <keyword> --prefix mdi
```

Browse visually: https://icon-sets.iconify.design/

## Exporting to Xcode asset catalog

After a mockup is approved, use the `/ios-icon-gen` skill to export as production-ready Xcode imagesets:
```
/ios-icon-gen mdi:receipt-text-outline myIconAsset --color 8E8E93 --output ./Assets.xcassets/icons
```
