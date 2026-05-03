from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CRATE_PATH = ROOT / 'catalog' / 'crate-cache' / 'prompt-crate-seed.json'


@lru_cache(maxsize=1)
def load_prompt_crate() -> dict[str, Any]:
    """Load the local prompt/crate seed.

    This is deliberately file-backed and local-only: it never starts providers,
    downloads models, uploads media, or reaches out to a generation backend.
    """
    return json.loads(CRATE_PATH.read_text(encoding='utf-8'))


ENERGY_ARC_TARGETS = {
    'warmup': 5,
    'groove': 6,
    'build': 7,
    'peak': 9,
    'comedown': 4,
    'afterglow': 3,
}

GENRE_AFFINITY = {
    'warmup': {'deep house', 'techno', 'warehouse', 'PNW'},
    'groove': {'deep house', 'breaks', 'disco echo', 'techno'},
    'build': {'electro house', 'breaks', 'bass', 'cyber-rave'},
    'peak': {'techno', 'rave stabs', 'AI ritual', 'VJ code rain'},
    'comedown': {'breakbeat', 'ambient techno', 'afterglow', 'community-care'},
    'afterglow': {'downtempo', 'disco echo', 'history', 'warm closure'},
}


def _entry_id(entry: dict[str, Any]) -> str:
    return str(entry.get('id', ''))


def _genre_overlap(entry: dict[str, Any], mode: str) -> int:
    wanted = GENRE_AFFINITY.get(mode, set())
    tags = {str(tag) for tag in entry.get('genre_tags', [])}
    return len(wanted & tags)


def select_crate_entry(mode: str, bpm: int, energy: int, recent_crate_ids: list[str] | None = None) -> dict[str, Any]:
    """Choose a deterministic crate entry using genre, novelty, repetition guard, and energy arc.

    The selector is intentionally local and explainable. It does not randomize,
    call a provider, or hide any sensor inference: every score component is
    returned in ``crate_selection.score_breakdown`` for UI/demo inspection.
    """
    crate = load_prompt_crate()
    entries = list(crate.get('entries', []))
    if not entries:
        return {}

    recent = [str(x) for x in (recent_crate_ids or []) if x]
    recent_set = set(recent[-3:])
    target_energy = ENERGY_ARC_TARGETS.get(mode, energy)
    recent_genres = {
        str(tag)
        for entry in entries
        if _entry_id(entry) in recent_set
        for tag in entry.get('genre_tags', [])
    }

    def score(entry: dict[str, Any]) -> tuple[int, int, int, int, str]:
        entry_id = _entry_id(entry)
        repetition_penalty = 100 if entry_id in recent_set else 0
        mode_penalty = 0 if entry.get('mode') == mode else 12
        genre_bonus = _genre_overlap(entry, mode) * -3
        bpm_penalty = abs(int(entry.get('bpm', bpm)) - bpm)
        energy_penalty = abs(int(entry.get('energy', energy)) - target_energy) * 4
        novelty_bonus = -2 if not (set(entry.get('genre_tags', [])) & recent_genres) else 0
        return (
            repetition_penalty + mode_penalty + genre_bonus + novelty_bonus,
            energy_penalty,
            bpm_penalty,
            abs(int(entry.get('energy', energy)) - energy),
            entry_id,
        )

    selected = min(entries, key=score).copy()
    selected_id = _entry_id(selected)
    score_breakdown = {
        'mode': mode,
        'requested_bpm': bpm,
        'requested_energy': energy,
        'energy_arc_target': target_energy,
        'mode_match': selected.get('mode') == mode,
        'genre_overlap_count': _genre_overlap(selected, mode),
        'bpm_delta': abs(int(selected.get('bpm', bpm)) - bpm),
        'energy_delta_from_arc': abs(int(selected.get('energy', energy)) - target_energy),
        'recent_crate_ids_considered': recent[-3:],
        'repetition_guard_applied': selected_id in recent_set,
        'novelty_tags': [tag for tag in selected.get('genre_tags', []) if tag not in recent_genres],
        'selector': 'genre_novelty_repetition_guard_energy_arc_v1',
    }
    selected['selection_reason'] = (
        f"local prompt crate match for mode={mode}, bpm={bpm}, energy={energy}; "
        f"energy arc target={target_energy}; repetition guard checked {recent[-3:] or 'none'}; "
        "planning hint only, no provider call"
    )
    selected['score_breakdown'] = score_breakdown
    selected['energy_arc'] = {
        'target': target_energy,
        'requested': energy,
        'selected': int(selected.get('energy', energy)),
        'note': 'deterministic demo arc only; no live crowd sensor or provider call',
    }
    selected['repetition_guard'] = {
        'window': 3,
        'recent_crate_ids': recent[-3:],
        'avoids_immediate_repeats': True,
        'selected_was_recent': selected_id in recent_set,
    }
    selected['source'] = str(CRATE_PATH.relative_to(ROOT))
    selected['starts_gpu'] = False
    selected['starts_paid_api'] = False
    selected['publishes_stream'] = False
    return selected
