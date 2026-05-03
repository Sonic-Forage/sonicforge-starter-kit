from pathlib import Path
import ast, json, math, sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

required = [
    'README.md','AGENTS.md','requirements.txt','server/main.py','server/schemas.py',
    'server/crate_cache.py','catalog/crate-cache/prompt-crate-seed.json',
    'server/adapters/mock.py','server/adapters/comfyui.py','server/adapters/runpod.py','server/set_manifest.py','server/timeline.py','server/program_status.py','server/program_manifest_renderer.py','server/backend_status.py','server/mc_breaks.py','server/launch_status.py',
    'app/static/index.html','app/static/launch.html','app/static/visualizer.html','docs/ARCHITECTURE.md','docs/DISCOVERY.md',
    'docs/RTMP_OBS_RESOLUME_SPOUT.md','docs/RESOURCE_POLICY.md',
    'docs/hermes-skill-package.md',
    'docs/product/HACKATHON_SUBMISSION_CHECKLIST.md',
    'docs/LAUNCH_COCKPIT.md',
    'skills/sonicforge-live-dj-vanta/SKILL.md',
    'docs/integrations/VISUAL_SPELL_ROUTING_CUE_PACKETS.md',
    'docs/integrations/COMFYUI_API.md', 'docs/integrations/MODAL_ENDPOINT.md',
    'docs/integrations/RUNPOD_ACE_STEP.md',
    'docs/integrations/RESOLUME_ARENA_MCP.md',
    'docs/integrations/TOUCHDESIGNER_SPOUT_SYPHON.md',
    'docs/integrations/TTS_ADAPTER_CONTRACT.md', '.env.example',
    'scripts/verify_survival_harm_reduction.py'
]
missing = [p for p in required if not (ROOT/p).exists()]
if missing:
    print('missing', missing); sys.exit(1)
for py in list((ROOT/'server').rglob('*.py')) + list((ROOT/'scripts').glob('*.py')):
    ast.parse(py.read_text())
if not (ROOT/'scripts/smoke_local_demo.py').exists():
    print('missing local demo smoke test script'); sys.exit(1)
health_text = (ROOT/'server/main.py').read_text()
checks = ['starts_gpu', 'starts_paid_api', 'publishes_stream', '/ws/control', 'RunPodAceStepAdapter', 'ComfyUIAdapter', '/api/next-segment', '/api/dj-brain/state', 'read_only_preview_no_generation_no_continuous_mixer', '/api/crate-cache', '/api/sample-pad', '/api/set-manifest', '/api/program-status', 'build_program_status', '/api/program-manifest', 'render_program_manifest', '/api/backends', 'build_backend_status', '/api/mc-breaks/preview', 'build_mc_break_preview', '/api/timeline', '/api/timeline/build', 'append_set_manifest', 'metadata_only_no_audio_playback', '/launch', '/api/launch-status', 'build_launch_status']
for c in checks:
    if c not in health_text:
        print('missing check string', c); sys.exit(1)
planner_text = (ROOT/'server/planner.py').read_text() + (ROOT/'server/schemas.py').read_text() + (ROOT/'server/crate_cache.py').read_text() + (ROOT/'server/mc_breaks.py').read_text()
for c in ['BeatmatchPlan', 'PhrasePlan', 'EQMove', 'CuePoint', 'CrowdState', 'TransitionPlan', 'CrossfaderPlan', 'CrossfaderPoint', 'equal_power', 'gainA = cos((value + 1) / 2 * PI / 2)', 'bass swap', 'DeckState', 'Deck A / current groove', 'Deck B / incoming portal', 'visual.spell', 'routing_contracts', 'resolume_contract', 'manual_operator_copy_to_resolume_or_future_mcp', 'touchdesigner_contract', 'manual_operator_copy_to_touchdesigner_or_future_twozero_mcp', 'comfyui.visual_spell.cue', 'api_routes_when_enabled', '/prompt', 'requires_human_approval', 'crate_selection', 'select_crate_entry', 'Prompt crate', 'score_breakdown', 'repetition_guard', 'energy_arc', 'genre_novelty_repetition_guard_energy_arc_v1', 'survival_kit', 'culture_cue', 'mc_break', 'build_mc_break', 'MC_BREAK_MODES', 'survival', 'history', 'hype', 'lore', 'technical', 'text_first_no_audio_output', 'sends_voice_message', 'voice_cloning_enabled', 'SURVIVAL_PING', 'community-care reminder only', 'disco-house-techno-rave-vj-ai', '_synthetic_crowd_state', 'warmup', 'curious', 'locked-in', 'peak', 'cooldown', 'care_intervention']:
    if c not in planner_text:
        print('missing real DJ feature model string', c); sys.exit(1)
