#!/usr/bin/env python3
import glob
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

CHANNEL_URL = "https://www.youtube.com/@theschooloflifetv/videos"
CHANNEL_NAME = "The School of Life"
BASE_DIR = Path("transcripts/the-school-of-life")
TRANSCRIPTS_DIR = BASE_DIR / "files"
VTT_DIR = BASE_DIR / "vtt"
CATALOG_PATH = BASE_DIR / "catalog.json"
INDEX_PATH = BASE_DIR / "INDEX.md"
YT_DLP_PATH = "/Users/isaachernandez/Library/Python/3.9/bin/yt-dlp"

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


def convert_vtt_to_markdown(vtt_file_path, video_id, title, url):
    if not os.path.exists(vtt_file_path):
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
            # Clean HTML/cue tags
            text = re.sub(r'<[^>]+>', '', line).replace('\n', ' ').strip()
            if text:
                total_words += len(text.split())
                minute_marker = int(current_start // 60) * 60
                if minute_marker not in blocks:
                    blocks[minute_marker] = []
                # Avoid duplicate adjacent lines
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

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(out_lines))

    return str(file_path.relative_to(BASE_DIR)), total_words


def run_yt_dlp_paced_download():
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    VTT_DIR.mkdir(parents=True, exist_ok=True)

    print("Executing yt-dlp subtitle download with request delays...")
    cmd = [
        YT_DLP_PATH,
        "--write-sub",
        "--write-auto-sub",
        "--sub-lang", "en",
        "--skip-download",
        "--sleep-requests", "3",
        "--sleep-interval", "5",
        "--max-sleep-interval", "10",
        "-o", str(VTT_DIR / "%(title)s_%(id)s.%(ext)s"),
        CHANNEL_URL
    ]

    subprocess.run(cmd)


def update_catalog_and_index():
    if not CATALOG_PATH.exists():
        return

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    # Match VTT files to catalog entries
    vtt_files = list(VTT_DIR.glob("*.vtt"))
    print(f"Processing {len(vtt_files)} downloaded VTT files...")

    converted_count = 0
    for vtt_path in vtt_files:
        name = vtt_path.name
        # Match video ID from filename (e.g. title_ID.en.vtt or title_ID.vtt)
        m = re.search(r'([a-zA-Z0-9_-]{11})\.(?:en\.)?vtt$', name)
        if m:
            v_id = m.group(1)
            if v_id in catalog and catalog[v_id].get("status") != "completed":
                entry = catalog[v_id]
                rel_path, word_count = convert_vtt_to_markdown(
                    vtt_path, v_id, entry["title"], entry["url"]
                )
                if rel_path:
                    catalog[v_id]["status"] = "completed"
                    catalog[v_id]["file"] = rel_path
                    catalog[v_id]["word_count"] = word_count
                    converted_count += 1

    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    total = len(catalog)
    completed = [v for v in catalog.values() if v.get("status") == "completed"]
    no_captions = [v for v in catalog.values() if v.get("status") == "no_captions"]
    pending = [v for v in catalog.values() if v.get("status") in ("pending", "failed")]
    total_words = sum(v.get("word_count", 0) for v in completed)

    index_lines = [
        f"# {CHANNEL_NAME} - Complete Transcript Archive",
        "",
        f"**Total Videos Discovered:** {total}  ",
        f"**Successfully Transcribed:** {len(completed)}  ",
        f"**No Captions Available:** {len(no_captions)}  ",
        f"**Remaining/Pending:** {len(pending)}  ",
        f"**Total Words Transcribed:** {total_words:,}",
        "",
        "## Index of Transcripts",
        "",
        "| # | Title | Duration | Transcript File | YouTube Link |",
        "|---|---|---|---|---|"
    ]

    sorted_entries = sorted(catalog.values(), key=lambda x: x.get("playlist_index", 999999))
    for idx, item in enumerate(sorted_entries, 1):
        v_title = item.get("title", "").replace("|", "\\|")
        v_url = item.get("url", "")
        v_file = item.get("file")
        v_status = item.get("status")

        if v_status == "completed" and v_file:
            file_link = f"[{v_file}]({v_file})"
        elif v_status == "no_captions":
            file_link = "*No Captions*"
        else:
            file_link = f"*{v_status}*"

        index_lines.append(f"| {idx} | {v_title} | - | {file_link} | [Watch]({v_url}) |")

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(index_lines))

    print(f"Updated catalog and generated {INDEX_PATH} with {len(completed)} completed entries.")


if __name__ == "__main__":
    run_yt_dlp_paced_download()
    update_catalog_and_index()
