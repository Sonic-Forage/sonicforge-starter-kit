from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

SAFE_REQUIRED = [
    "community-care",
    "medical advice",
    "not medical/legal/drug-use advice",
    "human override",
    "hydration",
    "earplugs",
    "buddy",
    "exits",
    "chill zone",
    "consent",
]

FORBIDDEN_UNSAFE_PHRASES = [
    "recommended dose",
    "safe dose",
    "take more",
    "mix substances",
    "drug identification instructions",
    "how to use drugs",
    "ignore emergency",
    "do not call emergency",
    "diagnose the problem",
    "medical diagnosis",
    "substitute for emergency services",
]

DOC_PATHS = [
    ROOT / "docs/features/RAVE_SURVIVAL_KIT.md",
    ROOT / "docs/features/HARM_REDUCTION_GUIDE.md",
    ROOT / "docs/culture/RAVE_DJ_HISTORY_GUIDE.md",
]

UI_PATHS = [
    ROOT / "app/static/index.html",
    ROOT / "app/static/main.js",
]


def _read(path: Path) -> str:
    if not path.exists():
        print(f"missing required file: {path.relative_to(ROOT)}")
        sys.exit(1)
    return path.read_text(encoding="utf-8")


def _assert_contains(haystack: str, needle: str, label: str) -> None:
    if needle.lower() not in haystack.lower():
        print(f"{label} missing required survival/harm-reduction string: {needle}")
        sys.exit(1)


def _assert_absent(haystack: str, phrase: str, label: str) -> None:
    if phrase.lower() in haystack.lower():
        print(f"{label} contains unsafe phrase: {phrase}")
        sys.exit(1)


def main() -> None:
    docs = "\n".join(_read(p) for p in DOC_PATHS)
    ui = "\n".join(_read(p) for p in UI_PATHS)
    planner_text = _read(ROOT / "server/planner.py")
    main_text = _read(ROOT / "server/main.py")

    combined = "\n".join([docs, ui, planner_text, main_text])
    runtime_copy = "\n".join([ui, planner_text, main_text])
    for required in SAFE_REQUIRED:
        _assert_contains(combined, required, "survival copy")
    # Docs may name red-line topics as prohibited. Runtime/UI copy must not contain
    # instructional or diagnosis-style language that could be mistaken for advice.
    for phrase in FORBIDDEN_UNSAFE_PHRASES:
        _assert_absent(runtime_copy, phrase, "runtime survival copy")

    from server.planner import plan_next_segment  # noqa: E402
    from server.schemas import SetState  # noqa: E402
    from server.main import sample_pad  # noqa: E402
    import asyncio  # noqa: E402

    states = [
        SetState(mode="warmup", energy=3),
        SetState(mode="build", energy=7),
        SetState(mode="peak", energy=9),
        SetState(mode="comedown", energy=4),
    ]
    modes_seen: set[str] = set()
    for state in states:
        segment = plan_next_segment(state)
        survival = segment.get("survival_kit", {})
        culture = segment.get("culture_cue", {})
        modes_seen.add(str(survival.get("mode")))
        if not str(survival.get("visual_spell", "")).startswith("SURVIVAL_PING"):
            print("survival_kit visual spell must be a SURVIVAL_PING")
            sys.exit(1)
        if survival.get("requires_human") is not False:
            print("survival_kit should be a reminder cue, not an automated emergency actor")
            sys.exit(1)
        for flag_word in ["water", "earplugs", "buddy", "exits", "chill zone", "human override"]:
            if flag_word not in " ".join(survival.get("checklist", [])).lower():
                print(f"survival checklist missing {flag_word}")
                sys.exit(1)
        if "not medical/legal/drug-use advice" not in survival.get("safe_scope", ""):
            print("survival safe_scope missing no-medical/legal/drug-use boundary")
            sys.exit(1)
        if "emergency" not in survival.get("human_override", "").lower():
            print("survival human_override must route emergencies to humans/help")
            sys.exit(1)
        if "AI is a guest" not in culture.get("respect_note", ""):
            print("culture cue must preserve respectful lineage framing")
            sys.exit(1)

    if not {"buddy_check", "hydration", "chill_zone"}.issubset(modes_seen):
        print(f"expected buddy/hydration/chill survival modes, saw {sorted(modes_seen)}")
        sys.exit(1)

    for pad in ["HYDRATE", "BUDDY", "CHILL"]:
        event = asyncio.run(sample_pad({"pad": pad}))
        payload = event.payload
        if payload.get("talk_break_mode") != "survival":
            print(f"{pad} pad is not a survival talk-break mode")
            sys.exit(1)
        if not str(payload.get("visual_spell", "")).startswith("SURVIVAL_PING"):
            print(f"{pad} pad missing SURVIVAL_PING visual spell")
            sys.exit(1)
        for flag in ["starts_gpu", "starts_paid_api", "publishes_stream"]:
            if payload.get(flag) is not False:
                print(f"{pad} pad safety flag is not fail-closed: {flag}")
                sys.exit(1)
        if payload.get("audio_cue") != "metadata_only_no_audio_playback":
            print(f"{pad} pad should stay metadata-only, no audio playback")
            sys.exit(1)
        if "not medical/legal/drug-use advice" not in payload.get("safe_scope", ""):
            print(f"{pad} pad safe_scope missing boundary copy")
            sys.exit(1)

    print(json.dumps({
        "ok": True,
        "checked": "survival_harm_reduction_copy_and_runtime_cues",
        "docs_checked": [str(p.relative_to(ROOT)) for p in DOC_PATHS],
        "ui_checked": [str(p.relative_to(ROOT)) for p in UI_PATHS],
        "survival_modes_seen": sorted(modes_seen),
        "sample_pads_checked": ["HYDRATE", "BUDDY", "CHILL"],
        "closed_gates_verified": True,
    }, indent=2))


if __name__ == "__main__":
    main()
