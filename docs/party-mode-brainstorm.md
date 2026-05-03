# SonicForge Live — Party Mode: Autonomous Party Creator System

**Status:** Product Architecture & Demo Flow Brainstorm
**Date:** 2026-05-01
**Project:** SonicForge Live / Intergalactic DJs / DJ VANTA
**Depends on:** Existing house-party-mode.md (safe local operator mode), parallel-party hub strategy, agent factory system
**Goal:** Turn SonicForge Live from a DJ/VJ _operator tool_ into a **forkable autonomous party creator** — a machine anyone can clone to conceive, plan, score, visualize, and host their own AI-powered party from scratch.

---

## 1. NORTH STAR

> They didn't invite me, so I built the venue. Everyone with autonomous DJs creates their own.

**Thesis:** SonicForge Live Party Mode shifts the product from "you run the DJ" to "you commission the party, and the machine builds it." The system generates a complete party concept, recruits autonomous DJ/VJ agents, plans the energy arc, produces the setlist, designs the visual identity, prints the survival kit, and delivers a ready-to-execute party package — all local-first, safety-gated, and forkable.

**Winning line:** "No golden ticket? No problem. Clone the repo, name your party, arm the agents, and press play."

---

## 2. PARTY MODE CONCEPT HIERARCHY

### 2.1 Three party "flavors" the machine can generate

| Party Type | Audience | Duration | Music Arc | Visual Posture | Survival Tone |
|---|---|---|---|---|---|
| **House Pulse** (under-21 safe) | Friends, roommates, study breaks | 2-4 hrs | Warmup → Groove → Peak → Cooldown | Browser VJ, ASCII spectrogram, code rain | Energetic care, hydration-forward |
| **Warehouse Signal** (21+ / private venue) | Adult house party, studio hang, afterparty | 4-8 hrs | Warmup → Build → Peak → Afterglow | Dark-neon, ComfyUI portal visuals, terminal shaders | Grown-up party host, consent/exit emphasis |
| **Intergalactic Transmission** (all ages / festival) | Livestream audience, venue, festival tent | 1-6 hrs | Signal-acquire → Launch → Orbit → Return | Full ComfyUI/TouchDesigner/Resolume bridge | Festival-ready, buddy system, visible exits |

**Under-21 safe defaults (House Pulse mode):**
- No alcohol references in talk breaks, visual overlays, or party copy
- Hydration station, earplugs, snack bar, chill corner, device charging
- Party concept names: "Neon Study Break," "Cyber Living Room," "Pixel Groove Afternoon"
- Talk-break tone: fun, inclusive, geeky, energizing — never club-exclusive
- Parent/guardian-friendly party summary card available as printable PDF

**21+ Warehouse Signal mode:**
- Responsible service language only: "Bartender's discretion," "Know your limit," "Water between rounds"
- No promotion of excessive consumption, no drinking games, no peer pressure copy
- Explicit consent culture reminders in every third talk break
- Exit/ride-share/buddy system surfaced persistently
- Operator card includes sober monitor designation

### 2.2 Party concept generation pipeline

When a user clicks **Create Party**, the system runs a deterministic concept generator that produces:

```
User input (optional):
  - Party name: "Neon Study Break" (or auto-generated)
  - Vibe words: "chill, cyberpunk, study beats, cozy"
  - Duration: 3 hours
  - Age gate: under-21 | 21+ | all-ages
  - Headcount: ~15 people
  - Space type: living room | basement | backyard | warehouse | festival tent

Machine output:
  ├── Party concept card (name, tagline, vibe palette, genre arc)
  ├── Autonomous DJ lineup (1-4 agents with roles)
  ├── Visual identity pack (color palette, logo prompt, flyer text, overlay style)
  ├── Music energy arc (timeline with BPM/mode/energy per block)
  ├── Survival/safety plan (age-appropriate checklist)
  ├── Supply checklist (physical items the host needs)
  ├── Invite copy (text template for messaging apps)
  ├── Pre-party setup walkthrough (local-first runbook)
  └── Printable QR party card (links to setup page + survival kit)
```