ui = (ROOT/'app/static/index.html').read_text() + (ROOT/'app/static/launch.html').read_text() + (ROOT/'app/static/visualizer.html').read_text() + (ROOT/'app/static/main.js').read_text()
for c in ['DJ VANTA', 'Generate Local WAV Sketch', 'Open VJ Window', 'OBS capture', 'Resolume', 'Plan Next Continuous Segment', 'Lineage + Rave Survival Kit', 'community-care reminders only', 'human override', 'renderSegment', 'Equal-power crossfader', 'crossfaderStatus', 'ComfyUI visual-spell cue', 'comfySpellStatus', 'comfyui_visual_spell', 'Text-first MC break generator', 'text-first-mc-breaks', 'renderMcBreakPreview', '/api/mc-breaks/preview', 'survival · history · hype · lore · technical', 'Culture mode selector', 'culture-mode-selector', 'applyCultureModeSelector', 'culture_mode_selector_fail_closed', 'history · hype · safety · lore selector', 'text_first_mc_break_generator_fail_closed', 'DJ Brain read-only preview', 'dj-brain-status-panel', 'renderDjBrainState', 'BPM / phrase / EQ / crowd signal', '/api/dj-brain/state', 'read_only_preview_no_generation_no_continuous_mixer', 'Prompt Crate Cache', 'Deck B crate-digging memory', 'renderCrateCache', '/api/crate-cache', 'Deck A / Deck B handoff cards', 'deck-ab-status-cards', 'renderDeckCards', 'deckACard', 'deckBCard', 'generated_mock', 'Sample-pad ritual buttons', 'sample-pad-rituals', 'renderSamplePad', '/api/sample-pad', 'metadata-only dry runs', 'Local Set Manifest Writer', 'local-set-manifest', 'setManifestStatus', 'generated/sets/', 'Honest status: mock audio vs real generated audio vs rendered program', 'honest-program-status', 'Program audio truth panel', 'renderProgramStatus', '/api/program-status', 'honest_program_status_mock_audio_no_rendered_program', 'mock audio sketches', 'real generated audio', 'rendered program mix', 'Local program manifest renderer with crossfade/ducking/LUFS metadata', 'program-manifest-renderer', 'renderProgramManifest', '/api/program-manifest', 'local_program_manifest_renderer_metadata_only', 'renders_program_audio=false', 'Backend status card endpoint/UI', 'backend-status-card', 'renderBackendStatus', '/api/backends', 'backend_status_card_fail_closed_no_provider_calls', 'closed_until_human_yes', 'blocked action', 'SDF/MSDF text shader future lane', 'sdf-msdf-text-shader-lane', 'sdf_text_fallback', 'MSDF_ATLAS_DRY_RUN', 'no remote shader downloads', 'starts_gpu=false', 'starts_paid_api=false', 'publishes_stream=false', 'records_audio=false', 'requires_human_approval=true', 'Dry-run autopilot controls', 'dry-run-autopilot-controls', 'renderTimeline', 'loadTimeline', 'startDryRunAutopilot', 'stopDryRunAutopilot', 'timeline_plan_only_no_generation_no_continuous_mixer', 'no live scheduler', 'code_rain', 'eq_bands', 'subtitle_spell', 'dual ASCII spectrograph', 'Dual ASCII spectrograph', 'COMFYUI_DRY_RUN', 'TOUCHDESIGNER_CONTRACT', 'care_intervention', 'visual_palette_hint']:
    if c not in ui:
        print('missing UI string', c); sys.exit(1)
for c in ['Talk-over-intro ducking plan', 'talkDuckingStatus', 'talk_over_intro_ducking_plan_metadata_only', 'EQ move schedule', 'eqMoveScheduleStatus', 'low swap · mid carve · high shimmer']:
    if c not in ui:
        print('missing talk-over-intro ducking/EQ schedule UI string', c); sys.exit(1)
for c in ['_talk_over_intro_ducking_plan', 'talk_over_intro_ducking_plan_metadata_only', 'target_clear_before_bar', 'sidechain_hint', '_eq_move_schedule', 'eq_move_schedule_metadata_only_no_audio_mixer', 'LOW swap', 'MID carve', 'HIGH shimmer']:
    if c not in planner_text:
        print('missing talk-over-intro ducking/EQ schedule planner string', c); sys.exit(1)
if not (ROOT/'site/data/final-demo-acceptance-checklist.json').exists():
    print('missing final demo acceptance checklist manifest'); sys.exit(1)
if not (ROOT/'docs/product/FINAL_DEMO_ACCEPTANCE_CHECKLIST.md').exists():
    print('missing final demo acceptance checklist doc'); sys.exit(1)
crate = json.loads((ROOT/'catalog/crate-cache/prompt-crate-seed.json').read_text())
if crate.get('status') != 'local_seed_only' or len(crate.get('entries', [])) < 5:
    print('invalid prompt crate cache seed'); sys.exit(1)
