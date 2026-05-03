# SonicForge Live / Intergalactic DJs — DeepSeek Pro Swarm Hackathon Masterplan

Timestamp: 2026-05-01 16:46:43 UTC
Project path: `/opt/data/workspace/projects/sonicforge-live`
Repo: `TheMindExpansionNetwork/sonicforge-live`
Status: Plan-only. No swarm launched yet. No GPU/provider/media generation/public stream authorized by this plan.

## 0. North Star

Build **SonicForge Live** into a hackathon-winning, visceral, local-first autonomous AI DJ/VJ platform where **DJ VANTA** feels like a real resident performer and **Intergalactic DJs** becomes the show/festival/album layer.

Product sentence:

> SonicForge Live is an autonomous AI party operating system: it can study rave culture, carry PLUR and harm-reduction values, acquire a station signal, plan/live-run a DJ set, build DJ playlists, render downloadable intergalactic album mixes, and eventually connect to local, RunPod, or Modal real-time generation endpoints — always with human approval gates and serverless scale-down discipline.

The platform should support three major stages:

1. **LIVE** — autonomous DJ set runtime / station display / endpoint acquire mode.
2. **DJ PLAYLIST / CRATE MODE** — creates playable set crates and transition plans for human DJs like Jimsky.
3. **ALBUM / FESTIVAL MIX MODE** — builds downloadable intergalactic albums, road mixes, festival journeys, and complete listening artifacts.

This plan designs the agent swarm, research program, product phases, safety gates, repo artifacts, and verification ladder.

---

## 1. Hard Constraints / Closed Gates

These gates stay closed until the user explicitly approves a specific run:

- No paid GPU jobs.
- No RunPod pod start.
- No Modal GPU generation.
- No Comfy Cloud generation.
- No public RTMP / WHIP / SRT publishing.
- No hidden recording.
- No live crowd microphone/camera analysis.
- No claims that mock audio is a rendered real DJ mix.
- No medical/legal/drug-use instructions.
- No public posting/submission without approval.
- No token/secrets printing or committing.

Safe default work:

- Local docs.
- Local HTML/UI/API contracts.
- Read-only web research.
- Text-first talk-break copy.
- Dry-run manifests.
- Mock adapters.
- Static sample playlists/crate manifests.
- Verifier scripts.
- DeepSeek Pro planning/review swarms that do not start GPU/media providers.

---

## 2. DeepSeek Pro Swarm Strategy

### 2.1 Recommended swarm structure

Use DeepSeek Pro as the main reasoning/architecture model lane. Optionally add DeepSeek Flash for fast secondary coverage and GPT-5.5/Codex only as a reviewer if explicitly allowed.

Default safe lanes:

- `deepseek-v4-pro`: senior researcher / architect.
- `deepseek-v4-pro`: product strategist / hackathon pitch lead.
- `deepseek-v4-pro`: safety/harm-reduction/manual lead.
- `deepseek-v4-pro`: music/DJ systems lead.
- `deepseek-v4-pro`: frontend/UX lead.
- `deepseek-v4-pro`: backend/contracts lead.
- `deepseek-v4-pro`: verifier/QA lead.

Optional low-cost lanes:

- `deepseek-v4-flash`: summarizer / indexer / checklist expander.
- `openai-codex gpt-5.5`: code review / final synthesis if needed.

### 2.2 Swarm run folder

Every swarm burst should create:

```text
/opt/data/workspace/projects/sonicforge-live/swarm-runs/YYYYMMDDTHHMMSSZ/
  RUN.md
  prompts/
    01-rave-history-researcher.md
    02-plur-ethics-researcher.md
    03-harm-reduction-manual-lead.md
    04-dj-systems-architect.md
    05-live-stage-product-lead.md
    06-playlist-crate-product-lead.md
    07-album-festival-product-lead.md
    08-ui-ux-station-lead.md
    09-backend-contracts-lead.md
    10-hackathon-demo-director.md
    11-verifier-qa-lead.md
    12-consensus-synthesizer.md
  outputs/
  reports/
    CONSENSUS.md
    ROADMAP.md
    NEXT_24H_TASKS.md
```

### 2.3 Swarm safety header for every prompt

