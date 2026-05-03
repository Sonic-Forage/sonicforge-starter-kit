from __future__ import annotations

from typing import Any


def build_program_status(state: Any, manifest: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return an honest audio-program readiness snapshot.

    This is a read-only status contract for the control UI. It distinguishes
    local mock WAV sketches from future generated audio and from a verified
    continuous rendered program. It does not inspect secrets, start providers,
    render audio, record, upload, or publish streams.
    """
    manifest = manifest or {}
    segment_count = int(manifest.get('segment_count') or len(manifest.get('segments', []) or []))
    latest_segment = (manifest.get('segments') or [{}])[-1] if manifest.get('segments') else {}
    track = latest_segment.get('track') or {}
    mix = latest_segment.get('mix') or {}
    deck_b = getattr(state, 'deck_b', None)
    deck_b_status = getattr(deck_b, 'status', 'idle')
    deck_b_artifact = getattr(deck_b, 'artifact_path', None)

    return {
        'ok': True,
        'status': 'honest_program_status_mock_audio_no_rendered_program',
        'summary': 'Mock audio sketches and mix metadata may exist; no verified continuous program render, recording, upload, public stream, or paid/provider generation is running.',
        'lanes': {
            'mock_audio_sketch': {
                'state': 'available_after_local_mock_generation' if segment_count or deck_b_artifact else 'pending_first_mock_segment',
                'artifact_path': deck_b_artifact or track.get('file'),
                'adapter': track.get('adapter') or 'mock_music_adapter',
                'claim': 'short local WAV sketch only; not a finished mixed program',
            },
            'real_generated_audio': {
                'state': 'closed_until_human_approval',
                'adapters': ['RunPod ACE-Step contract', 'Modal/serverless music endpoint contract'],
                'claim': 'future opt-in provider lane; no pod/GPU/API call starts by default',
            },
            'rendered_program_mix': {
                'state': 'not_rendered',
                'artifact_path': None,
                'claim': 'no continuous stitched/crossfaded program audio renderer has been verified yet',
            },
            'recording_and_stream': {
                'state': 'closed_until_human_approval',
                'claim': 'RECORD/sample-pad is intent metadata only; no recording, upload, or RTMP publish starts',
            },
        },
        'mix_metadata': {
            'manifest_path': manifest.get('manifest_path'),
            'segment_count': segment_count,
            'deck_b_status': deck_b_status,
            'latest_track_file': deck_b_artifact or track.get('file'),
            'crossfade_seconds': mix.get('crossfade_seconds'),
            'talk_over_intro_seconds': mix.get('talk_over_intro_seconds'),
            'duck_music_db': mix.get('duck_music_db'),
            'target_lufs': mix.get('target_lufs'),
            'crossfader_curve': mix.get('crossfader_curve'),
            'honest_status': mix.get('status') or 'metadata_only_no_continuous_mixer_started',
        },
        'operator_copy': 'Demo-safe status: mock audio vs real generated audio vs rendered program are separate lanes. Do not claim a continuous mix until a renderer creates and verifies one.',
        'starts_gpu': False,
        'starts_paid_api': False,
        'publishes_stream': False,
        'records_audio': False,
        'uploads_private_media': False,
    }
