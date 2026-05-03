# SonicForge Live Pitch Pack

**Public sentence:** Intergalactic DJs presents DJ VANTA, powered by SonicForge Live: the first Hermes-native autonomous AI DJ/VJ for local house parties, livestreams, clubs, and future festival stages.

## 30-second pitch

SonicForge Live turns Hermes from a chat assistant into a live autonomous performer. Intergalactic DJs is the party layer, and DJ VANTA//SonicForge is the first performer: a local-first AI DJ/VJ that plans tracks, writes MC breaks, models beatmatching, phrasing, EQ moves, cue points, crowd state, and visual cues without secretly starting cloud GPUs or public streams. Open the localhost deck, press **Plan Next Continuous Segment**, and VANTA returns a demo-ready track plan, talk break, visual cue, and honest transition metadata for OBS, browser visuals, ComfyUI, Resolume, TouchDesigner, RunPod, or RTMP adapters when an operator approves those lanes.

## 90-second pitch

Most AI music demos generate one asset. SonicForge Live demonstrates a performer.

The stack has three names with three jobs. **SonicForge Live** is the local runtime and control plane. **Intergalactic DJs** is the show/collective layer a house-party crowd can understand. **DJ VANTA//SonicForge** — Virtual Autonomous Nocturnal Transmission Artist — is the first autonomous DJ inside that system.

The current demo is intentionally local-first. The FastAPI app runs on `localhost:8788`, serves a control deck and VJ window, and exposes `/health`, `/api/state`, `/api/next-segment`, and backend status contracts. The next-segment endpoint does not pretend a seamless renderer exists; it returns a real DJ brain plan: BPM compatibility, 16-bar phrasing, bass swap on bar 17, drop release on bar 33, EQ move schedule, cue points, synthetic crowd read, MC/talk ducking, visual cue, and mix metadata. Default adapters are mocks and dry-runs, so the system is safe to run on a laptop at a hackathon table.

The bigger idea is that Hermes is the permanent home: memory, skills, cron, verification, safety gates, and backend contracts. SonicForge Live is where those abilities become a performer that can eventually route to ComfyUI, Modal, RunPod/ACE-Step, Resolume Arena MCP, TouchDesigner/Spout, OBS, or RTMP only after explicit human approval.

## Judge-facing pitch

SonicForge Live is a local-first autonomous DJ/VJ control plane that packages Hermes-native agency into a live creative entity. The project matters because it models the full performance job instead of only generating media:

- **Selection:** set state, mode, guide prompt, energy arc, queue.
- **Beatmatching:** current/next BPM, tempo-shift compatibility, warp/cut notes.
- **Phrasing:** mix-in, bass-swap, drop-release, intro/outro bar counts.
- **EQ and gain staging:** low/mid/high move schedule and talk ducking.
- **Cueing:** prelisten, mix-in, bass-swap, drop, talk-clear cue points.
- **Crowd reading:** synthetic local crowd state with explicit no-hidden-mic language.
- **VJ control:** browser visualizer first, professional VJ/stream adapters later.
- **Safety:** `/health` reports no GPU starts, no paid API starts, no public stream publishing.

Demo path: run the local server, open the control deck, press **Plan Next Continuous Segment**, show the structured JSON/event output, open the VJ window for OBS capture, and explain how the same contract can later drive real generation backends after operator approval.

## House-party pitch

Intergalactic DJs is the no-surprise AI party system. You run SonicForge Live locally, point a laptop at speakers/projector/OBS, and let DJ VANTA propose the next segment: music direction, a short MC line, a visual cue, and a transition plan that says exactly how the mix should happen. It is safe by default: no hidden recording, no cloud generation, no public stream, and no paid provider unless someone intentionally arms that adapter.

## One-line tagline options

1. **DJ VANTA is the first Hermes-native autonomous AI DJ/VJ: local deck, real DJ brain, opt-in backends.**
2. **Not a playlist. Not just a generator. A local-first autonomous performer.**
3. **Intergalactic DJs brings Hermes to the dancefloor — safely, locally, and with a beatmatch plan.**

## Demo proof points to show

- `GET /health` includes `starts_gpu: false`, `starts_paid_api: false`, and `publishes_stream: false`.
- `POST /api/next-segment` returns `track`, `talk`, `visual`, `mix`, `transition`, and `state`.
- `transition` includes beatmatch, phrase, EQ moves, cue points, crowd state, talk break, visual cue, and summary.
- Browser visualizer is captureable for OBS/projector use before any pro VJ adapter is armed.
- Backend lanes are contracts, not surprise jobs: ComfyUI, RunPod/ACE-Step, Resolume, TouchDesigner/Spout, RTMP.

## Safety close

SonicForge Live should never imply unattended approval. Cloud generation, RunPod pods, Modal GPU work, Comfy Cloud, public RTMP, model training/uploads, purchases, and private-media uploads stay closed until an awake human gives explicit lane-specific approval.
