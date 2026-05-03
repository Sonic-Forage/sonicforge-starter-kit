# Parallel Party Hub Build Swarm Summary

Report-only DeepSeek Pro brainstorm swarm synthesis used to guide the hub build. No GPU, RunPod, Modal, Comfy generation, stream, recording, download, public post, or cron job was started.

## 01-design-director.retry.out

# SONICFORGE LIVE — HUB PAGE VISUAL SYSTEM

## VISUAL DNA

- **Palette**: `#0a0a0f` (void black) / `#00ff88` (terminal green) / `#ff00aa` (neon magenta) / `#ffaa00` (amber warning) / `#1a1a2e` (deep panel bg) / `#e0e0e0` (body text)
- **Typo**: JetBrains Mono (code/terminal) + Space Grotesk (headings/ui) + a single glitch-effect webfont (Syne Mono) for hero logotype only
- **Aesthetic DNA**: tmux split-panes + Berghain flyer xerox texture + ComfyUI node-edge wires + CRT scanline overlay (CSS pseudo-element, `opacity: 0.03`)
- **Grid**: 12-col CSS Grid with visible 1px `#ffffff08` column rules — the grid is always faintly visible, like graph paper under a mixing desk
- **Background**: animated CSS noise + subtle radial vignette; no stock photos, no gradients that feel SaaS

## ROUTE MAP

| Route | Purpose | Vibe |
|-------|---------|------|
| `/` | The Hub — command center landing | Terminal + rave flyer |
| `/parallel-party` | Live multiverse party simulator | Glitch + node graph |
| `/station` | DJ VANTA streaming deck (existing) | Broadcast console |
| `/agents` | Hermes agent roster & spawner | Process table + ID badges |
| `/workflows` | ComfyUI-style visual workflow builder | Node-edge canvas |
| `/terminal-visuals` | ASCII art / shader gallery | Full CRT throwback |
| `/setup` | One-click local bootstrap | Install wizard but make it rave |
| `/about` | Manifesto + lore (existing) | Zine layout |
| `/vanta` | Visualizer (existing) | Keep as-is |

## `/` HUB PAGE — EXACT SECTION STRUCTURE

### 1. PRELOADER (fullscreen, 1.2s)
- Black screen → green cursor blink → ASCII "SONICFORGE LIVE" types out letter by letter → CRT power-on flash (white frame, 80ms) → fades to hub
- Audio: optional 8-bit kick + hi-hat sting on reveal (muted by default, unmute icon bottom-right)

### 2. HERO HEADER (top 40vh)
```
┌──────────────────────────────────────────┐
│  SONICFORGE LIVE                         │
│  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄   │
│                                          │
│  THE ELITE AI PARTY IS INVITE-ONLY.      │
│  THE BUILDER PARTY IS FORKABLE.          │
│                                          │
│  [ FORK REPO ]  [ LIVE DEMO ]  [ AGENTS ]│
└──────────────────────────────────────────┘
```
- Hero tagline in Space Grotesk 900, letterspaced wide, magenta
- Sub-tagline glitch-cycles between "invite-only" / "forkable" every 4s with a 200ms RGB-split transition
- Three CTA buttons: outlined neon green, no fill, 2px border, hover = fill + scanline wipe

### 3. LIVE SYSTEM STATUS BAR (sticky, full-width, 40px)
```
● ONLINE   ▲ COMMITS: 142   ▲ AGENTS: 3 ACTIVE   ▲ WORKFLOWS: 7   ▲ UPTIME: 12d 4h   ▲ [TERMINAL]
```
- Monospace 11px, green on black, live WebSocket-updated
- Each stat pulses its dot on change
- Click any stat → jumps to that section

