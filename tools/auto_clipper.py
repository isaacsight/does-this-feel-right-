#!/usr/bin/env python3
"""
Auto-Clipper Tool
Uses Gemini API to analyze timestamped transcript blocks and extract high-retention viral video clips.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from transcript_parser import parse_transcript_markdown, time_str_to_seconds

load_dotenv()

PROMPT_TEMPLATE = """You are an expert viral short-form video editor for TikTok, YouTube Shorts, and Instagram Reels.
Below is a full timestamped transcript of a long-form video/podcast.

Analyze the transcript and select {num_clips} standalone, highly engaging clip candidates.

Criteria for a viral clip candidate:
1. High emotional intensity, counter-intuitive insight, or strong hook within the first 5 seconds.
2. Self-contained story or business lesson (30 to 90 seconds in duration).
3. Clear start and end timestamps matching the transcript markers.

Output ONLY a raw valid JSON array of objects with the following schema for each clip candidate:
[
  {{
    "clip_id": 1,
    "title": "Descriptive Short Title",
    "start_timestamp": "MM:SS",
    "end_timestamp": "MM:SS",
    "start_sec": float,
    "end_sec": float,
    "hook": "The exact hook sentence spoken in the first 5 seconds",
    "viral_score": float (1-10 rating),
    "reasoning": "Brief explanation of why this clip will perform well on social media"
  }}
]

Transcript:
{transcript_text}
"""

def analyze_transcript_for_clips(transcript_path: str, num_clips: int = 5) -> list:
    api_key = os.getenv("VITE_GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing VITE_GEMINI_API_KEY or GEMINI_API_KEY environment variable.")

    parsed_blocks = parse_transcript_markdown(transcript_path)
    
    # Format transcript text for LLM context
    formatted_lines = []
    for b in parsed_blocks:
        formatted_lines.append(f"**[{b['start_str']}]** {b['text']}")
    transcript_text = "\n\n".join(formatted_lines)

    client = genai.Client(api_key=api_key)
    prompt = PROMPT_TEMPLATE.format(num_clips=num_clips, transcript_text=transcript_text)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.3
        )
    )

    result_json = json.loads(response.text)
    return result_json

def main():
    parser = argparse.ArgumentParser(description="AI Short-Form Video Clip Discoverer")
    parser.add_argument("--transcript", type=str, default="transcript_HwmwyBgzj8c.md", help="Path to timestamped transcript file")
    parser.add_argument("--clips", type=int, default=5, help="Number of viral clips to extract")
    parser.add_argument("--output", type=str, default="clips_analysis.json", help="Output JSON file path")
    args = parser.parse_args()

    print(f"Analyzing transcript '{args.transcript}' for top {args.clips} viral clips...")
    clips = analyze_transcript_for_clips(args.transcript, num_clips=args.clips)
    
    output_path = Path(args.output)
    output_path.write_text(json.dumps(clips, indent=2), encoding="utf-8")
    
    print(f"\nSuccessfully discovered {len(clips)} clips! Saved to '{args.output}'.\n")
    for c in clips:
        print(f"★ Clip #{c.get('clip_id', 1)} [{c.get('start_timestamp')} -> {c.get('end_timestamp')}] (Score: {c.get('viral_score')}/10)")
        print(f"  Title: {c.get('title')}")
        print(f"  Hook: \"{c.get('hook')}\"")
        print(f"  Reason: {c.get('reasoning')}\n")

if __name__ == "__main__":
    main()
