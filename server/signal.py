from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from typing import Any

SECRETISH = re.compile(r'(token|key|secret|password|bearer|ghp_|github_pat_|sk-|xoxb-)', re.I)


def _redact_url(url: str | None) -> str | None:
    if not url:
        return None
    if SECRETISH.search(url):
        return '[REDACTED_ENDPOINT_URL]'
    if len(url) > 120:
        return url[:80] + '…'
    return url


def _station_hash(station_signal_id: str, endpoint_kind: str, mode: str) -> str:
    raw = f'{station_signal_id}|{endpoint_kind}|{mode}'.encode()
    return hashlib.sha256(raw).hexdigest()[:12].upper()


def acquire_signal_contract(payload: dict[str, Any], flags: dict[str, bool]) -> dict[str, Any]:
    station_signal_id = str(payload.get('station_signal_id') or 'VANTA-LOCAL-128').strip()[:80]
    endpoint_kind = str(payload.get('endpoint_kind') or 'local').strip().lower()
    if endpoint_kind not in {'local', 'runpod', 'modal', 'custom'}:
        endpoint_kind = 'custom'
    mode = str(payload.get('mode') or 'intergalactic_mix').strip().lower()
    if mode not in {'single_dj', 'intergalactic_mix'}:
        mode = 'intergalactic_mix'
    try:
        set_minutes = int(payload.get('set_minutes') or 20)
    except (TypeError, ValueError):
        set_minutes = 20
    set_minutes = max(5, min(set_minutes, 180))
    allow_real_generation = bool(payload.get('allow_real_generation'))
    allow_public_stream = bool(payload.get('allow_public_stream'))
    real_generation_armed = bool(allow_real_generation and flags.get('ALLOW_GPU') and flags.get('ALLOW_PAID'))
    public_stream_armed = bool(allow_public_stream and flags.get('ALLOW_PUBLIC_STREAM'))
    signal_hash = _station_hash(station_signal_id, endpoint_kind, mode)
    warmup_steps = [
        {'step': 1, 'code': 'SIGNAL_CODE_RECEIVED', 'copy': f'Signal ID {station_signal_id} received. Opening DJ VANTA receiver.'},
        {'step': 2, 'code': 'TUNING_TO_STATION_ID', 'copy': f'Tuning station hash {signal_hash}. Acquiring… acquiring… acquiring…'},
        {'step': 3, 'code': 'VERIFYING_ENDPOINT_KIND', 'copy': f'Endpoint lane: {endpoint_kind}. No provider is called during dry-run acquisition.'},
        {'step': 4, 'code': 'CHECKING_SERVERLESS_WAKE_PATH', 'copy': 'Checking warmup path: local / RunPod / Modal endpoint contract only.'},
        {'step': 5, 'code': 'LOADING_DJ_PERSONA', 'copy': f'Loading {payload.get("dj_profile") or "DJ VANTA"}: nocturnal selector, VJ spellcaster, survival-kit buddy.'},
        {'step': 6, 'code': 'PREPARING_CREATOR_INTROS', 'copy': 'Preparing creator intro lane and intergalactic host breaks.' if mode == 'intergalactic_mix' else 'Preparing single-DJ continuous voice and set arc.'},
        {'step': 7, 'code': 'READING_CRAZY_DISCLAIMER', 'copy': 'Autonomous AI transmission. Protect ears, hydrate, watch friends, respect consent. Not medical/legal/drug-use advice.'},
        {'step': 8, 'code': 'LOCKING_HUMAN_OVERRIDE', 'copy': 'Human override locked: STOP SET / CHILL MODE remains with the sober operator.'},
        {'step': 9, 'code': 'READY_FOR_DRY_RUN', 'copy': f'{set_minutes}-minute set plan ready. Real generation armed: {real_generation_armed}.'},
    ]
    if real_generation_armed:
        warmup_steps.extend([
            {'step': 10, 'code': 'WAKING_APPROVED_WORKER', 'copy': 'Approved generation worker would wake here.'},
            {'step': 11, 'code': 'BUFFERING_FIRST_SEGMENT', 'copy': 'First real-time segment buffer would begin after endpoint health verifies.'},
        ])
    return {
        'ok': True,
        'status': 'signal_acquired_dry_run' if not real_generation_armed else 'signal_acquired_approved_contract',
        'station_signal_id': station_signal_id,
        'station_hash': signal_hash,
        'endpoint_kind': endpoint_kind,
        'endpoint_url': _redact_url(payload.get('endpoint_url')),
        'mode': mode,
        'set_minutes': set_minutes,
        'dj_profile': payload.get('dj_profile') or 'DJ VANTA',
        'voice_host': payload.get('voice_host') or 'text_first',
        'creator_intro_mode': bool(payload.get('creator_intro_mode', mode == 'intergalactic_mix')),
        'real_generation_armed': real_generation_armed,
        'public_stream_armed': public_stream_armed,
        'starts_gpu': real_generation_armed,
        'starts_paid_api': real_generation_armed,
        'publishes_stream': public_stream_armed,
        'records_audio': False,
        'serverless_note': 'Display can stay on; approved worker should wake for bounded set and scale down after outro.',
        'warmup_steps': warmup_steps,
        'disclaimer': 'DJ VANTA is an autonomous AI DJ/VJ assistant. Keep water nearby, protect hearing, watch friends, respect consent, and get human/emergency help when needed. No medical/legal/drug-use advice. Cloud providers, recording, and public streams require explicit operator approval.',
        'outro': f'Transmission complete after {set_minutes} minutes. DJ VANTA closes the station, writes the manifest, and expects serverless workers to return to zero.',
        'ts': datetime.now(timezone.utc).isoformat(),
    }


def session_plan_contract(payload: dict[str, Any], flags: dict[str, bool]) -> dict[str, Any]:
    acquired = acquire_signal_contract(payload, flags)
    minutes = acquired['set_minutes']
    segment_count = max(3, min(12, minutes // 5))
    segments = []
    for i in range(segment_count):
        is_first = i == 0
        is_last = i == segment_count - 1
        mode = 'intro' if is_first else 'outro' if is_last else 'creator_intro' if acquired['mode'] == 'intergalactic_mix' else 'continuous_mix'
        segments.append({
            'index': i + 1,
            'minute_mark': round(i * minutes / segment_count, 1),
            'mode': mode,
            'host_line': (
                'Station locked. Welcome to the VANTA transmission.' if is_first else
                'Outro orbit: hydrate, find your people, and let the signal fade clean.' if is_last else
                f'Next intergalactic creator signal entering Deck B: segment {i + 1}.' if acquired['mode'] == 'intergalactic_mix' else
                f'DJ VANTA continues the single-DJ arc into segment {i + 1}.'
            ),
            'generation_lane': 'approved_realtime_contract' if acquired['real_generation_armed'] else 'dry_run_metadata_only',
            'visual_spell': 'ACQUIRE_SIGNAL // PHRASE_LOCK // PORTAL_RING',
            'safety_ping': 'hydrate · protect ears · buddy check · human override visible',
        })
    return {
        **acquired,
        'status': 'session_plan_dry_run' if not acquired['real_generation_armed'] else 'session_plan_approved_contract',
        'segments': segments,
        'estimated_outro_at_minute': minutes,
        'scale_down_expectation': 'Modal tasks=0 / RunPod stopped or serverless idle / local worker stopped after outro unless operator keeps it on.',
    }
