from __future__ import annotations
from datetime import datetime, timezone
from typing import Literal, Optional
from pydantic import BaseModel, Field

SetMode = Literal['warmup', 'groove', 'build', 'peak', 'comedown', 'afterglow']
EventType = Literal['state.updated', 'track.queued', 'track.generated', 'talk.queued', 'visual.updated', 'stream.plan', 'system.warning', 'system.ready']
DeckRole = Literal['A', 'B']
DeckStatus = Literal['idle', 'playing', 'incoming', 'queued', 'generated_mock', 'dry_run']

class TrackBrief(BaseModel):
    title: str = 'Untitled signal'
    bpm: int = Field(default=128, ge=60, le=180)
    key: str = 'A minor'
    duration_seconds: int = Field(default=24, ge=5, le=600)
    style: str = 'rave-cyberpunk electro house, clean DJ intro and outro'
    energy: int = Field(default=7, ge=1, le=10)
    prompt: str = 'neon festival drop, sidechained bass, metallic percussion'
    lyrics: str = ''

class BeatmatchPlan(BaseModel):
    current_bpm: int = Field(default=128, ge=60, le=180)
    next_bpm: int = Field(default=128, ge=60, le=180)
    tempo_shift_percent: float = Field(default=0.0, ge=-8.0, le=8.0)
    compatible: bool = True
    notes: list[str] = Field(default_factory=list)

class PhrasePlan(BaseModel):
    intro_bars: int = Field(default=16, ge=4, le=64)
    mix_in_bar: int = Field(default=1, ge=1, le=129)
    bass_swap_bar: int = Field(default=17, ge=1, le=129)
    drop_release_bar: int = Field(default=33, ge=1, le=129)
    outro_bars: int = Field(default=16, ge=4, le=64)

class EQMove(BaseModel):
    bar: int = Field(ge=1, le=129)
    low_db: float = Field(default=0.0, ge=-24.0, le=6.0)
    mid_db: float = Field(default=0.0, ge=-18.0, le=6.0)
    high_db: float = Field(default=0.0, ge=-18.0, le=6.0)
    filter: Literal['none', 'lowpass', 'highpass', 'bandpass'] = 'none'
    note: str = ''

class CuePoint(BaseModel):
    name: str
    bar: int = Field(ge=1, le=129)
    seconds: float = Field(ge=0.0, le=600.0)
    purpose: Literal['prelisten', 'mix_in', 'bass_swap', 'drop', 'talk_out', 'mix_out']

class CrowdState(BaseModel):
    energy: int = Field(default=5, ge=1, le=10)
    density: int = Field(default=5, ge=1, le=10)
    response: Literal['warmup', 'curious', 'locked-in', 'peak', 'cooldown'] = 'warmup'
    synthetic_state: Literal['warmup', 'curious', 'locked-in', 'peak', 'cooldown'] = 'warmup'
    care_intervention: Literal['none', 'earplug_ping', 'buddy_check', 'hydration_reset', 'chill_zone'] = 'none'
    visual_palette_hint: str = 'low-fog cyan/magenta, no strobe'
    operator_note: str = 'Synthetic crowd read only; no live microphone/camera crowd analysis running.'
    observed_signal: str = 'synthetic local demo crowd state; no live microphone analysis running'

class CrossfaderPoint(BaseModel):
    value: float = Field(ge=-1.0, le=1.0)
    gain_a: float = Field(ge=0.0, le=1.0)
    gain_b: float = Field(ge=0.0, le=1.0)
    note: str = ''

class CrossfaderPlan(BaseModel):
    curve: Literal['equal_power'] = 'equal_power'
    formula: str = 'gainA = cos((value + 1) / 2 * PI / 2); gainB = sin((value + 1) / 2 * PI / 2)'
    automation: list[CrossfaderPoint] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)

class TalkBreak(BaseModel):
    persona: str = 'DJ VANTA//SonicForge'
    text: str
    seconds: int = Field(default=8, ge=1, le=60)
    duck_music_db: float = Field(default=-8.0, ge=-30, le=0)

class VisualCue(BaseModel):
    scene: str = 'neon plasma tunnel'
    palette: str = 'black, cyan, magenta, ultraviolet'
    intensity: int = Field(default=7, ge=1, le=10)
    output_mode: Literal['browser_window', 'obs_capture', 'comfyui', 'touchdesigner_spout', 'resolume'] = 'browser_window'

class DeckState(BaseModel):
    role: DeckRole
    name: str
    status: DeckStatus = 'idle'
    track: Optional[TrackBrief] = None
    prompt_stack: list[str] = Field(default_factory=list)
    bpm: int = Field(default=128, ge=60, le=180)
    key: str = 'A minor'
    energy: int = Field(default=5, ge=1, le=10)
    gain: float = Field(default=0.0, ge=0.0, le=1.0)
    artifact_path: Optional[str] = None
    visual_spell: dict = Field(default_factory=dict)
    safety_notes: list[str] = Field(default_factory=list)

class TransitionPlan(BaseModel):
    beatmatch: BeatmatchPlan
    phrase: PhrasePlan
    crossfader: CrossfaderPlan
    eq_moves: list[EQMove]
    cue_points: list[CuePoint]
    crowd: CrowdState
    talk_break: TalkBreak
    visual_cue: VisualCue
    summary: str

class StreamPlan(BaseModel):
    target_kind: Literal['local_preview', 'obs_window_capture', 'rtmp', 'whip', 'srt', 'spout_resolume'] = 'local_preview'
    target_url: Optional[str] = None
    publishes_stream: bool = False
    notes: list[str] = Field(default_factory=list)

class SetState(BaseModel):
    entity: str = 'DJ VANTA//SonicForge'
    product: str = 'SonicForge Live'
    mode: SetMode = 'warmup'
    set_title: str = 'VantaRave Autopilot Session'
    guide: str = 'Start local, keep it clean, build toward a euphoric cyber-rave peak.'
    bpm: int = 128
    energy: int = 5
    current_visual: VisualCue = Field(default_factory=VisualCue)
    deck_a: DeckState = Field(default_factory=lambda: DeckState(role='A', name='Deck A / current groove', status='playing', gain=1.0))
    deck_b: DeckState = Field(default_factory=lambda: DeckState(role='B', name='Deck B / incoming portal', status='idle', gain=0.0))
    queue: list[TrackBrief] = Field(default_factory=list)
    last_talk: Optional[TalkBreak] = None
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class SonicEvent(BaseModel):
    type: EventType
    message: str
    payload: dict = Field(default_factory=dict)
    ts: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
