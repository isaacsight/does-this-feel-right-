#!/usr/bin/env python3
"""Scrape the latest 10 transcripts from Modern Wisdom (Chris Williamson) YouTube channel.

Uses Tor SOCKS5 proxy (socks5h://127.0.0.1:9050) with yt-dlp to bypass YouTube IP rate limits.
Outputs:
  - Markdown transcripts: transcripts/modern-wisdom/files/<slug>_<video_id>.md
  - Catalog JSON: transcripts/modern-wisdom/catalog.json
  - Index Markdown: transcripts/modern-wisdom/INDEX.md
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

CHANNEL_URL = "https://www.youtube.com/@ChrisWillx/videos"
CHANNEL_NAME = "Modern Wisdom (Chris Williamson)"
BASE_DIR = Path("transcripts/modern-wisdom")
TRANSCRIPTS_DIR = BASE_DIR / "files"
VTT_DIR = BASE_DIR / "vtt"
CATALOG_PATH = BASE_DIR / "catalog.json"
INDEX_PATH = BASE_DIR / "INDEX.md"
YT_DLP_PATH = "/opt/homebrew/bin/yt-dlp"

if not os.path.exists(YT_DLP_PATH):
    YT_DLP_PATH = "yt-dlp"


def slugify(title):
    s = title.lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s).strip('-')
    return s[:80] if s else "video"


def format_timestamp(seconds):
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def parse_vtt_timestamp(ts_str):
    parts = ts_str.strip().split(':')
    if len(parts) == 3:
        h, m, s = parts
        return float(h) * 3600 + float(m) * 60 + float(s)
    elif len(parts) == 2:
        m, s = parts
        return float(m) * 60 + float(s)
    return 0.0


def fetch_latest_videos(count=10):
    print(f"Fetching latest {count} videos from {CHANNEL_URL}...")
    cmd = [
        YT_DLP_PATH,
        "--playlist-items", f"1-{count}",
        "--flat-playlist",
        "-j",
        CHANNEL_URL
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    videos = []
    for line in proc.stdout:
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            v_id = data.get("id")
            title = data.get("title")
            url = f"https://www.youtube.com/watch?v={v_id}"
            if v_id and title:
                videos.append({
                    "id": v_id,
                    "title": title,
                    "url": url,
                    "duration": data.get("duration"),
                    "playlist_index": len(videos) + 1
                })
        except json.JSONDecodeError:
            continue
    proc.wait()
    print(f"Discovered {len(videos)} videos.")
    return videos


def download_subtitles_via_tor(v_id):
    VTT_DIR.mkdir(parents=True, exist_ok=True)
    out_pattern = str(VTT_DIR / f"{v_id}.%(ext)s")
    url = f"https://www.youtube.com/watch?v={v_id}"
    cmd = [
        YT_DLP_PATH,
        "--proxy", "socks5h://127.0.0.1:9050",
        "--extractor-args", "youtube:player_client=android",
        "--write-auto-sub", "--write-sub", "--sub-lang", "en",
        "--skip-download",
        "-o", out_pattern,
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    # Check for downloaded vtt file
    matches = list(VTT_DIR.glob(f"{v_id}*.vtt"))
    if matches:
        return matches[0]
    return None


def convert_vtt_to_markdown(vtt_file_path, video_id, title, url):
    if not vtt_file_path or not os.path.exists(vtt_file_path):
        return None, 0

    blocks = {}
    total_words = 0

    with open(vtt_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    current_start = 0.0
    for line in lines:
        line = line.strip()
        if '-->' in line:
            start_str = line.split('-->')[0].strip()
            current_start = parse_vtt_timestamp(start_str)
        elif line and not line.startswith('WEBVTT') and not line.startswith('Kind:') and not line.startswith('Language:') and not line.isdigit():
            text = re.sub(r'<[^>]+>', '', line).replace('\n', ' ').strip()
            if text:
                minute_marker = int(current_start // 60) * 60
                if minute_marker not in blocks:
                    blocks[minute_marker] = []
                if not blocks[minute_marker] or blocks[minute_marker][-1] != text:
                    blocks[minute_marker].append(text)

    if not blocks:
        return None, 0

    out_lines = [
        f"# {title}",
        f"**Video ID:** {video_id} | **Link:** [Watch on YouTube]({url}) | **Channel:** {CHANNEL_NAME}",
        "",
        "---",
        ""
    ]

    for marker in sorted(blocks.keys()):
        timestamp_str = format_timestamp(marker)
        paragraph = " ".join(blocks[marker])
        out_lines.append(f"**[{timestamp_str}]** {paragraph}")
        out_lines.append("")

    slug = slugify(title)
    filename = f"{slug}_{video_id}.md"
    file_path = TRANSCRIPTS_DIR / filename
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))

    return str(file_path.relative_to(BASE_DIR)), total_words


def generate_index_and_catalog(catalog):
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    lines = [
        "# Modern Wisdom (Chris Williamson) — Transcripts Index",
        "",
        f"Collection of the latest **{len(catalog)}** transcripts from [Modern Wisdom](https://www.youtube.com/@ChrisWillx).",
        "",
        "| # | Title | Video ID | Words | Local File | YouTube Link |",
        "|---|---|---|---|---|---|"
    ]

    for idx, (v_id, item) in enumerate(sorted(catalog.items(), key=lambda x: x[1].get("playlist_index", 0)), 1):
        title = item["title"]
        rel_path = item.get("relative_file_path", "")
        words = item.get("word_count", 0)
        file_link = f"[`{rel_path.split('/')[-1]}`]({rel_path})" if rel_path else "N/A"
        yt_link = f"[Watch]({item['url']})"
        lines.append(f"| {idx:02d} | {title} | `{v_id}` | {words:,} | {file_link} | {yt_link} |")

    lines.append("")
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    VTT_DIR.mkdir(parents=True, exist_ok=True)

    videos = fetch_latest_videos(10)
    catalog = {}

    for idx, v in enumerate(videos, 1):
        v_id = v["id"]
        title = v["title"]
        url = v["url"]
        print(f"\n[{idx}/10] Processing: {title} ({v_id})")

        vtt_path = download_subtitles_via_tor(v_id)
        if vtt_path:
            rel_file, word_count = convert_vtt_to_markdown(vtt_path, v_id, title, url)
            catalog[v_id] = {
                "id": v_id,
                "title": title,
                "url": url,
                "duration": v.get("duration"),
                "playlist_index": idx,
                "relative_file_path": rel_file,
                "word_count": word_count,
                "status": "completed"
            }
            print(f"  -> Saved transcript ({word_count:,} words) to {rel_file}")
        else:
            catalog[v_id] = {
                "id": v_id,
                "title": title,
                "url": url,
                "duration": v.get("duration"),
                "playlist_index": idx,
                "status": "failed"
            }
            print(f"  -> Failed to download subtitles for {v_id}")

        time.sleep(1)

    generate_index_and_catalog(catalog)
    print("\nAll done! Catalog and INDEX.md generated.")


if __name__ == "__main__":
    main()
