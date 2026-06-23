#!/usr/bin/env python3
"""Ascendant Realms title-screen art - BRIGHT PAINTERLY (Mojang splash style).
Sunset vista with depth: forest-framed view over a reflective lake to a far shore, glowing
sun + distant gate, a lone hunter on a dock. Soft edges, bright, complements blue/green title.
1920x1080 -> config/fancymenu/assets/ascendant_realms_menu_art.png. Requires Pillow, numpy.
"""
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(REPO,"config/fancymenu/assets"); os.makedirs(OUT,exist_ok=True)
W,H=1920,1080
SHORE=566          # far shore line
LAKE_TOP=566; LAKE_BOT=940; BANK=940
rng=random.Random(5)
def lerp(a,b,t): return tuple(a[i]+(b[i]-a[i])*t for i in range(len(a)))
def newL(): return Image.new("RGBA",(W,H),(0,0,0,0))
def comp(layer,blur=0): img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)) if blur else layer)

# ---- SKY ----
stops=[(0.0,(120,112,194)),(0.34,(182,124,194)),(0.56,(236,136,166)),
       (0.74,(252,166,134)),(0.90,(255,202,146)),(1.0,(255,240,202))]
sky=np.zeros((H,W,3),np.float32)
for y in range(SHORE+30):
    t=y/(SHORE+30)
    for i in range(len(stops)-1):
        a,ca=stops[i]; b,cb=stops[i+1]
        if a<=t<=b: sky[y,:]=lerp(ca,cb,(t-a)/(b-a)); break
img=Image.fromarray(np.clip(sky,0,255).astype('uint8')).convert("RGBA"); d=ImageDraw.Draw(img,"RGBA")

# ---- SUN + bloom (center-right) ----
SX,SY=1240,486
for r,a in [(380,42),(260,58),(180,86),(120,140)]:
    l=newL(); ImageDraw.Draw(l).ellipse([SX-r,SY-r,SX+r,SY+r],fill=(255,240,206,a)); comp(l,64)
l=newL(); ImageDraw.Draw(l).ellipse([SX-82,SY-82,SX+82,SY+82],fill=(255,252,240,255)); comp(l,14)
# clouds
cl=newL(); dc=ImageDraw.Draw(cl)
for _ in range(10):
    cx=rng.randint(0,W); cy=rng.randint(60,420); cw=rng.randint(200,460); ch=rng.randint(24,54)
    c=lerp((255,214,204),(255,176,168),rng.random()); dc.ellipse([cx-cw,cy-ch,cx+cw,cy+ch],fill=(int(c[0]),int(c[1]),int(c[2]),64))
comp(cl,36)

# ---- distant hills + gate on far shore ----
def hill(yb,amp,col,al,bl):
    l=newL(); dl=ImageDraw.Draw(l); pts=[(0,H)]; x=-40
    while x<=W+40: pts.append((x, yb-amp*(0.5+0.5*math.sin(x*0.0015+yb)))); x+=26
    pts.append((W,H)); dl.polygon(pts,fill=(*col,al)); comp(l,bl)
hill(540,64,(220,168,184),200,9); hill(560,44,(196,150,182),205,6)
GX,GY,GR=470,548,52
g=newL(); dg=ImageDraw.Draw(g)
dg.ellipse([GX-GR*1.7,GY-GR*1.7,GX+GR*1.7,GY+GR*1.7],fill=(150,235,255,55))
dg.ellipse([GX-GR,GY-GR,GX+GR,GY+GR],fill=(214,250,255,140)); dg.ellipse([GX-GR,GY-GR,GX+GR,GY+GR],outline=(150,240,255,210),width=4)
comp(g,4)

# ---- far shore (lush lit green band with trees) ----
fs=newL(); dfs=ImageDraw.Draw(fs)
pts=[(0,H)]; x=-20
while x<=W+20: pts.append((x, SHORE-10*math.sin(x*0.004))); x+=22
pts+=[(W,H)]; dfs.polygon(pts,fill=(96,140,74,255))
fs2=newL(); ImageDraw.Draw(fs2).polygon(pts,fill=(150,190,104,255))  # lit grass rim
comp(fs2.filter(ImageFilter.GaussianBlur(3))); comp(fs,2)

