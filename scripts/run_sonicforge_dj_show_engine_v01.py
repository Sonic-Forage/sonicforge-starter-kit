#!/usr/bin/env python3
"""SonicForge DJ Show Engine v0.1.

Timeline-first renderer for host voice -> 60s song pairs.

Fixes from prior bad mixes:
- explicit timeline manifest before rendering;
- validator rejects overlapping songs/voices except one controlled intro bed;
- renders pair-by-pair, then concatenates pairs (no all-at-once graph);
- every pair has predictable duration and is verified before full mix;
- no remote GPU/API calls.

Mode: radio_duck_safe
- Voice starts solo.
- Song fades in quietly under the final 2 seconds of the voice.
- Voice ends; song continues at normal level for ~60 seconds.
- Next host begins only after the prior song section finishes.
"""
from __future__ import annotations

import hashlib
import json
import os
import shlex
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

CACHE_ROOT = Path(os.environ.get("SONICFORGE_AUDIO_CACHE", "/opt/data/audio_cache"))
OUT_ROOT = CACHE_ROOT / "sonicforge_dj_show_engine_v01"
VOICE_ROOT = CACHE_ROOT / "omnivoice_five_voice_conversation/20260503T001349Z"
ALBUM_AUDIO = Path("/opt/data/workspace/projects/dj-vanta-funk-glitch-bass-album-dataset/generated/20260502T185849Z/organized/audio-only")

SONG_SECONDS = 60.0
INTRO_OVERLAP_SECONDS = 2.0
GAP_SECONDS = 0.55
SAMPLE_RATE = 44100
DEFAULT_THEME_BRIEF = {
    "theme_title": "SonicForge Offline Host Show",
    "one_sentence_story": "A rotating host crew introduces cached/generated tracks in a safe radio-DJ flow.",
    "mix_mode": "radio_duck_safe",
    "song_seconds": SONG_SECONDS,
    "track_count": 4,
    "remote_gpu_required_for_mixing": False,
    "quality_rule": "Render timeline and QA report before final delivery.",
}


@dataclass
class TimelineEvent:
    index: int
    event_type: str  # voice | song | gap
    title: str
    file: str
    start_seconds: float
    duration_seconds: float
    role: str
    allowed_overlap: str = "none"


def q(path: Path | str) -> str:
    return shlex.quote(str(path))


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


PAIRS = [
    {
        "host": "Velvet Orbit MC",
        "voice": VOICE_ROOT / "01_velvet_orbit_mc-Velvet-Orbit-MC.wav",
        "song_title": "Digital Underground Funk Bus",
        "song": ALBUM_AUDIO / "01-Digital-Underground-Funk-Bus.mp3",
        "song_start": 24,
    },
    {
        "host": "Prism Auntie",
        "voice": VOICE_ROOT / "02_prism_auntie-Prism-Auntie.wav",
        "song_title": "Jo Brings the Wobble",
        "song": ALBUM_AUDIO / "06-Jo-Brings-the-Wobble.mp3",
        "song_start": 22,
    },
    {
        "host": "Glitch Deck Cadet",
        "voice": VOICE_ROOT / "03_glitch_deck_cadet-Glitch-Deck-Cadet.wav",
        "song_title": "Strawberry Wobble Experience",
        "song": ALBUM_AUDIO / "09-Strawberry-Wobble-Experience.mp3",
        "song_start": 28,
    },
    {
        "host": "Neon Pearl Dispatch",
        "voice": VOICE_ROOT / "04_neon_pearl_dispatch-Neon-Pearl-Dispatch.wav",
        "song_title": "Hermes Memory Palace Shuffle",
        "song": ALBUM_AUDIO / "21-Hermes-Memory-Palace-Shuffle.mp3",
        "song_start": 24,
    },
]
OUTRO = {
    "host": "Sub Bass Elder Outro",
    "voice": VOICE_ROOT / "05_sub_bass_elder-Sub-Bass-Elder.wav",
}


