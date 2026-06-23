#!/usr/bin/env python3
"""Solo Leveling 'gate' rift visuals: swirling VORTEX with a white-hot core, full spiral
arms, a DEFINED glowing OUTER RIM, gap fill + mystical wisps, and a soft outer halo.
Single centered sprite animated by rotation (seamless loop). 64x64 x 32 frames vertical
strip + .mcmeta, 5 rank colors. Translucent in the gaps so it still reads as a rift.
Requires Pillow, numpy.
"""
import os
import numpy as np
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "gate-art"); os.makedirs(OUT, exist_ok=True)
RP_GATE_OUT = os.path.join(REPO, "resourcepacks", "ascendant-dungeon-gates", "assets", "ascendant_dungeons", "textures", "gate")
RP_ITEM_OUT = os.path.join(REPO, "resourcepacks", "ascendant-dungeon-gates", "assets", "ascendant_dungeons", "textures", "item")
os.makedirs(RP_GATE_OUT, exist_ok=True)
os.makedirs(RP_ITEM_OUT, exist_ok=True)
S = 64; N = 32; ARMS = 2; TWIST = 5.0

RAMPS = {  # brightness 0..1 -> dark edge ... white-hot core
  "blue":   ([6,30,92,182,248],   [16,92,186,236,253], [40,176,236,255,255]),
  "purple": ([26,72,132,196,246], [8,26,82,160,236],   [44,150,222,250,255]),
  "red":    ([34,120,206,248,255],[8,24,60,128,214],   [12,28,52,98,178]),
  "gold":   ([40,140,214,248,255],[24,96,170,222,250], [8,18,40,116,206]),
  "green":  ([8,30,92,176,240],   [22,118,196,236,253],[16,52,104,150,226]),
}
XS = [0, .25, .5, .75, 1.0]

def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1); return t * t * (3 - 2 * t)

def write_mcmeta(folder, filename):
    open(os.path.join(folder, filename + ".mcmeta"), "w").write('{\n  "animation": {\n    "frametime": 1,\n    "interpolate": true\n  }\n}\n')

def item_aperture_strip(strip):
    yy, xx = np.mgrid[0:S, 0:S]
    dx = (xx - (S - 1) / 2) / (S / 2.0)
    dy = (yy - (S - 1) / 2) / (S / 2.0)
    r = np.sqrt(dx * dx + dy * dy)
    aperture = smoothstep(0.50, 0.78, r)
    tiled = np.tile(aperture, (N, 1))
    out = strip.copy().astype(np.float32)
    out[:, :, 3] *= tiled
    return np.clip(out, 0, 255).astype("uint8")

def build(name):
    R, G, B = RAMPS[name]
    rng = np.random.default_rng(11); noise = rng.random((S, S)); fine = rng.random((S, S))
    yy, xx = np.mgrid[0:S, 0:S]
    dx = (xx - (S - 1) / 2) / (S / 2.0); dy = (yy - (S - 1) / 2) / (S / 2.0)
    r = np.sqrt(dx * dx + dy * dy); theta = np.arctan2(dy, dx); logr = np.log(r + 0.06)
    frames = []
    for t in range(N):
        phase = 2 * np.pi * t / N
        arm    = 0.60 + 0.40 * np.sin(ARMS * theta - TWIST * logr + phase)        # main spiral
        swirl2 = 0.5 + 0.5 * np.sin(3 * theta + 4.0 * logr - 0.6 * phase)         # finer counter-swirl (depth)
        core   = np.exp(-(r / 0.30) ** 2)                                         # white-hot center
        glow   = np.exp(-(r / 0.60) ** 2)                                         # base radial fill
        env    = smoothstep(1.04, 0.08, r)                                        # arms extend nearly to rim
        rim    = np.exp(-((r - 0.86) / 0.05) ** 2)                                # defined glowing ring
        body = core * 1.5 + arm * env * (1 - core) * 1.02 + 0.38 * glow * (1 - core) + 0.22 * swirl2 * env * (1 - core)
        bright = np.clip(body, 0, 1) ** 0.80
        bright = np.clip(bright + 0.62 * rim, 0, 0.96)                            # rim = bright saturated ring
        bright = np.clip(bright * (0.92 + 0.08 * noise) + 0.05 * fine * env, 0, 1)  # sparkle wisps
        col = np.stack([np.interp(bright, XS, R), np.interp(bright, XS, G), np.interp(bright, XS, B)], -1)
        # alpha: fuller fill, defined rim, soft outer halo, gaps stay a little see-through
        disc = 1 - smoothstep(0.84, 0.99, r)
        halo = np.exp(-((r - 0.96) / 0.07) ** 2) * 0.45
        a = 0.30 + 0.64 * bright                                                  # gaps ~0.30, bright ~0.9
        alpha = np.clip(a * disc + 0.92 * rim * disc + halo, 0, 0.96)
        frames.append(np.dstack([np.clip(col, 0, 255), np.clip(alpha, 0, 1) * 255]).astype('uint8'))
    strip = np.concatenate(frames, axis=0)
    fn = "gate.png" if name == "blue" else f"gate_{name}.png"
    Image.fromarray(strip, "RGBA").save(os.path.join(OUT, fn))
    Image.fromarray(strip, "RGBA").save(os.path.join(RP_GATE_OUT, fn))
    Image.fromarray(item_aperture_strip(strip), "RGBA").save(os.path.join(RP_ITEM_OUT, fn))
    for folder in (OUT, RP_GATE_OUT, RP_ITEM_OUT):
        write_mcmeta(folder, fn)

