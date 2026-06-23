#!/usr/bin/env python3
"""Generate Arcane Void skill-tree art for the Ascendant Web (Puffish Skills):
  - a nebula background  -> assets/ascendant/textures/skilltree/background.png
  - lane-tinted frames per tier/state -> .../frames/<lane>_<tier>_<state>.png
  - 113 lane-colored glyph icons       -> .../icons/<node>.png
Writes into kubejs/assets/ascendant (KubeJS resource pack, always loaded).
Requires Pillow, numpy.
"""
import os, json, math, hashlib
import numpy as np
from PIL import Image, ImageDraw

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFS = os.path.join(REPO, "config/puffish_skills/categories/ascendant/definitions.json")
OUT  = os.path.join(REPO, "kubejs/assets/ascendant/textures/skilltree")
ICON = os.path.join(OUT, "icons"); FRAME = os.path.join(OUT, "frames")
for d in (ICON, FRAME): os.makedirs(d, exist_ok=True)

LANES = {
    "warrior":     (255, 92, 92),
    "rogue":       (178, 120, 255),
    "ranger":      (95, 230, 128),
    "arcanist":    (92, 196, 255),
    "engineer":    (255, 196, 70),
    "survivalist": (60, 224, 200),
    "dragonbound": (255, 132, 60),
    "ascendant":   (224, 246, 255),
}
TIER = {"task": "normal", "goal": "notable", "challenge": "major"}

def dark(c, f=0.32): return tuple(int(x*f) for x in c)
def light(c, f=0.5): return tuple(int(x+(255-x)*f) for x in c)

# ---------- background (arcane nebula) ----------
def make_background(path, S=1024):
    rng = np.random.default_rng(7)
    def fbm(scale, oct=5):
        acc = np.zeros((S, S)); amp = 1.0; tot = 0
        for o in range(oct):
            c = max(2, int(scale*(2**o)))
            g = rng.random((c, c)).astype('float32')
            up = np.asarray(Image.fromarray((g*255).astype('uint8')).resize((S, S), Image.BILINEAR), float)/255
            acc += up*amp; tot += amp; amp *= 0.5
        return acc/tot
    neb = fbm(3, 6)
    neb = (neb-neb.min())/(neb.max()-neb.min())
    yy, xx = np.mgrid[0:S, 0:S]
    r = np.sqrt((xx-S/2)**2+(yy-S/2)**2)/(S*0.7)
    vig = np.clip(1.2-r, 0, 1)
    deep = np.array([8, 7, 18]); mid = np.array([26, 20, 58]); glow = np.array([60, 70, 150])
    t = (neb**1.6)
    img = deep[None,None,:] + (mid-deep)[None,None,:]*t[...,None]
    img = img + (glow-mid)[None,None,:]*((neb*vig)**2.2)[...,None]*0.8
    # central arcane glow
    img = img + np.array([40, 60, 120])[None,None,:]*np.clip(1.1-r*1.3, 0, 1)[...,None]*0.5
    img = np.clip(img, 0, 255)
    out = Image.fromarray(img.astype('uint8'), "RGB").convert("RGBA")
    d = ImageDraw.Draw(out)
    # stars
    n = 1400
    for _ in range(n):
        x = rng.integers(0, S); y = rng.integers(0, S)
        b = rng.random()
        if b > 0.97: c = (200, 235, 255); s = 2
        elif b > 0.85: c = (150, 190, 255); s = 1
        else: c = (90, 110, 170); s = 1
        d.rectangle([x, y, x+s-1, y+s-1], fill=c)
    # a few faint rune rings
    for _ in range(5):
        cx, cy = rng.integers(120, S-120, size=2); rad = rng.integers(60, 160)
        col = (70, 90, 160, 40)
        d.ellipse([cx-rad, cy-rad, cx+rad, cy+rad], outline=col, width=2)
        d.ellipse([cx-rad+8, cy-rad+8, cx+rad-8, cy+rad-8], outline=(60, 80, 150, 28), width=1)
    out.save(path)

