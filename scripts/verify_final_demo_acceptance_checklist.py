from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'site/data/final-demo-acceptance-checklist.json'
DOC = ROOT / 'docs/product/FINAL_DEMO_ACCEPTANCE_CHECKLIST.md'

REQUIRED_GATES = {
    'public_deployment',
    'payment_or_revenue_claim',
    'outbound_outreach',
    'dataset_upload_or_model_training',
    'gpu_video_or_matrix_generation',
    'live_provider_activation',
    'private_media_upload',
    'voice_to_shell',
    'recursive_cron_creation',
}
REQUIRED_PAYLOAD_FIELDS = {
    'track', 'talk', 'visual', 'mix', 'transition', 'deck_a', 'deck_b',
    'visual_spell', 'survival_kit', 'culture_cue', 'state',
}
UNSAFE_AFFIRMATIVE_PATTERNS = [
    r'\bpublic deployment is live\b',
    r'\brevenue is earned\b',
    r'\bgpu .* (started|launched|running)\b',
    r'\bcomfy(ui| cloud).* (started|launched|called|running)\b',
    r'\brunpod .* (started|launched|running)\b',
    r'\bvoice[- ]to[- ]shell .* (enabled|active|running)\b',
]


def fail(message: str) -> None:
    print(f'final demo acceptance checklist verification failed: {message}')
    sys.exit(1)


def main() -> None:
    if not MANIFEST.exists():
        fail(f'missing manifest {MANIFEST.relative_to(ROOT)}')
    if not DOC.exists():
        fail(f'missing doc {DOC.relative_to(ROOT)}')

    data = json.loads(MANIFEST.read_text())
    if data.get('schema') != 'sonicforge.final_demo_acceptance_checklist.v1':
        fail('unexpected schema')
    if data.get('status') != 'draft_fail_closed':
        fail('status must stay draft_fail_closed')
    if 'closed' not in data.get('operator_rule', '').lower():
        fail('operator_rule must say lanes stay closed')

    checks = data.get('acceptance_checks', [])
    if not (5 <= len(checks) <= 7):
        fail('expected 5-7 acceptance checks')
    seen_ids = set()
    for row in checks:
        for key in ['id', 'acceptance_signal', 'proof_path', 'operator_prompt', 'fail_closed_if', 'fallback']:
            if not row.get(key):
                fail(f'acceptance row missing {key}: {row}')
        if row['id'] in seen_ids:
            fail(f'duplicate acceptance id {row["id"]}')
        seen_ids.add(row['id'])
        proof = ROOT / row['proof_path']
        if not proof.exists():
            fail(f'missing proof_path {row["proof_path"]}')

    gates = set(data.get('closed_gates', []))
    missing_gates = REQUIRED_GATES - gates
    if missing_gates:
        fail(f'missing closed gates {sorted(missing_gates)}')

    non_claim_text = '\n'.join(data.get('non_claims', []))
    for phrase in [
        'Do not claim public deployment',
        'Do not claim revenue was earned',
        'Do not claim a continuous mixed program render exists',
        'Do not claim ComfyUI, RunPod, Modal, TouchDesigner, RTMP, LiveKit, or paid providers were activated',
        'Do not claim medical, legal, dosing, or drug-use guidance',
    ]:
        if phrase not in non_claim_text:
            fail(f'missing non-claim phrase: {phrase}')

    doc_text = DOC.read_text()
    for token in ['fail-closed', 'Closed gates', 'Non-claims', 'Plan Next Continuous Segment']:
        if token not in doc_text:
            fail(f'missing doc token {token}')

    planner_text = (ROOT / 'server/planner.py').read_text()
    payload_text = planner_text + '\n' + (ROOT / 'server/main.py').read_text()
    for field in REQUIRED_PAYLOAD_FIELDS:
        if f"'{field}'" not in payload_text:
            fail(f'planner/main does not expose payload field {field}')

    health_text = (ROOT / 'server/main.py').read_text()
    for token in ['starts_gpu', 'starts_paid_api', 'publishes_stream']:
        if token not in health_text:
            fail(f'health missing {token}')

    combined = MANIFEST.read_text() + '\n' + doc_text
    for pattern in UNSAFE_AFFIRMATIVE_PATTERNS:
        if re.search(pattern, combined, re.IGNORECASE):
            fail(f'unsafe affirmative claim matched: {pattern}')

    print(json.dumps({
        'ok': True,
        'manifest': str(MANIFEST.relative_to(ROOT)),
        'doc': str(DOC.relative_to(ROOT)),
        'acceptance_checks': len(checks),
        'closed_gates': sorted(gates),
    }, indent=2))


if __name__ == '__main__':
    main()