### 4. COMMAND CENTER GRID (3-column, below hero)
```
┌─ AGENT ROSTER ──────┬─ LIVE WORKFLOWS ──────┬─ TERMINAL ─────────┐
│ ● hermix-v4    IDLE │ workflow:beatmatch    │ $ ssh sonicforge   │
│ ● jimsky-v2  ACTIVE │ ████████░░ 78%        │ > agent deploy     │
│ ● deepseek-v4 READY │ workflow:stem-sep     │ > workflow run     │
│                      │ ██████████ 100% ✓     │ >                   │
│ [SPAWN NEW AGENT]    │ [NEW WORKFLOW]        │ [_] [□] [X]        │
└──────────────────────┴───────────────────────┴────────────────────┘
```
- Agent roster: process-table style, click row → `/agents#hermix-v4`
- Workflows: mini progress bars styled as LED VU meters
- Terminal: live `$` prompt, accepts commands, outputs styled as green monospace — actual WebSocket to backend shell

### 5. NODE GRAPH TEASER (full-width band, 300px)
- Animated canvas: floating ComfyUI-style nodes with edge wires, each node is a route
- Nodes drift slowly, wires glow on hover
- Node labels: "STATION", "AGENTS", "WORKFLOWS", "SETUP", "TERMINAL"
- Click node → navigate to route; edge wires animate a pulse traveling from clicked node to destination

### 6. FORK CTA STRIP (full-width, dark panel)
```
┌──────────────────────────────────────────────────────────┐
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
│                                                          │
│    git clone https://github.com/themindexpansionnetwork/  │
│              sonicforge-live.git                          │
│                                                          │
│    cd sonicforge-live && pip install -r requirements.txt │
│    python main.py --hub                                  │
│                                                          │
│    ▸ NO API KEY REQUIRED TO START                        │
│    ▸ BRING YOUR OWN MODEL LANE                           │
│    ▸ RESPECT THE PLUR                                    │
│                                                          │
│  [📋 COPY]                    [VIEW SOURCE ON GITHUB ↗]   │
└──────────────────────────────────────────────────────────┘
```
- Dark panel with left-border neon green accent line
- Code block with syntax highlighting (green strings, magenta commands)
- "COPY" button uses Clipboard API, flashes "COPIED ✓" in green for 1.5s

### 7. FOOTER MANIFESTO STRIP
```
BUILT WITH ▸ HERMES AGENT ▸ COMFYUI ▸ FASTAPI ▸ LOVE
PLUR ▸ PEACE LOVE UNITY RESPECT ▸ HARM REDUCTION
© 2026 THE MIND EXPANSION NETWORK ▸ FORKABLE UNDER MIT
```

## MOTION LANGUAGE

- **Page transitions**: horizontal wipe (like switching decks on a DJ mixer), 300ms ease-out
- **Hover states**: 1px → 2px border expansion + 5% brightness increase, no scale transforms (feels hardware, not web)
- **Scanlines**: CSS `repeating-linear-gradient` overlay on all dark panels, subtle and always-on
- **Glitch micro-interactions**: route links do a 2-frame RGB split on click before navigating (CSS keyframe, 80ms)
- **Cursor**: custom `crosshair` on node graph; `text` on terminal; default `default` elsewhere
- **Scroll**: smooth but fast — no parallax, no scrolljacking. This is a tool, not a portfolio.

## SAFETY GATES (built into UI, not buried in docs)

-

---

## 02-hermes-product-architect.out

Now I have a thorough picture of the existing repo, strategy docs, and swarm context. Here's my full brainstorm report:

---

# SonicForge Live — Parallel Party Hub: System Surface Brainstorm

**Model:** DeepSeek V4 Pro direct
**Date:** 2026-05-01
**Mode:** REPORT-ONLY — no file edits

---

## 0. Summary Thesis

The existing pages (`/`, `/about`, `/vanta`, `/station`, `/visualizer`) are a strong local-first DJ control plane. What's missing is the **Hermes-first system surface** — the pages that sell Hermes Agent as an operating system, ComfyUI as a creative department, and SonicForge as the forkable station that proves the thesis.