---

## 3. PRODUCT ARCHITECTURE — NEW ROUTES & COMPONENTS

### 3.1 New route: `/party` — Party Creator Dashboard

```
┌──────────────────────────────────────────────────────────────────┐
│  SONICFORGE LIVE — PARTY CREATOR                                 │
│                                                                  │
│  [1] NAME YOUR PARTY              [2] CHOOSE YOUR VIBE           │
│  ┌─────────────────────┐         ┌──────────────────────────┐   │
│  │ party_name: _______ │         │ ○ House Pulse (all ages) │   │
│  │ tagline:  _________ │         │ ● Warehouse Signal (21+) │   │
│  │ age_gate: [▼ 21+]   │         │ ○ Intergalactic (fest)   │   │
│  └─────────────────────┘         └──────────────────────────┘   │
│                                                                  │
│  [3] PICK YOUR AGENTS             [4] SET THE ARC                │
│  ┌─────────────────────┐         ┌──────────────────────────┐   │
│  │ ☑ DJ VANTA (Host)   │         │ duration: [___] hours     │   │
│  │ ☑ BASS-BOT (Prod)   │         │ start BPM: [120]          │   │
│  │ ☐ VISUAL-I (VJ)     │         │ peak BPM:  [140]          │   │
│  │ ☐ LIGHT-SHOW (LD)   │         │ genres: [house, techno]   │   │
│  │ [+ Custom Agent]     │         │ energy curve: [▼ arc]     │   │
│  └─────────────────────┘         └──────────────────────────┘   │
│                                                                  │
│  [5] GENERATE PARTY PACKAGE                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  ▸ Party concept card                                     │   │
│  │  ▸ Agent manifests + Deck A/B assignments                 │   │
│  │  ▸ Music timeline (segments × energy)                     │   │
│  │  ▸ Visual spell deck (per-segment VJ cues)                │   │
│  │  ▸ Survival kit (age-appropriate checklist)               │   │
│  │  ▸ Supply checklist for host                              │   │
│  │  ▸ Invite text templates                                  │   │
│  │  ▸ Printable QR party card                                │   │
│  │                                                           │   │
│  │  [GENERATE PARTY PACKAGE]                                 │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  SAFETY STRIP:                                                    │
│  starts_gpu=false  starts_paid_api=false  publishes_stream=false  │
│  records_audio=false  uploads_private_media=false                │
└──────────────────────────────────────────────────────────────────┘
```

### 3.2 New API endpoint: `POST /api/party/generate`

**Input (PartyConfig schema):**

```json
{
  "party_name": "Neon Study Break",
  "age_gate": "under-21",
  "duration_hours": 3,
  "headcount": 15,
  "space_type": "living_room",
  "vibe_keywords": ["chill", "cyberpunk", "study beats", "cozy"],
  "agent_roles": ["host", "producer"],
  "start_bpm": 110,
  "peak_bpm": 130,
  "genre_arc": ["lo-fi house", "deep house", "progressive"],
  "visual_posture": "browser_vj_ascii",
  "survival_mode": "hydration_forward",
  "invite_tone": "casual_friends",
  "operator_name": "[local only, not committed]",
  "backup_operator": "[local only]",
  "emergency_info": "[local only]",
  "stop_phrase": "HUMAN OVERRIDE: STOP PARTY"
}
```

**Output (PartyPackage schema):**

