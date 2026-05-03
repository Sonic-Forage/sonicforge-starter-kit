from __future__ import annotations
import os, requests

class ComfyUIAdapter:
    name = 'comfyui-api'
    def __init__(self, base_url: str | None = None):
        self.base_url = (base_url or os.getenv('COMFYUI_BASE_URL') or 'http://127.0.0.1:8188').rstrip('/')

    def health(self) -> dict:
        try:
            r = requests.get(f'{self.base_url}/system_stats', timeout=2)
            return {'ok': r.ok, 'base_url': self.base_url, 'status_code': r.status_code}
        except Exception as exc:
            return {'ok': False, 'base_url': self.base_url, 'error': str(exc)}

    def workflow_contract(self) -> dict:
        return {
            'input': {'workflow': 'visual-reactive-loop', 'prompt': 'string', 'seed': 'int', 'width': 1024, 'height': 576},
            'output': {'files': [], 'prompt_id': '...', 'warnings': []},
            'safety': 'Requires SONICFORGE_ALLOW_GPU/PAID_API and explicit backend approval before remote/cloud execution.'
        }
