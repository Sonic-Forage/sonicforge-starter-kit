# Priority Addendum — Cloneable DJ Agents + Terminal Visual Spell Engine

Status: priority project addendum
Created from user voice note: 2026-05-01
Project: SonicForge Live / Intergalactic DJs / DJ VANTA

## Core idea

SonicForge Live should not only be a single DJ VANTA demo. It should become a **cloneable performer package**:

> Clone SonicForge, install a payload, and spawn your own custom autonomous DJ / VJ / rave-guide agent.

Each person, crew, venue, creator, or festival can get a custom agent with:

- its own name/personality/lore
- its own DJ taste profile
- its own visual identity
- its own safety boundaries
- its own station signal / intro voice / creator drop
- its own crate-building defaults
- its own album/festival mix style

This turns the hackathon project into a reusable **agent performer factory**, not just one app.

---

## Priority lane A — Cloneable custom DJ agent payloads

### Goal

Package SonicForge Live so someone can run:

```text
git clone <sonicforge-live>
cd sonicforge-live
python scripts/create_dj_agent.py --name "DJ ORBITAL MOTH" --style "psytrance warehouse alien sunrise"
```

Then get a new local custom performer:

```text
agents/dj-orbital-moth/
  AGENT.md
  manifest.json
  persona.md
  safety.md
  crate-profile.json
  visual-profile.json
  station-signal.json
  album-profile.json
  assets/
```

### Product framing

- **DJ VANTA** is the first resident.
- **Intergalactic DJs** is the roster / collective.
- **SonicForge Live** is the operating system.
- **Agent payloads** are the portable performer packs.

### MVP features

1. `agents/dj-vanta/` canonical payload.
2. `scripts/create_dj_agent.py` local generator.
3. `docs/product/CLONEABLE_DJ_AGENT_PAYLOADS.md` spec.
4. `/agents` page showing installed performer payloads.
5. `/station?agent=dj-vanta` style routing later.
6. No secrets, no provider keys, no public deployment in payloads.

### Payload manifest shape

```json
{
  "agent_id": "dj-vanta",
  "display_name": "DJ VANTA",
  "expansion": "Virtual Autonomous Nocturnal Transmission Artist",
  "role": "autonomous_dj_vj_rave_guardian",
  "style_tags": ["cyber-rave", "warehouse", "intergalactic", "harm-reduction"],
  "voice_rules": {
    "ai_is_guest": true,
    "credit_lineage": true,
    "no_dj_replacement_claims": true
  },
  "modes": ["live", "crate", "album"],
  "closed_gates": {
    "starts_gpu": false,
    "publishes_stream": false,
    "records_audio": false
  }
}
```

### Why this matters

This makes the project spreadable:

- DJs can clone and make their own agent.
- Crews can make branded station hosts.
- Venues can make house-party co-pilots.
- Artists can package album/festival personalities.
- Hackathon judges can see this is a platform, not a one-off demo.

---

## Priority lane B — Terminal Visual Spell Engine

### Goal

Build a text-first visual engine that looks like a living terminal / shader / rave signal console:

- terminal popups
- text glyph storms
- barely audio-reactive pulses
- ASCII/ANSI scanlines
- VANTA status lines
- lyrics / MC breaks / survival pings as kinetic typography
- shader-like CRT bloom and chromatic trails
- easy capture into OBS / Spout / Syphon / TouchDesigner later

This should feel organic, local, raw, and alive — like a mad-scientist DJ terminal that can be projected or piped into a real VJ engine.

### MVP architecture

Start browser-local and safe:

```text
/terminal-visuals
  p5.js / WebGL text-shader canvas
  no mic by default
  fake or local amplitude input first
  keyboard/manual trigger controls
  fullscreen mode for OBS/window capture
```

Later approved lanes:

```text
Browser canvas -> OBS window capture
Browser canvas -> Spout/Syphon bridge
Browser canvas -> TouchDesigner Web Render / NDI / Spout
Terminal/ANSI output -> captured as texture
WebSocket audio features -> visual pulse input
```

### Visual modes

1. **Signal Boot**
   - `ACQUIRING VANTA SIGNAL...`
   - station ID scan
   - packet loss / glitch lines
   - cyan/magenta scan beam

