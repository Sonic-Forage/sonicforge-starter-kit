# Station Signal UI — Autonomous DJ Interface

Updated: 2026-05-01
Status: local-first UI/API contract; no GPU/provider starts by default

## Core idea

DJ VANTA should feel like an always-on intergalactic radio/DJ appliance.

The operator opens a display, enters a **Station Signal ID** or **Signal Code**, chooses a backend lane, and presses **Acquire Signal**. The UI loops through warmup copy — acquiring, verifying, tuning, disclaimers, safety gates — before the set begins.

The same interface can connect to:

- **Local server** on the user's computer.
- **RunPod endpoint** for a GPU worker or serverless handler.
- **Modal endpoint** for scale-to-zero serverless generation.
- **Custom endpoint** for future ACE-Step/ComfyUI/audio mixer lanes.

Default behavior remains fail-closed: acquiring a signal never starts paid GPU, public stream, recording, or provider generation unless a human explicitly arms that lane.

## UX metaphor

**Acquire Signal → Warm Up Station → Run Set → Outro → Scale Down**

A user should feel like VANTA is tuning into a station from the future:

1. Display is always on.
2. Operator types a signal code.
3. VANTA checks endpoint kind and readiness.
4. VANTA plays fun disclaimer/house rules copy while waiting.
5. Station locks.
6. Set duration runs: 20, 30, 45, or custom minutes.
7. VANTA outro closes the transmission.
8. Serverless backend returns to zero.

## Modes

### Single DJ Mode

One customized DJ/persona runs the entire set.

- DJ identity: DJ VANTA or custom DJ profile later.
- Voice/talk-break style: consistent persona.
- Best for a house-party appliance, creator set, personal station.

### Intergalactic Mix Mode

VANTA acts as host/announcer between tracks.

- Introduces the next creator/track.
- Adds quick lore, vibe, or culture note.
- Can say: “This next signal comes from a creator who wanted a groovy midnight bounce — enjoy the ride.”
- Best for showcases, hackathons, community mixes, creator-radio style sets.

## Signal payload fields

```json
{
  "station_signal_id": "VANTA-LOCAL-128",
  "endpoint_kind": "local | runpod | modal | custom",
  "endpoint_url": "optional URL, redacted in UI if secret-like",
  "mode": "single_dj | intergalactic_mix",
  "set_minutes": 20,
  "dj_profile": "DJ VANTA",
  "voice_host": "text_first",
  "creator_intro_mode": true,
  "allow_real_generation": false,
  "allow_public_stream": false
}
```

## Warmup ladder

The first implementation is UI + contract only. Suggested status loop:

1. `SIGNAL_CODE_RECEIVED`
2. `TUNING_TO_STATION_ID`
3. `VERIFYING_ENDPOINT_KIND`
4. `CHECKING_SERVERLESS_WAKE_PATH`
5. `LOADING_DJ_PERSONA`
6. `PREPARING_CREATOR_INTROS`
7. `READING_CRAZY_DISCLAIMER`
8. `LOCKING_HUMAN_OVERRIDE`
9. `READY_FOR_DRY_RUN`

When real generation is approved later, the ladder can add:

- `WAKING_GPU_WORKER`
- `LOADING_MODEL_WEIGHTS`
- `PRIMING_AUDIO_CONTEXT`
- `BUFFERING_FIRST_SEGMENT`
- `LIVE_TRANSMISSION_READY`

## Disclaimer / hype copy

Draft waiting-room copy:

> Acquiring station signal. Please remain near the dance floor.
> This is an autonomous AI DJ/VJ transmission. Music, visuals, talk breaks, and timing may be generated or assisted by machines.
> Keep water nearby, protect your ears, watch your friends, respect consent, and follow sober human judgment.
> DJ VANTA is not medical, legal, emergency, or drug-use advice. If someone needs help, get a human and contact local emergency services.
> Public streaming, recording, paid GPUs, and cloud providers stay closed unless the operator explicitly arms them.

## Serverless rule

The product promise should be **serverless by default**:

- Local display can stay on.
- Modal/RunPod/worker endpoint wakes only for an approved set.
- Set has a defined duration and outro.
- After outro, backend is expected to scale down / stop / return tasks to zero.
- UI should visibly say when it is dry-run only vs live generation.

## Next implementation steps

1. Add `/station` always-on display page.
2. Add `/api/signal/acquire` dry-run endpoint.
3. Add `/api/signal/session` dry-run session plan endpoint.
4. Later: adapter-specific readiness probes that do not start GPU by default.
5. Later: approved real-time generation worker contract for RunPod/Modal/local.
