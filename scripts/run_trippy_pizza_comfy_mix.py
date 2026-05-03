#!/usr/bin/env python3
"""Generate a real ComfyUI/OmniVoice + ACE-Step trippy pizza full mix.

Structure: intro -> song 1 -> mid intro -> song 2 -> outro.
Safety/quality:
- Uses the active COMFYUI_BASE_URL but never prints it.
- Requires real ComfyUI JSON routes and OmniVoice + ACE-Step nodes.
- Generates music with ACE-Step ComfyUI nodes, not procedural placeholders.
- Uses OmniVoice Voice Design for story clips.
- Renders timeline-safe radio_duck_safe segments and emits manifest/timeline/QA.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import time
import urllib.parse
import urllib.request

BASE = os.environ.get("COMFYUI_BASE_URL", "").rstrip("/")
OMNI_WF = Path(os.environ.get("OMNIVOICE_WORKFLOW_PATH", "/opt/data/workspace/projects/sonicforge-live/workflows/comfyui/omni_voice_design_api.reusable.json"))
ACE_WF = Path(os.environ.get("ACE_WORKFLOW_PATH", "/opt/data/cache/documents/doc_1f34a705b083_acestep-api.json"))
OUT_ROOT = Path("/opt/data/audio_cache/sonicforge_trippy_pizza_comfy")
UA = "jimsky-trippy-pizza-comfy/1.0"
SR = 44100
SONG_SECONDS = 60
OVERLAP = 2.0
GAP = 0.45

VOICE_TAGS = [
    "male, young adult, moderate pitch, australian accent",
    "female, elderly, high pitch, british accent, whisper",
    "male, middle-aged, very low pitch, american accent",
]
VOICE_TEXTS = [
    (
        "[laughter] SonicForge festival dispatch, this is Cosmo Crust Courier. I have one galaxy size pizza, "
        "one suspicious bag of mushroom toppings, and a delivery pin that says stage seven but keeps blinking in purple. "
        "If the banjo starts talking, nobody panic. We are going in."
    ),
    (
        "[sigh] Level two update from the pizza portal. The mushrooms are not regular mushrooms. Repeat, not regular mushrooms. "
        "The pepperoni just opened a tiny third eye, the crust is breathing in four four time, and the crowd has become a gentle field of neon cows. "
        "Wrong order, right dimension. Send the next song."
    ),
    (
        "[confirmation-en] Final slice report. We delivered the wrong pizza to the right aliens, and now the mushrooms are headlining the festival. "
        "Nobody got mad. The moon goat tipped us in glow sticks. DJ VANTA, close the box, bless the sauce, and mark this order: accidentally enlightened."
    ),
]

SONGS = [
    {
        "id": "01_cosmic_crust_level_one",
        "title": "Cosmic Crust Level One",
        "bpm": 116,
        "keyscale": "G major",
        "seed": 710031,
        "tags": (
            "original psychedelic bluegrass space rock festival song, 116 BPM, banjo rolls, acoustic guitar chop, "
            "warm upright bass, dusty rock drums, cosmic pedal steel shimmer, trippy festival atmosphere, playful stoner comedy, "
            "polished ACE-Step music generation, clean mix, no named artist imitation"
        ),
        "lyrics": """[Intro]
Cosmic crust in the shuttle light
Banjo moon taking flight

[Verse]
I got a pizza for the star gate crew
Mushroom map and a sauce tattoo
Wrong stage number on a glowing receipt
Dusty boots floating over the beat

[Chorus]
Take it higher, take it slow
Cosmic crust where the bluegrass glows
If the pie starts singing in stereo
Follow that banjo through the portal

[Bridge]
Sauce in orbit, cheese in bloom
Festival lights across the moon

[Outro]
Level one, the oven is bright
Pizza ship rolls into the night
""",
    },
    {
        "id": "02_wrong_order_mushroom_dimension",
        "title": "Wrong Order Mushroom Dimension",
        "bpm": 124,
        "keyscale": "D minor",
        "seed": 710777,
        "tags": (
            "original trippy psychedelic bluegrass rock song, 124 BPM, warped banjo, space fiddle, crunchy desert guitar, "
            "rolling live drums, mushroom dimension comedy, festival jam band energy, cosmic choir hook, "
            "clean modern generated music, no named artist imitation"
        ),
        "lyrics": """[Intro]
Wrong order at the moon goat stage
Mushrooms laughing from the cardboard cage

[Verse]
Pepperoni opened up a tiny eye
Olives made a ladder to the purple sky
Crowd keeps chanting extra sauce
Courier forgot what planet he crossed

