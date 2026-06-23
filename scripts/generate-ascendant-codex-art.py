#!/usr/bin/env python3
"""Ascendant Codex grimoire art -> kubejs/assets/ascendant_realms/textures/...
Restyles Patchouli's book_purple.png (512x256) into an Arcane Void grimoire GUI
(exact UV layout preserved so text/arrows/progress still align), plus a held-book
item texture+model and a chapter banner. Source GUI is extracted from the Patchouli
jar at runtime (not redistributed). Requires Pillow, numpy.
"""
import os, sys, io, zipfile, glob
import numpy as np
from PIL import Image, ImageDraw

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = os.path.join(REPO, "kubejs/assets/ascendant_realms")
GUI = os.path.join(NS, "textures/gui"); ITEM = os.path.join(NS, "textures/item")
MODELS = os.path.join(NS, "models/item")
for d in (GUI, os.path.join(GUI, "codex"), ITEM, MODELS): os.makedirs(d, exist_ok=True)

# Arcane Void palette
VOID_TOP=(27,22,44); VOID_BOT=(17,13,28); LEATHER=(34,27,55); LEATHER_HI=(52,43,82)
CYAN=(124,242,255); CYAN_DIM=(70,120,170); GOLD=(255,213,138); MOON=(220,230,255)

def find_patchouli():
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]): return sys.argv[1]
    home=os.path.expanduser("~")
    pats=[os.path.join(home,"curseforge/minecraft/Instances/*/mods/Patchouli*.jar"),
          os.path.join(home,"curseforge/minecraft/Install/mods/Patchouli*.jar"),
          "/sessions/*/mnt/*/mods/Patchouli*.jar"]
    for p in pats:
        g=sorted(glob.glob(p))
        if g: return g[0]
    raise SystemExit("Patchouli jar not found; pass path as arg")

def erode(mask, k):
    m = mask.copy()
    for _ in range(k):
        m = m & np.roll(m,1,0) & np.roll(m,-1,0) & np.roll(m,1,1) & np.roll(m,-1,1)
    return m

def lerp(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))

def build_gui(src):
    im = np.asarray(Image.open(io.BytesIO(src)).convert("RGBA"), float)
    H,W = im.shape[:2]; rgb=im[...,:3]; a=im[...,3]
    L = (0.2126*rgb[...,0]+0.7152*rgb[...,1]+0.0722*rgb[...,2])/255.0
    warm = rgb[...,0] - rgb[...,2]
    has = a > 8
    spread = np.zeros((H,W),bool); spread[:188,:280] = True
    page    = has & spread & (L>0.60) & (warm>10)       # cream pages
    leather = has & spread & ~page                       # binding/frame
    ui      = has & ~spread                              # arrows/progress/buttons
    out = np.zeros_like(im); out[...,3]=a
    yy,xx = np.mgrid[0:H,0:W]
    # ----- pages -> dark arcane vellum with grain + vignette -----
    pidx = np.where(page)
    if len(pidx[0]):
        ys = pidx[0]; ty = ys/188.0
        grain = np.clip((L[page]-0.60)/0.40,0,1)
        base = np.stack([np.interp(ty,[0,1],[VOID_TOP[c],VOID_BOT[c]]) for c in range(3)],1)
        base = base*(0.82+0.30*grain[:,None])           # paper grain -> faint lightening
        out[...,:3][page] = np.clip(base,0,255)
    # per-page vignette + inner glow frame + rune ring
    img = Image.fromarray(np.clip(out,0,255).astype('uint8'),"RGBA")
    edge = page & ~erode(page,5)
    glow = np.zeros((H,W),float); glow[edge]=1.0
    g3 = np.dstack([glow*CYAN[0],glow*CYAN[1],glow*CYAN[2],glow*70]).astype('uint8')
    img.alpha_composite(Image.fromarray(g3,"RGBA"))
    # subtle rune corner ornaments per page (kept out of the text body)
    pcols=np.where(page.any(0))[0]; prows=np.where(page.any(1))[0]
    if len(pcols) and len(prows):
        spine=int((pcols.min()+pcols.max())/2)
        x0,x1,y0,y1=int(pcols.min()),int(pcols.max()),int(prows.min()),int(prows.max())
        d=ImageDraw.Draw(img,"RGBA")
        def corner(px,py,dx,dy,al=70):
            d.line([(px,py),(px+dx*6,py)],fill=(*CYAN,al)); d.line([(px,py),(px,py+dy*6)],fill=(*CYAN,al))
        for (lx,rx) in [(x0+6,spine-6),(spine+7,x1-6)]:
            corner(lx,y0+6,1,1); corner(rx,y0+6,-1,1); corner(lx,y1-6,1,-1); corner(rx,y1-6,-1,-1)
            cxp=(lx+rx)//2
            d.polygon([(cxp,y1-10),(cxp+3,y1-7),(cxp,y1-4),(cxp-3,y1-7)],outline=(*CYAN,55))
    out = np.asarray(img,float)
    # ----- leather binding -> void indigo -----
    lidx=np.where(leather)
    if len(lidx[0]):
        l=np.clip((L[leather]-0.10)/0.55,0,1)
        col=np.stack([np.interp(l,[0,1],[LEATHER[c],LEATHER_HI[c]]) for c in range(3)],1)
        out[...,:3][leather]=np.clip(col,0,255)
    img=Image.fromarray(np.clip(out,0,255).astype('uint8'),"RGBA")
    # cyan trim along inner page/leather boundary
    from PIL import ImageFilter
    page_dil = np.asarray(Image.fromarray((page*255).astype('uint8')).filter(ImageFilter.MaxFilter(7)))>0
    trim = leather & (~erode(leather,2)) & page_dil
    tr=np.zeros((H,W),float); tr[trim]=1
    img.alpha_composite(Image.fromarray(np.dstack([tr*CYAN[0],tr*CYAN[1],tr*CYAN[2],tr*60]).astype('uint8'),"RGBA"))
    out=np.asarray(img,float)
    # ----- UI bits (arrows/progress/buttons) -> cyan luminance ramp -----
    uidx=np.where(ui)
    if len(uidx[0]):
        l=L[ui]
        col=np.stack([np.interp(l,[0,.5,1],[10,CYAN_DIM[c],CYAN[c]]) for c in range(3)],1)
        out[...,:3][ui]=np.clip(col,0,255)
    Image.fromarray(np.clip(out,0,255).astype('uint8'),"RGBA").save(os.path.join(GUI,"codex_book.png"))

