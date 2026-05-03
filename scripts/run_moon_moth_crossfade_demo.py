#!/usr/bin/env python3
"""Generate a second SonicForge ComfyUI demo with crossfaded intro/song/outro.

Uses OmniVoice Voice Design TTS for intro/outro + ACE-Step for a short song.
The final clip uses ffmpeg acrossfade so narration flows into the music and music
flows into the outro instead of hard concatenation.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = os.environ.get("COMFYUI_BASE_URL", "").rstrip("/")
OMNI_WF = Path(os.environ.get("OMNIVOICE_WORKFLOW_PATH", "/opt/data/workspace/projects/sonicforge-live/workflows/comfyui/omni_voice_design_api.reusable.json"))
ACE_WF = Path(os.environ.get("ACE_WORKFLOW_PATH", "/opt/data/cache/documents/doc_1f34a705b083_acestep-api.json"))
OUT_ROOT = Path("/opt/data/audio_cache/sonicforge_moon_moth")
UA = "jimsky-moon-moth-comfy/1.0"

CHARACTER = "Captain Nibula, the moon-moth taxi dispatcher"
VOICE_INSTRUCT = "male, middle-aged, low pitch, australian accent"

INTRO_TEXT = (
    "[confirmation-en] Moon Moth Taxi dispatch to all glitter pilots. Your chariot has landed on platform seven. "
    "Please keep your kandi inside the vehicle, tip your bass goblin, and remember: if the moon starts flirting, "
    "you are probably already on the dancefloor."
)
OUTRO_TEXT = (
    "[laughter] Captain Nibula signing off. The mothership meter is paused, the bass goblin has been fed, "
    "and every lost raver gets one free ride back to hydration. Stay weird, stay kind, stay glowing."
)

SONG_TITLE = "Moon Moth Kandi Taxi"
SONG_TAGS = (
    "funky alien disco glitch bass, 110 BPM, moonlit rave taxi theme, rubbery slap synth bass, "
    "four-on-the-floor disco drums, glitch hop percussion fills, sparkling arpeggios, playful crowd chant, "
    "warm psychedelic bass, comedic intergalactic festival energy, clean modern mix, no real artist imitation"
)
SONG_LYRICS = """[Intro]
Moon moth taxi, blinking in blue
Kandi on the dash and a nebula view

[Verse 1]
Captain Nibula taps the fare
Three glow worms bouncing in the backseat air
Bass goblin grins from the radio light
Says everybody gets home kind tonight

[Chorus]
Moon moth taxi, take us around
Wings full of glitter, wheels off the ground
Left at the laser, right at the star
PLUR in the meter, love in the car

[Verse 2]
Lost little raver with a cup of ice
Says the moon gave surprisingly good advice
We laugh, we breathe, we find the beat
Then wobble like comets down the street

[Bridge]
No one gets stranded in the cosmic foam
Every bright weirdo gets a ride back home

[Outro]
Moon moth taxi, soft landing soon
Tip the bass goblin, wave at the moon
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
        headers={"Content-Type": "application/json", "Accept": "application/json", "User-Agent": UA},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read().decode("utf-8", "replace")
            return json.loads(body)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:1200]
        hint = ""
        if "GitHub" in detail or "<!DOCTYPE html" in detail:
            hint = " The configured COMFYUI_BASE_URL is not a ComfyUI API endpoint; it returned an HTML/GitHub page. Use the active RunPod/Comfy proxy base URL."
        raise RuntimeError(f"POST {path} failed HTTP {e.code}.{hint} Response preview: {detail}") from e


def require_comfy_json_route(route: str) -> dict:
    body, _ = http_get(route, 30)
    text = body.decode("utf-8", "replace")
    try:
        return json.loads(text or "{}")
    except json.JSONDecodeError as e:
        preview = text[:300].replace("\n", " ")
        raise RuntimeError(
            f"{route} did not return JSON. This is probably not the ComfyUI API base URL. "
            f"Response preview: {preview}"
        ) from e


