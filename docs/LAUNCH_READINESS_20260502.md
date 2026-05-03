# SonicForge Launch Readiness — 2026-05-02

Status: **green for private launch demo / operator cockpit review**.

## Live links

- HTTPS cockpit: https://sonicforge.srv1600947.hstgr.cloud/launch
- HTTPS API: https://sonicforge.srv1600947.hstgr.cloud/api/launch-status
- Raw fallback: http://2.24.214.114:8788/launch

## Current verified deployment

- Hostinger VPS path: `/opt/jimsky/workbenches/sonicforge-live`
- Docker container: `sonicforge-live`
- Docker image: `sonicforge-live:launch-cockpit`
- Public port fallback: `8788`
- HTTPS routing: existing Traefik Docker provider route for `sonicforge.srv1600947.hstgr.cloud`
- GitHub repo: `TheMindExpansionNetwork/sonicforge-live`
- Verified commit: `0b667ff feat: add Hostinger Docker launch deploy`

## Verification run

Latest launch backup verification captured:

- `/launch` HTTPS: HTTP `200`
- `/api/launch-status` HTTPS: HTTP `200`
- raw IP fallback `/launch`: HTTP `200`
- local verifier: `scripts/verify.py` passed
- remote Docker health: `healthy`
- remote Docker restart count: `0`
- API payload checks:
  - `ok=true`
  - total private dataset tracks: `40`
  - sample prompts: `2`
  - `training.started=false`
  - `starts_gpu=false`
  - `starts_paid_api=false`
  - `trains_models=false`
  - `uploads_private_media=false`
  - `publishes_stream=false`
  - `records_audio=false`
  - `requires_human_approval=true`

## Backup artifacts

Local launch backup folder:

`/opt/data/drops/sonicforge-launch-ready-20260502T214205Z/`

Includes:

- `sonicforge-live-sanitized-source-20260502T214205Z.tar.gz` — sanitized source snapshot, no generated audio or secrets.
- `dj-vanta-control-plane-metadata-20260502T214205Z.tar.gz` — lightweight metadata/prompts/docs snapshot, no generated audio.
- `vps-snapshot/sonicforge-vps-snapshot.tgz` — VPS Docker/compose/status/API snapshot.
- `reports/verification.md` — live URL/API/Docker verification evidence.
- `reports/secret-scan.md` — high-risk secret scan result.
- `checksums/SHA256SUMS.txt` and `checksums/SHA256SUMS.json` — integrity hashes.
- `launch-backup-manifest.json` — machine-readable launch backup manifest.

## Existing media/data backups

The corrected funk-glitch dataset archives remain available locally:

- `/opt/data/drops/dj-vanta-funk-glitch-bass-drama-engine-audio-only-20260502T185849Z.zip`
- `/opt/data/drops/dj-vanta-funk-glitch-bass-drama-engine-complete-20260502T185849Z.tar.gz`

Private Hugging Face dataset mirrors remain linked from the launch cockpit.

## Closed gates / non-claims

The cockpit is a launch proof and operator review surface. It does **not**:

- start GPU jobs;
- call paid providers;
- start ComfyUI or RunPod generation;
- start model training;
- upload private media;
- record audio;
- publish public streams;
- claim revenue or a completed trained model.

## Next few-hour launch checklist

1. Open the HTTPS cockpit from phone and laptop.
2. Review the two sample prompts and private dataset links.
3. Decide whether to keep this as private operator cockpit or add a public landing page in front of it.
4. If making public, add basic auth or hide sensitive operator routes first.
5. Only after human approval: start LoRA training or public release steps.