```json
{
  "ok": true,
  "party_id": "neon-study-break",
  "generated_at": "2026-05-01T19:55:00Z",
  "safety": {
    "starts_gpu": false,
    "starts_paid_api": false,
    "publishes_stream": false,
    "records_audio": false,
    "age_gate": "under-21",
    "alcohol_referenced": false,
    "responsible_service_notice": "Under-21 mode: no alcohol references in any generated content."
  },
  "party_concept": {
    "name": "Neon Study Break",
    "tagline": "Lo-fi photons. Deep focus. Cosmic coziness.",
    "vibe_palette": ["#0a0f1a", "#00ff88", "#7b68ee", "#ff6b9d"],
    "visual_motif": "floating geometric lanterns, ASCII constellation map, soft code rain",
    "description": "A cozy cyberpunk living room party for 15 friends. Chill beats, browser visuals, study-break energy. No alcohol. Snacks, hydration, and good vibes."
  },
  "agent_lineup": [
    {"role": "host", "agent": "DJ VANTA", "deck": "A", "persona_mode": "chill_host"},
    {"role": "producer", "agent": "BASS-BOT", "deck": "B", "persona_mode": "lo_fi_selector"}
  ],
  "energy_arc": {
    "total_segments": 18,
    "blocks": [
      {"block": 1, "minutes": "0-30", "mode": "warmup", "bpm": 110, "energy": 3, "genre": "lo-fi house"},
      {"block": 2, "minutes": "30-90", "mode": "groove", "bpm": 118, "energy": 5, "genre": "deep house"},
      {"block": 3, "minutes": "90-150", "mode": "peak", "bpm": 128, "energy": 7, "genre": "progressive"},
      {"block": 4, "minutes": "150-180", "mode": "comedown", "bpm": 115, "energy": 4, "genre": "ambient house"}
    ]
  },
  "survival_kit": {
    "age_gate": "under-21",
    "checklist": [
      "Water station with cups/bottles",
      "Earplugs near entry",
      "Chill corner with cushions",
      "Snack bar (chips, fruit, granola)",
      "Phone charging station",
      "Trash/recycling bags",
      "Clearly marked bathroom",
      "Sober host / check-in buddy"
    ],
    "talk_break_cadence": {
      "hydration_ping_every": 30,
      "earplug_reminder_at_start": true,
      "buddy_check_every": 60,
      "chill_zone_reminder_after_peak": true
    }
  },
  "invite": {
    "subject": "you're invited: neon study break 🪐",
    "body": "hey! throwing a cozy cyberpunk study-break party this [day]. lo-fi beats, browser visuals, snacks, good people. no alcohol — just chill vibes and cosmic coziness. bring a hoodie and your current obsession. [time] at [place]. powered by sonicforge live (it's a robot DJ, it's cool, i'll explain). text me if you're in. 🎧✨",
    "tone": "casual_friends",
    "include_survival_kit": false,
    "include_qr": true
  },
  "supply_checklist": [
    {"item": "Speaker system / bluetooth speaker", "category": "sound", "essential": true},
    {"item": "Laptop running SonicForge Live", "category": "tech", "essential": true},
    {"item": "Second screen or projector for visuals", "category": "tech", "essential": false},
    {"item": "Extension cords + power strip", "category": "setup", "essential": true},
    {"item": "Water dispenser or bottled water (1L/person)", "category": "survival", "essential": true},
    {"item": "Earplugs (bulk pack)", "category": "survival", "essential": true},
    {"item": "Snacks (chips, fruit, granola bars)", "category": "food", "essential": false},
    {"item": "Cushions / blankets for chill zone", "category": "comfort", "essential": false},
    {"item": "Trash bags + recycling bags", "category": "cleanup", "essential": true},
    {"item": "Phone charging cables (multi-tip)", "category": "tech", "essential": false},
    {"item": "Printed QR code card for setup page", "category": "tech", "essential": false},
    {"item": "Cable tape / gaffer tape", "category": "setup", "essential": true},
    {"item": "Basic first-aid kit", "category": "safety", "essential": true}
  ],
  "setup_runbook": {
    "pre_party_hours": 1,
    "steps": [
      "Clone sonicforge-live repo to laptop",
      "pip install -r requirements.txt",
      "cp .env.example .env",
      "Run verify.py to confirm readiness",
      "Connect laptop to speakers",
      "Set up second screen/projector for /visualizer",
      "Open control deck at http://127.0.0.1:8788",
      "Load this party package: POST /api/party/load/neon-study-break",
      "Verify Deck A/B render correctly",
      "Set hydration timer to 30 minutes",
      "Tape down cables, set up water station",
      "Press PLAY PARTY"
    ]
  },
  "qr_card": {
    "generated": false,
    "note": "QR card generation requires explicit human approval. See /api/party/qr-card.",
    "payload_summary": "Links to party setup page + survival kit for guests who scan."
  }
}
```

