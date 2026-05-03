# SonicForge Live Overnight Task Board

Owner: Hermes/Jimsky overnight autonomous loop
Project: Intergalactic DJs presents DJ VANTA, powered by SonicForge Live
Rule: Each cron run should complete or advance one checkbox, verify, journal, and commit if changed.

## A. Core brand + pitch

- [x] Lock naming hierarchy: SonicForge Live = platform, Intergalactic DJs = show/collective, DJ VANTA = first performer.
- [x] Add the naming hierarchy to README hero copy.
- [x] Add Intergalactic DJs / DJ VANTA copy to the control UI.
- [x] Create `docs/pitch.md` with 30-sec, 90-sec, and judge-facing pitch.
- [x] Create `docs/demo-runbook.md` with exact local demo steps.
- [x] Create `docs/house-party-mode.md` explaining safe local party setup.

## B. Real DJ brain

- [x] Add real DJ transition model for beatmatching/phrasing/EQ/crowd state.
- [x] Expose transition/DJ brain output in `/api/next-segment` response.
- [x] Add `/api/dj-brain/state` or equivalent endpoint.
- [x] Add UI panel for BPM, key/energy, phrase count, EQ move, crowd signal.
- [x] Add crowd-reading synthetic state: warmup, curious, locked-in, peak, cooldown.
- [x] Add crate-digging selector logic: genre, novelty, repetition guard, energy arc.

## C. Autopilot / timeline

- [x] Add bounded demo autopilot endpoint or script that creates 10/20/45 minute set plans.
- [x] Write `generated/timeline/demo-set.json` with segment list, no provider starts.
- [x] Add `/api/timeline` to read current set timeline.
- [x] Add start/stop dry-run autopilot controls in UI.
- [x] Add verifier checks for timeline output shape.

## D. Clean mix + audio artifacts

- [x] Add local program manifest renderer with crossfade/ducking/LUFS metadata.
- [ ] Add simple WAV stitcher/crossfade if safe within time.
- [x] Add talk-over-intro ducking plan per segment.
- [x] Add EQ move schedule per transition: low swap, mid carve, high shimmer.
- [x] Add “honest status” UI: mock audio vs real generated audio vs rendered program.

## E. TTS / MC persona

- [x] Add DJ VANTA culture interlude scripts.
- [x] Add TTS adapter contract for KittenTTS/QwenTTS/Voxtral/Qwen3-TTS.
- [x] Add text-first MC break generator with rave history, safety, hype, and lore modes.
- [x] Add verifier that voice/TTS remains opt-in and does not auto-send audio.

## F. ComfyUI / Modal / RunPod endpoints

- [x] Add `docs/integrations/COMFYUI_API.md` with /system_stats, /object_info, /prompt, /ws, /history, /view flow.
- [x] Add `docs/integrations/MODAL_ENDPOINT.md` for serverless endpoint contract, no GPU start.
- [x] Add `docs/integrations/RUNPOD_ACE_STEP.md` for music generation endpoint contract, no pod start.
- [x] Add `.env.example` endpoint variable names only, no secrets.
- [x] Add backend status card endpoint/UI for closed/open provider lanes.

## G. Resolume / TouchDesigner / VJ routing

- [x] Add `docs/integrations/RESOLUME_ARENA_MCP.md` for local MCP setup and fail-closed cue packets.
- [x] Add Resolume cue packet schema: composition, layer, clip/source, effect, BPM, palette, text overlay.
- [x] Add TouchDesigner/Spout/Syphon routing doc or backend card.
- [ ] Add browser visualizer mode: terminal code rain.
- [ ] Add browser visualizer mode: EQ bands / waveform gates.
- [ ] Add browser visualizer mode: scene text / DJ VANTA subtitle overlay.

## H. Culture / history package

- [x] Create DJ culture research notes.
- [x] Create PNW/Oregon rave research notes.
- [x] Create VANTA interludes.
- [ ] Convert culture notes into in-app rotating interlude/talk-break content.
- [x] Add visible “culture mode” selector in UI: history, hype, safety, lore.

## I. Hermes permanent skill package

- [x] Create `docs/hermes-skill-package.md` explaining how SonicForge becomes a reusable Hermes skill/entity.
- [x] Draft `skills/sonicforge-live-dj-vanta/SKILL.md` inside repo for later installation.
- [x] Add run commands, verification, safety gates, backend contracts, and demo script to the skill draft.
- [x] Add self-test instructions for future Hermes agents.

