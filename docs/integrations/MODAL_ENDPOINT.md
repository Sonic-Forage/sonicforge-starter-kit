# Modal Endpoint Contract — SonicForge Live

Status: **dry-run / operator-armed only**. This document is an integration contract for future Modal serverless endpoints; it does not start Modal apps, GPUs, jobs, queues, web endpoints, file uploads, training, or paid tasks.

## Purpose

SonicForge Live can eventually route bounded media or analysis work to Modal after an awake operator approves the lane. Candidate future uses:

- CPU-safe metadata utilities for demo packaging;
- bounded GPU visual/audio experiments that scale to zero;
- ComfyUI-adjacent preprocessing or postprocessing helpers;
- semantic audio/STT experiments after privacy review;
- asset validators for deck art, QR posters, or VJ loops.

Default local demo behavior stays mock/dry-run. The browser visualizer, planner, sample pads, crate cache, and set manifest writer must remain runnable without Modal.

## Closed flags

```yaml
starts_gpu: false
starts_paid_api: false
publishes_stream: false
records_audio: false
uploads_private_media: false
trains_models: false
purchases_services: false
requires_human_approval: true
```

## Environment variable names only

Use names and placeholders only. Never commit real `.env` values, API tokens, endpoint URLs for private projects, media URLs, customer data, or generated secrets.

```bash
MODAL_SONICFORGE_ENDPOINT_URL=[REDACTED]
MODAL_SONICFORGE_API_TOKEN=[REDACTED]
MODAL_ENABLE_GPU=false
MODAL_MAX_TASKS=0
SONICFORGE_ALLOW_GPU=false
SONICFORGE_ALLOW_PAID_API=false
SONICFORGE_ALLOW_PRIVATE_UPLOAD=false
SONICFORGE_REQUIRE_HUMAN_APPROVAL=true
```

## Required human approval question

Before any live Modal call, ask the awake operator:

> Do you approve this exact Modal lane, endpoint URL, task count, budget/time limit, input files, output destination, and post-run shutdown/verification plan?

Silence, enthusiasm, task-board priority, or prior general approval is not approval for a specific Modal run.

## Blocked without approval

The following actions remain blocked until the operator says yes for one exact run:

- creating or deploying a new Modal app;
- starting a GPU function or paid worker;
- calling a remote Modal endpoint;
- uploading private media, recordings, reference images, datasets, or secrets;
- training/fine-tuning models;
- generating public assets meant for publishing;
- leaving tasks running after the demo;
- mutating cron jobs or creating recursive schedules.

## Normalized dry-run input

```json
{
  "lane": "modal_serverless_gpu",
  "mode": "dry_run_contract_only",
  "endpoint_env": "MODAL_SONICFORGE_ENDPOINT_URL",
  "api_token_env": "MODAL_SONICFORGE_API_TOKEN",
  "task": "visual_spell_asset_probe",
  "segment_id": "seg-001",
  "deck": "B",
  "prompt": "DJ VANTA neon subtitle spell, readable text, browser-first fallback",
  "input_files": [],
  "max_tasks": 0,
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
  "status": "modal_dry_run_no_endpoint_called",
  "adapter": "modal_contract_only",
  "endpoint_called": false,
  "task_id": null,
  "files": [],
  "warnings": [
    "Modal endpoint is closed until explicit human approval.",
    "MODAL_ENABLE_GPU=false and MODAL_MAX_TASKS=0 prevent unattended GPU work."
  ],
  "starts_gpu": false,
  "starts_paid_api": false,
  "publishes_stream": false,
  "records_audio": false,
  "uploads_private_media": false,
  "requires_human_approval": true
}
```

## Future safe preflight after approval

Only after approval, a bounded operator run may verify the CLI and endpoint configuration without exposing secrets:

```bash
modal --version
python - <<'PY'
import os
print('MODAL_SONICFORGE_ENDPOINT_URL set:', bool(os.getenv('MODAL_SONICFORGE_ENDPOINT_URL')))
print('MODAL_ENABLE_GPU:', os.getenv('MODAL_ENABLE_GPU', 'false'))
print('MODAL_MAX_TASKS:', os.getenv('MODAL_MAX_TASKS', '0'))
PY
```

Do not print token values. If any approval variable is missing or false, stop before network calls.

## SonicForge integration shape

When implemented, Modal should be surfaced through the same backend-status card as the other future lanes:

- lane: `modal_serverless_gpu`;
- adapter: `modal_contract_only` until implemented;
- default state: `closed_until_human_yes`;
- first safe action: review this contract and `.env.example` variable names;
- blocked action list: GPU start, paid API call, private upload, training, public publishing;
- verification: task count returns to `0`, generated outputs are local-only unless explicitly approved.

## Safety copy for UI/docs

Use this visible copy near any Modal-related control:

> Modal is a future serverless worker lane. It is closed by default: no GPU, no paid job, no private upload, no recording, no stream, and no training starts without an awake human approving the exact endpoint, budget, input files, and shutdown check.

## Acceptance checks

- This file exists at `docs/integrations/MODAL_ENDPOINT.md`.
- `.env.example` includes `MODAL_SONICFORGE_ENDPOINT_URL`, `MODAL_SONICFORGE_API_TOKEN`, `MODAL_ENABLE_GPU=false`, and `MODAL_MAX_TASKS=0`.
- The aggregate verifier checks this doc for `dry-run / operator-armed only`, `modal_dry_run_no_endpoint_called`, `closed_until_human_yes`, `MODAL_MAX_TASKS=0`, and all fail-closed flags.
- No Modal endpoint, cloud GPU, training, upload, recording, stream, cron mutation, or paid provider call is started by default.
