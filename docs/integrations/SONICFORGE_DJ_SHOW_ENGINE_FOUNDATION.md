# SonicForge DJ Show Engine Foundation

Status: private/forkable foundation notes. No public release, no remote GPU calls, no paid API calls.

## What we learned

The latest timeline-first mix was the first one that did **not** collapse into a train wreck. The key win was not a fancy AI DJ algorithm; it was a safer arrangement model:

- make a show plan before rendering audio;
- render one voice/song pair at a time;
- allow only one controlled mini-overlap: a quiet song bed under the last seconds of a host bumper;
- concatenate verified pair files after each pair passes duration checks;
- never let two host clips or two full song sections overlap accidentally.

That becomes the baseline for SonicForge.

## Core product idea

If tracks are generated/downloaded offline, SonicForge does **not** need live GPU power for every mix. The offline workflow becomes:

1. Generate songs with ComfyUI/ACE-Step, Suno-like APIs, local models, or any approved source.
2. Download/cache the final audio tracks.
3. Generate/cache host voice bumpers separately.
4. Run the SonicForge DJ Show Engine locally against the cached library.
5. Produce a full show mix, timeline, manifest, hashes, and QA notes.

This makes the system autonomous, forkable, and cheaper: generation can happen in batches, while mixing can happen locally with FFmpeg/librosa.

## Mix modes

### 1. `reference_concat`

Use when testing a new theme or voice pack.

Behavior:

- host voice;
- small silence;
- song section;
- small silence;
- next host.

Rules:

- no overlaps;
- no crossfades;
- proves order, level matching, and source quality.

### 2. `radio_duck_safe`

Current best baseline.

Behavior:

- host voice starts alone;
- song fades in quietly under final ~2 seconds of host;
- host ends;
- song continues at normal level for the planned cut duration;
- next host starts only after prior song is done.

Rules:

- only one host at a time;
- only one song at a time;
- the only overlap is the controlled intro bed inside a single pair.

### 3. `song_to_song_transition_lab`

Use only after a clean radio-duck mix passes.

Behavior:

- test two song cuts without any host voice;
- try a transition style: crossfade, echo-out, EQ swap, pyCrossfade adapter, or Mixxx-inspired transition;
- export transition-only MP3 for listening.

Rules:

- never introduce this into a full show until the transition-only test sounds good;
- no host voice in this mode;
- no remote generation.

### 4. `autodj_adapter_lab`

Experimental mode for external frameworks:

- pyCrossfade: likely first adapter candidate for beat-matched song-to-song transitions;
- Mixxx: reference/operator tool for cue points, beat grids, harmonic flow;
- AI-DJ-Mixing-System: useful planning concepts, but must be audited before dependency adoption.

## Asset contract

Every offline asset should have metadata. Minimum song fields:

```json
{
  "title": "Song Title",
  "file": "path/to/song.mp3",
  "source": "comfyui_ace_step | suno | local | imported",
  "approved_for_private_demo": true,
  "duration_seconds": 120,
  "preferred_cut_start_seconds": 24,
  "preferred_cut_duration_seconds": 60,
  "energy": "warmup | groove | peak | finale",
  "bpm_hint": 124,
  "key_hint": "optional",
  "notes": "good intro after first phrase, avoid last noisy 10s"
}
```

Minimum host voice fields:

```json
{
  "host_name": "Velvet Orbit MC",
  "file": "path/to/voice.wav",
  "voice_source": "omnivoice_cached | comfyui_omnivoice | approved_other",
  "approved_for_private_demo": true,
  "persona_role": "warm welcome / lore / transition / outro",
  "notes": "clear, intelligible, no fake celebrity clone"
}
```

## Theme brief input

When the user gives a theme, convert it into a show brief before rendering. Required fields:

- `theme_title`
- `one_sentence_story`
- `mood_words`
- `track_count`
- `song_seconds`
- `host_count`
- `host_personas`
- `must_include_phrases`
- `avoid`
- `mix_mode`

Example theme prompt from user:

> “intergalactic candy-rave rescue mission, funny but badass, four tracks, aliens almost crash the party but the bass saves everyone.”

The engine should turn that into:

- 4 host/song pairs;
- 1 outro host;
- 4 cached/offline tracks or generation requests;
- host scripts with safe lore and no celebrity cloning;
- `radio_duck_safe` first render;
- transition lab only after the baseline is accepted.

## QA manifest requirements

Every rendered show must output:

- `manifest.json` — final file, SHA-256, duration, sources, rules;
- `timeline.json` — ordered event list;
- `qa_report.json` — pass/fail checks;
- `FULL_*.mp3` — final mix;
- optional `pair_*.wav` or `pair_*.mp3` files for debugging.

Minimum QA checks:

- sources exist;
- durations are non-zero;
- expected vs actual final duration within tolerance;
- no two pair-level events overlap;
- no host voice appears after the next song starts except controlled intro bed;
- no two full song sections overlap;
- secret scan clean;
- no remote GPU/API calls unless explicit approval is recorded.

## How to improve mixing skill safely

### Immediate improvements

1. Keep `radio_duck_safe` as the default.
2. Add a `theme_brief.json` per run.
3. Add `qa_report.json` per run.
4. Add per-track loudness normalization and true-peak limit.
5. Add per-pair debug exports so a bad pair can be fixed without rerendering the whole show.

### Next-level improvements

1. Use librosa to estimate BPM/energy on offline tracks.
2. Choose cut starts near phrase boundaries instead of hardcoded seconds.
3. Group generated/downloaded songs by energy arc: warmup -> groove -> peak -> finale.
4. Add pyCrossfade adapter for song-to-song-only tests.
5. Add Mixxx-style cue point metadata for human review.

### Don’t do yet

- Don’t put long crossfades into the full show until transition-only tests pass.
- Don’t add multiple simultaneous voices.
- Don’t silently substitute fake/procedural songs when requested generation fails.
- Don’t rerun remote GPU generation without explicit approval/fresh endpoint.

## Forkable architecture

Suggested repo layout:

```text
scripts/
  run_sonicforge_dj_show_engine_v01.py
  analyze_offline_track_library.py        # future
  run_transition_lab.py                   # future

data/
  templates/
    sonicforge_dj_show_brief.template.json
  manifests/
    generated_show_manifest.json

docs/integrations/
  AUTO_DJ_FRAMEWORK_RESEARCH.md
  SONICFORGE_DJ_SHOW_ENGINE_FOUNDATION.md
```

## Current best next user flow

1. User gives a theme/tidbit.
2. Hermes creates a theme brief.
3. Hermes selects 3–5 offline tracks or generates a task list for new tracks.
4. Hermes renders `radio_duck_safe` first.
5. User approves or rejects.
6. Only then Hermes runs a small transition lab for one or two song-to-song transitions.

This gives us autonomous growth without losing control of quality.
