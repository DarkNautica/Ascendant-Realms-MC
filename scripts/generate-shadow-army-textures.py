#!/usr/bin/env python3
"""Generate the Ascendant Shadow Army resource pack: Solo Leveling "shadow" reskins of
vanilla mobs. Near-black smoky bodies with the mob's own eyes lit blue.

Emissive: ETF (enableEmissiveTextures + alwaysCheckVanillaEmissiveSuffix) makes any
"<texture>_e.png" glow. We ship a transparent _e map per mob with ONLY the eye/glow
pixels colored blue (transparent elsewhere) so the eyes truly glow without lighting the
whole body. The eyes are also baked into the base texture so they read with emissive off.
The vanilla native eye overlays (enderman/spider) are shipped blank so they can't glow
full-body additively.

Usage (from repo root): python scripts/generate-shadow-army-textures.py [1.20.1.jar]
Requires: Pillow, numpy.
"""
import os, sys, io, hashlib, zipfile
import numpy as np
from PIL import Image, ImageDraw

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK = os.path.join(REPO, "resourcepacks", "ascendant-shadow-army")
ENT  = os.path.join(PACK, "assets", "minecraft", "textures", "entity")
PREFIX = "assets/minecraft/textures/entity/"

EYE_CORE = np.array([215, 248, 255.])
EYE_GLOW = np.array([120, 205, 255.])

EYE_SRC = {                                  # body -> vanilla overlay holding its eye pixels
    "enderman/enderman.png": "enderman/enderman_eyes.png",
    "spider/spider.png": "spider_eyes.png",
    "spider/cave_spider.png": "spider_eyes.png",
}
BLANK = {"enderman/enderman_eyes.png", "spider_eyes.png"}   # native overlays -> ship blank


def find_jar():
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        return sys.argv[1]
    home = os.path.expanduser("~")
    appdata = os.environ.get("APPDATA", os.path.join(home, "AppData", "Roaming"))
    for c in [
        os.path.join(home, "curseforge", "minecraft", "Install", "versions", "1.20.1", "1.20.1.jar"),
        os.path.join(appdata, ".minecraft", "versions", "1.20.1", "1.20.1.jar"),
        os.path.join(home, ".minecraft", "versions", "1.20.1", "1.20.1.jar"),
    ]:
        if os.path.isfile(c):
            return c
    raise SystemExit('Minecraft 1.20.1 jar not found. Pass it explicitly:\n'
                     '  python scripts/generate-shadow-army-textures.py "C:\\path\\to\\1.20.1.jar"')


def seed_of(n):
    return int(hashlib.md5(n.encode()).hexdigest()[:8], 16)

def fractal(h, w, seed):
    rng = np.random.default_rng(seed)
    def layer(c):
        s = (rng.random((c, c)) * 255).astype('uint8')
        return np.asarray(Image.fromarray(s).resize((w, h), Image.BILINEAR), float) / 255
    t = 0.6 * layer(4) + 0.4 * layer(8)
    return (t - t.min()) / max(1e-6, t.max() - t.min())

def lum(rgb):
    return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]

def ramp(Lc):
    xs = [0, .40, .65, .85, 1]
    R = np.interp(Lc, xs, [2, 6, 14, 30, 72])
    G = np.interp(Lc, xs, [3, 9, 20, 58, 135])
    B = np.interp(Lc, xs, [6, 16, 40, 104, 205])
    return np.stack([R, G, B], axis=-1)

def shadowize(rgb, seed):
    L = lum(rgb) / 255.0
    Lc = np.clip(L ** 1.7, 0, 1)
    base = ramp(Lc)
    chroma = rgb - (L[..., None] * 255.0)
    out = base + chroma * 0.10
    n = fractal(rgb.shape[0], rgb.shape[1], seed)
    out = out * (0.90 + 0.10 * n)[..., None]
    return np.clip(out, 0, 255)

def face_eye_mask(rgb, region, max_frac=0.45):
    """Eyes = darkest pixels inside a face region. Returns (mask, core) full-size bool arrays."""
    h, w = rgb.shape[:2]
    mask = np.zeros((h, w), bool); core = np.zeros((h, w), bool)
    x0, y0, x1, y1 = region
    sub = rgb[y0:y1, x0:x1]
    if sub.size:
        L = lum(sub); mn = float(L.min())
        m = L <= mn + 16
        if m.mean() > max_frac:
            m = L <= mn + 5
        mask[y0:y1, x0:x1] = m
        core[y0:y1, x0:x1] = m & (L <= mn + 4)
    return mask, core

