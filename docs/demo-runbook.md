# SonicForge Live Demo Runbook

Updated: 2026-05-01T09:31:01+00:00

## Demo promise

**Intergalactic DJs presents DJ VANTA, powered by SonicForge Live:** a local-first Hermes-native autonomous AI DJ/VJ control plane that plans a dual-deck set segment, writes safe talk-breaks, emits browser/ComfyUI/TouchDesigner visual-spell cues, logs a local metadata-only set manifest, and proves all paid/live lanes stay closed until a human says yes.

This runbook is for a private hackathon/judge demo. It does **not** start Comfy Cloud, RunPod, Modal, public RTMP, model training, voice cloning, private uploads, or purchases.

## 0. Safety preflight script for the operator

Say this out loud before the demo:

> This is SonicForge Live, the local runtime. Intergalactic DJs is the show layer, and DJ VANTA//SonicForge is the first autonomous performer: Virtual Autonomous Nocturnal Transmission Artist. Today we are showing local planning, mock audio, dry-run VJ cues, and closed approval gates only. No public stream, paid GPU, ComfyUI prompt, RunPod pod, or external provider starts from this demo.

Closed gates to point at:

- `/health` returns `starts_gpu: false`, `starts_paid_api: false`, and `publishes_stream: false`.
- ComfyUI visual spells are contracts with `mode: dry_run`, `prompt_id: null`, and `files: []`.
- Sample pads are `metadata_only_no_audio_playback` and never start real recording or audio playback.
- Rave Survival Kit copy is community-care only: hydration, earplugs, buddy check, exits, chill zone, consent, and human override.

## 1. Start from a clean local repo

```bash
cd /opt/data/workspace/projects/sonicforge-live
git status --short --branch
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/smoke_local_demo.py
git diff --check
```

Expected verifier highlights:

```text
"ok": true
"project": "sonicforge-live"
"dual_deck_contract_checked": true
"comfyui_dry_run_checked": true
"survival_culture_checked": true
```

Expected smoke-test behavior:

- `/health` is OK and fail-closed.
- `/`, `/visualizer`, `/api/crate-cache`, `POST /api/next-segment`, all sample pads, and `/api/set-manifest` respond locally.
- Smoke tests may append local generated set metadata while running; after a formal demo prep, check `git status --short` and keep or revert generated artifacts intentionally.

## 2. Launch SonicForge Live

```bash
. .venv/bin/activate
uvicorn server.main:app --host 127.0.0.1 --port 8788
```

Open these windows:

- Control deck: <http://127.0.0.1:8788/>
- Browser VJ output: <http://127.0.0.1:8788/visualizer>
- Health JSON: <http://127.0.0.1:8788/health>

Recommended screen layout:

1. Left: Control deck.
2. Right/top: VJ output window for OBS/browser capture.
3. Right/bottom or terminal tab: curl/smoke commands.

## 3. Thirty-second click path

1. In the control deck, read the hero line: **Intergalactic DJs presents DJ VANTA**.
2. Click **Plan Next Continuous Segment**.
3. Show the newly rendered sections:
   - Deck A / Deck B handoff cards.
   - Equal-power crossfader metadata.
   - Prompt Crate Cache / Deck B crate-digging memory.
   - ComfyUI visual-spell cue marked dry-run.
   - Lineage + Rave Survival Kit panel.
   - Local Set Manifest Writer status.
4. Open the VJ window and point out:
   - `code_rain`, `eq_bands`, and `subtitle_spell` browser modes.
   - dual ASCII spectrograph language.
   - dry-run labels: `COMFYUI_DRY_RUN` and `TOUCHDESIGNER_CONTRACT`.
5. Click sample pads in this order:
   - `VANTA` for identity.
   - `DROP` for phrase-lock/show-control metadata.
   - `HYDRATE` or `BUDDY` for Rave Survival Kit.
   - `PORTAL` for ComfyUI/Deck B dry-run visual lane.

## 4. API proof commands

Use a second terminal while the server is running:

