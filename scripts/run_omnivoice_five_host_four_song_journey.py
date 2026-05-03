#!/usr/bin/env python3
"""Five OmniVoice hosts + four 2-minute journey songs + final outro.

Structure:
  Host 1 intro -> Song 1 -> Host 2 intro -> Song 2 -> Host 3 intro ->
  Song 3 -> Host 4 intro -> Song 4 -> Host 5 outro

Voices use an allowlisted OmniVoice Voice Design tag algorithm. Music is generated
locally as procedural synthetic demo beds while ComfyUI/ACE-Step endpoint is not
available. The arrangement uses DJ-style overlap, sidechain ducking, and fades.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import shutil
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
from gradio_client import Client

SR = 44100
OUT_ROOT = Path("/opt/data/audio_cache/sonicforge_five_host_journey")
SPACE_ID = "k2-fsa/OmniVoice"
SONG_SECONDS = 120.0

VOICE_TAGS = {
    "gender": {"male": "Male / 男", "female": "Female / 女"},
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
    "style": {"auto": "Auto", "whisper": "Whisper / 耳语"},
    "accent": {
        "american accent": "American Accent / 美式口音",
        "british accent": "British Accent / 英国口音",
        "australian accent": "Australian Accent / 澳大利亚口音",
    },
    "dialect": {"auto": "Auto"},
}

HOSTS = [
    {
        "id": "01_velvet_orbit_mc",
        "name": "Velvet Orbit MC",
        "tags": {"gender": "male", "age": "middle-aged", "pitch": "low pitch", "style": "auto", "accent": "american accent", "dialect": "auto"},
        "text": "Welcome to the SonicForge relay, crew. I am Velvet Orbit MC. Door one is opening now: chrome clouds, warm bass reactor, friendly humans only. Stay close to the signal, because the journey is about to bend.",
    },
    {
        "id": "02_prism_auntie",
        "name": "Prism Auntie",
        "tags": {"gender": "female", "age": "elderly", "pitch": "high pitch", "style": "whisper", "accent": "british accent", "dialect": "auto"},
        "text": "[sigh] Oh my little neon travelers, you made it through door one. Door two is a crystal library with a rude subwoofer. Please whisper to the shelves, but dance with your whole heart.",
    },
    {
        "id": "03_glitch_deck_cadet",
        "name": "Glitch Deck Cadet",
        "tags": {"gender": "male", "age": "young adult", "pitch": "moderate pitch", "style": "auto", "accent": "australian accent", "dialect": "auto"},
        "text": "Cadet on deck! Door three is unstable in a good way. I patched the wobble bus into the moon modem, and if the snare teleports, do not panic. That means the forge accepted our offering.",
    },
    {
        "id": "04_neon_pearl_dispatch",
        "name": "Neon Pearl Dispatch",
        "tags": {"gender": "female", "age": "young adult", "pitch": "very high pitch", "style": "auto", "accent": "american accent", "dialect": "auto"},
        "text": "Neon Pearl Dispatch to all dancers: door four is the starlight tunnel. Hydration carts are stage left, lost aliens are stage right, and the cosmic wizard is definitely not supposed to be awake yet.",
    },
    {
        "id": "05_sub_bass_elder",
        "name": "Sub Bass Elder",
        "tags": {"gender": "male", "age": "elderly", "pitch": "very low pitch", "style": "auto", "accent": "british accent", "dialect": "auto"},
        "text": "[confirmation-en] I am the Sub Bass Elder. Wow. That was a close one. We nearly woke the Cosmic Wizard of the Wrong Drop, but kindness held the floor and the humans kept the glow alive. Return safely through the SonicForge portal, and never rush the build.",
    },
]

SONGS = [
    {"id": "song_01_chrome_cloud_gate", "title": "Chrome Cloud Gate", "bpm": 104, "root": 43.65, "style": "cybernetic glitch hop opener"},
    {"id": "song_02_crystal_library_bloom", "title": "Crystal Library Bloom", "bpm": 132, "root": 55.00, "style": "liquid garage psy-dub shimmer"},
    {"id": "song_03_moon_modem_wobble", "title": "Moon Modem Wobble", "bpm": 110, "root": 48.99, "style": "funky alien glitch bass"},
    {"id": "song_04_cosmic_wizard_near_miss", "title": "Cosmic Wizard Near Miss", "bpm": 128, "root": 51.91, "style": "festival rave rescue finale"},
]


def sh(cmd):
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def sanitize_tags(tags: dict) -> dict:
    clean = {}
    for family, allowed in VOICE_TAGS.items():
        raw = str(tags.get(family, "auto")).strip().lower()
        if raw not in allowed:
            raw = "auto" if "auto" in allowed else next(iter(allowed))
        clean[family] = raw
    voice_instruct = ", ".join(clean[k] for k in ["gender", "age", "pitch", "accent", "style"] if clean[k] != "auto")
    controls = {family: VOICE_TAGS[family][value] for family, value in clean.items()}
    return {"tags": clean, "voice_instruct": voice_instruct, "controls": controls}


def ffprobe(path: Path) -> dict:
    return json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration,size", "-of", "json", str(path)
    ], text=True)).get("format", {})


def find_cached_voice(host: dict) -> Path | None:
    root = Path("/opt/data/audio_cache/omnivoice_five_voice_conversation")
    if not root.exists():
        return None
    for folder in sorted([p for p in root.iterdir() if p.is_dir()], reverse=True):
        matches = sorted(folder.glob(f"{host['id']}-*.wav")) + sorted(folder.glob(f"{host['id']}-*.mp3"))
        if matches:
            return matches[0]
    return None


def render_voices(out_dir: Path) -> list[dict]:
    """Render fresh voices when quota allows; otherwise reuse the reviewed five-voice cache."""
    results = []
    client = None
    try:
        client = Client(SPACE_ID)
    except Exception as e:
        print(json.dumps({"voice_backend_warning": f"space client unavailable: {type(e).__name__}"}), flush=True)
    for host in HOSTS:
        pack = sanitize_tags(host["tags"])
        dest = out_dir / f"{host['id']}-{host['name'].replace(' ', '-')}.wav"
        status = "fresh"
        if client is not None:
            try:
                c = pack["controls"]
                audio_path, status = client.predict(
                    host["text"], "English", 32, 2.0, True, 1.0, 0.0, True, True,
                    c["gender"], c["age"], c["pitch"], c["style"], c["accent"], c["dialect"],
                    api_name="/_design_fn",
                )
                src = Path(audio_path)
                dest = out_dir / f"{host['id']}-{host['name'].replace(' ', '-')}{src.suffix or '.wav'}"
                shutil.copy2(src, dest)
            except Exception as e:
                cached = find_cached_voice(host)
                if cached is None:
                    raise
                dest = out_dir / f"{host['id']}-{host['name'].replace(' ', '-')}{cached.suffix}"
                shutil.copy2(cached, dest)
                status = f"reused cached reviewed voice after Space quota/error: {type(e).__name__}"
        else:
            cached = find_cached_voice(host)
            if cached is None:
                raise RuntimeError(f"no cached voice found for {host['id']}")
            dest = out_dir / f"{host['id']}-{host['name'].replace(' ', '-')}{cached.suffix}"
            shutil.copy2(cached, dest)
            status = "reused cached reviewed voice"
        meta = {**host, "audio_file": str(dest), "status": status, "voice_instruct": pack["voice_instruct"], "allowed_tags": pack["tags"], "probe": ffprobe(dest)}
        results.append(meta)
        print(json.dumps({"voice_done": host["name"], "file": str(dest), "voice_instruct": pack["voice_instruct"], "status": status}, ensure_ascii=False), flush=True)
    return results


def env(n: int, a=0.005, r=0.04):
    e = np.ones(n, dtype=np.float32)
    aa = min(n, int(a * SR)); rr = min(n, int(r * SR))
    if aa > 1: e[:aa] = np.linspace(0, 1, aa)
    if rr > 1: e[-rr:] = np.linspace(1, 0, rr)
    return e


def add_note(buf, start, dur, freq, amp, wave="sine", pan=0.0):
    i = int(start * SR); n = int(dur * SR)
    if i >= len(buf): return
    n = min(n, len(buf) - i)
    t = np.arange(n) / SR
    if wave == "saw": x = 2 * ((freq * t) % 1) - 1
    elif wave == "square": x = np.sign(np.sin(2 * np.pi * freq * t))
    elif wave == "tri": x = 2 * np.abs(2 * ((freq * t) % 1) - 1) - 1
    else: x = np.sin(2 * np.pi * freq * t)
    if wave != "sine": x = 0.38 * x + 0.62 * np.sin(2 * np.pi * freq * t)
    x = (x * amp * env(n)).astype(np.float32)
    l = math.cos((pan + 1) * math.pi / 4); r = math.sin((pan + 1) * math.pi / 4)
    buf[i:i+n, 0] += x * l; buf[i:i+n, 1] += x * r


def generate_song(song: dict, out_dir: Path) -> dict:
    dur = SONG_SECONDS; bpm = song["bpm"]; beat = 60 / bpm; root = song["root"]
    N = int(dur * SR); y = np.zeros((N, 2), np.float32); rng = np.random.default_rng(int(root * 1000) + bpm)
    progressions = [root, root * 2 ** (3/12), root * 2 ** (7/12), root * 2 ** (-2/12)]
    for bar in range(int(dur / (4 * beat)) + 1):
        base = bar * 4 * beat; r = progressions[bar % 4]
        # intensity curve for a journey: intro -> build -> drop -> bridge -> finale
        pos = base / dur
        intensity = 0.45 + 0.55 * min(1, max(0, (pos - 0.12) / 0.35))
        if 0.55 < pos < 0.68: intensity *= 0.58
        if pos > 0.72: intensity *= 1.12
        # bass patterns vary by track
        pattern = [(0, 1, .28), (0.75, 1.5, .16), (1.5, 2, .22), (2.5, 1, .24), (3.25, 1.25, .16)]
        if song["id"].endswith("bloom"):
            pattern = [(0, 1, .20), (1.25, 1.5, .16), (2.0, 2, .20), (3.25, 1, .18)]
        if song["id"].endswith("near_miss"):
            pattern = [(0, 1, .32), (1.0, 1, .18), (2.0, 2, .26), (3.0, 1.5, .22)]
        for off, mul, amp in pattern:
            add_note(y, base + off * beat, .25, r * mul, amp * intensity, "square" if song["id"] != "song_02_crystal_library_bloom" else "sine", pan=-.05)
        # arps/pads
        scale = [r*4, r*4*2**(2/12), r*4*2**(5/12), r*4*2**(7/12), r*8]
        divisions = 8 if bpm < 120 else 12
        for k in range(divisions):
            add_note(y, base + k * (4*beat/divisions), .10, scale[(k+bar) % len(scale)], .08 * intensity, "tri" if song["id"].endswith("bloom") else "saw", pan=np.sin(k + bar) * .75)
        # pad bed
        if bar % 2 == 0:
            for f in [r*2, r*2*2**(7/12), r*4]: add_note(y, base, 7.0*beat, f, .035 * intensity, "sine", pan=(rng.random()*2-1)*.5)
    # drums
    for b in np.arange(0, dur, beat):
        # Kick
        for off, amp in [(0, .75), (2.0, .48), (3.0, .25)]:
            i = int((b + off*beat) * SR); n = int(.15 * SR)
            if i+n < N:
                t = np.arange(n)/SR; f = 95*np.exp(-t*22)+42; ph = np.cumsum(2*np.pi*f/SR)
                k = np.sin(ph)*np.exp(-t*18)*amp; y[i:i+n] += k[:, None]
        # clap/snare
        for off in ([2.0] if bpm < 120 else [1.0, 3.0]):
            i = int((b + off*beat) * SR); n = int(.10 * SR)
            if i+n < N:
                sn = (rng.normal(0,1,n)*.12 + np.sin(2*np.pi*210*np.arange(n)/SR)*.12) * np.exp(-np.arange(n)/(.030*SR))
                y[i:i+n,0] += sn*.9; y[i:i+n,1] += sn
        # hats
        for off in [.5, 1.5, 2.5, 3.5]:
            i = int((b + off*beat) * SR); n = int(.026 * SR)
            if i+n < N:
                h = rng.normal(0,1,n) * np.exp(-np.arange(n)/(.008*SR)) * .045
                y[i:i+n,0] += h; y[i:i+n,1] += h*.85
    # special sweeps at doors
    for st in [24, 54, 86]:
        n = int(3.5*SR); i = int(st*SR)
        if i+n < N:
            t = np.arange(n)/SR
            sweep = (np.sin(2*np.pi*(180+1500*t/3.5)*t)*.09 + rng.normal(0,1,n)*.025) * (t/3.5)
            y[i:i+n,0] += sweep; y[i:i+n,1] -= sweep*.75
    # delay + arrangement fades
    for d, a in [(int(.17*SR), .14), (int(.34*SR), .07)]: y[d:] += y[:-d] * a
    fi = int(5*SR); fo = int(9*SR)
    y[:fi] *= np.linspace(0,1,fi)[:,None]; y[-fo:] *= np.linspace(1,0,fo)[:,None]
    y = np.tanh(y * 1.16); y = y/(np.max(np.abs(y))+1e-9) * .90
    wav = out_dir / f"{song['id']}-{song['title'].replace(' ', '-')}.wav"
    sf.write(wav, y, SR)
    mp3 = wav.with_suffix(".mp3")
    sh(["ffmpeg", "-y", "-i", str(wav), "-codec:a", "libmp3lame", "-q:a", "2", str(mp3)])
    meta = {**song, "file": str(mp3), "probe": ffprobe(mp3), "sha256": hashlib.sha256(mp3.read_bytes()).hexdigest()}
    print(json.dumps({"song_done": song["title"], "file": str(mp3)}, ensure_ascii=False), flush=True)
    return meta


def read_audio(path: Path):
    x, sr = sf.read(path, always_2d=True)
    if sr != SR:
        tmp = path.with_suffix(".441.wav")
        sh(["ffmpeg", "-y", "-i", str(path), "-ar", str(SR), "-ac", "2", str(tmp)])
        x, sr = sf.read(tmp, always_2d=True)
    return x.astype(np.float32)


def voice_env(stereo):
    mono = np.mean(np.abs(stereo), axis=1)
    win = int(.070 * SR); rel = int(.350 * SR)
    e = np.convolve(mono, np.ones(win)/win, "same")
    e = (e > .012).astype(np.float32)
    e = np.convolve(e, np.ones(rel)/rel, "same")
    return np.clip(e, 0, 1)


def place(dst, src, start):
    i = int(start * SR); n = len(src)
    if i < 0:
        src = src[-i:]; n = len(src); i = 0
    if i + n > len(dst):
        src = src[:len(dst)-i]; n = len(src)
    if n > 0: dst[i:i+n] += src


def build_full_mix(voice_results, song_results, out_dir: Path) -> Path:
    voice_audio = [read_audio(Path(v["audio_file"])) for v in voice_results]
    song_audio = [read_audio(Path(s["file"])) for s in song_results]
    timeline = []
    t = 0.0
    # Host 1 over beginning of song 1; each later host starts over tail of previous song / pre-roll into next.
    for i in range(4):
        vdur = len(voice_audio[i]) / SR
        timeline.append(("voice", i, t))
        song_start = t + max(1.0, vdur - 4.0)
        timeline.append(("song", i, song_start))
        t = song_start + SONG_SECONDS - 5.0  # next host comes over the tail
    # final elder outro over last song tail
    final_vdur = len(voice_audio[4]) / SR
    final_start = t
    timeline.append(("voice", 4, final_start))
    total = final_start + final_vdur + 2.0
    N = int(total * SR)
    music_bus = np.zeros((N,2), np.float32); voice_bus = np.zeros((N,2), np.float32)
    for kind, idx, start in timeline:
        if kind == "song": place(music_bus, song_audio[idx], start)
        else: place(voice_bus, voice_audio[idx], start)
    # Music fades and ducks under speech.
    gain = np.ones(N, np.float32)
    # detect voice and sidechain duck music under it
    duck = 1 - .70 * voice_env(voice_bus)
    gain *= duck
    # global fade in/out
    fi = int(2.5*SR); fo = int(8*SR)
    gain[:fi] *= np.linspace(.3,1,fi)
    gain[-fo:] *= np.linspace(1,.15,fo)
    music_bus *= gain[:,None]
    # voice slightly above music + small echo
    mix = music_bus + voice_bus * .96
    d = int(.130 * SR)
    mix[d:,0] += voice_bus[:-d,0] * .055; mix[d:,1] += voice_bus[:-d,1] * .080
    mix = np.tanh(mix * 1.06); mix = mix/(np.max(np.abs(mix))+1e-9) * .94
    wav = out_dir / "FULL_five_hosts_four_songs_cosmic_wizard_journey.wav"
    sf.write(wav, mix, SR)
    mp3 = wav.with_suffix(".mp3")
    sh(["ffmpeg", "-y", "-i", str(wav), "-codec:a", "libmp3lame", "-q:a", "2", str(mp3)])
    return mp3


def main() -> None:
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = OUT_ROOT / ts
    out_dir.mkdir(parents=True, exist_ok=True)
    voice_results = render_voices(out_dir)
    song_results = [generate_song(s, out_dir) for s in SONGS]
    full = build_full_mix(voice_results, song_results, out_dir)
    report = {
        "ok": True,
        "structure": "host1_intro_song1_host2_intro_song2_host3_intro_song3_host4_intro_song4_host5_outro",
        "voice_backend": "official k2-fsa/OmniVoice Space voice design fallback",
        "music_backend": "local procedural synthetic demo beds while ComfyUI/ACE-Step endpoint is unavailable",
        "song_seconds_each": SONG_SECONDS,
        "voices": voice_results,
        "songs": song_results,
        "full_mix": str(full),
        "full_mix_probe": ffprobe(full),
        "full_mix_sha256": hashlib.sha256(full.read_bytes()).hexdigest(),
    }
    (out_dir / "FIVE_HOST_FOUR_SONG_JOURNEY_REPORT.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
