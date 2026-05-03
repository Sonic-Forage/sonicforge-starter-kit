# ComfyUI Workflow Card — Intergalactic DJs Visual Spell

Status: **dry-run contract only**. Do not call local/remote ComfyUI unless explicitly enabled.

## Purpose

Generate or route visual spell assets for SonicForge Live / Intergalactic DJs:

- Deck A/B cover art;
- DJ VANTA phrase-lock cards;
- rave survival kit QR poster art;
- VJ portal stills/loops;
- readable text overlays for shader/code-rain modes.

## Safe first action

Expose this as a JSON cue returned by the planner and rendered by the browser visualizer. The cue can later become a ComfyUI `/prompt` payload.

## Required inputs

- `workflow`: `intergalactic-djs-visual-spell`
- `deck`: `A` or `B`
- `segment_id`
- `prompt`
- `negative_prompt`
- `seed`
- `width`, `height`
- `mode`: `dry_run` by default

## Example prompt

`readable neon typography, ASCII spectrograph star gate, DJ VANTA signal, words PHRASE LOCK 32, underground PNW rave flyer energy, black paper, vermilion accent, scanner grain`

## API routes when enabled

- `GET /system_stats`
- `GET /object_info`
- `POST /prompt`
- `GET /history/{prompt_id}`
- `GET /view?...`

## Safety

- No Comfy Cloud / paid GPU by default.
- No hidden model download.
- No public posting.
- Do not commit generated batches unless tiny and explicitly selected for demo.
- Preserve readable text constraints; prefer Qwen-Image/FLUX text-capable lanes later.
