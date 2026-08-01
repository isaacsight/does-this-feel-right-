#!/usr/bin/env python3
"""
Transcript Parser Tool
Parses timestamped markdown files (e.g. **[MM:SS]** or **[HH:MM:SS]**) into structured timestamped chunks.
"""

import re
from typing import List, Dict, Any
from pathlib import Path

TIMESTAMP_PATTERN = re.compile(r'\*\*\[(\d{1,2}:)?(\d{1,2}):(\d{2})\]\*\*')

def time_str_to_seconds(time_str: str) -> float:
    """Converts MM:SS or HH:MM:SS string to float seconds."""
    parts = time_str.split(':')
    parts = [int(p) for p in parts]
    if len(parts) == 2:
        return float(parts[0] * 60 + parts[1])
    elif len(parts) == 3:
        return float(parts[0] * 3600 + parts[1] * 60 + parts[2])
    return 0.0

def parse_transcript_markdown(filepath: str) -> List[Dict[str, Any]]:
    """
    Parses a timestamped markdown file into a list of transcript blocks.
    Returns list of dicts: [{'start_str': '01:00', 'start_sec': 60.0, 'text': '...'}]
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Transcript file not found: {filepath}")

    text = path.read_text(encoding='utf-8')
    matches = list(TIMESTAMP_PATTERN.finditer(text))
    
    blocks = []
    for i, match in enumerate(matches):
        raw_time = match.group(0).replace('**[', '').replace(']**', '')
        start_sec = time_str_to_seconds(raw_time)
        
        start_pos = match.end()
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        chunk_text = text[start_pos:end_pos].strip()
        
        if chunk_text:
            blocks.append({
                "start_str": raw_time,
                "start_sec": start_sec,
                "text": chunk_text
            })

    return blocks

if __name__ == "__main__":
    import sys
    file_path = sys.argv[1] if len(sys.argv) > 1 else "transcript_HwmwyBgzj8c.md"
    parsed = parse_transcript_markdown(file_path)
    print(f"Parsed {len(parsed)} timestamped blocks from {file_path}.")
    if parsed:
        print(f"Sample Block [0]: {parsed[0]}")
