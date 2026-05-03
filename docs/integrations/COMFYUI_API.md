# ComfyUI API Integration Contract — SonicForge Live

Status: **dry-run / operator-armed only**.

SonicForge Live treats ComfyUI as a future local visual/media workflow engine for Intergalactic DJs and DJ VANTA//SonicForge. This document is the exact integration recipe for deck art, readable visual spells, Rave Survival Kit QR posters, and future VJ loops **without starting ComfyUI, Comfy Cloud, GPUs, paid APIs, or public streams by default**.

## Safety posture

Default state:

```json
{
  "starts_gpu": false,
  "starts_paid_api": false,
  "publishes_stream": false,
  "records_audio": false,
  "uploads_private_media": false,
  "mode": "dry_run",
  "requires_human_approval": true
}
```

Operator rule: a human must explicitly set local endpoint configuration, verify the workflow, and approve a single lane before `/prompt` is called. Silence, enthusiasm, or a task-board checkbox is not approval.

Do not commit:

- API keys, Hugging Face tokens, private prompts, `.env`, reference photos, venue media, generated batches, model weights, or stream keys.
- Real output folders from ComfyUI unless a tiny demo artifact is intentionally selected and reviewed.

## Environment variables

`.env.example` may contain variable names and harmless defaults only:

```bash
COMFYUI_BASE_URL=http://127.0.0.1:8188
SONICFORGE_ALLOW_GPU=false
SONICFORGE_ALLOW_PAID_API=false
SONICFORGE_ALLOW_PUBLIC_STREAM=false
```

A real `.env` stays local and uncommitted. Never print secret values in logs or reports.

## Route map

When a human approves a local ComfyUI connection, the adapter should use these routes:

| Route | Method | SonicForge use |
|---|---:|---|
| `/system_stats` | GET | Verify local server health, Python/device info, and whether the operator is on CPU/GPU. |
| `/object_info` | GET | Confirm required nodes/workflows exist before submitting anything. |
| `/prompt` | GET | Inspect queue/status without submitting work. |
| `/prompt` | POST | Submit workflow JSON only after explicit approval. |
| `/ws?clientId=<uuid>` | WebSocket | Listen for execution progress and completion. |
| `/history/{prompt_id}` | GET | Fetch output metadata after completion. |
| `/view?filename=...&subfolder=...&type=output` | GET | Download approved output files. |
| `/queue` | GET/POST | Inspect or clear queue if a job is stuck. |
| `/interrupt` | POST | Stop a running workflow when needed. |
| `/free` | POST | Unload models/free memory after a bounded test. |

## Local preflight — read-only first

Use these commands only after the operator says a local ComfyUI server is expected:

```bash
export COMFYUI_BASE_URL="${COMFYUI_BASE_URL:-http://127.0.0.1:8188}"
curl -fsS "$COMFYUI_BASE_URL/system_stats"
curl -fsS "$COMFYUI_BASE_URL/object_info" >/tmp/sonicforge-comfy-object-info.json
```

If either command fails, keep SonicForge in `COMFYUI_DRY_RUN` mode and do not submit `/prompt`.

## Normalized visual-spell input

This is the payload SonicForge planners should build. It mirrors the existing dry-run `comfyui_visual_spell` contract returned by `/api/next-segment`.

```json
{
  "workflow": "intergalactic-djs-visual-spell",
  "mode": "dry_run",
  "deck": "B",
  "segment_id": "seg-004",
  "set_id": "vantarave-autopilot-session",
  "prompt": "readable neon typography, dual ASCII spectrograph portal, DJ VANTA signal, words PHRASE LOCK 32, underground rave flyer energy, black paper, cyan and magenta glow",
  "negative_prompt": "illegible typography, watermark, copied logos, medical claims, unsafe drug-use instruction",
  "width": 1024,
  "height": 1024,
  "seed": 1776,
  "reference_images": [],
  "output_prefix": "vanta_visual_spell_seg004",
  "requires_human_approval": true,
  "starts_gpu": false,
  "starts_paid_api": false,
  "publishes_stream": false
}
```

## Normalized output

Dry-run output before approval:

```json
{
  "ok": true,
  "mode": "dry_run",
  "workflow": "intergalactic-djs-visual-spell",
  "prompt_id": null,
  "files": [],
  "warnings": ["ComfyUI /prompt not called unless explicitly enabled"]
}
```

Approved local output after a bounded run:

