# SonicForge Live Overnight Agentic Build Plan — Midnight to 7AM

Created: 2026-05-01T06:52:30.915871+00:00
Window: 12:00 AM–7:00 AM Pacific, every 10 minutes, final wake report at 7:00 AM.

## Mission

Create the strongest one-day hackathon package for the **world's first Hermes-native autonomous AI DJ/VJ**.

Name stack:
- Product: **SonicForge Live**
- Entity: **DJ VANTA//SonicForge**
- VANTA: **Virtual Autonomous Nocturnal Transmission Artist**
- Core sentence: **OpenClub was the stage. Hermes is the permanent home. SonicForge Live is the first Hermes-native autonomous performer.**

## What makes it a real DJ, not just a generator

The system should model the actual DJ job as a set of synthetic skills:

1. **Crate digging / selection** — choose the next track based on genre, energy, crowd state, time-of-night, and narrative arc.
2. **Beatmatching** — BPM-aware transitions and tempo compatibility.
3. **Phrasing** — transitions on 8/16/32-bar sections, intro/outro awareness, drop timing.
4. **EQ mixing** — plan low/mid/high EQ moves, bass swaps, filter sweeps, and gain staging.
5. **Cueing** — pre-listen / next-track prep modeled as planned segment state.
6. **Crowd reading** — synthetic crowd/vibe state: energy, density, sentiment, dancefloor response.
7. **MC/talk breaks** — short spoken lore/history/safety/hype lines with ducking over intros.
8. **Visual performance** — VJ cue follows audio energy, BPM, section, and spoken theme.
9. **Routing** — local browser/OBS first; Resolume/Spout/TouchDesigner/RTMP adapters opt-in.
10. **Set memory** — do not repeat too much; maintain arc, motifs, history, and identity.

## Culture research to embed

The app should include educational/cultural content as short DJ VANTA interludes:

- DJ culture: beatmatching, phrasing, EQ, crowd reading, crate digging, selector culture.
- Rave culture: underground parties, warehouse/community scenes, DIY flyers, PLUR/safety language, sound-system culture.
- Pacific Northwest/Oregon angle: Portland/Seattle underground and electronic hardware/music communities; treat as respectful scene research, not fake authority.
- New contribution: SonicForge as a new autonomous performer continuing the lineage of selectors, VJs, MCs, sound-system operators, and DIY rave technologists.

Research seeds found tonight:
- Resolume 7.26 release notes mention Arena MCP servers and REST API upgrades; Arena MCP can build/manage compositions, load files/sources, add/remove effects, layers, columns, groups.
- Resolume support docs describe a local Arena MCP server for AI-assisted VJ composition management.
- ComfyUI API path: `/system_stats`, `/object_info`, `/prompt`, WebSocket `/ws`, `/history/{prompt_id}`, `/view`.
- Qwen3-TTS ComfyUI custom node repos exist and are candidates for local/serverless TTS lanes, with voice-cloning consent gates.

## Three-way architecture

### 1. Hermes permanent home

Hermes owns identity, skills, scheduling, files, verification, memory, reports, and safety gates.

### 2. SonicForge local runtime

FastAPI + browser UI:
- control deck: `http://127.0.0.1:8788/`
- VJ window: `http://127.0.0.1:8788/visualizer`
- segment planner: `/api/next-segment`
- future autopilot: `/api/autopilot/start`, `/api/autopilot/stop`, `/api/timeline`

### 3. Swappable media/render backends

Closed by default:
- ComfyUI / Comfy Cloud: visual workflows, Qwen/Voxtral/TTS nodes, code-to-visual packet rendering.
- Modal endpoint: serverless adapter for custom music/TTS/code-visual services.
- RunPod endpoint: ACE-Step/full music generation when approved.
- Resolume Arena MCP: VJ composition/layers/effects when local Resolume MCP is configured.
- TouchDesigner/Spout/Syphon: realtime audio-reactive visuals and pro VJ routing.
- RTMP/OBS: public/private stream publish only when explicitly armed.

## Tonight's autonomous sprint cadence

Each 10-minute job must do exactly one safe concrete increment, verify, and commit if changed.

Preferred increment order:

1. **Research cards**
   - `docs/culture/DJ_CULTURE_RESEARCH.md`
   - `docs/culture/PNW_OREGON_RAVE_RESEARCH.md`
   - `docs/culture/VANTA_INTERLUDES.md`

2. **Autopilot/timeline**
   - Add timeline state and manifest writing.
   - Add `/api/timeline`.
   - Add `/api/autopilot/plan-demo-set` or bounded local loop that creates a 10/20/45-minute set plan without starting providers.

3. **Real DJ feature model**
   - Add schemas for beatmatch, phrase, EQ, cue, crowd signal, transition plan.
   - Add mix plan generator with low/mid/high EQ moves and bar-count phrasing.

4. **Clean local audio artifact**
   - Build simple WAV stitcher/crossfade or program manifest if full mix is too much.
   - Keep generated audio untracked except tiny samples if intentionally approved.

5. **TTS lane**
   - Text-first by default.
   - Add adapter contract for local KittenTTS/QwenTTS/Voxtral, no paid/provider start.
   - Add DJ VANTA talk-break scripts and ducking plan.

6. **ComfyUI/Modal endpoint cards**
   - Add backend cards and `.env.example` variables only.
   - No secrets, no remote jobs.

7. **Resolume Arena MCP integration plan**
   - Add `docs/integrations/RESOLUME_ARENA_MCP.md`.
   - Add adapter contract for composition/layer/effect cue packets.
   - Do not assume Resolume is running; fail closed if MCP unavailable.

8. **Audio-reactive code visuals**
   - Add code packet output that visuals can display/react to.
   - Add browser visualizer modes: terminal code rain, waveform gates, EQ bands, scene text overlay.

9. **Demo polish**
   - Add pitch page, demo runbook, architecture diagram text, acceptance checklist.
   - Make the UI scream “DJ VANTA is alive” within 10 seconds.

10. **Final package**
   - Verify all scripts.
   - Commit cleanly.
   - Create morning report with file paths, features, blockers, and demo instructions.

## Safety boundaries

Closed during unattended work:
- no paid GPU or cloud jobs;
- no RunPod pod start;
- no Comfy Cloud generation;
- no public RTMP publish;
- no public posting/submission;
- no payment or purchase;
- no model training/upload;
- no secret printing or committing;
- no recursive cron creation.

Allowed:
- local code/docs/UI;
- web research summaries with citations;
- mock/local generated manifests;
- local verification;
- local git commits;
- final Telegram report at 7AM.

## Acceptance criteria by 7AM

Green if the repo contains:
- culture research + DJ VANTA interlude scripts;
- real-DJ feature model: beatmatch/phrasing/EQ/cue/crowd/talk/visual routing;
- bounded autopilot/timeline endpoint or script;
- ComfyUI, Modal, RunPod, Resolume MCP adapter contracts/cards;
- demo runbook and pitch;
- verification passing;
- clean git status or documented blockers.

Yellow if backend contracts and docs are strong but autopilot/mix renderer is partial.

Red only if verification fails or safety gates are violated.
