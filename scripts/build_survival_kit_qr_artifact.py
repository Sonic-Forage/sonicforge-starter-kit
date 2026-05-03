#!/usr/bin/env python3
"""Build a verified Intergalactic Rave Survival Kit QR prop-art card.

Local-only artifact generator: no network, no ComfyUI, no providers.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import cv2
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "survival-kit-qr"
PAYLOAD_PATH = OUT / "intergalactic-rave-survival-kit-payload.txt"
CLEAN_QR_PATH = OUT / "intergalactic-rave-survival-kit-clean-qr.png"
POSTER_PATH = OUT / "intergalactic-rave-survival-kit-card.png"
MANIFEST_PATH = OUT / "intergalactic-rave-survival-kit-manifest.json"

PAYLOAD = """Intergalactic DJs // Rave Survival Kit
DJ VANTA + SonicForge Live

Community-care checklist:
- Water station visible
- Earplugs / listening breaks
- Buddy check + meet-up point
- Ask before touch/filming
- Chill zone + clear exits
- Sober human override ready

Scope: community-care reminder only; not medical/legal/drug-use advice.
""".strip()

SAFE_FLAGS = {
    "starts_gpu": False,
    "starts_paid_api": False,
    "publishes_stream": False,
    "records_audio": False,
    "uploads_private_media": False,
    "requires_human_approval_before_public_use": True,
}


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def generate_clean_qr() -> Image.Image:
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=16, border=4)
    qr.add_data(PAYLOAD)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img.save(CLEAN_QR_PATH)
    return img


def decode(path: Path) -> str:
    img = cv2.imread(str(path))
    data, _pts, _straight = cv2.QRCodeDetector().detectAndDecode(img)
    return data


def draw_wrapped(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, width: int, fnt: ImageFont.ImageFont, fill, line_gap: int = 8):
    x, y = xy
    line = ""
    for word in text.split():
        test = (line + " " + word).strip()
        if draw.textbbox((0, 0), test, font=fnt)[2] <= width:
            line = test
        else:
            draw.text((x, y), line, font=fnt, fill=fill)
            y += fnt.size + line_gap
            line = word
    if line:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


def make_poster(qr_img: Image.Image) -> None:
    W, H = 1600, 2200
    base = Image.new("RGB", (W, H), (236, 226, 202))
    d = ImageDraw.Draw(base, "RGBA")

    # scanned-paper gradient/noise texture
    for y in range(0, H, 4):
        tint = int(10 * (y / H))
        d.rectangle([0, y, W, y + 4], fill=(236 - tint, 226 - tint, 202 - tint, 255))
    for i in range(420):
        x = (i * 137) % W
        y = (i * 283) % H
        r = 1 + (i % 4)
        d.ellipse([x, y, x + r, y + r], fill=(48, 35, 28, 18))

    # neon poster fields around QR, not over QR
    d.rounded_rectangle([70, 70, W - 70, H - 70], radius=38, outline=(28, 18, 36, 240), width=8)
    d.rounded_rectangle([105, 110, W - 105, 520], radius=26, fill=(18, 9, 38, 235), outline=(255, 43, 214, 230), width=5)
    d.text((145, 145), "INTERGALACTIC DJs", font=font(88, True), fill=(255, 242, 180, 255))
    d.text((150, 252), "RAVE SURVIVAL KIT", font=font(116, True), fill=(20, 245, 255, 255))
    d.text((154, 390), "DJ VANTA // SonicForge Live", font=font(46, True), fill=(255, 43, 214, 255))
    d.text((154, 455), "Hydrate · Earplugs · Buddy · Consent · Exits · Chill Zone", font=font(32), fill=(245, 245, 245, 230))

    # Clean mounted QR region with intact quiet zone.
    qr_size = 1020
    qx, qy = (W - qr_size) // 2, 645
    d.rounded_rectangle([qx - 55, qy - 55, qx + qr_size + 55, qy + qr_size + 55], radius=30, fill=(252, 248, 230, 255), outline=(16, 10, 35, 255), width=7)
    d.text((qx - 30, qy - 105), "SCAN THE SIGNAL — LOCAL CHECKLIST INSIDE", font=font(37, True), fill=(20, 12, 34, 255))
    base.paste(qr_img.resize((qr_size, qr_size), Image.Resampling.NEAREST), (qx, qy))

    # Decorative border glyphs and cue stamps outside the quiet zone.
    for i, label in enumerate(["SURVIVAL_PING", "HUMAN_OVERRIDE", "NO_AUTO_STREAM", "COMFYUI_DRY_RUN"]):
        y = 1725 + i * 72
        d.rounded_rectangle([145, y, W - 145, y + 48], radius=14, fill=(18, 9, 38, 218), outline=(20, 245, 255, 175), width=2)
        d.text((175, y + 8), label, font=font(27, True), fill=(255, 242, 180, 255))

    note = "Community-care reminder only. Not medical/legal/drug-use advice. If someone seems unsafe or distressed, pause the set and get sober humans / venue staff / emergency help as appropriate."
    draw_wrapped(d, (145, 2040), note, W - 290, font(30), (30, 20, 28, 255), 6)

    # scanner shadow after QR is pasted; avoids damaging modules.
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay, "RGBA")
    od.rectangle([0, 0, 35, H], fill=(0, 0, 0, 45))
    od.rectangle([W - 30, 0, W, H], fill=(0, 0, 0, 25))
    od.line([0, 612, W, 592], fill=(255, 255, 255, 24), width=3)
    base = Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")
    base.save(POSTER_PATH, quality=95)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    PAYLOAD_PATH.write_text(PAYLOAD + "\n", encoding="utf-8")
    clean = generate_clean_qr()
    make_poster(clean)
    clean_decoded = decode(CLEAN_QR_PATH)
    poster_decoded = decode(POSTER_PATH)
    ok = clean_decoded == PAYLOAD and poster_decoded == PAYLOAD
    manifest = {
        "schema": "sonicforge.survival_kit_qr_artifact.v1",
        "status": "verified_scannable" if ok else "decode_failed",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "purpose": "Intergalactic Rave Survival Kit QR prop-art card for local hackathon demo / house-party operator handout.",
        "payload_path": str(PAYLOAD_PATH.relative_to(ROOT)),
        "clean_qr_path": str(CLEAN_QR_PATH.relative_to(ROOT)),
        "poster_path": str(POSTER_PATH.relative_to(ROOT)),
        "decoded_payload_sha256_hint": "verify exact payload by OpenCV decode in scripts/verify_survival_kit_qr_artifact.py",
        "opencv_clean_decode_matches_payload": clean_decoded == PAYLOAD,
        "opencv_poster_decode_matches_payload": poster_decoded == PAYLOAD,
        "safe_scope": "community-care reminder only; not medical/legal/drug-use advice",
        **SAFE_FLAGS,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    if not ok:
        raise SystemExit("QR decode verification failed")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
