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
 *   - CSS mask icons (Iconify SVG used as `mask` with `background-color` tint)
 *   - overflow clipping via <clipPath>
 * Not exported:
 *   - box-shadow, backdrop-filter (glass), CSS filters, transforms
 *   - background-image (non-gradient), pseudo-elements (::before/::after)
 *
 * Loaded by every mockup the make-mobile-design skill scaffolds. Lives in
 * skills/make-mobile-design/assets/figma-export.js and is referenced via an
 * absolute file:// URL the scaffold script resolves at generation time.
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
    if (m) {
      var p = m[1].split(',').map(function (s) { return parseFloat(s.trim()); });
      return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
    }
    // Modern color() form — Chrome resolves color-mix() to this.
    // e.g. "color(srgb 1 1 1 / 0.92)" or "color(srgb 0.5 0.5 0.5)".
    var cm = str.match(/color\(\s*srgb\s+([^)]+)\)/i);
    if (cm) {
      var parts = cm[1].split('/');
      var rgb = parts[0].trim().split(/\s+/).map(parseFloat);
      var a = parts.length > 1 ? parseFloat(parts[1]) : 1;
      if (rgb.length >= 3) return { r: rgb[0] * 255, g: rgb[1] * 255, b: rgb[2] * 255, a: a };
    }
    return null;
  }

  function colorAttr(c) {
    return c ? 'rgb(' + Math.round(c.r) + ',' + Math.round(c.g) + ',' + Math.round(c.b) + ')' : 'none';
  }

  function num(v) { return Math.round(v * 100) / 100; }

  function gradientDef(bgImage) {
    if (!bgImage || bgImage === 'none') return null;
    var m = bgImage.match(/linear-gradient\(([\s\S]+)\)\s*$/);
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
    var degMatch = parts[0] && parts[0].match(/^(-?\d+(?:\.\d+)?)deg$/);
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

    // CSS mask icon (Iconify SVG used as `mask` with a `background-color`
    // tint — used by the iOS floating tab bar and the Android bottom nav).
    // Figma's SVG paste can't read CSS `mask`, so without this the icon
    // appears as a solid filled rectangle. Pre-fetched SVG markup is
    // recolored with the element's background-color and inlined.
    var maskImg = (cs.maskImage && cs.maskImage !== 'none') ? cs.maskImage : cs.webkitMaskImage;
    var maskMatch = maskImg && maskImg.match(/url\((['"]?)([^'")]+)\1\)/);
    if (maskMatch && window.__figmaMaskCache && window.__figmaMaskCache[maskMatch[2]]) {
      var maskSvg = window.__figmaMaskCache[maskMatch[2]];
      var maskColor = parseRgb(cs.backgroundColor) || parseRgb(cs.color) || { r: 0, g: 0, b: 0, a: 1 };
      var maskColorVal = colorAttr(maskColor);
      var vbm = maskSvg.match(/viewBox\s*=\s*"([^"]+)"/i);
      var vb = vbm ? vbm[1].split(/\s+/).map(parseFloat) : [0, 0, 24, 24];
      var inner = maskSvg.replace(/^[\s\S]*?<svg[^>]*>/i, '').replace(/<\/svg>\s*$/i, '');
      inner = inner.replace(/currentColor/g, maskColorVal);
      var msx = w / (vb[2] || 24), msy = h / (vb[3] || 24);
      if (op < 1) out.push('<g opacity="' + op + '">');
      out.push('<g transform="translate(' + num(x - vb[0] * msx) + ',' + num(y - vb[1] * msy) +
               ') scale(' + num(msx) + ',' + num(msy) + ')" fill="' + maskColorVal +
               '" fill-opacity="' + maskColor.a + '">' + inner + '</g>');
      if (op < 1) out.push('</g>');
      return;
    }

    if (tag === 'svg') {
      // Inline <svg> — embed the element verbatim so its own fill/stroke/
      // viewBox attributes survive. Wrap in a <g transform="translate(...)">
      // for positioning (don't mutate the inner svg's attributes — duplicate
      // width/height would produce invalid XML that Figma rejects).
      // Resolve `currentColor` to the actual text color at export time:
      // Figma's SVG paste parser doesn't reliably propagate color context,
      // so unresolved `currentColor` falls back to black.
      var fillRgb = parseRgb(cs.fill) || parseRgb(cs.color);
      var colorVal = fillRgb ? colorAttr(fillRgb) : 'black';
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
          // Preserve existing fill (incl. fill="none" for outline icons).
          // Only inject computed color when no fill attribute is present.
          // currentColor in attrs/children is resolved by the global replace below.
          var hasFill = /\sfill\s*=\s*"/i.test(stripped);
          var fillAttr = hasFill ? '' : ' fill="' + colorVal + '"';
          return '<svg width="' + num(w) + '" height="' + num(h) + '"' + fillAttr + stripped + '>';
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
      // Pre-fetch CSS mask SVG icons so emit() can inline them
      // synchronously. Each cached entry maps mask url -> raw SVG text.
      var maskUrls = {};
      root.querySelectorAll('*').forEach(function (n) {
        var s = getComputedStyle(n);
        var mi = (s.maskImage && s.maskImage !== 'none') ? s.maskImage : s.webkitMaskImage;
        var m = mi && mi.match(/url\((['"]?)([^'")]+)\1\)/);
        if (m) maskUrls[m[2]] = true;
      });
      var maskCache = {};
      await Promise.all(Object.keys(maskUrls).map(function (u) {
        return fetch(u).then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
          .then(function (t) { maskCache[u] = t; })
          .catch(function () { maskCache[u] = null; });
      }));
      window.__figmaMaskCache = maskCache;
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
