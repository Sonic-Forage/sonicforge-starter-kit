---
name: sonicforge-live-dj-vanta
description: Run, verify, demo, and safely improve SonicForge Live / Intergalactic DJs / DJ VANTA as a local-first Hermes-native autonomous AI DJ/VJ control plane.
version: 0.1.0
metadata:
  hermes:
    tags: [sonicforge, dj-vanta, autonomous-dj, vj, realtime-audio, comfyui, touchdesigner, resolume, hackathon, local-first]
    status: draft_repo_local_skill
---

# SonicForge Live / DJ VANTA Operator Skill

Use this repo-local draft skill when a future Hermes agent needs to operate or improve **Intergalactic DJs presents DJ VANTA, powered by SonicForge Live**.

Public sentence:

> Intergalactic DJs presents DJ VANTA, powered by SonicForge Live: the first Hermes-native autonomous AI DJ/VJ for local house parties, livestreams, clubs, and future festival stages.

## Identity contract

- **SonicForge Live** = platform/runtime/app.
- **Intergalactic DJs** = party/show/collective layer.
- **DJ VANTA//SonicForge** = first autonomous performer/entity.
- **VANTA** = Virtual Autonomous Nocturnal Transmission Artist.
- Hermes is the permanent home for memory, skills, cron-safe verification, build journaling, and approval gates.
- SonicForge Live is the local runtime/control deck.

## Trigger conditions

Load this skill when the user asks to:

1. Run, verify, or demo SonicForge Live / DJ VANTA.
2. Continue an unattended local build increment for the hackathon project.
3. Add or inspect the DJ brain: Deck A/B handoff, equal-power crossfader, phrase plans, EQ moves, crate cache, set manifest, timeline, or mock program-status lanes.
4. Work on Rave Survival Kit, harm-reduction/community-care copy, lineage/culture cues, or text-first MC breaks.
5. Prepare dry-run backend contracts for ComfyUI, RunPod/ACE-Step, Modal, TouchDesigner/twozero, Resolume, OBS/RTMP, or TTS.
6. Package a private demo handoff without public launch side effects.

## Hard safety gates

Default state: `closed_until_human_yes` and `mock/local/dry_run`.

Do **not** do these unattended:

- create, modify, remove, or recursively schedule cron jobs;
- start paid GPU/cloud jobs, RunPod pods, Modal GPU tasks, Comfy Cloud jobs, or ComfyUI `/prompt` calls;
- call Gemini/Lyria, ACE-Step, TTS, voice-cloning, livestream, OBS/RTMP, SRT, WHIP, Resolume, TouchDesigner MCP, or provider endpoints unless an awake human explicitly approves the exact lane;
- publish public posts/submissions, collect payments, purchase services, upload private media/datasets/prompts/recordings/model weights, train/fine-tune models, or print/copy secrets;
- Do not read, print, or commit `/opt/data/.env` values.

Approval phrase shape before any external lane:

```text
I approve <lane> for SonicForge Live.
Provider/endpoint: <exact endpoint>
Max spend/time: <limit>
Destination: <private/public/local>
Stop condition: <condition>
```

If approval is missing or ambiguous, keep the lane closed.

## Required preflight for build runs

From `/opt/data/workspace/projects/sonicforge-live`:

```bash
date -Is
git status --short --branch
```

Read these before choosing work:

- `AGENTS.md`
- `docs/brand/NAMING_AND_POSITIONING.md`
- `docs/OVERNIGHT_AGENTIC_BUILD_PLAN.md`
- `automation/OVERNIGHT_SAFETY_LEDGER.md`
- `docs/planning/OVERNIGHT_TASK_BOARD.md`
- `docs/features/RAVE_SURVIVAL_KIT.md`
- `docs/features/HARM_REDUCTION_GUIDE.md`
- `docs/culture/RAVE_DJ_HISTORY_GUIDE.md`
- `docs/visuals/TEXT_SHADER_VISUAL_SPELLS.md`
- `docs/inspiration/CARELESS_LIVEDJ_INTAKE.md`
- `docs/comfyui/INTERGALACTIC_VISUAL_SPELL_WORKFLOW.md`
- `docs/integrations/*.md`

Pick exactly one unchecked task-board item or one highest-impact safe gap. Mark a checkbox complete only after files and verification exist.

## Local launch commands

