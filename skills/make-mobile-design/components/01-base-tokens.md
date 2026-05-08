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
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

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

            /* Typography */
            --font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            --text-xs: 11px;
            --text-sm: 12px;
            --text-base: 14px;
            --text-md: 15px;
            --text-lg: 16px;
            --text-xl: 18px;
            --text-2xl: 22px;
            --text-3xl: 26px;
            --text-4xl: 30px;
        }

        body {
            font-family: var(--font-family);
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