for entry in crate['entries']:
    for key in ['id', 'name', 'mode', 'genre_tags', 'prompt_stack', 'visual_spell_text', 'survival_ping', 'lineage_note']:
        if key not in entry:
            print('prompt crate entry missing', key, entry.get('id')); sys.exit(1)


from server.launch_status import build_launch_status  # noqa: E402
launch_status = build_launch_status()
if not launch_status.get('ok'):
    print('launch cockpit status not ok'); sys.exit(1)
for gate_key in ['starts_gpu', 'trains_models', 'uploads_private_media']:
    if launch_status.get(gate_key) is not False:
        print('launch cockpit gate not fail-closed', gate_key, launch_status.get(gate_key)); sys.exit(1)
if len(launch_status.get('datasets', [])) < 2 or sum(d.get('track_count', 0) for d in launch_status.get('datasets', [])) < 40:
    print('launch cockpit dataset inventory incomplete'); sys.exit(1)
if len(launch_status.get('sample_prompts', [])) != 2:
    print('launch cockpit sample prompts missing'); sys.exit(1)
launch_ui = (ROOT/'app/static/launch.html').read_text()
for c in ['DJ VANTA LAUNCH', 'Training not started', 'explicit human approval required', 'Copy Prompt', 'Fail-closed gates', '/api/launch-status']:
    if c not in launch_ui:
        print('launch cockpit UI missing', c); sys.exit(1)
launch_doc = (ROOT/'docs/LAUNCH_COCKPIT.md').read_text()
for c in ['read-only control surface', 'does **not** start', 'Forkable architecture', 'server/launch_status.py']:
    if c not in launch_doc:
        print('launch cockpit doc missing', c); sys.exit(1)

# Semantic safety/contract checks for the hackathon-critical dual-deck lane.
# Keep these direct planner assertions so verify.py proves the JSON contract without
# starting providers, GPUs, streams, or a continuous mixer.
from server.planner import plan_next_segment  # noqa: E402
from server.schemas import SetState  # noqa: E402

segment = plan_next_segment(SetState())
crate_meta = segment['crate_selection']
for key in ['score_breakdown', 'energy_arc', 'repetition_guard']:
    if key not in crate_meta:
        print('crate selector missing explainable metadata', key); sys.exit(1)
if crate_meta['score_breakdown'].get('selector') != 'genre_novelty_repetition_guard_energy_arc_v1':
    print('crate selector did not use the expected genre/novelty/repetition/energy arc version'); sys.exit(1)
if crate_meta['energy_arc'].get('target') != 5 or crate_meta['repetition_guard'].get('window') != 3:
    print('crate selector missing warmup energy arc or repetition window'); sys.exit(1)
repeat_guard_segment = plan_next_segment(SetState(queue=[segment['track']]))
if repeat_guard_segment['crate_selection'].get('id') == crate_meta.get('id'):
    print('crate repetition guard failed to avoid immediate repeat'); sys.exit(1)
if repeat_guard_segment['crate_selection'].get('repetition_guard', {}).get('recent_crate_ids') != [crate_meta.get('id')]:
    print('crate repetition guard did not report recent crate id'); sys.exit(1)
for key in ['track', 'talk', 'visual', 'mix', 'transition', 'deck_a', 'deck_b', 'visual_spell', 'comfyui_visual_spell', 'crate_selection', 'survival_kit', 'culture_cue', 'mc_break']:
    if key not in segment:
        print('planner missing segment key', key); sys.exit(1)
if segment['deck_a'].role != 'A' or segment['deck_b'].role != 'B':
    print('planner deck roles are not stable A/B'); sys.exit(1)
if segment['deck_b'].status not in {'incoming', 'generated_mock'}:
    print('deck_b not in safe local incoming/generated_mock status', segment['deck_b'].status); sys.exit(1)
if segment['deck_b'].visual_spell.get('mode') != 'dry_run':
    print('deck_b visual spell is not dry_run'); sys.exit(1)
routes = segment['visual_spell'].get('routing_contracts', {})
for route_name in ['browser', 'resolume', 'touchdesigner', 'comfyui']:
    if route_name not in routes:
        print('visual spell missing routing contract', route_name); sys.exit(1)
for route_name in ['resolume', 'touchdesigner', 'comfyui']:
    route = routes[route_name]
    if route.get('mode') != 'dry_run' or route.get('requires_human_approval') is not True:
        print('visual spell route not dry-run/human-approved', route_name); sys.exit(1)
    for flag in ['starts_gpu', 'starts_paid_api', 'publishes_stream', 'records_audio']:
        if route.get(flag) is not False:
            print('visual spell route flag not fail-closed', route_name, flag); sys.exit(1)
if routes['resolume'].get('adapter') != 'resolume_contract' or 'Resolume' not in routes['resolume'].get('composition', ''):
    print('Resolume cue packet missing adapter/composition contract'); sys.exit(1)
