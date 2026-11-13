# AI Voiceover Demo Video Production (`ai-vo-demo-video-production`)

Automated, end-to-end skill and toolkit for turning raw screen recordings into professional, high-tempo, voiceovered product demo videos with synchronized subtitles.

Built for **GitHub Copilot (with Gemini 3.8 Flash High)**, **Google Antigravity**, and standalone CLI workflows.

---

## ⚡ Features

- **Automated Visual & Timeline Analysis**: Uses Apple Vision OCR and FFmpeg frame extraction to identify UI transitions, panel openings, feature demonstrations, and timestamps.
- **Human-in-the-Loop Review Gate**: Enforces a mandatory user review step of the drafted narration transcript before generating audio or rendering video.
- **Studio-Quality Neural Narration**: Generates crystal-clear voiceovers with Microsoft Edge-TTS (`en-US-JennyNeural`, `en-US-AriaNeural`, `en-US-GuyNeural`, etc.) with customizable pacing (`+15%` to `+26%`).
- **Precision Speedup & Audio Sync**: Automatically computes per-segment speedup factors ($\text{Speed} = \frac{\text{video duration}}{\text{audio duration}}$) so that visual actions match the spoken narration to the millisecond.
- **Embedded & Standalone Subtitles**: Generates `.srt` subtitle tracks and embeds soft subtitles (`mov_text`) directly into the output MP4.
- **Cross-Platform Agent Integration**: Fully configured for **GitHub Copilot** (`.github/`), **Google Antigravity** (`.agents/` and `skills/`), and terminal usage (`ai-video-demo/`).

---

## 🤖 Quick Start with GitHub Copilot (Gemini 3.8 Flash High)

👉 **For the complete step-by-step guide, see [`COPILOT_GEMINI_QUICKSTART.md`](./COPILOT_GEMINI_QUICKSTART.md)**.

1. **Select Gemini 3.8 Flash (High) in Copilot Chat**:
   In VS Code, open Copilot Chat (`Cmd+Shift+I` on Mac) and select **Gemini 3.8 Flash (High)** from the model dropdown above the prompt input.
2. **Prompt Copilot**:
   ```text
   @workspace /ai-video-demo for my recording "path/to/recording.mov".
   Cover all features, keep it under 1m30s, and show me the transcript for review before generating audio.
   ```
3. **Review & Approve**:
   Gemini 3.8 Flash (High) extracts timeline pointers and presents a structured feature-by-feature review table in chat. Reply with edits or approve it.
4. **Automatic Assembly**:
   Copilot runs Edge-TTS and FFmpeg to deliver the final MP4 with synchronized subtitles and a production report.

---

## 🚀 Quick Start (CLI)

### Prerequisites
- **FFmpeg & FFprobe**: `brew install ffmpeg`
- **Edge-TTS**: `pip install edge-tts` or `uvx edge-tts`
- **Python 3**: `python3 --version`

### Step 1: Analyze a Recording
Extract frames and identify visual timeline pointers:
```bash
python3 ai-video-demo/scripts/analyze_video.py <recording.mov> --output-json timeline.json
```

### Step 2: Formulate Transcript & Review
Create a segment specification JSON (e.g. `spec.json`):
```json
[
  {
    "id": "01_intro",
    "feature": "Overview",
    "original_timerange": [0.0, 15.0],
    "text": "Welcome to our product demo. Here we explore the core platform capabilities."
  }
]
```
> **Review Gate**: Always confirm the proposed script and duration with the user before proceeding to audio generation.

### Step 3: Generate Voiceover Clips
```bash
python3 ai-video-demo/scripts/generate_voiceover.py spec.json --voice en-US-JennyNeural --rate +22%
```

### Step 4: Assemble Synchronized Demo Video
```bash
python3 ai-video-demo/scripts/assemble_demo.py <recording.mov> audio/metadata.json --output demo_final.mp4
```

---

## 📂 Repository Structure

```text
ai-vo-demo-video-production/
├── README.md                                 # Documentation & usage guide
├── COPILOT_GEMINI_QUICKSTART.md              # Detailed Gemini 3.8 Flash (High) + Copilot guide
├── .gitignore                                # Ignores project subfolders, media, & artifacts
├── .github/
│   ├── copilot-instructions.md               # GitHub Copilot repository runbook
│   ├── prompts/
│   │   └── ai-video-demo.prompt.md           # Copilot Chat prompt template
│   └── skills/
│       └── ai-video-demo/                    # Copilot skill definition & scripts
├── ai-video-demo/                            # Root skill package
│   ├── SKILL.md                              # Master skill instructions & review gate
│   ├── scripts/
│   │   ├── analyze_video.py                  # OCR & timeline analysis
│   │   ├── generate_voiceover.py             # Edge-TTS voice generator
│   │   └── assemble_demo.py                  # FFmpeg speedup, mux & assembly
│   ├── references/
│   │   ├── edge_tts_voices.md                # Voice selection & pacing reference
│   │   └── ffmpeg_recipes.md                 # Scaling & speedup formulas
│   └── examples/
│       └── sample_spec.json                  # Sample segment spec
├── skills/
│   └── ai-video-demo/                        # Antigravity skills/ structure
└── .agents/
    └── skills/ai-video-demo/                 # Agentic discovery structure
```