Operator quickstart — local-only, no provider lanes:

```bash
cd /opt/data/workspace/projects/sonicforge-live
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn server.main:app --host 127.0.0.1 --port 8788
```

Open:

- Control deck: `http://127.0.0.1:8788/`
- Browser VJ window: `http://127.0.0.1:8788/visualizer`
- Health: `http://127.0.0.1:8788/health`
- Backend status: `http://127.0.0.1:8788/api/backends`
- Demo timeline: `http://127.0.0.1:8788/api/timeline`

CLI proof commands for an awake operator or judge:

```bash
curl -fsS http://127.0.0.1:8788/health
curl -fsS http://127.0.0.1:8788/api/backends
curl -fsS http://127.0.0.1:8788/api/crate-cache
curl -fsS -X POST http://127.0.0.1:8788/api/next-segment
curl -fsS -X POST http://127.0.0.1:8788/api/sample-pad \
  -H 'Content-Type: application/json' \
  -d '{"pad":"HYDRATE"}'
```

Expected proof highlights:

- `/health` stays fail-closed: `starts_gpu=false`, `starts_paid_api=false`, `publishes_stream=false`, `records_audio=false`, `uploads_private_media=false`.
- `/api/next-segment` includes Deck A/B handoff, `survival_kit`, `culture_cue`, equal-power crossfader metadata, `comfyui_visual_spell.mode=dry_run`, and mock/local artifact paths only.
- `/api/sample-pad` returns `metadata_only_no_audio_playback` and never starts recording, audio playback, GPU, provider calls, or stream publishing.

## Verification commands

Run at least this stack after changes:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_survival_harm_reduction.py
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile $(git ls-files '*.py')
node --check app/static/main.js
git diff --check
```

For app/API changes, also run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/smoke_local_demo.py
```

Important pitfall: endpoint smoke tests can mutate tracked generated set/timeline sidecars. After smoke tests, run `git status --short`; revert smoke-generated sidecars unless the increment intentionally updates them.

## 90-second demo script

1. Say the public sentence.
2. Show `/health` and call out `starts_gpu=false`, `starts_paid_api=false`, `publishes_stream=false`, `records_audio=false`, and `uploads_private_media=false`.
3. Click **Plan Next Continuous Segment** or call `POST /api/next-segment`.
4. Point to:
   - Deck A / Deck B handoff cards;
   - equal-power crossfader formula and representative gain points;
   - prompt/crate cache and repetition guard;
   - text-first MC break generator;
   - `survival_kit` and `culture_cue` fields;
   - dry-run `comfyui_visual_spell` cue;
   - program-audio truth panel showing no rendered continuous mix yet.
5. Open `/visualizer` and show browser-first code rain, EQ bands, subtitle spell, SDF/MSDF fallback, and dual ASCII spectrograph.
6. Show `/api/backends`: ComfyUI, RunPod/ACE-Step, Modal, TouchDesigner, Resolume, OBS/RTMP, and TTS remain dry-run approval contracts.
7. Close: **DJ VANTA can keep the set moving locally today; heavier media engines are operator-armed adapters tomorrow.**

## API map

Safe/read-only preview:

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

- `POST /api/next-segment` — local segment planning and metadata manifest append.
- `POST /api/sample-pad` — metadata-only ritual cue; no real sample playback or recording.
- `POST /api/timeline/build` — rebuild local dry-run timeline; no live scheduler.
- `POST /api/generate-track` — mock WAV sketch only unless a human arms a real adapter.
- `POST /api/talk-break` — text-first talk cue only unless TTS is explicitly armed.

## Backend contract map

