from __future__ import annotations
import math

from server.crate_cache import load_prompt_crate, select_crate_entry
from server.mc_breaks import build_mc_break
from server.schemas import (
    BeatmatchPlan,
    CrowdState,
    CrossfaderPlan,
    CrossfaderPoint,
    CuePoint,
    DeckState,
    EQMove,
    PhrasePlan,
    SetState,
    TalkBreak,
    TrackBrief,
    TransitionPlan,
    VisualCue,
)


def _bar_seconds(bpm: int) -> float:
    return round((60.0 / bpm) * 4.0, 3)


def _equal_power_point(value: float, note: str) -> CrossfaderPoint:
    normalized = (value + 1.0) / 2.0
    angle = normalized * math.pi / 2.0
    return CrossfaderPoint(
        value=round(value, 2),
        gain_a=round(math.cos(angle), 4),
        gain_b=round(math.sin(angle), 4),
        note=note,
    )


def _crossfader_plan() -> CrossfaderPlan:
    return CrossfaderPlan(
        automation=[
            _equal_power_point(-1.0, 'bar 1: Deck A full, Deck B preview/cued silently'),
            _equal_power_point(-0.5, 'bar 9: Deck B texture rises under Deck A'),
            _equal_power_point(0.0, 'bar 17: equal-power midpoint for bass swap'),
            _equal_power_point(0.5, 'bar 25: Deck B leads while Deck A tails'),
            _equal_power_point(1.0, 'bar 33: Deck B full, Deck A released'),
        ],
        notes=[
            'This is metadata only; no real continuous mixer is started.',
            'Equal-power keeps perceived loudness steadier than linear fades during the handoff.',
        ],
    )


def _talk_over_intro_ducking_plan(talk: TalkBreak, bpm: int) -> dict:
    """Describe how the MC break should sit over the intro without rendering audio.

    This is metadata for a future continuous mixer: no compressor, stem router,
    recorder, or program-audio renderer starts here.
    """
    talk_seconds = max(1, int(talk.seconds))
    release_seconds = 2
    bar_sec = _bar_seconds(bpm)
    return {
        'status': 'talk_over_intro_ducking_plan_metadata_only',
        'talk_over_intro_seconds': talk_seconds,
        'duck_music_db': talk.duck_music_db,
        'release_seconds': release_seconds,
        'target_clear_before_bar': 8,
        'bar_seconds': bar_sec,
        'automation': [
            {'at_seconds': 0.0, 'bar': 1, 'music_gain_db': talk.duck_music_db, 'mc_gain_db': 0.0, 'note': 'MC enters over Deck B intro; music bed ducks immediately.'},
            {'at_seconds': max(0.0, round(talk_seconds - release_seconds, 2)), 'bar': max(1, int((max(0, talk_seconds - release_seconds) / bar_sec) + 1)), 'music_gain_db': talk.duck_music_db, 'mc_gain_db': -1.5, 'note': 'Last words; keep duck steady and prepare release.'},
            {'at_seconds': float(talk_seconds), 'bar': min(8, max(1, int((talk_seconds / bar_sec) + 1))), 'music_gain_db': 0.0, 'mc_gain_db': -18.0, 'note': 'MC cleared; restore music before bass swap/drop impact.'},
        ],
        'sidechain_hint': 'future mixer: MC sidechain/volume automation only; no live renderer in this repo yet',
        'safe_scope': 'metadata only; records_audio=false, publishes_stream=false, no continuous mixer started',
        'starts_gpu': False,
        'starts_paid_api': False,
        'publishes_stream': False,
        'records_audio': False,
    }


