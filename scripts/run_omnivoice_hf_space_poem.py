#!/usr/bin/env python3
"""Fallback OmniVoice Voice Design runner via the official k2-fsa Hugging Face Space.

This is used only when the ComfyUI OmniVoice endpoint is not reachable. It still uses
OmniVoice voice-design controls (gender/age/pitch/style/accent), not generic TTS.
"""
from __future__ import annotations

import datetime as dt
import json
import shutil
from pathlib import Path

from gradio_client import Client

OUT_ROOT = Path("/opt/data/audio_cache/omnivoice_voice_design_poem")

VOICES = [
    {
        "id": "01_starport_mc",
        "name": "Starport MC",
        "text": "Welcome aboard the velvet-rope starship. We tune the bass by moonlight, and every lost signal becomes a doorway home.",
        "controls": {
            "gender": "Male / 男",
            "age": "Middle-aged / 中年",
            "pitch": "Low Pitch / 低音调",
            "style": "Auto",
            "accent": "American Accent / 美式口音",
            "dialect": "Auto",
        },
    },
    {
        "id": "02_nebula_oracle",
        "name": "Nebula Oracle",
        "text": "I heard the quiet code beneath the kick drum. It said: build the room with kindness, then let the machines learn how to dance.",
        "controls": {
            "gender": "Female / 女",
            "age": "Elderly / 老年",
            "pitch": "High Pitch / 高音调",
            "style": "Whisper / 耳语",
            "accent": "British Accent / 英国口音",
            "dialect": "Auto",
        },
    },
    {
        "id": "03_asteroid_hype_captain",
        "name": "Asteroid Hype Captain",
        "text": "Three voices hit the mic, three portals flash alive. SonicForge is online, DJ VANTA in the wires, humans on the heart switch.",
        "controls": {
            "gender": "Male / 男",
            "age": "Young Adult / 青年",
            "pitch": "Moderate Pitch / 中音调",
            "style": "Auto",
            "accent": "Australian Accent / 澳大利亚口音",
            "dialect": "Auto",
        },
    },
]


def main() -> None:
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = OUT_ROOT / ts
    out_dir.mkdir(parents=True, exist_ok=True)
    client = Client("k2-fsa/OmniVoice")
    results = []
    for v in VOICES:
        c = v["controls"]
        # API: text, lang, ns, gs, dn, sp, du, pp, po, gender, age, pitch, style, accent, dialect
        audio_path, status = client.predict(
            v["text"],
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
        suffix = src.suffix or ".wav"
        dest = out_dir / f"{v['id']}-{v['name'].replace(' ', '-')}{suffix}"
        shutil.copy2(src, dest)
        meta = {**v, "audio_file": str(dest), "status": status, "source": "k2-fsa/OmniVoice HF Space voice design"}
        (out_dir / f"{v['id']}.review.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))
        results.append(meta)
        print(json.dumps({"ok": True, "completed": v["id"], "audio_file": str(dest), "status": status}, indent=2, ensure_ascii=False), flush=True)
    (out_dir / "OMNIVOICE_HF_SPACE_REPORT.json").write_text(json.dumps({"ok": True, "results": results}, indent=2, ensure_ascii=False))
    print(json.dumps({"ok": True, "out_dir": str(out_dir), "results": results}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
