# Careless-LiveDJ Inspiration Intake → SonicForge Live / ComfyUI Pivot

Captured: 2026-05-01T07:46:02.007897+00:00
Source: https://github.com/MushroomFleet/Careless-LiveDJ
Local review clone: `/opt/data/workspace/candidates/Careless-LiveDJ`
Reviewed source commit: `6a37d7f`
License observed: Apache-2.0.

## Why this matters

Careless-LiveDJ is not just another music generator concept. Its useful pattern is a **real DJ rig wrapped around live AI generation**:

- two simultaneous live generation decks / plates;
- real crossfader and deck gain model;
- beat sync / timing discipline;
- prompt caches per deck;
- file decks and local track library;
- sample pads;
- master recording / crash recovery;
- spectrograph-first interface;
- MIDI / automation lane framing;
- local BYOK / secret handling.

For SonicForge Live, we should not clone its app literally. We should absorb the **dual-deck performance grammar** and swap the generation backend from Lyria/Gemini into our safer swappable lanes:

```text
Deck A / Deck B
  → SonicForge planner decides prompt + BPM + role
  → mock/local now
  → future RunPod ACE-Step or Modal music endpoint for audio
  → ComfyUI for visual/cover/poster/VJ frames
  → browser control deck + visualizer first
```

## Best ideas to steal/adapt ethically

### 1. Dual-deck AI rig

Use two conceptual decks:

- **Deck A**: current groove / playing segment.
- **Deck B**: next generated segment / incoming portal.

Each deck needs:

- prompt stack;
- BPM/key/energy config;
- status pill;
- generated audio artifact/path;
- visual spell cue;
- safety/compliance warning if prompt is filtered or unavailable;
- reconnect/regenerate/retry button.

### 2. Equal-power crossfader

Careless uses the classic equal-power curve:

```text
gainA = cos((value + 1) / 2 * PI / 2)
gainB = sin((value + 1) / 2 * PI / 2)
```

SonicForge should expose this as both:

- UI visualization on the control deck;
- JSON in `mix.crossfader_curve` / `transition.crossfader_plan`.

### 3. Prompt cache / crate cache

Turn prompt memory into **crate digging**:

- last 30 prompt packs;
- genre/energy labels;
- “PNW warehouse warmup,” “intergalactic bass handoff,” “rave survival cooldown,” etc.;
- one-click recall into Deck A or Deck B.

### 4. Sample pad as party ritual triggers

Instead of only audio one-shots, SonicForge sample pads should trigger:

- airhorn / riser / noise burst placeholder;
- VANTA voice tag;
- survival kit reminder;
- visual spell overlay;
- “buddy check” / “hydration ping” / “lights low” cues.

### 5. Continuous recording / manifest

Careless has the right instinct: never lose the take. For SonicForge, implement local-first manifests before real program audio:

```text
generated/sets/<set_id>/manifest.json
generated/sets/<set_id>/segments/*.wav
generated/sets/<set_id>/visual-cues.jsonl
generated/sets/<set_id>/talk-cues.md
generated/sets/<set_id>/survival-pings.md
```

### 6. ASCII / text spectrograph

This pairs perfectly with our text shader visual spell lane. The browser VJ should include:

- dual-deck ASCII spectrograph strip;
- code-rain transition metadata;
- live `PHRASE_LOCK`, `BASS_SWAP`, `SURVIVAL_PING`, `COMFY_PROMPT` glyphs;
- “Cross The Streams” energy without copying the brand.

### 7. MIDI / automation lanes later

Hackathon-safe version:

- fake automation timeline in UI first;
- JSON schema for crossfader and EQ automation;
- future Web MIDI / TouchOSC / Resolume control mapping.

## ComfyUI pivot

Careless is Lyria-first. SonicForge should become **ComfyUI-aware**, but not GPU-on by default.

### What ComfyUI does for this project

ComfyUI is the visual/media forge:

- poster/key art for each set;
- generated VJ frames/loops later;
- survival-kit QR prop art;
- deck artwork for Deck A/B;
- visual spell stills;
- future video loops with Wan/LTX/AnimateDiff-style workflows;
- future audio/TTS only if reliable Comfy nodes exist.

### Adapter contract

```json
{
  "workflow": "intergalactic-djs-visual-spell",
  "mode": "dry_run",
  "deck": "B",
  "prompt": "neon ASCII spectrograph portal, DJ VANTA signal, readable text PHRASE LOCK 32",
  "negative_prompt": "illegible typography, watermark, extra logos",
  "width": 1024,
  "height": 1024,
  "seed": 1776,
  "set_id": "demo-night-001",
  "segment_id": "seg-004",
  "output_prefix": "vanta_visual_spell_seg004"
}
```

Normalized output:

```json
{
  "ok": true,
  "mode": "dry_run",
  "workflow": "intergalactic-djs-visual-spell",
  "prompt_id": null,
  "files": [],
  "warnings": ["ComfyUI not called unless explicitly enabled"]
}
```

## Implementation priorities for overnight jobs

1. Add a dual-deck model to `server/schemas.py`.
2. Return Deck A / Deck B state in `/api/next-segment`.
3. Add crossfader plan with equal-power curve formula.
4. Add prompt/crate cache docs or local JSON seed.
5. Add UI card for Deck A / Deck B and incoming Deck B visual spell.
6. Add a ComfyUI visual workflow card: no real GPU call, but exact API contract.
7. Add a local set manifest writer.
8. Add sample-pad ritual buttons in UI: VANTA TAG, HYDRATE, BUDDY, DROP, PORTAL, AIRHORN, CHILL, RECORD.
9. Add visualizer dual ASCII spectrograph / code rain.
10. Add verifier checks for `Deck A`, `Deck B`, `crossfader`, `ComfyUI`, and `survival` strings.

## Attribution note

If we borrow language or distribute derivative pieces from the Apache-2.0 repo, retain attribution and license notices. For this project, the clean path is:

- cite Careless-LiveDJ as inspiration in docs;
- do not copy its brand assets or released binary;
- adapt concepts into original SonicForge code/docs;
- keep our product identity: Intergalactic DJs / DJ VANTA / SonicForge Live.
