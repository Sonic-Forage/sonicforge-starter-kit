from __future__ import annotations

import json
import os
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
_DEFAULT_WORKSPACE = ROOT.parents[1] if len(ROOT.parents) > 1 else ROOT.parent
WORKSPACE = Path(os.environ['SONICFORGE_WORKSPACE_ROOT']) if os.environ.get('SONICFORGE_WORKSPACE_ROOT') else _DEFAULT_WORKSPACE
SONIC_DATASET_STATUS = Path(os.environ['SONICFORGE_DATASET_STATUS_PATH']) if os.environ.get('SONICFORGE_DATASET_STATUS_PATH') else ROOT / 'data' / 'datasets' / 'dj_vanta_full_dataset_status.json'
FUNK_REPO = Path(os.environ['SONICFORGE_FUNK_REPO_PATH']) if os.environ.get('SONICFORGE_FUNK_REPO_PATH') else WORKSPACE / 'projects' / 'dj-vanta-funk-glitch-bass-album-dataset'
FUNK_RUN = Path(os.environ['SONICFORGE_FUNK_RUN_PATH']) if os.environ.get('SONICFORGE_FUNK_RUN_PATH') else FUNK_REPO / 'generated' / '20260502T185849Z'


def _read_json(path: Path, fallback=None):
    if fallback is None:
        fallback = {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return fallback


def _read_jsonl(path: Path):
    rows = []
    try:
        for line in path.read_text().splitlines():
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    except Exception:
        return []
    return rows


def _first_file(path: Path, pattern: str):
    try:
        return next(path.glob(pattern))
    except StopIteration:
        return None


def _load_funk_track_prompt(track_no: int) -> dict:
    tracks_root = FUNK_RUN / 'tracks'
    tdir = _first_file(tracks_root, f'{track_no:02d}_*') if tracks_root.exists() else None
    if not tdir:
        return {}
    settings_path = _first_file(tdir, '*.settings.json')
    lyrics_path = _first_file(tdir, '*.lyrics.txt')
    settings = _read_json(settings_path, {}) if settings_path else {}
    lyrics = lyrics_path.read_text().strip() if lyrics_path and lyrics_path.exists() else ''
    return {
        'track_number': track_no,
        'title': settings.get('title') or tdir.name,
        'audio_prompt': settings.get('tags', ''),
        'lyrics': lyrics,
        'bpm': settings.get('bpm') or settings.get('target_bpm'),
        'key_scale': settings.get('keyscale') or settings.get('key'),
        'time_signature': settings.get('timesignature') or settings.get('time_signature') or 4,
        'duration_sec': settings.get('duration') or settings.get('duration_seconds') or settings.get('duration_target_seconds') or 120,
        'language': settings.get('language', 'en'),
        'seed': settings.get('seed', 42),
        'lora_scale': settings.get('lora_scale', 1.0),
        'lyrics_sha256': settings.get('lyrics_sha256'),
    }


def _funk_dataset_card() -> dict:
    manifest = _read_json(FUNK_REPO / 'metadata' / 'album_manifest.json', {})
    rows = _read_jsonl(FUNK_RUN / 'metadata.jsonl')
    tracks = []
    for row in rows:
        tracks.append({
            'track_number': row.get('track_number'),
            'title': row.get('title'),
            'duration_seconds': row.get('duration_seconds'),
            'status': row.get('status'),
            'sha256': row.get('sha256'),
        })
    return {
        'id': 'funk-glitch-bass-drama-engine',
        'title': manifest.get('title', 'DJ VANTA — Funk Glitch Bass Drama Engine'),
        'run_id': '20260502T185849Z',
        'status': 'generated_private_uploaded_pending_review',
        'track_count': len(rows) or manifest.get('track_count', 22),
        'duration_each_seconds': 120.024 if rows else manifest.get('duration_target_seconds', 120),
        'unique_lyrics_verified': True,
        'private_hf_full': 'https://huggingface.co/datasets/TheMindExpansionNetwork/dj-vanta-funk-glitch-bass-drama-engine-synthetic-audio',
        'private_hf_audio_only': 'https://huggingface.co/datasets/TheMindExpansionNetwork/dj-vanta-funk-glitch-bass-drama-engine-audio-only',
        'local_complete_package': str(FUNK_RUN / 'organized' / 'complete-album-package'),
        'local_audio_only': str(FUNK_RUN / 'organized' / 'audio-only'),
        'cover_asset': '/static/assets/dj-vanta-gpt-image-2-hero.png',
        'tracks': tracks,
        'training_started': False,
        'human_listening_review': 'pending',
    }


def _classic_dataset_card() -> dict:
    status = _read_json(SONIC_DATASET_STATUS, {})
    return {
        'id': 'no-velvet-rope-node-graph',
        'title': 'DJ VANTA — No Velvet Rope in the Node Graph',
        'run_id': status.get('run_id'),
        'status': status.get('status', 'unknown'),
        'track_count': status.get('track_count', 18),
        'duration_each_seconds': status.get('duration_seconds_each', 120.024),
        'private_hf_full': status.get('hf_url'),
        'private_hf_audio_only': 'https://huggingface.co/datasets/TheMindExpansionNetwork/dj-vanta-no-velvet-rope-audio-only',
        'local_audio_mb': status.get('local_audio_mb'),
        'hf_file_count': status.get('hf_file_count'),
        'training_started': status.get('training_started', False),
        'human_listening_review': status.get('human_listening_review', 'pending'),
    }


def build_launch_status() -> dict:
    """Read-only launch cockpit payload.

    This intentionally reads local manifests only. It does not call Hugging Face,
    ComfyUI, RunPod, Modal, TTS, OBS, or training APIs.
    """
    prompt_1 = _load_funk_track_prompt(1)
    prompt_2 = _load_funk_track_prompt(22)
    gates = [
        ('GPU Compute', 'SONICFORGE_ALLOW_GPU'),
        ('Paid API / Provider Calls', 'SONICFORGE_ALLOW_PAID_API'),
        ('ComfyUI /prompt', 'SONICFORGE_ALLOW_COMFY_PROMPT'),
        ('RunPod / ACE-Step Generation', 'RUNPOD_ENABLE_ENDPOINT_CALL'),
        ('Model Downloads', 'SONICFORGE_ALLOW_MODEL_DOWNLOADS'),
        ('Recording', 'SONICFORGE_ALLOW_RECORDING'),
        ('Public Stream / RTMP', 'SONICFORGE_ALLOW_PUBLIC_STREAM'),
        ('Dataset Uploads', 'SONICFORGE_ALLOW_UPLOADS'),
        ('Training Start', 'HUMAN_APPROVAL_REQUIRED'),
    ]
    return {
        'ok': True,
        'status': 'sonicforge_launch_cockpit_read_only_fail_closed',
        'ts': datetime.now(timezone.utc).isoformat(),
        'product': 'SonicForge Live',
        'show': 'Intergalactic DJs',
        'performer': 'DJ VANTA',
        'tagline': 'Forkable AI DJ/VJ command cockpit for datasets, prompts, visuals, and human-approved backend lanes.',
        'datasets': [_funk_dataset_card(), _classic_dataset_card()],
        'sample_prompts': [p for p in [prompt_1, prompt_2] if p],
        'training': {
            'started': False,
            'status': 'not_started_requires_human_approval',
            'recommended_test_count': 2,
            'trigger_token_instruction': 'Paste your private trigger/style token into the audio prompt field before testing; do not commit it to repo docs.',
            'test_format': 'Audio Prompt + Lyrics + BPM + Key Scale + Time Signature + Duration + Language + Seed + LoRA Scale',
        },
        'launch_links': {
            'control_deck': '/',
            'station_signal': '/station',
            'vj_window': '/visualizer',
            'workflows': '/workflows',
            'agents': '/agents',
            'setup': '/setup',
            'backend_status_api': '/api/backends',
            'safety_policy_api': '/api/safety-policy',
        },
        'safety_gates': [
            {'name': name, 'flag': flag, 'state': 'LOCKED', 'requires_human_approval': True}
            for name, flag in gates
        ],
        'operator_rule': 'No GPU, provider call, training job, upload, recording, or public stream starts from this page. It is a launch cockpit and prompt review surface only.',
        'starts_gpu': False,
        'starts_paid_api': False,
        'publishes_stream': False,
        'records_audio': False,
        'uploads_private_media': False,
        'trains_models': False,
        'requires_human_approval': True,
    }
