# Training approval checklist

Nothing below is approved by default.

## Generation approval

- [ ] User approved a bounded ACE-Step generation batch.
- [ ] Batch size is stated.
- [ ] Max duration per candidate is stated.
- [ ] GPU/provider target is stated.
- [ ] Stop/check GPU step is included.
- [ ] No public upload.
- [ ] No training.

## Dataset approval

- [ ] Audio files are original to SonicForge or user-owned.
- [ ] Prompt/settings are saved for every candidate.
- [ ] Lyrics are saved and manually reviewed.
- [ ] Annotation JSON exists for selected tracks.
- [ ] Human listening review exists for every selected track.
- [ ] Rejected tracks are not silently used for training.

## Training readiness

- [ ] Dataset card accepted.
- [ ] Rights/provenance accepted.
- [ ] Eval plan accepted.
- [ ] Train/val/test split accepted.
- [ ] Exact ACE-Step model/base adapter target selected.
- [ ] Cost/time estimate accepted.
- [ ] Stop condition accepted.
- [ ] Upload/private storage target accepted, if any.

## Hard stops

Stop if any of these are true:

- unclear rights
- celebrity/artist imitation
- generated vocals sound like a known singer
- clipped/distorted output
- model download not approved
- GPU cost not approved
- public upload requested without explicit approval