def _eq_move_schedule(eq_moves: list[EQMove]) -> dict:
    """Return a readable EQ automation lane for LOW/MID/HIGH without mixing audio."""
    automation = [move.model_dump() for move in eq_moves]
    return {
        'status': 'eq_move_schedule_metadata_only_no_audio_mixer',
        'summary': 'LOW swap, MID carve, HIGH shimmer are transition notes only until a verified mixer adapter renders audio.',
        'low_swap': 'Bar 17: outgoing lows down, incoming Deck B lows to unity for the bass handoff.',
        'mid_carve': 'Bars 9-17: open Deck B mids gradually while leaving room for the MC/talk cue.',
        'high_shimmer': 'Bars 1-33: hats/noise shimmer enters first, then settles as Deck B takes the lead.',
        'automation': automation,
        'operator_note': 'Copy this EQ move schedule into a future mixer/DAW only after human approval; SonicForge Live is not rendering EQ automation yet.',
        'starts_gpu': False,
        'starts_paid_api': False,
        'publishes_stream': False,
        'records_audio': False,
        'requires_human_approval': True,
    }


def _recent_crate_ids_from_queue(state: SetState) -> list[str]:
    """Infer recent prompt crates from queued track metadata for repetition guard.

    TrackBrief does not have a dedicated crate_id field yet, so the planner
    writes the selected local crate id into future prompts and scans existing
    queue text. This keeps the guard file-backed and schema-compatible.
    """
    entries = load_prompt_crate().get('entries', [])
    known = [(str(e.get('id', '')), str(e.get('name', ''))) for e in entries]
    recent: list[str] = []
    for track in state.queue[-6:]:
        haystack = ' '.join([track.title, track.style, track.prompt, track.key]).lower()
        for crate_id, crate_name in known:
            if crate_id and (crate_id.lower() in haystack or crate_name.lower() in haystack):
                recent.append(crate_id)
                break
    return recent


def _synthetic_crowd_state(state: SetState, track_energy: int) -> dict:
    """Map set mode/energy into DJ-readable crowd phases without sensors.

    The five states are intentionally plain-language for the UI: warmup,
    curious, locked-in, peak, and cooldown. This is not live crowd detection;
    it is deterministic rehearsal metadata for party-care and VJ pacing.
    """
    if state.mode in {'comedown', 'afterglow'}:
        phase = 'cooldown'
        intervention = 'chill_zone'
        palette = 'soft amber/cyan, lower contrast, no strobe'
        note = 'Downshift intensity; point people toward water, exits, chill zone, and ride-home/buddy checks.'
    elif state.mode == 'warmup' and track_energy <= 4:
        phase = 'warmup'
        intervention = 'none'
        palette = 'low-fog cyan/black, generous negative space'
        note = 'Welcome arrivals, keep volume and visuals comfortable, and surface exits/chill-zone copy.'
    elif track_energy <= 4:
        phase = 'cooldown'
        intervention = 'chill_zone'
        palette = 'soft amber/cyan, lower contrast, no strobe'
        note = 'Downshift intensity; point people toward water, exits, chill zone, and ride-home/buddy checks.'
    elif state.mode == 'peak' or track_energy >= 9:
        phase = 'peak'
        intervention = 'hydration_reset'
        palette = 'ultraviolet/magenta with calm SURVIVAL_PING overlays, avoid harsh flashing'
        note = 'Keep peak-time care visible: hydration, air, ear protection, and sober human override.'
    elif state.mode == 'build' or track_energy >= 7:
        phase = 'locked-in'
        intervention = 'buddy_check'
        palette = 'cyan/magenta portal glow with phrase-lock accents'
        note = 'Room is engaged; maintain phrase discipline and slip in buddy-check microcopy.'
    elif state.mode == 'groove' or track_energy >= 5:
        phase = 'curious'
        intervention = 'earplug_ping'
        palette = 'blue-violet floor grid with inviting low-intensity motion'
        note = 'Invite the room deeper while reminding people to protect ears and respect space.'
    else:
        phase = 'warmup'
        intervention = 'none'
        palette = 'low-fog cyan/black, generous negative space'
        note = 'Welcome arrivals, keep volume and visuals comfortable, and surface exits/chill-zone copy.'
    return {
        'phase': phase,
        'intervention': intervention,
        'palette': palette,
        'note': note,
    }


