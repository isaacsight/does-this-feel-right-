#!/usr/bin/env python3
import json
import os
import re
import random
import sys
import time
from pathlib import Path

# TOR SOCKS5 Proxy Routing
os.environ['HTTP_PROXY'] = 'socks5h://127.0.0.1:9050'
os.environ['HTTPS_PROXY'] = 'socks5h://127.0.0.1:9050'

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "youtube-transcript-api"])
    from youtube_transcript_api import YouTubeTranscriptApi

BASE_DIR = Path("transcripts/the-school-of-life")
TRANSCRIPTS_DIR = BASE_DIR / "files"
CATALOG_PATH = BASE_DIR / "catalog.json"
INDEX_PATH = BASE_DIR / "INDEX.md"
CHANNEL_NAME = "The School of Life"


def rotate_tor_circuit():
    print("Rotating TOR exit node IP...")
    try:
        import subprocess
        subprocess.run(["brew", "services", "restart", "tor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
    except Exception as e:
        print(f"Tor rotation warning: {e}")


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


def main():
    catalog = load_catalog()
    ytt = YouTubeTranscriptApi()
    
    pending_ids = [v_id for v_id, v in catalog.items() if v.get("status") in ("pending", "failed")]
    print(f"TOR Auto-Rotating Engine started. {len(pending_ids)} videos queued.")
    
    completed_in_run = 0
    blocked_streak = 0
    
    for v_id in pending_ids:
        item = catalog[v_id]
        title = item["title"]
        url = item["url"]
        slug = slugify(title)
        filename = f"{slug}_{v_id}.md"
        file_path = TRANSCRIPTS_DIR / filename
        
        if file_path.exists() and file_path.stat().st_size > 100:
            with open(file_path, "r", encoding="utf-8") as f:
                w_count = len(f.read().split())
            catalog[v_id]["status"] = "completed"
            catalog[v_id]["file"] = str(file_path.relative_to(BASE_DIR))
            catalog[v_id]["word_count"] = w_count
            continue

        success = False
        for attempt in range(1, 4):
            try:
                snippets = ytt.fetch(v_id)
                if not snippets:
                    catalog[v_id]["status"] = "no_captions"
                    success = True
                    break
                    
                content, word_count = format_transcript_content(v_id, title, url, snippets)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                    
                catalog[v_id]["status"] = "completed"
                catalog[v_id]["file"] = str(file_path.relative_to(BASE_DIR))
                catalog[v_id]["word_count"] = word_count
                completed_in_run += 1
                blocked_streak = 0
                success = True
                
                print(f"[{completed_in_run}] Completed {v_id}: {title[:40]}")
                break
            except Exception as e:
                err = str(e)
                if "NoTranscriptFound" in err or "TranscriptsDisabled" in err or "VideoUnavailable" in err:
                    catalog[v_id]["status"] = "no_captions"
                    success = True
                    break
                if "RequestBlocked" in err or "IpBlocked" in err or "TooManyRequests" in err:
                    blocked_streak += 1
                    print(f"Rate limited on {v_id}. Auto-rotating TOR circuit...")
                    rotate_tor_circuit()
                    ytt = YouTubeTranscriptApi()
                    time.sleep(2)
                else:
                    time.sleep(1)
                    
        save_catalog(catalog)
        generate_index(catalog)
        time.sleep(random.uniform(0.3, 0.8))

    print("TOR Auto-Rotating Engine loop completed!")


if __name__ == "__main__":
    main()
