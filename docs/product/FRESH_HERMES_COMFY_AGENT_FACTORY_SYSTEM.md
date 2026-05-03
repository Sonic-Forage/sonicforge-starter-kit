# Fresh Hermes + Comfy Endpoint Agent Factory System

Status: deep architecture blueprint
Project: SonicForge Live / Intergalactic DJs / cloneable DJ agents
Safety posture: fail-closed, operator-approved model downloads and workflow execution

## 1. Big idea

SonicForge Live should ship as a **forkable performer factory** that can be installed into a fresh Hermes build.

The user flow should feel like this:

```text
1. Install fresh Hermes.
2. Clone SonicForge Live / Intergalactic DJs package.
3. Add API keys / provider credentials locally.
4. Add a ComfyUI endpoint URL or choose local Comfy install.
5. Run setup wizard.
6. The package verifies the endpoint, required models, and workflows.
7. Operator approves model downloads if missing.
8. The system installs or points to workflows.
9. User creates a custom DJ/VJ agent.
10. Agent can run dry-run sets, crate plans, visual spells, and approved Comfy workflows.
```

Pitch line:

> Clone the station, add your keys, plug in your Comfy endpoint, and grow your own autonomous DJ/VJ agent.

---

## 2. System layers

```text
Fresh Hermes Build
  ↓
SonicForge Payload Pack
  ↓
Agent Factory Wizard
  ↓
Custom DJ/VJ Agent Payload
  ↓
Workflow Registry
  ↓
ComfyUI Endpoint Adapter
  ↓
Model Manager / Download Ledger
  ↓
Station UI + Terminal Visual Spell Engine
```

### Layer A — Fresh Hermes base

The base is upstream-compatible Hermes Agent.

It provides:

- model/provider configuration
- tools/skills
- persistent memory
- Telegram/Discord/gateway if desired
- terminal/file/web/browser tooling
- cron later if approved

SonicForge should not require a hard-fork of Hermes. It should install as a payload/package.

### Layer B — SonicForge payload pack

Payload pack path:

```text
payloads/sonicforge-live/
  PAYLOAD.md
  manifest.json
  .env.example
  config.template.yaml
  docs/
  skills/
  agents/
  workflows/
  scripts/
```

The payload contains no secrets. It only contains templates, docs, manifests, scripts, and safe defaults.

### Layer C — Agent factory wizard

A local script or Hermes skill that asks:

- What is your DJ agent name?
- What genres/vibes?
- What visual identity?
- What voice/talk-break tone?
- Which modes should be enabled: LIVE, CRATE, ALBUM, VISUALS?
- Which Comfy workflow packs should be available?
- Is this local-only, venue, or creator/festival use?

It writes:

```text
agents/<agent-id>/
  manifest.json
  persona.md
  safety.md
  crate-profile.json
  visual-profile.json
  station-signal.json
  workflow-bindings.json
  README.md
```

### Layer D — Workflow registry

A local registry declares workflow templates and required models.

```text
workflows/registry.json
workflows/comfyui/
  visual-spell-poster.workflow.json
  visual-spell-poster.card.md
  agent-logo.workflow.json
  agent-logo.card.md
  album-cover.workflow.json
  album-cover.card.md
  terminal-loop-background.workflow.json
  terminal-loop-background.card.md
```

Each workflow card declares:

- workflow id
- input variables
- required custom nodes
- required model files
- expected VRAM
- license notes
- output type
- smoke-test prompt
- whether it can run in dry-run mode
- whether it is safe for hackathon demo

### Layer E — ComfyUI endpoint adapter

Adapter env var:

```text
COMFYUI_BASE_URL=http://127.0.0.1:8188
```

Adapter checks:

```text
GET /system_stats
GET /object_info
GET /prompt
GET /queue
```

Adapter only calls `POST /prompt` when an explicit local approval flag is set.

Suggested flags:

```text
SONICFORGE_COMFY_DRY_RUN=1
SONICFORGE_ALLOW_COMFY_PROMPT=0
SONICFORGE_ALLOW_MODEL_DOWNLOADS=0
SONICFORGE_ALLOW_REMOTE_ENDPOINT=0
```

Default behavior:

- endpoint preflight: allowed
- object info check: allowed
- workflow validation: dry-run only
- prompt execution: blocked
- model download: blocked
- upload private media: blocked

### Layer F — Model manager / download ledger

The model manager should never silently download giant weights.

It should produce a ledger like:

```text
models/ledger/model-download-plan.json
models/ledger/MODEL_DOWNLOAD_PLAN.md
```

The ledger includes:

- model name
- source URL
- license
- target folder
- size estimate
- checksum if available
- workflow(s) that need it
- disk space required
- approval status

Download command shape:

```bash
python scripts/model_manager.py plan --workflow visual-spell-poster
python scripts/model_manager.py download --model <id> --approved
```

No `--approved`, no download.

---

## 3. Fresh install onboarding flow

