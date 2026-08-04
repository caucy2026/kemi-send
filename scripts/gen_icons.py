#!/usr/bin/env python3
"""Generate KEMI Send app icons (paper-plane glyph on KEMI red)."""
import os
from PIL import Image, ImageDraw

KEMI_RED = (177, 12, 21, 255)   # #B10C15 from kemi-cart icon
WHITE = (255, 255, 255, 255)

# Material "send" icon outline (24x24 space)
PLANE = [(2.01, 3), (23, 12), (2.01, 21), (2, 14), (17, 12), (2, 10)]


def plane_polygon(w, h, center_frac=0.62):
    """Map Material plane outline into central fraction of w x h canvas."""
    # bounding box of source
    xs = [p[0] for p in PLANE]
    ys = [p[1] for p in PLANE]
    sx0, sx1, sy0, sy1 = min(xs), max(xs), min(ys), max(ys)
    src_w, src_h = sx1 - sx0, sy1 - sy0
    # target box: centered square of side = center_frac * min(w,h)
    side = min(w, h) * center_frac
    tx0 = (w - side) / 2
    ty0 = (h - side) / 2
    out = []
    for x, y in PLANE:
        nx = tx0 + (x - sx0) / src_w * side
        ny = ty0 + (y - sy0) / src_h * side
        out.append((nx, ny))
    return out


def rounded_rect(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def make_foreground(path, size, glyph_color=WHITE, center_frac=0.62):
    """Transparent background + centered glyph (for adaptive icons)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon(plane_polygon(size, size, center_frac), fill=glyph_color)
    im.save(path)


def make_legacy(path, size, radius_frac=0.18, center_frac=0.55):
    """Full-bleed rounded red square + white glyph (legacy launcher)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    r = int(size * radius_frac)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=KEMI_RED)
    d.polygon(plane_polygon(size, size, center_frac), fill=WHITE)
    im.save(path)


BASE = "/Volumes/ORICO/kemi/kemi-send/app/android/app/src/main/res"

# density -> (legacy launcher px, adaptive foreground px)
DENSITIES = {
    "mdpi": (48, 108),
    "hdpi": (72, 162),
    "xhdpi": (96, 216),
    "xxhdpi": (144, 324),
    "xxxhdpi": (192, 432),
}

for dens, (legacy, fg) in DENSITIES.items():
    mip = os.path.join(BASE, f"mipmap-{dens}")
    os.makedirs(mip, exist_ok=True)
    make_legacy(os.path.join(mip, "ic_launcher.png"), legacy)
    make_foreground(os.path.join(mip, "ic_launcher_foreground.png"), fg)
    make_foreground(os.path.join(mip, "ic_launcher_monochrome.png"), fg)
    make_foreground(os.path.join(mip, "ic_launcher_quicktile_foreground.png"), fg, center_frac=0.7)

print("Android icons done")

# Banner (Android TV) - wide red banner with white plane
banner = Image.new("RGBA", (320, 180), (0, 0, 0, 0))
db = ImageDraw.Draw(banner)
db.rectangle([0, 0, 319, 179], fill=KEMI_RED)
db.polygon(plane_polygon(320, 180, 0.22), fill=WHITE)
banner.save(os.path.join(BASE, "drawable", "banner.png"))
print("banner done")
