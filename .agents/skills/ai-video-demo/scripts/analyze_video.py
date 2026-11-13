#!/usr/bin/env python3
"""
Video Timeline & Visual Content Analyzer for Demo Video Production.
Extracts frames and runs OCR / scene detection to identify pointers and timestamps.
"""

import argparse
import json
import os
import subprocess
import sys


def get_video_info(video_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration,size,bit_rate",
        "-show_entries", "stream=width,height,codec_name,r_frame_rate",
        "-of", "json", video_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


def extract_frames(video_path, output_dir, interval=3):
    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"fps=1/{interval},scale=960:-1",
        f"{output_dir}/frame_%03d.jpg"
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def run_macos_vision_ocr(frames_dir):
    """Uses macOS native Vision Framework for fast, accurate text extraction."""
    swift_code = f"""
import Foundation
import Vision
import AppKit

let fileManager = FileManager.default
let dir = "{frames_dir}"
let files = (try? fileManager.contentsOfDirectory(atPath: dir))?.filter {{ $0.hasSuffix(".jpg") }}.sorted() ?? []

for file in files {{
    let path = "\\(dir)/\\(file)"
    guard let image = NSImage(contentsOfFile: path),
          let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {{ continue }}
    
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
    try? handler.perform([request])
    
    let texts = request.results?.compactMap {{ $0.topCandidates(1).first?.string }} ?? []
    let summary = texts.prefix(10).joined(separator: " | ")
    print("\\(file)\\t\\(summary)")
}}
"""
    cmd = ["swift", "-"]
    res = subprocess.run(cmd, input=swift_code, capture_output=True, text=True)
    results = []
    for line in res.stdout.strip().split("\n"):
        if "\t" in line:
            fname, text = line.split("\t", 1)
            results.append((fname, text))
    return results


def main():
    parser = argparse.ArgumentParser(description="Analyze video recording for demo creation")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("--interval", type=int, default=3, help="Sampling interval in seconds")
    parser.add_argument("--output-json", help="Save timeline to JSON file")
    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"Error: {args.video} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Inspecting {args.video}...")
    info = get_video_info(args.video)
    dur = float(info["format"]["duration"])
    vstream = next(s for s in info["streams"] if s.get("width"))
    w = vstream["width"]
    h = vstream["height"]
    print(f"Video specs: {w}x{h}, duration {dur:.2f}s ({dur/60:.2f} minutes)")

    temp_frames = ".temp_analysis_frames"
    print(f"Extracting frames every {args.interval}s...")
    extract_frames(args.video, temp_frames, args.interval)

    print("Analyzing visual timeline...")
    ocr_results = run_macos_vision_ocr(temp_frames)

    timeline = []
    for idx, (fname, text) in enumerate(ocr_results):
        t_sec = idx * args.interval
        timeline.append({"time_sec": t_sec, "frame": fname, "detected_text": text})
        print(f"[{t_sec:3d}s] {text[:90]}...")

    if args.output_json:
        with open(args.output_json, "w") as f:
            json.dump({"video": args.video, "duration": dur, "timeline": timeline}, f, indent=2)
        print(f"Saved timeline to {args.output_json}")

    # cleanup
    subprocess.run(["rm", "-rf", temp_frames])


if __name__ == "__main__":
    main()
