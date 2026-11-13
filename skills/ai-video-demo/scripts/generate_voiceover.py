#!/usr/bin/env python3
"""
Edge-TTS Voiceover Generator for Demo Videos.
Generates crystal-clear AI voice narration segments and computes exact durations.
"""

import argparse
import json
import os
import subprocess
import sys


def find_edge_tts():
    # check uvx or path
    if subprocess.run(["which", "edge-tts"], capture_output=True).returncode == 0:
        return ["edge-tts"]
    uvx_path = os.path.expanduser("~/.local/bin/uvx")
    if os.path.exists(uvx_path):
        return [uvx_path, "edge-tts"]
    if subprocess.run(["which", "uvx"], capture_output=True).returncode == 0:
        return ["uvx", "edge-tts"]
    print("Error: neither 'edge-tts' nor 'uvx' found in PATH.", file=sys.stderr)
    sys.exit(1)


def get_audio_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())


def main():
    parser = argparse.ArgumentParser(description="Generate AI voiceovers using Edge-TTS")
    parser.add_argument("spec_json", help="Path to JSON file with segments: [{'id', 'text', ...}]")
    parser.add_argument("--output-dir", default="audio", help="Directory to save generated audio files")
    parser.add_argument("--voice", default="en-US-JennyNeural", help="TTS Voice (default: en-US-JennyNeural)")
    parser.add_argument("--rate", default="+20%", help="TTS Speaking Rate (default: +20%)")
    args = parser.parse_args()

    if not os.path.exists(args.spec_json):
        print(f"Error: {args.spec_json} not found", file=sys.stderr)
        sys.exit(1)

    with open(args.spec_json) as f:
        segments = json.load(f)

    os.makedirs(args.output_dir, exist_ok=True)
    edge_cmd = find_edge_tts()

    total_dur = 0.0
    enriched = []

    print(f"Generating voiceover with voice='{args.voice}', rate='{args.rate}'...")
    for idx, seg in enumerate(segments):
        sid = seg.get("id", f"seg_{idx:02d}")
        text = seg["text"]
        out_file = os.path.join(args.output_dir, f"{sid}.mp3")

        cmd = edge_cmd + [
            "--voice", args.voice,
            "--rate", args.rate,
            "--text", text,
            "--write-media", out_file
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)

        dur = get_audio_duration(out_file)
        total_dur += dur
        seg_info = dict(seg)
        seg_info["audio_file"] = out_file
        seg_info["audio_duration"] = dur
        enriched.append(seg_info)
        print(f"  [{sid}] ({dur:.2f}s): {text[:60]}...")

    print(f"\nAll voice segments generated! Total voiceover length: {total_dur:.2f}s ({total_dur/60:.2f}m)")
    meta_path = os.path.join(args.output_dir, "metadata.json")
    with open(meta_path, "w") as f:
        json.dump(enriched, f, indent=2)
    print(f"Saved metadata to {meta_path}")


if __name__ == "__main__":
    main()
