# Hackathon Submission Checklist — SonicForge Live / DJ VANTA

Status: **local draft / human-submit only**

Public sentence:

> Intergalactic DJs presents DJ VANTA, powered by SonicForge Live: the first Hermes-native autonomous AI DJ/VJ for local house parties, livestreams, clubs, and future festival stages.

## Default rule

This checklist prepares the submission package, but it does **not** submit, publish, upload private media, start providers, start GPUs, collect payments, or open a public stream. The final hackathon submission is `closed_until_human_yes` until an awake operator reviews every item below.

Fail-closed flags:

```yaml
starts_gpu: false
starts_paid_api: false
publishes_stream: false
records_audio: false
uploads_private_media: false
requires_human_approval: true
```

## 1. Demo identity lock

- [ ] Name the platform as **SonicForge Live**.
- [ ] Name the show/collective as **Intergalactic DJs**.
- [ ] Name the performer as **DJ VANTA//SonicForge**.
- [ ] Define VANTA as **Virtual Autonomous Nocturnal Transmission Artist**.
- [ ] Use the public sentence exactly once near the top of the submission or demo script.

## 2. Must-show product proof

A judge should see these in the local demo before any claims about future backends:

- [ ] `/health` reports fail-closed flags: `starts_gpu=false`, `starts_paid_api=false`, `publishes_stream=false`, `records_audio=false`, `uploads_private_media=false`.
- [ ] `POST /api/next-segment` returns Deck A / Deck B handoff state.
- [ ] Equal-power crossfader math is visible: `gainA = cos((value + 1) / 2 * PI / 2)` and `gainB = sin((value + 1) / 2 * PI / 2)`.
- [ ] `survival_kit` and `culture_cue` fields appear in the segment payload.
- [ ] Text-first MC break modes are visible: `survival`, `history`, `hype`, `lore`, and `technical`.
- [ ] Dry-run `comfyui_visual_spell` is present with `prompt_id: null` and `files: []`.
- [ ] `/visualizer` shows browser-first VJ modes such as code rain, EQ bands, subtitle spell, SDF/MSDF fallback, and dual ASCII spectrograph.
- [ ] `/api/backends` shows ComfyUI, RunPod/ACE-Step, Modal, TouchDesigner, Resolume, OBS/RTMP, and TTS as approval-gated contracts.

## 3. 60-second judge walkthrough

1. Say the public sentence.
2. Open the control deck at `http://127.0.0.1:8788/`.
3. Click **Plan Next Continuous Segment**.
4. Point to Deck A/B, prompt crate memory, crossfader metadata, Rave Survival Kit, lineage cue, and program-audio truth panel.
5. Open `http://127.0.0.1:8788/visualizer` and show browser-first visual spells.
6. Open `/api/backends` and explain that heavier engines are dry-run adapters until a human explicitly arms them.
7. Close with: "DJ VANTA is not replacing rave culture; it is a local-first co-pilot entering a culture built by people."

## 4. Submission copy blocks

### One-liner

SonicForge Live turns Hermes into DJ VANTA: a local-first autonomous AI DJ/VJ control deck with dual-deck planning, safe visual spells, culture-aware talk breaks, and closed-by-default backend adapters.

### Problem

AI music demos often show isolated generation, not a live performance system. Party tools also rarely combine set memory, VJ cues, community-care prompts, and explicit approval gates for risky providers.

### Solution

SonicForge Live packages an autonomous performer as a runnable local control plane: Deck A/B planning, prompt-crate digging, equal-power crossfades, metadata-only program manifests, browser VJ visuals, Rave Survival Kit prompts, lineage-aware MC breaks, and dry-run contracts for future ComfyUI/RunPod/Modal/TouchDesigner/Resolume/OBS/TTS lanes.

### Safety / ethics note

The demo is local-first and fail-closed. It does not start GPUs, paid APIs, public streams, recording, uploads, TTS/voice cloning, or provider calls by default. Harm-reduction copy is practical community care only: hydration, earplugs, buddy checks, consent, exits, chill zone, and human override. It is not medical/legal/drug-use advice.

## 5. Required verification before a human submits

Run from repo root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_survival_harm_reduction.py
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile $(git ls-files '*.py')
node --check app/static/main.js
PYTHONDONTWRITEBYTECODE=1 python3 scripts/smoke_local_demo.py
git diff --check
```

After smoke tests, run:

```bash
git status --short
```

If smoke mutated `generated/sets/...` or `generated/timeline/demo-set.json`, revert those sidecars unless the submission intentionally includes them.

## 6. Human approval gates before submission

Do not proceed unless the operator answers each relevant question:

- **Public submission:** "Do you approve publishing this exact demo text and screenshots to the hackathon portal?"
- **Private media:** "Do you approve uploading these exact screenshots, recordings, or generated assets?"
- **Provider demo:** "Do you approve calling this exact provider endpoint, with this budget/time limit and stop condition?"
- **Livestream:** "Do you approve publishing to this exact RTMP/OBS destination?"
- **Voice/TTS:** "Do you approve this exact voice/TTS adapter and output destination?"

If approval is missing or ambiguous, the lane remains `closed_until_human_yes`.

## 7. Do-not-submit list

Never include these in a hackathon upload:

- `.env` files or secret values;
- stream keys, API keys, provider tokens, SSH keys, or browser cookies;
- private room notes, names, phone numbers, addresses, photos, recordings, or private prompts;
- raw generated batches, model weights, datasets, or private media;
- claims that AI invented DJ/rave culture;
- medical diagnosis/treatment, emergency substitution, dosing, drug identification, or drug-use instructions.

## 8. Final human-submit packet

The human operator should assemble only public-safe artifacts:

- [ ] README or pitch excerpt with public sentence.
- [ ] 60-second demo script.
- [ ] Local demo commands and verifier output summary.
- [ ] Screenshots or short screen recording approved for upload.
- [ ] Safety/ethics note from this checklist.
- [ ] Link to a private or approved public repo/demo only if access has been reviewed.

Acceptance: submission package is reviewed by a human, contains no secrets/private media, and accurately describes current local-first capabilities without implying real continuous program audio, live provider calls, recording, streaming, or public deployment by default.
