"""
Rebuilds the four Smart Plus brand logos as transparent PNGs in ../assets/.

  cd smart-plus-group/src/logo-source && python3 make_logos.py

The white "Smart Plus" wordmark is lifted from the existing Smart Plus Electrical
accreditation artwork (smart-plus-electrical-accreditation.webp); the coloured
descriptor words are set in Montserrat Bold (fonts/Montserrat-Bold.ttf, OFL).
Requires Pillow (pip install pillow).
"""
from PIL import Image, ImageDraw, ImageFont
import os
HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "..", "assets")
PREVIEW = os.path.join(HERE, "preview")
SOURCE = os.path.join(HERE, "smart-plus-electrical-accreditation.webp")
os.makedirs(PREVIEW, exist_ok=True)
RED="#E5232A"; BLUE="#1E9BE8"; YELLOW="#F7C719"; WHITE="#FFFFFF"

# ---- 1. extract the "Smart Plus" wordmark from the accreditation logo (653x591) ----
src=Image.open(SOURCE).convert("RGBA")
W,H=src.size; px=src.load()
def is_dark(p): return p[3]>40 and p[0]<90 and p[1]<90 and p[2]<90
rows=[y for y in range(H) if any(is_dark(px[x,y]) for x in range(0,W,2))]
bands=[]; s=rows[0]; prev=rows[0]
for y in rows[1:]:
    if y!=prev+1: bands.append((s,prev)); s=y
    prev=y
bands.append((s,prev)); print("dark bands",bands)
# wordmark = first band that is wide (spans >50% of width)
def band_width(b):
    xs=[x for y in range(b[0],b[1]+1,3) for x in range(W) if is_dark(px[x,y])]
    return (min(xs),max(xs)) if xs else (0,0)
for b in bands:
    x0,x1=band_width(b)
    print(" band",b,"x",x0,x1)
    if x1-x0>W*0.5: wb=b; wx=(x0,x1); break
y0,y1=wb; x0,x1=wx
crop=src.crop((x0,y0,x1+1,y1+1))
# build alpha from original alpha * darkness (so any faint colour fringe is dropped)
mask=Image.new("L",crop.size,0); cp=crop.load(); mp=mask.load()
for y in range(crop.height):
    for x in range(crop.width):
        r,g,b,a=cp[x,y]
        lum=(r+g+b)/3
        dark=max(0.0,min(1.0,(160-lum)/120))   # 1 when lum<=40, 0 when lum>=160
        mp[x,y]=int(a*dark)
wordmark=Image.new("RGBA",crop.size,(255,255,255,0)); wordmark.putalpha(mask)
wordmark.save(os.path.join(PREVIEW,"wordmark-white.png")); print("wordmark",wordmark.size)

# ---- 2. helpers ----
def load_font(name,size): return ImageFont.truetype(os.path.join(F,name),size)
def text_width(font,text,tracking):
    w=0
    for i,ch in enumerate(text):
        w+=font.getlength(ch)
        if i<len(text)-1: w+=tracking
    return w
def draw_tracked(draw,xy,text,font,fill,tracking):
    x,y=xy
    for ch in text:
        draw.text((x,y),ch,font=font,fill=fill); x+=font.getlength(ch)+tracking
def fit_wordmark(width):
    r=width/wordmark.width
    return wordmark.resize((int(wordmark.width*r),int(wordmark.height*r)),Image.LANCZOS)

# ---- 3. sub-brand logos: canvas 900x200 (same 4.5:1 aspect as the supplied files) ----
def sub_logo(word,colour,fname):
    CW,CH=900,200
    im=Image.new("RGBA",(CW,CH),(0,0,0,0))
    wm=fit_wordmark(580)
    im.alpha_composite(wm,((CW-wm.width)//2,14))
    d=ImageDraw.Draw(im)
    font=load_font("Montserrat-Bold.ttf",44); tracking=44*0.32
    tw=text_width(font,word,tracking)
    # font.getbbox for caps top offset
    bbox=font.getbbox("H"); capTop=bbox[1]
    ty=14+wm.height+18-capTop
    draw_tracked(d,((CW-tw)/2,ty),word,font,colour,tracking)
    im.save(os.path.join(OUT,fname)); print(fname,im.size,"wm",wm.size)
sub_logo("HEATING",RED,"logo-heating.png")
sub_logo("ELECTRIC",YELLOW,"logo-electric.png")
sub_logo("AIRCON",BLUE,"logo-aircon.png")

# ---- 4. group logo: wordmark + HEATING / AIR CONDITIONING / ELECTRICS row ----
def group_logo(fname):
    font=load_font("Montserrat-Bold.ttf",40); tracking=40*0.28; gap=64
    words=[("HEATING",RED),("AIR CONDITIONING",BLUE),("ELECTRICS",YELLOW)]
    widths=[text_width(font,w,tracking) for w,_ in words]
    row_w=sum(widths)+gap*(len(words)-1)
    wm=fit_wordmark(700)
    CW=int(row_w+120); CH=14+wm.height+22+52+14
    im=Image.new("RGBA",(CW,CH),(0,0,0,0))
    im.alpha_composite(wm,((CW-wm.width)//2,14))
    d=ImageDraw.Draw(im)
    capTop=font.getbbox("H")[1]
    ty=14+wm.height+22-capTop
    x=(CW-row_w)/2
    for (w,c),ww in zip(words,widths):
        draw_tracked(d,(x,ty),w,font,c,tracking); x+=ww+gap
    im.save(os.path.join(OUT,fname)); print(fname,im.size)
group_logo("logo-group.png")

# ---- 5. preview sheet on dark header colour ----
files=["logo-group.png","logo-heating.png","logo-electric.png","logo-aircon.png"]
ims=[Image.open(os.path.join(OUT,f)).convert("RGBA") for f in files]
# show each at header display scale (64px tall -> x3 for legibility = 192px) and full size
sheet_w=max(i.width for i in ims)+80; sheet_h=sum(i.height+40 for i in ims)+40
sheet=Image.new("RGBA",(sheet_w,sheet_h),(17,17,17,255)); y=20
for i in ims:
    sheet.alpha_composite(i,(40,y)); y+=i.height+40
sheet.convert("RGB").save(os.path.join(PREVIEW,"preview-sheet.png")); print("sheet",sheet.size)
# header-scale preview: each logo at 64px tall, 2x for retina
hs=Image.new("RGBA",(1400,4*160+40),(17,17,17,255)); y=20
for i in ims:
    h=128; r=h/i.height; s=i.resize((int(i.width*r),h),Image.LANCZOS)
    hs.alpha_composite(s,(40,y)); y+=160
hs.convert("RGB").save(os.path.join(PREVIEW,"preview-header-scale.png")); print("header-scale preview done")
