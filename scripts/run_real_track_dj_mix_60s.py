#!/usr/bin/env python3
"""Build a cleaner DJ-style SonicForge test mix from real generated tracks.

This is intentionally different from the emergency procedural synth demo:
- Uses previously generated ACE-Step/ComfyUI MP3 album tracks as the music source.
- Uses cached reviewed OmniVoice clips as host voices when fresh OmniVoice quota/endpoint is unavailable.
- Each music bed is 60 seconds for fast review.
- Voice sits over the intro/tail while FFmpeg sidechain compression ducks the music.
- Adjacent songs are crossfaded so the output feels like a DJ/radio journey, not hard concat.

No remote GPU/API calls are made by this script.
"""
from __future__ import annotations

import hashlib
import json
import os
import shlex
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = Path(os.environ.get("SONICFORGE_AUDIO_CACHE", "/opt/data/audio_cache")) / "sonicforge_real_track_dj_mix"
VOICE_ROOT = Path("/opt/data/audio_cache/omnivoice_five_voice_conversation/20260503T001349Z")
ALBUM_AUDIO = Path("/opt/data/workspace/projects/dj-vanta-funk-glitch-bass-album-dataset/generated/20260502T185849Z/organized/audio-only")

TRACKS = [
    {
        "title": "Digital Underground Funk Bus",
        "file": ALBUM_AUDIO / "01-Digital-Underground-Funk-Bus.mp3",
        "start": 18,
        "intro_voice": VOICE_ROOT / "01_velvet_orbit_mc-Velvet-Orbit-MC.wav",
    },
    {
        "title": "Jo Brings the Wobble",
        "file": ALBUM_AUDIO / "06-Jo-Brings-the-Wobble.mp3",
        "start": 16,
        "intro_voice": VOICE_ROOT / "02_prism_auntie-Prism-Auntie.wav",
    },
    {
        "title": "Strawberry Wobble Experience",
        "file": ALBUM_AUDIO / "09-Strawberry-Wobble-Experience.mp3",
        "start": 20,
        "intro_voice": VOICE_ROOT / "03_glitch_deck_cadet-Glitch-Deck-Cadet.wav",
    },
    {
        "title": "Hermes Memory Palace Shuffle",
        "file": ALBUM_AUDIO / "21-Hermes-Memory-Palace-Shuffle.mp3",
        "start": 14,
        "intro_voice": VOICE_ROOT / "04_neon_pearl_dispatch-Neon-Pearl-Dispatch.wav",
        "outro_voice": VOICE_ROOT / "05_sub_bass_elder-Sub-Bass-Elder.wav",
        "outro_delay_ms": 48500,
    },
]

SEGMENT_SECONDS = 60
CROSSFADE_SECONDS = 4


def run(cmd: list[str]) -> None:
    print("+", " ".join(shlex.quote(c) for c in cmd))
    subprocess.run(cmd, check=True)


def ffprobe_duration(path: Path) -> float:
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path)
    ], text=True).strip()
    return float(out)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require_files() -> None:
    required = []
    for t in TRACKS:
        required += [t["file"], t["intro_voice"]]
        if t.get("outro_voice"):
            required.append(t["outro_voice"])
    missing = [str(p) for p in required if not Path(p).exists()]
    if missing:
        raise FileNotFoundError("Missing source audio:\n" + "\n".join(missing))


