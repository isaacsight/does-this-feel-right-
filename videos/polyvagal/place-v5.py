import json, re, difflib
SEG=[(0,36,"You've felt this."),(38,117,"You've probably never had a name for it."),
(119,232,"Someone asked you a question in a meeting."),(234,331,"You know the answer, and nothing comes out."),
(335,423,"And you'll tell me that doesn't happen to you."),(430,500,"It happened on Tuesday."),
(504,680,"For about a 100 years, science had 2 explanations for stress."),(682,731,"Fight or run"),
(733,837,"You'll say you do neither, because you stay calm."),(841,905,"You didn't stay calm."),
(907,941,"You went still."),(943,1015,"You'll call that composure."),
(1017,1109,"You went gray and stopped blinking."),
(1118,1273,"Therapists watched people do this for decades and couldn't explain it."),
(1274,1485,"Then in 1994 a neuroscientist called Stephen Porges suggested something simple."),
(1485,1546,"There aren't 2 settings."),(1548,1584,"There are three."),(1588,1640,"Here's the first."),
(1642,1708,"You're with someone you trust."),(1710,1834,"You're relaxed, you're talking, your face moves easily."),
(1836,1888,"Everyone likes this one."),(1890,1931,"Here's the second."),(1933,1982,"Something goes wrong."),
(1987,2059,"Heart up, muscles tight."),(2061,2131,"Ready to argue or ready to leave."),
(2133,2201,"Everyone knows this one too."),(2203,2252,"And here's the third."),(2254,2308,"The one you don't want."),
(2309,2374,"You can't fight, you can't leave."),(2385,2475,"So your body does the only thing it has left."),
(2477,2518,"It shuts down."),(2520,2664,"Your heart slows, you go quiet, you go blank."),
(2666,2824,"Same person, same chair, 3 completely different settings."),
(2833,2929,"And here's why that landed in therapy rooms."),
(2932,3125,"If shutting down is a setting your body switches into, then going blank isn't weakness."),
(3127,3202,"It isn't you failing to cope."),(3206,3298,"It's the oldest survival move there is."),
(3310,3362,"Play dead."),(3364,3425,"And you're going to argue with that."),
(3434,3546,"From the floor, where you are currently lying."),(3550,3593,"Thinking."),
(3595,3656,"So who's doing the switching?"),(3661,3719,"You'll say you are."),
(3721,3865,"Think about walking into a room where 2 people have just stopped talking."),
(3875,3964,"You knew something was wrong before you could say what."),(3965,4014,"You didn't decide that."),
(4016,4122,"Something checked the room and made the call for you."),
(4124,4228,"Porges called it neuroception."),(4230,4277,"You're not doing it."),
(4279,4345,"It's being done to you."),(4352,4401,"Constantly."),(4403,4466,"Underneath everything."),
(4468,4518,"Most people hate that."),(4520,4615,"One more piece, and it's the one that matters most."),
(4617,4687,"Watch someone pick up a crying baby."),(4691,4763,"The baby stops."),
(4765,4844,"Not because of anything anyone said."),(4846,4900,"Because of a heartbeat."),
(4903,4955,"And a voice."),(4957,5015,"You never grow out of that."),
(5018,5114,"Someone walks into a room and it relaxes."),(5116,5188,"Someone else walks in and it doesn't."),
(5189,5283,"Porges called this co-regulation."),
(5290,5407,"You are not really built to calm yourself down on your own."),
(5416,5517,"You're built to be calmed down by other people."),
(5521,5609,"You'll want to tell me you're self-sufficient."),
(5611,5735,"You're patting your own head, which is worth sitting with."),
(5746,5818,"Because look at what we've changed."),
(5823,6016,"Every one of those signals is a face, a voice, or a person nearby."),
(6017,6071,"We text instead of calling."),(6073,6138,"We take the meeting with the camera off."),
(6140,6197,"We lie in bed scrolling."),(6201,6298,"Which looks like rest and settles nothing."),
(6300,6367,"You've been resting for 4 hours."),(6368,6422,"You feel worse."),
(6424,6509,"Now, one honest thing."),(6511,6628,"The biology behind all this is genuinely disputed."),
(6635,6874,"In 2023 a paper went through the theory's 5 main claims and challenged every one of them."),
(6881,6991,"And you would love that to mean you can ignore all of it."),
(6993,7087,"Porges answered, it isn't settled."),(7088,7132,"But here's the thing."),
(7133,7216,"Whether or not the anatomy turns out to be right."),(7220,7288,"The thing it named is real."),
(7290,7418,"People do go still, people do go blank."),
(7420,7529,"And what it tells you to do, find a face."),(7535,7650,"Hear a voice, breathe out slowly."),
(7655,7718,"Be near someone."),(7720,7812,"None of that depends on the biology being correct."),
(7816,7915,"You can doubt the theory and still take the advice."),
(7916,7990,"And maybe that's the useful part."),(7994,8071,"Not that it explains you."),
(8073,8215,"That it stops you being embarrassed about the part of you that goes quiet."),
]
REF={'v01':'565B0EFA','v02':'3A23C074','v03':'2AB6D935','v04':'9222C106','v05':'DAA39C6A','v06':'C06562F6',
'v07':'530B25BF','v08':'52A9D1D9','v09':'2F235665','v10':'C2F9CB55','v11':'CE9665AC','v12':'60A28BE6',
'v13':'047B42C5','v14':'080B1A5F','v15':'2FD309E6','v16':'B1E5E1F3','v17':'52B1D1B3','v18':'04603D36',
'v19':'C4F2C42C','v20':'1588D188','v21':'8A9EDFB6','v22':'A73111A9','v23':'46E730F3','v24':'EAEDB2C1',
'v25':'7368BF61','v26':'52D2D274','v27':'39D87511','v28':'956B4088','v29':'0B7D1432','v30':'C15A65E8',
'v31':'4B3B4560','v32':'4BB3392D','v33':'6957EBA5','v34':'89EB92BA','v35':'3C33277D','v36':'E530B2B4',
'v37':'C775582C','v38':'54FB89D0','v39':'82F54B30','v40':'F20944E4','v41':'46D97AFC','v42':'42F210CB',
'v43':'D8D59D86','v44':'63302970','v45':'D103491A','v46':'2FDFDE7B','v47':'18BBB175','v48':'38DD670F',
'v49':'8BCA39AE','v50':'375E4F14',
'w01':'201C8D4E','w02':'A7E95958','w03':'086B7D6D','w04':'B7621B5C','w05':'77FDB7E3',
'w06':'5AC81852','w07':'2A2BD817'}
END=8258
src=open('/Users/isaachernandez/blog design/videos/polyvagal/frames-v5.mjs').read()
lines={}
for m in re.finditer(r"id:\s*'([vw]\d+)',\s*kind:\s*'\w+',\s*line:\s*", src):
    gid=m.group(1); i=m.end(); q=src[i]; j=i+1; buf=[]
    while True:
        c=src[j]
        if c=='\\': buf.append(src[j+1]); j+=2; continue
        if c==q: break
        buf.append(c); j+=1
    lines[gid]=''.join(buf)          # later V5_FIX entries overwrite — correct
