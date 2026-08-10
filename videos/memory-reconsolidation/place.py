import json,re,difflib
FPS=30
W=json.load(open('/tmp/nar.json'))['transcription']
SEG=[(int(s['offsets']['from']*FPS/1000),int(s['offsets']['to']*FPS/1000),s['text'].strip()) for s in W]
json.dump({'fps':FPS,'segments':[[a,b,t] for a,b,t in SEG]},open('segments.json','w'),indent=1)

# frame -> narration line, from SHOT-LIST.md
rows=re.findall(r'^\|\s*\*{0,2}(m\d+b?)\*{0,2}\s*\|[^|]*\|[^|]*\|[^|]*\|\s*(.+?)\s*\|$',
                open('SHOT-LIST.md').read(),re.M)
lines={f:re.sub(r'[*"`]|—.*$|\(.*?\)','',t).strip() for f,t in rows}
order=[f for f,_ in rows]
norm=lambda s:re.sub(r'[^a-z0-9 ]','',s.lower())
segn=[norm(t) for _,_,t in SEG]

# Match EVERY frame independently against ALL segments, then sort by time.
# A monotonic cursor breaks the moment ids stop sorting in narration order.
start={}
for f in order:
    t=norm(lines.get(f,''))
    if not t: continue
    best,bi=0,0
    for i,sn in enumerate(segn):
        r=difflib.SequenceMatcher(None,t,sn).ratio()
        if t[:22] and t[:22] in sn: r=max(r,.93)
        if sn[:18] and sn[:18] in t: r=max(r,.90)
        if r>best: best,bi=r,i
    start[f]=(SEG[bi][0],best)

seq=sorted(start.items(),key=lambda kv:kv[1][0])
END=SEG[-1][1]
MIN,MAX=int(1.8*FPS),int(8.0*FPS)
edl=[]
for i,(f,(s,score)) in enumerate(seq):
    nxt=seq[i+1][1][0] if i+1<len(seq) else END
    hold=max(MIN,min(MAX,nxt-s))
    edl.append({'id':f,'start':s,'end':s+hold,'match':round(score,2)})
# Insert the two frames that carry no narration line of their own, beside the
# line they are held under: m03 under m02's line, m61 as the final held beat.
ins={'m03':'m02','m61':None}
for f,after in ins.items():
    if f in start: continue
    if after and any(e['id']==after for e in edl):
        j=[k for k,e in enumerate(edl) if e['id']==after][0]
        edl.insert(j+1,{'id':f,'start':edl[j]['start'],'end':edl[j]['start'],'match':None})
    else:
        edl.append({'id':f,'start':END,'end':END,'match':None})

# Local, non-cascading fix. A global cascade compressed the whole film forward
# and left 80s of dead air at the tail. Instead: where the gap to the next clip
# exceeds the ceiling, pull ONLY that next clip earlier, never the ones after it.
DRIFT=int(3.0*FPS)
edl.sort(key=lambda e:e['start'])
for i in range(len(edl)-1):
    gap=edl[i+1]['start']-edl[i]['start']
    if gap>MAX:
        edl[i+1]['start']=max(edl[i]['start']+MIN, edl[i+1]['start']-min(gap-MAX,DRIFT))
edl.sort(key=lambda e:e['start'])

for i in range(len(edl)-1):
    edl[i]['end']=max(edl[i]['start']+MIN, edl[i+1]['start'])
edl[-1]['end']=END
over=[e for e in edl if (e['end']-e['start'])/FPS>8.0]
weak=[e for e in edl if e['match'] is not None and e['match']<0.45]
json.dump(edl,open('edl.json','w'),indent=1)
print(f"{len(edl)} clips · {END/FPS:.1f}s · over-8s: {len(over)} · weak matches: {len(weak)}")
if over: print('  over:',[f"{e['id']} {(e['end']-e['start'])/FPS:.1f}s" for e in over][:6])
if weak: print('  weak:',[e['id'] for e in weak][:8])
missing=[f for f in order if f not in start]
print('unmatched frames:',missing or 'none')
