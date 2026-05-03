from __future__ import annotations
import os
from pathlib import Path
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from server.schemas import SetState, TrackBrief, TalkBreak, VisualCue, StreamPlan, SonicEvent
from server.adapters.mock import MockMusicAdapter, MockTTSAdapter, MockVisualAdapter, DryRunStreamAdapter
from server.adapters.comfyui import ComfyUIAdapter
from server.adapters.runpod import RunPodAceStepAdapter
from server.crate_cache import load_prompt_crate
from server.planner import plan_next_segment
from server.mc_breaks import build_mc_break_preview
from server.set_manifest import append_set_manifest, load_set_manifest
from server.timeline import load_demo_timeline, write_demo_timeline
from server.program_status import build_program_status
from server.program_manifest_renderer import render_program_manifest
from server.backend_status import build_backend_status
from server.signal import acquire_signal_contract, session_plan_contract
from server.safety_policy import blocked_action_for, safety_policy_snapshot
from server.ecosystem import build_ecosystem_status
from server.launch_status import build_launch_status

app = FastAPI(title='SonicForge Live', version='0.1.0')
static_dir = Path(__file__).resolve().parent.parent / 'app' / 'static'
app.mount('/static', StaticFiles(directory=str(static_dir)), name='static')

state = SetState()
music = MockMusicAdapter()
tts = MockTTSAdapter()
visuals = MockVisualAdapter()
stream = DryRunStreamAdapter()

ALLOW_GPU = os.getenv('SONICFORGE_ALLOW_GPU', 'false').lower() == 'true'
ALLOW_PAID = os.getenv('SONICFORGE_ALLOW_PAID_API', 'false').lower() == 'true'
ALLOW_PUBLIC_STREAM = os.getenv('SONICFORGE_ALLOW_PUBLIC_STREAM', 'false').lower() == 'true'

@app.middleware('http')
async def enforce_fail_closed_policy(request: Request, call_next):
    if request.url.path.startswith('/static/'):
        return await call_next(request)
    blocked = blocked_action_for(request.url.path, os.environ)
    if blocked is not None:
        return JSONResponse(status_code=403, content={
            'ok': False,
            'status': 'blocked_by_server_enforced_fail_closed_policy',
            'path': request.url.path,
            'reason': blocked.reason,
            'approval_flag': blocked.approval_flag,
            'starts_gpu': False,
            'starts_paid_api': False,
            'publishes_stream': False,
            'records_audio': False,
            'uploads_private_media': False,
        })
    return await call_next(request)

@app.get('/')
def index():
    return FileResponse(static_dir / 'index.html')

@app.get('/launch')
def launch():
    return FileResponse(static_dir / 'launch.html')

@app.get('/api/launch-status')
def launch_status():
    """Read-only launch cockpit: datasets, sample prompts, safety gates."""
    return build_launch_status()

@app.get('/visualizer')
def visualizer():
    return FileResponse(static_dir / 'visualizer.html')

@app.get('/about')
def about():
    return FileResponse(static_dir / 'about.html')

@app.get('/vanta')
def vanta():
    return FileResponse(static_dir / 'vanta.html')

@app.get('/station')
def station():
    return FileResponse(static_dir / 'station.html')

@app.get('/parallel-party')
def parallel_party():
    return FileResponse(static_dir / 'parallel-party.html')

@app.get('/setup')
def setup():
    return FileResponse(static_dir / 'setup.html')

@app.get('/agents')
def agents():
    return FileResponse(static_dir / 'agents.html')

@app.get('/workflows')
def workflows():
    return FileResponse(static_dir / 'workflows.html')

@app.get('/terminal-visuals')
def terminal_visuals():
    return FileResponse(static_dir / 'terminal-visuals.html')

@app.get('/health')
def health():
    return {
        'ok': True,
        'service': 'sonicforge-live',
        'entity': state.entity,
        'starts_gpu': False,
        'starts_paid_api': False,
        'publishes_stream': False,
        'approval_flags': {
            'SONICFORGE_ALLOW_GPU': ALLOW_GPU,
            'SONICFORGE_ALLOW_PAID_API': ALLOW_PAID,
            'SONICFORGE_ALLOW_PUBLIC_STREAM': ALLOW_PUBLIC_STREAM,
            'SONICFORGE_ALLOW_COMFY_PROMPT': os.getenv('SONICFORGE_ALLOW_COMFY_PROMPT', 'false').lower() == 'true',
            'SONICFORGE_ALLOW_MODEL_DOWNLOADS': os.getenv('SONICFORGE_ALLOW_MODEL_DOWNLOADS', 'false').lower() == 'true',
            'SONICFORGE_ALLOW_RECORDING': os.getenv('SONICFORGE_ALLOW_RECORDING', 'false').lower() == 'true',
            'SONICFORGE_ALLOW_UPLOADS': os.getenv('SONICFORGE_ALLOW_UPLOADS', 'false').lower() == 'true',
        },
        'adapters': {
            'music': music.name,
            'tts': tts.name,
            'visual': visuals.name,
            'stream': stream.name,
        }
    }

