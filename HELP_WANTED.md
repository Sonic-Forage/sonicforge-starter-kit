# Help Wanted — SonicForge Live / Intergalactic DJs

Captured: 2026-05-01T14:20:59.509826+00:00

## Project

**Intergalactic DJs presents DJ VANTA//SonicForge, powered by SonicForge Live.**

A local-first Hermes-native autonomous AI DJ/VJ control plane for house parties, livestream previews, hackathon demos, and future club/festival routing.

## Fast start

```bash
cd sonicforge-live
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python3 scripts/verify.py
python3 -m uvicorn server.main:app --host 127.0.0.1 --port 8788
```

Open:

- Control deck: http://127.0.0.1:8788/
- VJ visualizer: http://127.0.0.1:8788/visualizer
- Health: http://127.0.0.1:8788/health

## What helpers can work on

### Frontend / demo polish

- Make Deck A / Deck B visually obvious in the control deck.
- Make the Rave Survival Kit panel beautiful and judge-friendly.
- Improve visualizer text shaders/code rain/dual ASCII spectrograph.
- Add a one-click demo sequence button.

### Backend / planner

- Strengthen `/api/next-segment` payloads.
- Improve prompt/crate cache selection.
- Improve set manifest/timeline generation.
- Keep program status honest: mock audio until real renderer exists.

### ComfyUI lane

- Convert `docs/comfyui/INTERGALACTIC_VISUAL_SPELL_WORKFLOW.md` into a real ComfyUI workflow JSON card.
- Keep default mode dry-run.
- Do not start GPU/cloud jobs without explicit approval.

### Safety / culture

- Review `docs/features/HARM_REDUCTION_GUIDE.md` for safe copy.
- Keep harm reduction practical: hydration, hearing protection, buddy checks, consent, exits, chill zone.
- No medical advice, no drug dosing, no emergency substitution.

## Guardrails

- No secrets in git.
- No `.env`, API keys, stream keys, model weights, generated audio batches.
- No paid GPU/cloud by default.
- No public RTMP/posting by default.
- Text/TTS is opt-in; default talk breaks are text.

## Verification before PR/help handoff

```bash
python3 scripts/verify.py
python3 scripts/verify_survival_harm_reduction.py
python3 scripts/smoke_local_demo.py
git diff --check
```

## Best files to read first

- `README.md`
- `docs/pitch.md`
- `docs/demo-runbook.md`
- `docs/planning/OVERNIGHT_TASK_BOARD.md`
- `docs/inspiration/CARELESS_LIVEDJ_INTAKE.md`
- `docs/comfyui/INTERGALACTIC_VISUAL_SPELL_WORKFLOW.md`
- `docs/features/HARM_REDUCTION_GUIDE.md`
- `docs/culture/RAVE_DJ_HISTORY_GUIDE.md`
