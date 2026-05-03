# Visual Spell Routing Cue Packets — Resolume + TouchDesigner

Updated: 2026-05-01T10:10:37+00:00

## Purpose

This document turns SonicForge Live visual spells into **dry-run show-control cue packets** for the future VJ stack. It maps the same `visual_spell` object returned by `/api/next-segment` to browser, Resolume, TouchDesigner, and ComfyUI lanes without opening any provider, GPU, stream, or remote-control lane by default.

Brand context: **Intergalactic DJs presents DJ VANTA, powered by SonicForge Live**. DJ VANTA can plan browser-first VJ cues now, then route the same metadata into Resolume Arena, TouchDesigner/Spout/Syphon, OBS, or ComfyUI only after an awake operator approves and arms those adapters.

## Closed-by-default contract

Every cue packet must carry these flags:

```json
{
  "mode": "dry_run",
  "starts_gpu": false,
  "starts_paid_api": false,
  "publishes_stream": false,
  "records_audio": false,
  "requires_human_approval": true
}
```

No unattended run may:

- call ComfyUI `/prompt`;
- start Comfy Cloud, Modal, RunPod, or any paid GPU;
- publish RTMP/SRT/WHIP;
- control a live Resolume/TouchDesigner show machine beyond local dry-run packets;
- record or upload private party media.

## Normalized visual spell fields

`/api/next-segment` should keep one normalized cue that downstream adapters can read:

```json
{
  "type": "visual.spell",
  "workflow": "intergalactic-djs-visual-spell",
  "mode": "dry_run",
  "deck": "B",
  "scene": "code_rain_transmission",
  "text": "PHRASE_LOCK 32 // BASS_SWAP BAR_17 // SURVIVAL_PING HYDRATE",
  "bpm": 128,
  "energy": 6,
  "palette": "black, cyan, magenta, ultraviolet",
  "route_targets": ["browser", "resolume_contract", "touchdesigner_contract", "comfyui_dry_run"],
  "starts_gpu": false,
  "starts_paid_api": false,
  "publishes_stream": false
}
```

## Resolume cue packet mapping

Future adapter lane: `resolume_contract`.

```json
{
  "adapter": "resolume_contract",
  "mode": "dry_run",
  "composition": "Intergalactic DJs / DJ VANTA",
  "layer": "Deck B Visual Spell",
  "clip_or_source": "browser_visualizer_code_rain",
  "effect": "glow_feedback_chromatic_split",
  "bpm": 128,
  "palette": "black, cyan, magenta, ultraviolet",
  "text_overlay": "PHRASE_LOCK 32 // BASS_SWAP BAR_17",
  "survival_overlay": "SURVIVAL_PING HYDRATE",
  "crossfader_hint": "equal_power bar 17 midpoint",
  "route": "manual_operator_copy_to_resolume_or_future_mcp",
  "starts_gpu": false,
  "starts_paid_api": false,
  "publishes_stream": false,
  "requires_human_approval": true
}
```

Implementation notes:

- Browser visualizer stays the source of truth during the hackathon demo.
- Resolume receives a cue packet or browser-source recipe, not an automatic live OSC/MCP command.
- If a real Resolume MCP/OSC adapter is added later, add an approval gate and smoke-test it locally before any party use.

## TouchDesigner cue packet mapping

Future adapter lane: `touchdesigner_contract`.

```json
{
  "adapter": "touchdesigner_contract",
  "mode": "dry_run",
  "network": "/project1/sonicforge_visual_spell",
  "operator_family": "TOP/CHOP/DAT",
  "scene": "code_rain_transmission",
  "text_overlay": "PHRASE_LOCK 32 // BASS_SWAP BAR_17 // SURVIVAL_PING HYDRATE",
  "uniforms": {
    "uBpm": 128,
    "uEnergy": 6,
    "uDeck": "B",
    "uPhraseLockBars": 32,
    "uBassSwapBar": 17
  },
  "route": "manual_operator_copy_to_touchdesigner_or_future_twozero_mcp",
  "spout_syphon_hint": "send TOP out to OBS/Resolume only after operator approval",
  "starts_gpu": false,
  "starts_paid_api": false,
  "publishes_stream": false,
  "requires_human_approval": true
}
```

Implementation notes:

- Follow the TouchDesigner MCP rule: do not guess parameter names; inspect operator parameter info before setting live node params.
- Use browser fallback first. TouchDesigner output is a future local adapter, not a hidden dependency.
- Any Spout/Syphon/NDI/OBS output remains operator-armed and local-only until approved.

## Browser fallback mapping

Current working lane: `/visualizer`.

- `scene=code_rain_transmission` → `code_rain` mode.
- `scene=eq_band_shrine` → `eq_bands` mode.
- `text` / `survival_overlay` → `subtitle_spell` HUD.
- Deck A/B handoff → `dual_ascii_spectrograph` HUD.
- `COMFYUI_DRY_RUN` / `TOUCHDESIGNER_CONTRACT` labels stay visible so judges can see what is planned versus what is running.

## ComfyUI mapping

Future adapter lane: `comfyui_dry_run`.

- Read `comfyui_visual_spell.input.prompt` as the eventual `/prompt` source.
- Keep `prompt_id: null` and `files: []` until an operator approves a real local ComfyUI call.
- Use `/system_stats`, `/object_info`, `/prompt`, `/ws`, `/history/{prompt_id}`, and `/view` only in an approved adapter test.

## Demo operator script

1. Open `http://127.0.0.1:8000/visualizer` in a browser/OBS source.
2. Click `Plan Next Continuous Segment` in the control deck.
3. Show the `visual_spell.routing_contracts` JSON in the response/UI/devtools.
4. Say: “This is dry-run show-control metadata. Browser visuals run now; Resolume, TouchDesigner, and ComfyUI remain human-approved adapters.”

## Acceptance checks

- `/api/next-segment` includes `visual_spell.routing_contracts.resolume` and `visual_spell.routing_contracts.touchdesigner`.
- Every routing packet is `mode=dry_run` and has fail-closed flags.
- `/visualizer` still works as the browser-first output lane.
- No external provider, GPU, stream, recording, or live VJ app is started by default.
