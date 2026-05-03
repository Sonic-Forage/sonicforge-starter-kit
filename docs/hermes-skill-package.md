# Hermes Skill Package — sonicforge-live-dj-vanta

Status: **draft export guide / local-first operator skill**.

Purpose: make SonicForge Live reusable as a future Hermes skill/entity so an operator can launch, verify, demo, and safely improve **Intergalactic DJs presents DJ VANTA, powered by SonicForge Live** from a fresh Hermes session.

Public sentence:

> Intergalactic DJs presents DJ VANTA, powered by SonicForge Live: the first Hermes-native autonomous AI DJ/VJ for local house parties, livestreams, clubs, and future festival stages.

## Identity contract

- **SonicForge Live** = platform/runtime/app.
- **Intergalactic DJs** = party/show/collective layer.
- **DJ VANTA//SonicForge** = first autonomous performer/entity.
- **VANTA** = Virtual Autonomous Nocturnal Transmission Artist.
- Operator promise: Hermes is the permanent home for memory, skills, scheduled local verification, safety gates, and handoff artifacts; SonicForge Live is the local runtime/control deck.

## Trigger conditions for the future skill

Use the future `sonicforge-live-dj-vanta` skill when the user asks Hermes to:

1. Run or demo SonicForge Live / DJ VANTA.
2. Package an Intergalactic DJs hackathon/private-demo handoff.
3. Add safe local autonomous DJ/VJ increments: planner, timeline, crate cache, text-first MC breaks, visual spells, Rave Survival Kit, or static operator docs.
4. Prepare approval-gated backend lanes for ComfyUI, RunPod/ACE-Step, Modal, TouchDesigner, Resolume, OBS/RTMP, or TTS without starting them.
5. Explain why the project is Hermes-native and how it becomes a reusable autonomous performer.

## Safety gates — closed until human yes

Default adapter mode: `mock/local/dry_run`.

Never do these unattended:

- start paid GPU/cloud jobs;
- start RunPod pods or Modal GPU tasks;
- call Comfy Cloud or submit ComfyUI `/prompt` jobs;
- publish OBS/RTMP/SRT/WHIP streams;
- post publicly, submit to a public site, purchase services, or collect payments;
- upload private media, datasets, prompts, recordings, model weights, or secrets;
- train/fine-tune models;
- clone voices or send voice messages;
- create, edit, or delete cron jobs from inside a run.

Required human approval phrase shape before any external lane:

```text
I approve <lane> for SonicForge Live.
Provider/endpoint: <exact endpoint>
Max spend/time: <limit>
Destination: <private/public/local>
Stop condition: <condition>
```

If approval is missing or ambiguous, keep the lane `closed_until_human_yes`.

## Environment variables — names only

Use `.env.example` as the public contract. Do not read, print, or commit `/opt/data/.env` values.

Important names:

- `SONICFORGE_ALLOW_GPU=false`
- `SONICFORGE_ALLOW_PAID_API=false`
- `SONICFORGE_ALLOW_PUBLIC_STREAM=false`
- `SONICFORGE_REQUIRE_HUMAN_APPROVAL=true`
- `COMFYUI_BASE_URL=http://127.0.0.1:8188`
- `COMFYUI_ENABLE_PROMPT=false`
- `RUNPOD_ENDPOINT_URL=[REDACTED]`
- `RUNPOD_ENABLE_POD_START=false`
- `MODAL_SONICFORGE_ENDPOINT_URL=[REDACTED]`
- `TOUCHDESIGNER_MCP_URL=http://127.0.0.1:40404/mcp`
- `RESOLUME_MCP_BASE_URL=[REDACTED]`
- `RTMP_ENABLE_PUBLISH=false`
- `TTS_ENABLE_AUDIO_OUTPUT=false`
- `SONICFORGE_ALLOW_VOICE_CLONING=false`

## Local launch and verification commands

From repo root `/opt/data/workspace/projects/sonicforge-live`:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_survival_harm_reduction.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/smoke_local_demo.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_demo_timeline.py
uvicorn server.main:app --host 127.0.0.1 --port 8788
```

Open:

- Control deck: `http://127.0.0.1:8788/`
- Browser VJ window: `http://127.0.0.1:8788/visualizer`
- Health: `http://127.0.0.1:8788/health`
- Backend contract status: `http://127.0.0.1:8788/api/backends`
- Demo timeline: `http://127.0.0.1:8788/api/timeline`

## Demo script — 90 seconds

1. Say the public sentence and explain that Hermes is operating a persistent local performer, not just generating a track.
2. Run or show `/health`; call out `starts_gpu=false`, `starts_paid_api=false`, and `publishes_stream=false`.
3. Click **Plan Next Continuous Segment** or run `POST /api/next-segment`.
4. Point to the live payload/UI cards:
   - Deck A / Deck B handoff;
   - equal-power crossfader and EQ move schedule;
   - prompt/crate cache selection;
   - text-first MC break;
   - `survival_kit` and `culture_cue`;
   - dry-run ComfyUI visual-spell cue;
   - program-audio truth panel.
