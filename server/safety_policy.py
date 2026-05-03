from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Mapping


@dataclass(frozen=True)
class BlockedAction:
    path: str
    reason: str
    approval_flag: str


BLOCKED_ACTIONS = [
    BlockedAction('/prompt', 'ComfyUI prompt execution must be explicitly approved.', 'SONICFORGE_ALLOW_COMFY_PROMPT'),
    BlockedAction('/api/comfy/prompt', 'ComfyUI prompt execution must be explicitly approved.', 'SONICFORGE_ALLOW_COMFY_PROMPT'),
    BlockedAction('/api/model-download', 'Model downloads require a reviewed ledger entry and explicit approval.', 'SONICFORGE_ALLOW_MODEL_DOWNLOADS'),
    BlockedAction('/api/models/download', 'Model downloads require a reviewed ledger entry and explicit approval.', 'SONICFORGE_ALLOW_MODEL_DOWNLOADS'),
    BlockedAction('/api/stream/publish', 'Public stream publishing requires explicit approval.', 'SONICFORGE_ALLOW_PUBLIC_STREAM'),
    BlockedAction('/api/record', 'Recording requires explicit approval.', 'SONICFORGE_ALLOW_RECORDING'),
    BlockedAction('/api/upload', 'Uploads require explicit approval.', 'SONICFORGE_ALLOW_UPLOADS'),
]


def env_flag_enabled(env: Mapping[str, str], name: str) -> bool:
    return str(env.get(name, '')).lower() in {'1', 'true', 'yes', 'y'}


def blocked_action_for(path: str, env: Mapping[str, str]) -> BlockedAction | None:
    normalized = '/' + path.lstrip('/')
    for action in BLOCKED_ACTIONS:
        if normalized == action.path or normalized.startswith(action.path + '/'):
            if not env_flag_enabled(env, action.approval_flag):
                return action
    return None


def safety_policy_snapshot(env: Mapping[str, str]) -> dict:
    return {
        'status': 'server_enforced_fail_closed_policy',
        'starts_gpu': False,
        'starts_paid_api': False,
        'publishes_stream': False,
        'records_audio': False,
        'uploads_private_media': False,
        'blocked_actions': [
            {
                'path': action.path,
                'reason': action.reason,
                'approval_flag': action.approval_flag,
                'approved': env_flag_enabled(env, action.approval_flag),
            }
            for action in BLOCKED_ACTIONS
        ],
    }
