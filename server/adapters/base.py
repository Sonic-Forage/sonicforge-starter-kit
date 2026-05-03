from __future__ import annotations
from typing import Protocol
from server.schemas import TrackBrief, TalkBreak, VisualCue, StreamPlan

class MusicAdapter(Protocol):
    name: str
    async def generate(self, brief: TrackBrief) -> dict: ...

class TTSAdapter(Protocol):
    name: str
    async def speak(self, talk: TalkBreak) -> dict: ...

class VisualAdapter(Protocol):
    name: str
    async def cue(self, visual: VisualCue) -> dict: ...

class StreamAdapter(Protocol):
    name: str
    async def plan(self, plan: StreamPlan) -> dict: ...