@app.get('/api/safety-policy')
def safety_policy():
    return safety_policy_snapshot(os.environ)

@app.get('/api/state')
def get_state():
    return state

@app.post('/api/signal/acquire')
def acquire_signal(payload: dict):
    """Dry-run station signal acquisition contract.

    Models local/RunPod/Modal/custom endpoint warmup without calling providers,
    starting GPUs, recording, or publishing streams unless explicit environment
    approval flags are already set.
    """
    return acquire_signal_contract(payload, {
        'ALLOW_GPU': ALLOW_GPU,
        'ALLOW_PAID': ALLOW_PAID,
        'ALLOW_PUBLIC_STREAM': ALLOW_PUBLIC_STREAM,
    })

@app.post('/api/signal/session')
def signal_session(payload: dict):
    """Build a bounded autonomous DJ session plan from a station signal."""
    return session_plan_contract(payload, {
        'ALLOW_GPU': ALLOW_GPU,
        'ALLOW_PAID': ALLOW_PAID,
        'ALLOW_PUBLIC_STREAM': ALLOW_PUBLIC_STREAM,
    })

@app.post('/api/guide')
def update_guide(payload: dict):
    guide = str(payload.get('guide', '')).strip()
    mode = payload.get('mode')
    energy = payload.get('energy')
    bpm = payload.get('bpm')
    if guide:
        state.guide = guide
    if mode:
        state.mode = mode
    if energy is not None:
        state.energy = int(energy)
    if bpm is not None:
        state.bpm = int(bpm)
    return SonicEvent(type='state.updated', message='Guide updated', payload=state.model_dump())

@app.post('/api/generate-track')
async def generate_track(brief: TrackBrief):
    state.queue.append(brief)
    result = await music.generate(brief)
    return SonicEvent(type='track.generated', message=f'Generated local sketch: {brief.title}', payload=result)

@app.post('/api/talk-break')
async def talk_break(talk: TalkBreak):
    state.last_talk = talk
    result = await tts.speak(talk)
    return SonicEvent(type='talk.queued', message='Talk-break queued', payload=result)

@app.post('/api/visual')
async def visual(visual: VisualCue):
    state.current_visual = visual
    result = await visuals.cue(visual)
    return SonicEvent(type='visual.updated', message='Visual cue updated', payload=result)

@app.post('/api/stream/plan')
async def stream_plan(plan: StreamPlan):
    if plan.publishes_stream and not ALLOW_PUBLIC_STREAM:
        plan.publishes_stream = False
        plan.notes.append('Public stream disabled because SONICFORGE_ALLOW_PUBLIC_STREAM is not true.')
    result = await stream.plan(plan)
    return SonicEvent(type='stream.plan', message='Stream plan prepared', payload=result)

@app.get('/api/crate-cache')
def crate_cache():
    crate = load_prompt_crate()
    safe_entries = []
    for entry in crate.get('entries', []):
        safe_entries.append({
            **entry,
            'starts_gpu': False,
            'starts_paid_api': False,
            'publishes_stream': False,
        })
    return {
        **crate,
        'entries': safe_entries,
        'starts_gpu': False,
        'starts_paid_api': False,
        'publishes_stream': False,
        'ui_copy': 'Prompt crate cache is local seed memory for Deck B planning; review-only and provider-closed by default.',
    }

@app.get('/api/set-manifest')
def set_manifest():
    return load_set_manifest(state.set_title)

@app.get('/api/program-status')
def program_status():
    """Read-only honest status for mock audio vs real generated audio vs rendered program."""
    return build_program_status(state, load_set_manifest(state.set_title))

@app.get('/api/program-manifest')
def program_manifest():
    """Render crossfade/ducking/LUFS metadata from the local set manifest only."""
    return render_program_manifest(state.set_title, load_set_manifest(state.set_title))

