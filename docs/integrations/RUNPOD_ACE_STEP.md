# RunPod ACE-Step Endpoint Contract — SonicForge Live

Status: **dry-run / operator-armed only**. This document is a future integration contract for ACE-Step music generation on RunPod; it does not start pods, call endpoints, upload private media, download models, run GPUs, train models, publish streams, record audio, or purchase services.

## Purpose

SonicForge Live currently proves DJ VANTA//SonicForge with local mock WAV sketches, metadata-only mix plans, Deck A/B handoff state, prompt crate memory, MC text breaks, and browser visual spells. A future approved RunPod ACE-Step lane may generate track clips for Deck B after the control plane is already proven.

Candidate future uses:

- prompt-to-music generation for incoming Deck B segments;
- bounded stem or clip experiments for operator-reviewed house-party demos;
- offline render attempts that later feed the local program manifest renderer;
- comparison against local/mock adapters without changing the planner contract.

Default local demo behavior stays mock/dry-run. `/api/next-segment`, `/api/dj-brain/state`, `/api/backends`, the browser visualizer, crate cache, sample pads, and set manifests must remain runnable without RunPod.

## Closed flags

```yaml
starts_gpu: false
starts_paid_api: false
publishes_stream: false
records_audio: false
uploads_private_media: false
trains_models: false
purchases_services: false
starts_runpod_pod: false
calls_runpod_endpoint: false
requires_human_approval: true
```

## Environment variable names only

Use names and placeholders only. Never commit real `.env` values, RunPod keys, endpoint URLs for private projects, stream keys, generated secrets, private prompt packs, customer data, audio recordings, or reference media.

```bash
RUNPOD_ENDPOINT_URL=[REDACTED]
RUNPOD_ACE_STEP_API_URL=[REDACTED]
RUNPOD_API_KEY=***
RUNPOD_ENABLE_POD_START=false
RUNPOD_ENABLE_ENDPOINT_CALL=false
RUNPOD_MAX_SECONDS=0
RUNPOD_MAX_JOBS=0
ACE_STEP_MODEL_ID=[REDACTED]
ACE_STEP_ENABLE_GENERATION=false
SONICFORGE_ALLOW_GPU=false
SONICFORGE_ALLOW_PAID_API=false
SONICFORGE_ALLOW_PRIVATE_UPLOAD=false
SONICFORGE_ALLOW_RECORDING=false
SONICFORGE_REQUIRE_HUMAN_APPROVAL=true
```

## Required human approval question

Before any live RunPod or ACE-Step call, ask the awake operator:

> Do you approve this exact RunPod ACE-Step lane, endpoint URL, pod/start policy, budget/time limit, prompt, input files, output destination, and shutdown/verification plan for one bounded generation run?

Silence, enthusiasm, task-board priority, hackathon pressure, or prior general approval is not approval for a specific RunPod run.

## Blocked without approval

The following actions remain blocked until the operator says yes for one exact run:

- starting, resuming, renting, or modifying a RunPod pod;
- calling a RunPod serverless endpoint or ACE-Step API;
- uploading private media, recordings, reference images, datasets, prompts, or secrets;
- downloading model weights or custom nodes as part of an unattended cron run;
- training/fine-tuning models;
- recording, stitching, or publishing program audio as if it were a verified live mix;
- generating public assets meant for publishing;
- leaving pods, workers, queues, volumes, or paid tasks running after the demo;
- mutating cron jobs or creating recursive schedules.

## Normalized dry-run input

```json
{
  "lane": "runpod_ace_step_audio",
  "mode": "dry_run_contract_only",
  "endpoint_env": "RUNPOD_ENDPOINT_URL",
  "ace_step_api_env": "RUNPOD_ACE_STEP_API_URL",
  "api_key_env": "RUNPOD_API_KEY",
  "task": "deck_b_track_clip_generation",
  "segment_id": "seg-001",
  "deck": "B",
  "prompt_stack": [
    "Selected local crate id: pnw-warehouse-warmup",
    "warmup disco-house-techno handoff",
    "community-care reminder only"
  ],
  "bpm": 124,
  "key_hint": "A minor",
  "duration_seconds": 30,
  "output_destination": "generated/audio/runpod-dry-run-placeholder.wav",
  "input_files": [],
  "max_seconds": 0,
  "max_jobs": 0,
  "requires_human_approval": true,
  "starts_gpu": false,
  "starts_paid_api": false,
  "publishes_stream": false,
  "records_audio": false,
  "uploads_private_media": false
}
```

