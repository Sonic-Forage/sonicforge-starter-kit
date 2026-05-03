from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site" / "data" / "playwright-555-visual-qa"
SCREEN = OUT / "screenshots"
SCREEN.mkdir(parents=True, exist_ok=True)
BASE = "http://127.0.0.1:8788"

report: dict[str, object] = {
    "ok": False,
    "base_url": BASE,
    "screenshots": {},
    "console": [],
    "checks": [],
    "errors": [],
    "safe_flags": {},
}


def check(condition: bool, message: str) -> None:
    report["checks"].append({"ok": bool(condition), "message": message})
    if not condition:
        report["errors"].append(message)


def shot(page, name: str) -> None:
    path = SCREEN / f"{name}.png"
    page.screenshot(path=str(path), full_page=True)
    report["screenshots"][name] = str(path)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
    page.on("console", lambda msg: report["console"].append({"type": msg.type, "text": msg.text}))
    page.on("pageerror", lambda exc: report["console"].append({"type": "pageerror", "text": str(exc)}))

    page.goto(BASE + "/", wait_until="networkidle")
    shot(page, "01_home_loaded")
    check(page.locator("#collective-ecosystem-strip").is_visible(), "collective ecosystem strip visible")
    check("Intergalactic DJs is the team" in page.locator("body").inner_text(), "collective first headline rendered")
    check(page.locator("#ecosystemRoleList article").count() >= 5, "ecosystem roles rendered from /api/ecosystem")
    check(page.locator("#backendStatusList article").count() >= 7, "backend status lanes rendered")
    check(page.locator("#mcBreakPreview article").count() >= 1, "MC preview rendered")

    page.select_option("#cultureModeSelect", "hype")
    page.click("#applyCultureMode")
    time.sleep(0.25)
    shot(page, "02_culture_hype_preview")
    check("hype" in page.locator("#cultureMessage").inner_text().lower(), "culture mode selector updates hype preview")
    check(("text-first" in page.locator("#mcBreakStatus").inner_text()) or ("text_first" in page.locator("#mcBreakStatus").inner_text()), "MC status says text-first/fail-closed")

    page.click("#nextSegment")
    page.wait_for_timeout(800)
    shot(page, "03_next_segment_planned")
    body = page.locator("body").inner_text()
    check("generated_mock" in body, "Deck B generated_mock/dry-run status visible after next segment")
    check("honest_program_status_mock_audio_no_rendered_program" in body, "program truth status visible after next segment")
    check("ComfyUI" in body and "dry-run" in body, "ComfyUI dry-run copy visible")

    for pad in ["HYDRATE", "BUDDY", "DROP", "PORTAL", "CHILL"]:
        page.click(f"button[data-pad='{pad}']")
        page.wait_for_timeout(250)
        text = page.locator("#samplePadStatus").inner_text()
        check(pad in text, f"sample pad {pad} updates status")
    shot(page, "04_sample_pads")

    page.click("#buildTimeline")
    page.wait_for_timeout(500)
    check(page.locator("#timelinePreview article").count() >= 3, "timeline preview renders three plans")
    check("local_plan_only" in page.locator("#autopilotStatus").inner_text(), "timeline remains local plan only")

    # Check JSON safety flags via browser context fetch, not direct Python client.
    safety = page.evaluate("""async () => {
      const endpoints = ['/health','/api/ecosystem','/api/backends','/api/program-status','/api/mc-breaks/preview','/api/dj-brain/state'];
      const out = {};
      for (const ep of endpoints) out[ep] = await fetch(ep).then(r => r.json());
      return out;
    }""")
    report["safe_flags"] = safety
    check(all(v is False for v in safety["/health"]["approval_flags"].values()), "browser fetch: all health approval flags false")
    check(safety["/api/ecosystem"]["trains_models"] is False, "browser fetch: ecosystem trains_models false")
    check(safety["/api/program-status"]["publishes_stream"] is False, "browser fetch: program publishes_stream false")
    check(safety["/api/backends"]["starts_gpu"] is False, "browser fetch: backends starts_gpu false")

    vis = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    vis.on("console", lambda msg: report["console"].append({"type": f"visualizer:{msg.type}", "text": msg.text}))
    vis.goto(BASE + "/visualizer", wait_until="networkidle")
    shot(vis, "05_visualizer_loaded")
    vis.click("button[data-mode='asic_code_spell']")
    vis.wait_for_timeout(1000)
    shot(vis, "06_visualizer_asic_code_spell")
    check("mode=asic_code_spell" in vis.locator("#vibe").inner_text(), "visualizer switches to ASIC code spell mode")
    check("ASIC_CODE_SPELL" in vis.locator("#spellHud").inner_text(), "visualizer HUD reflects ASIC_CODE_SPELL")

    # Fail-closed route check from browser context.
    blocked = page.evaluate("""async () => {
      const paths = ['/api/comfy/prompt','/api/model-download','/api/stream/publish','/api/record','/api/upload'];
      const out = {};
      for (const path of paths) {
        const r = await fetch(path, {method:'POST', headers:{'content-type':'application/json'}, body:'{}'});
        out[path] = {status: r.status, body: await r.json()};
      }
      return out;
    }""")
    report["blocked_routes"] = blocked
    for path, result in blocked.items():
        check(result["status"] == 403, f"browser fetch: {path} blocked 403")
        check(result["body"].get("status") == "blocked_by_server_enforced_fail_closed_policy", f"browser fetch: {path} blocked by fail-closed policy")

    browser.close()

# Treat only unexpected errors/pageerrors as blocking. The browser logs intentional
# fail-closed POST checks as "Failed to load resource: 403"; those are expected
# because the app must block Comfy prompts, downloads, stream, record, and uploads.
def is_expected_console_noise(m: dict[str, str]) -> bool:
    text = m.get("text", "")
    if "WebSocket" in text:
        return True
    if "Failed to load resource: the server responded with a status of 403" in text:
        return True
    return False

blocking_console = [m for m in report["console"] if m["type"] in {"error", "pageerror"} and not is_expected_console_noise(m)]
check(len(blocking_console) == 0, f"no unexpected browser console/page errors ({len(blocking_console)} found)")
report["blocking_console"] = blocking_console
report["ok"] = len(report["errors"]) == 0
report_path = OUT / "report.json"
report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps({"ok": report["ok"], "checks": len(report["checks"]), "errors": report["errors"], "report": str(report_path), "screenshots": report["screenshots"]}, indent=2))
if not report["ok"]:
    sys.exit(1)