## J. Self-tests / acceptance / morning package

- [x] Add final demo acceptance checklist manifest/doc.
- [x] Add hackathon demo readiness scorecard.
- [x] Expand `scripts/verify.py` to check new docs/endpoints/UI strings.
- [x] Add local smoke test script for health, UI, visualizer, next-segment, sample-pad, and set-manifest.
- [x] Update README quickstart.
- [ ] Ensure git status clean or documented before 7AM report.

## K. Stretch if everything else is done

- [ ] Generate a sample 5-segment house-party set manifest.
- [ ] Generate a printable Intergalactic DJs flyer/poster prompt pack.
- [ ] Add screenshot/GIF capture instructions.
- [ ] Add OBS scene setup instructions.
- [x] Add hackathon submission checklist.

## L. Rave Survival Kit / party safety edge

- [x] Create `docs/features/RAVE_SURVIVAL_KIT.md`.
- [ ] Add Rave Survival Kit UI panel/toggle.
- [ ] Add `survival` talk-break mode and hydration/earplug/buddy-check interludes.
- [ ] Add calm visual cue for survival interludes.
- [x] Create Intergalactic Rave Survival Kit QR/prop-art plan or artifact.
- [x] Add verifier checks for survival kit copy and no unsafe medical/drug claims.

## M. Text shaders / visual spells

- [x] Create `docs/visuals/TEXT_SHADER_VISUAL_SPELLS.md`.
- [x] Add visualizer mode `code_rain`.
- [x] Add visualizer mode `eq_bands`.
- [x] Add visualizer mode `subtitle_spell`.
- [x] Add visual spell packet to `/api/next-segment`.
- [x] Add Resolume/TouchDesigner cue packet mapping for visual spells.
- [x] Add SDF/MSDF text shader future lane and browser fallback docs/UI.

## N. Careless-LiveDJ inspired dual-deck / ComfyUI pivot

- [x] Add Deck A / Deck B schemas and state to `/api/next-segment`.
- [x] Add equal-power crossfader formula to mix/transition output.
- [x] Add prompt/crate cache seed or doc.
- [x] Add Deck A/B UI cards and incoming-deck status.
- [x] Add sample-pad ritual buttons: VANTA, HYDRATE, BUDDY, DROP, PORTAL, CHILL, AIRHORN, RECORD.
- [x] Add local set manifest writer.
- [x] Add dual ASCII spectrograph/code-rain visualizer.
- [x] Add dry-run ComfyUI visual-spell cue in planner output.
- [x] Add verifier checks for dual-deck/crossfader/ComfyUI/survival strings.

## O. History + harm-reduction guide

- [x] Add rave/DJ history guide with respectful lineage and talk-break lines.
- [x] Add harm-reduction guide with safe scope, red lines, survival kit copy, and sources.
- [x] Add `culture_cue` and `survival_kit` fields to `/api/next-segment`.
- [x] Add UI drawer/panel for Lineage + Rave Survival Kit.
- [x] Add verifier checks that harm-reduction guide forbids medical/drug instructions.

## P. Party Supplies / Bartender / All-Ages Experience

- [x] Create `docs/features/PARTY_SUPPLIES_BARTENDER_LAYER.md` with full design spec.
- [ ] Add `PartyPlan` data model and `/api/party-plan/generate` endpoint (dry-run mock output).
- [ ] Add shopping checklist JSON generation from party inputs.
- [ ] Add all-ages creative beverage menu generator (zero alcohol references).
- [ ] Add 21+ cocktail menu generator behind explicit age-gate toggle.
- [ ] Add mandatory accessibility checklist in every plan (static default items).
- [ ] Add `party_host` talk-break mode with hydration/snack/chill/accessibility/consent rotation.
- [ ] Add `PARTY` sample pad that triggers party-host interlude rotation.
- [ ] Add UI cards: Party Plan Generator, Shopping Checklist, Drink Menu, Accessibility Checklist.
- [ ] Add `party_host` visual mode for browser visualizer (warm amber/green + text overlays).
- [ ] Add verifier checks: no alcohol in all-ages output, age-gate enforcement, accessibility presence, safety redlines, no medical claims, no drinking game language.
- [ ] Integrate with House-Party Mode doc as pre-event planning companion.
- [ ] Add timeline generator for party-host VANTA interludes across event duration.
- [ ] Add export/print views for menus and checklists.
