from __future__ import annotations

from server.schemas import SetState, TalkBreak

MC_BREAK_MODES = ['survival', 'history', 'hype', 'lore', 'technical']

MODE_SCRIPT_BANK = {
    'survival': {
        'label': 'Rave Survival Kit check-in',
        'text': 'Survival ping: water, earplugs, exits, buddy check, chill zone. If anything feels off, a sober human can stop the set.',
        'visual_spell': 'SURVIVAL_PING COMMUNITY_CARE',
    },
    'history': {
        'label': 'Lineage respect interlude',
        'text': 'Respect to the disco, house, techno, rave, sound-system, and VJ lineages. AI is a guest; humans made this culture move.',
        'visual_spell': 'LINEAGE_SIGNAL DISCO_HOUSE_TECHNO_RAVE',
    },
    'hype': {
        'label': 'Peak-room lift',
        'text': 'Intergalactic DJs, lock the phrase and watch Deck B open the portal. DJ VANTA is keeping it local, clean, and human-overridable.',
        'visual_spell': 'PHRASE_LOCK PORTAL_DROP',
    },
    'lore': {
        'label': 'DJ VANTA lore transmission',
        'text': 'DJ VANTA is the Virtual Autonomous Nocturnal Transmission Artist: Deck A to Deck B, browser light to room ritual, machine cue to human choice.',
        'visual_spell': 'VANTA_LORE SIGNAL_HANDOFF',
    },
    'technical': {
        'label': 'Transparent system note',
        'text': 'System note: this is a text-first MC break. TTS, recording, providers, streams, GPUs, and uploads remain closed until explicit human approval.',
        'visual_spell': 'SYSTEM_TRANSPARENT FAIL_CLOSED',
    },
}


def _pick_mode(state: SetState, requested_mode: str | None = None, segment_number: int | None = None) -> str:
    if requested_mode in MC_BREAK_MODES:
        return requested_mode
    if state.mode in {'comedown', 'afterglow'}:
        return 'survival'
    if state.mode == 'peak' or state.energy >= 8:
        return 'hype'
    if segment_number is not None:
        # Rotate the non-risky cultural/persona modes during normal planning.
        return ['history', 'hype', 'lore', 'technical'][(segment_number - 1) % 4]
    return 'history'


def build_mc_break(state: SetState, requested_mode: str | None = None, segment_number: int | None = None) -> dict:
    """Build a deterministic text-first MC break with all voice lanes closed.

    This generator produces copy and metadata only. It does not synthesize speech,
    record audio, send voice messages, call providers, upload private media, or
    start GPU/streaming backends.
    """
    mode = _pick_mode(state, requested_mode, segment_number)
    script = MODE_SCRIPT_BANK[mode]
    text = f"{script['text']} Mode {state.mode}, {state.bpm} BPM, energy {state.energy}."
    talk = TalkBreak(
        persona='DJ VANTA//SonicForge text-first MC',
        text=text,
        seconds=9 if mode in {'history', 'lore'} else 7,
        duck_music_db=-9.0 if mode != 'technical' else -6.0,
    )
    return {
        'mode': mode,
        'available_modes': MC_BREAK_MODES,
        'label': script['label'],
        'talk': talk,
        'text': text,
        'visual_spell': script['visual_spell'],
        'tts_status': 'text_first_no_audio_output',
        'adapter': 'mock-text-talk-break',
        'sends_voice_message': False,
        'voice_cloning_enabled': False,
        'starts_gpu': False,
        'starts_paid_api': False,
        'publishes_stream': False,
        'records_audio': False,
        'uploads_private_media': False,
        'requires_human_approval': True,
        'safe_scope': 'community-care and performance narration only; not medical/legal/drug-use advice',
        'human_override': 'Sober human operator may skip, edit, or stop the MC break before any live output.',
    }


def build_mc_break_preview(state: SetState) -> dict:
    return {
        'ok': True,
        'status': 'text_first_mc_break_generator_fail_closed',
        'modes': {mode: build_mc_break(state, requested_mode=mode) for mode in MC_BREAK_MODES},
        'starts_gpu': False,
        'starts_paid_api': False,
        'publishes_stream': False,
        'records_audio': False,
        'uploads_private_media': False,
        'requires_human_approval': True,
    }
