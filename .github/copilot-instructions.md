# GitHub Copilot Repository Instructions

This workspace contains specialized skills, runbooks, and automation scripts for AI-driven software development and automated video demo production.

---

## Available Skills

### 1. `ai-video-demo` (`.github/skills/ai-video-demo/` or `ai-video-demo/`)
**Purpose**: Transforms raw screencast recordings into polished, AI-narrated product walkthroughs and feature demos synchronized to Microsoft Edge-TTS voiceovers and subtitles.

Whenever the user asks to:
- Create an AI demo video, voiceover, or walkthrough from a screen recording (`.mov`, `.mp4`).
- Extract timeline pointers or transcribe actions from a video file.
- Generate voiceover scripts and speech audio with Edge-TTS.
- Speed up or synchronize video clips to fit a specific target duration (e.g., under 90 seconds).

**Strict Workflow Requirements**:
1. **Analyze Recording**:
   Run the analysis script to extract frames and detect visual text/UI transitions:
   ```bash
   python3 .github/skills/ai-video-demo/scripts/analyze_video.py <recording.mov> --output-json timeline.json
   ```
2. **Draft Voiceover Script & Pacing**:
   Draft a JSON specification matching each on-screen feature with start/end seconds and a concise, high-tempo narration sentence.
3. **MANDATORY USER REVIEW GATE**:
   **You MUST present the drafted voiceover transcript to the user for review before generating any audio or video!**
   - Present a clear markdown table with Segment Index, Timestamps, Feature Name, and the Spoken Script.
   - Specify the chosen voice (`en-US-JennyNeural`, `en-US-AriaNeural`, `en-US-GuyNeural`) and speaking rate.
   - Ask: *"Please review the proposed voiceover transcript and timeline. Would you like to adjust any wording, tone, or timing before I generate the voiceover and assemble the video?"*
   - Only proceed once the user approves or adjusts the script.
4. **Generate Voiceover (Post-Approval)**:
   Use Edge-TTS to produce high-fidelity voice clips:
   ```bash
   python3 .github/skills/ai-video-demo/scripts/generate_voiceover.py spec.json --voice en-US-JennyNeural --rate +22%
   ```
5. **Assemble & Synchronize Video**:
   Run the assembly engine to scale, time-stretch, mux audio, concatenate, and embed subtitles:
   ```bash
   python3 .github/skills/ai-video-demo/scripts/assemble_demo.py <recording.mov> audio/metadata.json --output demo_final.mp4
   ```

---

## Tooling & Environment
- **FFmpeg**: Available via Homebrew (`ffmpeg`, `ffprobe`).
- **Edge-TTS**: Available via `uvx edge-tts` or native CLI.
- **Python**: Use Python 3 (`python3` or `uv run python3`).
- **Subtitles**: Subtitles are generated in SubRip format (`.srt`) and embedded as soft subtitles (`mov_text`) in the MP4 container.