if routes['touchdesigner'].get('adapter') != 'touchdesigner_contract' or routes['touchdesigner'].get('uniforms', {}).get('uBassSwapBar') != 17:
    print('TouchDesigner cue packet missing adapter/uniform contract'); sys.exit(1)

crossfader = segment['transition'].crossfader
if crossfader.curve != 'equal_power' or 'cos' not in crossfader.formula or 'sin' not in crossfader.formula:
    print('crossfader formula missing equal-power cosine/sine contract'); sys.exit(1)
if len(crossfader.automation) < 5:
    print('crossfader automation missing representative points'); sys.exit(1)
midpoint = next((p for p in crossfader.automation if math.isclose(p.value, 0.0, abs_tol=1e-6)), None)
if midpoint is None or not math.isclose(midpoint.gain_a, 0.7071, abs_tol=0.002) or not math.isclose(midpoint.gain_b, 0.7071, abs_tol=0.002):
    print('crossfader midpoint is not approximately 0.7071/0.7071'); sys.exit(1)
if segment['mix']['crossfader_curve'].get('status') != 'metadata_only_no_continuous_mixer_started':
    print('mix crossfader status does not stay honest about no continuous mixer'); sys.exit(1)
ducking_plan = segment['mix'].get('talk_over_intro_ducking_plan', {})
if ducking_plan.get('status') != 'talk_over_intro_ducking_plan_metadata_only':
    print('mix missing talk-over-intro ducking metadata plan'); sys.exit(1)
if ducking_plan.get('talk_over_intro_seconds') != segment['talk'].seconds or ducking_plan.get('duck_music_db') != segment['talk'].duck_music_db:
    print('talk-over-intro ducking plan does not match talk cue timing/ducking'); sys.exit(1)
if len(ducking_plan.get('automation', [])) < 3 or ducking_plan['automation'][-1].get('music_gain_db') != 0.0:
    print('talk-over-intro ducking automation missing restore step'); sys.exit(1)
for flag in ['starts_gpu', 'starts_paid_api', 'publishes_stream', 'records_audio']:
    if ducking_plan.get(flag) is not False:
        print('talk-over-intro ducking plan flag not fail-closed', flag); sys.exit(1)
eq_schedule = segment['mix'].get('eq_move_schedule', {})
if eq_schedule.get('status') != 'eq_move_schedule_metadata_only_no_audio_mixer':
    print('mix missing metadata-only EQ move schedule'); sys.exit(1)
for key in ['low_swap', 'mid_carve', 'high_shimmer', 'automation']:
    if key not in eq_schedule:
        print('EQ move schedule missing key', key); sys.exit(1)
if len(eq_schedule.get('automation', [])) < 4:
    print('EQ move schedule missing representative automation steps'); sys.exit(1)
if not any(move.get('bar') == 17 and move.get('low_db') == 0.0 for move in eq_schedule.get('automation', [])):
    print('EQ move schedule missing bar-17 low-swap unity handoff'); sys.exit(1)
for flag in ['starts_gpu', 'starts_paid_api', 'publishes_stream', 'records_audio']:
    if eq_schedule.get(flag) is not False:
        print('EQ move schedule flag not fail-closed', flag); sys.exit(1)
from server.program_status import build_program_status  # noqa: E402
program_status = build_program_status(SetState(), {})
if program_status.get('status') != 'honest_program_status_mock_audio_no_rendered_program':
    print('program status missing honest mock/no-rendered-program state'); sys.exit(1)
for lane in ['mock_audio_sketch', 'real_generated_audio', 'rendered_program_mix', 'recording_and_stream']:
    if lane not in program_status.get('lanes', {}):
        print('program status missing lane', lane); sys.exit(1)
for flag in ['starts_gpu', 'starts_paid_api', 'publishes_stream', 'records_audio', 'uploads_private_media']:
    if program_status.get(flag) is not False:
        print('program status flag not fail-closed', flag); sys.exit(1)
if program_status['lanes']['rendered_program_mix'].get('state') != 'not_rendered':
    print('program status claims a rendered program exists'); sys.exit(1)

from server.program_manifest_renderer import render_program_manifest  # noqa: E402
program_manifest_sample = {
    'manifest_path': 'generated/sets/demo/manifest.json',
    'segments': [{
        'segment_id': 'seg-001',
        'track': {'file': 'generated/audio/mock.wav', 'duration_seconds': 12, 'adapter': 'mock_music_adapter'},
        'talk': {'text': 'metadata-only run sheet', 'duck_music_db': -8},
        'visual': {'output_url': '/visualizer'},
        'mix': segment['mix'],
        'transition': segment['transition'].model_dump(),
        'visual_spell': segment['visual_spell'],
        'survival_kit': segment['survival_kit'],
        'culture_cue': segment['culture_cue'],
    }],
}
program_manifest = render_program_manifest(SetState().set_title, program_manifest_sample)
if program_manifest.get('status') != 'local_program_manifest_renderer_metadata_only':
    print('program manifest renderer missing metadata-only status'); sys.exit(1)