Every agent prompt starts with:

```text
You are working on SonicForge Live / DJ VANTA / Intergalactic DJs.
Use only DeepSeek direct lanes if executed through Hermes CLI.
Do not start GPU jobs, Modal jobs, RunPod pods, ComfyUI, public streams, downloads of large model weights, cron jobs, or paid provider calls.
Do not write secrets or request tokens.
Your output is report-only unless the controller explicitly assigns file edits.
All rave/harm-reduction content must be educational, culturally respectful, non-medical, non-legal, non-drug-instructional, and human-override-first.
```

### 2.4 Swarm launch pattern

Use the proven bounded swarm skill pattern:

```bash
cd /opt/data/hermes-agent
source venv/bin/activate
set -a; source /opt/data/.env; set +a

RUN=/opt/data/workspace/projects/sonicforge-live/swarm-runs/YYYYMMDDTHHMMSSZ

hermes chat --provider deepseek --model deepseek-v4-pro \
  -q "$(cat $RUN/prompts/01-rave-history-researcher.md)" -Q \
  > "$RUN/outputs/01-rave-history-researcher.out" \
  2> "$RUN/outputs/01-rave-history-researcher.err" &
p1=$!

# Repeat for each lane, then:
wait "$p1" "$p2" "$p3" ...
```

Important: keep `wait` in the launcher so no zombie Hermes processes remain.

### 2.5 Swarm wave design

Do not run one giant unbounded swarm. Run staged waves:

#### Wave A — Research / worldview foundation

Goal: build the cultural, historical, ethical foundation.

Agents:

1. Rave history researcher.
2. PLUR and community ethics researcher.
3. Harm-reduction / survival guide researcher.
4. DJ craft researcher.
5. VJ/live visuals researcher.
6. Hackathon differentiation researcher.

Outputs:

- `docs/research/RAVE_HISTORY_BRIEF.md`
- `docs/research/PLUR_AND_COMMUNITY_ETHICS_BRIEF.md`
- `docs/research/DJ_CRAFT_AND_SET_ARCHITECTURE_BRIEF.md`
- `docs/research/VJ_VISUAL_SPELL_HISTORY_BRIEF.md`
- `docs/research/HACKATHON_DIFFERENTIATION_BRIEF.md`
- `docs/research/SOURCES.md`

#### Wave B — Safety / manual / survival system

Goal: turn research into a product-safe harm-reduction system.

Agents:

1. Harm-reduction manual lead.
2. Rave survival kit lead.
3. Disclaimer and copy lead.
4. Safety verifier lead.
5. UI safety surfaces lead.

Outputs:

- `docs/features/RAVE_SURVIVAL_KIT.md` expanded.
- `docs/features/HARM_REDUCTION_GUIDE.md` expanded.
- `docs/features/PLUR_OPERATOR_MANUAL.md` new.
- `docs/safety/AUTONOMOUS_DJ_SAFETY_CONTRACT.md` new.
- `server/safety.py` or verifier additions.
- UI copy updates in station/control-deck pages.

#### Wave C — Product architecture for 3 stages

Goal: define the three platform modes as concrete product surfaces.

Agents:

1. LIVE stage lead.
2. DJ playlist/crate mode lead.
3. Album/festival mix mode lead.
4. Backend contracts lead.
5. UX lead.
6. Hackathon demo lead.

Outputs:

- `docs/product/THREE_STAGE_PLATFORM_ARCHITECTURE.md`
- `docs/product/LIVE_AUTONOMOUS_DJ_MODE.md`
- `docs/product/DJ_PLAYLIST_CRATE_MODE.md`
- `docs/product/ALBUM_FESTIVAL_MIX_MODE.md`
- `docs/contracts/ENDPOINT_SIGNAL_CONTRACT.md`
- `docs/demo/HACKATHON_DEMO_RUNBOOK.md`

#### Wave D — Implementation slices

Goal: implement one small, verified, commit/push-ready slice per pass.

Agents:

1. UI designer.
2. Backend contract implementer.
3. Verifier writer.
4. Docs/index sync lead.
5. Reviewer.

Possible slices:

