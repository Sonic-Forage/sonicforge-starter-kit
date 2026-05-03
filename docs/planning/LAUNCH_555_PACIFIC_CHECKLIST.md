# SonicForge Live — 5:55 Pacific Launch Checklist

Status: priority launch checklist for the open-source Party AI OS push.

Target call / launch checkpoint:

- Date/time: 2026-05-02 17:55 America/Los_Angeles
- Note: Los Angeles is on PDT (-0700) on this date, even if we casually say PST.
- Launch posture: open-source-ready only after the gates below pass.

## Launch thesis

SonicForge Live is the world's first forkable Party AI Operating System:

- autonomous DJ/VJ control deck,
- audio workflow lane,
- TTS / MC talk-break lane,
- ComfyUI visual workflow lane,
- browser visualizer / shader output,
- cloneable DJ agent payloads,
- party / Kandi / PLUR / Festival 2045 movement layer,
- local-first safety gates.

## What must be true before launch

### 1. Audio workflow exists and is honest

Goal: prove the system can plan or route audio segments without pretending a verified continuous mix exists.

Minimum shippable state:

- `POST /api/next-segment` returns a segment payload.
- Payload includes track/segment metadata, BPM, energy, cue points, beatmatch plan, phrase plan, EQ moves, crossfade metadata, and deck handoff.
- Program audio status explicitly distinguishes:
  - mock/planner audio,
  - generated clip audio,
  - rendered continuous program mix,
  - recording,
  - streaming.
- If no real renderer is verified, UI says so clearly.

Safe default:

- starts_gpu: false
- starts_paid_api: false
- records_audio: false
- publishes_stream: false
- uploads_private_media: false

### 2. TTS / MC workflow exists as text-first, with voice as an approved adapter

Goal: get the MC/talk-break pipeline working before forcing real audio output.

Minimum shippable state:

- A text-first MC break generator exists with modes:
  - survival
  - history
  - hype
  - lore
  - technical
- UI can preview MC break text.
- Endpoint can return the MC break payload.
- TTS adapter contract exists for future real voice output.
- Real voice output remains opt-in unless explicitly enabled.

Safe default:

- sends_voice_message: false
- voice_cloning_enabled: false
- records_audio: false
- starts_gpu: false
- starts_paid_api: false
- uploads_private_media: false

### 3. ComfyUI workflow lane exists and is fail-closed

Goal: prove SonicForge treats ComfyUI as a real workflow engine.

Minimum shippable state:

- Workflow registry exists.
- Workflow cards exist for visual-spell / poster / VJ stills.
- Model download ledger exists.
- `/api/safety-policy` blocks unsafe actions by default.
- ComfyUI API contract documents:
  - `/system_stats`
  - `/object_info`
  - `/prompt`
  - `/ws`
  - `/history/{prompt_id}`
  - `/view`
  - `/queue`
  - `/interrupt`
  - `/free`
- Real `POST /prompt` is disabled unless explicitly approved.

Safe default:

- SONICFORGE_ALLOW_COMFY_PROMPT=0
- SONICFORGE_ALLOW_MODEL_DOWNLOADS=0
- SONICFORGE_ALLOW_REMOTE_ENDPOINT=0

### 4. Endpoint / backend status is visible

Goal: demo operators can see which backend lanes are available, closed, or future.

Minimum shippable state:

- Read-only backend status endpoint or equivalent exists.
- It does not call paid/GPU/remote providers by default.
- UI shows lanes:
  - audio planner
  - TTS / MC
  - ComfyUI
  - visualizer
  - RunPod / Modal future adapters
  - TouchDesigner / Resolume future adapters
  - OBS / RTMP future adapter

Safe default:

- all external/live lanes closed until human yes.

### 5. Visualizer / ASIC-code-style visual proof exists

Goal: prove the visual/shader direction without needing a risky live graphics pipeline.

Minimum shippable state:

- `/visualizer` works as a browser-captureable VJ window.
- Visuals can render dry-run cue text like:
  - PHRASE_LOCK
  - BASS_SWAP
  - SURVIVAL_PING
  - COMFYUI_DRY_RUN
  - TOUCHDESIGNER_CONTRACT
- At least one terminal/shader/ASIC-code-inspired visual mode is visible.
- No mic recording, stream publishing, or GPU provider is started by default.

### 6. Testing gates pass

Required before public/open-source launch:

- Python compile passes.
- `scripts/verify.py` passes.
- harm-reduction verifier passes.
- `git diff --check` passes.
- focused secret scan passes.
- FastAPI route smoke passes for:
  - `/`
  - `/about`
  - `/vanta`
  - `/station`
  - `/parallel-party`
  - `/setup`
  - `/agents`
  - `/workflows`
  - `/terminal-visuals`
  - `/visualizer`
  - `/health`
  - `/api/state`
  - `/api/safety-policy`
- Any generated smoke artifacts are reverted unless intentionally committed.

### 7. Open-source release hygiene

Before making anything public:

- Remove/avoid secrets, private tokens, private URLs, private logs.
- Keep `.env` out of git.
- Add or verify `.env.example` only uses variable names/placeholders.
- Add clear README launch flow.
- Add safety/approval section.
- Add license decision.
- Add screenshots/banner assets.
- Confirm generated assets are okay to include.
- Rotate/revoke any pasted tokens from prior chat history.

## Recommended build order before the 5:55 call

1. Text-first MC / TTS adapter contract.
2. Audio truth/status endpoint and UI card.
3. Backend status endpoint and UI card.
4. Visualizer proof pass: ASIC-code / terminal shader style.
5. ComfyUI integration doc/card polish.
6. README open-source launch pass.
7. Final verification matrix.
8. Release decision: public repo / package / demo link.

## Demo story for the call

1. Open SonicForge Live.
2. Show Party AI OS banner and hub.
3. Click Station Signal.
4. Acquire dry-run station signal.
5. Generate next segment / show DJ brain metadata.
6. Show MC break text-first output.
7. Show visualizer reacting to cue packet / visual spell.
8. Show backend status: everything dangerous is closed by default.
9. Show setup/workflows/agents pages proving forkability.
10. Explain: DJ VANTA is the first clone; the product is the forkable station factory.

## Launch line

The elite AI party is invite-only. The builder party is forkable.

SonicForge Live is the world's first forkable Party AI Operating System.
