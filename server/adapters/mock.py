from __future__ import annotations
import math, wave, struct, time
from pathlib import Path
from server.schemas import TrackBrief, TalkBreak, VisualCue, StreamPlan

AUDIO_DIR = Path('generated/audio')

class MockMusicAdapter:
    name = 'mock-local-wav'

    async def generate(self, brief: TrackBrief) -> dict:
        AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        safe = ''.join(ch.lower() if ch.isalnum() else '-' for ch in brief.title).strip('-') or 'track'
        path = AUDIO_DIR / f'{int(time.time())}-{safe}.wav'
        sample_rate = 44100
        seconds = min(max(brief.duration_seconds, 5), 30)
        # Tempo-coded test sketch: not a finished song, but a real local audio artifact for mixer tests.
        base = 55 + (brief.bpm - 60) * 0.7
        with wave.open(str(path), 'w') as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(sample_rate)
            for i in range(sample_rate * seconds):
                t = i / sample_rate
                beat = 1.0 if int(t * brief.bpm / 60 * 4) % 4 == 0 else 0.55
                env = min(1.0, t / 0.4) * min(1.0, (seconds - t) / 0.8)
                kick = math.sin(2*math.pi*(base*0.75)*t) * (0.35 if beat > 0.9 else 0.04)
                bass = math.sin(2*math.pi*base*t) * 0.22
                lead = math.sin(2*math.pi*(base*4.0)*t + math.sin(t*2.0)) * 0.08
                val = max(-1, min(1, (kick + bass + lead) * env * beat))
                frame = struct.pack('<hh', int(val * 32767), int(val * 32767))
                w.writeframesraw(frame)
        return {'ok': True, 'adapter': self.name, 'file': str(path), 'duration_seconds': seconds, 'bpm': brief.bpm, 'note': 'mock audio sketch for local routing tests'}

class MockTTSAdapter:
    name = 'mock-text-talk-break'

    async def speak(self, talk: TalkBreak) -> dict:
        return {'ok': True, 'adapter': self.name, 'text': talk.text, 'seconds': talk.seconds, 'duck_music_db': talk.duck_music_db, 'note': 'text-only talk cue; real TTS is opt-in'}

class MockVisualAdapter:
    name = 'browser-vj-canvas'

    async def cue(self, visual: VisualCue) -> dict:
        return {'ok': True, 'adapter': self.name, 'visual': visual.model_dump(), 'output_url': '/visualizer'}

class DryRunStreamAdapter:
    name = 'ffmpeg-rtmp-dry-run'

    async def plan(self, plan: StreamPlan) -> dict:
        warnings = []
        if plan.target_kind == 'rtmp' and not plan.publishes_stream:
            warnings.append('RTMP target requested but publishes_stream=false; staying dry-run.')
        return {'ok': True, 'adapter': self.name, 'plan': plan.model_dump(), 'warnings': warnings, 'note': 'no ffmpeg process started'}
