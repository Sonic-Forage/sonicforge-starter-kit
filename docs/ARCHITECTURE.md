# Architecture — SonicForge Live

SonicForge Live is a **control plane**, not a monolithic model. It keeps the show state, decides the next move, and routes work to swappable backends.

## Lanes

- **Guide lane:** human/Hermes instructions become set state: BPM, mode, energy, scene, transition intent.
- **Track lane:** mock local WAV now; ACE-Step local/RunPod/ComfyUI later.
- **Talk lane:** text talk-break now; local KittenTTS/Qwen3-TTS/VibeVoice later; voice cloning requires consent.
- **Mix lane:** clean intro/outro and ducking specs now; future FFmpeg/SoX/Python audio crossfade renderer.
- **Visual lane:** browser canvas now; ComfyUI/TouchDesigner/Spout/Resolume later.
- **Stream lane:** dry-run plans now; OBS/RTMP/WHIP/SRT with explicit approval later.

## Practical routing options

### Local window / OBS / projector

Use `/visualizer` as a full-screen browser source. Capture it in OBS, Resolume browser/source workflows, or projector display.

### TouchDesigner / Spout / Resolume

- Browser window capture is the universal fallback.
- On Windows, TouchDesigner can receive state over WebSocket/HTTP and output Spout to Resolume.
- If twozero MCP is available, Hermes can build/modify the TD patch directly.

### ComfyUI / Comfy Cloud

SonicForge Live should call a ComfyUI adapter using `COMFYUI_BASE_URL` and a workflow card. Cloud jobs stay approval-gated.

### RunPod ACE-Step

Use `RUNPOD_ACE_STEP_API_URL` to connect to an already-running ACE-Step API. Do not start pods from this repo by default.

### RTMP

Use OBS first for reliability. Direct FFmpeg RTMP can be added, but keep it dry-run until `SONICFORGE_ALLOW_PUBLIC_STREAM=true` and stream target is confirmed.
