#!/usr/bin/env python3
"""Ascendant unified HUD art -> kubejs/assets/ascendant/textures/gui/hud/
Vanilla 1.20.1 XP bar (gui/icons.png) recolored blue (XP) and cyan (mana); a 9x9
skill-point gem; an 18x18 faceted level-badge shield. Static icons only (Painter's
dynamic texture-fill path is unreliable, so the script draws the bar fills as rects).
Requires Pillow, numpy.
"""
import os, sys, zipfile, io
import numpy as np
from PIL import Image, ImageDraw

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "kubejs/assets/ascendant/textures/gui/hud")
os.makedirs(OUT, exist_ok=True)

def find_jar():
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]): return sys.argv[1]
    home = os.path.expanduser("~")
    ad = os.environ.get("APPDATA", os.path.join(home, "AppData", "Roaming"))
    for c in [os.path.join(home, "curseforge/minecraft/Install/versions/1.20.1/1.20.1.jar"),
              os.path.join(ad, ".minecraft/versions/1.20.1/1.20.1.jar"),
              os.path.join(home, ".minecraft/versions/1.20.1/1.20.1.jar")]:
        if os.path.isfile(c): return c
    raise SystemExit("1.20.1 jar not found; pass path as arg")

def lum(rgb): return 0.2126*rgb[...,0] + 0.7152*rgb[...,1] + 0.0722*rgb[...,2]

def recolor_bar(prog, lo, hi):
    arr = np.asarray(prog, float); rgb, a = arr[..., :3], arr[..., 3]
    L = lum(rgb); Ln = (L - L.min()) / max(1e-6, (L.max() - L.min()))
    lo = np.array(lo, float); hi = np.array(hi, float)
    out = lo[None, None, :] + (hi - lo)[None, None, :] * Ln[..., None]
    return Image.fromarray(np.dstack([np.clip(out, 0, 255), a]).astype('uint8'), "RGBA")

def tint_track(bg, mul, add):
    arr = np.asarray(bg, float); rgb, a = arr[..., :3], arr[..., 3]
    out = np.clip(rgb * np.array(mul) + np.array(add), 0, 255)
    return Image.fromarray(np.dstack([out, a]).astype('uint8'), "RGBA")

def sp_gem():
    P = {".": (0,0,0,0), "k": (8,16,28,255), "d": (28,86,140,255), "m": (60,150,210,255),
         "l": (120,205,250,255), "w": (224,248,255,255)}
    rows = ["....k....","...kwk...","..klmlk..",".klmmdlk.","kwmmddmdk",".kdmddlk.","..kdmdk..","...kdk...","....k...."]
    im = Image.new("RGBA", (9, 9), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row): im.putpixel((x, y), P[ch])
    return im

def make_level_badge():
    NAVY=(8,16,28,255); DK=(26,74,122,255); MID=(54,140,205,255)
    LT=(118,200,248,255); WHT=(226,248,255,255); PLATE=(12,22,38,255); GEM=(150,235,255,255)
    im = Image.new("RGBA", (18, 18), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    body = [(2, 2), (15, 2), (15, 9), (13, 13), (9, 16), (4, 13), (2, 9)]
    d.polygon(body, fill=MID, outline=NAVY)
    d.polygon([(4, 4), (13, 4), (13, 9), (11, 12), (8, 14), (5, 12), (4, 9)], fill=PLATE)
    d.line([(2, 3), (2, 9)], fill=LT); d.line([(3, 2), (14, 2)], fill=LT)
    d.line([(15, 3), (15, 9)], fill=DK); d.line([(9, 15), (13, 12)], fill=DK)
    d.polygon([(8, 0), (10, 2), (8, 4), (6, 2)], fill=GEM, outline=NAVY); d.point((8, 2), fill=WHT)
    d.point((4, 4), fill=LT); d.point((13, 4), fill=LT)
    return im

def main():
    jar = find_jar()
    zf = zipfile.ZipFile(jar)
    icons = Image.open(io.BytesIO(zf.read("assets/minecraft/textures/gui/icons.png"))).convert("RGBA")
    bg = icons.crop((0, 64, 182, 69)); prog = icons.crop((0, 69, 182, 74))
    track = tint_track(bg, (0.7, 0.78, 1.05), (0, 0, 8))
    track.save(os.path.join(OUT, "xp_track.png")); track.save(os.path.join(OUT, "mana_track.png"))
    recolor_bar(prog, (34, 84, 200), (150, 210, 255)).save(os.path.join(OUT, "xp_fill.png"))
    recolor_bar(prog, (22, 120, 165), (165, 240, 255)).save(os.path.join(OUT, "mana_fill.png"))
    sp_gem().save(os.path.join(OUT, "sp_gem.png"))
    make_level_badge().save(os.path.join(OUT, "level_badge.png"))
    print("HUD art ->", OUT)
    for f in sorted(os.listdir(OUT)): print("  ", f, Image.open(os.path.join(OUT, f)).size)

if __name__ == "__main__":
    main()
