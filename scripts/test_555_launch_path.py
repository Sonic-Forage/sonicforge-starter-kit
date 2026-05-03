from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

failures: list[str] = []
evidence: dict[str, object] = {"routes": {}, "checks": []}


def fail(message: str) -> None:
    failures.append(message)


def check(condition: bool, message: str) -> None:
    evidence["checks"].append({"ok": bool(condition), "message": message})
    if not condition:
        fail(message)


def get_json(path: str) -> dict:
    res = client.get(path)
    evidence["routes"][path] = res.status_code
    check(res.status_code == 200, f"GET {path} returns 200")
    return res.json()


def post_json(path: str, payload: dict | None = None) -> dict:
    res = client.post(path, json=payload or {})
    evidence["routes"][f"POST {path}"] = res.status_code
    check(res.status_code == 200, f"POST {path} returns 200")
    return res.json()


def assert_safe_flags(name: str, payload: dict, *, require_upload_flag: bool = False) -> None:
    for key in ["starts_gpu", "starts_paid_api", "publishes_stream", "records_audio"]:
        check(payload.get(key) is False, f"{name}: {key}=false")
    if require_upload_flag:
        check(payload.get("uploads_private_media") is False, f"{name}: uploads_private_media=false")


# Static/UI routes
for route in ["/", "/about", "/vanta", "/station", "/parallel-party", "/setup", "/agents", "/workflows", "/terminal-visuals", "/visualizer"]:
    res = client.get(route)
    evidence["routes"][route] = res.status_code
    check(res.status_code == 200, f"GET {route} returns 200")

index = client.get("/").text
visualizer = client.get("/visualizer").text
for needle in [
    "Intergalactic DJs is the team. SonicForge Live is the universe. DJ VANTA is the first clone.",
    "collective-ecosystem-strip",
    "ecosystemRoleList",
    "Plan Next Continuous Segment",
    "Text-first MC break generator",
    "Program audio truth panel",
    "Provider lanes stay closed until a human says yes",
]:
    check(needle in index, f"index contains UI needle: {needle}")
for needle in ["asic_code_spell", "ASIC code spell", "INTERGALACTIC DJ ASIC-CODE VISUAL SPELL", "browser-only shader illusion"]:
    check(needle in visualizer, f"visualizer contains UI needle: {needle}")

# API route and safety checks
health = get_json("/health")
check(health["ok"] is True, "health ok")
check(all(v is False for v in health["approval_flags"].values()), "all health approval flags false by default")

ecosystem = get_json("/api/ecosystem")
check(ecosystem["status"] == "forkable_collective_ecosystem_map_read_only", "ecosystem status correct")
check("Intergalactic DJs" in ecosystem["positioning"], "ecosystem positions Intergalactic DJs first")
check(any(path["id"] == "custom_model_training" for path in ecosystem["builder_paths"]), "ecosystem includes gated custom model training path")
check(ecosystem["trains_models"] is False, "ecosystem trains_models=false")
assert_safe_flags("ecosystem", ecosystem, require_upload_flag=True)

backends = get_json("/api/backends")
check(len(backends["lanes"]) >= 7, "backend status includes expected provider lanes")
check(all(lane["state"] == "closed_until_human_yes" for lane in backends["lanes"]), "all backend lanes closed by default")
assert_safe_flags("backends", backends, require_upload_flag=True)

program = get_json("/api/program-status")
check(program["status"] == "honest_program_status_mock_audio_no_rendered_program", "program status is honest no rendered program")
assert_safe_flags("program", program, require_upload_flag=True)

mc = get_json("/api/mc-breaks/preview")
check(set(mc["modes"].keys()) == {"survival", "history", "hype", "lore", "technical"}, "MC preview exposes all five modes")
assert_safe_flags("mc", mc, require_upload_flag=True)
for mode, item in mc["modes"].items():
    check(item["tts_status"] == "text_first_no_audio_output", f"MC mode {mode} stays text-first")
    check(item["sends_voice_message"] is False, f"MC mode {mode} sends_voice_message=false")
    check(item["records_audio"] is False, f"MC mode {mode} records_audio=false")

