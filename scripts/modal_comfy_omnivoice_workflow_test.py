#!/usr/bin/env python3
"""Run the user-provided OmniVoice ComfyUI workflow inside a temporary Modal GPU job.

This is a bounded smoke test for the actual ComfyUI API workflow JSON, used when the
external RunPod/ComfyUI endpoint is stale. It starts ComfyUI only inside the Modal
container, submits the uploaded workflow through /prompt, pulls audio from /view,
writes results to a Modal volume, then exits so the GPU can scale to zero.
"""
from __future__ import annotations

import modal

APP_NAME = "jimsky-comfy-omnivoice-workflow-smoke"
WORKFLOW_LOCAL = "/opt/data/workspace/projects/sonicforge-live/workflows/comfyui/omni_voice_design_api.reusable.json"
OUTPUT_VOL = modal.Volume.from_name("outputs", create_if_missing=True)
HF_CACHE = modal.Volume.from_name("huggingface-cache", create_if_missing=True)

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git", "ffmpeg", "curl", "ca-certificates", "build-essential", "libsndfile1")
    .pip_install("requests", "websocket-client", "soundfile", "numpy")
    .run_commands(
        "cd /opt && git clone --depth 1 https://github.com/comfyanonymous/ComfyUI.git",
        "cd /opt/ComfyUI && pip install -r requirements.txt",
        "cd /opt/ComfyUI/custom_nodes && git clone --depth 1 https://github.com/Saganaki22/ComfyUI-OmniVoice-TTS.git",
        "cd /opt/ComfyUI/custom_nodes/ComfyUI-OmniVoice-TTS && python install.py",
    )
    .add_local_file(WORKFLOW_LOCAL, remote_path="/workspace/VOICE_DESIGN_OMNI_VOICE_API.json")
)

app = modal.App(APP_NAME)


@app.function(
    image=image,
    gpu="L4",
    cpu=4,
    memory=24576,
    timeout=1800,
    scaledown_window=60,
    volumes={"/outputs": OUTPUT_VOL, "/cache": HF_CACHE},
)
def run_workflow() -> dict:
    import datetime as dt
    import hashlib
    import json
    import os
    import pathlib
    import subprocess
    import sys
    import time
    import urllib.parse
    import urllib.request

    os.environ.setdefault("HF_HOME", "/cache/huggingface")
    os.environ.setdefault("HUGGINGFACE_HUB_CACHE", "/cache/huggingface/hub")
    os.environ.setdefault("TRANSFORMERS_CACHE", "/cache/huggingface/transformers")

    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = pathlib.Path("/outputs/omnivoice-comfy-workflow-smoke") / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    base = "http://127.0.0.1:8188"
    log_path = out_dir / "comfyui.log"
    log = open(log_path, "w", buffering=1)
    proc = subprocess.Popen(
        [sys.executable, "main.py", "--listen", "127.0.0.1", "--port", "8188"],
        cwd="/opt/ComfyUI",
        stdout=log,
        stderr=subprocess.STDOUT,
        text=True,
    )

    def get(path: str, timeout: int = 30):
        req = urllib.request.Request(base + path, headers={"User-Agent": "JimskyComfyOmniSmoke/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()

    def post(path: str, payload: dict, timeout: int = 120):
        req = urllib.request.Request(
            base + path,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json", "User-Agent": "JimskyComfyOmniSmoke/1.0"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())

    try:
        ready = False
        last = None
        for _ in range(180):
            if proc.poll() is not None:
                raise RuntimeError(f"ComfyUI exited early rc={proc.returncode}")
            try:
                status, body = get("/object_info", 20)
                info = json.loads(body.decode())
                if "OmniVoiceVoiceDesignTTS" in info:
                    ready = True
                    break
                last = "object_info loaded but OmniVoiceVoiceDesignTTS missing"
            except Exception as e:
                last = repr(e)[:300]
            time.sleep(2)
        if not ready:
            raise RuntimeError(f"ComfyUI not ready: {last}")

        workflow = json.loads(pathlib.Path("/workspace/VOICE_DESIGN_OMNI_VOICE_API.json").read_text())
        workflow["1"]["inputs"].update({
            "text": "Welcome aboard the velvet-rope starship. We tune the bass by moonlight, and every lost signal becomes a doorway home.",
            "voice_instruct": "male, middle-aged, low pitch, american accent",
            "seed": 10101,
            "steps": 32,
            "guidance_scale": 2,
            "speed": 1,
            "duration": 0,
            "device": "auto",
            "dtype": "auto",
            "attention": "auto",
            "keep_model_loaded": False,
        })
        workflow["2"]["inputs"]["filename_prefix"] = "audio/omnivoice_comfy_starport_mc"
        (out_dir / "submitted_workflow.json").write_text(json.dumps(workflow, indent=2))

        resp = post("/prompt", {"prompt": workflow, "client_id": "jimsky-comfy-omnivoice-smoke"}, 120)
        (out_dir / "prompt_response.json").write_text(json.dumps(resp, indent=2))
        if resp.get("node_errors"):
            raise RuntimeError("node_errors: " + json.dumps(resp.get("node_errors"))[:1000])
        pid = resp["prompt_id"]

        hist = None
        last_hist = None
        deadline = time.time() + 1200
        while time.time() < deadline:
            if proc.poll() is not None:
                raise RuntimeError(f"ComfyUI exited during run rc={proc.returncode}")
            try:
                _s, body = get("/history/" + urllib.parse.quote(pid), 60)
                data = json.loads(body.decode() or "{}")
                if pid in data and (data[pid].get("outputs") or {}):
                    hist = data[pid]
                    break
                last_hist = str(data)[:300]
            except Exception as e:
                last_hist = repr(e)[:300]
            time.sleep(3)
        if hist is None:
            raise TimeoutError(f"history timeout; last={last_hist}")
        (out_dir / "history.json").write_text(json.dumps(hist, indent=2))

        files = []
        for _node, out in (hist.get("outputs") or {}).items():
            for _key, vals in (out or {}).items():
                if isinstance(vals, list):
                    files.extend([v for v in vals if isinstance(v, dict) and v.get("filename")])
        if not files:
            raise RuntimeError("no output files in history")
        f = files[0]
        q = urllib.parse.urlencode({"filename": f.get("filename", ""), "subfolder": f.get("subfolder", ""), "type": f.get("type", "output")})
        _s, blob = get("/view?" + q, 240)
        local = out_dir / "01_starport_mc_comfy_workflow.mp3"
        local.write_bytes(blob)
        sha = hashlib.sha256(blob).hexdigest()
        report = {"ok": True, "run_id": run_id, "prompt_id": pid, "modal_output_path": str(local), "size_bytes": len(blob), "sha256": sha}
        (out_dir / "REPORT.json").write_text(json.dumps(report, indent=2))
        OUTPUT_VOL.commit()
        HF_CACHE.commit()
        return report
    except Exception as e:
        err = {"ok": False, "error_type": type(e).__name__, "error": str(e)[:2000], "run_id": run_id, "out_dir": str(out_dir)}
        (out_dir / "ERROR.json").write_text(json.dumps(err, indent=2))
        OUTPUT_VOL.commit()
        return err
    finally:
        try:
            proc.terminate()
        except Exception:
            pass
        try:
            log.close()
        except Exception:
            pass


@app.local_entrypoint()
def main():
    import json
    print(json.dumps(run_workflow.remote(), indent=2))