### 3.3 New route: `/party/manifest` — Party Package Viewer

A read-only page that displays the generated party package with all sections expandable. Mimics a "receipt" or "boarding pass" aesthetic:

- Header: Party name, tagline, date, age gate badge
- Section cards: Concept, Agent Lineup, Energy Arc, Survival Kit, Invite, Supplies, Setup Runbook
- Copy-to-clipboard buttons on invite text and setup commands
- "Download Party Package" → exports JSON + markdown + printable HTML
- "Load This Party" → feeds the package into the live station (`POST /api/party/load`)

### 3.4 New endpoint: `POST /api/party/load` — Activate Party Mode

Takes a `party_id` and configures the live SonicForge Live station with the party's settings:

- Sets `guide` string from party concept
- Configures agent bindings (which agent on which deck)
- Sets the energy arc parameters (mode sequence, BPM curve, survival cadence)
- Arms survival kit with age-appropriate checklist
- Sets visual spell defaults
- Returns confirmation with Deck A/B ready

### 3.5 New route: `/party/checklist` — Host Readiness Checklist

An interactive pre-party verification page:

- Checkboxes for each supply item
- Green/amber/red status indicators
- "Everything ready? Start the party" button → loads party into station
- Printable view for offline reference

---

## 4. MUSIC ENERGY ARC — THE PARTY'S SPINE

### 4.1 Arc types (selectable by vibe)

| Arc Name | Description | BPM Range | Mode Sequence | Best For |
|---|---|---|---|---|
| **Gentle Rise** | Slow warmup, steady build, modest peak, soft landing | 90→120→100 | warmup→groove→peak→comedown | Study breaks, daytime hangs, all-ages |
| **Warehouse Wave** | Extended intro, long build, sustained peak, long afterglow | 120→140→125 | warmup→build→peak→peak→afterglow | 21+ house parties, studio nights |
| **Festival Orbit** | Quick acquire, rapid launch, high plateau, return signal | 128→145→128 | warmup→build→peak→peak→peak→comedown→afterglow | Livestreams, festival tents, showcases |
| **Chill Current** | Ambient start, deep groove, no hard peak, ambient close | 90→110→95 | warmup→groove→groove→comedown | Background music, dinner parties, creative sessions |

### 4.2 Per-segment generation

Each ~10-minute segment in the arc follows the existing `plan_next_segment()` contract but with party-mode parameters:

- Segment title auto-named: "Neon Rise 01," "Deep Groove 04," "Peak Portal 07"
- BPM follows the arc curve (linear interpolation between block anchors)
- Energy mapped to the arc's energy curve
- Survival kit interventions woven in at configured cadence
- Visual spells tagged with the party's visual motif
- Talk breaks use the party's chosen persona tone

### 4.3 Agent deck rotation

For multi-agent parties, the system alternates which agent "takes the lead" on each segment:

```
Segment 01: Deck A = DJ VANTA (host, warmup intro)
Segment 02: Deck B = BASS-BOT (first track drop)
Segment 03: Deck A = DJ VANTA (talk break + transition)
Segment 04: Deck B = BASS-BOT (groove deepens)
...
```

Agents can also be assigned to "micro-rotations" within a segment (e.g., VANTA handles talk breaks while BASS-BOT handles track selection).