@app.get('/api/mc-breaks/preview')
def mc_breaks_preview():
    """Preview text-first MC break modes without TTS/audio/provider side effects."""
    return build_mc_break_preview(state)

@app.get('/api/timeline')
def get_timeline():
    """Read a bounded local run-of-show timeline without provider side effects."""
    return load_demo_timeline(state)

@app.post('/api/timeline/build')
def build_timeline():
    """Write generated/timeline/demo-set.json as a local plan only."""
    return write_demo_timeline(state)

@app.get('/api/dj-brain/state')
def dj_brain_state():
    """Read-only snapshot of DJ VANTA's local performer brain.

    This endpoint exposes the current Deck A/B handoff model and a deterministic
    preview of the next transition without generating files, calling providers,
    appending set manifests, recording audio, or publishing streams.
    """
    preview = plan_next_segment(state)
    transition = preview['transition'].model_dump()
    return {
        'ok': True,
        'entity': state.entity,
        'product': state.product,
        'mode': state.mode,
        'set_title': state.set_title,
        'bpm': state.bpm,
        'energy': state.energy,
        'crowd_signal': transition['crowd'],
        'phrase_count': transition['phrase'],
        'beatmatch': transition['beatmatch'],
        'eq_move': transition['eq_moves'][0] if transition['eq_moves'] else {},
        'cue_points': transition['cue_points'],
        'crossfader': transition['crossfader'],
        'deck_a': state.deck_a.model_dump(),
        'deck_b': preview['deck_b'].model_dump(),
        'crate_selection': preview['crate_selection'],
        'survival_kit': preview['survival_kit'],
        'culture_cue': preview['culture_cue'],
        'mc_break': preview['mc_break'],
        'honest_status': 'read_only_preview_no_generation_no_continuous_mixer',
        'starts_gpu': False,
        'starts_paid_api': False,
        'publishes_stream': False,
        'records_audio': False,
        'uploads_private_media': False,
        'human_override': 'Sober human operator keeps STOP SET / CHILL MODE authority.',
    }

@app.post('/api/next-segment')
async def next_segment():
    segment = plan_next_segment(state)
    track = segment['track']
    talk = segment['talk']
    visual = segment['visual']
    state.queue.append(track)
    state.last_talk = talk
    state.current_visual = visual
    state.deck_a = segment['deck_a']
    state.deck_b = segment['deck_b']
    track_result = await music.generate(track)
    talk_result = await tts.speak(talk)
    visual_result = await visuals.cue(visual)
    state.deck_b.status = 'generated_mock'
    state.deck_b.artifact_path = track_result.get('file')
    payload = {
        'track': track_result,
        'talk': talk_result,
        'visual': visual_result,
        'mix': segment['mix'],
        'transition': segment['transition'].model_dump(),
        'deck_a': state.deck_a.model_dump(),
        'deck_b': state.deck_b.model_dump(),
        'visual_spell': segment['visual_spell'],
        'comfyui_visual_spell': segment['comfyui_visual_spell'],
        'crate_selection': segment['crate_selection'],
        'survival_kit': segment['survival_kit'],
        'culture_cue': segment['culture_cue'],
        'mc_break': segment['mc_break'],
        'state': state.model_dump(),
    }
    payload['set_manifest'] = append_set_manifest(state.set_title, payload)
    payload['program_status'] = build_program_status(state, load_set_manifest(state.set_title))
    payload['program_manifest'] = render_program_manifest(state.set_title, load_set_manifest(state.set_title))
    return SonicEvent(
        type='track.generated',
        message=f'Planned continuous segment: {track.title}',
        payload=payload,
    )

