# Quick Start with GitHub Copilot (Gemini 3.8 Flash High)

This guide walks you through using **GitHub Copilot powered by the latest Gemini 3.8 Flash (High) model** to create automated, AI-voiceovered demo videos in this repository.

---

## Why Use Gemini 3.8 Flash (High) with Copilot?

The latest **Gemini 3.8 Flash (High)** model offers distinct advantages for video demo automation:
- **Massive Context & Ultra-Fast Throughput**: Ingests extensive frame OCR data, visual timeline logs, and source code files simultaneously with lightning-fast response times.
- **High-Reasoning Precision Timing**: Accurately computes second-by-second speedup ratios ($\frac{D_{\text{video}}}{D_{\text{audio}}}$) with high-confidence mathematical logic to match video clips to narration lengths.
- **Crisp, High-Impact Scriptwriting**: Produces punchy, technical marketing narration tailored to strict speaking rates (+20% to +26%) and tight time limits.

---

## 🛠️ Step 1: Select Gemini 3.8 Flash (High) in GitHub Copilot

1. **Open VS Code** in this workspace:
   ```bash
   code /path/to/ai-vo-demo-video-production
   ```
2. **Open Copilot Chat**:
   - Press `Cmd + Shift + I` (Mac) or `Ctrl + Shift + I` (Windows/Linux).
   - Or click the **GitHub Copilot Chat** icon in the activity bar.
3. **Switch to Gemini 3.8 Flash (High)**:
   - Locate the **Model Picker dropdown** right above the chat prompt input box.
   - Click the dropdown and select **Gemini 3.8 Flash (High)**.

> [!TIP]
> **Don't see Gemini 3.8 Flash (High) in the model list?**
> - Make sure the **GitHub Copilot Chat** extension is updated to the latest release.
> - Ensure your GitHub organization or personal settings have multi-model access enabled:
>   Navigate to **GitHub.com → Settings → Copilot → Model Policies** and verify **Gemini 3.8 Flash (High)** is enabled.

---

## 🎬 Step 2: Prompt Copilot to Produce Your Demo

GitHub Copilot automatically loads [`.github/copilot-instructions.md`](./.github/copilot-instructions.md) and the `/ai-video-demo` prompt template.

### Example Prompt

Type the following into Copilot Chat with **Gemini 3.8 Flash (High)**:

```text
@workspace /ai-video-demo for my recording "path/to/screen_recording.mov".
Please:
1. Extract all visual pointers and UI transitions.
2. Cover all features shown in the recording.
3. Keep the total video duration strictly within 1 minute 30 seconds.
4. Use a clear female voice (en-US-JennyNeural).
5. Present the draft voiceover transcript for my review before generating audio!
```

---

## 🔍 Step 3: Review the Transcript (Human-in-the-Loop Gate)

Copilot (powered by Gemini 3.8 Flash High) will analyze your video's timeline and present a structured review table:

| Segment | Feature Name | Original Clip | Target Duration | Proposed Voiceover Script |
|---|---|---|---|---|
| `01_intro` | Landing Page | `0:00 - 0:15` | ~9.0s | *"Welcome to our platform overview..."* |
| `02_tools` | Feature Deep Dive | `0:15 - 0:45` | ~12.5s | *"Here we configure automated guardrails..."* |
| `03_outro` | Summary | `0:45 - 0:55` | ~4.0s | *"Get started today..."* |

### Approving or Editing the Script
- **To approve**: Simply reply: *"Looks great, proceed with generation!"*
- **To adjust wording**: Reply with changes, e.g.:
  > *"On segment 2, emphasize token optimization and cost savings instead."*

---

## ⚡ Step 4: Automated Assembly & Delivery

Once approved, Copilot executes the automated pipeline:
1. **Edge-TTS Audio Generation**:
   ```bash
   python3 .github/skills/ai-video-demo/scripts/generate_voiceover.py spec.json --voice en-US-JennyNeural --rate +24%
   ```
2. **FFmpeg Video Speedup & Synchronization**:
   ```bash
   python3 .github/skills/ai-video-demo/scripts/assemble_demo.py <recording.mov> audio/metadata.json --output final_demo.mp4
   ```
3. **Subtitles & Artifacts**:
   - Embeds soft subtitles (`mov_text`) directly into `final_demo.mp4`.
   - Generates standalone `final_demo.srt` and detailed production report.

---

## 💡 Pro Tips for Gemini 3.8 Flash (High) + Copilot

1. **Faster Demo Pacing**: Tell Gemini 3.8 Flash (High) *"Set voiceover rate to +25% and use snappy speedruns for menus"* to compress long recordings into crisp 60–90 second videos.
2. **Accents & Voice Selection**: Ask Gemini for alternative voices (e.g. `en-US-AriaNeural`, `en-GB-RyanNeural`, `en-US-GuyNeural`). Refer to [`ai-video-demo/references/edge_tts_voices.md`](./ai-video-demo/references/edge_tts_voices.md).
3. **Keep Heavy Media Out of Git**: Put your raw videos in subfolders like `projects/<name>/` or `demos/`; `.gitignore` will ensure they are not committed.