2. **Deck Telemetry**
   - Deck A/B BPM/key/energy
   - transition countdown
   - cue-point glyphs
   - phrase bars

3. **Survival Ping Overlay**
   - HYDRATE
   - BUDDY CHECK
   - CHILL ZONE
   - EARPLUGS
   - CONSENT / RESPECT

4. **Intergalactic Text Spell**
   - user-entered phrases become particle fields
   - words break into glyphs and re-form
   - audio amplitude modulates size, bloom, drift, and scanline offset

5. **Agent Clone Identity Screen**
   - each custom DJ agent gets its own boot screen, colors, glyph alphabet, and station ID.

### Shader stack candidates

Browser-first:

- p5.js 2D kinetic typography
- p5.js WEBGL fragment shader
- Canvas 2D + CSS mix-blend-mode
- Three.js later if needed

TouchDesigner later:

- Text TOP / GLSL TOP / Feedback TOP
- AudioSpectrum CHOP -> CHOP to TOP -> GLSL TOP
- Spout/Syphon output after explicit approval

Terminal-first experiments:

- Blessed / Ink / ncurses style local terminal visuals
- ANSI art frames captured by terminal window
- Textual/Rich Python terminal dashboard
- ASCII shader frames piped to OBS or screen capture

### Audio-reactive safety posture

Default is **not microphone-on**.

Phase 1 uses:

- fake amplitude slider
- local demo beat clock
- manual tap tempo
- optional uploaded demo audio only if user approves

Future real audio input requires explicit UI permission and visible status:

```text
MIC INPUT: OFF / ON
RECORDING: false
UPLOADING: false
STREAMING: false
```

### TouchDesigner / Spout note

Do not connect to live TouchDesigner MCP, Spout, Syphon, OBS, or recording in unattended mode. First create dry-run integration docs and keep the browser visualizer as the active fallback.

Future doc:

```text
docs/integrations/TERMINAL_VISUALS_TOUCHDESIGNER_SPOUT.md
```

Required flags:

```json
{
  "starts_gpu": false,
  "starts_paid_api": false,
  "publishes_stream": false,
  "records_audio": false,
  "uploads_private_media": false,
  "requires_human_approval": true
}
```

---

## Priority lane C — Packaging as a forkable hackathon artifact

### Deliverable

A zip/folder/repo structure that can be handed to another person:

```text
sonicforge-live/
  README.md
  QUICKSTART.md
  AGENTS.md
  agents/
    dj-vanta/
    template-agent/
  app/
  server/
  docs/
  scripts/
    create_dj_agent.py
    verify_agent_payloads.py
    package_agent_payload.py
  dist/
    sonicforge-live-agent-pack-YYYYMMDD.zip
```

### Quickstart story

1. Clone repo.
2. Run local app.
3. Open `/station`.
4. Open `/agents`.
5. Create a custom DJ agent from template.
6. Open `/terminal-visuals` fullscreen.
7. Start a dry-run set plan.
8. Capture the visual window into OBS / TouchDesigner manually if desired.

### First implementation slice

Build local, no-provider, no-GPU pieces:

1. Add `agents/dj-vanta/manifest.json`.
2. Add `agents/template-agent/manifest.json`.
3. Add `scripts/verify_agent_payloads.py`.
4. Add `/agents` page.
5. Add `/terminal-visuals` page with p5.js kinetic terminal text and manual amplitude slider.
6. Add docs for cloneable DJ agents and terminal visuals.

### Verification

- agent manifests parse
- required safety gates exist
- `/agents` returns 200
- `/terminal-visuals` returns 200
- no microphone enabled by default
- no stream/record/upload flags enabled
- project verifier passes
- harm-reduction verifier passes
- `git diff --check` passes

---

## Hackathon pitch line

> DJ VANTA is not the product. DJ VANTA is the first clone. SonicForge Live lets anyone fork the performer, give it a soul, give it a crate, give it a visual spell language, and run a safe local-first autonomous party station.

## Immediate priority ranking

1. Cloneable DJ agent payload spec and template.
2. Terminal Visual Spell Engine MVP page.
3. Agent roster page.
4. Packaging script / zip handoff.
5. TouchDesigner/Spout dry-run integration card.
6. Real audio-reactive input only after explicit approval.