---

## 5. VISUALS — PARTY IDENTITY SYSTEM

### 5.1 Per-party visual identity pack

When a party is generated, the system produces a visual identity pack:

```
generated/parties/neon-study-break/
  ├── identity/
  │   ├── palette.json       # 4-6 hex colors
  │   ├── logo_prompt.txt    # For ComfyUI image generation (approval-gated)
  │   ├── flyer_prompt.txt   # For ComfyUI flyer generation (approval-gated)
  │   └── overlay_styles.json # CSS + ASCII presets
  ├── visual_spells/
  │   ├── spell_deck.jsonl   # Per-segment visual cue deck
  │   └── survival_overlays/ # Hydration/Earplug/Buddy/Chill visual assets
  └── terminal_presets/
      ├── code_rain_config.json
      ├── eq_bands_config.json
      └── subtitle_spell_phrases.txt
```

### 5.2 Visual spell deck

Each segment gets a visual cue that references:

- Base visual mode (code_rain, eq_bands, subtitle_spell, dual_ascii_spectrograph)
- Party color palette applied
- Segment mood (warm, building, peak, cooling)
- Survival overlay if intervention is scheduled
- Text overlay with segment name and BPM

### 5.3 Terminal visual spell engine integration

The existing `/terminal-visuals` route gets party-mode aware settings:

- Party palette injected into WebGL/p5.js shader uniforms
- Segment phrases rendered as glitch-typed ASCII
- Survival pings rendered as overlay banners
- Fullscreen mode optimized for projector/OBS capture

---

## 6. SURVIVAL GUIDE — AGE-APPROPRIATE CARE

### 6.1 Under-21 Survival Kit (House Pulse mode)

```
┌─────────────────────────────────────────┐
│  🪐 NEON STUDY BREAK — PARTY CARE KIT   │
│                                         │
│  ☐ WATER STATION: cups, bottles, easy   │
│    to reach without leaving the room     │
│  ☐ EARPLUGS: near the door — protect    │
│    the ears that brought you here       │
│  ☐ SNACK BAR: chips, fruit, granola,    │
│    nothing that needs a kitchen         │
│  ☐ CHILL CORNER: cushions, low lights,  │
│    phone charging, quiet zone           │
│  ☐ PHONE CHARGING: multi-tip cables,    │
│    power strip, labeled spot            │
│  ☐ BATHROOM SIGN: clearly marked,       │
│    extra toilet paper visible           │
│  ☐ TRASH + RECYCLING: bags out early,   │
│    empty midway through                 │
│  ☐ SOBER HOST: one person stays clear,  │
│    can pause music, handle issues       │
│  ☐ EXITS CLEAR: no blocked doors,       │
│    everyone knows the way out           │
│  ☐ CONSENT REMINDER: visible sign —     │
│    "ask before touch, film, or post"    │
│                                         │
│  DJ VANTA will ping you every 30 min    │
│  with hydration + buddy-check reminders │
│                                         │
│  ⚠ No alcohol. No exceptions.           │
│  ⚠ If someone seems unwell: pause,      │
│    get sober host, call for help.       │
└─────────────────────────────────────────┘
```

### 6.2 21+ Survival Kit (Warehouse Signal mode)

Same base kit PLUS:

- **Responsible service language:** "Bartender's discretion. Know your limit. Water between rounds. Never pressure anyone."
- **Ride-share / designated driver:** QR code or printed info visible near exit
- **Sober monitor:** Designated person who is not drinking, can drive, can handle emergencies
- **No drinking games, no peer pressure copy, no "last call" urgency**
- **Consent culture elevated:** every third talk break includes a consent reminder
- **No references to illegal substances in any generated content**

### 6.3 Survival kit integration with DJ VANTA

The existing `_survival_kit_cue()` function in `server/planner.py` gets party-mode aware:

