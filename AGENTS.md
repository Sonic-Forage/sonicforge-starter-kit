# Agent Notes — SonicForge Live

Purpose: local-first autonomous DJ/VJ control plane for DJ VANTA//SonicForge.

Rules:

- Keep the repo runnable locally without GPU or paid APIs.
- Do not commit generated audio batches, stream keys, API keys, model weights, `.env`, or private prompts.
- Do not start RunPod/Modal/Comfy Cloud, public RTMP, or paid generation without explicit approval.
- Default adapters must be mocks or dry-runs.
- Preserve clean separation: this repo orchestrates; ACE-Step/ComfyUI/RunPod/TouchDesigner backends generate/render.
- Voice/TTS output is opt-in; text talk-break scripts are safe defaults.