def make_segment(track: dict, out: Path) -> None:
    inputs = ["-i", str(track["file"]), "-i", str(track["intro_voice"])]
    voice_filters = [
        "[1:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo,"
        "loudnorm=I=-13:TP=-1.5:LRA=8,adelay=650|650[v0]"
    ]
    voice_labels = ["[v0]"]

    if track.get("outro_voice"):
        inputs += ["-i", str(track["outro_voice"])]
        delay = int(track.get("outro_delay_ms", 48500))
        voice_filters.append(
            f"[2:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo,"
            f"loudnorm=I=-13:TP=-1.5:LRA=8,adelay={delay}|{delay}[v1]"
        )
        voice_labels.append("[v1]")

    # sidechaincompress follows the sidechain duration in this FFmpeg build, so
    # always pad/trim the voice bus to the full 60-second music segment. Without
    # this, intro-only segments collapse to the 8-10 second voice clip length.
    if len(voice_labels) == 1:
        voice_filters.append(f"[v0]apad,atrim=start=0:duration={SEGMENT_SECONDS}[voicebus]")
    else:
        voice_filters.append(
            "".join(voice_labels)
            + f"amix=inputs={len(voice_labels)}:duration=longest:dropout_transition=0,"
            + f"apad,atrim=start=0:duration={SEGMENT_SECONDS}[voicebus]"
        )
    voice_bus = "[voicebus]"

    filter_complex = ";".join([
        f"[0:a]atrim=start={track['start']}:duration={SEGMENT_SECONDS},asetpts=PTS-STARTPTS,"
        "aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo,"
        "loudnorm=I=-15:TP=-1.5:LRA=8,"
        f"afade=t=in:st=0:d=2,afade=t=out:st={SEGMENT_SECONDS-3}:d=3[music]",
        *voice_filters,
        f"[music]{voice_bus}sidechaincompress=threshold=0.018:ratio=12:attack=15:release=650:makeup=1[ducked]",
        f"[ducked]{voice_bus}amix=inputs=2:duration=first:dropout_transition=0,"
        "acompressor=threshold=-16dB:ratio=2.5:attack=10:release=150,alimiter=limit=0.94[out]",
    ])

    run([
        "ffmpeg", "-y", *inputs,
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-ar", "44100", "-ac", "2",
        "-codec:a", "libmp3lame", "-q:a", "2",
        str(out),
    ])


def crossfade_segments(segments: list[Path], final: Path) -> None:
    inputs = []
    for seg in segments:
        inputs += ["-i", str(seg)]

    chains = []
    prev = "[0:a]"
    for i in range(1, len(segments)):
        label = "out" if i == len(segments) - 1 else f"xf{i}"
        chains.append(f"{prev}[{i}:a]acrossfade=d={CROSSFADE_SECONDS}:c1=tri:c2=tri[{label}]")
        prev = f"[{label}]"
    chains.append("[out]loudnorm=I=-14:TP=-1.2:LRA=9,alimiter=limit=0.95[master]")

    run([
        "ffmpeg", "-y", *inputs,
        "-filter_complex", ";".join(chains),
        "-map", "[master]",
        "-codec:a", "libmp3lame", "-q:a", "2",
        str(final),
    ])


def main() -> None:
    require_files()
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = OUT_ROOT / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    segments = []
    for i, track in enumerate(TRACKS, start=1):
        seg = out_dir / f"segment_{i:02d}_{track['title'].lower().replace(' ', '_')}.mp3"
        make_segment(track, seg)
        segments.append(seg)

    final = out_dir / "FULL_real_tracks_60s_voice_song_dj_ducked_mix.mp3"
    crossfade_segments(segments, final)

    manifest = {
        "ok": True,
        "run_id": run_id,
        "final": str(final),
        "duration_seconds": ffprobe_duration(final),
        "sha256": sha256(final),
        "method": "cached real OmniVoice voices + existing ACE-Step/ComfyUI album tracks + FFmpeg sidechain ducking/acrossfade",
        "remote_gpu_calls": False,
        "space_quota_error_workaround": "fresh OmniVoice generation skipped; cached reviewed voices reused",
        "segment_seconds": SEGMENT_SECONDS,
        "crossfade_seconds": CROSSFADE_SECONDS,
        "tracks": [{k: str(v) if isinstance(v, Path) else v for k, v in t.items()} for t in TRACKS],
        "segments": [
            {"file": str(p), "duration_seconds": ffprobe_duration(p), "sha256": sha256(p)}
            for p in segments
        ],
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