- Party config determines which checklist is active
- Age gate determines which messages are appropriate
- Party duration determines intervention cadence
- Space type (living room vs warehouse) adjusts language ("water station" vs "hydration tent")

---

## 7. INVITE SYSTEM — THE VIBE BEFORE THE VIBE

### 7.1 Invite tone presets

| Tone | Example opening | Best for |
|---|---|---|
| **casual_friends** | "hey! throwing a thing this saturday..." | House parties, small hangs |
| **mysterious_signal** | "TRANSMISSION ACQUIRED. You are receiving..." | Warehouse/theme parties |
| **festival_crew** | "INTERGALACTIC DJs PRESENTS..." | Bigger events, livestreams |
| **cozy_geek** | "lo-fi photons. deep focus. cosmic coziness." | Study breaks, creative hangs |

### 7.2 Invite template structure

```
Subject: [auto-generated from party concept]

Body:
  [Opening hook — tone-matched]
  [What it is — one sentence]
  [When + where]
  [Vibe description — 2-3 keywords]
  [What to bring — from supply checklist, guest-relevant subset]
  [Age/consent note — if relevant]
  [Powered by SonicForge Live — one fun sentence]
  [RSVP ask]

QR: [generated programmatically, links to party setup page]
```

### 7.3 QR party card

A printable/sharable image that contains:

- Party name + tagline in party visual style
- Scannable QR code → links to `/party/guest/neon-study-break`
- Guest page shows: party info, survival kit, what to bring, house rules
- Generated using verified QR library (not hallucinated by AI image model)
- Can be composed with ComfyUI-generated background art (approval-gated)

---

## 8. LOCAL-FIRST SETUP — THE 60-SECOND PARTY

### 8.1 Pre-party bootstrap script

A new script `scripts/party_bootstrap.py` that:

1. Clones sonicforge-live if not already present
2. Installs requirements
3. Copies `.env.example` → `.env`
4. Runs `verify.py`
5. Starts uvicorn on localhost
6. Opens browser to control deck
7. Prints the party loading command

```bash
python3 scripts/party_bootstrap.py --party-id neon-study-break
```

### 8.2 Docker one-command party

```bash
docker compose -f docker-compose.party.yml up
```

Party-mode docker compose preset that auto-loads a party config from a mounted JSON file.

### 8.3 No-internet fallback

Party Mode works fully offline:
- All party generation is deterministic (no LLM call needed for basic generation)
- Visual spells route to browser canvas (no ComfyUI needed)
- Music uses mock adapter (WAV sketches only)
- Survival kit is static JSON
- Invite text is local template rendering
- QR code generated locally with `qrcode` library

---

## 9. DEMO FLOW — 5-MINUTE PARTY CREATION

### Scene 1 — The invitation we make ourselves (0:00-0:30)

```
Open /party
Hero: "They didn't invite me to the AI party.
       So I built my own venue.
       Everyone with autonomous DJs creates their own."

Three party-type cards:
  [HOUSE PULSE]    [WAREHOUSE SIGNAL]    [INTERGALACTIC TRANSMISSION]
  under-21 safe    21+ private venue     all-ages festival

Click: HOUSE PULSE
```

### Scene 2 — Name and vibe (0:30-1:00)

```
Party name: type "Neon Study Break" (or auto-fill)
Age gate: under-21 (pre-selected)
Space: living room
Headcount: 15
Vibe keywords: chill, cyberpunk, cozy
Duration: 3 hours

Party concept card renders live:
  "Neon Study Break — Lo-fi photons. Deep focus. Cosmic coziness."
  Visual palette: #0a0f1a / #00ff88 / #7b68ee / #ff6b9d
  Agent lineup: DJ VANTA (host) + BASS-BOT (selector)
```

### Scene 3 — Energy arc visualization (1:00-1:30)

