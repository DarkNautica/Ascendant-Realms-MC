#!/usr/bin/env python3
"""Animate AscendantBackgroundImage.png into a seamless ambient loop (chunked render).
Usage: python generate-ascendant-menu-anim.py <start> <end>   (renders frames [start,end))
Effects: breathing bloom, drifting+twinkling fireflies, water shimmer, star twinkle, drift.
Frames -> /tmp/menuframes/f_XXXX.jpg ; encode separately. Requires Pillow, numpy.
"""
import os, math, sys
import numpy as np
from PIL import Image, ImageFilter

REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC=os.path.join(REPO,"AscendantBackgroundImage.png")
FR="/tmp/menuframes"; os.makedirs(FR,exist_ok=True)
TW,TH=1600,900; ZOOM=1.03; WK,HK=int(TW*ZOOM),int(TH*ZOOM)
N=150
start=int(sys.argv[1]); end=int(sys.argv[2])
if start==0:
    for f in os.listdir(FR):
        if f.endswith(".jpg"): os.remove(os.path.join(FR,f))

base=Image.open(SRC).convert("RGB").resize((WK,HK),Image.LANCZOS)
B=np.asarray(base).astype(np.float32)
lum=0.2126*B[...,0]+0.7152*B[...,1]+0.0722*B[...,2]
bloom=np.asarray(Image.fromarray((B*np.clip((lum-205)/50,0,1)[...,None]).astype(np.uint8)).filter(ImageFilter.GaussianBlur(16))).astype(np.float32)
yy,xx=np.mgrid[0:HK,0:WK]
band=np.clip((yy-HK*0.60)/(HK*0.04),0,1)*np.clip((HK*0.96-yy)/(HK*0.06),0,1)
water=(band*np.clip((lum-90)/120,0,1)).astype(np.float32)
def kern(sz,sig):
    a=np.arange(sz)-sz//2; g=np.exp(-(a[:,None]**2+a[None,:]**2)/(2*sig*sig)); return (g/g.max()).astype(np.float32)
K=kern(13,2.6); KC=kern(5,1.1)
rng=np.random.default_rng(7); flies=[]
for _ in range(30):
    x=rng.integers(40,WK-40); y=rng.integers(int(HK*0.46),HK-26); cyan=(x>WK*0.66 and rng.random()<0.5)
    flies.append((float(x),float(y),rng.uniform(7,20),rng.uniform(5,14),rng.uniform(0,6.28),rng.uniform(0,6.28),
                  (150,232,255) if cyan else (255,236,150),rng.uniform(0.4,0.85),rng.uniform(0.4,0.7)))
stars=[(int(rng.integers(40,int(WK*0.6))),int(rng.integers(20,int(HK*0.24))),rng.uniform(0,6.28),rng.uniform(0.4,0.9)) for _ in range(12)]
def splat(out,cx,cy,k,col,amp):
    s=k.shape[0]; h=s//2; x0=int(cx)-h; y0=int(cy)-h; x1=x0+s; y1=y0+s
    kx0=max(0,-x0); ky0=max(0,-y0); x0=max(0,x0); y0=max(0,y0); x1=min(WK,x1); y1=min(HK,y1)
    if x1<=x0 or y1<=y0: return
    kk=k[ky0:ky0+(y1-y0),kx0:kx0+(x1-x0)]
    for c in range(3): out[y0:y1,x0:x1,c]+=kk*(col[c]*amp)
mx,my=WK-TW,HK-TH
for t in range(start,min(end,N)):
    p=2*math.pi*t/N; out=B.copy()
    out+=bloom*(0.16+0.08*math.sin(p))
    sh=np.sin(yy*0.045+xx*0.008-2*p); out+=(np.clip(sh-0.35,0,1)*water*24)[...,None]
    for (x,y,dx,dy,ph,tph,col,inten,halo) in flies:
        fx=x+dx*math.sin(p+ph); fy=y+dy*math.sin(p+ph+1.7); tw=0.25+0.75*(0.5+0.5*math.sin(2*p+tph))
        splat(out,fx,fy,K,col,15*halo*inten*tw); splat(out,fx,fy,KC,(255,240,195) if col[0]>200 else (200,238,255),44*inten*tw)
    for (x,y,tph,inten) in stars:
        tw=0.2+0.8*(0.5+0.5*math.sin(2*p+tph)); splat(out,x,y,KC,(235,240,255),60*inten*tw)
    out=np.clip(out,0,255).astype(np.uint8)
    ox=int(mx*0.5+20*math.sin(p)); oy=int(my*0.5+10*math.sin(p+math.pi/2))
    Image.fromarray(out[oy:oy+TH,ox:ox+TW]).save(f"{FR}/f_{t:04d}.jpg",quality=92)
    if t==0: Image.fromarray(out[oy:oy+TH,ox:ox+TW]).save(os.path.join(REPO,"codex-art","_anim_frame0.jpg"),quality=92)
print(f"rendered [{start},{min(end,N)}) ; total jpg now: {len([f for f in os.listdir(FR) if f.endswith('.jpg')])}")
