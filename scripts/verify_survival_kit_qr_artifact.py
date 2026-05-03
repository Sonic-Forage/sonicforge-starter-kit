#!/usr/bin/env python3
"""Verify the Intergalactic Rave Survival Kit QR artifact scans exactly."""
from __future__ import annotations

import json
from pathlib import Path

import cv2

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "survival-kit-qr"
PAYLOAD_PATH = OUT / "intergalactic-rave-survival-kit-payload.txt"
CLEAN_QR_PATH = OUT / "intergalactic-rave-survival-kit-clean-qr.png"
POSTER_PATH = OUT / "intergalactic-rave-survival-kit-card.png"
MANIFEST_PATH = OUT / "intergalactic-rave-survival-kit-manifest.json"

REQUIRED_TEXT = [
    "Community-care checklist",
    "Water station visible",
    "Earplugs / listening breaks",
    "Buddy check + meet-up point",
    "Ask before touch/filming",
    "Chill zone + clear exits",
    "Sober human override ready",
    "not medical/legal/drug-use advice",
]


def decode(path: Path) -> str:
    img = cv2.imread(str(path))
    if img is None:
        raise SystemExit(f"image not readable: {path}")
    data, _pts, _straight = cv2.QRCodeDetector().detectAndDecode(img)
    return data


def main() -> None:
    for path in [PAYLOAD_PATH, CLEAN_QR_PATH, POSTER_PATH, MANIFEST_PATH]:
        if not path.exists():
            raise SystemExit(f"missing QR artifact file: {path.relative_to(ROOT)}")
    payload = PAYLOAD_PATH.read_text(encoding="utf-8").strip()
    for needle in REQUIRED_TEXT:
        if needle not in payload:
            raise SystemExit(f"payload missing safe checklist text: {needle}")
    clean = decode(CLEAN_QR_PATH)
    poster = decode(POSTER_PATH)
    if clean != payload:
        raise SystemExit("clean QR does not decode to exact payload")
    if poster != payload:
        raise SystemExit("poster QR does not decode to exact payload")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("status") != "verified_scannable":
        raise SystemExit("manifest status is not verified_scannable")
    for key in ["starts_gpu", "starts_paid_api", "publishes_stream", "records_audio", "uploads_private_media"]:
        if manifest.get(key) is not False:
            raise SystemExit(f"manifest fail-closed flag is not false: {key}")
    if manifest.get("requires_human_approval_before_public_use") is not True:
        raise SystemExit("manifest missing human approval gate")
    print(json.dumps({
        "ok": True,
        "artifact": str(POSTER_PATH.relative_to(ROOT)),
        "clean_qr": str(CLEAN_QR_PATH.relative_to(ROOT)),
        "payload_chars": len(payload),
        "opencv_poster_decode_matches_payload": True,
        "starts_gpu": False,
        "starts_paid_api": False,
        "publishes_stream": False,
    }, indent=2))


if __name__ == "__main__":
    main()