**North star:** a viewer in under 2 minutes understands:
1. This is a real autonomous DJ/VJ operating system
2. It is local-first, safety-gated, and verifier-backed
3. It can create custom DJ agents and bind them to Comfy workflows
4. It packages into a fresh Hermes build
5. It is bigger than the hackathon — it's cloneable infrastructure

**Thesis line:** *The elite AI party is invite-only. The builder party is forkable.*

---

## 1. New Pages — Concrete Design

### 1.1 `/parallel-party` — The Invitation We Make Ourselves

**Purpose:** Frame the cultural moment respectfully, then redirect to the builder station.

**Visual posture:** Darker and more cinematic than existing pages. A single-column narrative scroll with a countdown/clock motif. Think SpaceX launch page meets warehouse flyer.

**Copy structure:**

```
EYEBROW: 5:55 PM — Two parties. One model launch. One station signal.

HERO:
  Somewhere in San Francisco, a frontier model celebrates its launch.
  Here, Hermes opens a station.

LEDE:
  Intergalactic DJs presents DJ VANTA//SonicForge — a local-first
  autonomous AI DJ/VJ system that anyone can clone, arm, and run.

  Respect to the people throwing the model party.
  This is the open-builder response: a party operating system
  you can fork right now.

THREE CARDS:
  [STATION]              [FACTORY]              [VISUALS]
  Clone the station      Create a DJ agent      Terminal VJ spells
  Acquire a signal ID,   Name it, style it,     Code rain, waveform
  choose local or        bind Comfy workflows,  ghosts, phrase-lock
  RunPod/Modal lane,     generate custom        glyphs, survival
  build a dry-run set.   payload, package it.   pings as projected
                                                light.

CTA ROW:
  [Acquire Station Signal → /station]
  [Create a DJ Agent → /agents]
  [Open Setup Dashboard → /setup]
  [See Workflow Registry → /workflows]
  [Launch Terminal Visuals → /terminal-visuals]

RESPECT BLOCK (smaller, at bottom):
  Respect to OpenAI, Hermes, ComfyUI, the DJs, the VJs, the warehouse
  crews, the sound-system builders, and every dancer who taught us a
  launch can be more than a changelog — it can be a room, a signal,
  and a shared ritual.
  We did not get a golden ticket. So we built a station.

FOOTER BAR:
  starts_gpu=false  starts_paid_api=false  publishes_stream=false
  Hermes-native  ComfyUI-ready  Local-first  Cloneable  Verifier-backed
```

**UI elements:**
- Dark gradient matching existing (ultraviolet/cyan/hot-pink)
- Large countdown clock element (5:55 PM motif — decorative, not real-time dependent)
- Scanline overlay effect (already in CSS toolkit from existing pages)
- Animated "signal acquired" pulse on the CTA buttons
- Respect block rendered in a distinct lower-contrast panel so the builder CTAs dominate

**Safety gates:**
- No auto-playing media
- No hidden API calls
- All CTAs are navigation links only
- Footer safety bar statically renders `starts_gpu=false` etc.

---

### 1.2 `/setup` — Fresh Hermes Readiness Dashboard

**Purpose:** The "prove it" page. Shows that a fresh Hermes install can verify everything before anything dangerous happens. This is the page that impresses Hermes people most.

**Visual posture:** Terminal + dashboard hybrid. Dark panels with monospace status indicators and green/amber/red dots. Think `htop` meets a launch control center.

**Copy and panel structure:**

