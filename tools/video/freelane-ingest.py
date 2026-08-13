#!/usr/bin/env python3
"""Free-lane ingest: claim the newest AI Studio download as a frame.

The free AI Studio lane (decided 2026-08-11) hand-drives one frame per run;
downloads land in ~/Downloads as "Generated Image <date>.jpg". This tool
closes the loop the fal pipeline had for free:

    python3 tools/video/freelane-ingest.py <film-dir> <frame-id>

  - finds the newest Generated Image* file in ~/Downloads (refuses files
    older than 10 minutes — stale downloads are how wrong frames get
    filed under right ids)
  - converts JPEG -> PNG at videos/<film>/public/images/frames/<id>-final.png
  - runs frame-gate.py on it with the film's WORLD.md assertions
  - on gate failure moves it to production/quarantine/<id>-try<N>.png and
    exits 1 (re-roll in the browser, run this again)
  - appends to production/spend.log with price 0.000 so the ledger stays
    the record of record

The gate exit code is THE result; never truncate its output (law 11).
"""
import subprocess, sys, time
from pathlib import Path

if len(sys.argv) < 3:
    sys.exit(__doc__)

FILM = Path(sys.argv[1]).resolve()
FID = sys.argv[2]
REPO = Path(__file__).resolve().parent.parent.parent
DL = Path.home() / 'Downloads'

cands = sorted(DL.glob('Generated Image*'), key=lambda p: p.stat().st_mtime, reverse=True)
if not cands:
    sys.exit('no Generated Image* files in ~/Downloads')
src = cands[0]
age = time.time() - src.stat().st_mtime
if age > 600:
    sys.exit(f'newest download is {age/60:.0f} min old — refusing (stale-download guard). '
             'Download the frame first, then ingest.')

out_dir = FILM / 'public' / 'images' / 'frames'
out_dir.mkdir(parents=True, exist_ok=True)
dest = out_dir / f'{FID}-final.png'
subprocess.run(['magick', str(src), str(dest)], check=True)

gate = subprocess.run(
    ['/usr/bin/python3', str(REPO / 'tools/video/frame-gate.py'), str(FILM),
     '--frame', FID],
    capture_output=True, text=True)
print(gate.stdout)
print(gate.stderr, file=sys.stderr)

ledger = FILM / 'production' / 'spend.log'
ledger.parent.mkdir(parents=True, exist_ok=True)

if gate.returncode != 0:
    q = FILM / 'production' / 'quarantine'
    q.mkdir(parents=True, exist_ok=True)
    n = 1
    while (q / f'{FID}-try{n}.png').exists():
        n += 1
    dest.rename(q / f'{FID}-try{n}.png')
    print(f'GATED — moved to quarantine/{FID}-try{n}.png; re-roll and ingest again')
    sys.exit(1)

with open(ledger, 'a') as f:
    f.write(f'{time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())} {FID} aistudio-free-lane 0.000\n')
src.unlink()
print(f'{FID}-final.png ingested, gate green, download consumed, $0.000')