if program_manifest.get('renders_program_audio') is not False or program_manifest.get('records_audio') is not False:
    print('program manifest renderer implies audio render or recording'); sys.exit(1)
for flag in ['starts_gpu', 'starts_paid_api', 'publishes_stream', 'uploads_private_media']:
    if program_manifest.get(flag) is not False:
        print('program manifest renderer flag not fail-closed', flag); sys.exit(1)
if not program_manifest.get('segments') or program_manifest['segments'][0].get('honest_status') != 'program_manifest_renderer_metadata_only_no_audio_render':
    print('program manifest renderer did not create segment run-sheet rows'); sys.exit(1)
if program_manifest['segments'][0].get('crossfade_seconds') is None or program_manifest['segments'][0].get('duck_music_db') is None or program_manifest['segments'][0].get('target_lufs') is None:
    print('program manifest renderer missing crossfade/ducking/LUFS metadata'); sys.exit(1)

from server.backend_status import build_backend_status  # noqa: E402
backend_status = build_backend_status()
if backend_status.get('status') != 'backend_status_card_fail_closed_no_provider_calls':
    print('backend status missing fail-closed no-provider-calls status'); sys.exit(1)
if len(backend_status.get('lanes', [])) < 7:
    print('backend status missing expected provider lanes'); sys.exit(1)
required_backend_lanes = {'comfyui_visual_workflow', 'runpod_ace_step_audio', 'modal_serverless_gpu', 'touchdesigner_twozero', 'resolume_mcp', 'obs_rtmp_streaming', 'tts_voice_output'}
if {lane.get('lane') for lane in backend_status.get('lanes', [])} != required_backend_lanes:
    print('backend status lanes mismatch'); sys.exit(1)
for lane in backend_status['lanes']:
    if lane.get('mode') != 'dry_run_contract_only' or lane.get('requires_human_approval') is not True:
        print('backend lane not dry-run/human-approved', lane.get('lane')); sys.exit(1)
    if not lane.get('blocked_without_approval') or not lane.get('approval_question'):
        print('backend lane missing approval/blocked action copy', lane.get('lane')); sys.exit(1)
    for flag in ['starts_gpu', 'starts_paid_api', 'publishes_stream', 'records_audio', 'uploads_private_media']:
        if lane.get(flag) is not False:
            print('backend lane flag not fail-closed', lane.get('lane'), flag); sys.exit(1)
for flag in ['starts_gpu', 'starts_paid_api', 'publishes_stream', 'records_audio', 'uploads_private_media']:
    if backend_status.get(flag) is not False:
        print('backend status top-level flag not fail-closed', flag); sys.exit(1)

timeline_text = (ROOT/'server/timeline.py').read_text()
for c in ['10_minute_private_demo', '20_minute_house_party_preview', '45_minute_full_arc_dry_run', 'timeline_plan_only_no_generation_no_continuous_mixer', 'starts_gpu', 'starts_paid_api', 'publishes_stream', 'records_audio', 'uploads_private_media']:
    if c not in timeline_text:
        print('timeline planner missing safety/planning string', c); sys.exit(1)
from server.timeline import build_demo_timeline  # noqa: E402

timeline = build_demo_timeline(SetState())
if timeline.get('status') != 'local_plan_only_fail_closed' or len(timeline.get('plans', [])) != 3:
    print('timeline did not return three fail-closed demo plans'); sys.exit(1)
for flag in ['starts_gpu', 'starts_paid_api', 'publishes_stream', 'records_audio', 'uploads_private_media']:
    if timeline.get(flag) is not False:
        print('timeline safety flag not fail-closed', flag); sys.exit(1)
for plan in timeline['plans']:
    if not plan.get('segments'):
        print('timeline plan missing segments', plan.get('id')); sys.exit(1)
    first = plan['segments'][0]
    if not str(first.get('track_title', '')).endswith('Signal 01'):
        print('timeline does not reset queued state for deterministic segment 01', first.get('track_title')); sys.exit(1)
    if 'with waveform gates and neon crowd ghosts with waveform gates' in first.get('visual_scene', ''):
        print('timeline reused mutated visual scene text'); sys.exit(1)
    for row in plan['segments']:
        if row.get('honest_status') != 'timeline_plan_only_no_generation_no_continuous_mixer':
            print('timeline segment honest_status missing', row.get('segment_id')); sys.exit(1)
        if row.get('comfyui_visual_spell', {}).get('mode') != 'dry_run':
            print('timeline ComfyUI cue is not dry_run', row.get('segment_id')); sys.exit(1)