def plan_transition(state: SetState, track: TrackBrief, talk: TalkBreak, visual: VisualCue) -> TransitionPlan:
    """Model the real DJ work behind a segment without rendering audio.

    The plan is deterministic, local, and honest: it describes beatmatching,
    phrasing, cueing, EQ, crowd read, talk-break, and VJ cue decisions for the
    later mixer/Resolume/TouchDesigner adapters to execute.
    """
    tempo_shift = round(((track.bpm - state.bpm) / state.bpm) * 100.0, 2)
    compatible = abs(tempo_shift) <= 4.0
    bar_sec = _bar_seconds(track.bpm)
    crowd_read = _synthetic_crowd_state(state, track.energy)
    phrase = PhrasePlan(
        intro_bars=16,
        mix_in_bar=1,
        bass_swap_bar=17,
        drop_release_bar=33,
        outro_bars=16,
    )
    return TransitionPlan(
        beatmatch=BeatmatchPlan(
            current_bpm=state.bpm,
            next_bpm=track.bpm,
            tempo_shift_percent=tempo_shift,
            compatible=compatible,
            notes=[
                'Keep master clock stable for the localhost demo.',
                'If tempo drift exceeds 4%, prefer phrase cut or energy reset instead of forced warp.',
            ],
        ),
        phrase=phrase,
        crossfader=_crossfader_plan(),
        eq_moves=[
            EQMove(bar=1, low_db=-18.0, mid_db=-2.0, high_db=1.5, filter='highpass', note='Introduce hats/texture over outgoing groove.'),
            EQMove(bar=9, low_db=-12.0, mid_db=0.0, high_db=1.0, filter='highpass', note='Open mids while confirming phrase alignment.'),
            EQMove(bar=17, low_db=0.0, mid_db=0.0, high_db=0.0, filter='none', note='Bass swap: outgoing lows down, incoming lows to unity.'),
            EQMove(bar=33, low_db=0.0, mid_db=1.0, high_db=1.0, filter='none', note='Release into drop; clear talk bed before impact.'),
        ],
        cue_points=[
            CuePoint(name='prelisten', bar=1, seconds=0.0, purpose='prelisten'),
            CuePoint(name='mix_in', bar=phrase.mix_in_bar, seconds=0.0, purpose='mix_in'),
            CuePoint(name='bass_swap', bar=phrase.bass_swap_bar, seconds=round((phrase.bass_swap_bar - 1) * bar_sec, 2), purpose='bass_swap'),
            CuePoint(name='drop_release', bar=phrase.drop_release_bar, seconds=round((phrase.drop_release_bar - 1) * bar_sec, 2), purpose='drop'),
            CuePoint(name='talk_clear', bar=8, seconds=float(talk.seconds), purpose='talk_out'),
        ],
        crowd=CrowdState(
            energy=track.energy,
            density=min(10, max(3, track.energy + 1)),
            response=crowd_read['phase'],
            synthetic_state=crowd_read['phase'],
            care_intervention=crowd_read['intervention'],
            visual_palette_hint=crowd_read['palette'],
            operator_note=f"Synthetic crowd read only; no live sensors. {crowd_read['note']}",
            observed_signal='synthetic set-state read only; no hidden mic/camera crowd recording',
        ),
        talk_break=talk,
        visual_cue=visual,
        summary=(
            f"{track.title}: {state.bpm}->{track.bpm} BPM, 16-bar blend, "
            f"bass swap on bar 17, VJ intensity {visual.intensity}, crowd {crowd_read['phase']}."
        ),
    )


