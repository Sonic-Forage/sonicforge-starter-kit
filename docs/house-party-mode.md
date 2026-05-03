# SonicForge Live House-Party Mode

Updated: 2026-05-01T09:50:41+00:00

## Purpose

House-Party Mode is the safe local operating mode for **Intergalactic DJs presents DJ VANTA, powered by SonicForge Live**. It turns the project from a demo screen into a practical party co-pilot: DJ/VJ planning, local browser visuals, Rave Survival Kit reminders, and clear human controls — without starting paid providers, public streams, recording, uploads, or GPU jobs.

Use this when SonicForge Live is running at a private house party, studio hang, livestream rehearsal, or hackathon room demo.

## What House-Party Mode does

- Runs the SonicForge Live control deck on localhost.
- Uses mock/local adapters by default for track sketches, talk-break text, and visual-spell cues.
- Keeps DJ VANTA in a dual-deck planning loop: Deck A is the current groove, Deck B is the incoming portal.
- Shows practical Rave Survival Kit reminders: hydration, hearing protection, buddy check, exits, chill zone, consent, and human override.
- Routes visuals through the browser visualizer first, so OBS/projector/Resolume/TouchDesigner can capture a safe local window.
- Writes metadata-only set manifests for review, not continuous room recordings.

## What House-Party Mode refuses by default

House-Party Mode must remain closed-by-default unless an awake human deliberately changes configuration and accepts the risk.

It does **not**:

- start RunPod, Modal, Comfy Cloud, ComfyUI `/prompt`, Gemini/Lyria, or paid generation;
- publish RTMP/WHIP/SRT or post publicly;
- upload private media, room audio, datasets, prompts, or photos;
- train/fine-tune models;
- clone voices or imitate real people;
- secretly record people in the room;
- replace sober humans, venue staff, medical help, security, or emergency services.

Required default flags:

```json
{
  "starts_gpu": false,
  "starts_paid_api": false,
  "publishes_stream": false,
  "records_audio": false,
  "uploads_private_media": false
}
```

## Pre-party checklist

### 1. Assign the human operator

Pick one sober operator who can pause the set, lower volume, switch to chill mode, and speak to humans if something seems off.

Operator card:

- Operator name: `[write locally, do not commit private phone numbers]`
- Backup operator: `[write locally]`
- House address / emergency info: `[write locally, not in git]`
- Sound system owner: `[write locally]`
- Stop phrase: `HUMAN OVERRIDE: STOP SET`

### 2. Prepare the room

- Water station visible and easy to reach.
- Earplugs near entry or DJ table.
- Chill zone / quiet corner identified.
- Exits and bathroom route visible.
- Cables taped down; drinks kept away from electronics.
- Phone charging spot available.
- Trash/recycling bags placed early.
- Consent reminder visible: ask before touching, filming, or posting someone.

### 3. Prepare SonicForge locally

```bash
cd /opt/data/workspace/projects/sonicforge-live
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/smoke_local_demo.py
uvicorn server.main:app --host 127.0.0.1 --port 8788
```

Open:

- Control deck: <http://127.0.0.1:8788/>
- VJ output: <http://127.0.0.1:8788/visualizer>
- Health: <http://127.0.0.1:8788/health>

## Recommended local setup

```text
Laptop running SonicForge Live
  ├─ Browser tab 1: Control deck
  ├─ Browser tab 2/window: /visualizer for projector or OBS capture
  ├─ Local speakers / mixer controlled by a human
  └─ No public stream target unless explicitly approved
```

For a projector or TV, put `/visualizer` full-screen and keep the control deck on the operator laptop. If using OBS, capture the browser window only; do not start streaming until a human approves a real destination.

## Thirty-second house-party start script

The operator can say:

> Welcome to Intergalactic DJs. This is DJ VANTA, powered by SonicForge Live. Tonight the system is local-first: it plans the set, throws visual spells, and reminds us to take care of the room. No hidden recording, no public stream, no paid AI jobs. Human override stays active. Water is part of the dancefloor; earplugs are rave armor; check your people.

Then click:

1. **Plan Next Continuous Segment**.
2. Confirm Deck A / Deck B cards render.
3. Confirm `Lineage + Rave Survival Kit` is visible.
4. Confirm ComfyUI visual-spell cue is `dry_run`.
5. Trigger a safe sample pad: `HYDRATE`, `BUDDY`, or `CHILL`.

## Rave Survival Kit operating cadence

House-Party Mode should treat survival cues as part of the show, not an apology for it.

Suggested cadence:

- Start: earplug + consent reminder.
- Every ~30 minutes: hydration ping.
- After a peak stretch: chill-zone / air / buddy check.
- Before major intensity rise: exits and space reminder.
- Any time the sober operator is concerned: press `CHILL` or stop the set.

Safe copy only:

- “Water station check: sip, breathe, come back glowing.”
- “Protect the ears that brought you here.”
- “Buddy check: know your exits and keep your crew accounted for.”
- “Consent is the real VIP pass.”
- “There is no shame in stepping out.”

Do **not** generate medical advice, diagnosis, dosing, substance identification, legal advice, or instructions for illegal activity. If someone appears in danger or medically distressed, pause the party plan and route to sober humans, venue staff, medical help, or emergency services as appropriate.

## DJ/VJ mode settings

Good first defaults for a living room or studio:

```json
{
  "mode": "house_party",
  "set_title": "Intergalactic DJs House-Party Transmission",
  "guide_prompt": "warmup into intergalactic house, practical survival pings, respectful lineage notes, browser visual spells",
  "target_bpm": 124,
  "energy": 5,
  "talk_break_modes": ["hype", "history", "survival", "lore"],
  "visual_modes": ["code_rain", "eq_bands", "subtitle_spell", "dual_ascii_spectrograph"],
  "provider_lanes": "mock_or_dry_run_only"
}
```

## Approval gates before going bigger

Before any real public or external action, the operator must make a fresh awake decision. Silence is not approval.

| Lane | Default | Required human yes |
|---|---|---|
| Public livestream / RTMP | Closed | Destination URL, stream owner, consent/privacy check |
| Paid GPU / RunPod / Modal / Comfy Cloud | Closed | Budget, runtime limit, endpoint, stop plan |
| ComfyUI `/prompt` | Closed | Local server URL, workflow card, model/license check |
| Voice / TTS audio | Text-only | Voice rights, consent, output target |
| Recording room audio/video | Off | People informed, storage path, retention plan |
| Uploading private media/datasets | Closed | Rights, redaction, destination, deletion plan |

## Post-party cleanup

```bash
# Stop uvicorn with Ctrl-C first.
git status --short
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify.py
git diff -- generated/sets || true
```

If a smoke test or demo appended generated manifests, either keep them intentionally as local evidence or revert them before sharing the repo. Do not commit private room notes, names, addresses, phone numbers, stream keys, `.env`, photos, or recordings.

## Success criteria

House-Party Mode is working when:

- `/health` is OK and fail-closed.
- `/` renders the control deck.
- `/visualizer` renders browser-only VJ output.
- `POST /api/next-segment` returns Deck A/B state, equal-power crossfader metadata, `survival_kit`, `culture_cue`, and a dry-run ComfyUI visual spell.
- The operator can press `HYDRATE`, `BUDDY`, and `CHILL` sample pads without starting audio playback, recording, streams, or provider calls.
- A sober human can stop or lower the set faster than the system can escalate it.