```json
{
  "ok": true,
  "mode": "local_operator_approved",
  "workflow": "intergalactic-djs-visual-spell",
  "prompt_id": "<comfyui-prompt-id>",
  "files": ["generated/comfyui/<reviewed-file>.png"],
  "elapsed_seconds": 0.0,
  "warnings": []
}
```

## Workflow lanes

### 1. Deck art

- Input: Deck A/B prompt stack, BPM, key, energy, culture cue, and selected crate.
- Output: still image for deck cards or OBS overlay.
- Must preserve: original SonicForge / Intergalactic DJs / DJ VANTA identity; no copied Careless-LiveDJ branding/assets.

### 2. Visual spells

- Input: planner strings like `PHRASE_LOCK 32 BARS`, `BASS_SWAP LOWS -> TRACK_B`, `SURVIVAL_PING HYDRATE`, and `COMFYUI_DRY_RUN`.
- Output: readable typography stills or future short loops.
- Must preserve: legibility, fail-closed flags, no surprise `/prompt`.

### 3. Rave Survival Kit QR posters

- Input: checklist and local/demo URL.
- Output: poster/card with a QR slot or a verified scannable QR artifact.
- Rule: if a real QR is needed, generate the QR programmatically and verify with OpenCV; do not ask an image model to invent QR modules.
- Harm-reduction copy remains practical community care only: hydration, hearing protection, consent, buddy check, exits, chill zone, human override. No medical claims, diagnosis, dosing, drug identification, or drug-use instructions.

### 4. Future VJ loops

- Input: segment visual spell, BPM, crowd synthetic state, EQ move, crossfader automation.
- Output: reviewed loop files or browser/OBS assets.
- Gate: human approval required before video workflows, model downloads, or GPU jobs.

## Adapter pseudo-flow

```python
# dry-run default
cue = planner_payload["comfyui_visual_spell"]
assert cue["mode"] == "dry_run"
assert cue["starts_gpu"] is False
assert cue["starts_paid_api"] is False
assert cue["publishes_stream"] is False

# approved local lane only
stats = GET(f"{COMFYUI_BASE_URL}/system_stats")
objects = GET(f"{COMFYUI_BASE_URL}/object_info")
validate_required_nodes(objects, workflow="intergalactic-djs-visual-spell")
prompt_id = POST(f"{COMFYUI_BASE_URL}/prompt", workflow_json)
watch_ws_until_complete(f"{COMFYUI_BASE_URL}/ws?clientId={client_id}", prompt_id)
history = GET(f"{COMFYUI_BASE_URL}/history/{prompt_id}")
files = download_outputs_with_view(history)
```

## Operator smoke test checklist

Read-only checks:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile $(git ls-files '*.py')
git diff --check
curl -fsS "$COMFYUI_BASE_URL/system_stats"
curl -fsS "$COMFYUI_BASE_URL/object_info" >/tmp/sonicforge-comfy-object-info.json
```

Local app contract checks:

```bash
python3 - <<'PY'
from server.planner import plan_next_segment
from server.schemas import SetState
seg = plan_next_segment(SetState())
cue = seg['comfyui_visual_spell']
assert cue['mode'] == 'dry_run'
assert cue['workflow'] == 'intergalactic-djs-visual-spell'
assert cue['output']['prompt_id'] is None
assert cue['output']['files'] == []
assert cue['starts_gpu'] is False
assert cue['starts_paid_api'] is False
assert cue['publishes_stream'] is False
assert '/prompt' in cue['api_routes_when_enabled']
print('COMFYUI_DRY_RUN contract ok')
PY
```

Approved `/prompt` run checks, when enabled later:

- `system_stats: OK`
- `object_info: OK`
- `prompt_id: <id>`
- WebSocket reaches completion.
- `history/{prompt_id}` contains expected output nodes.
- `/view` downloads files to a reviewed local path.
- `/queue` is empty or expected.
- No secrets/reference assets were committed.

## Failure handling

- Validation error from `/prompt`: check `/object_info` and required custom nodes/models.
- Workflow hangs: inspect `/queue`, use `/interrupt`, then `/free` if needed.
- Missing model: stop and document required model/license/VRAM; do not download large/gated models unattended.
- QR poster scan fails: regenerate QR programmatically at larger size; keep quiet zone clean; verify final composite with OpenCV.
- Text is illegible: route back to prompt card and prefer workflows/models with stronger text rendering.

## Current demo status

SonicForge Live already exposes `comfyui_visual_spell` in `/api/next-segment` as a dry-run cue. This doc makes the future local ComfyUI bridge operator-executable while keeping the hackathon demo safe: the browser visualizer remains the active local VJ surface until a human arms ComfyUI.
