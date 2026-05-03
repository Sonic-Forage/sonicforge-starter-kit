# How to Test SonicForge Live for the 5:55 Pacific Launch

Status: local/manual test script. No paid GPU, provider calls, public stream, recording, upload, dataset upload, or model training should start from these steps.

## 0. Start local server

```bash
cd /opt/data/workspace/projects/sonicforge-live
python3 -m uvicorn server.main:app --host 127.0.0.1 --port 8788
```

Open:

```text
http://127.0.0.1:8788/
```

## 1. Quick health checks

```bash
curl -fsS http://127.0.0.1:8788/health
curl -fsS http://127.0.0.1:8788/api/backends
curl -fsS http://127.0.0.1:8788/api/ecosystem
curl -fsS http://127.0.0.1:8788/api/program-status
curl -fsS http://127.0.0.1:8788/api/mc-breaks/preview
curl -fsS http://127.0.0.1:8788/api/dj-brain/state
```

Expected: all safety flags remain false.

## 2. UI test path

1. Open `/`.
2. Confirm the hero says Intergalactic DJs / DJ VANTA / SonicForge Live.
3. Confirm the collective/ecosystem card loads from `/api/ecosystem`.
4. Press **Preview Selected Culture Mode** and switch history/hype/survival/lore/technical.
5. Press **Plan Next Continuous Segment**.
6. Confirm Deck A/B cards update.
7. Confirm Program Audio Truth Panel says no rendered continuous program yet.
8. Confirm Backend Status says provider lanes are closed until human yes.
9. Open `/visualizer` in a new window.
10. Switch visual modes: plasma, code_rain, eq_bands, subtitle_spell, SDF/MSDF fallback, dual ASCII spectrograph.
11. Press sample pads: HYDRATE, BUDDY, DROP, PORTAL, CHILL. Confirm they are metadata-only dry runs.

## 3. Station Signal test

Open `/station`, run acquire/session dry-run. Expected:

- starts_gpu=false
- starts_paid_api=false
- publishes_stream=false
- records_audio=false

## 4. Launch story test

Say out loud:

> Intergalactic DJs is the collective. SonicForge Live is the universe/runtime. DJ VANTA is the first clone. Anyone can fork the station, build new agents, share skills/plugins/workflow cards, and later train custom models only after dataset/eval/rights approval.

## 5. Verifier stack

```bash
cd /opt/data/workspace/projects/sonicforge-live
python3 -m py_compile server/*.py server/adapters/*.py scripts/*.py
python3 scripts/verify.py
python3 scripts/verify_survival_harm_reduction.py
python3 scripts/smoke_local_demo.py
git diff --check
```

If smoke tests create generated set/timeline files, revert them unless intentionally committing a fixture.

## 6. No-go list

Do not do these without explicit approval:

- public repo visibility flip,
- public deployment,
- RTMP/OBS stream,
- ComfyUI `POST /prompt`,
- RunPod/Modal GPU job,
- model downloads,
- dataset upload,
- custom model training,
- voice cloning,
- recording/uploading private party media,
- outreach/payment automation.
