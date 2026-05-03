from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SETS_DIR = ROOT / 'generated' / 'sets'


def _slug(value: str) -> str:
    safe = re.sub(r'[^a-zA-Z0-9]+', '-', value.strip().lower()).strip('-')
    return safe or 'sonicforge-set'


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _compact_segment(payload: dict[str, Any]) -> dict[str, Any]:
    """Keep the set manifest useful and safe without copying bulky app state."""
    track = payload.get('track', {}) or {}
    talk = payload.get('talk', {}) or {}
    visual = payload.get('visual', {}) or {}
    mix = payload.get('mix', {}) or {}
    transition = payload.get('transition', {}) or {}
    deck_b = payload.get('deck_b', {}) or {}
    return {
        'segment_id': f"seg-{int(datetime.now(timezone.utc).timestamp())}",
        'captured_at': _now(),
        'track': {
            'file': track.get('file'),
            'duration_seconds': track.get('duration_seconds'),
            'bpm': track.get('bpm'),
            'adapter': track.get('adapter'),
            'note': track.get('note'),
        },
        'talk': {
            'text': talk.get('text'),
            'seconds': talk.get('seconds'),
            'duck_music_db': talk.get('duck_music_db'),
            'adapter': talk.get('adapter'),
            'note': talk.get('note'),
        },
        'visual': {
            'output_url': visual.get('output_url'),
            'adapter': visual.get('adapter'),
            'visual': visual.get('visual'),
        },
        'mix': {
            'crossfade_seconds': mix.get('crossfade_seconds'),
            'talk_over_intro_seconds': mix.get('talk_over_intro_seconds'),
            'duck_music_db': mix.get('duck_music_db'),
            'target_lufs': mix.get('target_lufs'),
            'crossfader_curve': mix.get('crossfader_curve'),
            'status': 'manifest_metadata_only_no_continuous_program_audio_renderer_started',
        },
        'transition': {
            'summary': transition.get('summary'),
            'phrase': transition.get('phrase'),
            'eq_moves': transition.get('eq_moves'),
            'cue_points': transition.get('cue_points'),
            'crossfader': transition.get('crossfader'),
        },
        'deck_b': {
            'status': deck_b.get('status'),
            'artifact_path': deck_b.get('artifact_path'),
            'visual_spell': deck_b.get('visual_spell'),
        },
        'visual_spell': payload.get('visual_spell'),
        'comfyui_visual_spell': payload.get('comfyui_visual_spell'),
        'survival_kit': payload.get('survival_kit'),
        'culture_cue': payload.get('culture_cue'),
        'crate_selection': payload.get('crate_selection'),
    }


def append_set_manifest(set_title: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Append the latest dry-run segment to a local set manifest.

    This only writes JSON/JSONL/Markdown metadata under generated/sets. It does
    not start recording, publish streams, call providers, upload files, or render
    continuous program audio.
    """
    set_id = _slug(set_title)
    set_dir = SETS_DIR / set_id
    set_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = set_dir / 'manifest.json'
    visual_cues_path = set_dir / 'visual-cues.jsonl'
    talk_cues_path = set_dir / 'talk-cues.md'
    survival_pings_path = set_dir / 'survival-pings.md'

    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
    else:
        manifest = {
            'schema': 'sonicforge.local_set_manifest.v1',
            'set_id': set_id,
            'set_title': set_title,
            'created_at': _now(),
            'updated_at': None,
            'safety': {
                'starts_gpu': False,
                'starts_paid_api': False,
                'publishes_stream': False,
                'records_audio': False,
                'uploads_private_media': False,
                'status': 'local metadata manifest only; mock artifacts may be referenced but no live provider is armed',
            },
            'segments': [],
        }

    segment = _compact_segment(payload)
    segment['segment_id'] = f"seg-{len(manifest.get('segments', [])) + 1:03d}"
    manifest.setdefault('segments', []).append(segment)
    manifest['updated_at'] = _now()
    manifest['segment_count'] = len(manifest['segments'])
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')

    with visual_cues_path.open('a') as f:
        f.write(json.dumps({'segment_id': segment['segment_id'], 'visual_spell': segment.get('visual_spell'), 'comfyui_visual_spell': segment.get('comfyui_visual_spell'), 'visual': segment.get('visual')}, sort_keys=True) + '\n')
    with talk_cues_path.open('a') as f:
        prefix = '\n' if talk_cues_path.stat().st_size else ''
        f.write(f"{prefix}## {segment['segment_id']} — {segment['captured_at']}\n\n{segment['talk'].get('text') or '[no talk text]'}\n")
    with survival_pings_path.open('a') as f:
        survival = segment.get('survival_kit') or {}
        prefix = '\n' if survival_pings_path.stat().st_size else ''
        f.write(f"{prefix}## {segment['segment_id']} — {survival.get('mode', 'survival')}\n\n{survival.get('message', '[no survival ping]')}\n\nSafe scope: {survival.get('safe_scope', 'community-care reminder only')}\n")

    return {
        'ok': True,
        'set_id': set_id,
        'segment_count': manifest['segment_count'],
        'manifest_path': str(manifest_path.relative_to(ROOT)),
        'visual_cues_path': str(visual_cues_path.relative_to(ROOT)),
        'talk_cues_path': str(talk_cues_path.relative_to(ROOT)),
        'survival_pings_path': str(survival_pings_path.relative_to(ROOT)),
        'starts_gpu': False,
        'starts_paid_api': False,
        'publishes_stream': False,
        'records_audio': False,
        'uploads_private_media': False,
        'note': 'local set manifest writer only; no continuous mixer, recording, provider call, upload, or stream publish started',
    }


def load_set_manifest(set_title: str) -> dict[str, Any]:
    manifest_path = SETS_DIR / _slug(set_title) / 'manifest.json'
    if not manifest_path.exists():
        return {
            'ok': False,
            'set_id': _slug(set_title),
            'manifest_path': str(manifest_path.relative_to(ROOT)),
            'segment_count': 0,
            'starts_gpu': False,
            'starts_paid_api': False,
            'publishes_stream': False,
            'records_audio': False,
            'uploads_private_media': False,
            'note': 'manifest will be created after POST /api/next-segment',
        }
    data = json.loads(manifest_path.read_text())
    safety = data.get('safety', {})
    return {
        'ok': True,
        'manifest_path': str(manifest_path.relative_to(ROOT)),
        'starts_gpu': safety.get('starts_gpu', False),
        'starts_paid_api': safety.get('starts_paid_api', False),
        'publishes_stream': safety.get('publishes_stream', False),
        'records_audio': safety.get('records_audio', False),
        'uploads_private_media': safety.get('uploads_private_media', False),
        **data,
    }
