# SonicForge Launch Cockpit

Status: local-first launch UI, fail-closed by default.

## Open it

```bash
uvicorn server.main:app --host 127.0.0.1 --port 8788
```

Then open:

- `/launch` — SonicForge/DJ VANTA launch cockpit
- `/api/launch-status` — JSON status backing the cockpit
- `/station` — station signal UI
- `/visualizer` — local VJ window
- `/workflows` — workflow registry
- `/agents` — agent factory / fork setup lanes

## What it proves

- Two private DJ VANTA/SonicForge album datasets are surfaced in one operator view.
- The current generated-track count is read from local manifests, not hard-coded in the page.
- Two paste-ready training-test prompts are rendered from the corrected per-track lyrics/settings.
- Hugging Face dataset links are shown for review, while datasets remain private unless the human changes policy.
- Safety gates are visible and locked by default.

## Safety posture

The launch cockpit is a read-only control surface. It does **not** start:

- GPU jobs
- paid provider calls
- ComfyUI `/prompt`
- RunPod / ACE-Step generation
- model downloads
- recording
- RTMP/public stream publishing
- dataset uploads
- training

Every production action must be explicitly human-approved and routed through the appropriate operator workflow.

## Forkable architecture

- `server/launch_status.py` builds the cockpit payload from local project manifests.
- `server/main.py` serves `/launch` and `/api/launch-status`.
- `app/static/launch.html` is a single-file static cockpit that can be copied into a fork.
- The existing `/setup`, `/agents`, `/workflows`, `/station`, and `/visualizer` routes remain linked from the cockpit.

## Verification

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/smoke_local_demo.py
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from server.launch_status import build_launch_status
j = build_launch_status()
assert j['ok'] is True
assert j['starts_gpu'] is False
assert j['trains_models'] is False
assert j['uploads_private_media'] is False
assert len(j['sample_prompts']) == 2
print('launch cockpit ok', j['status'])
PY
```

Optional browser smoke:

```bash
python3 - <<'PY'
import json, urllib.request
for url in ['http://127.0.0.1:8788/launch', 'http://127.0.0.1:8788/api/launch-status']:
    with urllib.request.urlopen(url, timeout=10) as r:
        body = r.read()
        print(url, r.status, len(body))
        if url.endswith('launch-status'):
            j = json.loads(body)
            assert j['starts_gpu'] is False
            assert j['trains_models'] is False
            assert len(j['sample_prompts']) == 2
PY
```