for k in RAMPS: build(k)
print("enhanced gate art (rim + fill + halo) ->", OUT, "| colors:", ", ".join(RAMPS))

# ---------------- moving energy / wisps overlay layer (layer1) ----------------
WISP_COL = {"blue":(160,228,255),"red":(255,120,86),"gold":(255,212,130),
            "green":(150,236,176),"purple":(196,156,255)}

def build_wisps(name):
    col = WISP_COL[name]
    yy, xx = np.mgrid[0:S, 0:S]
    cx = cy = (S - 1) / 2.0
    dx = (xx - cx) / (S / 2.0); dy = (yy - cy) / (S / 2.0)
    r = np.sqrt(dx * dx + dy * dy); th = np.arctan2(dy, dx)
    rng = np.random.default_rng(7)
    tendrils = []
    for _ in range(6):
        rad = 0.60 + 0.32 * rng.random(); a0 = rng.random() * 2 * np.pi
        dirn = 1 if rng.random() < 0.65 else -1
        speed = dirn * (1 if rng.random() < 0.6 else 2)        # integer turns -> seamless
        arc = 0.45 + 0.65 * rng.random(); thick = 0.045 + 0.04 * rng.random()
        inten = 0.55 + 0.45 * rng.random()
        tendrils.append((rad, a0, speed, arc, thick, inten))
    embers = []
    for _ in range(11):
        a = rng.random() * 2 * np.pi; off = rng.random()
        sp = 1 if rng.random() < 0.5 else 2; drift = (rng.random() - 0.5) * 1.1
        embers.append((a, off, sp, drift))
    frames = []
    for t in range(N):
        ph = 2 * np.pi * t / N
        buf = np.zeros((S, S))
        for rad, a0, speed, arc, thick, inten in tendrils:
            ac = a0 + speed * ph
            dth = ((th - ac + np.pi) % (2 * np.pi)) - np.pi
            buf += inten * np.exp(-2 * (dth / arc) ** 2) * np.exp(-((r - rad) / thick) ** 2)
        for a, off, sp, drift in embers:
            p = (off + sp * ph / (2 * np.pi)) % 1.0
            er = 0.5 + 0.72 * p; ea = a + drift * p
            ex = cx + er * (S / 2.0) * np.cos(ea); ey = cy + er * (S / 2.0) * np.sin(ea)
            d2 = (xx - ex) ** 2 + (yy - ey) ** 2
            buf += 0.85 * np.sin(np.pi * p) * np.exp(-d2 / (1.7 ** 2))
        buf = np.clip(buf, 0, 1)
        buf *= (0.20 + 0.80 * smoothstep(0.34, 0.60, r))      # wisps live AROUND the core
        buf *= (1 - smoothstep(1.04, 1.26, r))                # fade beyond rim
        hot = buf ** 3
        R = col[0] + (255 - col[0]) * hot * 0.7
        G = col[1] + (255 - col[1]) * hot * 0.7
        B = col[2] + (255 - col[2]) * hot * 0.7
        alpha = np.clip(buf, 0, 1) * 0.85
        frames.append(np.dstack([np.clip(np.stack([R, G, B], -1), 0, 255), alpha * 255]).astype('uint8'))
    strip = np.concatenate(frames, axis=0)
    fn = "gate_wisps.png" if name == "blue" else f"gate_wisps_{name}.png"
    Image.fromarray(strip, "RGBA").save(os.path.join(OUT, fn))
    Image.fromarray(strip, "RGBA").save(os.path.join(RP_GATE_OUT, fn))
    Image.fromarray(strip, "RGBA").save(os.path.join(RP_ITEM_OUT, fn))
    for folder in (OUT, RP_GATE_OUT, RP_ITEM_OUT):
        write_mcmeta(folder, fn)

for k in WISP_COL: build_wisps(k)
print("wisps overlay layer ->", OUT)