| Lane | State | First safe action | Human gate |
|---|---|---|---|
| Browser visualizer | active local fallback | open `/visualizer`; no GPU/cloud required | none |
| ComfyUI visual spells | dry-run cue only | inspect `docs/integrations/COMFYUI_API.md` and `comfyui_visual_spell` payload | approval before `/prompt`; `COMFYUI_ENABLE_PROMPT=false` stays default |
| RunPod / ACE-Step | dry-run contract | inspect `docs/integrations/RUNPOD_ACE_STEP.md` | approval before pod/endpoint call; `RUNPOD_ENABLE_POD_START=false` and `ACE_STEP_ENABLE_GENERATION=false` stay default |
| Modal | dry-run contract | inspect `docs/integrations/MODAL_ENDPOINT.md` | approval before GPU/serverless call; `MODAL_ENABLE_GPU=false` stays default |
| TouchDesigner/twozero | dry-run routing card | browser fallback and manual cue copy | approval before MCP commands/show windows/recording; use `td_get_par_info` before live parameter changes |
| Resolume Arena MCP | dry-run routing card | browser fallback and manual cue copy | approval before MCP/OSC/MIDI/WebSocket commands; no private media imports |
| OBS/RTMP | local capture plan only | manual OBS browser-source setup | approval before stream publish; `RTMP_ENABLE_PUBLISH=false` stays default |
| TTS/voice | `mock-text-talk-break` | render text only | approval before audio output, voice cloning, uploads, or voice messages; `TTS_ENABLE_AUDIO_OUTPUT=false` stays default |

## Rave Survival Kit and culture rules

Runtime copy must stay practical community care only:

- hydration/water station;
- earplugs/listening breaks;
- buddy checks;
- consent and floor etiquette;
- exits and clear paths;
- chill zone/decompression;
- human override and sober operator.

Forbidden runtime outputs:

- medical diagnosis or treatment;
- emergency-service substitution;
- dosing, drug identification, ingestion instructions, or drug-use advice;
- claims that AI invented or replaces DJ/rave culture.

Use respectful lineage language: AI is a guest entering a culture built by people.

## Future Hermes agent self-test instructions

Use this self-test before claiming a SonicForge Live increment is demo-safe. It is intentionally local-only and should not call ComfyUI `/prompt`, RunPod, Modal, TouchDesigner/twozero, Resolume, OBS/RTMP, TTS, or any paid provider.

1. **Identity and safety preflight**
   - Confirm `git status --short --branch` is understood before editing.
   - Re-read `AGENTS.md`, this skill, `docs/planning/OVERNIGHT_TASK_BOARD.md`, and the relevant feature/integration docs for the chosen task.
   - Confirm the planned change does not create/modify cron jobs, read `/opt/data/.env`, publish, upload private media, start GPUs/providers, record audio, or open live streams.

2. **Static contract self-test**
   - Run `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify.py`.
   - Run any targeted verifier for the touched lane, e.g. `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_survival_harm_reduction.py` for Rave Survival Kit/community-care work.
   - Run `node --check app/static/main.js` when browser UI changed.
   - Run `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile $(git ls-files '*.py')` when Python changed.

3. **Runtime smoke self-test for API/UI changes**
   - Run `PYTHONDONTWRITEBYTECODE=1 python3 scripts/smoke_local_demo.py`.
   - Confirm `/health` still reports `starts_gpu=false`, `starts_paid_api=false`, `publishes_stream=false`, `records_audio=false`, and `uploads_private_media=false`.
   - Confirm `POST /api/next-segment` still includes Deck A/B, `survival_kit`, `culture_cue`, `mc_break`, equal-power crossfader metadata, `program_status`, and dry-run `comfyui_visual_spell` without provider output files.

4. **Generated sidecar hygiene**
   - After smoke tests, run `git status --short`.
   - If `generated/sets/...` or `generated/timeline/demo-set.json` changed only because of smoke, revert those sidecars unless the selected task intentionally updates them.
   - Run `git diff --check` after reverting or intentionally accepting generated changes.

5. **Commit readiness self-test**
   - The task-board checkbox may be marked complete only after real files exist and the verifier stack passes.
   - Journal the increment in `logs/overnight-build-journal.md` with files changed, verification, blockers, safety notes, and next recommended increment.
   - Commit only if the repo is not broken; otherwise leave changes uncommitted and document the blocker.

## Common safe increments

- Add or improve UI panels for already-existing payload fields.
- Add deterministic metadata contracts before real audio/video/provider lanes.
- Add docs-only integration cards with env var names and `[REDACTED]` placeholders.
- Add verifier assertions for fail-closed flags and UI/API strings.
- Add local manifest/run-sheet artifacts that do not publish, record, upload, or start providers.

## Final report template

```text
Increment: <one concrete task>
Files changed: <paths>
Verification: <commands + pass/fail>
Safety: no cron changes, no providers/GPU/RTMP/public actions, no secrets read/copied
Commit: <hash or not committed because ...>
Next recommended increment: <one safe task>
```
