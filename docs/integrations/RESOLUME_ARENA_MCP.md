# Resolume Arena MCP / Visual Cue Routing Contract

Updated: 2026-05-01T13:04:21Z

## Status

`dry-run / operator-armed only`

This card documents how **SonicForge Live** can hand DJ VANTA visual-spell metadata to a future local Resolume Arena operator or MCP-style bridge. It does not connect to Resolume, start any MCP server, open output windows, publish streams, record media, upload private visuals, or call ComfyUI/TouchDesigner/GPU providers by default.

Brand context: **Intergalactic DJs** is the show/collective layer, **DJ VANTA//SonicForge** is the first performer, and **SonicForge Live** is the local-first runtime/platform.

## Closed flags

```json
{
  "adapter": "resolume_contract",
  "status": "dry_run_operator_armed_only",
  "mode": "dry_run",
  "starts_gpu": false,
  "starts_paid_api": false,
  "publishes_stream": false,
  "records_audio": false,
  "uploads_private_media": false,
  "requires_human_approval": true
}
```

Operator rule: browser `/visualizer` remains the active local fallback. Resolume Arena, Spout/Syphon, OBS/RTMP, TouchDesigner, ComfyUI, and any future `RESOLUME_MCP_BASE_URL` route stay review-only until an awake operator approves local show-control work.

## Current source packet

`POST /api/next-segment` already returns a dry-run packet at `visual_spell.routing_contracts.resolume`:

```json
{
  "adapter": "resolume_contract",
  "mode": "dry_run",
  "composition": "Intergalactic DJs / DJ VANTA / Resolume dry-run",
  "layer": "Deck B Visual Spell",
  "clip_or_source": "browser_visualizer_code_rain",
  "effect": "glow_feedback_chromatic_split",
  "bpm": 124,
  "palette": ["#0b0014", "#7c3cff", "#00f5ff"],
  "text_overlay": "PHRASE_LOCK 32 // BASS_SWAP BAR_17",
  "survival_overlay": "SURVIVAL_PING hydrate / earplugs / buddy / exits / chill zone",
  "crossfader_hint": "equal_power bar 17 midpoint",
  "route": "manual_operator_copy_to_resolume_or_future_mcp",
  "starts_gpu": false,
  "starts_paid_api": false,
  "publishes_stream": false,
  "records_audio": false,
  "requires_human_approval": true
}
```

The packet is metadata only. It is safe to display in the browser UI or copy manually into operator notes; it is not an automatic Resolume control command.

## Cue packet schema

| Field | Required | Meaning | Safe handling |
| --- | --- | --- | --- |
| `adapter` | yes | Always `resolume_contract` until a real adapter is approved. | Verifier should reject any live adapter claim by default. |
| `mode` | yes | `dry_run` for cron/unattended work. | No provider or MCP call. |
| `composition` | yes | Human-readable Resolume composition target. | Example: `Intergalactic DJs / DJ VANTA / Resolume dry-run`. |
| `layer` | yes | Target layer concept such as `Deck B Visual Spell`. | Operator chooses the real layer manually. |
| `clip_or_source` | yes | Browser source / clip placeholder. | Default is `browser_visualizer_code_rain`; no media import. |
| `effect` | yes | Suggested effect stack. | Text cue only, not an OSC/MIDI command. |
| `bpm` | yes | Planner BPM for VJ sync. | Metadata; no beat detector claimed. |
| `palette` | yes | Color tokens from the visual state. | Local display only. |
| `text_overlay` | yes | Readable PHRASE_LOCK/BASS_SWAP/live spell text. | Keep readable; no private names or venue details. |
| `survival_overlay` | yes | `SURVIVAL_PING` community-care copy. | Hydration, earplugs, buddy, exits, chill zone only. |
| `crossfader_hint` | yes | Visual handoff note aligned with Deck A/B mix metadata. | Metadata-only; no video mixer automation. |
| `route` | yes | `manual_operator_copy_to_resolume_or_future_mcp`. | Manual copy or future human-approved local bridge only. |
| `starts_gpu` / `starts_paid_api` / `publishes_stream` / `records_audio` / `uploads_private_media` | yes | Fail-closed flags. | Must remain `false` in unattended runs. |
| `requires_human_approval` | yes | Approval gate. | Must remain `true` until an operator arms local Resolume testing. |

## Future local operator flow

1. Run SonicForge Live locally and open `/visualizer`.
2. In Resolume Arena, add a browser/source/NDI/Spout input manually if the operator approves local VJ routing.
3. Copy the current `visual_spell.routing_contracts.resolume` packet from `/api/next-segment` into the operator notes or a future local bridge.
4. Match the Resolume composition/layer/clip/effect fields manually.
5. Keep OBS/RTMP publishing disabled unless a separate public-stream approval exists.

Future env var names only:

```bash
RESOLUME_MCP_BASE_URL=http://127.0.0.1:40440
RESOLUME_ENABLE_MCP=false
RESOLUME_ENABLE_OSC=false
RESOLUME_ENABLE_OUTPUT_RECORDING=false
RTMP_ENABLE_PUBLISH=false
```

Never commit real room notes, IPs for non-local machines, stream keys, venue details, private photos, or recordings.

## Blocked actions without approval

- No unattended Resolume MCP, OSC, MIDI, WebSocket, or REST commands.
- No importing private media into Resolume.
- No activating Spout/Syphon/NDI bridges into public outputs.
- No OBS/RTMP/SRT/WHIP publishing.
- No recording via Resolume, OBS, MovieFileOut, screen capture, or external recorder.
- No ComfyUI `/prompt`, RunPod, Modal, paid GPU, training, purchases, uploads, or cron mutation.

## Failure handling

- If Resolume is unavailable, keep using browser `/visualizer` as the active fallback.
- If text is unreadable, switch to the browser `subtitle_spell` / `sdf_text_fallback` lane before trying a live graphics bridge.
- If any route could reveal private room visuals, names, addresses, phone numbers, stream keys, or recordings, stop and keep the route closed.
- If `SURVIVAL_PING` copy drifts beyond practical community care, revert to hydration / earplugs / buddy / exits / chill-zone language. This is not medical/legal/drug-use advice.

## Acceptance checks

Fail-closed verifier needles: `starts_gpu: false`, `starts_paid_api: false`, `publishes_stream: false`, `records_audio: false`, `uploads_private_media: false`, and `requires_human_approval: true`.

- This doc includes `dry_run_operator_armed_only`, `RESOLUME_MCP_BASE_URL`, `RESOLUME_ENABLE_MCP=false`, `manual_operator_copy_to_resolume_or_future_mcp`, `composition`, `layer`, `clip_or_source`, `effect`, `bpm`, `palette`, `text_overlay`, `survival_overlay`, and all fail-closed flags.
- `scripts/verify.py` requires this doc and the key guardrail strings.
- `/api/next-segment` remains the source of Resolume cue metadata, and it stays `dry_run` with `requires_human_approval=true`.
- No live Resolume command, provider call, stream publish, recording, upload, purchase, training job, GPU start, or cron mutation is performed by this documentation increment.