print(len(lines),"frames with lines")
norm=lambda s: re.sub(r"[^a-z0-9 ]","",s.lower())
segn=[norm(t) for _,_,t in SEG]
starts={}
for g,t0 in lines.items():           # match INDEPENDENTLY against all segments
    t=norm(t0); best,bi=0,0
    for i,sn in enumerate(segn):
        r=difflib.SequenceMatcher(None,t,sn).ratio()
        if t[:22] and t[:22] in sn: r=max(r,.93)
        if sn[:18] and sn[:18] in t: r=max(r,.9)
        if r>best: best,bi=r,i
    starts[g]=SEG[bi][0]
    if best<.5: print(f"  weak {g} {best:.2f}: {t0[:42]!r} -> {SEG[bi][2][:42]!r}")
seq=sorted(starts.items(), key=lambda x:x[1])
for i in range(1,len(seq)):
    if seq[i][1]<=seq[i-1][1]: seq[i]=(seq[i][0],seq[i-1][1]+30)
b=[s for _,s in seq]+[END]
MIN,MAX,DRIFT=54,240,45
lock=b[:]
for _ in range(400):
    ch=False; h=[b[i+1]-b[i] for i in range(len(b)-1)]
    for i,x in enumerate(h):
        if x<MIN and i+1<len(b)-1 and h[i+1]>MIN+(MIN-x) and abs(b[i+1]+(MIN-x)-lock[i+1])<=DRIFT:
            b[i+1]+=MIN-x; ch=True
        elif x<MIN and i>0 and h[i-1]>MIN+(MIN-x) and abs(b[i]-(MIN-x)-lock[i])<=DRIFT:
            b[i]-=MIN-x; ch=True
    h=[b[i+1]-b[i] for i in range(len(b)-1)]
    for i,x in enumerate(h):
        if x>MAX and i+1<len(b)-1 and abs(b[i+1]-(x-MAX)-lock[i+1])<=DRIFT:
            b[i+1]-=x-MAX; ch=True
        elif x>MAX and i>0 and abs(b[i]+(x-MAX)-lock[i])<=DRIFT:
            b[i]+=x-MAX; ch=True
    if not ch: break
h=[b[i+1]-b[i] for i in range(len(b)-1)]
print(f"{len(seq)} clips | avg {sum(h)/len(h)/30:.2f}s min {min(h)/30:.1f} max {max(h)/30:.1f}")
print("under 1.8s:",sum(1 for x in h if x<54)," over 8s:",sum(1 for x in h if x>240))
ents=[{"mediaRef":REF[seq[i][0]],"startFrame":b[i],"endFrame":b[i+1]} for i in range(len(seq))]
json.dump(ents,open('edl-v5.json','w'))
for i in range(0,len(ents),25):
    print(f"--{i}--"); print(json.dumps(ents[i:i+25],separators=(',',':')))