```
Energy arc renders as interactive timeline:

  0min ───────────────────────────────────────────── 180min
  [warmup 110bpm] [groove 118bpm] [peak 128bpm] [comedown 115bpm]
  energy ▁▂▃▄▅▆▇██▇▆▅▄▃▂▁

  18 segments auto-generated
  Survival interventions marked: 💧 at 30, 60, 90, 120, 150 min
  Earplug reminder at 0:00
  Buddy check at 60, 120 min
```

### Scene 4 — Generate party package (1:30-2:00)

```
Click: GENERATE PARTY PACKAGE

Terminal-style output panel shows generation:
  ✓ Party concept card
  ✓ Agent manifests (DJ VANTA + BASS-BOT)
  ✓ Energy arc timeline (18 segments)
  ✓ Visual spell deck (18 cues)
  ✓ Survival kit (under-21 checklist)
  ✓ Supply checklist (13 items)
  ✓ Invite text (casual_friends tone)
  ✓ Setup runbook (11 steps)

Package saved: generated/parties/neon-study-break/
```

### Scene 5 — Invite and supplies (2:00-2:30)

```
Show invite text:
  "hey! throwing a cozy cyberpunk study-break party..."

Copy button → clipboard flash

Show supply checklist with checkboxes:
  ☐ Water station
  ☐ Earplugs
  ☐ Snacks
  ☐ Chill corner cushions
  ☐ Extension cords
  ...

Show "Print QR Card" button (generates local QR → ComfyUI art compose, approval-gated)
```

### Scene 6 — Load and play (2:30-3:00)

```
Click: LOAD PARTY → ACTIVATE STATION

Station transitions to party mode:
  ● VANTA ONLINE — Neon Study Break
  Deck A: DJ VANTA (host, warmup intro)
  Deck B: BASS-BOT (first track queued)
  Survival kit: ARMED (under-21 protocol)
  Hydration timer: 30 minutes

Click: PLAY PARTY

  00:03 — "Welcome to Neon Study Break. This is DJ VANTA.
          Lo-fi photons, deep focus, cosmic coziness.
          Water station is by the window, earplugs by the door.
          Let's begin."

  Visualizer shows: party logo in code rain, BPM counter, "WARMUP" overlay
```

### Scene 7 — Respect + close (3:00-3:30)

```
Close card:

  "This is SonicForge Live Party Mode.
   You just created a complete autonomous party in under 3 minutes.
   No API key required. No GPU started. No hidden recording.

   The elite AI party is invite-only.
   The builder party is forkable.

   git clone https://github.com/TheMindExpansionNetwork/sonicforge-live.git
   cd sonicforge-live
   python3 scripts/party_bootstrap.py

   Your party. Your agents. Your room. Your rules.

   PLUR: Peace Love Unity Respect.
   The machine keeps the set alive. The human keeps the room safe."
```

---

## 10. IMPLEMENTATION PLAN

### 10.1 New files to create

```
server/
  party_generator.py        # Party concept/package generator
  party_schemas.py          # PartyConfig, PartyPackage, PartyManifest schemas
  party_routes.py           # FastAPI routes for /party/*

scripts/
  party_bootstrap.py        # One-command local party launcher

app/static/
  party.html                # Party creator dashboard
  party-manifest.html       # Party package viewer
  party-checklist.html      # Host readiness checklist
  party-guest.html          # Guest-facing landing page (QR target)

generated/parties/
  .gitkeep                  # Party packages stored here (gitignored except .gitkeep)

templates/
  invite/                   # Invite text templates by tone
    casual_friends.txt
    mysterious_signal.txt
    festival_crew.txt
    cozy_geek.txt
  survival/                 # Age-gated survival kit templates
    under-21.json
    adult-21-plus.json
    all-ages-festival.json
  supply/                   # Supply checklist templates by space type
    living-room.json
    basement.json
    backyard.json
    warehouse.json
    festival-tent.json

docs/
  party-mode-brainstorm.md  # This document
```

### 10.2 Files to modify

