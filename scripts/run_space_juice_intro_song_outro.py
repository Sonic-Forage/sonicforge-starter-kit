#!/usr/bin/env python3
"""Generate a funny rave intro + ACE-Step song + outro, then combine to one MP3.

Uses the active ComfyUI API endpoint with the user's OmniVoice Voice Design workflow
and ACE-Step workflow. Does not print secrets; output goes to /opt/data/audio_cache.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import urllib.parse
import urllib.request

BASE = os.environ.get("COMFYUI_BASE_URL", "").rstrip("/")
OMNI_WF = Path(os.environ.get("OMNIVOICE_WORKFLOW_PATH", "/opt/data/workspace/projects/sonicforge-live/workflows/comfyui/omni_voice_design_api.reusable.json"))
ACE_WF = Path(os.environ.get("ACE_WORKFLOW_PATH", "/opt/data/cache/documents/doc_1f34a705b083_acestep-api.json"))
OUT_ROOT = Path("/opt/data/audio_cache/sonicforge_space_juice")
UA = "jimsky-space-juice-comfy/1.0"

INTRO_TEXT = (
    "[laughter] Attention intergalactic ravers. If your buddy says he can hear the disco ball breathing, "
    "he has probably had too much space juice. Please guide him gently toward hydration station alpha. "
    "The bass is friendly. The lasers are not snacks."
)
OUTRO_TEXT = (
    "[confirmation-en] Hydrate your aliens, hug your humans, and return all borrowed glow sticks to the mothership. "
    "This has been SonicForge safety radio, broadcasting live from the wobbliest corner of the galaxy."
)
VOICE_INSTRUCT = "female, young adult, high pitch, british accent"

SONG_TAGS = (
    "funny alien rave anthem, funky glitch hop, playful festival bass, 108 BPM, rubbery synth bass, "
    "bouncy four-on-the-floor drums, squelchy acid stabs, cosmic arcade bleeps, crowd chant hook, "
    "clean modern mix, comedic rave safety announcement energy, no real artist imitation"
)
SONG_LYRICS = """[Intro]
Space juice in the cup, stars in the shoes
Gary tried to handshake with the moon

[Verse 1]
He said the sub bass knows his name
He told the fog machine it looked insane
Kandi on his wrist, grin too wide
Dancing with a traffic cone like it's his guide

[Chorus]
Too much space juice, bring the water crew
Glow stick rescue coming through
Bassline wobble, little cosmic dude
Hydrate the rave, change the mood

[Verse 2]
Lasers are not snacks, buddy take a seat
Count four kicks and breathe with the beat
PLUR patrol in a glitter vest
Everybody laughs, everybody gets rest

