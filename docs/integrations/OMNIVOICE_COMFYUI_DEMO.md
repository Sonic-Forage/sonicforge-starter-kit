# OmniVoice ComfyUI Demo Lane

Status: private/operator demo lane. ComfyUI is the active backend for OmniVoice host voices.

## Saved workflows

- Exact uploaded workflow: `workflows/comfyui/omni_voice_design_api.keep_model_unloaded.json`
- Reusable API workflow: `workflows/comfyui/omni_voice_design_api.reusable.json`

The operator-edited workflow sets:

```json
"keep_model_loaded": false
```

That is intentional for the demo lane so the OmniVoice model does not stay resident after each generation.

## Current rule

- Use ComfyUI endpoint routes: `/system_stats`, `/object_info`, `/queue`, `/prompt`, `/history/{prompt_id}`, `/view`.
- Do not commit endpoint URLs, API keys, RunPod tokens, or private media credentials.
- Keep `voice_instruct` as OmniVoice tag-style descriptors. Put persona/story in `text`.
- For demo playback, use the already generated audio under `/opt/data/audio_cache/sonicforge_space_juice/` unless the operator asks for another generation.

## Continuous-play next step

For continuous play, prefer a local/static playlist manifest first, then patch plugin/endpoint adapters later so backends can swap cleanly:

1. Manifest of approved audio clips.
2. Browser/player loop controls.
3. ComfyUI adapter contract for generation.
4. Endpoint registry that can rotate RunPod/Modal/local ComfyUI bases without hardcoding secrets.

## Latest demo asset manifest

See `data/manifests/omnivoice_demo_assets_manifest.json`.
