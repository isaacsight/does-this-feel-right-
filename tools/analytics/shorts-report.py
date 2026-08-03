#!/usr/bin/env python3
"""Weekly read: which shorts earn views, so the next cuts are chosen by
evidence instead of editorial taste.

    .venv-youtube/bin/python tools/analytics/shorts-report.py

Why this exists: the channel's numbers say the shorts ARE the audience -- one
short at 603 views while its parent film sat at 2 -- and nothing was feeding
that back into which passages get cut next. This pulls YouTube Data API
statistics for every video the manifests know about, ranks them, and writes a
dated report the next cutting session reads first.

Data API only (views/likes/comments) -- retention curves live in the Analytics
API, which needs a scope our OAuth token does not carry. Views per short is
enough to rank passages; add the scope later if retention starts mattering.

Reuses youtube-upload.py's authenticate() so there is exactly one token flow.
"""
import json
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))
import importlib.util
spec = importlib.util.spec_from_file_location("ytu", REPO / "tools" / "youtube-upload.py")
ytu = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ytu)

OUT = REPO / "output" / "analytics"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    rows = []
    for mf in sorted((REPO / "output" / "publish").glob("manifest-*.json")):
        m = json.load(open(mf))
        film = m.get("film") if isinstance(m.get("film"), str) else m.get("film", {}).get("title", mf.stem)
        for s in m.get("shorts", []):
            vid = (s.get("status", {}).get("youtube", {}) or {}).get("id") or s.get("youtube_id")
            if vid:
                rows.append({"film": film, "slug": s["slug"], "id": vid})

    youtube = ytu.authenticate()
    stats = {}
    ids = [r["id"] for r in rows]
    for i in range(0, len(ids), 50):
        resp = youtube.videos().list(part="statistics", id=",".join(ids[i:i+50])).execute()
        for item in resp.get("items", []):
            st = item["statistics"]
            stats[item["id"]] = {k: int(st.get(k, 0)) for k in ("viewCount", "likeCount", "commentCount")}

    for r in rows:
        r.update(stats.get(r["id"], {"viewCount": 0, "likeCount": 0, "commentCount": 0}))
    rows.sort(key=lambda r: -r["viewCount"])

    today = date.today().isoformat()
    lines = [f"# Shorts performance — {today}", "",
             "| # | short | film | views | likes | comments |",
             "|---|---|---|---|---|---|"]
    for i, r in enumerate(rows, 1):
        lines.append(f"| {i} | [{r['slug']}](https://youtu.be/{r['id']}) | {r['film']} "
                     f"| {r['viewCount']} | {r['likeCount']} | {r['commentCount']} |")
    total = sum(r["viewCount"] for r in rows)
    lines += ["", f"Total short views: {total} across {len(rows)} shorts.", "",
              "Read before cutting the next batch: the top rows say which registers",
              "and passages travel; cut toward them, not toward what reads well on paper."]

    path = OUT / f"shorts-report-{today}.md"
    path.write_text("\n".join(lines) + "\n")
    print(f"{len(rows)} shorts -> {path}")
    for r in rows[:5]:
        print(f"  {r['viewCount']:>6}  {r['slug']}  ({r['film']})")


if __name__ == "__main__":
    main()
