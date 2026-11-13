#!/usr/bin/env python3
"""
FFmpeg Demo Video Assembly & Synchronization Engine.
Trims video clips, calculates speedup factors to match voiceover timing,
concatenates segments, and embeds subtitles.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys


def fmt_srt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int((sec - int(sec)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def assemble(video_input, spec_file, output_mp4, scale_res="1920:1242", fps=30):
    with open(spec_file) as f:
        segments = json.load(f)

    temp_dir = ".temp_assemble_clips"
    os.makedirs(temp_dir, exist_ok=True)
    concat_list = []
    srt_entries = []
    cumulative_time = 0.0

    print(f"Assembling demo from '{video_input}' with {len(segments)} segments...")

    for idx, seg in enumerate(segments):
        sid = seg.get("id", f"seg_{idx:02d}")
        v_start, v_end = seg["original_timerange"]
        audio_path = seg.get("audio_file") or f"audio/{sid}.mp3"

        # Check audio file
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file '{audio_path}' not found for segment '{sid}'")

        # Get audio duration
        ffprobe_cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", audio_path
        ]
        a_dur = float(subprocess.check_output(ffprobe_cmd).decode().strip())

        v_dur = v_end - v_start
        speed = v_dur / a_dur
        out_clip = os.path.join(temp_dir, f"clip_{idx:02d}_{sid}.mp4")

        print(f"  Rendering [{sid}]: {v_start:.1f}s-{v_end:.1f}s ({v_dur:.1f}s) -> {a_dur:.2f}s (speed: {speed:.2f}x)")

        # Render clip with video speedup & audio resample
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(v_start),
            "-to", str(v_end),
            "-i", video_input,
            "-i", audio_path,
            "-filter_complex",
            f"[0:v]setpts=PTS/{speed:.6f},scale={scale_res},fps={fps}[v];[1:a]aformat=sample_rates=48000:channel_layouts=stereo[a]",
            "-map", "[v]",
            "-map", "[a]",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            out_clip
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        concat_list.append(f"file '{os.path.abspath(out_clip)}'")

        # Subtitle entry
        start_t = cumulative_time
        end_t = cumulative_time + a_dur
        cumulative_time = end_t
        text = seg.get("text", "")
        srt_entries.append(f"{idx+1}\n{fmt_srt_time(start_t)} --> {fmt_srt_time(end_t)}\n{text}\n")

    # Write concat list
    concat_file = os.path.join(temp_dir, "concat.txt")
    with open(concat_file, "w") as f:
        f.write("\n".join(concat_list) + "\n")

    # Generate SRT file
    base_name = os.path.splitext(output_mp4)[0]
    srt_file = f"{base_name}.srt"
    with open(srt_file, "w") as f:
        f.write("\n".join(srt_entries))
    print(f"Generated subtitles: {srt_file}")

    temp_concat_mp4 = os.path.join(temp_dir, "concatenated.mp4")
    print("Concatenating clips...")
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_file,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        temp_concat_mp4
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Embed soft subtitles
    print(f"Embedding subtitles and finalizing '{output_mp4}'...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", temp_concat_mp4,
        "-i", srt_file,
        "-c", "copy",
        "-c:s", "mov_text",
        "-metadata:s:s:0", "language=eng",
        output_mp4
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Cleanup temp directory
    shutil.rmtree(temp_dir)
    print(f"Demo video assembly complete! Output: {output_mp4} (Duration: {cumulative_time:.2f}s)")


def main():
    parser = argparse.ArgumentParser(description="Assemble video and voiceover clips into a final demo video")
    parser.add_argument("video", help="Input raw video recording")
    parser.add_argument("spec", help="Segment specification JSON with original_timerange and text")
    parser.add_argument("--output", default="demo_final.mp4", help="Output final video MP4")
    parser.add_argument("--scale", default="1920:1242", help="Scale resolution (width:height, default: 1920:1242)")
    parser.add_argument("--fps", type=int, default=30, help="Target FPS (default: 30)")
    args = parser.parse_args()

    assemble(args.video, args.spec, args.output, scale_res=args.scale, fps=args.fps)


if __name__ == "__main__":
    main()
