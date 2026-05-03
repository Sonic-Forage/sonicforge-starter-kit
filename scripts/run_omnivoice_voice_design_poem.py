#!/usr/bin/env python3
"""Run a 3-voice OmniVoice Voice Design poem through a ComfyUI API workflow.

Safety:
- Uses only allowlisted OmniVoice voice_instruct tags from ComfyUI-OmniVoice-TTS docs.
- Does not print endpoint URLs or secrets.
- Writes outputs to /opt/data/audio_cache/omnivoice_voice_design_poem/<timestamp>/.

Set COMFYUI_BASE_URL to the active ComfyUI/RunPod URL before running.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import time
import urllib.parse
import urllib.request

WORKFLOW_PATH = Path(os.environ.get(
    "OMNIVOICE_WORKFLOW_PATH",
    "/opt/data/workspace/projects/sonicforge-live/workflows/comfyui/omni_voice_design_api.reusable.json",
))
OUT_ROOT = Path("/opt/data/audio_cache/omnivoice_voice_design_poem")
BASE = os.environ.get("COMFYUI_BASE_URL", "").rstrip("/")
UA = "jimsky-omnivoice-voice-design-poem/0.2"

# Allowlisted by ComfyUI-OmniVoice-TTS README: gender, age, accent, pitch, style.
VOICES = [
    {
        "id": "01_starport_mc",
        "name": "Starport MC",
        "voice_instruct": "male, middle-aged, low pitch, american accent",
        "text": "[confirmation-en] Welcome aboard the velvet-rope starship. We tune the bass by moonlight, and every lost signal becomes a doorway home.",
        "seed": 10101,
    },
    {
        "id": "02_nebula_oracle",
        "name": "Nebula Oracle",
        "voice_instruct": "female, elderly, high pitch, british accent, whisper",
        "text": "[sigh] I heard the quiet code beneath the kick drum. It said: build the room with kindness, then let the machines learn how to dance.",
        "seed": 20202,
    },
    {
        "id": "03_asteroid_hype_captain",
        "name": "Asteroid Hype Captain",
        "voice_instruct": "male, young adult, moderate pitch, australian accent",
        "text": "[surprise-ah] Three voices hit the mic, three portals flash alive. SonicForge is online, DJ VANTA in the wires, humans on the heart switch.",
        "seed": 30303,
    },
]

ALLOWED = {
    "male", "female", "child", "young adult", "teenager", "middle-aged", "elderly",
    "american accent", "british accent", "australian accent", "canadian accent", "chinese accent",
    "indian accent", "japanese accent", "korean accent", "portuguese accent", "russian accent",
    "very low pitch", "low pitch", "moderate pitch", "high pitch", "very high pitch", "whisper",
}


def validate_voice_tags(s: str) -> None:
    tags = [x.strip() for x in s.split(",") if x.strip()]
    bad = [x for x in tags if x not in ALLOWED]
    if bad:
        raise ValueError(f"unsupported OmniVoice voice_instruct tags: {bad}")


def http_get(url: str, timeout: int = 60) -> tuple[bytes, str | None, int]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers.get("content-type"), r.status


def http_post(url: str, payload: dict, timeout: int = 120) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "User-Agent": UA},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def wait_for_history(pid: str, max_wait: int = 900) -> dict:
    start = time.time()
    last = None
    while time.time() - start < max_wait:
        try:
            body, _, _ = http_get(BASE + "/history/" + urllib.parse.quote(pid), 60)
            data = json.loads(body.decode("utf-8", "replace")) if body else {}
            if data and pid in data:
                return data[pid]
        except Exception as e:
            last = repr(e)[:200]
        time.sleep(3)
    raise TimeoutError(f"history timeout for prompt_id={pid}; last={last}")


def find_output_files(hist: dict) -> list[dict]:
    outs = []
    for _node, out in (hist.get("outputs") or {}).items():
        for _key, vals in (out or {}).items():
            if isinstance(vals, list):
                outs.extend([v for v in vals if isinstance(v, dict) and v.get("filename")])
    return outs


def main() -> None:
    if not BASE:
        raise SystemExit("COMFYUI_BASE_URL is not set")
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = OUT_ROOT / ts
    out_dir.mkdir(parents=True, exist_ok=True)
    template = json.loads(WORKFLOW_PATH.read_text())

    # health probe without printing the URL
    health = {}
    for path in ("/queue", "/prompt"):
        try:
            body, _ct, status = http_get(BASE + path, 20)
            health[path] = {"ok": True, "status": status, "preview": body.decode("utf-8", "replace")[:120]}
        except Exception as e:
            health[path] = {"ok": False, "error_type": type(e).__name__, "error": str(e)[:200]}
    (out_dir / "endpoint_probe_redacted.json").write_text(json.dumps(health, indent=2))
    if not health.get("/queue", {}).get("ok") or not health.get("/prompt", {}).get("ok"):
        print(json.dumps({"ok": False, "reason": "endpoint_not_ready", "out_dir": str(out_dir), "probe": health}, indent=2))
        return

    results = []
    for item in VOICES:
        validate_voice_tags(item["voice_instruct"])
        workflow = json.loads(json.dumps(template))
        workflow["1"]["inputs"].update({
            "text": item["text"],
            "voice_instruct": item["voice_instruct"],
            "seed": item["seed"],
            "steps": 32,
            "guidance_scale": 2,
            "speed": 1,
            "duration": 0,
            "dtype": "auto",
            "device": "auto",
            "attention": "auto",
            "keep_model_loaded": False,
        })
        workflow["2"]["inputs"]["filename_prefix"] = f"audio/omnivoice_poem_{item['id']}"
        wf_path = out_dir / f"{item['id']}.workflow.json"
        wf_path.write_text(json.dumps(workflow, indent=2))
        resp = http_post(BASE + "/prompt", {"prompt": workflow, "client_id": f"jimsky-omnivoice-{item['id']}"}, 120)
        pid = resp.get("prompt_id")
        if not pid or resp.get("node_errors"):
            raise RuntimeError(json.dumps(resp, indent=2)[:1000])
        hist = wait_for_history(pid)
        (out_dir / f"{item['id']}.history.json").write_text(json.dumps(hist, indent=2))
        files = find_output_files(hist)
        if not files:
            raise RuntimeError(f"no output files for {item['id']}")
        f = files[0]
        blob, _ctype, _status = http_get(BASE + "/view?" + urllib.parse.urlencode({
            "filename": f.get("filename", ""),
            "subfolder": f.get("subfolder", ""),
            "type": f.get("type", "output"),
        }), 240)
        safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "-", f"{item['id']}-{item['name']}.mp3")
        local = out_dir / safe_name
        local.write_bytes(blob)
        sha = hashlib.sha256(blob).hexdigest()
        meta = {**item, "prompt_id": pid, "audio_file": str(local), "sha256": sha, "size_bytes": local.stat().st_size}
        (out_dir / f"{item['id']}.review.json").write_text(json.dumps(meta, indent=2))
        results.append(meta)
        print(json.dumps({"ok": True, "completed": item["id"], "audio_file": str(local), "voice_instruct": item["voice_instruct"]}, indent=2), flush=True)
    (out_dir / "OMNIVOICE_POEM_REPORT.json").write_text(json.dumps({"ok": True, "results": results}, indent=2))
    print(json.dumps({"ok": True, "out_dir": str(out_dir), "results": results}, indent=2))


if __name__ == "__main__":
    main()