### Step 1 — Install Hermes

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
hermes setup
```

### Step 2 — Clone SonicForge

```bash
git clone git@github.com:TheMindExpansionNetwork/sonicforge-live.git
cd sonicforge-live
```

### Step 3 — Copy env template

```bash
cp .env.example .env
```

The `.env.example` should contain placeholders only:

```text
DEEPSEEK_API_KEY=
OPENAI_API_KEY=
COMFYUI_BASE_URL=http://127.0.0.1:8188
SONICFORGE_COMFY_DRY_RUN=1
SONICFORGE_ALLOW_COMFY_PROMPT=0
SONICFORGE_ALLOW_MODEL_DOWNLOADS=0
SONICFORGE_ALLOW_REMOTE_ENDPOINT=0
```

### Step 4 — Run SonicForge setup wizard

```bash
python scripts/sonicforge_setup.py wizard
```

Wizard output:

```text
✅ Hermes present
✅ Python deps present
✅ SonicForge app routes present
✅ Comfy endpoint reachable / or not configured
✅ Workflow registry parsed
⚠ Missing models detected
❌ Model downloads blocked until approval
✅ Dry-run mode active
```

### Step 5 — Create custom DJ agent

```bash
python scripts/create_dj_agent.py \
  --name "DJ ORBITAL MOTH" \
  --style "psytrance warehouse alien sunrise" \
  --modes live,crate,album,visuals
```

### Step 6 — Open local station

```bash
python3 -m uvicorn server.main:app --host 127.0.0.1 --port 8788
```

Routes:

- `/station`
- `/agents`
- `/terminal-visuals`
- `/crate`
- `/album`
- `/live`

---

## 4. Comfy workflow lifecycle

### 4.1 Register workflow

A workflow template enters the system as:

```text
workflows/comfyui/<workflow-id>.json
workflows/comfyui/<workflow-id>.card.md
```

Example workflow ids:

- `agent-logo-generate`
- `agent-hero-art-generate`
- `visual-spell-poster`
- `album-cover-generate`
- `terminal-loop-background`
- `rave-flyer-safe-qr-composite`

### 4.2 Inspect endpoint

```bash
python scripts/comfy_adapter.py preflight
```

Checks:

- `/system_stats`
- `/object_info`
- required custom nodes
- workflow node compatibility
- queue state

### 4.3 Plan missing models

```bash
python scripts/model_manager.py plan --workflow agent-logo-generate
```

Writes:

```text
models/ledger/MODEL_DOWNLOAD_PLAN.md
```

### 4.4 Approve downloads

Human approval required:

```bash
python scripts/model_manager.py download --plan models/ledger/model-download-plan.json --approved
```

### 4.5 Dry-run workflow

```bash
python scripts/comfy_adapter.py dry-run \
  --workflow agent-logo-generate \
  --agent dj-orbital-moth
```

Output should be normalized:

```json
{
  "ok": true,
  "mode": "dry_run",
  "would_call_prompt": false,
  "prompt_id": null,
  "files": [],
  "warnings": ["/prompt not called because SONICFORGE_ALLOW_COMFY_PROMPT=0"]
}
```

### 4.6 Real execution after approval

Only with:

```text
SONICFORGE_ALLOW_COMFY_PROMPT=1
```

Command:

```bash
python scripts/comfy_adapter.py run \
  --workflow agent-logo-generate \
  --agent dj-orbital-moth \
  --approved