```
NAV: [Parallel Party] [Setup] [Agents] [Workflows] [Terminal] [Deck]

HERO:
  Fresh Hermes Readiness Dashboard
  Verify your station before anyone arms a lane.

FOUR-COLUMN STATUS GRID:

  [HERMES]
  ● Hermes Agent: present vX.Y.Z
  ● DeepSeek V4 Pro: configured
  ● Skills loaded: N
  ● Gateway: Telegram/Discord ready
  ● Memory: N entries
  → hermes doctor

  [COMFYUI ENDPOINT]
  ○ Endpoint URL: not configured
  ○ /system_stats: unchecked
  ○ /object_info: unchecked
  ○ Workflows: 0 installed
  → configure endpoint

  [MODELS]
  ○ SDXL / Flux / etc: not downloaded
  ○ Download ledger: 0 approved
  ○ VRAM estimate: N/A
  → open model ledger

  [SAFETY GATES]
  ● starts_gpu: false
  ● starts_paid_api: false
  ● publishes_stream: false
  ● records_audio: false
  ● TTS: opt-in only
  All lanes closed — human must arm.

SETUP WIZARD PANEL (collapsible steps):
  STEP 1: Verify Hermes installation      [CHECK] hermes doctor
  STEP 2: Configure API providers          [CHECK] hermes config verify
  STEP 3: Add ComfyUI endpoint URL         [  ]  configure
  STEP 4: Run endpoint health check        [  ]  GET /system_stats
  STEP 5: Audit required models            [  ]  open ledger
  STEP 6: Install workflows                [  ]  install from registry
  STEP 7: Run dry-run smoke test           [  ]  python scripts/verify.py
  STEP 8: Create first DJ agent            [  ]  → /agents

VERIFICATION OUTPUT PANEL:
  Last check: 2026-05-01T18:55:00Z
  scripts/verify.py ....................... PASS
  hermes doctor ........................... PASS
  secret scan ............................. CLEAN
  comfy endpoint .......................... SKIPPED (not configured)
  model ledger ............................ 0 models pending
  0 high-risk patterns in tracked files
```

