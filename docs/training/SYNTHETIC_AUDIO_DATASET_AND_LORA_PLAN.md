# Synthetic audio dataset + LoRA plan for SonicForge Live

Status: **research / readiness only**
Live generation: **not started**
Model downloads: **not started**
Training: **not started**
GPU spend: **not started**

## Why this is interesting

The idea is strong: generate a small, original SonicForge/DJ VANTA album, listen to it, keep only the good tracks, annotate them cleanly, then use that as a synthetic dataset for style tuning later.

This gives us three things at once:

1. A real album/drop people can hear.
2. A clean rights/provenance story because the tracks are generated specifically for this project.
3. A future LoRA/fine-tune dataset that teaches the model the SonicForge scene: cyber-rave, DJ VANTA, PLUR, terminal visuals, continuous set energy, safety/care layer, and Festival 2045 mythology.

The trap to avoid: generating a pile of random tracks and calling it training data. The dataset has to be curated like a record, not scraped like a dump.

## Ground rules

- Use only original generated tracks made for SonicForge Live, or user-owned audio with clear rights.
- Do not train on commercial songs, artist clones, copyrighted vocals, or style prompts that name living artists as targets.
- Do not start model downloads, GPU generation, Comfy Cloud, RunPod, Modal, or training without explicit approval.
- Every generated track candidate must get metadata, prompt, settings, and human review notes.
- The album is the first artifact. The dataset is the second artifact. Training is the third artifact.

## ACE-Step facts that matter

From ACE-Step 1.5 docs and tutorial material:

- ACE-Step 1.5 supports local music generation and LoRA training.
- ACE-Step 1.5 XL uses larger DiT variants for higher quality.
- LoRA training can work with a small number of songs. The official materials mention examples around a few songs and a tutorial album of 13 tracks.
- Training data should include:
  - audio file: `.mp3`, `.wav`, `.flac`, `.ogg`, or `.opus`
  - lyrics file: `{filename}.lyrics.txt` preferred
  - optional annotation JSON with caption, BPM, keyscale, time signature, language
- Structural lyric tags help the model understand arrangement:
  - `[Intro]`
  - `[Verse]`
  - `[Pre-Chorus]`
  - `[Chorus]`
  - `[Drop]`
  - `[Bridge]`
  - `[Breakdown]`
  - `[Outro]`
- The ACE-Step docs explicitly recommend using your own original works for training.

## Minimum viable album dataset

Recommended first target:

```text
12 generated candidates
→ human review
→ keep best 8
→ sequence as a mini album
→ annotate cleanly
→ split into train/val/test readiness
```

Why 8 kept tracks:

- Small enough to review tonight.
- Close to the small-data LoRA examples people talk about.
- Enough variation to avoid one-note overfitting.
- Big enough to become a real demo album.

If time is tight, do:

```text
5 generated candidates
→ keep best 3
→ no training yet
→ prove the workflow
```

## Album concept

Working title:

```text
DJ VANTA — No Golden Ticket Required
```

Scene:

A 24-hour birthday-to-eclipse transmission from the Intergalactic DJs station. The sound moves from signal acquisition to warehouse rave, care-layer pause, portal drop, sunrise archive, and Festival 2045 myth.

Core sound:

- futuristic warehouse rave
- clean sub bass
- sharp drums
- cyberpunk synths
- festival laser atmospheres
- spoken/chantable hooks
- occasional text-first MC callouts
- PLUR/community-care warmth, not just dark aggression

Avoid:

- artist imitation
- copyrighted references
- vocals that sound like a specific famous singer
- random genre soup
- muddy mixes
- unreadable lyrics
- fake “live crowd” noise overpowering the track

## Candidate track list

1. `signal_acquired`
   - opener / boot sequence
   - 126 BPM
   - key: A minor
   - mood: anticipation, system wakeup

2. `no_golden_ticket`
   - mission statement anthem
   - 128 BPM
   - key: C minor
   - mood: defiant, communal

3. `fork_the_station`
   - peak builder-party drop
   - 130 BPM
   - key: F minor
   - mood: aggressive but clean

4. `deck_ab_handoff`
   - DJ mechanics / phrase mixing energy
   - 128 BPM
   - key: G minor
   - mood: technical, rolling, precise

5. `asic_code_spell`
   - terminal visualizer track
   - 132 BPM
   - key: D minor
   - mood: glitchy, neon, coded

6. `kandi_protocol`
   - PLUR / friendship-token track
   - 124 BPM
   - key: A major
   - mood: bright, melodic, human

7. `hydration_ping`
   - care-layer interlude
   - 100 BPM
   - key: E minor
   - mood: warm, halftime, reset

8. `comfy_workflow_ritual`
   - visual workflow station theme
   - 126 BPM
   - key: B minor
   - mood: procedural, hypnotic

9. `agent_factory`
   - clone creation / template agent energy
   - 129 BPM
   - key: F# minor
   - mood: mechanical, playful, alive

10. `archive_the_night`
    - memory/archive closer
    - 118 BPM
    - key: D major
    - mood: reflective, sunrise

11. `festival_2045`
    - long horizon / eclipse myth
    - 128 BPM
    - key: E minor
    - mood: cosmic, emotional, huge

12. `the_people_keep_the_room_human`
    - final anthem
    - 126 BPM
    - key: C major
    - mood: communal, warm, singable

## Dataset folder layout