# ---------- frames (26x26 lane-tinted rune ring) ----------
def make_frame(lane, tier, state, path):
    c = LANES[lane]; S = 26
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    bright = state == "unlocked"
    ring = light(c, 0.45) if bright else c
    edge = dark(c, 0.22)
    inner_a = 120 if bright else 70
    # outer glow for unlocked
    if bright:
        for i, a in [(0, 26), (1, 18)]:
            d.ellipse([1-i, 1-i, S-2+i, S-2+i], outline=(*c, a), width=1)
    # node disc (tinted, translucent) so icon reads
    d.ellipse([4, 4, S-5, S-5], fill=(*dark(c, 0.16), inner_a))
    # main ring
    d.ellipse([2, 2, S-3, S-3], outline=edge, width=2)
    d.ellipse([3, 3, S-4, S-4], outline=ring, width=2)
    if bright:
        d.ellipse([5, 5, S-6, S-6], outline=(*light(c, 0.7), 150), width=1)
    pts_card = [(13, 1), (13, 24), (1, 13), (24, 13)]
    pts_diag = [(4, 4), (21, 4), (4, 21), (21, 21)]
    if tier in ("notable", "major"):
        for (x, y) in pts_card:
            d.ellipse([x-1, y-1, x+1, y+1], fill=ring); d.point([x, y], fill=light(c, 0.8))
    if tier == "major":
        for (x, y) in pts_diag:
            d.polygon([(x, y-2), (x+2, y), (x, y+2), (x-2, y)], fill=ring)
        d.ellipse([1, 1, S-2, S-2], outline=edge, width=1)
    im.save(path)

# ---------- glyph icons (16x16) ----------
def base_icon():
    return Image.new("RGBA", (16, 16), (0, 0, 0, 0))

def stroke(d, pts, col, w=1):
    d.line(pts, fill=col, width=w)

# each glyph: draw(d, dk, md, hi)
def g_sword(d, dk, md, hi):
    d.line([(8,1),(8,11)], fill=dk, width=3); d.line([(8,1),(8,11)], fill=md, width=1)
    d.point((8,2), fill=hi)
    d.line([(4,10),(12,10)], fill=dk, width=1)
    d.rectangle([7,11,9,13], fill=md); d.point((8,14), fill=dk)
def g_shield(d, dk, md, hi):
    d.polygon([(8,1),(13,3),(13,8),(8,14),(3,8),(3,3)], fill=md, outline=dk)
    d.line([(8,3),(8,11)], fill=hi); d.line([(5,6),(11,6)], fill=hi)
def g_axe(d, dk, md, hi):
    d.line([(6,2),(11,14)], fill=dk, width=2); d.line([(6,2),(11,14)], fill=light(md,.2), width=1)
    d.polygon([(4,2),(11,1),(12,6),(5,8)], fill=md, outline=dk); d.line([(6,3),(10,3)], fill=hi)
def g_bow(d, dk, md, hi):
    d.arc([3,2,12,13], 300, 60, fill=md, width=2); d.line([(11,3),(11,12)], fill=hi)
    d.line([(2,8),(13,8)], fill=dk, width=1); d.polygon([(13,8),(10,6),(10,10)], fill=md)
def g_dagger(d, dk, md, hi):
    d.line([(8,2),(8,10)], fill=dk, width=2); d.line([(8,2),(8,10)], fill=md, width=1); d.point((8,3), fill=hi)
    d.line([(5,10),(11,10)], fill=md); d.rectangle([7,11,8,13], fill=dk)
def g_boot(d, dk, md, hi):
    d.polygon([(5,2),(8,2),(8,9),(13,9),(13,13),(5,13)], fill=md, outline=dk); d.line([(6,3),(6,12)], fill=hi)
def g_book(d, dk, md, hi):
    d.rectangle([3,3,12,13], fill=md, outline=dk); d.line([(8,3),(8,13)], fill=dk)
    d.line([(5,6),(7,6)], fill=hi); d.line([(9,6),(11,6)], fill=hi); d.line([(5,9),(7,9)], fill=hi); d.line([(9,9),(11,9)], fill=hi)