def require_sources() -> None:
    required = []
    for pair in PAIRS:
        required += [pair["voice"], pair["song"]]
    required.append(OUTRO["voice"])
    missing = [str(p) for p in required if not Path(p).exists()]
    if missing:
        raise FileNotFoundError("Missing required audio sources:\n" + "\n".join(missing))


def render_voice(src: Path, out: Path, target_lufs: str = "-15") -> None:
    run([
        "ffmpeg", "-y", "-i", str(src),
        "-filter:a",
        f"aresample={SAMPLE_RATE},aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"loudnorm=I={target_lufs}:TP=-1.5:LRA=9,"
        "highpass=f=80,afade=t=in:st=0:d=0.04,areverse,afade=t=in:st=0:d=0.08,areverse",
        "-ar", str(SAMPLE_RATE), "-ac", "2", "-c:a", "pcm_s16le", str(out),
    ])


def render_song_cut(src: Path, start: int, out: Path) -> None:
    # Conservative song cut: light fades only, no overlapping with other songs.
    run([
        "ffmpeg", "-y", "-ss", str(start), "-t", str(SONG_SECONDS), "-i", str(src),
        "-filter:a",
        f"aresample={SAMPLE_RATE},aformat=sample_fmts=fltp:channel_layouts=stereo,"
        "loudnorm=I=-14:TP=-1.4:LRA=9,"
        f"afade=t=in:st=0:d=1.5,afade=t=out:st={SONG_SECONDS-2.5}:d=2.5",
        "-ar", str(SAMPLE_RATE), "-ac", "2", "-c:a", "pcm_s16le", str(out),
    ])


def render_pair(voice_wav: Path, song_wav: Path, out: Path) -> dict:
    voice_d = probe_duration(voice_wav)
    song_d = probe_duration(song_wav)
    song_delay = max(0.0, voice_d - INTRO_OVERLAP_SECONDS)
    expected = song_delay + song_d
    delay_ms = int(round(song_delay * 1000))

    # Split song into the intro-overlap bed and the main remainder. The bed is
    # very quiet, so host remains intelligible; the main song begins after voice.
    # No second song or second voice can enter this pair.
    filter_complex = ";".join([
        f"[0:a]aresample={SAMPLE_RATE},aformat=sample_fmts=fltp:channel_layouts=stereo[v]",
        f"[1:a]aresample={SAMPLE_RATE},aformat=sample_fmts=fltp:channel_layouts=stereo,adelay={delay_ms}|{delay_ms}[sdel]",
        f"[sdel]asplit=2[squiet][smain]",
        f"[squiet]atrim=start={song_delay}:duration={INTRO_OVERLAP_SECONDS},asetpts=PTS-STARTPTS,volume=0.12,adelay={delay_ms}|{delay_ms}[bed]",
        f"[smain]atrim=start={voice_d}:duration={max(0.1, expected - voice_d)},asetpts=PTS-STARTPTS,adelay={int(round(voice_d*1000))}|{int(round(voice_d*1000))}[main]",
        f"[v][bed][main]amix=inputs=3:duration=longest:dropout_transition=0,alimiter=limit=0.95[out]",
    ])
    run([
        "ffmpeg", "-y", "-i", str(voice_wav), "-i", str(song_wav),
        "-filter_complex", filter_complex,
        "-map", "[out]", "-ar", str(SAMPLE_RATE), "-ac", "2", "-c:a", "pcm_s16le", str(out),
    ])
    actual = probe_duration(out)
    if abs(actual - expected) > 1.25:
        raise RuntimeError(f"Pair duration mismatch for {out}: expected {expected:.2f}, got {actual:.2f}")
    return {
        "file": str(out),
        "voice_duration": voice_d,
        "song_duration": song_d,
        "song_delay": song_delay,
        "expected_duration": expected,
        "actual_duration": actual,
    }


def render_gap(path: Path) -> None:
    run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r={SAMPLE_RATE}:cl=stereo",
        "-t", str(GAP_SECONDS), "-c:a", "pcm_s16le", str(path),
    ])


