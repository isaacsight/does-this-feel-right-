#!/usr/bin/env python3
"""Render board.json as a visual frame book you can actually read.

STORYBOARD.md is for the pipeline — map-shots.py parses it. This is for the human
gate before spending: 78 panels, act-grouped, each showing its camera, what the
object DOES, the narration line it sits under, and the picture. Colour-coded by
camera distance so a run of same-shot frames is visible at a glance, which is the
exact fault that survived 88 frames on the last film because nobody laid them out
side by side until after they were paid for.

Once frames exist, re-run with --frames to drop the real images into the panels.
"""
import json, sys, html, base64
from pathlib import Path

FILM = Path(__file__).resolve().parent
board = json.loads((FILM / 'production' / 'board.json').read_text())
USE_FRAMES = '--frames' in sys.argv
FRAMES = FILM / 'public' / 'images' / 'frames'

ACTS = [("THE CAUSES YOU WERE HANDED",1,11), ("THE CHEMICAL",12,32),
        ("THE GENE",33,44), ("THE SAMPLE",45,54),
        ("THE TURN",55,66), ("WHAT SURVIVED, AND THE CONFESSION",67,78)]

CAM = {'XCU':'#E8467F','CU':'#E8467F','MED':'#7B5CC4','WIDE':'#2E4EA8',
       'XWIDE':'#2E4EA8','OVER':'#1B8A7A','LOW':'#C4761B'}

def thumb(fid):
    p = FRAMES / f'{fid}-final.png'
    if not (USE_FRAMES and p.exists()):
        return ''
    import subprocess
    out = subprocess.run(['magick', str(p), '-resize', '420x236', 'png:-'],
                         capture_output=True).stdout
    return (f'<img src="data:image/png;base64,{base64.b64encode(out).decode()}" '
            f'alt="{fid}">')

P = []
w = P.append
w('<title>Who You Measured — frame book</title>')
w('''<style>
:root{--paper:#F2EDE2;--ink:#22212B;--pink:#E8467F;--blue:#2E4EA8;--line:#D9D2C4}
@media (prefers-color-scheme:dark){:root{--paper:#17161C;--ink:#EDE9DF;--line:#2E2C36}}
:root[data-theme=dark]{--paper:#17161C;--ink:#EDE9DF;--line:#2E2C36}
:root[data-theme=light]{--paper:#F2EDE2;--ink:#22212B;--line:#D9D2C4}
*{box-sizing:border-box}
body{margin:0;padding:28px 20px 60px;background:var(--paper);color:var(--ink);
 font:15px/1.5 ui-sans-serif,-apple-system,Segoe UI,Helvetica,sans-serif}
header{max-width:1180px;margin:0 auto 26px}
h1{font-size:26px;margin:0 0 6px;letter-spacing:-.01em}
.sub{opacity:.7;font-size:14px}
.key{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.key b{font-weight:600;font-size:11px;letter-spacing:.08em;padding:3px 9px;
 border-radius:99px;color:#fff}
h2{max-width:1180px;margin:34px auto 12px;font-size:13px;letter-spacing:.14em;
 text-transform:uppercase;opacity:.65;border-bottom:1px solid var(--line);
 padding-bottom:7px}
.grid{max-width:1180px;margin:0 auto;display:grid;gap:14px;
 grid-template-columns:repeat(auto-fill,minmax(268px,1fr))}
.card{border:1px solid var(--line);border-radius:9px;overflow:hidden;
 background:color-mix(in srgb,var(--paper) 88%,var(--ink))}
.bar{height:3px}
.top{display:flex;align-items:center;gap:8px;padding:9px 11px 0}
.id{font:600 12px ui-monospace,SFMono-Regular,Menlo,monospace;opacity:.75}
.cam{font-size:10px;font-weight:700;letter-spacing:.07em;color:#fff;
 padding:2px 7px;border-radius:99px}
.beh{font-size:11px;font-style:italic;opacity:.6;margin-left:auto}
.line{padding:8px 11px 0;font-size:13.5px;font-weight:600;line-height:1.35}
.scene{padding:7px 11px 12px;font-size:12px;opacity:.72;line-height:1.45}
img{display:block;width:100%;height:auto;margin-top:9px}
</style>''')
w('<header><h1>Who You Measured</h1>')
w(f'<div class="sub">{len(board)} frames &middot; one per sentence &middot; '
  'risograph, two inks, no cast &middot; stills only</div>')
w('<div class="key">')
for k in ['XCU','CU','MED','WIDE','XWIDE','OVER','LOW']:
    n = sum(1 for f in board if f['camera'] == k)
    w(f'<b style="background:{CAM[k]}">{k} {n}</b>')
w('</div></header>')

for title, lo, hi in ACTS:
    w(f'<h2>{html.escape(title)} &middot; {hi-lo+1} frames</h2><div class="grid">')
    for f in board[lo-1:hi]:
        c = CAM[f['camera']]
        w(f'<div class="card"><div class="bar" style="background:{c}"></div>'
          f'<div class="top"><span class="id">{f["id"]}</span>'
          f'<span class="cam" style="background:{c}">{f["camera"]}</span>'
          f'<span class="beh">{html.escape(f["behaviour"])}</span></div>'
          f'<div class="line">{html.escape(f["line"])}</div>'
          f'{thumb(f["id"])}'
          f'<div class="scene">{html.escape(f["scene"])}</div></div>')
    w('</div>')

out = FILM / 'production' / 'frame-book.html'
out.write_text('\n'.join(P))
print(f'{out}  ({len(board)} panels, frames={"on" if USE_FRAMES else "off"})')
