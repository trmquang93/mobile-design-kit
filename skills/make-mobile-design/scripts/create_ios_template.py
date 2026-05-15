#!/usr/bin/env python3
"""Generate a standalone HTML iPhone device template with Dynamic Island
and home indicator, ready to be filled with screen content.

Usage:
    python create_ios_template.py <output.html> [--title "Screen Name"]
"""

import argparse
import sys
from pathlib import Path
from string import Template

TEMPLATE = Template(r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>$title</title>
    <style>
        :root {
            --color-bg: #FFFFFF;
            --color-text: #000000;
            --color-text-secondary: #6B7280;
            --color-island: #000000;
            --font-system: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", system-ui, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;

            /* iOS HIG type ramp — keep in sync with components/ios/01-base-tokens.md */
            --text-caption2:    11px;
            --text-caption1:    12px;
            --text-footnote:    13px;
            --text-subheadline: 15px;
            --text-callout:     16px;
            --text-body:        17px;
            --text-title3:      20px;
            --text-title2:      22px;
            --text-title1:      28px;
            --text-largetitle:  34px;
            --text-md:          var(--text-body);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        html, body {
            background: #1a1a1a;
            font-family: var(--font-system);
            font-size: var(--text-body);
            line-height: 1.29;
            letter-spacing: -0.022em;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            color: var(--color-text);
            min-height: 100vh;
        }

        body {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px 0;
        }

        .device {
            position: relative;
            width: 430px;
            height: 932px;
            min-width: 430px;
            min-height: 932px;
            flex-shrink: 0;
            background: var(--color-bg);
            border-radius: 48px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            overflow: hidden;
        }

        /* Dynamic Island */
        .dynamic-island {
            position: absolute;
            top: 11px;
            left: 50%;
            transform: translateX(-50%);
            width: 126px;
            height: 37px;
            background: var(--color-island);
            border-radius: 19px;
            z-index: 100;
            pointer-events: none;
        }

        /* Status Bar (matches components/ios/02-status-bar.md) — overlays content, stays fixed during scroll */
        .status-bar {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 59px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 24px 8px;
            z-index: 50;
            pointer-events: none;
        }

        .status-bar-time {
            font-size: var(--text-md);
            font-weight: 600;
        }

        .status-bar-icons {
            display: flex;
            gap: 6px;
            align-items: center;
        }

        /* Scrollable content — scrolls behind status bar and home indicator.
           Any floating overlay placed over .device-content (custom tab bar, FAB,
           banner, sheet handle) MUST set `pointer-events: none` on its wrapper
           and `pointer-events: auto` on its interactive children, otherwise the
           overlay swallows wheel/touch and the screen stops scrolling under it.

           NOTE: padding-top is intentionally 0 — the 59px status-bar safe area
           is the responsibility of the FIRST element inside .device-content,
           NOT this container. This is so navigation bars (.nav-header, glass
           top bars, hero images) can render their background behind the status
           bar to the very top edge of the screen, which is the correct iOS
           behavior. See components/ios/03-navigation.md §3a for the pattern. */
        .device-content {
            position: absolute;
            inset: 0;
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
            padding-top: 0;       /* status-bar offset belongs on first child */
            padding-bottom: 34px; /* space for home indicator */
        }
        /* Block layout, NOT flex — flex-direction:column with overflow:auto
           lets browsers shrink children below their content size and the
           container then reports scrollHeight == clientHeight (no scroll). */

        .device-content::-webkit-scrollbar { display: none; }
        .device-content { scrollbar-width: none; }

        /* Home Indicator — overlays content, stays fixed during scroll */
        .home-indicator-area {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 34px;
            display: flex;
            justify-content: center;
            align-items: flex-end;
            padding-bottom: 8px;
            pointer-events: none;
            z-index: 50;
        }

        .home-indicator {
            width: 134px;
            height: 5px;
            background: var(--color-text);
            border-radius: 3px;
            opacity: 0.9;
        }

        /* Figma export chrome — host page only, not part of the design payload */
        .figma-export-toolbar {
            position: fixed;
            top: 16px;
            right: 16px;
            display: flex;
            gap: 8px;
            align-items: center;
            z-index: 1000;
            font-family: var(--font-system);
        }
        .figma-export-btn {
            appearance: none;
            border: 1px solid rgba(255,255,255,0.18);
            background: rgba(28,28,30,0.72);
            backdrop-filter: blur(20px) saturate(160%);
            -webkit-backdrop-filter: blur(20px) saturate(160%);
            color: #fff;
            font: 600 13px var(--font-system);
            padding: 8px 14px;
            border-radius: 999px;
            cursor: pointer;
        }
        .figma-export-btn:hover { background: rgba(44,44,46,0.85); }
        .figma-export-btn:active { transform: scale(0.98); }
        .figma-export-toast {
            color: #fff;
            font-size: 12px;
            opacity: 0.9;
            background: rgba(28,28,30,0.72);
            padding: 6px 10px;
            border-radius: 999px;
            backdrop-filter: blur(20px) saturate(160%);
            -webkit-backdrop-filter: blur(20px) saturate(160%);
        }
        .figma-export-toast[hidden] { display: none; }
    </style>
</head>
<body>
    <div class="device">
        <!-- Dynamic Island (always on top) -->
        <div class="dynamic-island"></div>

        <!-- Status Bar -->
        <div class="status-bar">
            <span class="status-bar-time">9:41</span>
            <div class="status-bar-icons">
                <svg width="16" height="12" viewBox="0 0 16 12" fill="currentColor"><rect x="0" y="3" width="3" height="9" rx="1"/><rect x="4.5" y="2" width="3" height="10" rx="1"/><rect x="9" y="0" width="3" height="12" rx="1"/><rect x="13" y="1" width="3" height="11" rx="1"/></svg>
                <svg width="16" height="12" viewBox="0 0 16 12" fill="currentColor"><path d="M8 3C10.7 3 13.1 4.2 14.7 6.1L16 4.8C14 2.5 11.2 1 8 1S2 2.5 0 4.8L1.3 6.1C2.9 4.2 5.3 3 8 3Z"/><path d="M8 7C9.5 7 10.9 7.6 11.9 8.6L13.2 7.3C11.8 5.9 10 5 8 5S4.2 5.9 2.8 7.3L4.1 8.6C5.1 7.6 6.5 7 8 7Z"/><circle cx="8" cy="11" r="1.5"/></svg>
                <svg width="25" height="12" viewBox="0 0 25 12" fill="currentColor"><rect x="0" y="1" width="21" height="10" rx="2" stroke="currentColor" stroke-width="1" fill="none"/><rect x="22" y="4" width="2" height="4" rx="1"/><rect x="2" y="3" width="17" height="6" rx="1"/></svg>
            </div>
        </div>

        <!-- Insert screen content here -->
        <main class="device-content">
            <!-- Screen content goes here -->
        </main>

        <!-- Home Indicator -->
        <div class="home-indicator-area">
            <div class="home-indicator"></div>
        </div>
    </div>

    <!-- Figma export chrome (host page only; not serialized into the payload) -->
    <div class="figma-export-toolbar" data-figma-export-ignore>
        <span class="figma-export-toast" hidden></span>
        <button type="button" class="figma-export-btn" onclick="window.__copyDesignToFigma()">
            Copy to Figma
        </button>
    </div>

    <script>
    /*
     * Figma-ready SVG export
     *
     * Walks .device and emits real SVG primitives (rect, text, image, nested
     * <svg>, linearGradient, clipPath). Result is copied to the clipboard as
     * plain text — Figma's onPaste handler detects an SVG string and converts
     * it to editable vector layers (text stays text, shapes stay shapes).
     *
     * Coverage:
     *   - solid fills, linear gradients, borders, border-radius, opacity
     *   - text (multi-line via Range.getClientRects per line)
     *   - inline <svg> icons (embedded as nested <svg>, color inherited)
     *   - <img> (emitted as <image href="..."> — Figma may refuse remote URLs)
     *   - overflow clipping via <clipPath>
     * Not exported:
     *   - box-shadow, backdrop-filter (glass), CSS filters, transforms
     *   - background-image (non-gradient), pseudo-elements (::before/::after)
     */
    (function () {
      var SVG_NS = 'http://www.w3.org/2000/svg';
      var defs = [];
      var defCounter = 0;

      function esc(s) {
        return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
      }

      function parseRgb(str) {
        if (!str || str === 'transparent' || str === 'rgba(0, 0, 0, 0)') return null;
        var m = str.match(/rgba?\(([^)]+)\)/);
        if (!m) return null;
        var p = m[1].split(',').map(function (s) { return parseFloat(s.trim()); });
        return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
      }

      function colorAttr(c) {
        return c ? 'rgb(' + Math.round(c.r) + ',' + Math.round(c.g) + ',' + Math.round(c.b) + ')' : 'none';
      }

      function num(v) { return Math.round(v * 100) / 100; }

      function gradientDef(bgImage) {
        if (!bgImage || bgImage === 'none') return null;
        var m = bgImage.match(/linear-gradient\(([\s\S]+)\)\s*$$/);
        if (!m) return null;
        var inner = m[1];
        var parts = [], depth = 0, start = 0;
        for (var i = 0; i <= inner.length; i++) {
          var ch = inner[i];
          if (ch === '(') depth++;
          else if (ch === ')') depth--;
          else if ((ch === ',' && depth === 0) || i === inner.length) {
            parts.push(inner.slice(start, i).trim());
            start = i + 1;
          }
        }
        var angle = 180;
        var stopParts = parts;
        var degMatch = parts[0] && parts[0].match(/^(-?\d+(?:\.\d+)?)deg$$/);
        if (degMatch) { angle = parseFloat(degMatch[1]); stopParts = parts.slice(1); }
        else if (parts[0] && /^to\s+/.test(parts[0])) {
          var dirs = { top: 0, right: 90, bottom: 180, left: 270,
                       'top right': 45, 'bottom right': 135, 'bottom left': 225, 'top left': 315 };
          var key = parts[0].replace(/^to\s+/, '').trim();
          angle = dirs[key] !== undefined ? dirs[key] : 180;
          stopParts = parts.slice(1);
        }
        var stops = stopParts.map(function (s, idx, arr) {
          var cm = s.match(/rgba?\([^)]+\)|#[0-9a-f]+|[a-z]+/i);
          var pm = s.match(/(\d+(?:\.\d+)?)%/);
          return {
            color: parseRgb(cm ? cm[0] : '#000') || { r: 0, g: 0, b: 0, a: 1 },
            pos: pm ? parseFloat(pm[1]) / 100 : (arr.length > 1 ? idx / (arr.length - 1) : 0)
          };
        });
        // CSS gradient angle: 0deg points up. SVG x1/y1 -> x2/y2 in objectBoundingBox.
        var rad = (angle - 90) * Math.PI / 180;
        var dx = Math.cos(rad) * 0.5, dy = Math.sin(rad) * 0.5;
        var id = 'fgmg' + (++defCounter);
        var stopXml = stops.map(function (s) {
          return '<stop offset="' + num(s.pos) + '" stop-color="' + colorAttr(s.color) + '" stop-opacity="' + s.color.a + '"/>';
        }).join('');
        defs.push('<linearGradient id="' + id + '" x1="' + num(0.5 - dx) + '" y1="' + num(0.5 - dy) +
                  '" x2="' + num(0.5 + dx) + '" y2="' + num(0.5 + dy) + '">' + stopXml + '</linearGradient>');
        return 'url(#' + id + ')';
      }

      function clipDef(x, y, w, h, rx) {
        var id = 'fgmc' + (++defCounter);
        defs.push('<clipPath id="' + id + '"><rect x="' + num(x) + '" y="' + num(y) +
                  '" width="' + num(w) + '" height="' + num(h) +
                  '" rx="' + num(rx) + '" ry="' + num(rx) + '"/></clipPath>');
        return id;
      }

      function lineRectsForText(textNode) {
        var text = textNode.textContent;
        if (!text.trim()) return [];
        var range = document.createRange();
        range.selectNodeContents(textNode);
        var rects = Array.prototype.slice.call(range.getClientRects());
        if (rects.length === 0) return [];
        if (rects.length === 1) return [{ text: text, rect: rects[0] }];
        // Multi-line: binary-search per line to find character span
        var lines = [];
        var len = text.length;
        var offset = 0;
        for (var li = 0; li < rects.length; li++) {
          var targetTop = rects[li].top;
          while (offset < len && /\s/.test(text[offset])) offset++;
          var lo = offset, hi = len;
          while (lo < hi) {
            var mid = (lo + hi + 1) >> 1;
            range.setStart(textNode, offset);
            range.setEnd(textNode, mid);
            var rs = range.getClientRects();
            var lastTop = rs.length ? rs[rs.length - 1].top : targetTop;
            if (Math.abs(lastTop - targetTop) < 1) lo = mid;
            else hi = mid - 1;
          }
          var lineEnd = lo > offset ? lo : Math.min(offset + 1, len);
          var lineText = text.slice(offset, lineEnd);
          if (lineText.trim().length) lines.push({ text: lineText, rect: rects[li] });
          offset = lineEnd;
        }
        return lines;
      }

      function emitTextNode(textNode, ox, oy, out) {
        var parent = textNode.parentElement;
        if (!parent) return;
        var cs = getComputedStyle(parent);
        var color = parseRgb(cs.color);
        var family = (cs.fontFamily || '').replace(/"/g, "'");
        var size = parseFloat(cs.fontSize);
        var weight = cs.fontWeight;
        var align = cs.textAlign;
        var lines = lineRectsForText(textNode);
        for (var i = 0; i < lines.length; i++) {
          var ln = lines[i];
          var lx = ln.rect.left - ox;
          var ly = ln.rect.top - oy;
          // Baseline ≈ font cap-height. Center font within line box, then drop to baseline.
          var ty = ly + (ln.rect.height - size) / 2 + size * 0.82;
          var tx = lx;
          var anchor = 'start';
          if (align === 'center') { anchor = 'middle'; tx = lx + ln.rect.width / 2; }
          else if (align === 'right' || align === 'end') { anchor = 'end'; tx = lx + ln.rect.width; }
          out.push('<text x="' + num(tx) + '" y="' + num(ty) +
                   '" font-family="' + esc(family) +
                   '" font-size="' + num(size) +
                   '" font-weight="' + weight +
                   '" fill="' + colorAttr(color) +
                   (color && color.a < 1 ? '" fill-opacity="' + color.a : '') +
                   '" text-anchor="' + anchor +
                   '" xml:space="preserve">' + esc(ln.text) + '</text>');
        }
      }

      function emit(node, ox, oy, out) {
        if (node.nodeType === 3) { emitTextNode(node, ox, oy, out); return; }
        if (node.nodeType !== 1) return;
        if (node.dataset && 'figmaExportIgnore' in node.dataset) return;
        var cs = getComputedStyle(node);
        if (cs.display === 'none' || cs.visibility === 'hidden') return;
        var op = parseFloat(cs.opacity);
        if (op === 0) return;
        var tag = node.tagName.toLowerCase();
        var r = node.getBoundingClientRect();
        var x = r.left - ox, y = r.top - oy, w = r.width, h = r.height;
        if (w <= 0 || h <= 0) return;

        // Inline <svg> — embed the element verbatim so its own fill/stroke/
        // viewBox attributes survive. Wrap in a <g transform="translate(...)">
        // for positioning (don't mutate the inner svg's attributes — duplicate
        // width/height would produce invalid XML that Figma rejects).
        // Resolve `currentColor` to the actual text color at export time:
        // Figma's SVG paste parser doesn't reliably propagate color context,
        // so unresolved `currentColor` falls back to black.
        if (tag === 'svg') {
          var color = parseRgb(cs.color);
          var colorVal = color ? colorAttr(color) : 'black';
          // Strip any existing width/height (may come from CSS, not attrs) and
          // inject the computed render size, otherwise a nested <svg> without
          // width/height defaults to 100% of the root viewport in Figma.
          // Also resolve currentColor so strokes/fills don't fall back to black.
          // Only strip width/height on the OUTER <svg ...> opening tag — a
          // global replace also wipes width/height from inner <rect>/<image>
          // elements (e.g. status-bar cellular/battery rects), erasing them.
          var markup = node.outerHTML.replace(
            /^<svg\b([^>]*)>/i,
            function (_m, attrs) {
              var stripped = attrs.replace(/\s(?:width|height)\s*=\s*"[^"]*"/gi, '');
              return '<svg width="' + num(w) + '" height="' + num(h) + '"' + stripped + '>';
            }
          ).replace(/currentColor/g, colorVal);
          if (op < 1) out.push('<g opacity="' + op + '">');
          out.push('<g transform="translate(' + num(x) + ',' + num(y) + ')">' + markup + '</g>');
          if (op < 1) out.push('</g>');
          return;
        }

        // <img> — emit as <image>; Figma may or may not fetch the href on paste
        if (tag === 'img') {
          var src = node.currentSrc || node.src;
          out.push('<image x="' + num(x) + '" y="' + num(y) +
                   '" width="' + num(w) + '" height="' + num(h) +
                   '" href="' + esc(src) + '" preserveAspectRatio="xMidYMid slice"/>');
          return;
        }

        if (op < 1) out.push('<g opacity="' + op + '">');

        // Background / border rect
        var bg = parseRgb(cs.backgroundColor);
        var grad = gradientDef(cs.backgroundImage);
        var borderW = parseFloat(cs.borderTopWidth) || 0;
        var borderC = borderW > 0 ? parseRgb(cs.borderTopColor) : null;
        var rx = parseFloat(cs.borderTopLeftRadius) || 0;
        // Clamp rx to min(w,h)/2 — CSS border-radius: 9999px renders as a
        // pill, but SVG clamps rx and ry independently, producing an ellipse.
        rx = Math.min(rx, Math.min(w, h) / 2);
        if (grad || bg || (borderW && borderC)) {
          var fillVal = grad || (bg ? colorAttr(bg) : 'none');
          var fillOp = (!grad && bg) ? bg.a : 1;
          var strokeAttr = (borderW && borderC)
            ? ' stroke="' + colorAttr(borderC) + '" stroke-opacity="' + borderC.a + '" stroke-width="' + num(borderW) + '"'
            : '';
          out.push('<rect x="' + num(x) + '" y="' + num(y) +
                   '" width="' + num(w) + '" height="' + num(h) +
                   '" rx="' + num(rx) + '" ry="' + num(rx) +
                   '" fill="' + fillVal + '" fill-opacity="' + fillOp + '"' + strokeAttr + '/>');
        }

        // Children, possibly clipped by overflow.
        // SVG paint order is strict DOM order — CSS z-index is ignored.
        // Stable-sort element children by computed z-index so stacked
        // positioned layers (e.g. status-bar over .ambient) paint correctly.
        var kids = Array.prototype.slice.call(node.childNodes);
        var ordered = kids.map(function (c, idx) {
          var z = 0;
          if (c.nodeType === 1) {
            var zs = getComputedStyle(c).zIndex;
            if (zs && zs !== 'auto') { var zn = parseInt(zs, 10); if (!isNaN(zn)) z = zn; }
          }
          return { node: c, idx: idx, z: z };
        });
        ordered.sort(function (a, b) { return (a.z - b.z) || (a.idx - b.idx); });
        var childOut = [];
        for (var i = 0; i < ordered.length; i++) {
          emit(ordered[i].node, ox, oy, childOut);
        }
        var needsClip = (cs.overflow === 'hidden' || cs.overflow === 'auto' || cs.overflow === 'scroll' || cs.overflowX === 'hidden' || cs.overflowY === 'hidden');
        if (needsClip && childOut.length) {
          var cid = clipDef(x, y, w, h, rx);
          out.push('<g clip-path="url(#' + cid + ')">');
          out.push(childOut.join(''));
          out.push('</g>');
        } else {
          out.push(childOut.join(''));
        }

        if (op < 1) out.push('</g>');
      }

      function showToast(msg, isError) {
        var t = document.querySelector('.figma-export-toast');
        if (!t) return;
        t.textContent = msg;
        t.hidden = false;
        t.style.color = isError ? '#ff9f9f' : '#fff';
        clearTimeout(showToast._timer);
        showToast._timer = setTimeout(function () { t.hidden = true; }, 2500);
      }

      window.__copyDesignToFigma = async function () {
        try {
          defs = [];
          defCounter = 0;
          var root = document.querySelector('.device');
          if (!root) { showToast('No .device frame found', true); return; }
          var r = root.getBoundingClientRect();
          var out = [];
          emit(root, r.left, r.top, out);
          var svg = '<svg xmlns="' + SVG_NS + '" width="' + num(r.width) + '" height="' + num(r.height) +
                    '" viewBox="0 0 ' + num(r.width) + ' ' + num(r.height) + '">' +
                    (defs.length ? '<defs>' + defs.join('') + '</defs>' : '') +
                    out.join('') +
                    '</svg>';
          await navigator.clipboard.writeText(svg);
          showToast('Copied — paste into Figma (Cmd+V)');
        } catch (err) {
          console.error('[figma-export]', err);
          showToast('Clipboard blocked — serve over http(s) or grant permission', true);
        }
      };
    })();
    </script>
</body>
</html>
""")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate an iPhone device template HTML file with Dynamic Island and home indicator."
    )
    parser.add_argument("output", help="Output HTML file path")
    parser.add_argument("--title", default="Mobile Screen", help="Page title (default: 'Mobile Screen')")
    args = parser.parse_args()

    out_path = Path(args.output)
    if not out_path.parent.exists():
        print(f"Error: parent directory does not exist: {out_path.parent}", file=sys.stderr)
        return 1

    html = TEMPLATE.substitute(title=args.title)
    out_path.write_text(html, encoding="utf-8")
    print(f"Created device template: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