def src_eye_mask(zf, names, src_rel, shape):
    """Eyes/glow parts = opaque & bright pixels of a vanilla/mod emissive overlay."""
    h, w = shape
    mask = np.zeros((h, w), bool); core = np.zeros((h, w), bool)
    key = PREFIX + src_rel
    if key not in names:
        return mask, core
    s = np.asarray(Image.open(io.BytesIO(zf.read(key))).convert("RGBA"), float)
    if s.shape[:2] != shape:
        return mask, core
    sa, sL = s[..., 3], lum(s[..., :3])
    m = (sa > 8) & (sL > 40)
    if not m.any():
        m = sa > 8
    mask = m
    if m.any():
        core = m & (sL >= sL[m].mean())
    return mask, core

def save_rgba(rgb, a, rel):
    dst = os.path.join(ENT, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    Image.fromarray(np.dstack([rgb, a]).astype('uint8'), "RGBA").save(dst)

def save_emissive(rel, shape, mask, core):
    h, w = shape
    em = np.zeros((h, w, 4), float)
    em[mask] = np.append(EYE_GLOW, 255)
    em[core] = np.append(EYE_CORE, 255)
    rel_e = rel[:-4] + "_e.png"
    dst = os.path.join(ENT, rel_e.replace("/", os.sep))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    Image.fromarray(em.astype('uint8'), "RGBA").save(dst)


def main():
    jar = find_jar()
    print("Source jar:", jar)
    zf = zipfile.ZipFile(jar)
    names = set(zf.namelist())

    jobs = [
        ("zombie/zombie.png", "face"), ("zombie/husk.png", "face"),
        ("zombie/drowned.png", "face"), ("zombie/drowned_outer_layer.png", "plain"),
        ("zombie_villager/zombie_villager.png", "face"),
        ("skeleton/skeleton.png", "face"), ("skeleton/wither_skeleton.png", "face"),
        ("skeleton/stray.png", "face"), ("skeleton/stray_overlay.png", "plain"),
        ("creeper/creeper.png", "creeper"),
        ("enderman/enderman.png", "plain"), ("enderman/enderman_eyes.png", "blank"),
        ("spider/spider.png", "plain"), ("spider/cave_spider.png", "plain"),
        ("spider_eyes.png", "blank"),
        ("wolf/wolf.png", "plain"), ("wolf/wolf_tame.png", "plain"),
        ("wolf/wolf_angry.png", "plain"), ("wolf/wolf_collar.png", "plain"),
    ]
    for n in sorted(names):
        if n.startswith(PREFIX + "zombie_villager/") and n.endswith(".png"):
            rel = n[len(PREFIX):]
            if rel != "zombie_villager/zombie_villager.png":
                jobs.append((rel, "plain"))

    count = emissive = 0
    for rel, mode in jobs:
        key = PREFIX + rel
        if key not in names:
            print("  (skip, not in jar)", rel)
            continue
        arr = np.asarray(Image.open(io.BytesIO(zf.read(key))).convert("RGBA"), float)
        rgb, a = arr[..., :3], arr[..., 3].copy()
        if mode == "blank":
            save_rgba(np.zeros_like(rgb), np.zeros_like(a), rel)
            count += 1
            continue
        out = shadowize(rgb, seed_of(rel))
        mask = np.zeros(rgb.shape[:2], bool); core = np.zeros(rgb.shape[:2], bool)
        if mode == "face":
            mask, core = face_eye_mask(rgb, (8, 8, 16, 16))
        elif mode == "creeper":
            mask, core = face_eye_mask(rgb, (8, 8, 16, 12))
        if rel in EYE_SRC:
            m2, c2 = src_eye_mask(zf, names, EYE_SRC[rel], rgb.shape[:2])
            mask, core = mask | m2, core | c2
        out[mask] = EYE_GLOW
        out[core] = EYE_CORE
        save_rgba(out, a, rel)
        count += 1
        if mask.any():
            save_emissive(rel, rgb.shape[:2], mask, core)
            emissive += 1

    with open(os.path.join(PACK, "pack.mcmeta"), "w") as f:
        f.write('{\n  "pack": {\n    "pack_format": 15,\n'
                '    "description": "\\u00a75Ascendant Shadow Army \\u00a77- shadow reskins of mobs"\n  }\n}\n')
    ic = Image.new("RGBA", (128, 128), (4, 5, 10, 255)); d = ImageDraw.Draw(ic)
    for r, al in [(54, 40), (44, 70), (34, 110)]:
        d.ellipse([64 - r, 64 - r, 64 + r, 64 + r], outline=(60, 130, 220, al))
    d.polygon([(64, 30), (86, 64), (64, 98), (42, 64)], outline=(110, 190, 255, 255))
    d.ellipse([52, 58, 60, 66], fill=(210, 245, 255, 255)); d.ellipse([68, 58, 76, 66], fill=(210, 245, 255, 255))
    ic.save(os.path.join(PACK, "pack.png"))
    print(f"Recolored {count} textures ({emissive} with _e emissive maps) into {PACK}")


if __name__ == "__main__":
    main()