```text
datasets/synthetic_audio/dj-vanta-no-golden-ticket-required/
├── README.md
├── album_manifest.json
├── approval_ledger.json
├── prompts/
│   ├── prompt_bank.md
│   └── generation_queue.jsonl
├── candidates/
│   ├── signal_acquired/
│   │   ├── signal_acquired.prompt.md
│   │   ├── signal_acquired.settings.json
│   │   ├── signal_acquired.review.json
│   │   └── signal_acquired.lyrics.txt
│   └── ...
├── selected/
│   ├── track01_signal_acquired.wav
│   ├── track01_signal_acquired.lyrics.txt
│   ├── track01_signal_acquired.json
│   └── ...
├── rejected/
│   └── README.md
├── splits/
│   ├── train.jsonl
│   ├── val.jsonl
│   └── test.jsonl
└── training_readiness/
    ├── DATASET_CARD.md
    ├── RIGHTS_AND_PROVENANCE.md
    ├── LISTENING_REVIEW.md
    └── TRAINING_APPROVAL_CHECKLIST.md
```

## Per-track annotation JSON

ACE-Step tutorial annotations are optional, but we should write them anyway.

```json
{
  "id": "track01_signal_acquired",
  "title": "Signal Acquired",
  "artist": "DJ VANTA",
  "project": "SonicForge Live",
  "album": "No Golden Ticket Required",
  "caption": "Futuristic warehouse rave opener with clean sub bass, crisp drums, neon synth pulses, cyberpunk boot-sequence atmosphere, and a chantable autonomous DJ hook.",
  "bpm": 126,
  "keyscale": "A minor",
  "timesignature": "4/4",
  "language": "en",
  "duration_target_seconds": 180,
  "vocal_mode": "chant / short vocal hook",
  "energy_level": 7,
  "scene_tags": ["cyber-rave", "DJ VANTA", "signal acquisition", "warehouse", "Party AI OS"],
  "safety_tags": ["original_generated_audio", "no_artist_imitation", "human_review_required"],
  "generation_model": "ACE-Step 1.5 XL candidate",
  "generation_status": "planned_not_generated",
  "human_review_status": "pending",
  "approved_for_album": false,
  "approved_for_training": false
}
```

## Lyrics format

Use structural tags even when lyrics are minimal.

Example:

```text
[Intro]
Signal in the dark
VANTA online

[Build]
No golden ticket
We build the room

[Drop]
Fork the station
Run the night
The machine keeps the set alive
The people keep the room human

[Outro]
Archive the signal
Carry it home
```

## Prompting pattern

Each candidate should have:

- style caption
- arrangement plan
- lyric sheet
- negative constraints
- target BPM/key
- duration
- seed/settings if available
- review rubric

Good prompt shape:

```text
Caption:
Futuristic warehouse rave opener, clean sub bass, crisp four-on-the-floor drums, neon arpeggiated synth pulses, cyberpunk boot sequence atmosphere, DJ intro energy, polished modern electronic production, chantable short vocal hook, no artist imitation.

Lyrics:
[Intro]
Signal in the dark
VANTA online

[Build]
No golden ticket
We build the room

[Drop]
Fork the station
Run the night
The machine keeps the set alive
The people keep the room human

[Outro]
Archive the signal
Carry it home

Negative constraints:
No copyrighted melody. No named artist imitation. No muddy low end. No harsh clipping. No random spoken ad-libs. No fake radio tag. No long silence. No distorted unintelligible vocals.

Targets:
BPM 126, A minor, 4/4, 180 seconds.
```

## Listening rubric

Every candidate gets scored 0–5.

```text
musical_coherence: does it feel like a real track?
mix_quality: is the low end clean, drums clear, not clipped?
prompt_adherence: does it match the intended scene?
usable_vocals: are lyrics intelligible enough, or is instrumental better?
loop_or_set_usability: can a DJ use it in a set?
sonicforge_identity: does it feel like DJ VANTA / Intergalactic DJs?
training_value: would this teach the model something we want?
legal_safety: original, no obvious imitation, no copyrighted hooks?
```

Keep rule:

```text
album_candidate = average >= 3.8 and legal_safety >= 5 and mix_quality >= 3
training_candidate = average >= 4.2 and legal_safety >= 5 and prompt_adherence >= 4 and sonicforge_identity >= 4
```

## Split plan

For 8 selected tracks:

```text
train: 6 tracks
val: 1 track
test: 1 track
```

For 12 selected tracks:

```text
train: 9 tracks
val: 1 track
test: 2 tracks
```

Do not split random chunks from the same track across train and test if the goal is honest evaluation. Keep whole tracks together by split.

## Tonight-ready execution plan once approved

Approval question before any live generation:

```text
Approve one bounded ACE-Step generation batch for SonicForge synthetic album candidates?
Scope: 5 short candidates, 60–90 seconds each, batch_size=1, no training, no public upload, stop/check GPU after completion.
```

If approved:

1. Create dataset folder and prompt bank.
2. Generate 5 candidates first, not 12.
3. Download audio locally.
4. Run `ffprobe` and basic audio stats.
5. Deliver the 5 tracks to the user as review media.
6. Fill human review JSON after listening.
7. Pick 3 keepers.
8. Only then expand to 12 candidates.
9. Package a mini album manifest.
10. Ask separately before any LoRA/training.

Training approval question:

```text
Approve a bounded ACE-Step LoRA training readiness run using only selected original SonicForge-generated tracks?
Scope: prepare dataset and dry-run validation first; no training starts until the dataset card, rights sheet, and eval plan are accepted.
```

## What we can say publicly

Safe:

```text
We are preparing an original synthetic audio dataset for DJ VANTA by generating and curating a small SonicForge album first. The album becomes the proof artifact, and only approved tracks can become training candidates later.
```

Do not say yet:

```text
We trained the model.
We have a custom audio model.
The album is finished.
The LoRA exists.
```

Until those things are actually true.

## Current state

As of this document:

- no ACE-Step generation has been run for this dataset
- no model has been downloaded
- no LoRA has been trained
- no GPU job has started
- this is a closed-gate plan and prompt/design scaffold only