def g_rune(d, dk, md, hi):
    d.polygon([(8,1),(14,8),(8,15),(2,8)], outline=md); d.polygon([(8,3),(12,8),(8,13),(4,8)], outline=dk)
    d.line([(8,4),(8,12)], fill=md); d.line([(5,8),(11,8)], fill=md); d.point((8,8), fill=hi)
def g_snow(d, dk, md, hi):
    for a in range(0,360,60):
        x=8+int(6*math.cos(math.radians(a))); y=8+int(6*math.sin(math.radians(a)))
        d.line([(8,8),(x,y)], fill=md, width=1)
    d.point((8,8), fill=hi)
    for a in range(0,360,60):
        x=8+int(4*math.cos(math.radians(a))); y=8+int(4*math.sin(math.radians(a)))
        d.point((x,y), fill=hi)
def g_flame(d, dk, md, hi):
    d.polygon([(8,1),(11,6),(11,11),(8,14),(5,11),(5,6)], fill=md, outline=dk)
    d.polygon([(8,5),(10,9),(8,12),(6,9)], fill=hi)
def g_bolt(d, dk, md, hi):
    d.polygon([(9,1),(4,8),(7,8),(6,15),(12,6),(9,6)], fill=md, outline=dk); d.line([(8,3),(6,7)], fill=hi)
def g_leaf(d, dk, md, hi):
    d.polygon([(8,1),(13,7),(8,15),(3,7)], fill=md, outline=dk); d.line([(8,2),(8,14)], fill=dk); d.line([(8,6),(11,5)], fill=hi); d.line([(8,9),(5,8)], fill=hi)
def g_gear(d, dk, md, hi):
    d.ellipse([3,3,12,12], fill=md, outline=dk)
    for a in range(0,360,45):
        x=8+int(6*math.cos(math.radians(a))); y=8+int(6*math.sin(math.radians(a))); d.rectangle([x-1,y-1,x+1,y+1], fill=md)
    d.ellipse([6,6,9,9], fill=dk); d.point((7,5), fill=hi)
def g_eye(d, dk, md, hi):
    d.ellipse([2,5,13,10], fill=light(md,.15), outline=dk); d.ellipse([6,5,10,10], fill=dk); d.point((8,7), fill=hi)
def g_dragon(d, dk, md, hi):
    d.polygon([(2,9),(7,7),(9,3),(11,7),(14,7),(11,10),(13,13),(8,11),(4,13)], fill=md, outline=dk)
    d.point((9,7), fill=hi); d.line([(9,3),(10,1)], fill=md)
def g_crown(d, dk, md, hi):
    d.polygon([(3,12),(3,6),(6,9),(8,4),(10,9),(13,6),(13,12)], fill=md, outline=dk); d.line([(3,12),(13,12)], fill=dk)
    d.point((8,5), fill=hi); d.point((4,7), fill=hi); d.point((12,7), fill=hi)
def g_star(d, dk, md, hi):
    for a in range(0,360,45):
        r=7 if a%90==0 else 3; x=8+int(r*math.cos(math.radians(a))); y=8+int(r*math.sin(math.radians(a)))
        d.line([(8,8),(x,y)], fill=md, width=1)
    d.ellipse([6,6,9,9], fill=hi)
def g_gem(d, dk, md, hi):
    d.polygon([(8,1),(13,6),(8,15),(3,6)], fill=md, outline=dk); d.line([(3,6),(13,6)], fill=dk); d.line([(8,1),(8,15)], fill=light(md,.3)); d.point((6,4), fill=hi)
def g_cross(d, dk, md, hi):
    d.rectangle([6,2,9,13], fill=md, outline=dk); d.rectangle([2,6,13,9], fill=md, outline=dk); d.point((7,7), fill=hi)
def g_portal(d, dk, md, hi):
    d.ellipse([3,3,12,12], outline=md, width=2); d.ellipse([6,6,9,9], outline=hi); d.arc([1,1,14,14],200,40, fill=light(md,.3))
def g_compass(d, dk, md, hi):
    d.ellipse([2,2,13,13], outline=md, width=1); d.polygon([(8,3),(10,8),(8,12),(6,8)], fill=md); d.line([(8,3),(8,8)], fill=hi); d.point((8,8), fill=dk)
