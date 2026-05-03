from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from server.planner import plan_next_segment
from server.schemas import DeckState, SetState, VisualCue

ROOT = Path(__file__).resolve().parents[1]
TIMELINE_DIR = ROOT / 'generated' / 'timeline'
TIMELINE_PATH = TIMELINE_DIR / 'demo-set.json'

PLAN_LENGTH_MINUTES = {
    '10_minute_private_demo': 10,
    '20_minute_house_party_preview': 20,
    '45_minute_full_arc_dry_run': 45,
}


def _mode_for_progress(progress: float) -> str:
    if progress < 0.18:
        return 'warmup'
    if progress < 0.42:
        return 'groove'
    if progress < 0.68:
        return 'build'
    if progress < 0.84:
        return 'peak'
    return 'comedown'


def _energy_for_progress(progress: float) -> int:
    if progress < 0.18:
        return 5
    if progress < 0.42:
        return 6
    if progress < 0.68:
        return 7
    if progress < 0.84:
        return 9
    return 4


def build_demo_timeline(seed_state: SetState | None = None) -> dict:
    """Build a bounded local set timeline without generating media or providers.

    This is a planning artifact only: no audio rendering, recording, ComfyUI prompt,
    RunPod/Modal job, upload, public stream, or paid API starts here.
    """
    base_state = deepcopy(seed_state or SetState())
    # Keep the timeline deterministic even when called after a demo smoke has
    # mutated the live in-memory app state with queued mock segments.
    base_state.queue = []
    base_state.last_talk = None
    base_state.current_visual = VisualCue()
    base_state.deck_a = DeckState(role='A', name='Deck A / current groove', status='playing', gain=1.0)
    base_state.deck_b = DeckState(role='B', name='Deck B / incoming portal', status='idle', gain=0.0)
    plans = []
    for plan_id, minutes in PLAN_LENGTH_MINUTES.items():
        local_state = deepcopy(base_state)
        segment_count = max(3, minutes // 5)
        segments = []
        elapsed_seconds = 0
        for index in range(1, segment_count + 1):
            progress = (index - 1) / max(1, segment_count - 1)
            local_state.mode = _mode_for_progress(progress)
            local_state.energy = _energy_for_progress(progress)
            segment = plan_next_segment(local_state)
            transition = segment['transition'].model_dump()
            track = segment['track'].model_dump()
            talk = segment['talk'].model_dump()
            visual = segment['visual'].model_dump()
            visual_spell = segment['visual_spell']
            comfyui_visual_spell = segment['comfyui_visual_spell']
            segments.append({
                'segment_id': f'{plan_id}-segment-{index:02d}',
                'starts_at_seconds': elapsed_seconds,
                'duration_seconds': round(minutes * 60 / segment_count),
                'mode': local_state.mode,
                'energy': local_state.energy,
                'bpm': local_state.bpm,
                'track_title': track['title'],
                'track_key': track.get('key'),
                'talk_text': talk['text'],
                'visual_scene': visual['scene'],
                'visual_spell_text': visual_spell['text'],
                'crate_id': segment['crate_selection'].get('id'),
                'survival_ping': segment['survival_kit'].get('visual_spell'),
                'culture_mode': segment['culture_cue'].get('mode'),
                'transition_summary': transition['summary'],
                'beatmatch': transition['beatmatch'],
                'phrase': transition['phrase'],
                'crossfader': transition['crossfader'],
                'eq_moves': transition['eq_moves'],
                'comfyui_visual_spell': comfyui_visual_spell,
                'honest_status': 'timeline_plan_only_no_generation_no_continuous_mixer',
            })
            elapsed_seconds += round(minutes * 60 / segment_count)
            local_state.queue.append(segment['track'])
            local_state.deck_a = segment['deck_b']
            local_state.deck_a.role = 'A'
            local_state.deck_a.name = 'Deck A / current groove'
            local_state.deck_a.status = 'playing'
            local_state.deck_a.gain = 1.0
        plans.append({
            'id': plan_id,
            'minutes': minutes,
            'segment_count': segment_count,
            'segments': segments,
        })
    return {
        'schema': 'sonicforge.live.timeline.demo-set.v1',
        'title': 'DJ VANTA bounded dry-run set timeline',
        'status': 'local_plan_only_fail_closed',
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'purpose': 'Give the private demo operator 10/20/45 minute set arcs without starting providers, recording, or publishing.',
        'operator_rule': 'Review timeline as a run-of-show only; human approval is still required before live providers, GPU jobs, recording, uploads, or public streams.',
        'plans': plans,
        'closed_gates': [
            'public_deployment',
            'payment_or_revenue_claim',
            'outbound_outreach',
            'dataset_upload_or_model_training',
            'gpu_video_or_matrix_generation',
            'live_provider_activation',
            'private_media_upload',
            'voice_to_shell',
            'recursive_cron_creation',
        ],
        'starts_gpu': False,
        'starts_paid_api': False,
        'publishes_stream': False,
        'records_audio': False,
        'uploads_private_media': False,
        'timeline_path': 'generated/timeline/demo-set.json',
    }


def write_demo_timeline(seed_state: SetState | None = None) -> dict:
    TIMELINE_DIR.mkdir(parents=True, exist_ok=True)
    timeline = build_demo_timeline(seed_state)
    TIMELINE_PATH.write_text(json.dumps(timeline, indent=2) + '\n')
    return timeline


def load_demo_timeline(seed_state: SetState | None = None) -> dict:
    if not TIMELINE_PATH.exists():
        return write_demo_timeline(seed_state)
    return json.loads(TIMELINE_PATH.read_text())
