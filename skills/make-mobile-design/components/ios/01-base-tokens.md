## 1. Base Layout & Design Tokens

Every screen MUST start with this boilerplate. Adjust token values based on the project's `design-system.html` if one exists.

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Screen Name</title>
    <style>
        /* iOS targets: do NOT import a Google Font — use the SF system stack below.
           For non-iOS / platform-agnostic mockups, you may add a Google Fonts @import here
           and override --font-family in :root. */

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            /* Primary */
            --color-primary: #2563EB;
            --color-primary-light: #EFF6FF;
            --color-primary-50: #DBEAFE;

            /* Semantic */
            --color-success: #16A34A;
            --color-success-light: #F0FDF4;
            --color-error: #DC2626;
            --color-error-light: #FEF2F2;
            --color-warning: #EA580C;
            --color-warning-light: #FFF7ED;
            --color-info: #7C3AED;
            --color-info-light: #F5F3FF;

            /* Neutrals */
            --gray-50: #F9FAFB;
            --gray-100: #F3F4F6;
            --gray-200: #E5E7EB;
            --gray-300: #D1D5DB;
            --gray-400: #9CA3AF;
            --gray-500: #6B7280;
            --gray-600: #4B5563;
            --gray-700: #374151;
            --gray-800: #1F2937;
            --gray-900: #111827;

            /* Spacing (4px base) */
            --space-1: 4px;
            --space-2: 8px;
            --space-3: 12px;
            --space-4: 16px;
            --space-5: 20px;
            --space-6: 24px;
            --space-8: 32px;

            /* Radius */
            --radius-xs: 8px;
            --radius-sm: 12px;
            --radius-md: 16px;
            --radius-lg: 20px;
            --radius-full: 9999px;

            /* Shadows */
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
            --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
            --shadow-lg: 0 8px 24px rgba(0,0,0,0.12);

            /* Typography — iOS HIG type ramp (pt → px 1:1 in mockups).
               Default to the SF system stack on iOS. For non-iOS targets,
               override --font-family in your screen's :root after importing
               a webfont. */
            --font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", system-ui, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;

            --text-caption2:    11px;  /* Caption 2 — tab bar labels, fine print */
            --text-caption1:    12px;  /* Caption 1 */
            --text-footnote:    13px;  /* Footnote — list meta, section headers */
            --text-subheadline: 15px;  /* Subheadline */
            --text-callout:     16px;  /* Callout */
            --text-body:        17px;  /* Body / Headline — DEFAULT for body, list rows, buttons */
            --text-title3:      20px;  /* Title 3 — card titles */
            --text-title2:      22px;  /* Title 2 — sheet headers */
            --text-title1:      28px;  /* Title 1 */
            --text-largetitle:  34px;  /* Large Title — top-of-scroll page titles */

            /* Back-compat aliases — existing components keep working but render at iOS sizes. */
            --text-xs:   var(--text-caption2);
            --text-sm:   var(--text-footnote);
            --text-base: var(--text-body);
            --text-md:   var(--text-body);
            --text-lg:   var(--text-body);
            --text-xl:   var(--text-title3);
            --text-2xl:  var(--text-title2);
            --text-3xl:  var(--text-title1);
            --text-4xl:  var(--text-largetitle);
        }

        body {
            font-family: var(--font-family);
            font-size: var(--text-body);
            line-height: 1.29;
            letter-spacing: -0.022em;
            background: #FFFFFF;
            color: var(--gray-900);
            max-width: 430px;
            margin: 0 auto;
            min-height: 100vh;
            position: relative;
            -webkit-font-smoothing: antialiased;
        }
    </style>
</head>
<body>
    <!-- Screen content here -->
</body>
</html>
```