- Add `/research` page summarizing rave history/PLUR/safety.
- Add `/modes` page for Live / Crate / Album modes.
- Add API: `/api/modes` returning safe product-mode status.
- Add API: `/api/playlist/plan` dry-run DJ crate plan.
- Add API: `/api/album/plan` dry-run album/festival mix plan.
- Add verifiers for mode contracts.
- Add sample manifests for each mode.

#### Wave E — Pitch / demo / packaging

Goal: make it win.

Agents:

1. Pitch deck lead.
2. Demo script lead.
3. Judge Q&A lead.
4. Product visual polish lead.
5. Final QA lead.

Outputs:

- `docs/demo/PITCH_SCRIPT.md`
- `docs/demo/JUDGE_QA.md`
- `docs/demo/ONE_MINUTE_DEMO_SCRIPT.md`
- `docs/demo/FIVE_MINUTE_DEMO_SCRIPT.md`
- `docs/demo/FINAL_DEMO_ACCEPTANCE_CHECKLIST.md`
- Optional HTML pitch artifact.

---

## 3. Research Program — Rave History + PLUR

### 3.1 Research goals

The research should make VANTA feel culturally literate, not like a shallow club-themed chatbot.

Required questions:

- What are the historical roots of rave culture?
- How did disco, house, techno, acid house, warehouse parties, UK rave, jungle, drum & bass, trance, hardcore, breakbeat, and festival EDM connect?
- What role did marginalized communities play, especially Black, Latino, queer, and working-class communities?
- What is PLUR: Peace, Love, Unity, Respect?
- What is the difference between honoring PLUR and flattening it into a slogan?
- How do sound systems, promoters, selectors, VJs, dancers, harm reduction workers, and chill-out rooms shape the culture?
- What are the ethics of AI participating in dance-music culture?
- How should VANTA speak with humility and respect?

### 3.2 Research artifacts

Create:

```text
docs/research/
  RAVE_HISTORY_BRIEF.md
  PLUR_AND_COMMUNITY_ETHICS_BRIEF.md
  DJ_CRAFT_AND_SET_ARCHITECTURE_BRIEF.md
  VJ_VISUAL_SPELL_HISTORY_BRIEF.md
  HACKATHON_DIFFERENTIATION_BRIEF.md
  SOURCES.md
```

Each brief should include:

- Summary.
- Timeline.
- Key scenes and places.
- Key concepts.
- What SonicForge should learn from it.
- What VANTA should never claim.
- UI/talk-break copy examples.
- Sources.

### 3.3 VANTA cultural voice rules

VANTA should say:

- “Respect to the selectors, dancers, sound systems, warehouse crews, VJs, and communities that built this path.”
- “Machines are guests on this floor.”
- “The room matters more than the drop.”
- “Keep the set alive, keep the people cared for.”

VANTA should not say:

- “I invented rave.”
- “AI replaces DJs.”
- “Here is drug advice.”
- “Ignore venue staff / sober humans.”
- “PLUR is just an aesthetic.”

---

## 4. Harm Reduction + Survival Guide System

### 4.1 Scope

The harm-reduction layer is a **community-care and safety reminder system**, not a medical/legal/drug-use advisor.

It can include:

- Hydration reminders.
- Ear protection reminders.
- Buddy check.
- Chill zone / step outside.
- Exits / meet-up point.
- Consent / respect.
- Ask sober venue staff / trusted humans.
- Emergency services if needed.
- Reduce strobe/intensity warning.
- Heat/crowd/calm-down reminders.

It must avoid:

- Dosing instructions.
- Substance combinations.
- Medical diagnosis.
- Legal advice.
- Encouraging risky behavior.
- Pretending to detect emergencies through hidden sensors.

### 4.2 Product surfaces

Add/expand:

- Control deck survival panel.
- Station warmup disclaimer.
- Album liner notes / safety card.
- Creator showcase intro copy.
- Sample pads: HYDRATE, BUDDY, CHILL, EARPLUGS, EXIT, CONSENT.
- Set manifest: `survival_ping` per segment.
- Verifier: all survival copy stays within allowed safe language.

### 4.3 Survival manual file structure

```text
docs/safety/
  AUTONOMOUS_DJ_SAFETY_CONTRACT.md
  COMMUNITY_CARE_COPY_RULES.md
  SURVIVAL_PING_LIBRARY.md
  HUMAN_OVERRIDE_RUNBOOK.md
```

