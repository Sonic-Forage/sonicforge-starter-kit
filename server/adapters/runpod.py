from __future__ import annotations
import os, requests

class RunPodAceStepAdapter:
    name = 'runpod-ace-step-api'
    def __init__(self, api_url: str | None = None):
        self.api_url = (api_url or os.getenv('RUNPOD_ACE_STEP_API_URL') or '').rstrip('/')

    def health(self) -> dict:
        if not self.api_url:
            return {'ok': False, 'error': 'RUNPOD_ACE_STEP_API_URL is not set'}
        try:
            r = requests.get(f'{self.api_url}/health', timeout=5)
            return {'ok': r.ok, 'status_code': r.status_code, 'api_url': self.api_url}
        except Exception as exc:
            return {'ok': False, 'api_url': self.api_url, 'error': str(exc)}

    def generation_contract(self) -> dict:
        return {
            'endpoint': 'POST /release_task then POST /query_result then GET /v1/audio',
            'prompt_field': 'prompt / caption alias',
            'duration_field': 'audio_duration / duration alias',
            'hard_requirements': 'CUDA 13, 48GB+ VRAM for ACE-Step 1.5 XL',
            'safety': 'Do not start pod or generate without explicit approval; stop pod when done.'
        }