def g_skull(d, dk, md, hi):
    d.ellipse([3,2,12,11], fill=light(md,.15), outline=dk); d.ellipse([5,5,7,8], fill=dk); d.ellipse([8,5,10,8], fill=dk)
    d.rectangle([5,11,10,13], fill=md); d.line([(6,11),(6,13)], fill=dk); d.line([(9,11),(9,13)], fill=dk)
def g_totem(d, dk, md, hi):
    d.rectangle([5,2,10,14], fill=md, outline=dk); d.ellipse([6,4,9,7], fill=dk); d.line([(5,9),(10,9)], fill=hi); d.point((7,5), fill=hi)
def g_horn(d, dk, md, hi):
    d.arc([2,2,16,16], 150, 270, fill=md, width=3); d.point((4,5), fill=hi)
def g_chest(d, dk, md, hi):
    d.rectangle([3,5,12,13], fill=md, outline=dk); d.rectangle([3,5,12,7], fill=light(md,.2)); d.rectangle([7,7,8,10], fill=dk)

GLYPHS = {
 "sword": g_sword, "shield": g_shield, "axe": g_axe, "bow": g_bow, "dagger": g_dagger,
 "boot": g_boot, "book": g_book, "rune": g_rune, "snow": g_snow, "flame": g_flame,
 "bolt": g_bolt, "leaf": g_leaf, "gear": g_gear, "eye": g_eye, "dragon": g_dragon,
 "crown": g_crown, "star": g_star, "gem": g_gem, "cross": g_cross, "portal": g_portal,
 "compass": g_compass, "skull": g_skull, "totem": g_totem, "horn": g_horn, "chest": g_chest,
}

# keyword -> glyph (first hit wins, scanned against node id + title)
KW = [
 ("dragon","dragon"),("wyrm","dragon"),("scale","dragon"),("rider","dragon"),("mounted","dragon"),
 ("frost","snow"),("ice","snow"),("cold","snow"),("winter","snow"),("snow","snow"),
 ("flame","flame"),("fire","flame"),("blaze","flame"),("forge","flame"),("temper","flame"),("cataclysm","flame"),
 ("storm","bolt"),("lightning","bolt"),("thunder","bolt"),("spark","bolt"),
 ("shield","shield"),("guard","shield"),("bulwark","shield"),("bastion","shield"),("ward","shield"),("plate","shield"),("mail","shield"),("armor","shield"),
 ("axe","axe"),("heavy","axe"),("giant","axe"),("titan","axe"),("break","axe"),
 ("bow","bow"),("draw","bow"),("marks","bow"),("sky","bow"),("arrow","bow"),("tension","bow"),("beast_breaker","bow"),
 ("knife","dagger"),("backstab","dagger"),("cutpurse","dagger"),("glass","dagger"),("grip","dagger"),("edge","dagger"),
 ("step","boot"),("quick","boot"),("stride","boot"),("travel","boot"),("path","boot"),("delver","boot"),("landing","boot"),("roll","boot"),("soft","boot"),
 ("lore","book"),("scholar","book"),("monster_lore","book"),("habit","book"),("math","book"),("formula","book"),("reading","book"),
 ("rune","rune"),("glyph","rune"),("mana","rune"),("arcane","rune"),("spell","rune"),("invoker","rune"),("archmage","rune"),("weave","rune"),("ritual","rune"),("channel","rune"),("focus","rune"),
 ("leaf","leaf"),("nature","leaf"),("season","leaf"),("wheat","leaf"),("ration","leaf"),("provision","leaf"),("medic","cross"),("camp","leaf"),("hearth","flame"),
 ("gear","gear"),("tinker","gear"),("workshop","gear"),("factory","gear"),("artificer","gear"),("engine","gear"),("siege","gear"),("cannon","gear"),("brass","gear"),("logistic","gear"),("belt","gear"),("repair","gear"),("ship","gear"),("frame","gear"),("loader","gear"),
 ("eye","eye"),("sense","eye"),("track","eye"),("instinct","eye"),("venom","eye"),("apex","eye"),
 ("crown","crown"),("lord","crown"),("legend","crown"),("champion","crown"),("command","crown"),("warlord","crown"),("master","crown"),("king","crown"),
 ("star","star"),("oath","star"),("ascendant","star"),("ender","star"),("myth","star"),("realm","star"),
 ("relic","gem"),("artifact","gem"),("trophy","gem"),("treasure","gem"),("luck","gem"),("market","chest"),("looter","chest"),("night_market","chest"),
 ("portal","portal"),("shadowstep","portal"),("pearl","portal"),("moonlit","portal"),("gap","portal"),("panic","portal"),
 ("compass","compass"),("pathfinder","compass"),("expedition","compass"),("map","compass"),("weather","compass"),("cliff","compass"),
 ("slayer","skull"),("hunter","skull"),("abyssal","skull"),("boss","skull"),("hunt","skull"),
 ("totem","totem"),("undying","totem"),("ready","totem"),("oath_w","totem"),
 ("horn","horn"),("trophy_marks","horn"),
 ("bond","leaf"),("pack","leaf"),("tamed","leaf"),("wild","leaf"),
 ("feather","boot"),("recovery","cross"),("heal","cross"),
 ("pressure","sword"),("rhythm","sword"),("forms","sword"),("momentum","sword"),("duelist","sword"),("blade","sword"),("counter","sword"),("weight","sword"),
]
def pick_glyph(node, title):
    s = (node + " " + title).lower()
    for kw, g in KW:
        if kw in s: return g
    return "rune"