## Normalized disabled output

```json
{
  "ok": true,
  "status": "runpod_ace_step_dry_run_no_pod_started_no_endpoint_called",
  "adapter": "RunPodAceStepAdapter contract",
  "pod_started": false,
  "endpoint_called": false,
  "job_id": null,
  "files": [],
  "warnings": [
    "RunPod ACE-Step is closed until explicit human approval.",
    "RUNPOD_ENABLE_POD_START=false, RUNPOD_ENABLE_ENDPOINT_CALL=false, and RUNPOD_MAX_JOBS=0 prevent unattended GPU work."
  ],
  "starts_gpu": false,
  "starts_paid_api": false,
  "publishes_stream": false,
  "records_audio": false,
  "uploads_private_media": false,
  "trains_models": false,
  "purchases_services": false,
  "requires_human_approval": true
}
```

## Future safe preflight after approval

Only after approval, a bounded operator run may verify local configuration without exposing secrets:

```bash
python - <<'PY'
import os
for name in [
    'RUNPOD_ENDPOINT_URL',
    'RUNPOD_ACE_STEP_API_URL',
    'RUNPOD_API_KEY',
    'RUNPOD_ENABLE_POD_START',
    'RUNPOD_ENABLE_ENDPOINT_CALL',
    'RUNPOD_MAX_SECONDS',
    'RUNPOD_MAX_JOBS',
    'ACE_STEP_ENABLE_GENERATION',
]:
    value = os.getenv(name, '')
    if 'KEY' in name or 'TOKEN' in name or 'SECRET' in name:
        print(f'{name} set:', bool(value))
    else:
        print(f'{name}:', value or '<unset>')
PY
```

Do not print API key values. If any approval variable is missing, false, or unbounded, stop before network calls.

## SonicForge integration shape

When implemented, RunPod ACE-Step should remain a swappable adapter behind the existing planner contracts:

- lane: `runpod_ace_step_audio`;
- adapter: `RunPodAceStepAdapter contract` until implemented;
- default state: `closed_until_human_yes`;
- first safe action: review this contract and `.env.example` variable names;
- planner input: Deck B prompt stack, BPM, key hint, duration, energy, crate id, and safety notes;
- planner output: local file path only after verified generation, never a public URL by default;
- backend-status card: show approval question, blocked action list, and env var names only;
- manifest integration: record generated clip metadata separately from `rendered_program_mix` until a continuous mixer is verified;
- verification: job count returns to `0`, pod/worker is stopped, generated outputs are local-only unless explicitly approved.

## Safety copy for UI/docs

Use this visible copy near any RunPod or ACE-Step control:

> RunPod ACE-Step is a future music-generation lane. It is closed by default: no pod start, no endpoint call, no GPU, no paid job, no private upload, no recording, no stream, and no training starts without an awake human approving the exact endpoint, budget, prompt/input files, output path, and shutdown check.

## Acceptance checks

- This file exists at `docs/integrations/RUNPOD_ACE_STEP.md`.
- `.env.example` includes `RUNPOD_ENDPOINT_URL`, `RUNPOD_API_KEY`, `RUNPOD_ENABLE_POD_START=false`, and ACE-Step variable names.
- The aggregate verifier checks this doc for `dry-run / operator-armed only`, `RUNPOD_ENABLE_POD_START=false`, `RUNPOD_MAX_JOBS=0`, `runpod_ace_step_dry_run_no_pod_started_no_endpoint_called`, `closed_until_human_yes`, and all fail-closed flags.
- No RunPod pod, ACE-Step endpoint, cloud GPU, paid job, training, upload, recording, stream, cron mutation, or provider call is started by default.