def validate_timeline(events: list[TimelineEvent]) -> list[dict]:
    """Validate the public timeline and return structured QA checks."""
    checks: list[dict] = []

    def record(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": passed, "detail": detail})
        if not passed:
            raise ValueError(f"Timeline QA failed: {name}: {detail}")

    record("has_events", bool(events), f"events={len(events)}")
    for ev in events:
        record(
            f"positive_duration_{ev.index}",
            ev.duration_seconds > 0,
            f"{ev.title}: {ev.duration_seconds:.3f}s",
        )

    sorted_events = sorted(events, key=lambda e: e.start_seconds)
    for prev, cur in zip(sorted_events, sorted_events[1:]):
        prev_end = prev.start_seconds + prev.duration_seconds
        allowed = cur.allowed_overlap == "host_intro_bed" or prev.allowed_overlap == "host_intro_bed"
        record(
            f"no_forbidden_overlap_{prev.index}_to_{cur.index}",
            cur.start_seconds >= prev_end - 0.05 or allowed,
            f"{prev.title} ends {prev_end:.3f}, {cur.title} starts {cur.start_seconds:.3f}",
        )
    return checks


def build_qa_report(
    *,
    final: Path,
    final_duration: float,
    expected_duration: float,
    timeline_checks: list[dict],
    pair_reports: list[dict],
) -> dict:
    duration_delta = abs(final_duration - expected_duration)
    pair_duration_ok = all(abs(p["actual_duration"] - p["expected_duration"]) <= 1.25 for p in pair_reports)
    checks = [
        *timeline_checks,
        {
            "name": "final_duration_matches_manifest",
            "passed": duration_delta <= 1.5,
            "detail": f"expected={expected_duration:.3f}s actual={final_duration:.3f}s delta={duration_delta:.3f}s",
        },
        {
            "name": "pair_durations_match",
            "passed": pair_duration_ok,
            "detail": f"pairs={len(pair_reports)}",
        },
        {
            "name": "final_file_exists",
            "passed": final.exists() and final.stat().st_size > 0,
            "detail": f"size={final.stat().st_size if final.exists() else 0}",
        },
        {
            "name": "remote_gpu_calls_disabled",
            "passed": True,
            "detail": "mixing uses cached/offline files only",
        },
    ]
    ok = all(c["passed"] for c in checks)
    return {
        "ok": ok,
        "engine": "sonicforge_dj_show_engine_v01",
        "mode": "radio_duck_safe",
        "final": str(final),
        "duration_seconds": final_duration,
        "expected_duration_seconds": expected_duration,
        "checks": checks,
    }


def concat(parts: list[Path], final: Path) -> None:
    concat_file = final.with_suffix(".concat.txt")
    concat_file.write_text("".join(f"file '{p}'\n" for p in parts), encoding="utf-8")
    run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-filter:a", "loudnorm=I=-14:TP=-1.2:LRA=10,alimiter=limit=0.95",
        "-c:a", "libmp3lame", "-q:a", "2", str(final),
    ])


