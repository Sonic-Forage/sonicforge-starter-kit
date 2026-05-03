# SonicForge Auto-DJ Framework Research

Status: private research / no remote GPU calls / no publishing.

## Why the last mixes failed

The problem is not only “crossfade vs no crossfade.” The current SonicForge host-show mixer needs an explicit arrangement model:

1. spoken host segments must not be stacked on top of each other;
2. songs need known safe entry/exit points;
3. transition logic needs beat/phrase awareness before long overlaps;
4. voice ducking should be introduced after the basic order is verified;
5. all generated outputs need an audible QA reference: voice-only, song-only, transition-only, full mix.

## Candidate tools/frameworks

### 1. pyCrossfade

URL: https://github.com/oguzhan-yilmaz/pyCrossfade

What it is: Python/Docker tool for beat-matched crossfade transitions. It includes BPM shifting on bars, EQ modification, CLI, Docker image, and metadata extraction. It appears maintained recently, with a 2024 CLI/Docker update and 2025 README activity.

Why it is relevant:

- beat-matched crossfades;
- gradual BPM shifting on bars;
- EQ changes during transitions;
- extracts BPM, downbeats/bars, key/scale, replay gain, danceability;
- Docker route can avoid local dependency pain.

Risks:

- may require Docker; local Hermes environment may not have Docker;
- designed for track-to-track DJ transitions, not voice-host radio segments;
- should be tested on copies of our 60-second song cuts first.

Recommended use in SonicForge:

- Use as an offline transition-engine candidate for song-to-song parts only.
- Keep host voice sequencing outside pyCrossfade.
- Pipeline: voice bumper -> song A -> pyCrossfade transition A/B -> song B -> host bumper.

### 2. Mixxx Auto DJ / scripting

URLs:

- https://www.mixxx.org/
- https://github.com/byronxu99/AutoDJ
- https://mixxx.discourse.group/t/auto-dj-extension-for-beatmatching-and-harmonic-mixing/15962

What it is: Mixxx is mature open-source DJ software. It has Auto DJ, BPM/key analysis, crates, cue points, controller scripting, and real DJ deck concepts.

Why it is relevant:

- closest thing to real DJ behavior;
- supports BPM/key analysis, cue points, beat grids;
- has scripting automation via JavaScript/controller mappings;
- can teach us the right primitives: decks, cues, beatgrid, bass EQ swap, transition timing.

Risks:

- heavier than a Python script;
- headless/offline export workflow may be awkward;
- AutoDJ scripts can be old and Mixxx-version-specific;
- may require GUI/audio backend setup.

Recommended use in SonicForge:

- Treat Mixxx as reference architecture and possible operator tool, not the first automated backend.
- Add Mixxx export/import later if we want human-in-the-loop DJ review.

### 3. MixingBear

URL: https://github.com/dodiku/MixingBear

What it is: Small Python package for automatic beat-mixing of WAV files using AudioOwl.

Why it is relevant:

- simple API: `mixingbear.mix(track01.wav, track02.wav, output.wav)`;
- intended for automatic beat-mixing;
- MIT license.

Risks:

- appears inactive since 2018;
- only a few commits;
- WAV-focused;
- dependency compatibility unknown.

Recommended use in SonicForge:

- Only as a quick lab experiment if pyCrossfade is too heavy.
- Do not build the main architecture on it without a successful smoke test.

### 4. AI-DJ-Mixing-System

URL: https://github.com/kckDeepak/AI-DJ-Mixing-System

What it is: Recent Python pipeline that claims BPM/key/energy/structure analysis, transition planning, echo transitions, JSON setlists, and natural language track selection.

Why it is relevant:

- closest conceptual fit to “autonomous DJ brain”;
- uses librosa-style analysis plus transition plans;
- outputs final mix plus JSON planning files;
- includes radio-style echo transition idea that avoids muddy long overlaps.

Risks:

- small/new repo;
- likely depends on OpenAI APIs for its full feature set;
- must be sanitized/forked carefully before integration;
- claims need verification.

Recommended use in SonicForge:

- Study architecture and planning JSON format.
- Borrow the idea of explicit `setlist.json` and `transition_plan.json` even if we do not use the whole repo.

### 5. Librosa + FFmpeg custom engine

URLs:

- https://librosa.org/doc/main/generated/librosa.beat.beat_track.html
- https://essentia.upf.edu/tutorial_rhythm_beatdetection.html

What it is: Build our own small deterministic engine using installed tools. Current environment already has `librosa`, `numpy`, `scipy`, `soundfile`, and FFmpeg filters such as `loudnorm`, `acrossfade`, `sidechaincompress`, `acompressor`, and `alimiter`.

Why it is relevant:

- no external APIs;
- easiest to make forkable;
- can be tailored to host-voice + generated-song structure;
- can generate QA artifacts after every stage.

Risks:

- we must implement arrangement rules correctly;
- naïve beat detection can be wrong;
- requires careful staged testing, not one giant full-mix jump.

Recommended use in SonicForge:

- This should be our baseline “SonicForge DJ Show Engine.”
- Add pyCrossfade/Mixxx later as optional transition adapters.

## Proposed SonicForge DJ Show Engine v0.1

### Core rule

Separate arrangement from rendering.

Do not directly throw all audio into one FFmpeg graph. First create a timeline manifest, then render it.

### Timeline manifest example

```json
{
  "show_id": "sonicforge_test_001",
  "safe_mode": true,
  "sections": [
    {
      "type": "voice",
      "title": "Host intro 1",
      "file": "voice_01.wav",
      "start_mode": "after_previous",
      "overlap_allowed": false
    },
    {
      "type": "song",
      "title": "Song 1",
      "file": "song_01.mp3",
      "duration_seconds": 60,
      "fade_in_seconds": 1.5,
      "fade_out_seconds": 2.5,
      "overlap_allowed": false
    }
  ]
}
```

### Renderer modes

1. `reference_concat`
   - voice -> silence -> song;
   - no overlays;
   - proves order and levels.

2. `radio_duck`
   - music bed starts quietly under final seconds of host;
   - sidechain/volume automation only within one voice+song pair;
   - no song-to-song crossfade yet.

3. `dj_transition`
   - only after pair mode passes;
   - use beat/phrase-aware crossfade between song tails/heads;
   - optional pyCrossfade adapter.

4. `autodj_lab`
   - pyCrossfade/Mixxx/AI-DJ candidates tested on copied song cuts;
   - no host voice until song-to-song result is approved.

### QA checkpoints

For every generated show:

- `voice_only_preview.mp3`
- `song_cut_preview.mp3`
- `pair_01_voice_song.mp3`
- `transition_01_song_to_song.mp3`
- `FULL_mix.mp3`
- `timeline.json`
- `qa_report.json`

### Hard fail rules

- If two voice clips overlap, fail.
- If two full songs overlap outside a transition window, fail.
- If any segment is shorter than expected by more than 2 seconds, fail.
- If FFmpeg output duration is wildly shorter than manifest duration, fail.
- If remote OmniVoice/ComfyUI quota fails, do not silently switch to garbage procedural substitutes; label/cache reuse explicitly.

## Recommendation

Immediate next technical path:

1. keep the newest clean reference mix as sequencing baseline;
2. build `timeline.json` + QA validator before making another “DJ” version;
3. test pyCrossfade in a local sandbox against two 60-second real song cuts;
4. if pyCrossfade works, use it only for song-to-song transitions;
5. keep host voice rendering as strict radio bumpers until the transition engine is proven.

Most promising external candidate: `pyCrossfade`.
Most robust forkable baseline: custom `librosa + FFmpeg + timeline manifest` engine.
Most real-DJ reference: Mixxx.
