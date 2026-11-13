# FFmpeg Recipes for Screencast Demo Videos

## 1. Video Speed Adjustment (`setpts`)
To speed up a video segment to match a target voiceover duration:
$$\text{Speedup Factor } S = \frac{D_{\text{original}}}{D_{\text{audio}}}$$

FFmpeg video filter:
```bash
-vf "setpts=PTS/S,fps=30"
```
*Example*: To turn 20 seconds into 8 seconds ($S = 2.5$):
```bash
-vf "setpts=PTS/2.5,fps=30"
```

## 2. Aspect Ratio & Scaling Preservation
For Retina Mac recordings (3456x2234, ~16:10):
- Scale preserving aspect ratio:
  ```bash
  scale=1920:1242
  ```
- Or maintain width and auto-calculate even height:
  ```bash
  scale=1920:-2
  ```

## 3. High-Quality H.264 Video Encoding
```bash
-c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p
```
- `-crf 18`: Near visually lossless, preserves code syntax highlighting, small text, and sharp icons.
- `-pix_fmt yuv420p`: Universally compatible with iOS, Android, macOS, Windows, and web browsers.

## 4. Audio Resampling & Bitrate
```bash
-c:a aac -b:a 192k -ar 48000 -ac 2
```

## 5. Seamless Multi-Clip Concatenation
1. Create `concat.txt`:
   ```text
   file '/absolute/path/to/clip_01.mp4'
   file '/absolute/path/to/clip_02.mp4'
   ```
2. Concatenate with audio re-mux:
   ```bash
   ffmpeg -f concat -safe 0 -i concat.txt -c:v copy -c:a aac -b:a 192k output.mp4
   ```

## 6. Embedding Subtitles
```bash
ffmpeg -i video.mp4 -i subtitles.srt -c copy -c:s mov_text -metadata:s:s:0 language=eng output_subtitled.mp4
```