def build_item():
    P={".":(0,0,0,0),"k":(10,8,16,255),"c":(28,22,44,255),"C":(40,32,62,255),
       "e":(58,47,88,255),"y":(124,242,255,255),"g":(255,213,138,255),"m":(150,170,210,255),"w":(230,240,255,255)}
    grid=[
      "................",
      "...kkkkkkkkkk...",
      "..kCCCCCCCCCCk..",
      "..kCeeeeeeeeCk..",
      "..kCe.yyyy.eCk..",
      "..kCe.y..y.eCk..",
      "..kCe.yyyy.eCk..",
      "..kCe.y....eCk..",
      "..kCe.y....eCk..",
      "..kCeeeeeeeeCk..",
      "..kCeeeeeeeeCk..",
      "..kCe.gg...eCk..",
      "..kCgggg...eCk..",
      "..kCe.gg...eCk..",
      "...kCCCCCCCCk...",
      "....kkkkkkkk...."]
    im=Image.new("RGBA",(16,16),(0,0,0,0))
    for y,r in enumerate(grid):
        for x,ch in enumerate(r):
            if ch in P: im.putpixel((x,y),P[ch])
    im.save(os.path.join(ITEM,"ascendant_codex.png"))
    open(os.path.join(MODELS,"ascendant_codex.json"),"w").write(
      '{\n  "parent": "item/generated",\n  "textures": { "layer0": "ascendant_realms:item/ascendant_codex" }\n}\n')

def build_banner():
    W,Hh=200,84; im=Image.new("RGBA",(W,Hh),(0,0,0,0)); d=ImageDraw.Draw(im,"RGBA")
    for y in range(Hh):
        t=y/Hh; c=lerp(VOID_TOP,VOID_BOT,t); d.line([(0,y),(W,y)],fill=(*c,235))
    # vortex motif
    import math
    cx,cy=W//2,Hh//2
    for i in range(220):
        a=i*0.30; rr=i*0.16; x=cx+rr*math.cos(a); y=cy+rr*0.5*math.sin(a)
        if 0<=x<W and 0<=y<Hh:
            br=max(0,1-rr/46); col=lerp((40,60,90),CYAN,br)
            d.point((x,y),fill=(*col,int(120+120*br)))
    d.ellipse([cx-5,cy-5,cx+5,cy+5],fill=(*MOON,255))
    # rune frame
    d.rectangle([2,2,W-3,Hh-3],outline=(*CYAN,150))
    d.rectangle([5,5,W-6,Hh-6],outline=(*CYAN_DIM,120))
    for x in range(10,W-10,14): d.line([(x,2),(x,7)],fill=(*CYAN,90)); d.line([(x,Hh-8),(x,Hh-3)],fill=(*CYAN,90))
    im.save(os.path.join(GUI,"codex","banner_getting_started.png"))

def main():
    jar=find_patchouli(); src=zipfile.ZipFile(jar).read("assets/patchouli/textures/gui/book_purple.png")
    build_gui(src); build_item(); build_banner()
    print("Codex art ->", NS)
    for root,_,fs in os.walk(NS):
        for f in fs:
            p=os.path.join(root,f)
            try: sz=Image.open(p).size
            except Exception: sz="-"
            print("  ", os.path.relpath(p,REPO), sz)

if __name__=="__main__": main()