```bash
curl -fsS http://127.0.0.1:8788/health | python3 -m json.tool
curl -fsS http://127.0.0.1:8788/api/crate-cache | python3 -m json.tool | head -80
curl -fsS -X POST http://127.0.0.1:8788/api/next-segment | python3 -m json.tool > /tmp/sonicforge-next-segment.json
python3 - <<'PY'
import json
p = json.load(open('/tmp/sonicforge-next-segment.json'))['payload']
print('deck_a.role=', p['deck_a']['role'])
print('deck_b.role/status=', p['deck_b']['role'], p['deck_b']['status'])
print('crossfader=', p['transition']['crossfader']['curve'])
print('comfy=', p['comfyui_visual_spell']['workflow'], p['comfyui_visual_spell']['mode'], p['comfyui_visual_spell']['output'])
print('survival=', p['survival_kit']['visual_spell'])
print('culture=', p['culture_cue']['lineage'])
print('manifest=', p['set_manifest']['path'])
PY
curl -fsS -X POST http://127.0.0.1:8788/api/sample-pad \
  -H 'Content-Type: application/json' \
  -d '{"pad":"HYDRATE"}' | python3 -m json.tool
curl -fsS http://127.0.0.1:8788/api/set-manifest | python3 -m json.tool | head -120
```

Expected proof points:

- `deck_a.role= A` and `deck_b.role/status= B generated_mock`.
- Crossfader curve is `equal_power` with cosine/sine formula and metadata-only mixer status.
- ComfyUI workflow is `intergalactic-djs-visual-spell`, `mode` is `dry_run`, and output has `prompt_id: null`, `files: []`.
- `SURVIVAL_PING` appears in survival output with safe-scope copy.
- Culture lineage is `disco-house-techno-rave-vj-ai` with a respect note that AI is a guest.

## 5. Two-minute judge narrative

Use this sequence:

1. **Identity:** “SonicForge Live is the runtime, Intergalactic DJs is the show, DJ VANTA is the first performer.”
2. **Why Hermes-native matters:** “Hermes is not just a chat assistant here; it is the persistent operator that plans, verifies, journals, and improves the performer.”
3. **Real DJ brain:** “We model beatmatching, phrasing, EQ moves, cue points, crowd state, crossfader automation, and crate-digging memory before claiming real continuous mix audio.”
4. **Dual-deck flow:** “Deck A is the current groove; Deck B is the incoming portal. The handoff uses equal-power crossfader metadata and stays honest that no continuous mixer is running yet.”
5. **Visual/media lanes:** “Browser VJ works now. ComfyUI, TouchDesigner, Resolume, OBS, RunPod, and Modal are adapter contracts until approved.”
6. **Party operating system:** “Rave Survival Kit and lineage cues make it a safety buddy and culture narrator, not just a music generator.”
7. **Closed gates:** “The app proves false for GPU, paid API, and public stream flags on every default path.”

## 6. Rave Survival Kit demo guardrails

Safe lines to use:

- “Water station check: sip, breathe, come back glowing.”
- “Protect the ears that brought you here.”
- “Buddy check: know your exits, agree on a meet-up point, and keep your crew accounted for.”
- “Consent is the real VIP pass.”
- “Human override stays with the sober operator.”

Do not say or generate:

- drug dosing, ingestion, or identification guidance;
- medical diagnosis/treatment;
- emergency-service substitution;
- claims that the AI can keep people safe without humans.

## 7. If something fails

- **Server import error:** confirm `. .venv/bin/activate` and `pip install -r requirements.txt` ran.
- **Port already in use:** run on another local port, for example `--port 8790`, and adjust URLs.
- **Smoke test mutated generated manifests:** decide whether to keep them as demo evidence or revert them before commit.
- **ComfyUI not running:** expected for this demo. The ComfyUI lane is a dry-run cue contract only.
- **No audio heard:** this demo currently proves mock WAV sketch generation and metadata, not a continuous live mixer.

## 8. Post-demo cleanup

```bash
# Stop uvicorn with Ctrl-C first.
git status --short
git diff -- generated/sets || true
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify.py
git diff --check
```

If generated set metadata changed during the demo, either:

- keep it deliberately as local demo evidence and mention it in the handoff, or
- revert it so the repo returns to a clean source-only state.

## 9. Next demo upgrade lanes

- Add `/api/timeline` and a bounded 10/20/45-minute demo autopilot plan.
- Add a simple local program manifest renderer or WAV stitcher once continuous-mix claims can be verified.
- Add `docs/integrations/COMFYUI_API.md`, `RUNPOD_ACE_STEP.md`, and `MODAL_ENDPOINT.md` as approval-gated backend cards.
- Add a QR/prop-art Rave Survival Kit card only after the payload is final and the QR can be generated and decoded programmatically.