```
server/main.py              # Add party routes
server/schemas.py           # Add PartyConfig, PartyPackage, PartyManifest
server/planner.py           # Make survival_kit_cue party-mode-aware
server/set_manifest.py      # Support party-scoped manifests
app/static/styles.css       # Add party dashboard styles
app/static/main.js          # Add party creation flow
```

### 10.3 Implementation phases

**Phase 1 — Concept generator (deterministic, no API calls)**
- Party name/tagline templating
- Visual palette generation
- Agent lineup assignment
- Energy arc math (BPM interpolation)
- Survival kit template selection
- Supply checklist template selection
- Invite text rendering
- Setup runbook generation

**Phase 2 — Party dashboard UI**
- `/party` creation wizard
- `/party/manifest` package viewer
- `/party/checklist` readiness page
- All safety gates visible and persistent

**Phase 3 — Station integration**
- `POST /api/party/load` → configures live station
- Party-aware survival kit cadence
- Party-aware visual spell defaults
- Party-aware agent deck rotation
- Party-scoped set manifest storage

**Phase 4 — Guest experience**
- `/party/guest/:id` landing page
- QR code generation + verification
- ComfyUI art composition (approval-gated)
- Printable party card

**Phase 5 — Autonomous party runtime**
- Party auto-starts when loaded
- DJ VANTA runs the full set without human input
- Survival pings fire on schedule
- Visual spells rotate with segments
- Human override always armed

---

## 11. SAFETY GATES — NON-NEGOTIABLE

### 11.1 All generated content passes through safety filters

- No alcohol references in under-21 mode
- Responsible service language ONLY in 21+ mode
- No medical claims in survival kit
- No drug references in any mode
- No promotion of illegal activity
- No peer pressure language
- No "drinking games" or "last call" urgency
- No imitation of real people or venues
- No hidden recording, streaming, or uploading

### 11.2 Party config safety schema

```json
{
  "age_gate": "under-21 | 21-plus | all-ages",
  "alcohol_referenced": false,
  "responsible_service_notice": "string (always present in 21+ mode)",
  "consent_culture_active": true,
  "survival_kit_armed": true,
  "sober_host_required": true,
  "human_override_armed": true,
  "starts_gpu": false,
  "starts_paid_api": false,
  "publishes_stream": false,
  "records_audio": false,
  "uploads_private_media": false
}
```

### 11.3 Human override always armed

Every party page shows:
```
⚠ HUMAN OVERRIDE: "STOP PARTY"
  A sober human can pause or stop the set at any time.
  The machine is a guest in the room.
```

---

## 12. SUCCESS CRITERIA

Party Mode is working when:

1. A new user can visit `/party`, click "House Pulse," type a party name, and get a complete party package in under 60 seconds.
2. The generated package includes: concept card, agent lineup, energy arc, survival kit, supply checklist, invite text, and setup runbook.
3. Under-21 mode contains zero alcohol references and uses appropriate survival language.
4. 21+ mode includes responsible service language and consent culture reminders.
5. Loading a party configures the live station with correct agents, BPM arc, and survival cadence.
6. The entire flow works without internet, GPU, paid APIs, or hidden downloads.
7. A human can stop the party faster than the machine can escalate it.
8. The generated party package is a standalone directory that can be shared, forked, or archived.
9. `/party/guest/:id` renders a mobile-friendly guest page with party info and survival kit.
10. Someone who "wasn't invited" can clone the repo and create their own party in under 5 minutes.

---

## 13. CLOSING THESIS

> The elite AI party has a velvet rope. Party Mode tears it down.
>
> You don't need an invitation. You don't need API keys. You don't need a
> GPU cluster. You need a repo, a laptop, some speakers, and a room.
>
> SonicForge Live Party Mode turns every clone into a venue. Every DJ agent
> into a host. Every living room into a parallel party.
>
> They threw a party for the model.
> We built the party the model can run.
> Now you can too.
>
> **git clone and create your own.**
