#!/usr/bin/env python3
"""Clean non-overlapping voice/song remix.

Purpose: fix the previous "scrambled / train wreck" mix by guaranteeing only one
main program element plays at a time:
  voice bumper -> short silence -> 60s song -> short silence -> next voice -> song ...

No sidechain, no multi-song crossfade, no overlapping host beds. This is the safe
reference mix. Once this sounds correct, DJ ducking can be reintroduced carefully.
"""
from __future__ import annotations

import hashlib
import json
import os
import shlex
import subprocess
from datetime import datetime, timezone
from pathlib import Path

OUT_ROOT = Path(os.environ.get("SONICFORGE_AUDIO_CACHE", "/opt/data/audio_cache")) / "sonicforge_clean_voice_song_remix"
VOICE_ROOT = Path("/opt/data/audio_cache/omnivoice_five_voice_conversation/20260503T001349Z")
ALBUM_AUDIO = Path("/opt/data/workspace/projects/dj-vanta-funk-glitch-bass-album-dataset/generated/20260502T185849Z/organized/audio-only")

SONG_SECONDS = 60
SILENCE_SECONDS = 0.65

PROGRAM = [
    ("voice", "Velvet Orbit MC", VOICE_ROOT / "01_velvet_orbit_mc-Velvet-Orbit-MC.wav", None),
    ("song", "Digital Underground Funk Bus", ALBUM_AUDIO / "01-Digital-Underground-Funk-Bus.mp3", 18),
    ("voice", "Prism Auntie", VOICE_ROOT / "02_prism_auntie-Prism-Auntie.wav", None),
    ("song", "Jo Brings the Wobble", ALBUM_AUDIO / "06-Jo-Brings-the-Wobble.mp3", 16),
    ("voice", "Glitch Deck Cadet", VOICE_ROOT / "03_glitch_deck_cadet-Glitch-Deck-Cadet.wav", None),
    ("song", "Strawberry Wobble Experience", ALBUM_AUDIO / "09-Strawberry-Wobble-Experience.mp3", 20),
    ("voice", "Neon Pearl Dispatch", VOICE_ROOT / "04_neon_pearl_dispatch-Neon-Pearl-Dispatch.wav", None),
    ("song", "Hermes Memory Palace Shuffle", ALBUM_AUDIO / "21-Hermes-Memory-Palace-Shuffle.mp3", 14),
    ("voice", "Sub Bass Elder Outro", VOICE_ROOT / "05_sub_bass_elder-Sub-Bass-Elder.wav", None),
]


def run(cmd: list[str]) -> None:
    print("+", " ".join(shlex.quote(c) for c in cmd))
    subprocess.run(cmd, check=True)


def duration(path: Path) -> float:
    return float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path)
    ], text=True).strip())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def make_voice(src: Path, out: Path) -> None:
    run([
        "ffmpeg", "-y", "-i", str(src),
        "-filter:a",
        "aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo,"
        "loudnorm=I=-15:TP=-1.5:LRA=9,"
        "afade=t=in:st=0:d=0.05,areverse,afade=t=in:st=0:d=0.10,areverse,"
        "apad=pad_dur=0.25",
        "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le", str(out),
    ])


def make_song(src: Path, start: int, out: Path) -> None:
    # Slightly de-emphasize the vocal band so host clips feel separated from songs.
    run([
        "ffmpeg", "-y", "-ss", str(start), "-t", str(SONG_SECONDS), "-i", str(src),
        "-filter:a",
        f"aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"loudnorm=I=-14:TP=-1.4:LRA=9,"
        f"firequalizer=gain_entry='entry(120,1);entry(250,0);entry(1000,-1.5);entry(2500,-2.5);entry(6000,0)',"
        f"afade=t=in:st=0:d=1.25,afade=t=out:st={SONG_SECONDS-2.5}:d=2.5",
        "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le", str(out),
    ])


def make_silence(out: Path) -> None:
    run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo",
        "-t", str(SILENCE_SECONDS), "-c:a", "pcm_s16le", str(out),
    ])


def main() -> None:
    missing = [str(p) for _, _, p, _ in PROGRAM if not p.exists()]
    if missing:
        raise FileNotFoundError("Missing source audio:\n" + "\n".join(missing))

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = OUT_ROOT / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    parts: list[Path] = []
    report_parts = []

    silence = out_dir / "silence_650ms.wav"
    make_silence(silence)

    for idx, (kind, title, src, start) in enumerate(PROGRAM, 1):
        safe = title.lower().replace(" ", "_").replace("/", "_")
        out = out_dir / f"{idx:02d}_{kind}_{safe}.wav"
        if kind == "voice":
            make_voice(src, out)
        else:
            assert start is not None
            make_song(src, int(start), out)
        parts.append(out)
        report_parts.append({"kind": kind, "title": title, "source": str(src), "file": str(out), "duration_seconds": duration(out)})
        if idx != len(PROGRAM):
            parts.append(silence)

    concat_file = out_dir / "concat.txt"
    concat_file.write_text("".join(f"file '{p}'\n" for p in parts), encoding="utf-8")
    final = out_dir / "FULL_clean_voice_song_60s_reference_mix.mp3"
    run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-filter:a", "loudnorm=I=-14:TP=-1.2:LRA=10,alimiter=limit=0.95",
        "-c:a", "libmp3lame", "-q:a", "2", str(final),
    ])

    manifest = {
        "ok": True,
        "run_id": run_id,
        "final": str(final),
        "duration_seconds": duration(final),
        "sha256": sha256(final),
        "method": "strict non-overlap reference: voice -> silence -> 60s real song -> silence; no sidechain/crossfade overlays",
        "remote_gpu_calls": False,
        "parts": report_parts,
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