[Outro]
Space juice down, water bottle up
Back to the dancefloor with a safer cup
"""


def http_get(path_or_url: str, timeout: int = 60) -> tuple[bytes, int]:
    url = path_or_url if path_or_url.startswith("http") else BASE + path_or_url
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.status


def http_post(path: str, payload: dict, timeout: int = 120) -> dict:
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "User-Agent": UA},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def wait_history(prompt_id: str, max_wait: int = 1200) -> dict:
    start = time.time()
    last = None
    while time.time() - start < max_wait:
        try:
            body, _ = http_get("/history/" + urllib.parse.quote(prompt_id), 60)
            data = json.loads(body.decode("utf-8", "replace") or "{}")
            if prompt_id in data and (data[prompt_id].get("outputs") or {}):
                return data[prompt_id]
        except Exception as e:
            last = repr(e)[:250]
        time.sleep(3)
    raise TimeoutError(f"history timeout {prompt_id}; last={last}")


def extract_first_file(hist: dict) -> dict:
    for _node, out in (hist.get("outputs") or {}).items():
        for _key, vals in (out or {}).items():
            if isinstance(vals, list):
                for v in vals:
                    if isinstance(v, dict) and v.get("filename"):
                        return v
    raise RuntimeError("no output file found")


def download_output(fileinfo: dict, dest: Path) -> None:
    q = urllib.parse.urlencode({
        "filename": fileinfo.get("filename", ""),
        "subfolder": fileinfo.get("subfolder", ""),
        "type": fileinfo.get("type", "output"),
    })
    blob, _ = http_get("/view?" + q, 240)
    dest.write_bytes(blob)


def run_tts(text: str, prefix: str, seed: int, out_dir: Path) -> dict:
    wf = json.loads(OMNI_WF.read_text())
    wf["1"]["inputs"].update({
        "text": text,
        "voice_instruct": VOICE_INSTRUCT,
        "seed": seed,
        "steps": 32,
        "guidance_scale": 2,
        "speed": 1,
        "duration": 0,
        "device": "auto",
        "dtype": "auto",
        "attention": "auto",
        "keep_model_loaded": False,
    })
    wf["2"]["inputs"]["filename_prefix"] = f"audio/{prefix}"
    resp = http_post("/prompt", {"prompt": wf, "client_id": f"jimsky-{prefix}"}, 120)
    if resp.get("node_errors"):
        raise RuntimeError(json.dumps(resp, indent=2)[:1000])
    pid = resp["prompt_id"]
    hist = wait_history(pid, 900)
    info = extract_first_file(hist)
    dest = out_dir / f"{prefix}.mp3"
    download_output(info, dest)
    return {"prompt_id": pid, "file": str(dest), "voice_instruct": VOICE_INSTRUCT, "text": text}


def run_song(out_dir: Path) -> dict:
    wf = json.loads(ACE_WF.read_text())
    wf["94"]["inputs"].update({
        "tags": SONG_TAGS,
        "lyrics": SONG_LYRICS,
        "bpm": 108,
        "duration": 45,
        "timesignature": "4",
        "language": "en",
        "keyscale": "F minor",
        "cfg_scale": 2,
        "temperature": 0.85,
        "top_p": 0.9,
    })
    wf["98"]["inputs"].update({"seconds": 45, "batch_size": 1})
    wf["109"]["inputs"]["value"] = 424242
    wf["3"]["inputs"].update({"steps": 8, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "denoise": 1})
    wf["107"]["inputs"]["filename_prefix"] = "audio/space_juice_rave_rescue_song"
    resp = http_post("/prompt", {"prompt": wf, "client_id": "jimsky-space-juice-song"}, 120)
    if resp.get("node_errors"):
        raise RuntimeError(json.dumps(resp, indent=2)[:2000])
    pid = resp["prompt_id"]
    hist = wait_history(pid, 1500)
    info = extract_first_file(hist)
    dest = out_dir / "02_space_juice_rave_rescue_song.mp3"
    download_output(info, dest)
    return {"prompt_id": pid, "file": str(dest), "tags": SONG_TAGS, "lyrics": SONG_LYRICS}


def ffprobe(path: Path) -> dict:
    try:
        data = json.loads(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration,size", "-of", "json", str(path)
        ], text=True))
        return data.get("format", {})
    except Exception as e:
        return {"probe_error": str(e)}


def combine(parts: list[Path], dest: Path) -> None:
    wavs = []
    for i, p in enumerate(parts):
        wav = dest.parent / f"part_{i:02d}.wav"
        subprocess.check_call(["ffmpeg", "-y", "-i", str(p), "-ar", "44100", "-ac", "2", str(wav)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        wavs.append(wav)
    concat = dest.parent / "concat.txt"
    concat.write_text("".join(f"file '{w}'\n" for w in wavs))
    subprocess.check_call(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-codec:a", "libmp3lame", "-q:a", "2", str(dest)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main() -> None:
    if not BASE:
        raise SystemExit("COMFYUI_BASE_URL is not set")
    # preflight
    for route in ["/object_info", "/queue", "/prompt"]:
        http_get(route, 30)
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = OUT_ROOT / ts
    out_dir.mkdir(parents=True, exist_ok=True)
    intro = run_tts(INTRO_TEXT, "01_space_juice_intro", 515151, out_dir)
    song = run_song(out_dir)
    outro = run_tts(OUTRO_TEXT, "03_space_juice_outro", 616161, out_dir)
    full = out_dir / "FULL_space_juice_rave_rescue_intro_song_outro.mp3"
    combine([Path(intro["file"]), Path(song["file"]), Path(outro["file"])], full)
    results = {"ok": True, "out_dir": str(out_dir), "intro": intro, "song": song, "outro": outro, "full_clip": str(full)}
    for p in [Path(intro["file"]), Path(song["file"]), Path(outro["file"]), full]:
        results.setdefault("probes", {})[p.name] = ffprobe(p)
        results.setdefault("sha256", {})[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    (out_dir / "SPACE_JUICE_RAVE_RESCUE_REPORT.json").write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