# ---- LAKE: reflective water ----
wg=np.zeros((H,W,4),np.uint8)
for y in range(LAKE_TOP,LAKE_BOT):
    t=(y-LAKE_TOP)/(LAKE_BOT-LAKE_TOP)
    c=lerp((250,196,158),(150,104,150),t); wg[y,:]=(int(c[0]),int(c[1]),int(c[2]),255)
water=Image.fromarray(wg,"RGBA"); comp(water)
# sun reflection (broken shimmer column under the sun)
rf=newL(); drf=ImageDraw.Draw(rf)
for y in range(LAKE_TOP+8,LAKE_BOT,9):
    t=(y-LAKE_TOP)/(LAKE_BOT-LAKE_TOP); wdt=int(30*(1-t)+8); ox=rng.randint(-wdt,wdt)//2
    drf.ellipse([SX+ox-wdt//2,y-2,SX+ox+wdt//2,y+2],fill=(255,246,216,int(95*(1-t)+18)))
for y in range(LAKE_TOP+8,LAKE_TOP+150,10):
    drf.ellipse([GX-7,y-2,GX+7,y+2],fill=(160,238,255,60))
comp(rf,5)
# ripples + lily pads
rp=newL(); drp=ImageDraw.Draw(rp)
for y in range(LAKE_TOP+18,LAKE_BOT,20): drp.line([(0,y),(W,y)],fill=(255,255,255,22),width=2)
for _ in range(12):
    lx=rng.randint(60,W-60); ly=rng.randint(LAKE_TOP+70,LAKE_BOT-30); s=rng.randint(7,14)
    drp.ellipse([lx-s,ly-s//2,lx+s,ly+s//2],fill=(72,118,66,190))
comp(rp,1)

# ---- soft trees (painterly) ----
def tree(cx,base,scale,far=False):
    l=newL(); dl=ImageDraw.Draw(l); th=int(40*scale); tw=max(3,int(7*scale))
    tr=lerp((150,150,168),(92,66,50),0.0 if far else 1.0)
    dl.rectangle([cx-tw//2,base-th,cx+tw//2,base],fill=(int(tr[0]),int(tr[1]),int(tr[2]),255))
    cr=int(30*scale)
    for ox,oy,rr,sh in [(-cr*0.6,-th-cr*0.4,cr,0.1),(cr*0.5,-th-cr*0.3,cr*0.9,0.3),(0,-th-cr*1.0,cr*1.05,-0.15),(-cr*0.1,-th+cr*0.1,cr*0.8,0.4)]:
        c=lerp((158,200,98),(64,100,52),0.5+sh)
        if far: c=lerp(c,(205,176,186),0.5)
        dl.ellipse([cx+ox-rr,base+oy-rr,cx+ox+rr,base+oy+rr],fill=(int(c[0]),int(c[1]),int(c[2]),255))
    dl.ellipse([cx-cr,base-th-cr*1.4,cx+cr*0.2,base-th-cr*0.4],fill=(255,226,150,80))  # warm rim
    comp(l,3 if far else 1.5)
def canopy_band(yb,s0):
    l=newL(); dl=ImageDraw.Draw(l); x=-30
    while x<=W+30:
        s=s0*(0.7+0.6*rng.random()); cr=int(34*s); cx=x; cy=yb-int(16*s)-rng.randint(0,26)
        for ox,oy,rr,sh in [(-cr*0.5,0,cr,0.15),(cr*0.5,cr*0.1,cr*0.9,0.3),(0,-cr*0.6,int(cr*1.05),-0.12)]:
            c=lerp((152,198,98),(60,98,52),0.5+sh); dl.ellipse([cx+ox-rr,cy+oy-rr,cx+ox+rr,cy+oy+rr],fill=(int(c[0]),int(c[1]),int(c[2]),255))
        dl.ellipse([cx-cr,cy-int(cr*1.2),cx+int(cr*0.1),cy-int(cr*0.2)],fill=(255,226,150,55))
        x+=int(cr*0.85)
    comp(l,2)
canopy_band(SHORE+6,0.95)
for x in [250,980,1560,1770]:
    if abs(x-GX)<80: continue
    tree(x+rng.randint(-20,20), SHORE+rng.randint(2,12), 1.0+0.35*rng.random())

# ---- near bank + dock + hunter ----
nb=newL(); dnb=ImageDraw.Draw(nb)
pts=[(0,H),(0,BANK+24)]; x=0
while x<=W: pts.append((x, BANK+10*math.sin(x*0.006))); x+=24
pts+=[(W,H)]; dnb.polygon(pts,fill=(74,104,58,255))
ImageDraw.Draw(nb).polygon(pts,fill=(74,104,58,255))
comp(nb,2)
lit=newL(); ImageDraw.Draw(lit).polygon(pts[:-2]+[ (W,BANK), (0,BANK) ],fill=(140,178,96,160)); comp(lit,3)
# wooden dock (lower-left into lake)
dk=newL(); ddk=ImageDraw.Draw(dk)
ddk.polygon([(120,946),(470,902),(470,930),(120,980)],fill=(96,70,46,255))
for px in range(140,460,34): ddk.line([(px,978-(px-120)*0.12),(px,906-(px-120)*0.0)],fill=(60,42,28,180),width=3)
comp(dk,1)
# hunter standing at dock end, gazing toward sun (right)
hl=newL(); dh=ImageDraw.Draw(hl); hx,hy=440,902; u=4.6
def hb(x0,y0,x1,y1,c): dh.rectangle([hx+x0*u,hy+y0*u,hx+x1*u,hy+y1*u],fill=c)
SIL=(48,42,60,255)
hb(-3,-13,3,-6,SIL); hb(-2.5,-18,2.5,-13,SIL); hb(-3,-6,-0.3,0,SIL); hb(0.3,-6,3,0,SIL); hb(-4,-13,-3,-6,SIL); hb(3,-13,4,-6,SIL)
dh.rectangle([hx+2.6*u,hy-18*u,hx+3.4*u,hy-6*u],fill=(255,216,150,160))  # warm rim (sun side)
dh.rectangle([hx-2.5*u,hy-18.3*u,hx+2.6*u,hy-17.4*u],fill=(255,222,156,120))
comp(hl,0.8)

# ---- foreground framing trees (soft, out of focus) ----
fg=newL(); dfg=ImageDraw.Draw(fg)
dfg.rectangle([40,0,170,H],fill=(44,38,46,255))
for x in range(-20,340,42): dfg.ellipse([x-40,-60,x+70,210+rng.randint(0,140)],fill=(38,50,40,238))
for x in range(1640,1980,44): dfg.ellipse([x-40,-60,x+80,180+rng.randint(0,160)],fill=(40,50,42,238))
dfg.rectangle([1820,0,1920,H],fill=(42,36,44,238))
comp(fg,7)
# grass tufts
gt=newL(); dgt=ImageDraw.Draw(gt)
for x in range(0,W,24):
    if 360<x<1560 and rng.random()<0.55: continue
    gx=x+rng.randint(-8,8); gh=rng.randint(22,50); dgt.line([(gx,H),(gx+rng.randint(-6,6),H-gh)],fill=(38,58,36,235),width=3)
comp(gt,1)
# fireflies
ff=newL(); dff=ImageDraw.Draw(ff)
for _ in range(64):
    x=rng.randint(0,W); y=rng.randint(440,H-30); s=rng.choice([2,2,3,4]); dff.ellipse([x-s,y-s,x+s,y+s],fill=(255,246,170,rng.randint(120,235)))
comp(ff,1.0); comp(ff.filter(ImageFilter.GaussianBlur(5)))

# ---- atmosphere + grade ----
haze=newL(); ImageDraw.Draw(haze).rectangle([0,440,W,720],fill=(255,210,176,58)); comp(haze,90)
img=Image.blend(img,img.filter(ImageFilter.GaussianBlur(3)),0.20)
img=ImageEnhance.Color(img).enhance(1.18); img=ImageEnhance.Brightness(img).enhance(1.08); img=ImageEnhance.Contrast(img).enhance(1.05)
yy,xx=np.mgrid[0:H,0:W]; r=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2); vg=np.clip((r-0.82)/0.6,0,1)*84
img=Image.alpha_composite(img.convert("RGBA"),Image.fromarray(np.dstack([np.zeros((H,W)),np.zeros((H,W)),np.zeros((H,W)),vg]).astype('uint8')))
gnoise=(np.random.default_rng(1).random((H,W))*9-4.5).astype(np.int16)
base=np.asarray(img.convert("RGB")).astype(np.int16); img=Image.fromarray(np.clip(base+gnoise[...,None],0,255).astype('uint8'),"RGB")
out=os.path.join(OUT,"ascendant_realms_menu_art.png"); img.save(out)
img.resize((1366,768)).save(os.path.join(REPO,"codex-art","_menu_bright.png"))
print("bright painterly v2 ->", out, img.size)