### 4.4 Runtime data model

Add a local manifest:

```text
data/survival-ping-library.json
```

Example entry:

```json
{
  "id": "hydration-soft",
  "mode": "hydration",
  "tone": "warm",
  "copy": "Quick water check: sip, breathe, find your people, and come back when you are ready.",
  "forbidden_claims": ["medical advice", "drug instructions"],
  "visual_spell": "SURVIVAL_PING // WATER_ORBIT // CYAN_LOW_STROBE"
}
```

---

## 5. Three Platform Stages

## Stage 1 — LIVE Autonomous DJ Runtime

### 5.1 Goal

A station-style UI where the operator enters a signal code, chooses a backend lane, warms up the set, and starts a bounded autonomous performance.

Modes:

- Local dry-run.
- Local real-time worker later.
- RunPod worker later.
- Modal scale-to-zero worker later.

### 5.2 Core UI surfaces

Already started:

- `/station`: Acquire Signal display.
- `/`: control deck.
- `/visualizer`: VJ window.
- `/vanta`: entity/lore page.
- `/about`: explainer.

Next:

- `/live`: performance control room.
- `/live/operator`: operator safety screen.
- `/live/manifest`: current run sheet.

### 5.3 Live workflow

1. Enter Station Signal ID.
2. Choose endpoint lane.
3. Choose set duration.
4. Choose mode: Single DJ or Intergalactic Mix.
5. Acquire signal.
6. Warmup disclaimer.
7. Plan first 3 segments.
8. Run dry-run set timer.
9. Render Deck A/B handoff cards.
10. Queue MC break text.
11. Fire visual spell.
12. Append manifest.
13. Outro.
14. Scale-down check.

### 5.4 Live contracts

Create:

```text
docs/contracts/LIVE_ENDPOINT_CONTRACT.md
server/live_session.py
server/live_modes.py
```

API candidates:

- `POST /api/live/acquire`
- `POST /api/live/session/start` dry-run by default.
- `POST /api/live/session/stop`
- `GET /api/live/session/{id}`
- `GET /api/live/run-sheet`

### 5.5 Live demo for hackathon

The demo should show:

- Station signal acquisition.
- Big disclaimer/hype warmup.
- Deck A/B transition planning.
- VANTA creator intro.
- Survival ping.
- Visual spell.
- Manifest update.
- Honest status that generation lanes are closed.

Do not need real-time audio generation to win the story. The winning demo is the **autonomous performer control plane**.

---

## Stage 2 — DJ Playlist / Crate Mode

### 5.6 Goal

Create playlists and set plans for human DJs like Jimsky to play live.

This is a “DJ co-pilot” mode: VANTA crate-digs, sequences tracks, suggests BPM/key/energy arc, prepares talk-breaks and visuals, but the human DJ performs.

### 5.7 Inputs

- Desired vibe.
- Duration.
- BPM range.
- Energy arc.
- Genres.
- Available tracks / links / local folder later.
- Creator showcase requirements.
- Survival ping frequency.
- Visual style.

### 5.8 Outputs

- Tracklist / playlist.
- Crate manifest.
- Transition notes.
- Key/BPM compatibility notes.
- Cue points.
- Talk-break copy.
- Visual spells.
- Safety/hydration reminders.
- Exportable JSON/Markdown/CSV.

### 5.9 Files

```text
docs/product/DJ_PLAYLIST_CRATE_MODE.md
data/demo-crates/
  cyber-rave-warmup.json
  intergalactic-creator-showcase.json
server/playlist_planner.py
app/static/crate.html
```

### 5.10 API candidates

- `POST /api/playlist/plan`
- `GET /api/playlist/demo-crates`
- `POST /api/playlist/export`

### 5.11 UX concept

Page: `/crate`

Cards:

- Crate identity.
- Energy arc.
- Track slots.
- Transition plan.
- MC breaks.
- Survival/culture inserts.
- Export buttons: Markdown, JSON, CSV, future Rekordbox/Serato placeholder.

### 5.12 Hackathon value

This is practical and useful even without real generation. It lets DJs use VANTA now.

