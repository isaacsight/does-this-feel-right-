#!/usr/bin/env python3
import json
import os
import re
import random
import subprocess
import sys
import time
from pathlib import Path

# Enable TOR SOCKS5 proxy routing
os.environ['HTTP_PROXY'] = 'socks5h://127.0.0.1:9050'
os.environ['HTTPS_PROXY'] = 'socks5h://127.0.0.1:9050'

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "youtube-transcript-api"])
    from youtube_transcript_api import YouTubeTranscriptApi

CHANNEL_URL = "https://www.youtube.com/@theschooloflifetv/videos"
CHANNEL_NAME = "The School of Life"
BASE_DIR = Path("transcripts/the-school-of-life")
TRANSCRIPTS_DIR = BASE_DIR / "files"
CATALOG_PATH = BASE_DIR / "catalog.json"
INDEX_PATH = BASE_DIR / "INDEX.md"


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


def load_catalog():
    if CATALOG_PATH.exists():
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_catalog(catalog):
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)


def format_transcript_content(video_id, title, url, snippets):
    blocks = {}
    total_words = 0
    
    for snip in snippets:
        if isinstance(snip, dict):
            text = snip.get('text', '')
            start = snip.get('start', 0)
        else:
            text = getattr(snip, 'text', '')
            start = getattr(snip, 'start', 0)
            
        text = text.replace('\n', ' ').strip()
        if not text:
            continue
            
        total_words += len(text.split())
        minute_marker = int(start // 60) * 60
        if minute_marker not in blocks:
            blocks[minute_marker] = []
        blocks[minute_marker].append(text)
        
    lines = [
        f"# {title}",
        f"**Video ID:** {video_id} | **Link:** [Watch on YouTube]({url}) | **Channel:** {CHANNEL_NAME}",
        "",
        "---",
        ""
    ]
    
    for marker in sorted(blocks.keys()):
        timestamp_str = format_timestamp(marker)
        paragraph = " ".join(blocks[marker])
        lines.append(f"**[{timestamp_str}]** {paragraph}")
        lines.append("")
        
    return "\n".join(lines), total_words


def process_single_video(entry, ytt):
    v_id = entry["id"]
    title = entry["title"]
    url = entry["url"]
    
    slug = slugify(title)
    filename = f"{slug}_{v_id}.md"
    file_path = TRANSCRIPTS_DIR / filename
    
    # Check if already saved on disk
    if file_path.exists() and file_path.stat().st_size > 100:
        with open(file_path, "r", encoding="utf-8") as f:
            words = len(f.read().split())
        return v_id, "completed", str(file_path.relative_to(BASE_DIR)), words
        
    for attempt in range(1, 4):
        try:
            snippets = ytt.fetch(v_id)
            if not snippets:
                return v_id, "no_captions", None, 0
                
            content, word_count = format_transcript_content(v_id, title, url, snippets)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            return v_id, "completed", str(file_path.relative_to(BASE_DIR)), word_count
        except Exception as e:
            err_msg = str(e)
            if "NoTranscriptFound" in err_msg or "TranscriptsDisabled" in err_msg or "VideoUnavailable" in err_msg:
                return v_id, "no_captions", None, 0
            time.sleep(random.uniform(1.0, 2.0))
            
    return v_id, "pending", None, 0


def generate_index(catalog):
    total = len(catalog)
    completed = [v for v in catalog.values() if v.get("status") == "completed"]
    no_captions = [v for v in catalog.values() if v.get("status") == "no_captions"]
    pending = [v for v in catalog.values() if v.get("status") in ("pending", "failed")]
    total_words = sum(v.get("word_count", 0) for v in completed)
    
    lines = [
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
        dur = format_timestamp(item.get("duration", 0)) if item.get("duration") else "-"
        
        if v_status == "completed" and v_file:
            file_link = f"[{v_file}]({v_file})"
        elif v_status == "no_captions":
            file_link = "*No Captions*"
        else:
            file_link = f"*{v_status}*"
            
        lines.append(f"| {idx} | {v_title} | {dur} | {file_link} | [Watch]({v_url}) |")
        
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Generated {INDEX_PATH} with {len(sorted_entries)} records.")


def main():
    catalog = load_catalog()
    pending_items = [v for v in catalog.values() if v.get("status") in ("pending", "failed")]
    print(f"Starting TOR continuous loop for {len(pending_items)} pending items...")

    ytt = YouTubeTranscriptApi()
    processed_count = 0
    
    for item in pending_items:
        v_id = item["id"]
        vid, status, rel_file, word_count = process_single_video(item, ytt)
        
        catalog[vid]["status"] = status
        catalog[vid]["file"] = rel_file
        catalog[vid]["word_count"] = word_count
        processed_count += 1
        
        title_snip = catalog[vid]['title'][:40]
        print(f"[{processed_count}/{len(pending_items)}] {vid} ({status}): {title_snip}")
        
        if processed_count % 5 == 0:
            save_catalog(catalog)
            generate_index(catalog)
            
        time.sleep(random.uniform(0.5, 1.2))

    save_catalog(catalog)
    generate_index(catalog)
    print("\nAll pending transcripts processed via TOR!")


if __name__ == "__main__":
    main()
