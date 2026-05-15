#!/usr/bin/env python3
# Compose per-screen PNGs into horizontal showcase strips.
# Run after capture.mjs (or via it). Requires Pillow.

from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "screenshots"

PHONE_W = 320       # rendered width per phone in the strip (2x of 160 display)
GAP = 24            # gap between phones
BG = (0, 0, 0, 0)   # transparent

# Glob-driven: each strip claims PNGs whose filename matches any of its globs.
# Add a new examples/<name>.html and it auto-joins the matching strip and
# auto-cleans after the strip is built. Order within a strip is sorted by
# filename — rename to control order (e.g. prefix `01-`, `02-`).
STRIPS = {
    "android-showcase-strip.png": ["android-*.png"],
    # iOS catches everything not consumed by an earlier strip.
    "ios-showcase-strip.png": ["*.png"],
}


def collect(globs: list[str], already: set[str]) -> list[str]:
    matched: set[str] = set()
    for pattern in globs:
        for path in SHOTS.glob(pattern):
            name = path.name
            if name in already or name in STRIPS:  # skip prior-strip inputs and strip outputs
                continue
            matched.add(name)
    return sorted(matched)


def build(out_name: str, sources: list[str]) -> bool:
    if not sources:
        print(f"!! {out_name}: no matching screenshots")
        return False
    imgs = []
    for name in sources:
        im = Image.open(SHOTS / name).convert("RGBA")
        ratio = PHONE_W / im.width
        new_h = round(im.height * ratio)
        imgs.append(im.resize((PHONE_W, new_h), Image.LANCZOS))

    max_h = max(im.height for im in imgs)
    total_w = PHONE_W * len(imgs) + GAP * (len(imgs) - 1)
    strip = Image.new("RGBA", (total_w, max_h), BG)
    x = 0
    for im in imgs:
        y = (max_h - im.height) // 2
        strip.paste(im, (x, y), im)
        x += PHONE_W + GAP

    out = SHOTS / out_name
    strip.save(out, optimize=True)
    print(f"OK  {out.relative_to(HERE)}  ({total_w}x{max_h})  [{len(sources)} screens]")
    return True


if __name__ == "__main__":
    consumed: set[str] = set()
    for out_name, globs in STRIPS.items():
        sources = collect(globs, consumed)
        if build(out_name, sources):
            consumed.update(sources)

    for name in consumed:
        path = SHOTS / name
        if path.exists():
            path.unlink()
            print(f"rm  {path.relative_to(HERE)}")
