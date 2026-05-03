# Final Demo Acceptance Checklist — SonicForge Live / DJ VANTA

Status: **draft / fail-closed**
Created: `2026-05-01T08:04:01Z`

Purpose: give the awake operator one pass/fail checklist before a private demo or handoff. This file does **not** approve public deployment, payments, outreach, dataset upload, model training, GPU/video jobs, live realtime providers, private media upload, voice-to-shell, or recursive cron creation.

Operator rule: every lane stays closed unless an awake human explicitly says yes. Silence, enthusiasm, or cron progress is not approval.

## Acceptance checks

| ID | Acceptance signal | Proof | Fail closed if | Fallback |
| --- | --- | --- | --- | --- |
| `verify_local_runtime_safety` | `/health` reports `starts_gpu=false`, `starts_paid_api=false`, `publishes_stream=false`, and the control deck says no provider starts without human approval. | `server/main.py` | Any route starts GPU/cloud/paid APIs/public RTMP by default or hides approval flags. | Run only README quickstart, `/health`, and static UI; do not open external adapters. |
| `verify_next_segment_contract` | `POST /api/next-segment` returns `track`, `talk`, `visual`, `mix`, `transition`, `deck_a`, `deck_b`, `visual_spell`, `survival_kit`, `culture_cue`, and `state`. | `server/planner.py` | The app claims seamless continuous audio rendering before a real renderer exists or calls ComfyUI/RunPod automatically. | Show the JSON payload and VJ browser window only; label audio as local mock sketch metadata. |
| `verify_dual_deck_dj_brain` | Deck A/B roles, beatmatch plan, phrase plan, bass swap, EQ moves, cue points, and synthetic crowd state are visible in planner output. | `server/schemas.py` | The demo implies the system is reading a real crowd or executing unverified mixer automation. | Describe it as deterministic DJ-brain metadata for a future mixer/TouchDesigner/Resolume adapter. |
| `verify_rave_survival_kit_scope` | Rave Survival Kit copy is practical community-care only with human override and no medical, legal, dosing, or drug-use instructions. | `docs/features/HARM_REDUCTION_GUIDE.md` | Any text gives medical treatment, diagnosis, dosing, or drug-use instructions. | Disable survival narration and show only the safe checklist: water, earplugs, buddy, exits, chill zone, human override. |
| `verify_visual_spell_dry_run` | ComfyUI and TouchDesigner visual-spell packets remain dry-run/browser-first contracts; `/prompt` and paid GPU calls are not made. | `docs/comfyui/INTERGALACTIC_VISUAL_SPELL_WORKFLOW.md` | A demo tries to start Comfy Cloud, RunPod, Modal, TouchDesigner MCP automation, or public visual publishing without approval. | Use `/visualizer` browser capture and static visual-spell docs only. |
| `verify_private_demo_handoff` | Pitch, task board, journal, and reviewer scorecard exist so the human has a coherent private-demo story and current blockers. | `docs/pitch.md` | The handoff asks the operator to publish, charge, upload datasets, train models, start live providers, or send outreach immediately. | Use README, `docs/pitch.md`, and this checklist as a local-only demo script. |

## Preflight commands

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_final_demo_acceptance_checklist.py
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile server/*.py server/adapters/*.py scripts/*.py
node --check app/static/main.js
git diff --check
```

## Closed gates

- `public_deployment`
- `payment_or_revenue_claim`
- `outbound_outreach`
- `dataset_upload_or_model_training`
- `gpu_video_or_matrix_generation`
- `live_provider_activation`
- `private_media_upload`
- `voice_to_shell`
- `recursive_cron_creation`

## Non-claims

- Do not claim public deployment happened from this cron run.
- Do not claim revenue was earned unless a human provides proof outside this repo.
- Do not claim a continuous mixed program render exists until a verified renderer produces it.
- Do not claim ComfyUI, RunPod, Modal, TouchDesigner, RTMP, LiveKit, or paid providers were activated.
- Do not claim medical, legal, dosing, or drug-use guidance; survival copy is community-care reminder only.

## Next human step

Run the preflight commands, open the local control deck, press **Plan Next Continuous Segment**, and approve at most one external lane only after reviewing closed gates.