def _survival_kit_cue(state: SetState, energy: int) -> dict:
    """Return one practical community-care cue for the next segment.

    Safe scope: reminders only. No medical claims, no drug-use instructions, and
    no substitution for sober human operators or emergency services.
    """
    if energy >= 8:
        mode = 'hydration'
        message = 'Cool-down orbit: water, air, bathroom, buddy check. Then we launch again.'
        priority = 'medium'
    elif state.mode in {'comedown', 'afterglow'}:
        mode = 'chill_zone'
        message = 'Rest is part of the ritual. Step out, sit down, breathe slow, come back when ready.'
        priority = 'low'
    else:
        mode = 'buddy_check'
        message = 'Intergalactic check-in: know your exits, protect your ears, ask before touch, and keep your crew accounted for.'
        priority = 'low'
    return {
        'mode': mode,
        'priority': priority,
        'message': message,
        'visual_spell': f'SURVIVAL_PING {mode.upper()}',
        'checklist': ['water station', 'earplugs', 'buddy check', 'exits clear', 'chill zone', 'human override'],
        'requires_human': False,
        'human_override': 'If someone seems distressed or unsafe, pause the set and alert sober humans/venue staff/emergency help as appropriate.',
        'safe_scope': 'community-care reminder only; not medical/legal/drug-use advice',
    }


def _culture_cue(state: SetState, n: int) -> dict:
    """Return a respectful lineage cue for short in-app talk breaks."""
    cues = [
        {
            'mode': 'history',
            'lineage': 'disco-house-techno-rave-vj-ai',
            'message': 'Respect to the selectors and sound systems that taught machines how to move.',
        },
        {
            'mode': 'safety',
            'lineage': 'community-care-sound-system-culture',
            'message': 'Intergalactic DJs rule one: the party is only alive if the people are okay.',
        },
        {
            'mode': 'lore',
            'lineage': 'warehouse-dust-browser-visuals-autonomous-dj',
            'message': 'This is not just a drop. It is a handoff: Deck A to Deck B, past to future, human to machine and back again.',
        },
    ]
    cue = cues[(n - 1) % len(cues)].copy()
    cue.update({
        'respect_note': 'AI is a guest in dance-music culture; keep history, consent, care, and human override visible.',
        'source_docs': ['docs/culture/RAVE_DJ_HISTORY_GUIDE.md', 'docs/features/HARM_REDUCTION_GUIDE.md'],
        'talk_break_mode': cue['mode'],
        'ui_drawer': 'Lineage + Rave Survival Kit',
    })
    return cue


