#!/usr/bin/env python3
"""Early warning for a distribution collapse. Snapshot, then compare.

WHY THIS EXISTS. Google's S-CTS paper (Scalable Detection of Adversarial
Synthetic Slop and Coordinated Media Abuse, 2026) describes automated
classification applied to synthetic content at platform scale. Its termination
path needs the INTERSECTION of coordinated-account signals and synthetic content,
so a single channel is structurally outside it. But the reported failure mode for
legitimate channels is not termination — it is silent suppression: Kurzgesagt
reported click-through UP, watch time UP, and views at their worst since 2013.

That shape is invisible if you only watch views, because a view drop looks like a
bad week. It is only diagnostic as a RATIO: if the people who reach the video like
it just as much as ever, and there are simply far fewer of them, the problem is
distribution, not the work. If engagement falls with reach, the work is the
problem. Those two need completely different responses, and guessing wrong is
expensive either way.

WHAT IT MEASURES. Ideally impressions and CTR from the YouTube Analytics API.
That needs the yt-analytics.readonly scope, which this token does not carry — the
uploader only ever asked for upload/youtube/force-ssl. Until that re-consent, this
uses the Data API's public statistics as a proxy:

    view velocity   views gained per day, per video, between snapshots
    like rate       likes / views, the engagement proxy that stands in for CTR

A collapse in velocity while like rate HOLDS is the Kurzgesagt signature. Both
falling together is an editorial problem, not a platform one.

LIMITS, STATED. This is a proxy and it cannot see impressions, so it cannot prove
suppression — it can only tell you the shape is worth investigating. It also needs
at least two snapshots: the first run establishes a baseline and reports nothing.
Run it daily.

Usage:
    reach-monitor.py snapshot        record today's numbers
    reach-monitor.py check           compare and report (exit 1 if alerting)
    reach-monitor.py check --json
"""
import json
import pathlib
import statistics
import sys
from datetime import datetime, timezone

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN = pathlib.Path.home() / ".config" / "kernel" / "youtube-token.json"
LEDGER = pathlib.Path("output/publish/reach.jsonl")

# A view drop this steep, with engagement intact, is the shape worth a look. Set
# from the Kurzgesagt account: views to their worst in a decade while CTR rose.
VELOCITY_DROP = 0.55        # flag when velocity falls below 45% of baseline
LIKE_RATE_TOLERANCE = 0.80  # ...and like rate is still >= 80% of its baseline
MIN_BASELINE_VIEWS = 50     # ignore videos too new or too small to read


def service():
    creds = Credentials.from_authorized_user_file(str(TOKEN))
    return build("youtube", "v3", credentials=creds)


def snapshot(yt):
    """Every video on the channel with its current counts."""
    ch = yt.channels().list(part="contentDetails,snippet", mine=True).execute()["items"][0]
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]

    ids, page = [], None
    while True:
        r = yt.playlistItems().list(part="contentDetails", playlistId=uploads,
                                    maxResults=50, pageToken=page).execute()
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]
        page = r.get("nextPageToken")
        if not page:
            break

    vids = {}
    for i in range(0, len(ids), 50):
        r = yt.videos().list(part="statistics,snippet,contentDetails",
                             id=",".join(ids[i:i + 50])).execute()
        for it in r["items"]:
            st = it["statistics"]
            vids[it["id"]] = {
                "title": it["snippet"]["title"][:70],
                "published": it["snippet"]["publishedAt"],
                "views": int(st.get("viewCount", 0)),
                "likes": int(st.get("likeCount", 0)),
                "comments": int(st.get("commentCount", 0)),
            }
    return {"at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "channel": ch["snippet"]["title"], "videos": vids}


def load():
    if not LEDGER.exists():
        return []
    return [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()]


def hours_between(a, b):
    fmt = "%Y-%m-%dT%H:%M:%S%z"
    return max(0.01, (datetime.strptime(b, fmt) - datetime.strptime(a, fmt)).total_seconds() / 3600)


def check(as_json=False):
    snaps = load()
    if len(snaps) < 3:
        print(f"{len(snaps)} snapshot(s) on file. Need 3 to read a trend "
              f"(one baseline pair, one current pair). Run `snapshot` daily.")
        return 0

    cur, prev = snaps[-1], snaps[-2]
    span = hours_between(prev["at"], cur["at"])

    # Baseline velocity from every earlier consecutive pair, so one quiet day does
    # not read as a collapse.
    base_v, base_l = {}, {}
    for a, b in zip(snaps[:-2], snaps[1:-1]):
        h = hours_between(a["at"], b["at"])
        for vid, now in b["videos"].items():
            was = a["videos"].get(vid)
            if not was:
                continue
            base_v.setdefault(vid, []).append((now["views"] - was["views"]) / h * 24)
            if now["views"] >= MIN_BASELINE_VIEWS:
                base_l.setdefault(vid, []).append(now["likes"] / max(1, now["views"]))

    alerts, watched = [], 0
    for vid, now in cur["videos"].items():
        was = prev["videos"].get(vid)
        if not was or vid not in base_v or now["views"] < MIN_BASELINE_VIEWS:
            continue
        bv = statistics.median(base_v[vid])
        if bv < 1:                      # already flat; nothing to fall from
            continue
        watched += 1
        vel = (now["views"] - was["views"]) / span * 24
        rate = now["likes"] / max(1, now["views"])
        brate = statistics.median(base_l.get(vid, [rate]))
        if vel < bv * VELOCITY_DROP:
            engaged = brate > 0 and rate >= brate * LIKE_RATE_TOLERANCE
            alerts.append({
                "id": vid, "title": now["title"],
                "velocity_now": round(vel, 1), "velocity_base": round(bv, 1),
                "drop": round(1 - vel / bv, 2),
                "like_rate_now": round(rate, 4), "like_rate_base": round(brate, 4),
                # THE distinction this tool exists to draw.
                "verdict": "DISTRIBUTION — reach fell, the people who arrive still like it"
                           if engaged else
                           "CONTENT — reach and engagement fell together",
            })

    if as_json:
        print(json.dumps({"watched": watched, "alerts": alerts}, indent=1))
    else:
        print(f"{cur['channel']} — {len(cur['videos'])} videos, {watched} with enough "
              f"history to read, {span:.1f}h since last snapshot\n")
        if not alerts:
            print("  no collapse detected")
        for a in sorted(alerts, key=lambda x: -x["drop"]):
            print(f"  {a['drop']:.0%} drop  {a['title']}")
            print(f"     {a['velocity_base']:.0f} -> {a['velocity_now']:.0f} views/day  "
                  f"| like rate {a['like_rate_base']:.3f} -> {a['like_rate_now']:.3f}")
            print(f"     {a['verdict']}")
        if any(a["verdict"].startswith("DISTRIBUTION") for a in alerts):
            print("\n  A distribution verdict is NOT proof of suppression — this proxy")
            print("  cannot see impressions. It means the shape is worth investigating,")
            print("  and that yt-analytics.readonly would settle it.")
    return 1 if alerts else 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "snapshot":
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        s = snapshot(service())
        with LEDGER.open("a") as f:
            f.write(json.dumps(s) + "\n")
        print(f"snapshot {s['at']} — {len(s['videos'])} videos, "
              f"{sum(v['views'] for v in s['videos'].values()):,} total views")
    elif cmd == "check":
        sys.exit(check("--json" in sys.argv))
    else:
        print(__doc__)
        sys.exit(1)