def make_icon(node, lane, glyph, path):
    c = LANES[lane]
    im = base_icon(); d = ImageDraw.Draw(im)
    GLYPHS[glyph](d, dark(c, 0.30), c, light(c, 0.55))
    im.save(path)


THEME_OF = {"warrior": "combat", "rogue": "exploration", "ranger": "hunting", "arcanist": "magic", "engineer": "crafting", "survivalist": "survival", "dragonbound": "dragon", "ascendant": "magic"}
ZIPTIER = {"normal": "normal", "notable": "notable", "major": "keystone"}
NODE_SRC = os.path.join(REPO, "codex-art", "skilltree_nodes")

NODE_SCALE = 1.5   # bump node/icon render size

def _upscale(path):
    im = Image.open(path).convert("RGBA")
    im = im.resize((round(im.width * NODE_SCALE), round(im.height * NODE_SCALE)), Image.NEAREST)
    im.save(path)

def copy_frames():
    import shutil
    for lane in LANES:
        theme = THEME_OF.get(lane, "magic")
        for tier in ("normal", "notable", "major"):
            zt = ZIPTIER[tier]
            u = os.path.join(FRAME, lane + "_" + tier + "_unlocked.png")
            av = os.path.join(FRAME, lane + "_" + tier + "_available.png")
            shutil.copyfile(os.path.join(NODE_SRC, "frames", theme + "_" + zt + "_unlocked.png"), u); _upscale(u)
            shutil.copyfile(os.path.join(NODE_SRC, "masters", zt + "_master.png"), av); _upscale(av)

def main():
    make_background(os.path.join(OUT, "background.png"), 1600)
    copy_frames()
    import shutil
    ICON_SRC = os.path.join(REPO, "codex-art", "skilltree_icons")
    defs = json.load(open(DEFS))
    n = 0
    for node, v in defs.items():
        dst = os.path.join(ICON, node + ".png")
        src = os.path.join(ICON_SRC, node + ".png")
        if os.path.isfile(src):
            shutil.copyfile(src, dst)   # custom art
        else:
            lane = node.split("_")[0]
            if lane not in LANES: lane = "ascendant"
            title = v.get("title", "") if isinstance(v.get("title"), str) else ""
            glyph = "star" if node == "ascendant_oath" else pick_glyph(node, title)
            make_icon(node, lane, glyph, dst)   # procedural fallback
        _upscale(dst)
        n += 1
    print(f"bg + {len(LANES)*3*2} frames + {n} icons -> {OUT}")

if __name__ == "__main__":
    main()
