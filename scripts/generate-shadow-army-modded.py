#!/usr/bin/env python3
"""Add modded mob shadow reskins to the Ascendant Shadow Army pack. Same recolor as the
vanilla generator: near-black body, eyes baked in, plus a transparent "_e" emissive map
(ETF) so eyes/glow-parts bloom. Reads the real mod jars.

Usage: python scripts/generate-shadow-army-modded.py [mods_dir]
  mods_dir defaults to the active CurseForge instance's mods folder, else pass a path
  (or a folder of extracted jars). Requires Pillow, numpy.
"""
import os, sys, io, glob, hashlib, zipfile
import numpy as np
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK = os.path.join(REPO, "resourcepacks", "ascendant-shadow-army")
ASSETS = os.path.join(PACK, "assets")
EYE_CORE = np.array([215, 248, 255.]); EYE_GLOW = np.array([120, 205, 255.])

# (jar name substring, [(body_asset_path, emissive_source_or_None, label)])
MODDED = [
 ("born_in_chaos", [
   ("assets/born_in_chaos_v1/textures/entities/bone_imp.png", "assets/born_in_chaos_v1/textures/entities/bone_imp_e.png", "Shadow Bone Imp"),
   ("assets/born_in_chaos_v1/textures/entities/baby_skeleton.png", "assets/born_in_chaos_v1/textures/entities/babyskeleton_e.png", "Shadow Baby Skeleton"),
   ("assets/born_in_chaos_v1/textures/entities/bloodygadfly.png", "assets/born_in_chaos_v1/textures/entities/bloodygadfly_e.png", "Shadow Bloody Gadfly"),
   ("assets/born_in_chaos_v1/textures/entities/bonescaller.png", None, "Shadow Bonescaller"),
   ("assets/born_in_chaos_v1/textures/entities/barrel_zombie.png", None, "Shadow Barrel Zombie"),
 ]),
 ("mowziesmobs", [
   ("assets/mowziesmobs/textures/entity/frostmaw.png", None, "Shadow Frostmaw"),
   ("assets/mowziesmobs/textures/entity/foliaath.png", None, "Shadow Foliaath"),
 ]),
]

def lum(rgb): return 0.2126*rgb[...,0] + 0.7152*rgb[...,1] + 0.0722*rgb[...,2]
def seed_of(n): return int(hashlib.md5(n.encode()).hexdigest()[:8], 16)
def fractal(h, w, seed):
    rng = np.random.default_rng(seed)
    def layer(c):
        s = (rng.random((c, c))*255).astype('uint8')
        return np.asarray(Image.fromarray(s).resize((w, h), Image.BILINEAR), float)/255
    t = 0.6*layer(4) + 0.4*layer(8)
    return (t - t.min())/max(1e-6, t.max()-t.min())
def ramp(Lc):
    xs=[0,.40,.65,.85,1]
    return np.stack([np.interp(Lc,xs,[2,6,14,30,72]), np.interp(Lc,xs,[3,9,20,58,135]), np.interp(Lc,xs,[6,16,40,104,205])], -1)
def shadowize(rgb, seed):
    L = lum(rgb)/255.0; base = ramp(np.clip(L**1.7,0,1))
    out = base + (rgb - L[...,None]*255.0)*0.10
    return np.clip(out*(0.90 + 0.10*fractal(rgb.shape[0],rgb.shape[1],seed))[...,None], 0, 255)

def find_jar(mods_dir, sub):
    hits = [p for p in glob.glob(os.path.join(mods_dir, "*.jar")) if sub.lower() in os.path.basename(p).lower()]
    return hits[0] if hits else None

def write(rel, rgb, a):
    dst = os.path.join(ASSETS, rel[len("assets/"):].replace("/", os.sep))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    Image.fromarray(np.dstack([rgb, a]).astype('uint8'), "RGBA").save(dst)

def main():
    default_inst = os.path.expanduser("~/curseforge/minecraft/Instances")
    mods_dir = sys.argv[1] if len(sys.argv) > 1 else None
    if not mods_dir:
        cands = sorted(glob.glob(os.path.join(default_inst, "*", "mods")), reverse=True)
        mods_dir = cands[0] if cands else "."
    print("Mods dir:", mods_dir)
    done = []
    for sub, texs in MODDED:
        jar = find_jar(mods_dir, sub)
        if not jar:
            print("  (jar not found)", sub); continue
        zf = zipfile.ZipFile(jar); names = set(zf.namelist())
        for body, emi, label in texs:
            if body not in names:
                print("  (missing)", body); continue
            arr = np.asarray(Image.open(io.BytesIO(zf.read(body))).convert("RGBA"), float)
            rgb, a = arr[..., :3], arr[..., 3].copy()
            out = shadowize(rgb, seed_of(body))
            mask = np.zeros(rgb.shape[:2], bool); core = np.zeros(rgb.shape[:2], bool)
            if emi and emi in names:
                s = np.asarray(Image.open(io.BytesIO(zf.read(emi))).convert("RGBA"), float)
                if s.shape[:2] == rgb.shape[:2]:
                    sa, sL = s[..., 3], lum(s[..., :3])
                    m = (sa > 8) & (sL > 40)
                    if not m.any(): m = sa > 8
                    mask = m
                    if m.any(): core = m & (sL >= sL[m].mean())
            out[mask] = EYE_GLOW; out[core] = EYE_CORE
            write(body, out, a)
            # emissive map(s): ETF "<body>_e.png" convention + override the original _e name
            if mask.any():
                em = np.zeros((*rgb.shape[:2], 4), float)
                em[mask] = np.append(EYE_GLOW, 255); em[core] = np.append(EYE_CORE, 255)
                targets = {body[:-4] + "_e.png"}
                if emi: targets.add(emi)
                for t in targets:
                    write(t, em[..., :3], em[..., 3])
            done.append((label, body, bool(mask.any())))
    print(f"Recolored {len(done)} modded textures:")
    for label, body, glow in done:
        print(f"  {'glow' if glow else '    '}  {label:24s} {body}")

if __name__ == "__main__":
    main()