comfy_spell = segment['comfyui_visual_spell']
if comfy_spell.get('mode') != 'dry_run' or comfy_spell.get('workflow') != 'intergalactic-djs-visual-spell':
    print('ComfyUI visual spell is not the expected dry-run workflow'); sys.exit(1)
if comfy_spell.get('output', {}).get('prompt_id') is not None or comfy_spell.get('output', {}).get('files') != []:
    print('ComfyUI visual spell implies real provider output'); sys.exit(1)
for flag in ['starts_gpu', 'starts_paid_api', 'publishes_stream']:
    if comfy_spell.get(flag) is not False or segment['visual_spell'].get(flag) is not False or segment['crate_selection'].get(flag) is not False:
        print('provider/stream flag not fail-closed', flag); sys.exit(1)
if '/prompt' not in comfy_spell.get('api_routes_when_enabled', []):
    print('ComfyUI cue missing future /prompt route contract'); sys.exit(1)

comfy_api_doc = (ROOT/'docs/integrations/COMFYUI_API.md').read_text()
for c in ['COMFYUI_BASE_URL', '/system_stats', '/object_info', '/prompt', '/ws?clientId=', '/history/{prompt_id}', '/view?filename=', 'requires_human_approval', 'COMFYUI_DRY_RUN', 'starts_gpu', 'starts_paid_api', 'publishes_stream', 'OpenCV', 'No medical claims']:
    if c not in comfy_api_doc:
        print('ComfyUI API doc missing safety/route string', c); sys.exit(1)

modal_doc = (ROOT/'docs/integrations/MODAL_ENDPOINT.md').read_text()
for c in ['dry-run / operator-armed only', 'MODAL_SONICFORGE_ENDPOINT_URL', 'MODAL_SONICFORGE_API_TOKEN', 'MODAL_ENABLE_GPU=false', 'MODAL_MAX_TASKS=0', 'modal_dry_run_no_endpoint_called', 'modal_contract_only', 'closed_until_human_yes', 'starts_gpu: false', 'starts_paid_api: false', 'publishes_stream: false', 'records_audio: false', 'uploads_private_media: false', 'trains_models: false', 'requires_human_approval: true', 'No Modal endpoint, cloud GPU, training, upload, recording, stream, cron mutation, or paid provider call is started by default']:
    if c not in modal_doc:
        print('Modal endpoint doc missing safety/route string', c); sys.exit(1)

runpod_doc = (ROOT/'docs/integrations/RUNPOD_ACE_STEP.md').read_text()
for c in ['dry-run / operator-armed only', 'RUNPOD_ENDPOINT_URL', 'RUNPOD_ACE_STEP_API_URL', 'RUNPOD_API_KEY', 'RUNPOD_ENABLE_POD_START=false', 'RUNPOD_ENABLE_ENDPOINT_CALL=false', 'RUNPOD_MAX_JOBS=0', 'ACE_STEP_ENABLE_GENERATION=false', 'runpod_ace_step_dry_run_no_pod_started_no_endpoint_called', 'RunPodAceStepAdapter contract', 'closed_until_human_yes', 'starts_gpu: false', 'starts_paid_api: false', 'publishes_stream: false', 'records_audio: false', 'uploads_private_media: false', 'trains_models: false', 'purchases_services: false', 'requires_human_approval: true', 'No RunPod pod, ACE-Step endpoint, cloud GPU, paid job, training, upload, recording, stream, cron mutation, or provider call is started by default']:
    if c not in runpod_doc:
        print('RunPod ACE-Step endpoint doc missing safety/route string', c); sys.exit(1)

resolume_doc = (ROOT/'docs/integrations/RESOLUME_ARENA_MCP.md').read_text()
for c in ['dry_run_operator_armed_only', 'RESOLUME_MCP_BASE_URL', 'RESOLUME_ENABLE_MCP=false', 'manual_operator_copy_to_resolume_or_future_mcp', 'resolume_contract', 'composition', 'layer', 'clip_or_source', 'effect', 'bpm', 'palette', 'text_overlay', 'survival_overlay', 'starts_gpu: false', 'starts_paid_api: false', 'publishes_stream: false', 'records_audio: false', 'uploads_private_media: false', 'requires_human_approval: true', 'browser `/visualizer` remains the active local fallback', 'No unattended Resolume MCP']:
    if c not in resolume_doc:
        print('Resolume Arena MCP doc missing safety/routing string', c); sys.exit(1)

td_doc = (ROOT/'docs/integrations/TOUCHDESIGNER_SPOUT_SYPHON.md').read_text()
for c in ['dry_run_operator_armed_only', 'TOUCHDESIGNER_MCP_URL', 'manual_operator_copy_to_touchdesigner_or_future_twozero_mcp', 'Spout', 'Syphon', 'td_get_par_info', 'td_get_errors', 'starts_gpu', 'starts_paid_api', 'publishes_stream', 'records_audio', 'uploads_private_media', 'requires_human_approval', 'browser `/visualizer` remains the active local fallback']:
    if c not in td_doc:
        print('TouchDesigner/Spout/Syphon doc missing safety/routing string', c); sys.exit(1)