**Repo artifacts needed:**
- `scripts/sonicforge_setup.py` — the setup wizard CLI that the dashboard calls
- `scripts/verify_comfy_endpoint.py` — pings `/system_stats` and `

---

## 03-comfyui-workflow-architect.retry.out

# SonicForge Live — Forkable Builder Hub Design

## Hero Section (`/` — Landing)

**Tagline (rotating, glitch-typed):**
- "The elite AI party is invite-only. The builder party is forkable."
- "No VIP list. Just `git clone`."
- "PLUR: Pull, Launch, Understand, Remix."

**Visual:** Dark terminal-green matrix rain over a pulsing waveform. ASCII art VU meter in `<pre>` block. Background: low-poly 3D rave geometry (Three.js, <100KB).

**CTA Buttons (3-column card grid):**
- `FORK & RUN` → `/setup` (install-flow)
- `EXPLORE WORKFLOWS` → `/workflows` (registry browser)
- `DEPLOY AGENT` → `/agents` (agent launcher)

**Footer badge:**
```
[ VERIFIED BUILD ] [ COMPOSABLE ] [ MODEL-GATED ] [ ZERO HIDDEN DOWNLOADS ]
```

---

## `/parallel-party` — The Multiverse Party Portal

**Concept:** Every running station is a "room." Rooms are ephemeral WebSocket nodes. No persistent state.

**UI Cards (real-time):**
- **ROOM GRID**: Card per active station. Shows: station name, model lane (DeepSeek/Codex/OpenRouter), current BPM (tempo of workflow execution), queue depth, "vibe" (prompt sentiment emoji).
- **JOIN ROOM**: Click → WebSocket handshake → see prompt queue + workflow graph live.
- **HOST ROOM**: Input station name → spawns a lightweight FastAPI worker. Returns `room_id` + invite link.

**Copy:**
> "Every `git clone` opens a portal. Every station is a parallel party. The multiverse doesn't ask for your email."

**Safety Gate:** Rooms auto-expire after 60min idle. No user auth. Rate-limited prompt queue (5/min per room).

**Artifacts:**
- `routes/parallel_party.py` (FastAPI route)
- `static/js/parallel-party.js` (WebSocket client, room grid with htmx)
- `templates/parallel-party.html`

---

## `/setup` — One-Command Install Flow

**Copy:**
> "One command. No hidden model downloads. Every dependency declared. Every endpoint preflighted."

**UI:**
- **Step cards**: 1. Clone repo → 2. `pip install -r requirements.txt` → 3. `cp .env.example .env` → 4. `python preflight.py` → 5. `uvicorn main:app --port 8788`
- **Preflight results panel**: Shows green/red checks for: Python version, CUDA available (optional), env vars present, model API reachable, ComfyUI endpoint ping.
- **"Warp Run" button**: Calls `/api/preflight` and renders results as a terminal emulator `<pre>` block with green `[PASS]` / red `[FAIL]` lines.

**Safety Gate:** Preflight NEVER downloads models. Only validates endpoints and env vars.

**Artifacts:**
- `preflight.py` (standalone validation script)
- `templates/setup.html`
- `static/css/terminal.css` (green-on-black monospace)

---

## `/agents` — Custom DJ Agent Builder

**Concept:** Visual workshop for composing agent personalities from modular parts.

**Card UI:**
- **AGENT WORKBENCH**: Left panel = component palette (Prompt Template, Model Lane, Tool Registry, Voice Persona, Safety Policy). Right panel = live YAML preview.
- **COMPONENT CARDS (draggable)**:
  - *Prompt Template*: Dropdown of vibe presets ("Hype MC", "Chill Selector", "Tech Explainer", "PLUR Ambassador")
  - *Model Lane*: Radio: DeepSeek V4 Pro / Codex / OpenRouter fallback
  - *Tool Registry*: Checkbox grid: `web_search`, `spotify`, `comfyui_trigger`, `tts_kittentts`, `image_generate`
  - *Voice Persona*: KittenTTS voice selector + pitch slider
  - *Safety Policy*: Rate limit, blocked prompt patterns, content filter level
- **DEPLOY BUTTON** → calls `/api/agents/spawn` → returns agent ID + WebSocket channel.
- **LIVE OUTPUT PANEL**: Streaming agent response in terminal-green `<pre>`.

**Copy:**
> "Build your DJ agent like a modular synth. Patch prompt templates into model lanes. Route tools like FX sends. Every agent is a YAML file — fork it, remix it, drop it in your set."

**Safety Gate:** All spawned agents inherit a mandatory policy envelope: no system prompts with jailbreak patterns, rate-limited API calls, audit log to `~/.sonicforge/agent-logs/`.

**Artifacts:**
- `routes/agents.py`
- `agent_factory.py` (YAML→agent assembler)
- `schemas/agent_config.yaml` (JSON Schema for validation)
- `templates/agents.html`
- `static/js/agent-workbench.js`

---

## `/workflows` — ComfyUI Workflow Registry

**Concept:** Browseable, forkable gallery of prompt→media workflows. Each is a versioned JSON file.

**UI:**
- **WORKFLOW CARDS (grid, filterable by tag)**:
  - Thumbnail (last generated output cached at 256px)
  - Title + author
  - Tags: `musicgen`, `stable-diffusion`, `tts`, `vanta-visual`, `ascii-video`
  - Badges: `[VERIFIED]` `[MODEL: DeepSeek]` `[STEPS: 50]`
  - "TRY IT" button → opens workflow detail
- **WORKFLOW DETAIL PAGE**:
  - Full ComfyUI API JSON (syntax-highlighted `<pre>`)
  - Model manifest: exact model names, hashes, sources
  - Preflight checklist: "This workflow requires: ComfyUI running on port 8188, SDXL base 1.0, ControlNet Canny"
  - "RUN WORKFLOW" → calls `/api/workflows/execute/{id}` → streams progress
  - "FORK" → copies JSON to user's clipboard/local config

**Copy:**
> "No black boxes. Every workflow declares its models upfront. Every prompt is inspectable. Fork the ones you love, improve them, submit a PR."

**Safety Gate:** Workflow execution requires explicit confirmation: modal popup showing ALL models that will be downloaded/loaded. User must click "I understand — execute."

**Artifacts:**
- `routes/workflows.py`
- `workflow_registry/` (directory of versioned JSON files)
- `schemas/workflow_manifest.json`
- `templates/workflows.html` + `templates/workflow-detail.html`
- `static/js/workflow-executor.js`

---

## `/terminal-visuals` — ASCII/Vanta Render Farm

**Concept:** WebSocket-driven terminal art engine. Prompts in → ASCII/Vanta frames out.

**UI:**
- **INPUT BAR**: "Describe the visual..." + vibe selector (cyberpunk, rave, glitch, ambient)
- **LIVE CANVAS**: `<pre>` block with streaming ASCII frames at 15fps via WebSocket
- **RENDER CONTROLS**: Resolution (char width×height), palette (green-phosphor, amber, matrix, vaporwave), frame rate slider
- **EXPORT**: "Save as .txt" / "Save as

---

## 04-hackathon-demo-producer.retry.out

**SonicForge Live — Implementation Brainstorm**
*(Report-only. No edits. No GPUs. No secrets.)*

---

## Narrative Arc

- **Opening gambit:** "They sent velvet-rope invites. We brought the sound system."
- **Thesis:** Invite-only AI launches are status games. Open builders don't need permission — they fork repos and wire things together.
- **Anchor metaphor:** DJ culture. Decks = agent slots. Rave = live demo. Sound system = repo. PLUR = community values.
- **Climax:** `/parallel-party` — four agents run simultaneously in one browser tab. No API key. No waitlist.
- **Resolution:** "Your fork is your rig. Your repo is your party. Press play."

---

## Judge-First Demo Flow (3 Minutes)

- **(0:00)** Cold open: "The elite AI party is invite-only. The builder party is forkable." Hero copy lands.
- **(0:15)** `/terminal-visuals` — full-screen animated ASCII equalizer, DJ VANTA portrait in pyfiglet, scanlines.
- **(0:30)** `/parallel-party` — four-panel split: Prompt → Image → Music → Render. All panels animate pre-canned demo output.
- **(1:00)** `/agents` — four DJ-themed agent cards. DJ VANTA (MC), VISUAL-I (VJ), BASS-BOT (Producer), LIGHT-SHOW (LD). "Swap agents like DJs swap decks."
- **(1:30)** `/workflows` — single killer workflow: "One prompt → full music video." Input/output cards with agent pipeline.
- **(1:50)** `/setup` — `git clone && docker compose up` in a terminal block. "60 seconds to sound system."
- **(2:15)** CTA close: "Fork the party. The repo is public. The velvet rope is gone."
- **(2:45)** Q&A buffer.

---

## Page Hub Architecture

### `/` (Hub — Expand existing)
- **Hero:** "The Elite AI Party Is Invite-Only. The Builder Party Is Forkable."
- **Sub:** "SonicForge Live — Your Open-Source AI Sound System. No API Key. No Waitlist. Just Fork and Build."
- **Visual:** Vanta.js particle background (existing). Terminal-embedded ASCII art at viewport bottom: DJ VANTA spinning.
- **CTA stack:** [Fork the Repo] [Live Demo] [Agent Deck] [60-Second Setup]
- **Footer bar:** PLUR icons (✌️🤝🫶✊) + "Peace (open-source) · Love (community) · Unity (composable agents) · Respect (attribution + safety)"
- **Harm reduction link:** Small, tasteful — rave safety + AI safety resources.

### `/parallel-party` (New — Flagship Page)
- **Tagline:** "Four agents. One tab. Zero permission slips."
- **Layout:** 2×2 responsive grid. Each panel = one agent stage with terminal-style output.
- **Panel 1 — PROMPT:** Input box showing "cyberpunk warehouse rave, 140bpm breakbeat". Output: structured prompt decomposition.
- **Panel 2 — VISUAL-I (VJ):** ComfyUI agent. Shows workflow JSON → preview frame. "SDXL + AnimateDiff chain."
- **Panel 3 — BASS-BOT (Producer):** MusicGen agent. Shows spectrogram → play button. "AudioCraft v2, 30 seconds, .wav."
- **Panel 4 — RENDER:** Final composition. Video embed or animated ASCII. "One pipeline. Open-source. Forkable."
- **Interaction:** Pre-canned demo with "Run Your Own" toggle (gated behind setup check — local mode only, no cloud at demo time).
- **Status indicator:** Each panel has a glowing dot (green = demo loaded, yellow = waiting, off = no backend).

### `/setup` (New — Conversion Page)
- **Hero:** "60 Seconds to Sound System."
- **Command block:**
  ```bash
  git clone https://github.com/yourname/sonicforge-live
  cd sonicforge-live
  docker compose up
  # Open http://localhost:8788
  ```
- **Requirements table:** Python 3.10+, Docker, 8GB RAM. GPU: "Optional. Local mode runs CPU."
- **Architecture diagram:** ASCII-art flow — `Browser → FastAPI → Hermes Agent → ComfyUI → Modal (optional GPU). "Every component swappable. BYO backend."
- **No-API mode callout:** "Zero-config local mode. No API keys. No cloud. Your machine is the venue."
- **Links:** Full README.md, CONTRIBUTING.md, PLUR.md, HARM_REDUCTION.md.

