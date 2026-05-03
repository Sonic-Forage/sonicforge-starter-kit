# TouchDesigner / Spout / Syphon Routing Contract

Updated: 2026-05-01T11:04:58Z

## Status

`dry-run / operator-armed only`

This card documents how **SonicForge Live** can hand DJ VANTA visual-spell metadata to a future local TouchDesigner show computer. It does not control TouchDesigner, start twozero MCP, open Spout/Syphon output, publish streams, record media, or call any paid provider by default.

Brand context: **Intergalactic DJs** is the show layer, **DJ VANTA//SonicForge** is the first performer, and **SonicForge Live** is the local-first runtime/platform.

## Closed flags

```json
{
  "adapter": "touchdesigner_contract",
  "status": "dry_run_operator_armed_only",
  "starts_gpu": false,
  "starts_paid_api": false,
  "publishes_stream": false,
  "records_audio": false,
  "uploads_private_media": false,
  "requires_human_approval": true
}
```

Operator rule: browser `/visualizer` remains the active local fallback. TouchDesigner, Spout, Syphon, NDI, OBS capture, Resolume, and twozero MCP are review-only routes until an awake operator explicitly arms a local machine and confirms venue/consent/privacy rules.

## Current source packet

`POST /api/next-segment` already returns:

- `visual_spell.routing_contracts.touchdesigner.adapter = touchdesigner_contract`
- `visual_spell.routing_contracts.touchdesigner.mode = dry_run`
- `visual_spell.routing_contracts.touchdesigner.route = manual_operator_copy_to_touchdesigner_or_future_twozero_mcp`
- uniforms such as `uBpm`, `uEnergy`, `uDeck`, `uPhraseLockBars`, and `uBassSwapBar`
- fail-closed flags: `starts_gpu=false`, `starts_paid_api=false`, `publishes_stream=false`, `records_audio=false`

The same payload also carries `COMFYUI_DRY_RUN` and browser fallback labels so the presenter can distinguish running local visuals from future adapter contracts.

## Suggested TouchDesigner network shape

Future local network name: `/project1/sonicforge_visual_spell`

Recommended operator families:

- `DAT` for incoming JSON cue packets and readable text overlays.
- `CHOP` for BPM, energy, phrase-lock bars, bass-swap bar, EQ LOW/MID/HIGH metadata, and future audio-reactive values.
- `TOP` for code rain, dual ASCII spectrograph, subtitle spell, survival ping, and final output.
- `windowCOMP` only when the operator intentionally opens a local show window.

Suggested logical chain, still dry-run until implemented:

```text
visual_spell_json DAT
  -> select/parse DAT callbacks
  -> constants CHOP: uBpm, uEnergy, uDeck, uPhraseLockBars, uBassSwapBar
  -> text TOP overlays: PHRASE_LOCK / BASS_SWAP / SURVIVAL_PING
  -> GLSL/code-rain TOP or browser-source TOP
  -> null TOP: sonicforge_out
  -> optional Spout/Syphon/OBS capture only after human approval
```

## twozero MCP guardrails

If a future approved session uses twozero MCP, follow these rules from the TouchDesigner MCP workflow:

1. Call `td_get_hints` before building a network.
2. Call `td_get_par_info` for each operator type before setting parameters. Never guess TouchDesigner 2025.32 parameter names.
3. If `tdAttributeError` appears, stop and inspect the node with `td_get_operator_info` before continuing.
4. Split cleanup and creation into separate MCP calls; do not destroy and recreate same-named nodes in one script.
5. Prefer native MCP tools (`td_create_operator`, `td_set_operator_pars`, `td_get_errors`) over arbitrary `td_execute_python`.
6. Use relative paths in callbacks (`me.parent()` / `scriptOp.parent()`), not hardcoded local absolute paths.
7. Verify with `td_get_errors`, `td_get_perf`, and `td_get_screenshot` before any window/output/recording step.

No unattended cron run may connect to `TOUCHDESIGNER_MCP_URL`, send MCP commands, open show windows, start MovieFileOut recording, or bridge Spout/Syphon.

## Spout / Syphon / OBS route notes

Spout/Syphon is a local video-sharing lane, not a publishing lane by itself. It still needs approval because it can expose private room visuals, faces, names, or venue information if routed into OBS/projectors.

Manual approval checklist before local routing:

- Confirm the output is test/demo art only and contains no private photos, names, addresses, phone numbers, stream keys, or recordings.
- Keep `records_audio=false` and no MovieFileOut recording unless a human explicitly approves a renderer/recording test.
- Confirm `publishes_stream=false`; OBS may preview locally, but RTMP/SRT/WHIP stays disabled.
- Use browser `/visualizer` as fallback if TouchDesigner FPS is 0, output is black, or cue parsing fails.
- Keep Rave Survival Kit copy practical: hydration, earplugs, buddy checks, chill-zone/exits. Do not add medical, legal, or drug-use instructions.

## Visual spell field mapping

| SonicForge field | TouchDesigner use | Safe note |
| --- | --- | --- |
| `text` | Text TOP / DAT overlay | Readable captions only |
| `bpm` | `uBpm` uniform / CHOP channel | Metadata; no beat detector claimed |
| `energy` | `uEnergy` uniform / intensity | Deterministic planner value |
| `deck` | `uDeck` uniform / A-B HUD label | Deck B usually incoming/dry-run |
| `phrase_lock_bars` | `uPhraseLockBars` | Planned phrase metadata |
| `bass_swap_bar` | `uBassSwapBar` | Planned EQ handoff metadata |
| `survival_kit.visual_spell` | `SURVIVAL_PING` overlay | Community-care reminder only |
| `culture_cue.short_message` | Lineage caption | Respectful context, not scene authority |

## Failure handling

- Missing MCP server: keep `TOUCHDESIGNER_MCP_URL` unset or pointed at localhost only; continue with browser `/visualizer`.
- Black TD output: check shader errors, inputs, FPS, and TOP resolution before display.
- Wrong parameter name: stop, inspect with `td_get_par_info` / `td_get_operator_info`; do not guess.
- Spout/Syphon not visible in OBS/Resolume: keep route disabled, use browser source capture.
- Any accidental recording/streaming risk: stop output, close routing, leave `records_audio=false` and `publishes_stream=false`.

## Acceptance checks

- This doc includes `dry_run_operator_armed_only`, `TOUCHDESIGNER_MCP_URL`, `manual_operator_copy_to_touchdesigner_or_future_twozero_mcp`, `Spout`, `Syphon`, `td_get_par_info`, `td_get_errors`, and the fail-closed flags.
- `scripts/verify.py` requires this doc and the key guardrail strings.
- `/api/next-segment` remains the only source of TouchDesigner cue metadata, and it stays dry-run.
- No live MCP command, GPU job, provider call, stream publish, recording, upload, purchase, training job, or cron mutation is performed by this documentation increment.
