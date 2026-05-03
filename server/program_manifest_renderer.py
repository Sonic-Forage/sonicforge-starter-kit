from __future__ import annotations

from typing import Any


def _first_eq_move(transition: dict[str, Any]) -> dict[str, Any]:
    moves = transition.get('eq_moves') or []
    return moves[0] if moves else {}


def _crossfader_label(mix: dict[str, Any], transition: dict[str, Any]) -> str:
    curve = mix.get('crossfader_curve') or transition.get('crossfader') or {}
    formula = curve.get('formula') or 'gainA = cos((value + 1) / 2 * PI / 2); gainB = sin((value + 1) / 2 * PI / 2)'
    status = curve.get('status') or 'metadata_only_no_continuous_mixer_started'
    return f"equal_power · {formula} · {status}"


def render_program_manifest(set_title: str, manifest: dict[str, Any] | None = None) -> dict[str, Any]:
    """Render a compact program-manifest view from the local set manifest.

    This is metadata-only: it converts segment manifest rows into an operator-usable
    crossfade/ducking/LUFS run sheet. It does not stitch audio, render a program
    mix, record, upload, publish, call providers, or start GPU/cloud lanes.
    """
    manifest = manifest or {}
    segments = manifest.get('segments') or []
    rendered_segments: list[dict[str, Any]] = []
    total_track_seconds = 0.0
    total_crossfade_seconds = 0.0

    for index, segment in enumerate(segments, start=1):
        track = segment.get('track') or {}
        talk = segment.get('talk') or {}
        visual = segment.get('visual') or {}
        mix = segment.get('mix') or {}
        transition = segment.get('transition') or {}
        survival = segment.get('survival_kit') or {}
        culture = segment.get('culture_cue') or {}
        duration = float(track.get('duration_seconds') or 0)
        crossfade = float(mix.get('crossfade_seconds') or 0)
        total_track_seconds += duration
        total_crossfade_seconds += crossfade
        eq_move = _first_eq_move(transition)
        rendered_segments.append({
            'index': index,
            'segment_id': segment.get('segment_id') or f'seg-{index:03d}',
            'track_file': track.get('file'),
            'track_adapter': track.get('adapter') or 'mock_music_adapter',
            'duration_seconds': duration,
            'crossfade_seconds': crossfade,
            'talk_over_intro_seconds': mix.get('talk_over_intro_seconds'),
            'duck_music_db': mix.get('duck_music_db') if mix.get('duck_music_db') is not None else talk.get('duck_music_db'),
            'target_lufs': mix.get('target_lufs'),
            'crossfader': _crossfader_label(mix, transition),
            'eq_move_schedule': {
                'bar': eq_move.get('bar'),
                'low_db': eq_move.get('low_db'),
                'mid_db': eq_move.get('mid_db'),
                'high_db': eq_move.get('high_db'),
                'filter': eq_move.get('filter'),
                'note': eq_move.get('note') or 'metadata-only EQ move; no continuous mixer started',
            },
            'talk_text': talk.get('text'),
            'visual_output_url': visual.get('output_url'),
            'visual_spell_text': (segment.get('visual_spell') or {}).get('text'),
            'survival_ping': survival.get('visual_spell') or survival.get('message'),
            'culture_cue': culture.get('lineage') or culture.get('message'),
            'honest_status': 'program_manifest_renderer_metadata_only_no_audio_render',
        })

    estimated_program_seconds = max(0.0, total_track_seconds - total_crossfade_seconds)
    default_target_lufs = next((row.get('target_lufs') for row in rendered_segments if row.get('target_lufs') is not None), -14)
    return {
        'ok': True,
        'status': 'local_program_manifest_renderer_metadata_only',
        'set_title': set_title,
        'source_manifest_path': manifest.get('manifest_path'),
        'segment_count': len(rendered_segments),
        'estimated_program_seconds': round(estimated_program_seconds, 2),
        'total_track_seconds': round(total_track_seconds, 2),
        'total_crossfade_seconds': round(total_crossfade_seconds, 2),
        'target_lufs': default_target_lufs,
        'segments': rendered_segments,
        'operator_copy': 'Program manifest renderer: crossfade/ducking/LUFS metadata only; no WAV stitcher, continuous mixer, recording, upload, stream, provider, or GPU starts.',
        'next_safe_step': 'After human approval, a local WAV stitcher can consume this run sheet and verify a rendered program mix before any recording/stream claim.',
        'starts_gpu': False,
        'starts_paid_api': False,
        'publishes_stream': False,
        'records_audio': False,
        'uploads_private_media': False,
        'renders_program_audio': False,
        'requires_human_approval': True,
    }