### `/agents` (New — Roster Page)
- **Tagline:** "Swap AI Agents Like DJs Swap Decks."
- **Card grid (4 cards):**
  - **DJ VANTA · MC/Host:** Realtime TTS, personality engine, crowd-work. "The voice of the party."
  - **VISUAL-I · VJ:** ComfyUI workflow agent. SDXL, AnimateDiff, ControlNet. "Visuals that breathe."
  - **BASS-BOT · Producer:** AudioCraft/MusicGen agent. Text-to-music, stem separation. "Bass so deep it needs its own agent."
  - **LIGHT-SHOW · LD:** Shader/visual agent. GLSL, p5.js, TouchDesigner bridge. "Lighting that reads the room."
- **Each card:** Avatar (SVG badge) · Role · Capabilities bullet list · Status dot · "Powered by Hermes Agent" badge.
- **Footer:** "Agents are ComfyUI nodes. Agents are Hermes tools. Plug them together."

### `/workflows` (New — Pipeline Gallery)
- **Tagline:** "Chain Agents Like Effects Pedals."
- **Killer demo workflow — 'One Prompt → Music Video':**
  - Input: "synthwave neon cathedral, 128bpm, breakbeat drop"
  - Pipeline: `[DJ VANTA: Decompose] → [VISUAL-I: Generate keyframes] → [BASS-BOT: Generate audio] → [LIGHT-SHOW: Sync shaders] → [Render: Composite]`
  - Output card: "1 prompt → 30s video + .wav + ASCII visualizer. 47 seconds total. CPU-local mode: 4m 12s."
- **Secondary workflows:** "Text → ASCII Rave Loop", "MIDI → Reactive Visuals", "Playlist → AI VJ Set"
- **Each card:** Inputs · Agent chain diagram · Outputs · Time-to-complete · Hardware requirement badge.
- **Interaction:** Static demo gallery. "All workflows run locally. No cloud dependency."

### `/terminal-visuals` (New — Showcase Page)
- **Tagline:** "This Page Runs in Your Terminal. No Browser Needed."
- **Content:** Full-screen ANSI-art experience. Animated equalizers, particle rain, scanline overlay, DJ VANTA ASCII portrait (pyfiglet `slant` or `doom` font).
- **Color cycle:** Neon cyan (#00ffff) → magenta (#ff00ff) → electric purple (#7b2fbe) on deep black (#0a0a0a).
- **Beat sync:** If audio context available (Web Audio API), equalizer bars pulse to a demo beat. Otherwise, CSS keyframe loop.
- **Footer link:** `nc sonicforge.live 8788` — "Full terminal experience. No browser. Just netcat." (Future feature, placeholder link for demo
