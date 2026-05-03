#!/usr/bin/env python3
"""Generate five OmniVoice Voice Design voices using an allowlisted tag algorithm.

Current purpose: hear voice-design variation quickly while the ComfyUI endpoint is
unavailable/stale. Uses official k2-fsa/OmniVoice HF Space voice-design controls,
then combines the five resulting clips into a short SonicForge roundtable.

The same VOICE_TAGS allowlist can be mapped back to ComfyUI `voice_instruct` as
comma-separated attributes once COMFYUI_BASE_URL is healthy again.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from gradio_client import Client

OUT_ROOT = Path("/opt/data/audio_cache/omnivoice_five_voice_conversation")
SPACE_ID = "k2-fsa/OmniVoice"

# ComfyUI Voice Design tag allowlist from OmniVoice/ComfyUI docs.
VOICE_TAGS = {
    "gender": {
        "male": "Male / 男",
        "female": "Female / 女",
    },
    "age": {
        "child": "Child / 儿童",
        "teenager": "Teenager / 少年",
        "young adult": "Young Adult / 青年",
        "middle-aged": "Middle-aged / 中年",
        "elderly": "Elderly / 老年",
    },
    "pitch": {
        "very low pitch": "Very Low Pitch / 极低音调",
        "low pitch": "Low Pitch / 低音调",
        "moderate pitch": "Moderate Pitch / 中音调",
        "high pitch": "High Pitch / 高音调",
        "very high pitch": "Very High Pitch / 极高音调",
    },
    "style": {
        "auto": "Auto",
        "whisper": "Whisper / 耳语",
    },
    "accent": {
        "american accent": "American Accent / 美式口音",
        "british accent": "British Accent / 英国口音",
        "australian accent": "Australian Accent / 澳大利亚口音",
    },
    "dialect": {
        "auto": "Auto",
    },
}

# Five different synthetic SonicForge host characters. No real-person cloning.
VOICE_PLANS = [
    {
        "id": "01_velvet_orbit_mc",
        "name": "Velvet Orbit MC",
        "tags": {
            "gender": "male",
            "age": "middle-aged",
            "pitch": "low pitch",
            "style": "auto",
            "accent": "american accent",
            "dialect": "auto",
        },
        "text": "Welcome to SonicForge, crew. I am Velvet Orbit MC. The starship doors are open, the bass reactor is warm, and tonight every friendly human gets a frequency badge.",
    },
    {
        "id": "02_prism_auntie",
        "name": "Prism Auntie",
        "tags": {
            "gender": "female",
            "age": "elderly",
            "pitch": "high pitch",
            "style": "whisper",
            "accent": "british accent",
            "dialect": "auto",
        },
        "text": "[sigh] Dearest little ravers, do not fear the glowing machinery. I filed the sparks alphabetically, and I gave the kick drum a cup of tea.",
    },
    {
        "id": "03_glitch_deck_cadet",
        "name": "Glitch Deck Cadet",
        "tags": {
            "gender": "male",
            "age": "young adult",
            "pitch": "moderate pitch",
            "style": "auto",
            "accent": "australian accent",
            "dialect": "auto",
        },
        "text": "Yo, Cadet on deck. I patched the wobble bus into the moon modem. If the snare starts teleporting, that means the system is perfectly unstable.",
    },
    {
        "id": "04_neon_pearl_dispatch",
        "name": "Neon Pearl Dispatch",
        "tags": {
            "gender": "female",
            "age": "young adult",
            "pitch": "very high pitch",
            "style": "auto",
            "accent": "american accent",
            "dialect": "auto",
        },
        "text": "Neon Pearl Dispatch calling all dancers. Hydration carts are passing stage left, lost aliens are stage right, and the love signal is loud and clear.",
    },
    {
        "id": "05_sub_bass_elder",
        "name": "Sub Bass Elder",
        "tags": {
            "gender": "male",
            "age": "elderly",
            "pitch": "very low pitch",
            "style": "auto",
            "accent": "british accent",
            "dialect": "auto",
        },
        "text": "[confirmation-en] I am the Sub Bass Elder. I have seen a thousand drops, and the truth remains simple: protect the floor, share the glow, and never rush the build.",
    },
]


def sanitize_tags(tags: dict) -> dict:
    """Return HF Space controls and ComfyUI voice_instruct from allowlisted tags only."""
    clean = {}
    for family, allowed in VOICE_TAGS.items():
        raw = str(tags.get(family, "auto")).strip().lower()
        if raw not in allowed:
            if "auto" in allowed:
                raw = "auto"
            else:
                raise ValueError(f"invalid {family}={tags.get(family)!r}; allowed={sorted(allowed)}")
        clean[family] = raw
    # ComfyUI voice_instruct uses comma-separated attributes; omit auto/dialect.
    voice_instruct = ", ".join(
        clean[k]
        for k in ["gender", "age", "pitch", "accent", "style"]
        if clean[k] != "auto"
    )
    space_controls = {family: VOICE_TAGS[family][value] for family, value in clean.items()}
    return {"tags": clean, "voice_instruct": voice_instruct, "space_controls": space_controls}


def ffprobe(path: Path) -> dict:
    data = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration,size", "-of", "json", str(path)
    ], text=True))
    return data.get("format", {})


def combine_with_pauses(files: list[Path], dest: Path, pause_sec: float = 0.35) -> None:
    parts = []
    silence = dest.parent / "pause.wav"
    subprocess.check_call([
        "ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo", "-t", str(pause_sec), str(silence)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for i, f in enumerate(files):
        wav = dest.parent / f"conversation_part_{i:02d}.wav"
        subprocess.check_call([
            "ffmpeg", "-y", "-i", str(f), "-ar", "44100", "-ac", "2", "-filter:a", "loudnorm=I=-16:TP=-1.5:LRA=11", str(wav)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        parts.append(wav)
        if i != len(files) - 1:
            parts.append(silence)
    concat = dest.parent / "conversation_concat.txt"
    concat.write_text("".join(f"file '{p}'\n" for p in parts))
    subprocess.check_call([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-codec:a", "libmp3lame", "-q:a", "2", str(dest)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main() -> None:
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = OUT_ROOT / ts
    out_dir.mkdir(parents=True, exist_ok=True)
    client = Client(SPACE_ID)
    results = []
    audio_files = []
    for plan in VOICE_PLANS:
        control_pack = sanitize_tags(plan["tags"])
        c = control_pack["space_controls"]
        # HF Space API: text, lang, ns, gs, dn, sp, du, pp, po, gender, age, pitch, style, accent, dialect
        audio_path, status = client.predict(
            plan["text"],
            "English",
            32,
            2.0,
            True,
            1.0,
            0.0,
            True,
            True,
            c["gender"],
            c["age"],
            c["pitch"],
            c["style"],
            c["accent"],
            c["dialect"],
            api_name="/_design_fn",
        )
        src = Path(audio_path)
        dest = out_dir / f"{plan['id']}-{plan['name'].replace(' ', '-')}{src.suffix or '.wav'}"
        shutil.copy2(src, dest)
        audio_files.append(dest)
        meta = {
            "id": plan["id"],
            "name": plan["name"],
            "text": plan["text"],
            "allowed_tags": control_pack["tags"],
            "comfyui_voice_instruct": control_pack["voice_instruct"],
            "space_controls": c,
            "audio_file": str(dest),
            "status": status,
            "probe": ffprobe(dest),
            "sha256": hashlib.sha256(dest.read_bytes()).hexdigest(),
            "source": "k2-fsa/OmniVoice HF Space voice design fallback",
        }
        (out_dir / f"{plan['id']}.review.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))
        results.append(meta)
        print(json.dumps({"ok": True, "completed": plan["id"], "audio_file": str(dest), "voice_instruct": control_pack["voice_instruct"]}, ensure_ascii=False), flush=True)
    full = out_dir / "FULL_five_omnivoice_sonicforge_roundtable.mp3"
    combine_with_pauses(audio_files, full)
    report = {
        "ok": True,
        "backend": "official k2-fsa/OmniVoice HF Space voice design fallback",
        "note": "ComfyUI endpoint is unavailable; controls are allowlisted so the same tags can map back to ComfyUI voice_instruct.",
        "tag_allowlist": VOICE_TAGS,
        "results": results,
        "conversation_file": str(full),
        "conversation_probe": ffprobe(full),
        "conversation_sha256": hashlib.sha256(full.read_bytes()).hexdigest(),
    }
    (out_dir / "OMNIVOICE_FIVE_VOICE_CONVERSATION_REPORT.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