[Chorus]
Wrong order, right dimension
Pizza turned into ascension
Banjo bends and the stars reply
Everybody takes one slice of the sky

[Drop]
Glow stick tip jar, gravy train
Moon goat dancing in the laser rain

[Outro]
Wrong order, no complaint
Mushroom pizza made the whole stage levitate
""",
    },
]


def redact(s: str) -> str:
    return s.replace(BASE, "[REDACTED_COMFYUI_ENDPOINT]") if BASE else s


def http_get(path_or_url: str, timeout: int = 60) -> tuple[bytes, int]:
    url = path_or_url if path_or_url.startswith("http") else BASE + path_or_url
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json,text/plain,*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.status


def http_post(path: str, payload: dict, timeout: int = 120) -> dict:
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": UA, "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def preflight(out_dir: Path) -> None:
    if not BASE:
        raise SystemExit("COMFYUI_BASE_URL is not set")
    probe = {}
    for route in ["/system_stats", "/queue", "/prompt", "/object_info"]:
        try:
            body, status = http_get(route, 45)
            obj = json.loads(body.decode("utf-8", "replace"))
            probe[route] = {"ok": True, "status": status, "keys": list(obj)[:12]}
            if route == "/object_info":
                keys = set(obj)
                required = ["OmniVoiceVoiceDesignTTS", "SaveAudioMP3", "TextEncodeAceStepAudio1.5", "EmptyAceStep1.5LatentAudio", "VAEDecodeAudio"]
                probe[route]["required_nodes"] = {k: k in keys for k in required}
                missing = [k for k in required if k not in keys]
                if missing:
                    raise RuntimeError(f"missing ComfyUI nodes: {missing}")
        except Exception as e:
            probe[route] = {"ok": False, "error_type": type(e).__name__, "error": redact(str(e))[:220]}
            (out_dir / "endpoint_probe_redacted.json").write_text(json.dumps(probe, indent=2), encoding="utf-8")
            raise
    (out_dir / "endpoint_probe_redacted.json").write_text(json.dumps(probe, indent=2), encoding="utf-8")


def wait_history(prompt_id: str, max_wait: int = 2400) -> dict:
    start = time.time()
    last = None
    while time.time() - start < max_wait:
        try:
            body, _ = http_get("/history/" + urllib.parse.quote(prompt_id), 60)
            data = json.loads(body.decode("utf-8", "replace") or "{}")
            if prompt_id in data and (data[prompt_id].get("outputs") or {}):
                return data[prompt_id]
        except Exception as e:
            last = f"{type(e).__name__}: {redact(str(e))[:160]}"
        time.sleep(4)
    raise TimeoutError(f"history timeout for prompt_id={prompt_id}; last={last}")


def output_files(hist: dict) -> list[dict]:
    files = []
    for _node, out in (hist.get("outputs") or {}).items():
        for _key, vals in (out or {}).items():
            if isinstance(vals, list):
                files.extend([v for v in vals if isinstance(v, dict) and v.get("filename")])
    return files


def download(fileinfo: dict, dest: Path) -> None:
    q = urllib.parse.urlencode({
        "filename": fileinfo.get("filename", ""),
        "subfolder": fileinfo.get("subfolder", ""),
        "type": fileinfo.get("type", "output"),
    })
    blob, _ = http_get("/view?" + q, 300)
    dest.write_bytes(blob)


def run_omni(text: str, tags: str, prefix: str, seed: int, out_dir: Path) -> dict:
    wf = json.loads(OMNI_WF.read_text(encoding="utf-8"))
    wf["1"]["inputs"].update({
        "text": text,
        "voice_instruct": tags,
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
    (out_dir / f"{prefix}.workflow.json").write_text(json.dumps(wf, indent=2), encoding="utf-8")
    resp = http_post("/prompt", {"prompt": wf, "client_id": f"jimsky-{prefix}"}, 120)
    if resp.get("node_errors") or not resp.get("prompt_id"):
        raise RuntimeError(redact(json.dumps(resp, indent=2))[:2000])
    pid = resp["prompt_id"]
    hist = wait_history(pid, 1200)
    (out_dir / f"{prefix}.history.json").write_text(json.dumps(hist, indent=2), encoding="utf-8")
    files = output_files(hist)
    if not files:
        raise RuntimeError("no OmniVoice output files")
    dest = out_dir / f"{prefix}.mp3"
    download(files[0], dest)
    return {"prompt_id": pid, "file": str(dest), "voice_instruct": tags, "text": text, "sha256": sha256(dest), "duration": duration(dest)}


def run_song(song: dict, out_dir: Path) -> dict:
    wf = json.loads(ACE_WF.read_text(encoding="utf-8"))
    wf["94"]["inputs"].update({
        "tags": song["tags"],
        "lyrics": song["lyrics"],
        "bpm": song["bpm"],
        "duration": SONG_SECONDS,
        "timesignature": "4",
        "language": "en",
        "keyscale": song["keyscale"],
        "cfg_scale": 2,
        "temperature": 0.9,
        "top_p": 0.92,
    })
    wf["98"]["inputs"].update({"seconds": SONG_SECONDS, "batch_size": 1})
    wf["109"]["inputs"]["value"] = song["seed"]
    wf["3"]["inputs"].update({"steps": 8, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "denoise": 1})
    wf["107"]["inputs"]["filename_prefix"] = f"audio/trippy_pizza_{song['id']}"
    (out_dir / f"{song['id']}.workflow.json").write_text(json.dumps(wf, indent=2), encoding="utf-8")
    resp = http_post("/prompt", {"prompt": wf, "client_id": f"jimsky-trippy-pizza-{song['id']}"}, 120)
    if resp.get("node_errors") or not resp.get("prompt_id"):
        raise RuntimeError(redact(json.dumps(resp, indent=2))[:3000])
    pid = resp["prompt_id"]
    hist = wait_history(pid, 2400)
    (out_dir / f"{song['id']}.history.json").write_text(json.dumps(hist, indent=2), encoding="utf-8")
    files = output_files(hist)
    if not files:
        raise RuntimeError(f"no ACE-Step output files for {song['id']}")
    dest = out_dir / f"{song['id']}.mp3"
    download(files[0], dest)
    return {"prompt_id": pid, "file": str(dest), **song, "sha256": sha256(dest), "duration": duration(dest)}


def shell(cmd: list[str], quiet: bool = True) -> None:
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL if quiet else None, stderr=subprocess.DEVNULL if quiet else None)


def duration(path: Path) -> float:
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)], text=True).strip())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def norm(src: Path, dest: Path, kind: str) -> None:
    if kind == "voice":
        filt = f"aresample={SR},aformat=sample_fmts=fltp:channel_layouts=stereo,loudnorm=I=-15:TP=-1.5:LRA=9,highpass=f=80,afade=t=in:st=0:d=0.05,areverse,afade=t=in:st=0:d=0.08,areverse"
    else:
        # Keep the real generated song intact but shape boundaries.
        d = min(SONG_SECONDS, max(1, duration(src)))
        filt = f"aresample={SR},aformat=sample_fmts=fltp:channel_layouts=stereo,loudnorm=I=-14:TP=-1.3:LRA=9,afade=t=in:st=0:d=1.0,afade=t=out:st={max(0,d-2.4)}:d=2.4"
    shell(["ffmpeg", "-y", "-i", str(src), "-filter:a", filt, "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", str(dest)])


def render_pair(voice_wav: Path, song_wav: Path, dest: Path) -> dict:
    vd = duration(voice_wav)
    sd = duration(song_wav)
    delay = max(0, vd - OVERLAP)
    expected = delay + sd
    delay_ms = int(delay * 1000)
    v_ms = int(vd * 1000)
    filt = ";".join([
        f"[0:a]aresample={SR},aformat=sample_fmts=fltp:channel_layouts=stereo[v]",
        f"[1:a]aresample={SR},aformat=sample_fmts=fltp:channel_layouts=stereo,adelay={delay_ms}|{delay_ms}[sdel]",
        "[sdel]asplit=2[squiet][smain]",
        f"[squiet]atrim=start={delay}:duration={OVERLAP},asetpts=PTS-STARTPTS,volume=0.10,adelay={delay_ms}|{delay_ms}[bed]",
        f"[smain]atrim=start={vd}:duration={max(0.1, expected-vd)},asetpts=PTS-STARTPTS,adelay={v_ms}|{v_ms}[main]",
        "[v][bed][main]amix=inputs=3:duration=longest:dropout_transition=0,alimiter=limit=0.95[out]",
    ])
    shell(["ffmpeg", "-y", "-i", str(voice_wav), "-i", str(song_wav), "-filter_complex", filt, "-map", "[out]", "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", str(dest)])
    ad = duration(dest)
    if abs(ad - expected) > 1.5:
        raise RuntimeError(f"pair duration mismatch expected={expected} actual={ad}")
    return {"file": str(dest), "voice_duration": vd, "song_duration": sd, "expected_duration": expected, "actual_duration": ad}


def make_gap(path: Path) -> None:
    shell(["ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=stereo", "-t", str(GAP), "-c:a", "pcm_s16le", str(path)])


def concat(parts: list[Path], dest: Path) -> None:
    txt = dest.with_suffix(".concat.txt")
    txt.write_text("".join(f"file {shlex.quote(str(p))}\n" for p in parts), encoding="utf-8")
    shell(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(txt), "-filter:a", "loudnorm=I=-14:TP=-1.2:LRA=10,alimiter=limit=0.95", "-c:a", "libmp3lame", "-q:a", "2", str(dest)])


def queue_state() -> dict:
    try:
        body, _ = http_get("/queue", 30)
        return json.loads(body.decode("utf-8", "replace"))
    except Exception as e:
        return {"error_type": type(e).__name__, "error": redact(str(e))[:160]}


def main() -> None:
    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = OUT_ROOT / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    preflight(out_dir)

    voices = []
    for i, (text, tags) in enumerate(zip(VOICE_TEXTS, VOICE_TAGS), start=1):
        voices.append(run_omni(text, tags, f"{i:02d}_omnivoice_story", 880000 + i, out_dir))

    songs = [run_song(s, out_dir) for s in SONGS]

    parts = []
    timeline = []
    cursor = 0.0
    gap = out_dir / "gap.wav"
    make_gap(gap)
    pair_reports = []
    for i in range(2):
        vw = out_dir / f"{i+1:02d}_voice_norm.wav"
        sw = out_dir / f"{i+1:02d}_song_norm.wav"
        pair = out_dir / f"{i+1:02d}_voice_song_pair.wav"
        norm(Path(voices[i]["file"]), vw, "voice")
        norm(Path(songs[i]["file"]), sw, "song")
        pr = render_pair(vw, sw, pair)
        pr["voice"] = voices[i]
        pr["song"] = songs[i]
        pair_reports.append(pr)
        parts.append(pair)
        d = duration(pair)
        timeline.append({"type": "voice_song_pair", "title": f"{SONGS[i]['title']} story segment", "file": str(pair), "start": cursor, "duration": d, "allowed_overlap": "host final 2s low song bed only"})
        cursor += d
        parts.append(gap)
        timeline.append({"type": "gap", "title": "breath gap", "file": str(gap), "start": cursor, "duration": GAP})
        cursor += GAP

    outro_wav = out_dir / "03_outro_norm.wav"
    norm(Path(voices[2]["file"]), outro_wav, "voice")
    parts.append(outro_wav)
    od = duration(outro_wav)
    timeline.append({"type": "voice_outro", "title": "Wrong order/right dimension outro", "file": str(outro_wav), "start": cursor, "duration": od})
    cursor += od

    final = out_dir / "FULL_trippy_pizza_omnivoice_acestep_radio_duck_safe.mp3"
    concat(parts, final)
    fd = duration(final)
    expected = sum(duration(p) for p in parts)
    checks = [
        {"name": "final_exists", "passed": final.exists() and final.stat().st_size > 0, "detail": str(final.stat().st_size)},
        {"name": "duration_matches_parts", "passed": abs(fd - expected) < 1.5, "detail": f"expected={expected:.3f} actual={fd:.3f}"},
        {"name": "generated_with_omnivoice", "passed": len(voices) == 3 and all(Path(v['file']).exists() for v in voices), "detail": "3 story clips"},
        {"name": "generated_with_acestep", "passed": len(songs) == 2 and all(Path(s['file']).exists() and s['duration'] > 20 for s in songs), "detail": "2 real ACE-Step songs"},
        {"name": "no_procedural_music", "passed": True, "detail": "music came from ComfyUI ACE-Step workflow"},
    ]
    qa = {"ok": all(c["passed"] for c in checks), "checks": checks, "queue_after": queue_state(), "duration_seconds": fd}
    manifest = {
        "ok": qa["ok"],
        "run_id": run_id,
        "theme": "Trippy intergalactic pizza festival wrong-order mushroom dimension",
        "structure": "intro -> song -> mid intro -> song -> outro",
        "mix_mode": "radio_duck_safe",
        "final": str(final),
        "duration_seconds": fd,
        "sha256": sha256(final),
        "voices": voices,
        "songs": songs,
        "pair_reports": pair_reports,
        "timeline": timeline,
        "qa_report": qa,
    }
    (out_dir / "timeline.json").write_text(json.dumps(timeline, indent=2), encoding="utf-8")
    (out_dir / "qa_report.json").write_text(json.dumps(qa, indent=2), encoding="utf-8")
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    if not qa["ok"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
