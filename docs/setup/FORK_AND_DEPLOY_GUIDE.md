# Fork and Deploy Guide

## 1. Create a new repo

Recommended names: `sonicforge-starter-kit`, `your-dj-name-sonicforge`, or `your-collective-command-center`.

Keep it private while customizing. Flip public only after secret scans pass and you are ready.

## 2. Clone and install

```bash
git clone https://github.com/YOUR_OWNER/sonicforge-starter-kit.git
cd sonicforge-starter-kit
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python3 scripts/verify_starter_kit.py
```

## 3. Run local cockpit

```bash
python3 -m uvicorn server.main:app --host 127.0.0.1 --port 8799
```

Open `http://127.0.0.1:8799/launch`.

## 4. Connect creative backends safely

For ComfyUI: set `COMFYUI_BASE_URL` in `.env`, keep `ALLOW_WORKFLOW_PROMPT=0` for read-only checks, verify endpoint compatibility first, then enable execution only when intentional.

## 5. Deploy

Before deploying: change domains, set environment variables on the server instead of git, keep public posting/training/upload gates closed, and run starter verification.

## 6. Public release checklist

```bash
python3 scripts/verify_starter_kit.py
git status --short --branch
git log --oneline -5
```

Confirm `.env` is ignored, no real tokens/endpoints are tracked, no model weights/private media are tracked, and public copy/assets are yours or licensed.
