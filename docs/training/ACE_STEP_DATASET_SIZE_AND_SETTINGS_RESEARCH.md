# ACE-Step 1.5 / 1.5 XL Dataset Size + Training Settings Research

Status: research note only. No generation, model download, GPU job, or training was started.

## Sources checked

- ACE-Step 1.5 official LoRA Training Tutorial
- ACE-Step 1.5 official Ultimate Guide / Tutorial
- ACE-Step 1.5 Side-Step end-to-end tutorial
- ACE-Step 1.5 GitHub Discussion #235, musician guide
- ACE-Step 1.5 GitHub Issue #728, LoRA effect not noticeable
- ACE-Step 1.5 GitHub Issue #805, unseen/novel instrument fine-tuning
- ACE-Step GitHub Issue #33, local LoRA training on 24GB VRAM
- ACE-Step 1.5 GitHub Issue #56, dataset preprocessing errors
- Web search snippets for relevant Reddit threads where full Reddit scraping was blocked
- filliptm/ComfyUI-FL-AceStep-Training repo summary

## Core dataset-size findings

### Official tutorial baseline

The official ACE-Step 1.5 LoRA tutorial demonstrates training on 13 tracks for 500 epochs with batch size 1.

This is the strongest project-doc anchor for our first album-sized LoRA plan.

### Musician guide recommendation

A GitHub discussion aimed at musicians recommends collecting roughly 8–20 songs that represent the desired style before training a LoRA.

This aligns well with a focused album dataset rather than a huge mixed library.

### Community issue advice

In GitHub Issue #728, a user trained around 400 songs for 500 epochs and reported the LoRA effect was not noticeable. Community replies suggested the dataset may have been too broad/varied. One user reported preferring 9–11 tightly related tracks for album-style LoRAs.

Key lesson: more songs is not automatically better. Consistency and style coherence matter more.

### Larger datasets can work, but can also dilute style

Other reports mentioned 50 songs working for a singer/voice case and 70 songs learning well locally, but the 70-song run also had an important failure mode: differing short durations made the model appear to learn duration cues and ignore prompts.

For our SonicForge lane, that means we should avoid a giant mixed-genre pile at the start.

### Small datasets can work for a focused target

One GitHub discussion reported a first XL LoRA trained from only about 14 minutes of data. It was not perfect, but it did produce a recognizable result.

This suggests our first run can be intentionally small if the dataset is consistent and reviewed.

## Recommended SonicForge dataset target

For the first real LoRA experiment, target:

- Minimum useful pilot: 8 reviewed tracks or 12–20 minutes of clean audio
- Preferred first album LoRA: 10–12 reviewed tracks
- Maximum first pass: 16–20 tracks only if they are tightly consistent
- Avoid first pass: 50–400 mixed tracks across many genres

For DJ VANTA / SonicForge, the best shape is an album-like dataset:

- consistent sonic identity
- consistent BPM family
- consistent mix quality
- consistent lyrical world
- consistent structural tags
- consistent metadata captions

## Track duration recommendation

For generation candidates:

- first smoke batch: 30–60 seconds
- first useful review batch: 60–90 seconds
- album keeper target: 90–180 seconds if compute allows

For training prep:

- keep duration strategy consistent
- do not mix many wildly different durations in the first training set
- if chunking is required, keep chunks around 30–40 seconds and keep train/val/test splits track-safe
- do not leak chunks from the same source track across train and test

## Metadata recommendation

Each selected audio file should have:

- audio file: `.wav` preferred for quality; `.mp3`, `.flac`, `.ogg`, `.opus` also supported by ACE-Step docs
- lyrics file: `{filename}.lyrics.txt`
- annotation JSON: `{filename}.json`

Useful JSON fields:

```json
{
  "caption": "Original SonicForge Live cyber-rave track with clean sub bass, festival synths, text-first MC phrases, and PLUR care layer energy",
  "bpm": 128,
  "keyscale": "F minor",
  "timesignature": "4",
  "language": "en",
  "custom_tag": "dj_vanta_sonicforge"
}
```

Lyrics should use structural tags:

```text
[Intro]
[Verse]
[Pre-Chorus]
[Chorus]
[Drop]
[Breakdown]
[Bridge]
[Outro]
```

## Settings recommendation for first generation batch

Generation is still approval-gated. If approved later, start with:

```json
{
  "model": "acestep-v15-xl-base or acestep-v15-xl-sft",
  "lm_model": "acestep-5Hz-lm-1.7B",
  "batch_size": 1,
  "audio_duration": 60,
  "inference_steps": 50,
  "guidance_scale": 7.0,
  "thinking": true,
  "audio_format": "wav"
}
```

For a faster smoke test only:

```json
{
  "audio_duration": 30,
  "batch_size": 1,
  "inference_steps": 8,
  "thinking": false,
  "audio_format": "mp3"
}
```

## Settings recommendation for first LoRA training plan

Training is separately approval-gated. Based on official/tutorial/community signals, the safest first training concept is:

- train on base if possible, because community reports suggest base-trained LoRAs may transfer better to base/SFT/turbo than the reverse
- batch size: 1
- first rank: 32 or 64
- first epochs: 100–300 for a quick signal test, then compare checkpoints
- official tutorial reference: 500 epochs, batch size 1, 13 tracks
- save checkpoints regularly
- evaluate with fixed prompts/seeds/settings against no-LoRA baseline
- avoid judging only one generation; test multiple seeds/prompts

## Inference settings to compare after training

For base/SFT:

```json
{
  "shift": 1.0,
  "inference_steps": 50
}
```

For turbo:

```json
{
  "shift": 3.0,
  "inference_steps": 8
}
```

Community reports conflict on `thinking` during LoRA inference. So the eval matrix should test both:

- LoRA on + thinking on
- LoRA on + thinking off
- LoRA off + thinking on
- LoRA off + thinking off

## Failure modes to avoid

- Too many mixed genres in one style LoRA
- Mixing house, trance, dubstep, techno, pop vocal, and experimental noise before the core identity is learned
- Weak captions or inconsistent metadata
- Unreviewed lyrics/transcripts
- Differing durations causing the model to learn duration shortcuts
- Training and then judging without A/B fixed-seed comparisons
- Assuming bigger dataset means stronger style
- Using copyrighted songs, named artist imitation, celebrity/soundalike vocal targets, or commercial samples

## Updated recommendation for SonicForge

The original 12-track plan is in the right zone.

Do not jump to hundreds of generated tracks. Instead:

1. Generate 5 short candidates only after approval.
2. Listen and refine prompt/settings.
3. Generate enough candidates to select 10–12 keepers.
4. Keep the dataset album-coherent.
5. Build metadata and lyrics sidecars.
6. Run dataset validation.
7. Only then ask for separate LoRA training approval.

Recommended first album LoRA target:

```text
10–12 reviewed tracks, 60–180 seconds each, same SonicForge/DJ VANTA identity, consistent captions/lyrics/metadata, no copyrighted references, no named artist imitation.
```

## Current status

No GPU, generation, model download, training, upload, or public release was started during this research.