def plan_next_segment(state: SetState) -> dict:
    """Create the next clean autonomous DJ segment from the current guide/state.

    This is deterministic and local-first. Later the same contract can call an LLM,
    but the shape should stay stable for the mixer/visual/stream lanes.
    """
    n = len(state.queue) + 1
    energy = min(10, max(1, state.energy + (1 if state.mode in {'build', 'peak'} else 0)))
    survival_kit = _survival_kit_cue(state, energy)
    culture_cue = _culture_cue(state, n)
    bpm = state.bpm
    recent_crate_ids = _recent_crate_ids_from_queue(state)
    crate_selection = select_crate_entry(state.mode, bpm, energy, recent_crate_ids=recent_crate_ids)
    crate_prompts = crate_selection.get('prompt_stack', [])
    crate_tags = ', '.join(crate_selection.get('genre_tags', [])) or state.mode
    title = f"{state.mode.title()} Signal {n:02d}"
    style = (
        f"{state.mode} cyber-rave DJ tool, {bpm} BPM, clean 16-bar intro, "
        f"sidechained bass, clear outro tail, club mix polish, crate tags: {crate_tags}"
    )
    prompt_parts = [state.guide, 'Make this segment mixable: intro/outro, stable tempo, no muddy master.', f"Selected local crate id: {crate_selection.get('id', 'local-seed')}"] + crate_prompts
    prompt = "\n".join(p for p in prompt_parts if p)
    track = TrackBrief(title=title, bpm=bpm, duration_seconds=18, style=style, energy=energy, prompt=prompt, key=crate_selection.get('key_hint', 'A minor'))
    mc_break = build_mc_break(state, segment_number=n)
    talk = mc_break['talk']
    visual = VisualCue(
        scene=f"{state.mode} {state.current_visual.scene} with waveform gates and neon crowd ghosts",
        palette=state.current_visual.palette,
        intensity=energy,
        output_mode='browser_window',
    )
    talk_ducking_plan = _talk_over_intro_ducking_plan(talk, bpm)
    transition = plan_transition(state, track, talk, visual)
    eq_schedule = _eq_move_schedule(transition.eq_moves)
    mix = {
        'crossfade_seconds': 8,
        'talk_over_intro_seconds': talk.seconds,
        'duck_music_db': talk.duck_music_db,
        'talk_over_intro_ducking_plan': talk_ducking_plan,
        'eq_move_schedule': eq_schedule,
        'target_lufs': -14,
        'beatmatch': 'stable-grid local plan; no timestretch renderer started',
        'phrase_bars': 'mix in 1, bass swap 17, release 33',
        'crossfader_curve': {
            'curve': 'equal_power',
            'formula': 'gainA = cos((value + 1) / 2 * PI / 2); gainB = sin((value + 1) / 2 * PI / 2)',
            'automation_bars': [1, 9, 17, 25, 33],
            'status': 'metadata_only_no_continuous_mixer_started',
        },
        'deck_roles': 'Deck A is the current groove; Deck B is the incoming portal queued for the next transition.',
        'notes': [
            'Track should have clean intro/outro for beatmatching.',
            'Talk cue sits over intro with ducking, then clears before drop.',
            'Future mixer adapter renders continuous program output.'
        ]
    }
    spell_text = crate_selection.get('visual_spell_text') or f'PHRASE_LOCK 32 // BASS_SWAP BAR_17 // {title.upper()}'
    comfy_prompt = (
        'readable neon typography, ASCII spectrograph star gate, DJ VANTA signal, '
        f'words {spell_text}, {state.mode} energy {energy}, underground rave flyer grain, '
        'clear survival/culture text overlay, browser-first VJ cue'
    )
    routing_contracts = {
        'browser': {
            'adapter': 'browser_visualizer',
            'mode': 'active_local_fallback',
            'route': '/visualizer',
            'scene': 'code_rain_transmission',
            'modes': ['code_rain', 'eq_bands', 'subtitle_spell', 'dual_ascii_spectrograph'],
            'text_overlay': spell_text,
            'survival_overlay': survival_kit['visual_spell'],
            'starts_gpu': False,
            'starts_paid_api': False,
            'publishes_stream': False,
            'records_audio': False,
        },
        'resolume': {
            'adapter': 'resolume_contract',
            'mode': 'dry_run',
            'composition': 'Intergalactic DJs / DJ VANTA / Resolume dry-run',
            'layer': 'Deck B Visual Spell',
            'clip_or_source': 'browser_visualizer_code_rain',
            'effect': 'glow_feedback_chromatic_split',
            'bpm': bpm,
            'palette': state.current_visual.palette,
            'text_overlay': spell_text,
            'survival_overlay': survival_kit['visual_spell'],
            'crossfader_hint': 'equal_power bar 17 midpoint',
            'route': 'manual_operator_copy_to_resolume_or_future_mcp',
            'starts_gpu': False,
            'starts_paid_api': False,
            'publishes_stream': False,
            'records_audio': False,
            'requires_human_approval': True,
        },
        'touchdesigner': {
            'adapter': 'touchdesigner_contract',
            'mode': 'dry_run',
            'network': '/project1/sonicforge_visual_spell',
            'operator_family': 'TOP/CHOP/DAT',
            'scene': 'code_rain_transmission',
            'text_overlay': f"{spell_text} // {survival_kit['visual_spell']}",
            'uniforms': {
                'uBpm': bpm,
                'uEnergy': energy,
                'uDeck': 'B',
                'uPhraseLockBars': 32,
                'uBassSwapBar': 17,
            },
            'route': 'manual_operator_copy_to_touchdesigner_or_future_twozero_mcp',
            'spout_syphon_hint': 'send TOP out to OBS/Resolume only after operator approval',
            'starts_gpu': False,
            'starts_paid_api': False,
            'publishes_stream': False,
            'records_audio': False,
            'requires_human_approval': True,
        },
        'comfyui': {
            'adapter': 'comfyui_dry_run',
            'mode': 'dry_run',
            'workflow': 'intergalactic-djs-visual-spell',
            'api_routes_when_enabled': ['/system_stats', '/object_info', '/prompt', '/ws', '/history/{prompt_id}', '/view'],
            'prompt_id': None,
            'files': [],
            'starts_gpu': False,
            'starts_paid_api': False,
            'publishes_stream': False,
            'records_audio': False,
            'requires_human_approval': True,
        },
    }
    visual_spell = {
        'type': 'visual.spell',
        'workflow': 'intergalactic-djs-visual-spell',
        'mode': 'dry_run',
        'deck': 'B',
        'scene': 'code_rain_transmission',
        'text': spell_text,
        'prompt': comfy_prompt,
        'negative_prompt': 'illegible typography, watermark, extra logos, fake QR code, brand logos',
        'route_targets': ['browser', 'resolume_contract', 'touchdesigner_contract', 'comfyui_dry_run'],
        'routing_contracts': routing_contracts,
        'starts_gpu': False,
        'starts_paid_api': False,
        'publishes_stream': False,
        'records_audio': False,
        'requires_human_approval': True,
        'warnings': ['ComfyUI/Resolume/TouchDesigner are not called; dry-run cue packet only.'],
    }
    comfyui_visual_spell = {
        'ok': True,
        'type': 'comfyui.visual_spell.cue',
        'mode': 'dry_run',
        'workflow': 'intergalactic-djs-visual-spell',
        'deck': 'B',
        'segment_id': f'segment-{n:03d}',
        'client_route': 'COMFYUI_DRY_RUN',
        'api_routes_when_enabled': ['/system_stats', '/object_info', '/prompt', '/ws', '/history/{prompt_id}', '/view'],
        'input': {
            'workflow': 'intergalactic-djs-visual-spell',
            'mode': 'dry_run',
            'deck': 'B',
            'segment_id': f'segment-{n:03d}',
            'prompt': comfy_prompt,
            'negative_prompt': visual_spell['negative_prompt'],
            'width': 1024,
            'height': 1024,
            'seed': 1776 + n,
            'output_prefix': f'vanta_visual_spell_segment_{n:03d}',
        },
        'output': {
            'prompt_id': None,
            'files': [],
            'warnings': ['ComfyUI /prompt is not called unless a human explicitly enables the backend.'],
        },
        'route_targets': ['browser_visualizer', 'comfyui_adapter_contract', 'touchdesigner_contract'],
        'starts_gpu': False,
        'starts_paid_api': False,
        'publishes_stream': False,
        'requires_human_approval': True,
        'safety': 'dry-run visual-spell cue only; no Comfy Cloud, local GPU job, model download, or public publishing starts from this planner output',
    }
    deck_a = DeckState(
        role='A',
        name='Deck A / current groove',
        status='playing',
        track=state.queue[-1] if state.queue else None,
        prompt_stack=[state.guide],
        bpm=state.bpm,
        key='A minor',
        energy=state.energy,
        gain=1.0,
        artifact_path=None,
        visual_spell={'scene': state.current_visual.scene, 'mode': 'browser_window'},
        safety_notes=['Current deck is mock/local state only; no live stream or provider is running.'],
    )
    deck_b = DeckState(
        role='B',
        name='Deck B / incoming portal',
        status='incoming',
        track=track,
        prompt_stack=[prompt, visual_spell['prompt']],
        bpm=track.bpm,
        key=track.key,
        energy=energy,
        gain=0.0,
        artifact_path=None,
        visual_spell=visual_spell,
        safety_notes=['Incoming deck is a local plan until the mock generator returns an artifact path.', f"Prompt crate: {crate_selection.get('name', 'local seed')} ({crate_selection.get('id', 'n/a')})"],
    )
    return {
        'track': track,
        'talk': talk,
        'visual': visual,
        'mix': mix,
        'transition': transition,
        'deck_a': deck_a,
        'deck_b': deck_b,
        'visual_spell': visual_spell,
        'comfyui_visual_spell': comfyui_visual_spell,
        'crate_selection': crate_selection,
        'survival_kit': survival_kit,
        'culture_cue': culture_cue,
        'mc_break': mc_break,
    }
