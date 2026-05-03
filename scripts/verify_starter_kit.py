#!/usr/bin/env python3
import json, re, sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
required = ['README.md','.env.example','docs/start-here/CREATE_YOUR_OWN_SONICFORGE.md','docs/setup/FORK_AND_DEPLOY_GUIDE.md','docs/safety/SAFETY_BOUNDARIES.md','docs/swarm/SWARM_NIGHT_OPERATING_MODEL.md','payloads/sonicforge-creator-template/PAYLOAD.md','payloads/sonicforge-creator-template/manifest.json','payloads/sonicforge-creator-template/config.template.yaml','payloads/sonicforge-creator-template/agents/template-agent/manifest.json','payloads/sonicforge-creator-template/workflows/registry.json','payloads/sonicforge-creator-template/models/ledger/MODEL_DOWNLOAD_PLAN.md']
errors=[]
missing=[p for p in required if not (root/p).exists()]
if missing: errors.append({'missing_required_files':missing})
json_docs={}
for rel in ['payloads/sonicforge-creator-template/manifest.json','payloads/sonicforge-creator-template/agents/template-agent/manifest.json','payloads/sonicforge-creator-template/workflows/registry.json']:
    try: json_docs[rel]=json.loads((root/rel).read_text())
    except Exception as e: errors.append({'json_error':rel,'error':str(e)})
patterns=[r'github_pat_[A-Za-z0-9_]{20,}',r'ghp_[A-Za-z0-9_]{20,}',r'hf_[A-Za-z0-9]{20,}',r'sk-[A-Za-z0-9_-]{20,}',r'xox[baprs]-[A-Za-z0-9-]{20,}',r'-----BEGIN (?:RSA |OPENSSH |EC |)PRIVATE KEY-----']
hits=[]; text_files=0
for p in root.rglob('*'):
    if not p.is_file() or any(part in {'.git','.venv','node_modules','__pycache__'} for part in p.parts): continue
    if p.suffix.lower() in {'.png','.jpg','.jpeg','.mp3','.wav','.flac','.ogg','.mp4','.mov','.zip','.gz','.tar','.safetensors','.ckpt','.pt','.pth','.bin'}: continue
    text_files += 1
    txt=p.read_text(errors='ignore')[:2000000]
    for pat in patterns:
        if re.search(pat, txt): hits.append(str(p.relative_to(root)))
if hits: errors.append({'secret_like_hits': sorted(set(hits))[:25]})
heavy=[str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and '.git' not in p.parts and p.stat().st_size > 25000000]
if heavy: errors.append({'large_files_over_25mb': heavy})
closed=(root/'.env.example').read_text()
for gate in ['ALLOW_GPU=0','ALLOW_PAID_API=0','ALLOW_PUBLIC_POSTING=0','ALLOW_TRAINING=0','ALLOW_WORKFLOW_PROMPT=0']:
    if gate not in closed: errors.append({'missing_closed_gate':gate})
payload_manifest=json_docs.get('payloads/sonicforge-creator-template/manifest.json', {})
for gate in payload_manifest.get('closed_gates', []):
    expected=f'{gate}=0'
    if expected not in closed: errors.append({'payload_gate_not_closed_in_env_example':expected})
if not payload_manifest.get('closed_gates'):
    errors.append({'payload_manifest_closed_gates':'missing_or_empty'})
if errors:
    print(json.dumps({'ok':False,'errors':errors}, indent=2)); sys.exit(1)
print(json.dumps({'ok':True,'required_files_checked':len(required),'text_files_scanned':text_files,'closed_gates_verified':True}, indent=2))