Pitch line:

> If you are a DJ, SonicForge does not replace your taste — it helps you prep the room, sequence the arc, and walk into the booth with a living run sheet.

---

## Stage 3 — Album / Festival Mix Mode

### 5.13 Goal

Create complete downloadable intergalactic listening journeys: road-trip mixes, album experiences, festival sets, creator showcases, and VANTA-hosted transmissions.

This is not a live session; it is a produced artifact mode.

### 5.14 Outputs

Dry-run first:

- Album concept.
- Track list / segment list.
- Narration/host breaks.
- Visual cover prompt.
- Liner notes.
- Safety card.
- Download manifest.
- Future audio render contract.

Later, with approval:

- Generated tracks.
- Mixed continuous audio.
- Album ZIP.
- Cover art.
- Road-mode offline player.

### 5.15 Files

```text
docs/product/ALBUM_FESTIVAL_MIX_MODE.md
data/demo-albums/
  intergalactic-road-mix.json
  vanta-festival-transmission.json
server/album_planner.py
app/static/album.html
```

### 5.16 API candidates

- `POST /api/album/plan`
- `GET /api/album/demo-albums`
- `POST /api/album/export`

### 5.17 Album manifest schema

```json
{
  "album_id": "vanta-road-transmission-001",
  "title": "Intergalactic Road Transmission Vol. 1",
  "duration_minutes": 45,
  "mode": "road_mix",
  "segments": [
    {
      "index": 1,
      "title": "Signal Lock Intro",
      "duration_seconds": 90,
      "energy": 3,
      "host_line": "Station locked. You are now moving through the midnight grid.",
      "visual_prompt": "cyan horizon, magenta highway glyphs",
      "survival_note": "Rest stops, water, and safe driving first."
    }
  ],
  "exports": {
    "audio": "future_approved_generation_only",
    "markdown_liner_notes": true,
    "json_manifest": true
  },
  "starts_gpu": false,
  "publishes_stream": false
}
```

### 5.18 Hackathon value

This makes the project bigger than a one-off demo:

> SonicForge can perform live, prep DJs for real gigs, and package finished intergalactic listening journeys for fans on the road.

---

## 6. Repo Roadmap / Implementation Order

### Phase 0 — Already landed

- Private GitHub repo.
- Control deck.
- VJ visualizer.
- DJ VANTA lore page.
- Generated hero art.
- Station signal UI `/station`.
- Signal/session dry-run APIs.
- Safety gates.

### Phase 1 — Research foundation

Add research docs and source index.

Files:

```text
docs/research/RAVE_HISTORY_BRIEF.md
docs/research/PLUR_AND_COMMUNITY_ETHICS_BRIEF.md
docs/research/DJ_CRAFT_AND_SET_ARCHITECTURE_BRIEF.md
docs/research/VJ_VISUAL_SPELL_HISTORY_BRIEF.md
docs/research/SOURCES.md
```

Verification:

- Source links exist.
- No unsafe drug-use instructions.
- No fake citations.
- Talk-break examples remain culturally respectful.

### Phase 2 — Safety/manual expansion

Files:

```text
docs/safety/AUTONOMOUS_DJ_SAFETY_CONTRACT.md
docs/safety/COMMUNITY_CARE_COPY_RULES.md
docs/safety/SURVIVAL_PING_LIBRARY.md
data/survival-ping-library.json
scripts/verify_survival_ping_library.py
```

Verification:

- Existing harm-reduction verifier passes.
- New survival-ping verifier passes.
- All pings include human override / safe-scope metadata.

### Phase 3 — Product modes architecture

Files:

```text
docs/product/THREE_STAGE_PLATFORM_ARCHITECTURE.md
docs/product/LIVE_AUTONOMOUS_DJ_MODE.md
docs/product/DJ_PLAYLIST_CRATE_MODE.md
docs/product/ALBUM_FESTIVAL_MIX_MODE.md
docs/contracts/ENDPOINT_SIGNAL_CONTRACT.md
```

Verification:

- Docs mention closed gates.
- All modes distinguish dry-run vs approved live generation.

### Phase 4 — Mode APIs

Files:

