# Dataset card: DJ VANTA — No Golden Ticket Required

Status: planned / no generated audio yet.

## Dataset summary

This dataset is intended to contain original generated audio candidates for a SonicForge Live / DJ VANTA mini album. The first use is creative review and album packaging. A later use may be ACE-Step LoRA/style tuning, but only after explicit approval.

## Source

Planned source: original ACE-Step 1.5 XL generations created from SonicForge-owned prompts and lyrics.

Current source state: no audio files generated yet.

## Intended contents

- 12 planned album candidates
- 8 selected keepers after human listening review
- per-track lyrics files
- per-track annotation JSON
- per-track generation settings
- per-track review JSON
- train/val/test split files after selection

## Rights / provenance

Allowed:

- original prompts written for SonicForge Live
- original lyrics written for DJ VANTA / Intergalactic DJs
- generated audio created specifically for this project
- user-owned source material if explicitly added later

Not allowed:

- copyrighted song recreations
- prompts naming living artists as targets
- commercial sample imitation
- cloned vocals
- scraped music datasets
- unclear provenance

## Safety / approval gates

Current state:

```json
{
  "gpu_generation_started": false,
  "model_download_started": false,
  "training_started": false,
  "public_upload_started": false,
  "approved_for_generation": false,
  "approved_for_training": false
}
```

Before generation, ask:

```text
Approve one bounded ACE-Step generation batch for SonicForge synthetic album candidates?
Scope: 5 short candidates, 60-90 seconds each, batch_size=1, no training, no public upload, stop/check GPU after completion.
```

Before training, ask separately:

```text
Approve a bounded ACE-Step LoRA training readiness run using only selected original SonicForge-generated tracks?
Scope: prepare dataset and dry-run validation first; no training starts until the dataset card, rights sheet, and eval plan are accepted.
```

## Evaluation rubric

Each candidate is scored 0-5 for:

- musical coherence
- mix quality
- prompt adherence
- usable vocals
- loop/set usability
- SonicForge identity
- training value
- legal safety

## Known limitations

Synthetic tracks can collapse into repetitive structure, muddy low end, strange vocals, or generic genre output. Human review is required before album selection or training use.

## Public claim policy

Allowed today:

```text
We are preparing an original synthetic audio dataset for DJ VANTA by designing a SonicForge album and review workflow.
```

Not allowed yet:

```text
We trained a custom model.
We generated the finished album.
The DJ VANTA LoRA exists.
```