tts_doc = (ROOT/'docs/integrations/TTS_ADAPTER_CONTRACT.md').read_text()
for c in ['dry-run / operator-armed only', 'text_first_no_audio_output', 'KittenTTS', 'Qwen3-TTS', 'Voxtral TTS', 'TTS_ENABLE_AUDIO_OUTPUT=false', 'SONICFORGE_ALLOW_VOICE_CLONING=false', 'metadata_only_no_audio_playback', 'sends_voice_message: false', 'voice_cloning_enabled: false', 'requires_human_approval: true', 'not medical/legal/drug-use advice', 'No audio generated; human approval required', 'mock-text-talk-break']:
    if c not in tts_doc:
        print('TTS adapter contract doc missing safety/route string', c); sys.exit(1)

text_shader_doc = (ROOT/'docs/visuals/TEXT_SHADER_VISUAL_SPELLS.md').read_text()
for c in ['SDF/MSDF browser fallback', 'sdf-msdf-text-shader-lane', 'sdf_text_fallback', 'MSDF_ATLAS_DRY_RUN', 'PHRASE_LOCK', 'BASS_SWAP', 'SURVIVAL_PING', 'starts_gpu=false', 'starts_paid_api=false', 'publishes_stream=false', 'records_audio=false', 'requires_human_approval=true']:
    if c not in text_shader_doc:
        print('text shader visual spell doc missing SDF/MSDF fallback string', c); sys.exit(1)

hermes_skill_doc = (ROOT/'docs/hermes-skill-package.md').read_text()
for c in ['sonicforge-live-dj-vanta', 'Intergalactic DJs presents DJ VANTA', 'Virtual Autonomous Nocturnal Transmission Artist', 'closed_until_human_yes', 'PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify.py', 'PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_survival_harm_reduction.py', 'uvicorn server.main:app --host 127.0.0.1 --port 8788', '/api/next-segment', '/api/backends', 'COMFYUI_ENABLE_PROMPT=false', 'RUNPOD_ENABLE_POD_START=false', 'TTS_ENABLE_AUDIO_OUTPUT=false', 'Do not read, print, or commit `/opt/data/.env` values', 'No medical diagnosis or treatment', 'no recursive cron changes']:
    if c not in hermes_skill_doc:
        print('Hermes skill package doc missing operator/safety string', c); sys.exit(1)

hackathon_submission_doc = (ROOT/'docs/product/HACKATHON_SUBMISSION_CHECKLIST.md').read_text()
for c in ['Hackathon Submission Checklist', 'local draft / human-submit only', 'Intergalactic DJs presents DJ VANTA', 'Virtual Autonomous Nocturnal Transmission Artist', 'closed_until_human_yes', 'starts_gpu: false', 'starts_paid_api: false', 'publishes_stream: false', 'records_audio: false', 'uploads_private_media: false', 'requires_human_approval: true', 'POST /api/next-segment', 'Deck A / Deck B', 'gainA = cos((value + 1) / 2 * PI / 2)', 'survival_kit', 'culture_cue', 'comfyui_visual_spell', 'prompt_id: null', 'files: []', '/api/backends', 'PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify.py', 'PYTHONDONTWRITEBYTECODE=1 python3 scripts/smoke_local_demo.py', 'Do not proceed unless the operator answers', 'Do-not-submit list', 'not medical/legal/drug-use advice']:
    if c not in hackathon_submission_doc:
        print('Hackathon submission checklist missing safety/demo string', c); sys.exit(1)

skill_draft = (ROOT/'skills/sonicforge-live-dj-vanta/SKILL.md').read_text()
for c in ['name: sonicforge-live-dj-vanta', 'Intergalactic DJs presents DJ VANTA', 'Virtual Autonomous Nocturnal Transmission Artist', 'closed_until_human_yes', 'Do not read, print, or commit `/opt/data/.env` values', 'date -Is', 'git status --short --branch', 'Operator quickstart — local-only, no provider lanes', 'CLI proof commands for an awake operator or judge', 'curl -fsS http://127.0.0.1:8788/health', 'curl -fsS -X POST http://127.0.0.1:8788/api/sample-pad', 'Expected proof highlights', 'COMFYUI_ENABLE_PROMPT=false', 'RUNPOD_ENABLE_POD_START=false', 'ACE_STEP_ENABLE_GENERATION=false', 'RTMP_ENABLE_PUBLISH=false', 'TTS_ENABLE_AUDIO_OUTPUT=false', 'PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify.py', 'PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_survival_harm_reduction.py', 'uvicorn server.main:app --host 127.0.0.1 --port 8788', '/api/next-segment', '/api/backends', 'COMFYUI', 'RunPod / ACE-Step', 'TouchDesigner/twozero', 'Resolume Arena MCP', 'mock-text-talk-break', 'medical diagnosis or treatment', 'dosing, drug identification, ingestion instructions, or drug-use advice', 'Future Hermes agent self-test instructions', 'Runtime smoke self-test', 'Generated sidecar hygiene', 'Commit readiness self-test', 'scripts/smoke_local_demo.py', 'git diff --check', 'Final report template']:
    if c not in skill_draft:
        print('SonicForge skill draft missing operator/safety string', c); sys.exit(1)

