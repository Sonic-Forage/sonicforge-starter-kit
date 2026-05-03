# SonicForge Live Permanent Home + One-Day Hackathon Sprint

Created: 2026-05-01T05:26:42.967152+00:00

## North Star

SonicForge Live is not only an autonomous DJ app. It is a permanent Hermes-native creative performance package: a reusable skill/entity bundle that lets Hermes operate a stage-ready AI performer named **DJ VANTA//SonicForge**.

The winning framing for the hackathon is:

> Hermes becomes the home base for a living AI stage entity: it plans the set, generates/queues music, writes talk breaks, drives visuals, exposes safe local controls, and can hand off to cloud/RTMP/VJ systems only when the human arms those adapters.

## Permanent Home

SonicForge should live in three layers:

1. **Project repo home**
   - Path: `/opt/data/workspace/projects/sonicforge-live`
   - Purpose: runnable app, adapters, demo site, docs, scripts, verification, commits.

2. **Hermes skill package home**
   - Future skill name: `sonicforge-live-dj-vanta`
   - Purpose: installed Hermes procedure for operating, packaging, improving, and demoing DJ VANTA from any future session.
   - Contents should include runbook, architecture, safety gates, backend contracts, demo script, and verifier commands.

3. **Stage/runtime home**
   - Local URL: `http://127.0.0.1:8788/`
   - VJ URL: `http://127.0.0.1:8788/visualizer`
   - Purpose: the human-facing control deck and capture/output surface for OBS, projector, Resolume, TouchDesigner, Spout/Syphon, or RTMP.

## What VANTA Means

Recommended expansion:

**VANTA = Virtual Autonomous Nocturnal Transmission Artist**

Meaning:
- **Virtual**: software-born stage entity, not a fake human.
- **Autonomous**: can keep a set moving with human guidance.
- **Nocturnal**: rave/club/night signal energy.
- **Transmission**: stream, radio, projector, RTMP, festival feed.
- **Artist**: it performs; it is not just infrastructure.

Alt expansions to keep in the pitch reserve:
- **Vector Autonomous Neural Transmission Artist** — more cybernetic/technical.
- **Void Audio Narrative Transmission Avatar** — more mythic/festival.
- **Visual Audio Neural Touring Agent** — more product/function.

## Best Hackathon Aspect

The strongest aspect is not pure music generation alone. The strongest aspect is **Hermes as a permanent creative operator for a multimodal stage entity**.

This makes the package fit Hermes because it uses Hermes strengths:
- persistent memory and skills;
- tool use and verification;
- local files/repos/processes;
- scheduled/autonomous overnight build loops;
- safe gating before paid APIs, GPU, RTMP, or public publishing;
- clear handoff artifacts for humans.

## One-Day Demo Promise

By the deadline, the demo should prove:

1. The user opens SonicForge Live.
2. DJ VANTA has a named identity and mission.
3. The user gives a vibe/energy/BPM prompt.
4. Hermes/SonicForge plans the next live segment.
5. The system produces a timeline entry with:
   - track cue/audio artifact;
   - DJ talk break;
   - visual cue;
   - clean-mix instructions;
   - output routing plan.
6. Browser VJ output is visible and capture-ready.
7. The package explains how ComfyUI, RunPod, RTMP, OBS, Resolume, TouchDesigner/Spout become opt-in adapters.
8. Safety badges show no paid cloud/GPU/public stream starts by default.

## Overnight Autonomous Build Priorities

If the user approves an overnight run, build in this order:

### 1. Autopilot timeline
- Add `/api/autopilot/start`, `/api/autopilot/stop`, `/api/timeline` or local CLI equivalent.
- Maintain a timeline manifest under `generated/timeline/`.
- Generate 5-8 mock segments with rising/falling energy.

### 2. Clean local audio program artifact
- Stitch generated WAV sketches into `generated/program/program.wav`.
- Add simple crossfades.
- Add talk-break placement/ducking metadata at minimum; actual local TTS if safe and available.

### 3. DJ VANTA identity + demo deck
- Create `docs/demo-runbook.md`.
- Create `docs/pitch.md`.
- Add a landing/demo panel to the UI.
- Add “VANTA = Virtual Autonomous Nocturnal Transmission Artist.”

### 4. Hermes package layer
- Draft `skills/sonicforge-live-dj-vanta/SKILL.md` or a skill-export doc in `docs/hermes-skill-package.md`.
- Include exact run commands, endpoints, safety gates, backend env contracts, and demo script.

### 5. Acceptance checklist + reveal pack
- Add file-backed acceptance checklist.
- Add manifest JSON for demo artifacts.
- Add verification script.
- Commit cleanly.

## Closed Gates During Autonomous Overnight Work

Do not do unattended:
- paid cloud/GPU starts;
- RunPod pod starts;
- Comfy Cloud jobs;
- public RTMP publish;
- domain purchase;
- outbound posting/submission;
- secret printing or committing;
- recursive cron creation.

Allowed unattended:
- local app code;
- docs/pitch/deck;
- mock audio/visual artifacts;
- local TTS if no paid provider/secrets required;
- verification scripts;
- local commits;
- final report back to origin chat.

## Package Sent to Hackathon Judges

The final package should look like:

- `README.md` — what it is and quickstart.
- `docs/pitch.md` — story, why Hermes, why it matters.
- `docs/demo-runbook.md` — exact 90-second demo.
- `docs/architecture.md` — local-first + adapters.
- `docs/hermes-skill-package.md` — how this becomes a permanent Hermes skill/entity.
- `generated/demo/` — sample timeline/audio/visual artifacts.
- `scripts/verify.py` — proof the safe demo works.
- optional short video/GIF/screenshot if time permits.

## Final Framing

**Open club was the original battlefield. Hermes is the permanent home.**

SonicForge Live turns Hermes into the command center for autonomous creative entities. DJ VANTA is the first entity: a local-first AI DJ/VJ that can run safely on a laptop, then plug into ComfyUI, RunPod, OBS, Resolume, Spout, or RTMP when the operator arms those lanes.
