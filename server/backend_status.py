from __future__ import annotations

import os


def _env_bool(name: str, default: str = 'false') -> bool:
    return os.getenv(name, default).strip().lower() in {'1', 'true', 'yes', 'on'}


def _lane(
    *,
    lane: str,
    label: str,
    adapter: str,
    enabled_env: str,
    url_env: str | None = None,
    purpose: str,
    first_safe_action: str,
    approval_question: str,
    blocked_actions: list[str],
    extra_routes: list[str] | None = None,
) -> dict:
    enabled = _env_bool(enabled_env)
    url_configured = bool(url_env and os.getenv(url_env, '').strip())
    state = 'operator_armed_requires_human_review' if enabled else 'closed_until_human_yes'
    return {
        'lane': lane,
        'label': label,
        'adapter': adapter,
        'state': state,
        'enabled_env': enabled_env,
        'enabled': enabled,
        'url_env': url_env,
        'url_configured': url_configured,
        'mode': 'dry_run_contract_only',
        'purpose': purpose,
        'first_safe_action': first_safe_action,
        'approval_question': approval_question,
        'blocked_without_approval': blocked_actions,
        'routes_when_enabled': extra_routes or [],
        'starts_gpu': False,
        'starts_paid_api': False,
        'publishes_stream': False,
        'records_audio': False,
        'uploads_private_media': False,
        'requires_human_approval': True,
    }


def build_backend_status() -> dict:
    """Return a read-only provider-lane status card without contacting providers.

    This intentionally does not call ComfyUI, RunPod, Modal, OBS, Resolume,
    TouchDesigner, or TTS endpoints. It is a closed-gate operator dashboard for
    the UI and judges, not a preflight that starts services or leaks secrets.
    """
    lanes = [
        _lane(
            lane='comfyui_visual_workflow',
            label='ComfyUI visual spell engine',
            adapter='ComfyUIAdapter contract',
            enabled_env='COMFYUI_ENABLE_PROMPT',
            url_env='COMFYUI_BASE_URL',
            purpose='Deck art, visual spells, QR/poster assets, and future VJ loops.',
            first_safe_action='Run read-only /system_stats and /object_info only after an awake operator approves local ComfyUI checks.',
            approval_question='Approve local ComfyUI /prompt calls for intergalactic-djs-visual-spell?',
            blocked_actions=['POST /prompt', 'model downloads', 'Comfy Cloud jobs', 'generated batch commits'],
            extra_routes=['/system_stats', '/object_info', '/prompt', '/ws?clientId=', '/history/{prompt_id}', '/view'],
        ),
        _lane(
            lane='runpod_ace_step_audio',
            label='RunPod ACE-Step music generation',
            adapter='RunPodAceStepAdapter contract',
            enabled_env='RUNPOD_ENABLE_POD_START',
            url_env='RUNPOD_ENDPOINT_URL',
            purpose='Future generated clips for Deck B after the mock planner proves the set flow.',
            first_safe_action='Review endpoint card and cost/VRAM limits; keep mock WAV sketches as default.',
            approval_question='Approve a bounded RunPod ACE-Step generation test and pod shutdown proof?',
            blocked_actions=['pod start', 'paid GPU generation', 'private media upload', 'model downloads'],
            extra_routes=['POST /release_task', 'POST /query_result', 'GET /v1/audio'],
        ),
        _lane(
            lane='modal_serverless_gpu',
            label='Modal serverless GPU lane',
            adapter='Modal endpoint contract',
            enabled_env='MODAL_ENABLE_GPU',
            url_env='MODAL_SONICFORGE_ENDPOINT_URL',
            purpose='Future bounded image/audio/video workers with scale-to-zero checks.',
            first_safe_action='Document endpoint contract and task-count limits before any GPU run.',
            approval_question='Approve one bounded Modal GPU smoke test with task count returning to zero?',
            blocked_actions=['GPU job start', 'dataset upload', 'model training', 'unbounded batch generation'],
            extra_routes=['health/readiness endpoint only until approved'],
        ),
        _lane(
            lane='touchdesigner_twozero',
            label='TouchDesigner / twozero MCP show-control',
            adapter='TouchDesigner MCP contract',
            enabled_env='TOUCHDESIGNER_ENABLE_MCP',
            url_env='TOUCHDESIGNER_MCP_URL',
            purpose='Future local VJ node graph control, Spout/Syphon routing, and projector visuals.',
            first_safe_action='Use browser /visualizer fallback; never issue unattended MCP commands.',
            approval_question='Approve local TouchDesigner MCP inspection using td_get_hints / td_get_par_info first?',
            blocked_actions=['td_execute_python', 'show windows', 'MovieFileOut recording', 'Spout/Syphon bridge start'],
            extra_routes=['td_get_hints', 'td_get_par_info', 'td_get_operator_info', 'td_get_errors'],
        ),
        _lane(
            lane='resolume_mcp',
            label='Resolume Arena cue routing',
            adapter='Resolume MCP contract',
            enabled_env='RESOLUME_ENABLE_MCP',
            url_env='RESOLUME_MCP_BASE_URL',
            purpose='Future local VJ composition/layer/clip/effect routing for visual spell packets.',
            first_safe_action='Manually copy dry-run cue packets; keep browser visualizer active.',
            approval_question='Approve local Resolume cue packet testing?',
            blocked_actions=['MCP commands', 'composition mutation', 'public show output'],
            extra_routes=['manual_operator_copy_to_resolume_or_future_mcp'],
        ),
        _lane(
            lane='obs_rtmp_streaming',
            label='OBS / RTMP livestream publishing',
            adapter='DryRunStreamAdapter',
            enabled_env='RTMP_ENABLE_PUBLISH',
            url_env='RTMP_TARGET_URL',
            purpose='Future approved livestream output after program audio and visuals are verified.',
            first_safe_action='Preview local browser windows only; do not publish.',
            approval_question='Approve a specific RTMP target, time window, stream key, and stop condition?',
            blocked_actions=['public RTMP publish', 'stream key use', 'recording', 'private upload'],
            extra_routes=['OBS browser source preview only until approved'],
        ),
        _lane(
            lane='tts_voice_output',
            label='TTS / MC voice output',
            adapter='MockTTSAdapter text-first contract',
            enabled_env='TTS_ENABLE_AUDIO_OUTPUT',
            url_env='KITTENTTS_BASE_URL',
            purpose='Future persona narration after consent and operator approval.',
            first_safe_action='Use text-first MC breaks; no audio files or voice messages.',
            approval_question='Approve local synthetic TTS output for DJ VANTA text only?',
            blocked_actions=['voice cloning', 'audio output', 'voice messages', 'recording/upload'],
            extra_routes=['mock-text-talk-break', 'text_first_no_audio_output'],
        ),
    ]
    closed = sum(1 for lane in lanes if lane['state'] == 'closed_until_human_yes')
    return {
        'ok': True,
        'status': 'backend_status_card_fail_closed_no_provider_calls',
        'operator_rule': 'Required human inputs and blocked-action lists are review-only; they do not open any external lane.',
        'summary': f'{closed}/{len(lanes)} backend lanes are closed until an awake human says yes.',
        'lanes': lanes,
        'closed_gates': ['public deploy', 'payments', 'outreach', 'dataset upload/training', 'GPU/video generation', 'private media upload', 'voice-to-shell/live provider actions'],
        'starts_gpu': False,
        'starts_paid_api': False,
        'publishes_stream': False,
        'records_audio': False,
        'uploads_private_media': False,
        'requires_human_approval': True,
    }
