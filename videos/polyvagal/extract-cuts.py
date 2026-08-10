import json,re,subprocess,os
exec(open('place-v5.py').read().split("src=open")[0])
INV={v:k for k,v in REF.items()}
src=open('/Users/isaachernandez/blog design/videos/polyvagal/frames-v5.mjs').read()
lines={}
for m in re.finditer(r"id:\s*'([vw]\d+)',\s*kind:\s*'\w+',\s*line:\s*", src):
    g=m.group(1); i=m.end(); q=src[i]; j=i+1; b=[]
    while True:
        c=src[j]
        if c=='\\': b.append(src[j+1]); j+=2; continue
        if c==q: break
        b.append(c); j+=1
    lines[g]=''.join(b)
ents=json.load(open('edl-v5.json'))
V="/Users/isaachernandez/blog design/output/publish/the-third-thing.mp4"
os.makedirs("w5",exist_ok=True); rows=[]
for n,e in enumerate(ents):
    g=INV[e['mediaRef']]; s,t=e['startFrame'],e['endFrame']
    o=f"w5/{n:02d}.png"
    if not os.path.exists(o):
        subprocess.run(["ffmpeg","-y","-v","error","-ss",str(((s+t)//2)/30),"-i",V,"-vframes","1",o],check=True)
    rows.append((n,g,round(s/30,1),round((t-s)/30,1),lines.get(g,'?')))
json.dump(rows,open("w5/rows.json","w")); print(len(rows))
