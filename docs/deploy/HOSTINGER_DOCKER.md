# Hostinger Docker Deploy — SonicForge Live

This package adds a Hostinger-ready Docker image definition for **Intergalactic DJs presents DJ VANTA, powered by SonicForge Live**.

## Safety posture

The container is closed by default:

- `SONICFORGE_ALLOW_GPU=false`
- `SONICFORGE_ALLOW_PAID_API=false`
- `SONICFORGE_ALLOW_PUBLIC_STREAM=false`
- `COMFYUI_ENABLE_PROMPT=false`
- `RUNPOD_ENABLE_POD_START=false`
- `TTS_ENABLE_AUDIO_OUTPUT=false`

Do not put API keys, Hostinger tokens, GitHub tokens, SSH private keys, or `.env` contents in this repo, Dockerfile, compose file, or Hostinger Docker Manager content.

## Files

- `Dockerfile` — builds the FastAPI SonicForge Live app image.
- `.dockerignore` — excludes secrets, git metadata, venvs, caches, logs, and generated media.
- `docker-compose.hostinger.yml` — Hostinger/VPS-ready Compose stack using port `8788` and named volumes.

## Local build commands, if Docker is available

```bash
docker compose -f docker-compose.hostinger.yml build
docker compose -f docker-compose.hostinger.yml up -d
curl -fsS http://127.0.0.1:8788/health | python3 -m json.tool
curl -fsS http://127.0.0.1:8788/about | head
```

Stop it locally when done:

```bash
docker compose -f docker-compose.hostinger.yml down
```

## Hostinger Docker Manager path

Hostinger Docker Manager can deploy Compose projects to an existing VPS.

Preferred clean path:

1. Push this repo to GitHub once GitHub permissions are fixed.
2. In Hostinger Docker Manager, create/update a project named `sonicforge-live` from the repo URL, or paste the compose content if the VPS already has this source directory.
3. Expose only the desired port/domain. Start with private/test access before public demo.
4. Verify:

```bash
curl -fsS http://<VPS-IP>:8788/health | python3 -m json.tool
curl -fsS http://<VPS-IP>:8788/about | head
```

Expected health safety flags:

```json
{
  "starts_gpu": false,
  "starts_paid_api": false,
  "publishes_stream": false
}
```

## Current blocker noted by Hermes/Jimsky

Hostinger API token was present locally, but the VPS list request returned `403 Forbidden`, so Hermes could not safely select a VPS or create/update a Hostinger Docker project automatically.

No paid resources were created. No public service was started. No secrets were printed.

## Manual upload fallback

If GitHub permissions are still blocked, upload the project archive to the VPS, extract it, then run:

```bash
cd sonicforge-live
docker compose -f docker-compose.hostinger.yml up -d --build
```

Then verify `/health`, `/about`, `/`, and `/visualizer`.
