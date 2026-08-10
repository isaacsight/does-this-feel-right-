from PIL import Image, ImageDraw, ImageFont
import glob, os
files = sorted(glob.glob("/Users/isaachernandez/blog design/videos/polyvagal/frames/v*.png"))
W, COLS = 400, 5
f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)
def build(chunk, out):
    th=[]
    for p in chunk:
        im=Image.open(p); h=int(W*im.height/im.width)
        t=im.resize((W,h),Image.LANCZOS); d=ImageDraw.Draw(t)
        d.rectangle([0,0,66,34],fill=(226,78,27)); d.text((6,4),os.path.basename(p)[:3],font=f,fill=(255,255,255))
        th.append(t)
    H=th[0].height; rows=(len(th)+COLS-1)//COLS
    s=Image.new("RGB",(W*COLS,H*rows),(20,20,20))
    for i,t in enumerate(th):
        r,c=divmod(i,COLS); s.paste(t,(c*W,r*H))
    s.save(out); print(out, s.size)
build(files[:25],"v5-A.png"); build(files[25:],"v5-B.png")