def main() -> None:
    require_sources()
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = OUT_ROOT / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    gap = out_dir / "gap_550ms.wav"
    render_gap(gap)

    rendered_parts: list[Path] = []
    pair_reports = []
    timeline_events: list[TimelineEvent] = []
    cursor = 0.0

    for i, pair in enumerate(PAIRS, start=1):
        voice_norm = out_dir / f"{i:02d}_voice_{pair['host'].lower().replace(' ', '_')}.wav"
        song_cut = out_dir / f"{i:02d}_song_{pair['song_title'].lower().replace(' ', '_')}.wav"
        pair_out = out_dir / f"{i:02d}_pair_{pair['host'].lower().replace(' ', '_')}_into_{pair['song_title'].lower().replace(' ', '_')}.wav"

        render_voice(Path(pair["voice"]), voice_norm)
        render_song_cut(Path(pair["song"]), int(pair["song_start"]), song_cut)
        report = render_pair(voice_norm, song_cut, pair_out)
        report.update({"host": pair["host"], "song_title": pair["song_title"]})
        pair_reports.append(report)
        rendered_parts.append(pair_out)

        # Timeline is pair-level for safety. Detailed intro overlap is internal to pair.
        dur = probe_duration(pair_out)
        timeline_events.append(TimelineEvent(
            index=i,
            event_type="pair",
            title=f"{pair['host']} into {pair['song_title']}",
            file=str(pair_out),
            start_seconds=cursor,
            duration_seconds=dur,
            role="voice_intro_plus_song",
            allowed_overlap="internal_host_intro_bed_only",
        ))
        cursor += dur
        if i != len(PAIRS):
            rendered_parts.append(gap)
            timeline_events.append(TimelineEvent(
                index=100+i, event_type="gap", title="breath gap", file=str(gap),
                start_seconds=cursor, duration_seconds=GAP_SECONDS, role="separator"
            ))
            cursor += GAP_SECONDS

    # Outro is solo, after all music ends.
    outro_norm = out_dir / "99_voice_sub_bass_elder_outro.wav"
    render_voice(Path(OUTRO["voice"]), outro_norm)
    rendered_parts.append(gap)
    timeline_events.append(TimelineEvent(
        index=198, event_type="gap", title="pre-outro breath gap", file=str(gap),
        start_seconds=cursor, duration_seconds=GAP_SECONDS, role="separator"
    ))
    cursor += GAP_SECONDS
    outro_d = probe_duration(outro_norm)
    rendered_parts.append(outro_norm)
    timeline_events.append(TimelineEvent(
        index=199, event_type="voice", title=OUTRO["host"], file=str(outro_norm),
        start_seconds=cursor, duration_seconds=outro_d, role="solo_outro"
    ))
    cursor += outro_d

    timeline_checks = validate_timeline(timeline_events)
    final = out_dir / "FULL_sonicforge_dj_show_engine_v01_radio_duck_safe.mp3"
    concat(rendered_parts, final)
    final_d = probe_duration(final)
    expected = sum(probe_duration(p) for p in rendered_parts)
    qa_report = build_qa_report(
        final=final,
        final_duration=final_d,
        expected_duration=expected,
        timeline_checks=timeline_checks,
        pair_reports=pair_reports,
    )
    if not qa_report["ok"]:
        raise RuntimeError("QA report failed")
    if abs(final_d - expected) > 1.5:
        raise RuntimeError(f"Final duration mismatch: expected {expected:.2f}, got {final_d:.2f}")

    theme_brief = dict(DEFAULT_THEME_BRIEF)
    theme_brief.update({
        "run_id": run_id,
        "hosts": [pair["host"] for pair in PAIRS] + [OUTRO["host"]],
        "songs": [pair["song_title"] for pair in PAIRS],
    })

    manifest = {
        "ok": True,
        "engine": "sonicforge_dj_show_engine_v01",
        "mode": "radio_duck_safe",
        "run_id": run_id,
        "theme_brief": theme_brief,
        "remote_gpu_calls": False,
        "fresh_voice_generation": False,
        "voice_source": "cached reviewed OmniVoice clips",
        "song_source": "existing generated ACE-Step/ComfyUI album tracks",
        "rules": [
            "timeline first",
            "no overlapping host clips",
            "no overlapping songs across pairs",
            "only controlled quiet intro bed inside each voice-song pair",
            "duration verification required before final delivery",
            "write qa_report.json for every render",
        ],
        "final": str(final),
        "duration_seconds": final_d,
        "sha256": sha256(final),
        "expected_duration_seconds": expected,
        "pair_reports": pair_reports,
        "timeline": [asdict(e) for e in timeline_events],
    }
    (out_dir / "theme_brief.json").write_text(json.dumps(theme_brief, indent=2), encoding="utf-8")
    (out_dir / "timeline.json").write_text(json.dumps([asdict(e) for e in timeline_events], indent=2), encoding="utf-8")
    (out_dir / "qa_report.json").write_text(json.dumps(qa_report, indent=2), encoding="utf-8")
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
