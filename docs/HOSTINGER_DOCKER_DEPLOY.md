# Hostinger Docker Deploy

This repo can run as the SonicForge launch cockpit on the Hostinger VPS.

## Public routes

- `https://sonicforge.srv1600947.hstgr.cloud/launch`
- `http://2.24.214.114:8788/launch`
- `https://sonicforge.srv1600947.hstgr.cloud/api/launch-status`

## Deploy on VPS

```bash
cd /opt/jimsky/workbenches/sonicforge-live
cp docker-compose.hostinger.yml docker-compose.yml
DOCKER_BUILDKIT=1 docker compose build
COMPOSE_PROJECT_NAME=sonicforge-live docker compose up -d
```

## Safety

This image serves the SonicForge FastAPI UI/API. The launch cockpit remains fail-closed:

- no GPU jobs
- no provider calls
- no ComfyUI `/prompt`
- no RunPod generation
- no training start
- no public stream start
- no dataset upload

The external funk album metadata is mounted read-only under `./workspace` so the cockpit can show the 22-track dataset and sample prompts on the VPS.
