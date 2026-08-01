#!/usr/bin/env python3
import json
import os
import re
from pathlib import Path

BASE_DIR = Path("transcripts/modern-wisdom")
TRANSCRIPTS_DIR = BASE_DIR / "files"
VTT_DIR = BASE_DIR / "vtt"
CATALOG_PATH = BASE_DIR / "catalog.json"
INDEX_PATH = BASE_DIR / "INDEX.md"
CHANNEL_NAME = "Modern Wisdom (Chris Williamson)"

VIDEOS = [
    {"id": "D60hHjROMts", "title": "Why Almost Nobody Gets The Life They Want - Jett Franzen", "url": "https://www.youtube.com/watch?v=D60hHjROMts"},
    {"id": "0GISrdSHUuk", "title": "The Free Fuel That Makes Discipline Easy", "url": "https://www.youtube.com/shorts/0GISrdSHUuk"},
    {"id": "5RpSmbKnl-M", "title": "He Said The Quiet Part Out Loud…", "url": "https://www.youtube.com/shorts/5RpSmbKnl-M"},
    {"id": "nR3ge9B6JG4", "title": "\"Women Are Furious About This Research.\" - Darby Saxbe", "url": "https://www.youtube.com/watch?v=nR3ge9B6JG4"},
    {"id": "3dqtuk828_I", "title": "Nietzsche’s Brutal Psychology Of Losers", "url": "https://www.youtube.com/shorts/3dqtuk828_I"},
    {"id": "V5A9q4HZ1Ro", "title": "Polyvagal Theory: Why You Feel So Anxious All The Time - Dr Stephen Porges", "url": "https://www.youtube.com/watch?v=V5A9q4HZ1Ro"},
    {"id": "WmRkGYB0xm0", "title": "People Really Hate New Dads With Depression", "url": "https://www.youtube.com/shorts/WmRkGYB0xm0"},
    {"id": "qVdr4CQyiQw", "title": "“Terrifying Things Are Happening Inside Biolabs\" - Annie Jacobsen", "url": "https://www.youtube.com/watch?v=qVdr4CQyiQw"},
    {"id": "KnoWCHZRZiQ", "title": "High T & Deadbeat Dads: The Shocking Link", "url": "https://www.youtube.com/shorts/KnoWCHZRZiQ"},
    {"id": "LaSq6lvf_wM", "title": "\"A Lab Will Explode In Russia & Release Something Awful\" - Annie Jacobsen", "url": "https://www.youtube.com/shorts/LaSq6lvf_wM"}
]


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


def process_vtt(vtt_path):
    blocks = {}
    total_words = 0
    with open(vtt_path, 'r', encoding='utf-8', errors='ignore') as f:
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
                    total_words += len(text.split())
    return blocks, total_words


def process_json(json_path):
    blocks = {}
    total_words = 0
    with open(json_path, 'r', encoding='utf-8') as f:
        cues = json.load(f)

    for item in cues:
        text = item.get('text', '').replace('\n', ' ').strip()
        start = item.get('start', 0.0)
        if text:
            minute_marker = int(start // 60) * 60
            if minute_marker not in blocks:
                blocks[minute_marker] = []
            if not blocks[minute_marker] or blocks[minute_marker][-1] != text:
                blocks[minute_marker].append(text)
                total_words += len(text.split())
    return blocks, total_words


def main():
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    catalog = {}

    for idx, item in enumerate(VIDEOS, 1):
        v_id = item["id"]
        title = item["title"]
        url = item["url"]

        vtt_file = VTT_DIR / f"{v_id}.en.vtt"
        json_file = VTT_DIR / f"{v_id}.json"

        blocks, total_words = {}, 0
        if vtt_file.exists():
            blocks, total_words = process_vtt(vtt_file)
        elif json_file.exists():
            blocks, total_words = process_json(json_file)

        if blocks:
            out_lines = [
                f"# {title}",
                f"**Video ID:** `{v_id}` | **Link:** [Watch on YouTube]({url}) | **Channel:** {CHANNEL_NAME}",
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
            filename = f"{slug}_{v_id}.md"
            file_path = TRANSCRIPTS_DIR / filename
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(out_lines))

            rel_path = f"files/{filename}"
            catalog[v_id] = {
                "id": v_id,
                "title": title,
                "url": url,
                "playlist_index": idx,
                "relative_file_path": rel_path,
                "word_count": total_words,
                "status": "completed"
            }
            print(f"[{idx:02d}/10] Saved {filename} ({total_words:,} words)")
        else:
            catalog[v_id] = {
                "id": v_id,
                "title": title,
                "url": url,
                "playlist_index": idx,
                "status": "failed"
            }
            print(f"[{idx:02d}/10] Missing cues for {v_id}")

    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    index_lines = [
        "# Modern Wisdom (Chris Williamson) — Transcripts Index",
        "",
        f"Collection of the latest **{len(catalog)}** transcripts from [Modern Wisdom](https://www.youtube.com/@ChrisWillx).",
        "",
        "| # | Title | Video ID | Words | Local File | YouTube Link |",
        "|---|---|---|---|---|---|"
    ]

    for idx, (v_id, data) in enumerate(sorted(catalog.items(), key=lambda x: x[1].get("playlist_index", 0)), 1):
        rel_path = data.get("relative_file_path", "")
        words = data.get("word_count", 0)
        file_link = f"[`{rel_path.split('/')[-1]}`](file:///Users/isaachernandez/blog%20design/transcripts/modern-wisdom/{rel_path})" if rel_path else "Pending"
        yt_link = f"[Watch]({data['url']})"
        index_lines.append(f"| {idx:02d} | {data['title']} | `{v_id}` | {words:,} | {file_link} | {yt_link} |")

    index_lines.append("")
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(index_lines))

    print("Catalog & INDEX.md generated successfully!")


if __name__ == "__main__":
    main()