```

It should:

1. upload required reference images if any
2. inject prompt variables
3. call `POST /prompt`
4. track `/ws`
5. fetch `/history/{prompt_id}`
6. download `/view` outputs
7. save metadata under `generated/comfy/<agent-id>/`

---

## 5. Agent-to-workflow binding

Each DJ agent should define what workflows it can use.

```json
{
  "agent_id": "dj-vanta",
  "workflow_bindings": {
    "logo": "agent-logo-generate",
    "hero_art": "agent-hero-art-generate",
    "visual_spell": "visual-spell-poster",
    "album_cover": "album-cover-generate",
    "terminal_background": "terminal-loop-background"
  },
  "prompt_style": {
    "colors": ["black", "cyan", "magenta", "ultraviolet"],
    "symbols": ["black star portal", "VA monogram", "waveform halo"],
    "avoid": ["watermark", "real brand logos", "drug instructions", "medical claims"]
  }
}
```

The adapter turns agent identity into safe prompt packets.

---

## 6. Package formats

### 6.1 Repo mode

For builders:

```text
git clone sonicforge-live
```

Best for hackathon judges/devs.

### 6.2 Payload zip mode

For fresh Hermes installs:

```text
dist/sonicforge-live-hermes-payload-YYYYMMDD.zip
```

Contains:

```text
PAYLOAD.md
manifest.json
.env.example
agents/template-agent/
workflows/
docs/
scripts/install_payload.py
scripts/verify_payload.py
```

### 6.3 Agent pack mode

For sharing just one custom DJ:

```text
dist/dj-orbital-moth-agent-pack-YYYYMMDD.zip
```

Contains:

```text
AGENT.md
manifest.json
persona.md
safety.md
crate-profile.json
visual-profile.json
workflow-bindings.json
assets/
```

### 6.4 Workflow pack mode

For sharing visual/mix generation packs:

```text
dist/sonicforge-comfy-workflows-YYYYMMDD.zip
```

Contains:

```text
workflows/comfyui/*.json
workflows/comfyui/*.card.md
models/ledger/model-download-plan.example.json
```

No model weights by default.

---

## 7. Required scripts

### `scripts/sonicforge_setup.py`

Commands:

```bash
python scripts/sonicforge_setup.py doctor
python scripts/sonicforge_setup.py wizard
python scripts/sonicforge_setup.py write-env-example
```

Responsibilities:

- check Python version
- check Hermes availability
- check app deps
- check Comfy URL presence
- check route files
- check workflow registry
- check agents folder
- print next safe steps

### `scripts/create_dj_agent.py`

Commands:

```bash
python scripts/create_dj_agent.py --name "DJ NAME" --style "..."
python scripts/create_dj_agent.py --from-template agents/template-agent --name "..."
```

Responsibilities:

- slugify name
- create manifest
- create persona/safety/profile files
- bind default workflows
- never include secrets

### `scripts/verify_agent_payloads.py`

Checks:

- every agent manifest parses
- required keys exist
- safety gates are present and false by default
- no forbidden overclaims
- no tokens/secrets

### `scripts/comfy_adapter.py`

Commands:

```bash
python scripts/comfy_adapter.py preflight
python scripts/comfy_adapter.py dry-run --workflow <id> --agent <id>
python scripts/comfy_adapter.py run --workflow <id> --agent <id> --approved
python scripts/comfy_adapter.py interrupt
python scripts/comfy_adapter.py free
```

### `scripts/model_manager.py`

Commands:

```bash
python scripts/model_manager.py list
python scripts/model_manager.py plan --workflow <id>
python scripts/model_manager.py download --model <id> --approved
```

### `scripts/package_agent_payload.py`

Commands:

```bash
python scripts/package_agent_payload.py --agent dj-vanta
python scripts/package_agent_payload.py --all
```

### `scripts/package_sonicforge_payload.py`

Creates the full fresh-Hermes payload zip.

---

## 8. UI routes

### `/setup`

Local setup dashboard:

- Hermes status
- Comfy endpoint status
- workflow registry status
- model readiness
- closed gates
- next commands

### `/agents`

Installed agent roster:

- DJ VANTA
- template agent
- created custom agents
- modes enabled
- safety status
- workflow bindings

### `/workflows`

Workflow registry UI:

- workflow cards
- required models
- endpoint compatibility
- dry-run button
- blocked real-run button unless approved

### `/terminal-visuals`

Text shader / kinetic terminal / visual spell page.

### `/station?agent=<id>`

Station signal page with selected DJ agent identity.

---

## 9. Security and safety rules

Hard rules:

- No `.env` in payload zips.
- No tokens in manifests.
- No private reference images in public packs.
- No model weights in default zips.
- No model download without explicit `--approved`.
- No `/prompt` call without explicit `--approved` and allow flag.
- No remote endpoint unless `SONICFORGE_ALLOW_REMOTE_ENDPOINT=1`.
- No microphone on by default.
- No recording or streaming by default.
- No public posting.

Workflow prompt safety:

- no real credentials
- no fake QR codes if scanability matters
- QR codes must be programmatic and verified
- no medical/drug-use instruction text
- no copyrighted brand logos as requested output
- no claims that AI invented rave/DJ culture

---

## 10. First build slice recommendation

Implement in this order:

1. `docs/product/FRESH_HERMES_COMFY_AGENT_FACTORY_SYSTEM.md` — this blueprint.
2. `.env.example` with safe placeholders.
3. `agents/dj-vanta/manifest.json`.
4. `agents/template-agent/manifest.json`.
5. `workflows/registry.json` with dry-run placeholder workflows.
6. `docs/integrations/COMFYUI_API.md` fail-closed operator card.
7. `scripts/verify_agent_payloads.py`.
8. `scripts/sonicforge_setup.py doctor`.
9. `/setup`, `/agents`, `/workflows` static pages.
10. Add verifier checks to `scripts/verify.py`.

Only after that:

11. Implement `scripts/comfy_adapter.py preflight` read-only.
12. Implement `scripts/comfy_adapter.py dry-run`.
13. Implement model ledger planning.
14. Ask for explicit approval before downloads or real workflow execution.

---

## 11. Hackathon demo story

Demo sequence:

1. Open `/setup`: fresh install status, Comfy endpoint status, gates closed.
2. Open `/agents`: DJ VANTA plus template agent.
3. Create a new custom DJ agent locally.
4. Open `/station?agent=new-agent`.
5. Open `/terminal-visuals`: custom text spell identity.
6. Open `/workflows`: visual spell / album cover workflows are installed as dry-run contracts.
7. Show model/download ledger: no hidden cost, operator approval required.
8. Explain future: add Comfy endpoint, approve models, run workflows, output custom logos/visuals/album art/VJ loops.

Killer line:

> It is not one AI DJ. It is a station cloning system: Hermes gives it a brain, Comfy gives it a visual workshop, and SonicForge gives it a soul, crate, safety manual, and stage.
