# Text Shader + Audio-Reactive Visual Plan

Updated: 2026-05-01T07:41:29.515724+00:00

## Why this helps us win

The demo should look like Hermes is literally casting spells into the rave system: text, code, GLSL packets, and DJ VANTA interludes become visuals. This connects the hackathon's agent/code angle to the party/show angle.

Winning sentence:

> DJ VANTA turns Hermes text/code output into live visual spells: audio-reactive typography, shader packets, code rain, subtitle overlays, and VJ cue packets for browser, Resolume, or TouchDesigner.

## Visual modes to build

### 1. Code Rain Transmission

- Terminal glyphs, BPM numbers, DJ VANTA phrases, EQ moves, and set-state JSON fall downward.
- Audio energy controls fall speed, glow, chromatic split, and line density.
- Works in browser visualizer without WebGL dependency.

### 2. SDF/MSDF Text Shader Lane

- Use signed distance field text rendering principles for crisp scalable text in WebGL later.
- Research seeds:
  - MSDF collections exist for GLSL/high-quality text rendering: https://github.com/Blatko1/awesome-msdf
  - SDF text is commonly used for vector-like text in OpenGL/WebGL.
- For tonight: create the contract and a browser fallback using canvas text; future WebGL shader upgrades can use SDF/MSDF atlases.

### 3. Kinetic Typography / Spell Overlay

- Hermes produces short “visual spell” lines:
  - `BASS_SWAP LOWS -> TRACK_B`
  - `PHRASE_LOCK 32 BARS`
  - `SURVIVAL_PING HYDRATE`
  - `VANTA_SIGNAL INTERGALACTIC_DJS`
- Visualizer renders them as pulsing/subtitle overlays.

### 4. EQ Band Shrine

- Three large visual bands: LOW / MID / HIGH.
- Transition planner EQ moves animate the bands.
- Bass swap = low band flips color; mid carve = mid band opens; high shimmer = high band sparkles.

### 5. Waveform Gate / Portal

- Mock/audio energy drives neon gate geometry.
- Phrase count controls gate rotations every 8/16/32 bars.
- Crowd state changes palette: warmup, curious, locked-in, peak, cooldown.

### 6. Resolume/TouchDesigner Cue Packet Output

Each visual spell can be serialized as:

```json
{
  "type": "visual.spell",
  "scene": "code_rain_transmission",
  "text": "SURVIVAL_PING HYDRATE",
  "bpm": 128,
  "energy": 6,
  "palette": ["black", "cyan", "magenta", "ultraviolet"],
  "effect_cues": ["glow", "feedback", "chromatic_split"],
  "route_targets": ["browser", "resolume_mcp", "touchdesigner"]
}
```

## Implementation tasks

- Add visualizer mode switcher: `plasma`, `code_rain`, `eq_bands`, `waveform_gate`, `subtitle_spell`.
- Add visual spell packet to `/api/next-segment` response.
- Add UI panel showing current spell/code visual text.
- Add browser implementation first; keep Resolume/TouchDesigner as opt-in adapter contracts.
- Add verifier strings so the demo proves text/code visuals exist.

## Safety / performance

- Browser-first, no GPU cloud.
- Use Canvas 2D fallback before heavy WebGL.
- No remote shader downloads at runtime unless explicitly approved.
- Avoid flashing/strobe extremes; include `reduced_motion` or calm mode for survival kit moments.

## 2026-05-01 implementation note — SDF/MSDF browser fallback

Task-board item M.7 is now represented in the running demo as a **future lane plus safe browser fallback**, not a live WebGL shader stack:

- Control deck panel: `id="sdf-msdf-text-shader-lane"` explains the SDF/MSDF text shader future lane, closed gates, and browser-first fallback.
- Visualizer mode: `sdf_text_fallback` renders layered high-contrast Canvas 2D typography with `SDF/MSDF TEXT SHADER FUTURE LANE`, `MSDF_ATLAS_DRY_RUN`, `PHRASE_LOCK`, `BASS_SWAP`, and `SURVIVAL_PING` vocabulary.
- Future implementation contract: use a local WebGL SDF/MSDF atlas for crisp scalable text only after a human approves local graphics work; do not fetch remote shaders/assets at runtime, do not start ComfyUI/TouchDesigner/provider lanes, and do not claim a verified live shader until browser and capture smoke tests pass.
- Fail-closed flags stay explicit: `starts_gpu=false`, `starts_paid_api=false`, `publishes_stream=false`, `records_audio=false`, `requires_human_approval=true`.
