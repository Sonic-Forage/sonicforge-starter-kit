#!/usr/bin/env python3
"""Render the Intergalactic Pizza Festival test mix.

User brief:
- intro -> 60s psychedelic bluegrass/space-rock track -> intro -> 60s track -> outro
- story: cosmic pizza delivery at an intergalactic music festival
- offline/local mixing; no GPU/API generation for music
- timeline-first radio_duck_safe layout with QA artifacts
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import shlex
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import soundfile as sf

CACHE_ROOT = Path(os.environ.get("SONICFORGE_AUDIO_CACHE", "/opt/data/audio_cache"))
OUT_ROOT = CACHE_ROOT / "sonicforge_pizza_festival"
SAMPLE_RATE = 44100
SONG_SECONDS = 60.0
INTRO_OVERLAP_SECONDS = 2.0
GAP_SECONDS = 0.55

VOICE_1 = Path("/opt/data/audio_cache/tts_20260503_010718.ogg")
VOICE_2 = Path("/opt/data/audio_cache/tts_20260503_010725.ogg")
VOICE_3 = Path("/opt/data/audio_cache/tts_20260503_010730.ogg")


@dataclass
class TimelineEvent:
    index: int
    event_type: str
    title: str
    file: str
    start_seconds: float
    duration_seconds: float
    role: str
    allowed_overlap: str = "none"


def q(x: str | Path) -> str:
    return shlex.quote(str(x))


def run(cmd: list[str]) -> None:
    print("+", " ".join(q(c) for c in cmd))
    subprocess.run(cmd, check=True)


def probe_duration(path: Path) -> float:
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


def soft_clip(x: np.ndarray) -> np.ndarray:
    return np.tanh(x * 1.4) * 0.82


def adsr(n: int, attack: float, decay: float, sustain: float, release: float, sr: int = SAMPLE_RATE) -> np.ndarray:
    a = max(1, int(attack * sr))
    d = max(1, int(decay * sr))
    r = max(1, int(release * sr))
    s = max(0, n - a - d - r)
    env = np.concatenate([
        np.linspace(0, 1, a, endpoint=False),
        np.linspace(1, sustain, d, endpoint=False),
        np.full(s, sustain),
        np.linspace(sustain, 0, r, endpoint=True),
    ])
    if len(env) < n:
        env = np.pad(env, (0, n - len(env)))
    return env[:n]


def karplus(freq: float, dur: float, decay: float = 0.985, brightness: float = 0.8) -> np.ndarray:
    n = int(dur * SAMPLE_RATE)
    period = max(2, int(SAMPLE_RATE / freq))
    rng = np.random.default_rng(int(freq * 1000 + dur * 100))
    buf = rng.uniform(-1, 1, period) * brightness
    out = np.zeros(n)
    idx = 0
    for i in range(n):
        out[i] = buf[idx]
        nxt = decay * 0.5 * (buf[idx] + buf[(idx + 1) % period])
        buf[idx] = nxt
        idx = (idx + 1) % period
    return out * adsr(n, 0.003, 0.07, 0.55, min(0.25, dur * 0.35))


def add(buf: np.ndarray, mono: np.ndarray, start_s: float, gain: float = 1.0, pan: float = 0.0) -> None:
    start = int(start_s * SAMPLE_RATE)
    end = min(buf.shape[0], start + len(mono))
    if end <= start:
        return
    m = mono[: end - start] * gain
    left = math.cos((pan + 1) * math.pi / 4)
    right = math.sin((pan + 1) * math.pi / 4)
    buf[start:end, 0] += m * left
    buf[start:end, 1] += m * right


def sine(freq: float, dur: float, gain: float = 1.0, phase: float = 0.0) -> np.ndarray:
    t = np.arange(int(dur * SAMPLE_RATE)) / SAMPLE_RATE
    return np.sin(2 * np.pi * freq * t + phase) * gain


def kick() -> np.ndarray:
    dur = 0.32
    t = np.arange(int(dur * SAMPLE_RATE)) / SAMPLE_RATE
    freq = 90 * np.exp(-t * 11) + 42
    phase = 2 * np.pi * np.cumsum(freq) / SAMPLE_RATE
    return np.sin(phase) * np.exp(-t * 10)


def snare() -> np.ndarray:
    dur = 0.22
    n = int(dur * SAMPLE_RATE)
    rng = np.random.default_rng(808)
    noise = rng.normal(0, 1, n) * np.exp(-np.arange(n) / (SAMPLE_RATE * 0.055))
    tone = sine(190, dur, 0.5) * np.exp(-np.arange(n) / (SAMPLE_RATE * 0.09))
    return (noise * 0.5 + tone) * adsr(n, 0.001, 0.03, 0.2, 0.08)


def hat() -> np.ndarray:
    dur = 0.055
    n = int(dur * SAMPLE_RATE)
    rng = np.random.default_rng(909)
    noise = rng.normal(0, 1, n)
    # crude highpass-ish differentiator
    hp = np.concatenate([[0], np.diff(noise)])
    return hp * np.exp(-np.arange(n) / (SAMPLE_RATE * 0.018)) * 0.25


def render_psy_bluegrass_track(path: Path, *, bpm: float, root: float, title: str, variant: int) -> dict:
    total = int(SONG_SECONDS * SAMPLE_RATE)
    buf = np.zeros((total, 2), dtype=np.float32)
    beat = 60.0 / bpm
    bar = beat * 4
    # Mixolydian / major-ish bluegrass palette
    scale = np.array([0, 2, 4, 5, 7, 9, 10, 12])
    chords = [0, 5, 7, 0, 10, 5, 7, 0] if variant == 1 else [0, 7, 10, 5, 0, 5, 7, 0]

    # Space pad drone, subtle and wide.
    t = np.arange(total) / SAMPLE_RATE
    pad = (np.sin(2*np.pi*root*t) + 0.5*np.sin(2*np.pi*root*1.5*t + 0.7) + 0.35*np.sin(2*np.pi*root*2*t + 1.4))
    pad *= (0.45 + 0.2*np.sin(2*np.pi*0.07*t))
    add(buf, pad, 0, gain=0.055, pan=-0.35)
    add(buf, pad, 0, gain=0.045, pan=0.45)

    # Drums.
    for b in np.arange(0, SONG_SECONDS, beat):
        beat_idx = int(round(b / beat)) % 4
        if beat_idx in (0, 2):
            add(buf, kick(), b, 0.55, 0)
        if beat_idx in (1, 3):
            add(buf, snare(), b, 0.38, 0.05)
        add(buf, hat(), b + beat * 0.5, 0.18, 0.65)

    # Upright bass / psych rock root movement.
    for i, b in enumerate(np.arange(0, SONG_SECONDS, beat)):
        chord = chords[(int(b // bar)) % len(chords)]
        freq = root * (2 ** (chord / 12)) / 2
        note = sine(freq, beat * 0.84, 0.55) * adsr(int(beat * 0.84 * SAMPLE_RATE), 0.008, 0.06, 0.5, 0.08)
        note += 0.18 * sine(freq * 2, beat * 0.84, 1.0) * adsr(len(note), 0.006, 0.04, 0.35, 0.08)
        add(buf, note, b, 0.32, -0.1)

    # Banjo rolls: alternating 8th/16th-note plucks.
    roll = [0, 4, 7, 12, 7, 4, 10, 7]
    step = beat / (2 if variant == 1 else 2.5)
    cur = 0.0
    k = 0
    while cur < SONG_SECONDS:
        chord = chords[(int(cur // bar)) % len(chords)]
        interval = roll[k % len(roll)] + chord
        freq = root * (2 ** (interval / 12)) * (2 if k % 11 == 0 else 1)
        pluck = karplus(freq, 0.34 if variant == 1 else 0.28, decay=0.977 if variant == 1 else 0.972, brightness=0.9)
        pan = -0.45 if k % 2 == 0 else 0.35
        add(buf, pluck, cur, 0.22 if cur > 3 else 0.12, pan)
        cur += step
        k += 1

    # Guitar/mandolin chop on offbeats.
    for b in np.arange(beat, SONG_SECONDS, beat * 2):
        chord = chords[(int(b // bar)) % len(chords)]
        freqs = [root * (2 ** ((chord + iv) / 12)) for iv in (0, 4, 7)]
        chop = sum(karplus(f, 0.18, decay=0.94, brightness=0.65) for f in freqs) / 3
        add(buf, chop, b, 0.38, 0.25)

    # Psychedelic lead phrases every 8 bars.
    phrase_times = [8, 24, 40, 52] if variant == 1 else [4, 20, 36, 48]
    for start in phrase_times:
        for j, deg in enumerate([7, 9, 10, 12, 14, 12, 10, 7]):
            freq = root * (2 ** (deg / 12)) * (1.0 if variant == 1 else 1.5)
            dur = beat * 0.72
            lead = sine(freq, dur, 0.35, phase=0.2) + 0.25 * sine(freq * 2.01, dur, 0.22)
            lead *= adsr(len(lead), 0.018, 0.08, 0.55, 0.16)
            # Tremolo for space-rock shimmer.
            tt = np.arange(len(lead)) / SAMPLE_RATE
            lead *= 0.75 + 0.25 * np.sin(2*np.pi*(5.5 + variant)*tt)
            add(buf, lead, start + j * beat * 0.75, 0.24, 0.55 if j % 2 else -0.55)

    # Arrange intro/outro dynamics.
    fade = int(2.2 * SAMPLE_RATE)
    buf[:fade] *= np.linspace(0, 1, fade)[:, None]
    buf[-fade:] *= np.linspace(1, 0, fade)[:, None]
    buf = soft_clip(buf)
    sf.write(path, buf, SAMPLE_RATE)
    return {"title": title, "file": str(path), "bpm": bpm, "root_hz": root, "duration_seconds": probe_duration(path)}


def render_voice(src: Path, out: Path) -> None:
    run([
        "ffmpeg", "-y", "-i", str(src),
        "-filter:a",
        f"aresample={SAMPLE_RATE},aformat=sample_fmts=fltp:channel_layouts=stereo,"
        "loudnorm=I=-15:TP=-1.5:LRA=9,highpass=f=80,afade=t=in:st=0:d=0.04,areverse,afade=t=in:st=0:d=0.08,areverse",
        "-ar", str(SAMPLE_RATE), "-ac", "2", "-c:a", "pcm_s16le", str(out),
    ])


def render_song_norm(src: Path, out: Path) -> None:
    run([
        "ffmpeg", "-y", "-i", str(src),
        "-filter:a",
        f"aresample={SAMPLE_RATE},aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"loudnorm=I=-14:TP=-1.3:LRA=8,afade=t=in:st=0:d=1.2,afade=t=out:st={SONG_SECONDS-2.4}:d=2.4",
        "-ar", str(SAMPLE_RATE), "-ac", "2", "-c:a", "pcm_s16le", str(out),
    ])


def render_pair(voice_wav: Path, song_wav: Path, out: Path) -> dict:
    voice_d = probe_duration(voice_wav)
    song_d = probe_duration(song_wav)
    song_delay = max(0.0, voice_d - INTRO_OVERLAP_SECONDS)
    expected = song_delay + song_d
    delay_ms = int(round(song_delay * 1000))
    voice_ms = int(round(voice_d * 1000))
    filt = ";".join([
        f"[0:a]aresample={SAMPLE_RATE},aformat=sample_fmts=fltp:channel_layouts=stereo[v]",
        f"[1:a]aresample={SAMPLE_RATE},aformat=sample_fmts=fltp:channel_layouts=stereo,adelay={delay_ms}|{delay_ms}[sdel]",
        "[sdel]asplit=2[squiet][smain]",
        f"[squiet]atrim=start={song_delay}:duration={INTRO_OVERLAP_SECONDS},asetpts=PTS-STARTPTS,volume=0.11,adelay={delay_ms}|{delay_ms}[bed]",
        f"[smain]atrim=start={voice_d}:duration={max(0.1, expected - voice_d)},asetpts=PTS-STARTPTS,adelay={voice_ms}|{voice_ms}[main]",
        "[v][bed][main]amix=inputs=3:duration=longest:dropout_transition=0,alimiter=limit=0.95[out]",
    ])
    run(["ffmpeg", "-y", "-i", str(voice_wav), "-i", str(song_wav), "-filter_complex", filt, "-map", "[out]", "-ar", str(SAMPLE_RATE), "-ac", "2", "-c:a", "pcm_s16le", str(out)])
    actual = probe_duration(out)
    if abs(actual - expected) > 1.25:
        raise RuntimeError(f"Pair duration mismatch {out}: expected {expected:.2f}, got {actual:.2f}")
    return {"file": str(out), "voice_duration": voice_d, "song_duration": song_d, "song_delay": song_delay, "expected_duration": expected, "actual_duration": actual}


def render_gap(path: Path) -> None:
    run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r={SAMPLE_RATE}:cl=stereo", "-t", str(GAP_SECONDS), "-c:a", "pcm_s16le", str(path)])


def concat(parts: list[Path], final: Path) -> None:
    txt = final.with_suffix(".concat.txt")
    txt.write_text("".join(f"file '{p}'\n" for p in parts), encoding="utf-8")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(txt), "-filter:a", "loudnorm=I=-14:TP=-1.2:LRA=10,alimiter=limit=0.95", "-c:a", "libmp3lame", "-q:a", "2", str(final)])


def main() -> None:
    for p in [VOICE_1, VOICE_2, VOICE_3]:
        if not p.exists():
            raise FileNotFoundError(p)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = OUT_ROOT / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    theme_brief = {
        "theme_title": "Intergalactic Pizza Festival Delivery Run",
        "one_sentence_story": "A stoner-space pizza courier tries to deliver one cosmic pie through an intergalactic music festival while bluegrass banjos go psychedelic.",
        "structure": "intro -> track -> intro -> track -> outro",
        "mix_mode": "radio_duck_safe",
        "song_seconds": SONG_SECONDS,
        "remote_gpu_calls": False,
        "music_generation": "offline procedural psychedelic bluegrass/space-rock instrumentals for quick test",
        "voice_generation": "Hermes TTS voice segments for theme-specific story; not celebrity cloning",
    }

    raw1 = out_dir / "track_01_cosmic_crust_run_raw.wav"
    raw2 = out_dir / "track_02_moon_goat_extra_sauce_raw.wav"
    song_reports = [
        render_psy_bluegrass_track(raw1, bpm=112, root=98.0, title="Cosmic Crust Run", variant=1),
        render_psy_bluegrass_track(raw2, bpm=126, root=73.42, title="Moon Goat Extra Sauce", variant=2),
    ]

    voices = [VOICE_1, VOICE_2]
    songs = [raw1, raw2]
    rendered_parts: list[Path] = []
    pair_reports = []
    events: list[TimelineEvent] = []
    cursor = 0.0
    gap = out_dir / "gap_550ms.wav"
    render_gap(gap)

    names = [("Captain Crustwave", "Cosmic Crust Run"), ("Slice Deck Update", "Moon Goat Extra Sauce")]
    for i, (voice_src, song_src) in enumerate(zip(voices, songs), start=1):
        voice_wav = out_dir / f"{i:02d}_voice.wav"
        song_wav = out_dir / f"{i:02d}_song.wav"
        pair_wav = out_dir / f"{i:02d}_pair.wav"
        render_voice(voice_src, voice_wav)
        render_song_norm(song_src, song_wav)
        report = render_pair(voice_wav, song_wav, pair_wav)
        report.update({"host": names[i-1][0], "song_title": names[i-1][1]})
        pair_reports.append(report)
        rendered_parts.append(pair_wav)
        dur = probe_duration(pair_wav)
        events.append(TimelineEvent(i, "pair", f"{names[i-1][0]} into {names[i-1][1]}", str(pair_wav), cursor, dur, "voice_intro_plus_song", "internal_host_intro_bed_only"))
        cursor += dur
        rendered_parts.append(gap)
        events.append(TimelineEvent(100+i, "gap", "breath gap", str(gap), cursor, GAP_SECONDS, "separator"))
        cursor += GAP_SECONDS

    outro = out_dir / "99_outro_voice.wav"
    render_voice(VOICE_3, outro)
    outro_d = probe_duration(outro)
    rendered_parts.append(outro)
    events.append(TimelineEvent(199, "voice", "Pizza Delivered Outro", str(outro), cursor, outro_d, "solo_outro"))
    cursor += outro_d

    # Pair-level timeline should be sequential.
    checks = []
    for prev, cur in zip(events, events[1:]):
        prev_end = prev.start_seconds + prev.duration_seconds
        ok = cur.start_seconds >= prev_end - 0.05
        checks.append({"name": f"no_overlap_{prev.index}_to_{cur.index}", "passed": ok, "detail": f"prev_end={prev_end:.3f} cur_start={cur.start_seconds:.3f}"})
        if not ok:
            raise RuntimeError(checks[-1])

    final = out_dir / "FULL_intergalactic_pizza_festival_radio_duck_safe.mp3"
    concat(rendered_parts, final)
    final_d = probe_duration(final)
    expected = sum(probe_duration(p) for p in rendered_parts)
    checks.extend([
        {"name": "final_duration_matches_expected", "passed": abs(final_d - expected) <= 1.5, "detail": f"expected={expected:.3f} actual={final_d:.3f}"},
        {"name": "final_file_exists", "passed": final.exists() and final.stat().st_size > 0, "detail": f"size={final.stat().st_size}"},
        {"name": "remote_gpu_calls_disabled", "passed": True, "detail": "offline/local only"},
    ])
    qa = {"ok": all(c["passed"] for c in checks), "checks": checks, "duration_seconds": final_d, "expected_duration_seconds": expected}
    if not qa["ok"]:
        raise RuntimeError("QA failed")

    manifest = {
        "ok": True,
        "run_id": run_id,
        "theme_brief": theme_brief,
        "engine": "sonicforge_dj_show_engine_v01_custom_pizza",
        "mode": "radio_duck_safe",
        "final": str(final),
        "duration_seconds": final_d,
        "sha256": sha256(final),
        "song_reports": song_reports,
        "pair_reports": pair_reports,
        "timeline": [asdict(e) for e in events],
    }
    (out_dir / "theme_brief.json").write_text(json.dumps(theme_brief, indent=2), encoding="utf-8")
    (out_dir / "timeline.json").write_text(json.dumps([asdict(e) for e in events], indent=2), encoding="utf-8")
    (out_dir / "qa_report.json").write_text(json.dumps(qa, indent=2), encoding="utf-8")
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
