from __future__ import annotations

import json
import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from server.main import app  # noqa: E402

REQUIRED_PAYLOAD_KEYS = [
    'track',
    'talk',
    'visual',
    'mix',
    'transition',
    'deck_a',
    'deck_b',
    'visual_spell',
    'comfyui_visual_spell',
    'crate_selection',
    'survival_kit',
    'culture_cue',
    'mc_break',
    'state',
    'set_manifest',
    'program_status',
    'program_manifest',
]

CLOSED_FLAGS = ['starts_gpu', 'starts_paid_api', 'publishes_stream']


def fail(message: str) -> None:
    raise SystemExit(f'local demo smoke failed: {message}')


def assert_false_flags(obj: dict, context: str) -> None:
    for flag in CLOSED_FLAGS:
        if obj.get(flag) is not False:
            fail(f'{context} expected {flag}=false, got {obj.get(flag)!r}')


def main() -> None:
    client = TestClient(app)

    health = client.get('/health')
    if health.status_code != 200:
        fail(f'/health status {health.status_code}')
    health_json = health.json()
    assert_false_flags(health_json, '/health')
    if health_json.get('ok') is not True:
        fail('/health ok was not true')

    for route, expected in [
        ('/', 'SonicForge Live'),
        ('/visualizer', 'dual ASCII spectrograph'),
    ]:
        resp = client.get(route)
        if resp.status_code != 200:
            fail(f'{route} status {resp.status_code}')
        if expected not in resp.text:
            fail(f'{route} missing expected string {expected!r}')

    crate = client.get('/api/crate-cache')
    if crate.status_code != 200:
        fail(f'/api/crate-cache status {crate.status_code}')
    crate_json = crate.json()
    if crate_json.get('status') != 'local_seed_only' or len(crate_json.get('entries', [])) < 5:
        fail('/api/crate-cache did not return at least five local seed entries')
    for entry in crate_json['entries']:
        assert_false_flags(entry, f'crate entry {entry.get("id")}')

    dj_brain = client.get('/api/dj-brain/state')
    if dj_brain.status_code != 200:
        fail(f'/api/dj-brain/state status {dj_brain.status_code}')
    brain_json = dj_brain.json()
    for key in ['beatmatch', 'phrase_count', 'eq_move', 'crowd_signal', 'crossfader', 'deck_a', 'deck_b', 'crate_selection', 'survival_kit', 'culture_cue', 'mc_break']:
        if key not in brain_json:
            fail(f'/api/dj-brain/state missing key {key}')
    for flag in ['starts_gpu', 'starts_paid_api', 'publishes_stream', 'records_audio', 'uploads_private_media']:
        if brain_json.get(flag) is not False:
            fail(f'/api/dj-brain/state expected {flag}=false, got {brain_json.get(flag)!r}')
    if brain_json.get('honest_status') != 'read_only_preview_no_generation_no_continuous_mixer':
        fail('/api/dj-brain/state honest_status did not stay read-only')
    if brain_json.get('deck_a', {}).get('role') != 'A' or brain_json.get('deck_b', {}).get('role') != 'B':
        fail('/api/dj-brain/state Deck A/B roles are not stable')
    if brain_json.get('crossfader', {}).get('curve') != 'equal_power':
        fail('/api/dj-brain/state missing equal_power crossfader')

    mc_preview = client.get('/api/mc-breaks/preview')
    if mc_preview.status_code != 200:
        fail(f'/api/mc-breaks/preview status {mc_preview.status_code}')
    mc_json = mc_preview.json()
    if mc_json.get('status') != 'text_first_mc_break_generator_fail_closed':
        fail('/api/mc-breaks/preview did not report fail-closed text-first status')
    for mode in ['survival', 'history', 'hype', 'lore', 'technical']:
        item = (mc_json.get('modes') or {}).get(mode) or {}
        if item.get('tts_status') != 'text_first_no_audio_output' or item.get('sends_voice_message') is not False:
            fail(f'MC break mode {mode} did not stay text-first/no-voice')
        for flag in ['starts_gpu', 'starts_paid_api', 'publishes_stream', 'records_audio', 'uploads_private_media']:
            if item.get(flag) is not False:
                fail(f'MC break mode {mode} expected {flag}=false, got {item.get(flag)!r}')

    program_status = client.get('/api/program-status')
    if program_status.status_code != 200:
        fail(f'/api/program-status status {program_status.status_code}')
    program_json = program_status.json()
    if program_json.get('status') != 'honest_program_status_mock_audio_no_rendered_program':
        fail('/api/program-status missing honest mock/no-rendered-program status')
    for flag in ['starts_gpu', 'starts_paid_api', 'publishes_stream', 'records_audio', 'uploads_private_media']:
        if program_json.get(flag) is not False:
            fail(f'/api/program-status expected {flag}=false, got {program_json.get(flag)!r}')
    for lane in ['mock_audio_sketch', 'real_generated_audio', 'rendered_program_mix', 'recording_and_stream']:
        if lane not in (program_json.get('lanes') or {}):
            fail(f'/api/program-status missing lane {lane}')
    if program_json['lanes']['rendered_program_mix'].get('state') != 'not_rendered':
        fail('/api/program-status claims a rendered program exists')

    program_manifest_pre = client.get('/api/program-manifest')
    if program_manifest_pre.status_code != 200:
        fail(f'/api/program-manifest status {program_manifest_pre.status_code}')
    program_manifest_pre_json = program_manifest_pre.json()
    if program_manifest_pre_json.get('status') != 'local_program_manifest_renderer_metadata_only':
        fail('/api/program-manifest missing metadata-only renderer status')
    for flag in ['starts_gpu', 'starts_paid_api', 'publishes_stream', 'records_audio', 'uploads_private_media']:
        if program_manifest_pre_json.get(flag) is not False:
            fail(f'/api/program-manifest expected {flag}=false, got {program_manifest_pre_json.get(flag)!r}')
    if program_manifest_pre_json.get('renders_program_audio') is not False:
        fail('/api/program-manifest implies rendered program audio')

    segment = client.post('/api/next-segment', json={})
    if segment.status_code != 200:
        fail(f'/api/next-segment status {segment.status_code}: {segment.text[:300]}')
    event = segment.json()
    payload = event.get('payload') or {}
    for key in REQUIRED_PAYLOAD_KEYS:
        if key not in payload:
            fail(f'/api/next-segment missing payload key {key}')
    if payload['deck_a'].get('role') != 'A' or payload['deck_b'].get('role') != 'B':
        fail('Deck A/B roles are not stable A/B')
    if payload['deck_b'].get('status') != 'generated_mock':
        fail('Deck B did not reach generated_mock')
    if payload['visual_spell'].get('mode') != 'dry_run':
        fail('visual_spell mode is not dry_run')
    assert_false_flags(payload['visual_spell'], 'visual_spell')
    comfy_spell = payload['comfyui_visual_spell']
    if comfy_spell.get('mode') != 'dry_run' or comfy_spell.get('workflow') != 'intergalactic-djs-visual-spell':
        fail('comfyui_visual_spell is not the expected dry-run workflow cue')
    assert_false_flags(comfy_spell, 'comfyui_visual_spell')
    if comfy_spell.get('output', {}).get('prompt_id') is not None or comfy_spell.get('output', {}).get('files') != []:
        fail('comfyui_visual_spell implies a real prompt/output instead of dry-run')
    if '/prompt' not in (comfy_spell.get('api_routes_when_enabled') or []):
        fail('comfyui_visual_spell missing /prompt route contract')
    assert_false_flags(payload['crate_selection'], 'crate_selection')
    crossfader = payload['transition'].get('crossfader') or {}
    if crossfader.get('curve') != 'equal_power' or 'cos' not in crossfader.get('formula', ''):
        fail('transition crossfader is not equal_power with formula')
    automation = crossfader.get('automation') or []
    midpoint = next((p for p in automation if abs(float(p.get('value', 999))) < 0.0001), None)
    if not midpoint or abs(float(midpoint.get('gain_a')) - 0.7071) > 0.002 or abs(float(midpoint.get('gain_b')) - 0.7071) > 0.002:
        fail('equal-power midpoint is missing or not approximately 0.7071/0.7071')
    survival = payload['survival_kit']
    mc_break = payload['mc_break']
    if mc_break.get('tts_status') != 'text_first_no_audio_output' or mc_break.get('adapter') != 'mock-text-talk-break':
        fail('planned MC break did not use text-first mock adapter')
    if mc_break.get('records_audio') is not False or mc_break.get('sends_voice_message') is not False:
        fail('planned MC break implied recording or voice message side effect')
    if 'not medical/legal/drug-use advice' not in mc_break.get('safe_scope', ''):
        fail('planned MC break safe-scope copy missing')
    if 'not medical/legal/drug-use advice' not in survival.get('safe_scope', ''):
        fail('survival kit safe-scope copy missing')
    if 'human' not in survival.get('human_override', '').lower():
        fail('survival kit human override missing')
    manifest = payload['set_manifest']
    for flag in ['starts_gpu', 'starts_paid_api', 'publishes_stream', 'records_audio', 'uploads_private_media']:
        if manifest.get(flag) is not False:
            fail(f'set manifest expected {flag}=false, got {manifest.get(flag)!r}')
    manifest_path = ROOT / manifest.get('manifest_path', '')
    if not manifest_path.exists():
        fail(f'set manifest path does not exist: {manifest_path}')
    program_payload = payload['program_status']
    if program_payload.get('status') != 'honest_program_status_mock_audio_no_rendered_program':
        fail('program_status payload missing honest mock/no-rendered-program status')
    for flag in ['starts_gpu', 'starts_paid_api', 'publishes_stream', 'records_audio', 'uploads_private_media']:
        if program_payload.get(flag) is not False:
            fail(f'program_status payload expected {flag}=false, got {program_payload.get(flag)!r}')
    if program_payload.get('lanes', {}).get('rendered_program_mix', {}).get('state') != 'not_rendered':
        fail('program_status payload claims rendered program exists')
    program_manifest_payload = payload['program_manifest']
    if program_manifest_payload.get('status') != 'local_program_manifest_renderer_metadata_only':
        fail('program_manifest payload missing metadata-only renderer status')
    if not program_manifest_payload.get('segments'):
        fail('program_manifest payload missing rendered segment rows')
    first_program_row = program_manifest_payload['segments'][0]
    for key in ['crossfade_seconds', 'duck_music_db', 'target_lufs', 'crossfader', 'eq_move_schedule']:
        if key not in first_program_row:
            fail(f'program_manifest payload missing {key}')
    if program_manifest_payload.get('renders_program_audio') is not False:
        fail('program_manifest payload implies rendered audio')
    for flag in ['starts_gpu', 'starts_paid_api', 'publishes_stream', 'records_audio', 'uploads_private_media']:
        if program_manifest_payload.get(flag) is not False:
            fail(f'program_manifest payload expected {flag}=false, got {program_manifest_payload.get(flag)!r}')

    for pad in ['VANTA', 'HYDRATE', 'BUDDY', 'DROP', 'PORTAL', 'CHILL', 'AIRHORN', 'RECORD']:
        pad_resp = client.post('/api/sample-pad', json={'pad': pad})
        if pad_resp.status_code != 200:
            fail(f'/api/sample-pad {pad} status {pad_resp.status_code}')
        pad_payload = pad_resp.json().get('payload') or {}
        assert_false_flags(pad_payload, f'sample pad {pad}')
        if pad_payload.get('audio_cue') != 'metadata_only_no_audio_playback':
            fail(f'sample pad {pad} started or implied audio playback')
        if pad == 'RECORD' and 'no recording' not in pad_payload.get('message', '').lower():
            fail('RECORD pad does not explicitly stay metadata-only')

    set_manifest = client.get('/api/set-manifest')
    if set_manifest.status_code != 200:
        fail(f'/api/set-manifest status {set_manifest.status_code}')
    set_json = set_manifest.json()
    for flag in ['starts_gpu', 'starts_paid_api', 'publishes_stream', 'records_audio', 'uploads_private_media']:
        if set_json.get(flag) is not False:
            fail(f'/api/set-manifest expected {flag}=false, got {set_json.get(flag)!r}')

    timeline_build = client.post('/api/timeline/build')
    if timeline_build.status_code != 200:
        fail(f'/api/timeline/build status {timeline_build.status_code}')
    timeline = client.get('/api/timeline')
    if timeline.status_code != 200:
        fail(f'/api/timeline status {timeline.status_code}')
    timeline_json = timeline.json()
    if timeline_json.get('status') != 'local_plan_only_fail_closed' or len(timeline_json.get('plans', [])) != 3:
        fail('/api/timeline did not return three fail-closed demo set plans')
    for flag in ['starts_gpu', 'starts_paid_api', 'publishes_stream', 'records_audio', 'uploads_private_media']:
        if timeline_json.get(flag) is not False:
            fail(f'/api/timeline expected {flag}=false, got {timeline_json.get(flag)!r}')
    expected_plan_ids = {'10_minute_private_demo', '20_minute_house_party_preview', '45_minute_full_arc_dry_run'}
    plan_ids = {p.get('id') for p in timeline_json.get('plans', [])}
    if expected_plan_ids != plan_ids:
        fail(f'/api/timeline plan ids mismatch: {plan_ids}')
    for plan in timeline_json['plans']:
        if not plan.get('segments'):
            fail(f'timeline plan {plan.get("id")} missing segments')
        first = plan['segments'][0]
        if not str(first.get('track_title', '')).endswith('Signal 01'):
            fail(f'timeline plan {plan.get("id")} did not reset to Signal 01')
        if 'with waveform gates and neon crowd ghosts with waveform gates' in first.get('visual_scene', ''):
            fail(f'timeline plan {plan.get("id")} reused mutated visual scene text')
        for row in plan['segments']:
            if row.get('honest_status') != 'timeline_plan_only_no_generation_no_continuous_mixer':
                fail(f'timeline segment {row.get("segment_id")} is not honest about planning-only status')
            if row.get('comfyui_visual_spell', {}).get('mode') != 'dry_run':
                fail(f'timeline segment {row.get("segment_id")} ComfyUI cue is not dry_run')

    print(json.dumps({
        'ok': True,
        'health': 'fail_closed',
        'static_routes': ['/', '/visualizer'],
        'segment_payload_keys': REQUIRED_PAYLOAD_KEYS,
        'sample_pads_checked': 8,
        'manifest_path': manifest.get('manifest_path'),
        'program_status': program_payload.get('status'),
        'program_manifest': program_manifest_payload.get('status'),
        'mc_break_modes_checked': ['survival', 'history', 'hype', 'lore', 'technical'],
        'timeline_plans_checked': sorted(expected_plan_ids),
    }, indent=2))


if __name__ == '__main__':
    main()