def wait_history(prompt_id: str, max_wait: int = 1500) -> dict:
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
        "bpm": 110,
        "duration": 48,
        "timesignature": "4",
        "language": "en",
        "keyscale": "D minor",
        "cfg_scale": 2,
        "temperature": 0.88,
        "top_p": 0.9,
    })
    wf["98"]["inputs"].update({"seconds": 48, "batch_size": 1})
    wf["109"]["inputs"]["value"] = 737373
    wf["3"]["inputs"].update({"steps": 8, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "denoise": 1})
    wf["107"]["inputs"]["filename_prefix"] = "audio/moon_moth_kandi_taxi_song"
    resp = http_post("/prompt", {"prompt": wf, "client_id": "jimsky-moon-moth-song"}, 120)
    if resp.get("node_errors"):
        raise RuntimeError(json.dumps(resp, indent=2)[:2000])
    pid = resp["prompt_id"]
    hist = wait_history(pid, 1500)
    info = extract_first_file(hist)
    dest = out_dir / "02_moon_moth_kandi_taxi_song.mp3"
    download_output(info, dest)
    return {"prompt_id": pid, "file": str(dest), "title": SONG_TITLE, "tags": SONG_TAGS, "lyrics": SONG_LYRICS}


def ffprobe(path: Path) -> dict:
    try:
        data = json.loads(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration,size", "-of", "json", str(path)
        ], text=True))
        return data.get("format", {})
    except Exception as e:
        return {"probe_error": str(e)}


def combine_crossfade(parts: list[Path], dest: Path, crossfade: float = 3.0) -> None:
    wavs = []
    for i, p in enumerate(parts):
        wav = dest.parent / f"xfade_part_{i:02d}.wav"
        subprocess.check_call([
            "ffmpeg", "-y", "-i", str(p), "-ar", "44100", "-ac", "2", "-filter:a", "loudnorm=I=-16:TP=-1.5:LRA=11", str(wav)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        wavs.append(wav)
    subprocess.check_call([
        "ffmpeg", "-y",
        "-i", str(wavs[0]), "-i", str(wavs[1]), "-i", str(wavs[2]),
        "-filter_complex",
        f"[0:a][1:a]acrossfade=d={crossfade}:c1=tri:c2=tri[a01];[a01][2:a]acrossfade=d={crossfade}:c1=tri:c2=tri,alimiter=limit=0.95[out]",
        "-map", "[out]", "-codec:a", "libmp3lame", "-q:a", "2", str(dest)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main() -> None:
    if not BASE:
        raise SystemExit("COMFYUI_BASE_URL is not set")
    # Hard preflight: /prompt and /queue must return ComfyUI JSON, not a proxy/GitHub/HTML page.
    prompt_state = require_comfy_json_route("/prompt")
    queue_state = require_comfy_json_route("/queue")
    object_info_status = None
    try:
        object_info = require_comfy_json_route("/object_info")
        object_info_status = "ok"
        for cls in ["OmniVoiceVoiceDesignTTS", "SaveAudioMP3", "TextEncodeAceStepAudio1.5", "EmptyAceStep1.5LatentAudio", "VAEDecodeAudio"]:
            if cls not in object_info:
                raise SystemExit(f"required ComfyUI node missing: {cls}")
    except Exception as e:
        # Some RunPod proxy states expose /queue and /prompt but 404 on /object_info.
        # We can still let /prompt validate the actual workflow, but now only after
        # proving /prompt and /queue are real JSON routes.
        object_info_status = f"skipped: {type(e).__name__}"
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = OUT_ROOT / ts
    out_dir.mkdir(parents=True, exist_ok=True)
    intro = run_tts(INTRO_TEXT, "01_captain_nibula_intro", 919191, out_dir)
    song = run_song(out_dir)
    outro = run_tts(OUTRO_TEXT, "03_captain_nibula_outro", 929292, out_dir)
    full = out_dir / "FULL_moon_moth_kandi_taxi_crossfaded.mp3"
    combine_crossfade([Path(intro["file"]), Path(song["file"]), Path(outro["file"])], full, 3.0)
    # verify post-run queue visibility without printing endpoint
    queue_body = json.loads(http_get("/queue", 30)[0].decode("utf-8", "replace"))
    results = {
        "ok": True,
        "character": CHARACTER,
        "song_title": SONG_TITLE,
        "crossfade_seconds": 3.0,
        "out_dir": str(out_dir),
        "intro": intro,
        "song": song,
        "outro": outro,
        "full_clip": str(full),
        "queue_empty_after": not queue_body.get("queue_running") and not queue_body.get("queue_pending"),
    }
    for p in [Path(intro["file"]), Path(song["file"]), Path(outro["file"]), full]:
        results.setdefault("probes", {})[p.name] = ffprobe(p)
        results.setdefault("sha256", {})[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    (out_dir / "MOON_MOTH_KANDI_TAXI_REPORT.json").write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
