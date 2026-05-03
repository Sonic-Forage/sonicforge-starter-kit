from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from server.timeline import write_demo_timeline  # noqa: E402


def main() -> None:
    timeline = write_demo_timeline()
    print(json.dumps({
        'ok': True,
        'timeline_path': timeline['timeline_path'],
        'plans': [p['id'] for p in timeline['plans']],
        'status': timeline['status'],
        'starts_gpu': timeline['starts_gpu'],
        'starts_paid_api': timeline['starts_paid_api'],
        'publishes_stream': timeline['publishes_stream'],
    }, indent=2))


if __name__ == '__main__':
    main()