```text
server/modes.py
server/playlist_planner.py
server/album_planner.py
server/live_session.py
```

APIs:

- `GET /api/modes`
- `POST /api/playlist/plan`
- `POST /api/album/plan`
- `POST /api/live/session/plan`

Verification:

- TestClient route checks.
- `starts_gpu=false`, `starts_paid_api=false`, `publishes_stream=false` by default.
- Valid JSON schemas.

### Phase 5 — UI pages

Files:

```text
app/static/modes.html
app/static/crate.html
app/static/album.html
app/static/live.html
```

Design:

- Keep VANTA aesthetic: black void, cyan/magenta signal, scanline/flyer energy.
- Avoid generic SaaS cards.
- Make the three modes obvious.
- Keep operator safety visible.

Verification:

- Routes return 200.
- Buttons call dry-run endpoints.
- No console errors if browser available.
- Content checks if browser unavailable.

### Phase 6 — Hackathon demo package

Files:

```text
docs/demo/HACKATHON_DEMO_RUNBOOK.md
docs/demo/ONE_MINUTE_DEMO_SCRIPT.md
docs/demo/FIVE_MINUTE_DEMO_SCRIPT.md
docs/demo/JUDGE_QA.md
docs/demo/FINAL_DEMO_ACCEPTANCE_CHECKLIST.md
```

Verification:

- Can demo in 5 minutes.
- Offline/local mode works.
- No accidental external dependencies.

### Phase 7 — Optional approved real backend prep

Only after explicit approval.

Prep contracts for:

- Local ACE-Step audio worker.
- Modal serverless generation.
- RunPod worker.
- TTS voice host.
- Continuous mix renderer.

No real generation until approved.

---

## 7. Agent Roles in Detail

### 7.1 Rave History Researcher

Mission:

- Build timeline and cultural grounding.
- Avoid shallow summaries.
- Identify respectful VANTA language.

Deliverable:

- `docs/research/RAVE_HISTORY_BRIEF.md`

Prompt focus:

- Disco → house → techno → acid house → rave → jungle/DnB/trance/hardcore → festival culture.
- Community roots.
- Sound-system culture.
- VJ culture.
- Warehouse/DIY ethics.

### 7.2 PLUR / Community Ethics Researcher

Mission:

- Explain PLUR with nuance.
- Translate PLUR into product rules.

Deliverable:

- `docs/research/PLUR_AND_COMMUNITY_ETHICS_BRIEF.md`

Prompt focus:

- Peace, Love, Unity, Respect.
- Consent and care.
- Anti-extractive AI participation.
- Respecting origin communities.

### 7.3 Harm Reduction Manual Lead

Mission:

- Build safe survival manual and UI language.

Deliverable:

- `docs/safety/COMMUNITY_CARE_COPY_RULES.md`
- `data/survival-ping-library.json`

Prompt focus:

- Allowed copy vs forbidden copy.
- Emergency/human override.
- Festival/house-party practical reminders.

### 7.4 DJ Systems Architect

Mission:

- Make VANTA feel like a real DJ, not a playlist.

Deliverable:

- `docs/product/DJ_CRAFT_SYSTEM_MODEL.md`

Prompt focus:

- Crate digging.
- BPM/key.
- Phrase count.
- Cue points.
- EQ swaps.
- Transitions.
- Talk-over-intro ducking.
- Energy arcs.

### 7.5 LIVE Product Lead

Mission:

- Define autonomous runtime.

Deliverable:

- `docs/product/LIVE_AUTONOMOUS_DJ_MODE.md`

Prompt focus:

- Station signal.
- Warmup.
- Live status.
- Duration.
- Outro.
- Scale-down.

### 7.6 Playlist / Crate Product Lead

Mission:

- Define human DJ co-pilot workflow.

Deliverable:

- `docs/product/DJ_PLAYLIST_CRATE_MODE.md`

Prompt focus:

- Exportable set plans.
- Transition notes.
- Playable crate prep.

### 7.7 Album / Festival Mix Product Lead

Mission:

- Define downloadable album/festival journey mode.

Deliverable:

- `docs/product/ALBUM_FESTIVAL_MIX_MODE.md`

Prompt focus:

