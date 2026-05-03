# TTS Adapter Contract — DJ VANTA Text-First MC Lane

Status: **dry-run / operator-armed only**. SonicForge Live does not synthesize, play, upload, or send voice by default.

## Purpose

This card defines the future text-to-speech lane for **Intergalactic DJs presents DJ VANTA, powered by SonicForge Live**. The current runtime is text-first: talk-breaks are planned as readable cue text with ducking metadata. Future local or approved endpoints may render DJ VANTA's MC lines only after a human explicitly enables audio output.

Candidate lanes:

- `KittenTTS` local synthetic voice for low-latency demo narration.
- `Qwen3-TTS` / `QwenTTS` through a local ComfyUI workflow or local endpoint.
- `Voxtral TTS` / speech-understanding-adjacent lane when a verified local service exists.
- `ComfyUI TTS workflow` when custom nodes and model licenses are approved.

## Closed-by-default flags

```yaml
starts_gpu: false
starts_paid_api: false
publishes_stream: false
records_audio: false
uploads_private_media: false
sends_voice_message: false
voice_cloning_enabled: false
requires_human_approval: true
status: text_first_no_audio_output
```

No cron run may flip these flags. Silence, excitement, or a demo deadline is not approval.

## Environment variable names only

Use `.env.example` names only; never commit real endpoints, tokens, voice samples, or private prompts.

```bash
SONICFORGE_ALLOW_TTS=false
SONICFORGE_ALLOW_VOICE_CLONING=false
TTS_ENABLE_AUDIO_OUTPUT=false
TTS_VOICE_ID=demo_synthetic_only
KITTENTTS_BASE_URL=http://127.0.0.1:7860
QWEN_TTS_BASE_URL=http://127.0.0.1:8188
VOXTRAL_TTS_BASE_URL=
COMFYUI_ENABLE_PROMPT=false
```

If `TTS_ENABLE_AUDIO_OUTPUT=false`, adapters must return metadata only:

```json
{
  "ok": true,
  "adapter": "mock-text-talk-break",
  "status": "text_first_no_audio_output",
  "file": null,
  "text": "Intergalactic check-in: water station is part of the dancefloor.",
  "seconds": 12,
  "duck_music_db": -7,
  "warnings": ["TTS audio output is disabled until explicit human approval"]
}
```

## Normalized input contract

```json
{
  "segment_id": "seg-001",
  "performer": "DJ VANTA//SonicForge",
  "mode": "survival | history | hype | lore | technical",
  "text": "We are guests in a culture with history. Hydrate, protect your ears, check your people, and dance with respect.",
  "duration_seconds": 12,
  "duck_music_db": -7,
  "talk_over_intro_seconds": 10,
  "voice_id": "demo_synthetic_only",
  "route": "metadata_only_no_audio_playback",
  "requires_human_approval": true
}
```

## Normalized output contract

Dry-run response:

```json
{
  "ok": true,
  "provider": "tts_contract_dry_run",
  "status": "text_first_no_audio_output",
  "file": null,
  "duration_seconds": 12,
  "starts_gpu": false,
  "starts_paid_api": false,
  "publishes_stream": false,
  "records_audio": false,
  "uploads_private_media": false,
  "sends_voice_message": false,
  "warnings": ["No audio generated; human approval required"]
}
```

Future approved response:

```json
{
  "ok": true,
  "provider": "local_kittentts_or_approved_tts",
  "status": "local_audio_rendered_after_human_approval",
  "file": "generated/tts/<set_id>/<segment_id>.wav",
  "duration_seconds": 12,
  "voice_id": "approved_synthetic_voice",
  "license_note": "operator verified model/license before enabling",
  "warnings": []
}
```

## Voice cloning and consent guardrails

- Real-person voice cloning is **off** unless the awake operator provides written consent, source-rights confirmation, and a bounded local test plan.
- Do not clone DJs, artists, friends, guests, celebrities, judges, or streamers without permission.
- Do not upload private voice samples, recordings, room audio, or crowd audio to a provider from unattended cron.
- Do not send unsolicited voice messages; text-only responses are the safe default.
- Generated MC audio must be labeled synthetic when used in a real party or livestream.

## Talk-break modes

### `survival`

Community-care reminders only: hydration, earplugs, buddy check, consent, exits, chill zone, sober operator, human override. This is **not medical/legal/drug-use advice**.

Example: “DJ VANTA survival protocol: bass is sacred, hearing is too. Earplugs in, shoulders loose, next transmission is rising.”

### `history`

Respectful lineage notes: disco, house, techno, rave, VJ culture, sound systems, community care. Do not claim AI invented or replaces these cultures.

Example: “Respect to the selectors and sound systems that taught machines how to move.”

### `hype`

Short stage energy lines that do not imply public streaming, real generated audio, or unsafe crowd commands.

Example: “Intergalactic DJs, Deck B is glowing. Human override is ready; the portal opens on the phrase.”

### `lore`

DJ VANTA identity and SonicForge world-building.

Example: “VANTA means Virtual Autonomous Nocturnal Transmission Artist — local-first, dry-run safe, and watching the crossfader.”

### `technical`

Explain the performer brain without overclaiming.

Example: “Equal-power handoff planned: bass swap on bar seventeen, midpoint gains at point seven zero seven.”

## Adapter behavior checklist

1. Read `TTS_ENABLE_AUDIO_OUTPUT`; default to `false`.
2. If disabled, return metadata only and never create an audio file.
3. If enabled, require `SONICFORGE_REQUIRE_HUMAN_APPROVAL=true` plus an explicit operator approval record before rendering.
4. Keep generated audio under `generated/tts/` and do not commit batches by default.
5. Add ducking metadata to the set manifest instead of claiming a rendered program mix.
6. Keep provider calls local unless a separate approval ledger opens exactly one external lane.
7. Preserve safety copy: community-care only; no medical claims, diagnosis, dosing, drug identification, or emergency substitution.

## Demo smoke checks

Safe proof commands should verify contract text and existing mock behavior only:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify.py
python3 -m py_compile server/*.py server/adapters/*.py scripts/*.py
python3 - <<'PY'
from server.adapters.mock import MockTTSAdapter
print(MockTTSAdapter.name)
PY
```

Expected result: `mock-text-talk-break`; no TTS service process, GPU, provider call, recording, upload, voice message, or stream starts.