5. Open `/visualizer` and show browser-first visual spells: code rain, EQ bands, subtitle spell, SDF/MSDF fallback, dual ASCII spectrograph.
6. Open `/api/backends` or the backend status UI card and explain that ComfyUI, RunPod, Modal, TouchDesigner, Resolume, OBS/RTMP, and TTS lanes are explicit approval contracts.
7. Close with: **DJ VANTA can keep the set moving locally today; heavier media engines are operator-armed adapters tomorrow.**

## API endpoints the future skill should know

Read-only / safe preview:

- `GET /health`
- `GET /api/state`
- `GET /api/dj-brain/state`
- `GET /api/crate-cache`
- `GET /api/set-manifest`
- `GET /api/program-status`
- `GET /api/program-manifest`
- `GET /api/backends`
- `GET /api/mc-breaks/preview`
- `GET /api/timeline`

Local metadata/mock actions:

- `POST /api/next-segment` — appends local set manifest metadata and returns track/talk/visual/mix/transition/deck/care/culture payloads.
- `POST /api/sample-pad` — metadata-only sample-pad ritual cue; no real sample playback or recording.
- `POST /api/timeline/build` — rebuilds local dry-run timeline; no scheduler, no generation, no continuous mixer.
- `POST /api/generate-track` — mock WAV sketch only unless a human arms a real adapter.
- `POST /api/talk-break` — text-first talk cue only unless TTS is explicitly armed.

## Backend contract map

| Lane | Current state | First safe action | Approval gate |
|---|---|---|---|
| Browser visualizer | active local fallback | open `/visualizer` | none |
| ComfyUI visual spells | dry-run cue only | inspect `docs/integrations/COMFYUI_API.md` and `comfyui_visual_spell` payload | explicit approval before `/prompt` |
| RunPod / ACE-Step | dry-run contract | inspect `docs/integrations/RUNPOD_ACE_STEP.md` | explicit approval before pod/endpoint call |
| Modal | dry-run contract | inspect `docs/integrations/MODAL_ENDPOINT.md` | explicit approval before GPU/serverless call |
| TouchDesigner/twozero | dry-run routing card | use browser fallback and manual cue copy | explicit approval before MCP commands/show windows/recording |
| Resolume Arena MCP | dry-run routing card | use browser fallback and manual cue copy | explicit approval before MCP/OSC/MIDI/WebSocket commands |
| OBS/RTMP | local capture plan only | open browser windows for manual OBS capture | explicit approval before public/private stream publish |
| TTS/voice | mock-text-talk-break | render text; no audio output | explicit approval before TTS audio, voice cloning, uploads, or voice messages |

## Rave Survival Kit / culture rules

Runtime copy must stay practical community care:

- hydration/water station;
- earplugs/listening breaks;
- buddy checks;
- consent and floor etiquette;
- exits and clear paths;
- chill zone/decompression;
- human override and sober operator.

Forbidden runtime outputs:

- No medical diagnosis or treatment;
- emergency-service substitution;
- dosing, drug identification, ingestion instructions, or drug-use advice;
- claims that AI invented or replaces DJ/rave culture.

Use respectful lineage language from `docs/culture/RAVE_DJ_HISTORY_GUIDE.md`: AI is a guest entering a culture built by people.

## Files to consult before future increments

- `README.md`
- `AGENTS.md`
- `docs/brand/NAMING_AND_POSITIONING.md`
- `docs/OVERNIGHT_AGENTIC_BUILD_PLAN.md`
- `automation/OVERNIGHT_SAFETY_LEDGER.md`
- `docs/planning/OVERNIGHT_TASK_BOARD.md`
- `docs/demo-runbook.md`
- `docs/house-party-mode.md`
- `docs/features/RAVE_SURVIVAL_KIT.md`
- `docs/features/HARM_REDUCTION_GUIDE.md`
- `docs/culture/RAVE_DJ_HISTORY_GUIDE.md`
- `docs/inspiration/CARELESS_LIVEDJ_INTAKE.md`
- `docs/comfyui/INTERGALACTIC_VISUAL_SPELL_WORKFLOW.md`
- `docs/integrations/*.md`
- `docs/visuals/TEXT_SHADER_VISUAL_SPELLS.md`

## Future `SKILL.md` skeleton

When installing as a real Hermes skill, copy this logic into `skills/sonicforge-live-dj-vanta/SKILL.md` with:

1. trigger conditions;
2. prerequisite repo path check;
3. mandatory safety gates;
4. exact launch/verify/demo commands;
5. common increments and verifier expectations;
6. known pitfalls: smoke tests may mutate generated set/timeline sidecars; revert them unless intentionally included;
7. final report template with commit hash, files changed, verification, blockers, and next increment.

## Acceptance checks for this package doc

A future operator can use this doc alone to:

- name the platform/show/performer correctly;
- run the local app;
- verify fail-closed behavior;
- demo DJ VANTA in 90 seconds;
- understand which backend lanes are dry-run contracts;
- avoid secrets, uploads, voice cloning, public streams, provider starts, or recursive cron changes;
- no recursive cron changes.
- preserve Rave Survival Kit and culture-cue boundaries.
