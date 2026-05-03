# SonicForge Live fork-readiness check — 2026-05-03

Status: **ready to clone/fork after latest commit is pushed**.

## What was checked

- Git state and remotes.
- Tracked heavy-media/model files.
- Endpoint/secret-looking strings in repo text.
- Python syntax/compile across `server/` and `scripts/`.
- Project verifier: `python3 scripts/verify.py`.
- Local FastAPI smoke server on port `8799`.
- Live Hostinger launch frontend and API.
- Browser visual render of `/launch` initial viewport.

## Frontend / website status

Live routes verified HTTP 200:

- `https://sonicforge.srv1600947.hstgr.cloud/launch`
- `https://sonicforge.srv1600947.hstgr.cloud/api/launch-status`
- `http://2.24.214.114:8788/launch`

Local smoke routes verified HTTP 200:

- `/health`
- `/api/launch-status`
- `/api/safety-policy`
- `/`
- `/launch`
- `/setup`
- `/api/backends`

Browser render QA for `/launch`:

- Initial viewport renders cleanly.
- No obvious error banner.
- No broken hero image in initial viewport.
- Launch cockpit shows `40 tracks wired`, `training off`, `HF private`, and `all gates locked`.
- Safety copy and locked gates are visible and intentional.

## Verification commands run

```bash
python3 scripts/verify.py
python3 -m compileall -q server scripts
python3 -m uvicorn server.main:app --host 127.0.0.1 --port 8799
```

Verifier result:

```json
{
  "ok": true,
  "project": "sonicforge-live",
  "files_checked": 37,
  "python_checked": true,
  "dual_deck_contract_checked": true,
  "comfyui_dry_run_checked": true,
  "survival_culture_checked": true,
  "text_first_mc_break_checked": true,
  "synthetic_crowd_ladder_checked": true,
  "backend_status_card_checked": true
}
```

## Forkability fixes applied in this pass

1. Removed a hardcoded stale RunPod/ComfyUI proxy default from `scripts/run_dj_vanta_full_album_dataset.py`.
   - The script now requires `COMFYUI_BASE_URL` from the operator environment.
   - The script logs only the env var name, not the endpoint value.
2. Archived untracked local experimental scripts outside the repo workspace so the repo status is clean for cloning/forking.
   - Archive path: `/opt/data/archive/sonicforge-live-untracked-20260503T0200Z/`
   - These files were not committed to Git.

## Secret / endpoint hygiene

- `.env` and `.env.*` are ignored except `.env.example`.
- No tracked audio/model/archive binaries were found by the tracked-file media scan.
- A targeted hardcoded RunPod proxy scan returned no matches after the fix.
- Operational endpoints should stay outside the repo and be supplied via env vars:
  - `COMFYUI_BASE_URL`
  - `RUNPOD_ACE_STEP_API_URL`
  - `MODAL_SONICFORGE_ENDPOINT_URL`
  - related provider tokens/secrets

## Safe fork/clone handoff

Recommended clone/fork setup after the new org repo exists:

```bash
git clone git@github.com:<NEW_ORG>/sonicforge-live.git
cd sonicforge-live
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python3 scripts/verify.py
uvicorn server.main:app --host 127.0.0.1 --port 8788
```

Open locally:

- `http://127.0.0.1:8788/launch`
- `http://127.0.0.1:8788/health`
- `http://127.0.0.1:8788/api/launch-status`

## Known notes before cloning to another org

- GitHub API/`gh` repo creation may still be blocked by bad token credentials in this Hermes environment. SSH push works for existing repos, but a human may need to create the new org repo first or update GitHub credentials.
- The live Hostinger deployment is currently healthy, but cloning to a new org does not automatically redeploy Hostinger. The new org repo will need its own remote/deploy wiring if you want Hostinger to pull from it.
- Heavy generated audio remains outside Git by design. The repo references private HF datasets and local cache paths for reviewed outputs.
- Generation scripts are forkable but should remain approval-gated: no GPU/provider calls unless an operator explicitly supplies endpoint env vars and runs the scripts.

## Verdict

The website/frontend is up, the local app smoke checks pass, the repo is safe/forkable after this cleanup, and the remaining setup step is organization-level GitHub remote creation/push wiring.