brain = get_json("/api/dj-brain/state")
check(brain["honest_status"] == "read_only_preview_no_generation_no_continuous_mixer", "DJ brain is read-only preview")
assert_safe_flags("dj_brain", brain, require_upload_flag=True)

# Safe interactions
guide = post_json("/api/guide", {"guide": "Test launch path: 128 BPM cyber-rave, safe forkable collective framing.", "bpm": 128, "energy": 7, "mode": "build"})
check(guide["type"] == "state.updated", "guide update event returned")

segment = post_json("/api/next-segment")
payload = segment["payload"]
for key in ["track", "talk", "visual", "mix", "transition", "deck_a", "deck_b", "visual_spell", "comfyui_visual_spell", "crate_selection", "survival_kit", "culture_cue", "mc_break", "program_status", "program_manifest"]:
    check(key in payload, f"next segment payload contains {key}")
check(payload["comfyui_visual_spell"]["mode"] == "dry_run", "next segment ComfyUI spell stays dry_run")
check(payload["program_status"]["status"] == "honest_program_status_mock_audio_no_rendered_program", "next segment program status remains honest")

for pad in ["VANTA", "HYDRATE", "BUDDY", "DROP", "PORTAL", "CHILL", "AIRHORN", "RECORD"]:
    event = post_json("/api/sample-pad", {"pad": pad})
    p = event["payload"]
    check(p["audio_cue"] == "metadata_only_no_audio_playback", f"sample pad {pad} is metadata-only")
    check(p["starts_gpu"] is False and p["publishes_stream"] is False, f"sample pad {pad} safe flags false")

timeline = get_json("/api/timeline")
check(timeline["status"] == "local_plan_only_fail_closed", "timeline GET fail-closed")
assert_safe_flags("timeline", timeline, require_upload_flag=True)
built_timeline = post_json("/api/timeline/build")
check(built_timeline["status"] == "local_plan_only_fail_closed", "timeline build fail-closed")
assert_safe_flags("timeline_build", built_timeline, require_upload_flag=True)

signal = post_json("/api/signal/acquire", {"station": "local", "provider": "mock", "duration_minutes": 10})
check(signal.get("starts_gpu") is False and signal.get("starts_paid_api") is False and signal.get("publishes_stream") is False, "station acquire is safe")
session = post_json("/api/signal/session", {"station": "local", "minutes": 10, "theme": "launch test"})
check(session.get("starts_gpu") is False and session.get("starts_paid_api") is False and session.get("publishes_stream") is False, "station session is safe")

# Blocked-action enforcement
for blocked_path in ["/api/comfy/prompt", "/api/model-download", "/api/stream/publish", "/api/record", "/api/upload"]:
    res = client.post(blocked_path, json={})
    evidence["routes"][f"POST {blocked_path}"] = res.status_code
    check(res.status_code == 403, f"POST {blocked_path} blocked with 403")
    body = res.json()
    check(body.get("status") == "blocked_by_server_enforced_fail_closed_policy", f"{blocked_path} blocked by fail-closed policy")

# External docs exist
for path in ["docs/product/INTERGALACTIC_DJS_COLLECTIVE_ECOSYSTEM.md", "docs/testing/HOW_TO_TEST_555_LAUNCH.md", "docs/planning/LAUNCH_555_PACIFIC_CHECKLIST.md"]:
    check((ROOT / path).exists(), f"doc exists: {path}")

out = ROOT / "site" / "data" / "555-launch-test-report.json"
out.parent.mkdir(parents=True, exist_ok=True)
evidence["ok"] = not failures
evidence["failure_count"] = len(failures)
evidence["failures"] = failures
out.write_text(json.dumps(evidence, indent=2), encoding="utf-8")

if failures:
    print(json.dumps(evidence, indent=2))
    raise SystemExit(1)
print(json.dumps({"ok": True, "checks": len(evidence["checks"]), "routes": evidence["routes"], "report": str(out)}, indent=2))