@app.post('/api/sample-pad')
async def sample_pad(payload: dict):
    """Trigger a local-only ritual pad cue for the control deck.

    These are metadata events for browser/OBS/TouchDesigner/ComfyUI routing tests.
    They do not play audio, start recording, call providers, publish streams, or
    open paid GPU lanes.
    """
    pad = str(payload.get('pad', 'VANTA')).upper().strip()
    pads = {
        'VANTA': {
            'label': 'VANTA voice tag',
            'talk_break_mode': 'lore',
            'message': 'DJ VANTA online: Virtual Autonomous Nocturnal Transmission Artist, local-first and human-overridable.',
            'visual_spell': 'VANTA_SIGNAL INTERGALACTIC_DJS',
        },
        'HYDRATE': {
            'label': 'hydration ping',
            'talk_break_mode': 'survival',
            'message': 'Water station check: sip water, protect your ears, and keep the dancefloor kind.',
            'visual_spell': 'SURVIVAL_PING HYDRATE',
        },
        'BUDDY': {
            'label': 'buddy check',
            'talk_break_mode': 'survival',
            'message': 'Buddy check: know your exits, agree on a meet-up point, and do not let anyone disappear alone.',
            'visual_spell': 'SURVIVAL_PING BUDDY_CHECK',
        },
        'DROP': {
            'label': 'drop marker',
            'talk_break_mode': 'hype',
            'message': 'Phrase lock: bass swap armed on bar seventeen, drop release on bar thirty-three.',
            'visual_spell': 'PHRASE_LOCK 32 // DROP_RELEASE BAR_33',
        },
        'PORTAL': {
            'label': 'Deck B portal',
            'talk_break_mode': 'lore',
            'message': 'Incoming portal: Deck B visual spell is dry-run routed to browser first, ComfyUI later only with approval.',
            'visual_spell': 'DECK_B PORTAL // COMFYUI_DRY_RUN',
        },
        'CHILL': {
            'label': 'chill zone',
            'talk_break_mode': 'survival',
            'message': 'Cool-down orbit: step out, sit down, breathe, find the chill zone, and bring a sober human if help is needed.',
            'visual_spell': 'SURVIVAL_PING CHILL_ZONE',
        },
        'AIRHORN': {
            'label': 'mock airhorn',
            'talk_break_mode': 'hype',
            'message': 'Airhorn marker queued as text metadata only; no speaker blast or sample playback is started.',
            'visual_spell': 'AIRHORN_TEXT_ONLY // NO_AUDIO_PLAYBACK',
        },
        'RECORD': {
            'label': 'manifest marker',
            'talk_break_mode': 'technical',
            'message': 'Record marker noted for the future set manifest; no recording or stream publishing starts from this pad.',
            'visual_spell': 'MANIFEST_MARKER RECORD_INTENT_CLOSED',
        },
    }
    cue = pads.get(pad, pads['VANTA'])
    event_payload = {
        **cue,
        'pad': pad if pad in pads else 'VANTA',
        'mode': 'dry_run',
        'audio_cue': 'metadata_only_no_audio_playback',
        'route_targets': ['browser_control_deck', 'browser_visualizer', 'touchdesigner_contract', 'comfyui_dry_run'],
        'starts_gpu': False,
        'starts_paid_api': False,
        'publishes_stream': False,
        'requires_human': False,
        'human_override': 'STOP SET / CHILL MODE stays with the sober human operator.',
        'safe_scope': 'community-care and show-control cue only; not medical/legal/drug-use advice',
    }
    return SonicEvent(type='system.ready', message=f"Sample pad ritual cue: {event_payload['label']}", payload=event_payload)

@app.get('/api/backends')
def backends():
    """Read-only backend lane status card; no provider preflight or generation."""
    return build_backend_status()

@app.get('/api/ecosystem')
def ecosystem():
    """Read-only Intergalactic DJs collective / forkable ecosystem map."""
    return build_ecosystem_status()

@app.websocket('/ws/control')
async def ws_control(ws: WebSocket):
    await ws.accept()
    await ws.send_json(SonicEvent(type='system.ready', message='DJ VANTA online', payload=state.model_dump()).model_dump())
    try:
        while True:
            data = await ws.receive_json()
            cmd = data.get('cmd')
            if cmd == 'guide':
                state.guide = str(data.get('guide', state.guide))
                await ws.send_json(SonicEvent(type='state.updated', message='Guide updated over websocket', payload=state.model_dump()).model_dump())
            elif cmd == 'visual':
                v = VisualCue(**data.get('visual', {}))
                state.current_visual = v
                await ws.send_json(SonicEvent(type='visual.updated', message='Visual cue updated over websocket', payload=v.model_dump()).model_dump())
            elif cmd == 'track':
                brief = TrackBrief(**data.get('brief', {}))
                result = await music.generate(brief)
                await ws.send_json(SonicEvent(type='track.generated', message=f'Generated sketch: {brief.title}', payload=result).model_dump())
            elif cmd == 'talk':
                talk = TalkBreak(**data.get('talk', {'text':'Vanta is online.'}))
                result = await tts.speak(talk)
                await ws.send_json(SonicEvent(type='talk.queued', message='Talk-break queued', payload=result).model_dump())
            else:
                await ws.send_json(SonicEvent(type='system.warning', message=f'Unknown command: {cmd}', payload=data).model_dump())
    except WebSocketDisconnect:
        return