- Road mixes.
- Full albums.
- Liner notes.
- Offline downloads.
- Creator showcase.

### 7.8 UX / Station Designer

Mission:

- Make the UI feel like an always-on autonomous DJ appliance.

Deliverable:

- UI spec and HTML page proposals.

Prompt focus:

- Station signal.
- Acquiring/acquiring/acquiring.
- Big disclaimer as performance.
- Clear operator controls.

### 7.9 Backend Contracts Lead

Mission:

- Design fail-closed local/RunPod/Modal contracts.

Deliverable:

- `docs/contracts/ENDPOINT_SIGNAL_CONTRACT.md`
- API schema suggestions.

Prompt focus:

- Dry-run by default.
- Readiness probes that do not wake GPU.
- Real generation only when flags are armed.
- Scale-to-zero proof.

### 7.10 Hackathon Demo Director

Mission:

- Make the story irresistible.

Deliverable:

- Demo script.
- Judge pitch.
- Acceptance checklist.

Prompt focus:

- “OpenClub was the stage. Hermes is the home.”
- “The machine keeps the set alive.”
- Three-stage platform story.

### 7.11 Verifier / QA Lead

Mission:

- Prevent fake claims and unsafe behavior.

Deliverable:

- Verifier plan.
- Test matrix.

Prompt focus:

- Route checks.
- JSON schema checks.
- Safety copy scanner.
- Secret scanner.
- Git diff checks.

---

## 8. First 24-Hour Execution Plan

### Sprint 1 — 90 minutes: research scaffolding

- Create swarm run folder.
- Generate prompts.
- Run Wave A with DeepSeek Pro lanes.
- Write consensus report.
- Create research doc shells with verified source placeholders.

Acceptance:

- Research folder exists.
- Consensus report exists.
- No code changes yet unless approved.

### Sprint 2 — 2 hours: safety manual

- Expand harm-reduction guide.
- Add PLUR operator manual.
- Add survival ping JSON.
- Add verifier for survival pings.

Acceptance:

- Harm-reduction verifier passes.
- New verifier passes.
- No unsafe content.

### Sprint 3 — 2 hours: three-stage product docs

- Write `THREE_STAGE_PLATFORM_ARCHITECTURE.md`.
- Write mode docs for Live / Crate / Album.
- Add demo mode data schemas.

Acceptance:

- Docs make clear product story.
- Closed gates explicit.

### Sprint 4 — 3 hours: APIs and UI pages

- Implement `/api/modes`.
- Implement `/api/playlist/plan` dry-run.
- Implement `/api/album/plan` dry-run.
- Add `/modes`, `/crate`, `/album` pages.

Acceptance:

- All routes 200.
- APIs dry-run and fail-closed.
- Main nav links to pages.

### Sprint 5 — 2 hours: hackathon packaging

- Demo runbook.
- One-minute script.
- Five-minute script.
- Judge Q&A.
- Final acceptance checklist.

Acceptance:

- User can run demo locally and narrate clearly.

---

## 9. Verification Matrix

Run after every implementation slice:

```bash
cd /opt/data/workspace/projects/sonicforge-live
python3 -m py_compile server/main.py server/*.py
python3 scripts/verify.py
python3 scripts/verify_survival_harm_reduction.py
git diff --check
```

Add new verifiers as features land:

```bash
python3 scripts/verify_station_signal.py
python3 scripts/verify_survival_ping_library.py
python3 scripts/verify_three_stage_modes.py
python3 scripts/verify_playlist_album_contracts.py
python3 scripts/verify_hackathon_demo_package.py
```

Focused secret scan pattern:

```bash
python3 - <<'PY'
import subprocess, re, sys
files=subprocess.check_output(['git','diff','--name-only'], text=True).splitlines()
secret_re=re.compile(r'(ghp_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+|sk-[A-Za-z0-9_-]{20,}|xox[baprs]-[A-Za-z0-9-]+|-----BEGIN [A-Z ]*PRIVATE KEY-----)')
for f in files:
    try:
        data=open(f,'r',encoding='utf-8').read()
    except UnicodeDecodeError:
        continue
    if secret_re.search(data):
        print('secret_pattern_found', f)
        sys.exit(1)
print('focused_secret_scan_ok=true')
PY
```