env_example = (ROOT/'.env.example').read_text()
for c in ['SONICFORGE_ALLOW_GPU=false', 'SONICFORGE_ALLOW_PAID_API=false', 'SONICFORGE_ALLOW_PUBLIC_STREAM=false', 'SONICFORGE_REQUIRE_HUMAN_APPROVAL=true', 'COMFYUI_BASE_URL', 'COMFYUI_ENABLE_PROMPT=false', 'MODAL_SONICFORGE_ENDPOINT_URL', 'RUNPOD_ENDPOINT_URL', 'RUNPOD_ENABLE_POD_START=false', 'TOUCHDESIGNER_MCP_URL', 'RESOLUME_MCP_BASE_URL', 'RTMP_ENABLE_PUBLISH=false', 'TTS_ENABLE_AUDIO_OUTPUT=false', '[REDACTED]', 'No hidden recording', 'not medical/legal/drug-use advice']:
    if c not in env_example:
        print('env example missing closed-gate variable/string', c); sys.exit(1)
for forbidden in ['sk-', 'ghp_', 'hf_', 'xoxb-', 'BEGIN PRIVATE KEY']:
    if forbidden in env_example:
        print('env example appears to contain a secret-looking token marker', forbidden); sys.exit(1)

survival = segment['survival_kit']
culture = segment['culture_cue']
if 'SURVIVAL_PING' not in survival.get('visual_spell', ''):
    print('survival kit missing SURVIVAL_PING visual text'); sys.exit(1)
if 'not medical/legal/drug-use advice' not in survival.get('safe_scope', ''):
    print('survival kit safe-scope copy missing'); sys.exit(1)
if 'human' not in survival.get('human_override', '').lower():
    print('survival kit human override missing'); sys.exit(1)
if culture.get('lineage') != 'disco-house-techno-rave-vj-ai' or 'AI is a guest' not in culture.get('respect_note', ''):
    print('culture cue missing respectful lineage contract'); sys.exit(1)
mc_break = segment['mc_break']
if mc_break.get('mode') not in ['survival', 'history', 'hype', 'lore', 'technical']:
    print('MC break missing expected text-first mode'); sys.exit(1)
if mc_break.get('tts_status') != 'text_first_no_audio_output' or mc_break.get('adapter') != 'mock-text-talk-break':
    print('MC break does not use text-first mock adapter'); sys.exit(1)
for flag in ['starts_gpu', 'starts_paid_api', 'publishes_stream', 'records_audio', 'uploads_private_media', 'sends_voice_message', 'voice_cloning_enabled']:
    if mc_break.get(flag) is not False:
        print('MC break flag not fail-closed', flag); sys.exit(1)
if 'not medical/legal/drug-use advice' not in mc_break.get('safe_scope', ''):
    print('MC break safe-scope copy missing'); sys.exit(1)

crowd_phases = {
    plan_next_segment(SetState(mode='warmup', energy=3))['transition'].crowd.synthetic_state,
    plan_next_segment(SetState(mode='groove', energy=5))['transition'].crowd.synthetic_state,
    plan_next_segment(SetState(mode='build', energy=7))['transition'].crowd.synthetic_state,
    plan_next_segment(SetState(mode='peak', energy=9))['transition'].crowd.synthetic_state,
    plan_next_segment(SetState(mode='comedown', energy=4))['transition'].crowd.synthetic_state,
}
if crowd_phases != {'warmup', 'curious', 'locked-in', 'peak', 'cooldown'}:
    print('synthetic crowd state ladder missing expected phases', sorted(crowd_phases)); sys.exit(1)
if segment['transition'].crowd.operator_note.find('Synthetic crowd read only') == -1:
    print('crowd state missing honest synthetic/no-sensor note'); sys.exit(1)

print(json.dumps({'ok': True, 'project': 'sonicforge-live', 'files_checked': len(required), 'python_checked': True, 'dual_deck_contract_checked': True, 'comfyui_dry_run_checked': True, 'survival_culture_checked': True, 'text_first_mc_break_checked': True, 'synthetic_crowd_ladder_checked': True, 'backend_status_card_checked': True}, indent=2))
