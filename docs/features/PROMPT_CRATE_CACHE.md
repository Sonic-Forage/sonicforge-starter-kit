# Prompt / Crate Cache Seed

Status: **local seed only** — no provider starts, uploads, paid APIs, public streams, or generated media jobs.

This crate turns the Careless-LiveDJ-inspired prompt-cache idea into SonicForge language: DJ VANTA can pick from reusable prompt packs the same way a human DJ digs from a crate. Each entry carries music intent, deck-transition grammar, a visual-spell line, a safe survival ping, and a respectful lineage note.

Source data: `catalog/crate-cache/prompt-crate-seed.json`

## How the planner uses it

- Match the current `SetState.mode` first.
- Score genre affinity with a mode-specific tag map so warmup/groove/build/peak/comedown/afterglow feel like intentional crate digging instead of random prompt lookup.
- Follow a deterministic energy arc target (`warmup=5`, `groove=6`, `build=7`, `peak=9`, `comedown=4`, `afterglow=3`) before falling back to the requested set energy.
- Apply a three-crate repetition guard by scanning recent queued track prompt metadata for local crate ids; this avoids immediate repeat pulls when the set state already contains a selected crate.
- Add a small novelty preference for genre tags that were not present in the recent crate window.
- Inject the selected entry into Deck B's `prompt_stack` and write `Selected local crate id: ...` into the planned track prompt so future iterations can detect it.
- Surface the selection in `/api/next-segment` as `crate_selection`, including `score_breakdown`, `energy_arc`, and `repetition_guard` fields for UI/demo inspection.
- Keep it honest: these are planning hints only until a mock/local or human-approved backend renders artifacts.

## Seed entries

1. `pnw-warehouse-warmup-001` — grounded warmup crate with earplug/check-in framing.
2. `intergalactic-bass-handoff-002` — build-mode bass handoff with phrase-lock and bar-17 bass-swap language.
3. `rave-survival-cooldown-003` — lower-intensity cooldown crate with hydration/chill-zone cue.
4. `vanta-peak-transmission-004` — peak VANTA/code-rain crate with explicit human-in-charge note.
5. `afterglow-lineage-005` — respectful history/exit/buddy closer.

## Safety boundaries

- This cache does **not** call ComfyUI, RunPod, Modal, Gemini/Lyria, RTMP, or any realtime provider.
- Entries may mention future visuals or audio, but they are local JSON prompts only.
- Survival copy remains practical community care: hydration, hearing protection, buddy checks, exits, chill zone, consent, and human override.
- No medical/legal/drug-use advice, no dosing, no diagnosis, no substance identification.

## Demo line

> DJ VANTA is not just making a random next song. It is crate-digging from a local memory bank: genre, energy, survival ping, lineage note, and visual spell all travel with the incoming Deck B plan.