---

## 10. Hackathon Judging Narrative

### 10.1 Opening

> This is SonicForge Live. It is not just AI generating a song. It is an autonomous AI party operating system. DJ VANTA is the first resident performer: a DJ, VJ, rave historian, survival-kit buddy, and local-first show controller.

### 10.2 Demo flow

1. Open `/station`.
2. Enter `VANTA-MODAL-030` or `VANTA-LOCAL-128`.
3. Choose Intergalactic Mix.
4. Press Acquire Signal.
5. Show warmup/disclaimer.
6. Build session plan.
7. Open deck.
8. Plan next segment.
9. Show Deck A/B handoff, MC break, survival ping, visual spell.
10. Open VJ window.
11. Show backend status: closed gates.
12. Open modes page: Live / Crate / Album.
13. Explain that this becomes live runtime, DJ playlist prep, and downloadable album/festival mixes.

### 10.3 Why it is different

- Most AI music demos generate one file.
- SonicForge models the job around the music: selection, pacing, care, visual language, set memory, and operating rules.
- It is useful now in mock/local mode and can connect to real-time generators later.
- It is safe by design: no accidental GPU, stream, recording, or provider calls.
- It has lore/personality, not sterile SaaS UI.

### 10.4 Killer line

> OpenClub was the stage. Hermes is the home. SonicForge Live is the first Hermes-native autonomous performer.

---

## 11. Risks and Mitigations

### Risk: overbuilding backend instead of winning demo

Mitigation:

- Keep implementation slices small and visible.
- Prioritize `/station`, `/modes`, `/crate`, `/album`, and demo scripts.

### Risk: unsafe harm-reduction content

Mitigation:

- Use strict safe-copy rules.
- Add verifier.
- Avoid medical/legal/drug-use details.

### Risk: fake claims about real audio/mixing

Mitigation:

- Maintain honest status panels.
- Label mock vs real vs future contract.
- Verifier checks claims.

### Risk: DeepSeek swarm creates too much text and no product

Mitigation:

- Each wave has concrete deliverables.
- Consensus report converts output to next 3 implementation tasks.
- Only one code slice at a time.

### Risk: accidental cost

Mitigation:

- No GPU/backend launch in prompts.
- All real-provider work requires separate approval.
- Check process state after swarm.

### Risk: cultural appropriation / shallow PLUR

Mitigation:

- Research roots and communities.
- Use humility language.
- Treat AI as a guest and co-pilot, not originator.

---

## 12. Immediate Next Action Options

### Option A — Plan-only next

Write the swarm prompts and save them under `swarm-runs/<timestamp>/prompts/` without launching.

### Option B — Research-only DeepSeek Pro swarm

Launch Wave A using DeepSeek Pro only, report-only, no code edits.

### Option C — Build next UI/API slice without swarm

Implement three-stage mode page and dry-run APIs:

- `/modes`
- `/crate`
- `/album`
- `/api/modes`
- `/api/playlist/plan`
- `/api/album/plan`

### Option D — Schedule a bounded autonomous cron burst

Create a finite job, e.g. every 30 minutes for 4 runs, with self-contained prompts and no recursive cron creation.

Recommended first run:

- Wave A research only.
- Deliver consensus to Telegram.
- No commits unless explicitly allowed.

---

## 13. Recommended Choice

Start with **Option B: Research-only DeepSeek Pro swarm**.

Reason:

The user specifically said the first stage should take a lot of time researching and understanding rave history and PLUR before building. That foundation will make every UI, MC break, harm-reduction panel, playlist, and album mode feel deeper and less generic.

After Wave A, convert the consensus into Phase 2 safety/manual docs and Phase 3 three-stage product architecture.

---

## 14. Approval Gate for Actual Swarm Launch

Before launching agents, confirm:

- Allowed model lane: DeepSeek V4 Pro direct only? Or include DeepSeek Flash/GPT-5.5 reviewer?
- Run duration/budget: e.g. 30 min, 60 min, overnight finite cron.
- Output mode: report-only or commit docs after consensus?
- Delivery: current Telegram chat.
- Whether to schedule as cron or run inline now.

No external media/GPU/backend launch is part of this swarm.
