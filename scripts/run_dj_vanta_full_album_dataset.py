#!/usr/bin/env python3
"""Generate the DJ VANTA synthetic album dataset through a ComfyUI ACE-Step workflow and upload to HF.

Secrets are loaded only from environment/.env and are never printed.
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import random
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("COMFYUI_BASE_URL", "").rstrip("/")
WORKFLOW_PATH = Path(os.environ.get("COMFYUI_WORKFLOW_JSON", "/opt/data/cache/documents/doc_1f34a705b083_acestep-api.json"))
QUEUE_PATH = Path(os.environ.get("SONICFORGE_QUEUE_JSONL", "datasets/synthetic_audio/dj-vanta-no-golden-ticket-required/prompts/generation_queue_v6_builder_mythology.jsonl"))
ALBUM_SLUG = "dj-vanta-no-velvet-rope-in-the-node-graph"
REPO_ID_DEFAULT = os.environ.get("HF_DATASET_REPO_ID", f"TheMindExpansionNetwork/{ALBUM_SLUG}-synthetic-audio")
DURATION_SECONDS = int(os.environ.get("SONICFORGE_AUDIO_DURATION", "120"))
BATCH_SIZE = 1
RUN_ID = os.environ.get("SONICFORGE_RUN_ID", dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOCAL_ALBUM_ROOT = PROJECT_ROOT / "datasets" / "synthetic_audio" / "dj-vanta-no-golden-ticket-required" / "generated_albums" / RUN_ID
HF_EXPORT_ROOT = Path("/opt/data/workspace/hf-dataset-exports") / f"{ALBUM_SLUG}-{RUN_ID}"
USER_AGENT = "jimsky-sonicforge-album-dataset/0.1"


def log(*parts):
    print(dt.datetime.now(dt.timezone.utc).isoformat(), *parts, flush=True)


def load_dotenv_safe(path: Path = Path("/opt/data/.env")):
    if not path.exists():
        return
    try:
        for line in path.read_text(errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k and k not in os.environ:
                os.environ[k] = v
    except Exception as e:
        log("dotenv_load_warning", type(e).__name__)


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "track"


def http_get(url: str, timeout: int = 120):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers.get("content-type"), r.status


def http_post_json(url: str, payload: dict, timeout: int = 120):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT, "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ffprobe_duration(path: Path) -> float | None:
    if not shutil.which("ffprobe"):
        return None
    try:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            text=True,
            timeout=30,
        ).strip()
        return float(out)
    except Exception:
        return None


def make_tags(row: dict) -> str:
    base = row.get("prompt_sketch") or "Original SonicForge DJ VANTA cyber-rave track, open-source builder movement, no named artist imitation."
    genre = row.get("genre_flavor", "cyber-rave electro house")
    bpm = row.get("target_bpm", 128)
    return (
        f"{genre}, {bpm} BPM, original DJ VANTA SonicForge synthetic album track, "
        "dark warehouse rave energy, clean club mix, strong kick and sub bass, neon synths, "
        "node graph mythology, Hermes agent swarm, ComfyUI workflow heartbeat, dataset-ready structure, "
        "clear intro build drop breakdown outro, no named artist imitation. " + base
    )


def make_lyrics(row: dict, index: int) -> str:
    title = row.get("title") or row.get("id") or f"Track {index:02d}"
    hook = row.get("hook") or f"{title}, signal in the node graph"
    act = str(row.get("act", "SonicForge"))
    safe_title = title.replace("&", "and")
    hook_lines = [x.strip() for x in re.split(r"/|\n", hook) if x.strip()]
    while len(hook_lines) < 4:
        hook_lines.append(f"{safe_title}, we build it alive")
    hook_block = "\n".join(hook_lines[:4])
    return f"""[Intro]
DJ VANTA on the wire, SonicForge in the room
Hermes lights the console, Comfy makes it bloom
{safe_title} is the signal, act {act}
Original transmission, no borrowed mask

[Verse 1]
We came through the side door with a laptop and a dream
Node graph in the basement, ultraviolet on the screen
Every prompt has a purpose, every seed has a name
We turn the workflow heartbeat into data and flame

[Pre-Chorus]
No golden ticket, no velvet rope
We fork the room and we build our own hope
Human at the kill switch, safety in the chain
Then the bassline rises and the signal rains

[Chorus]
{hook_block}

[Drop]
Node to node, let it flow
Deck A, Deck B, make the crossfade glow
Bassline clean, signal true
Synthetic album built by me and you

[Verse 2]
Metadata written and the lyrics stay clear
Training comes later when the review is sincere
Prompt bank, manifest, every track in line
DJ VANTA transmission through the dataset spine

[Bridge]
Keep it original, keep the credits bright
No fake endorsement in the neon night
Open-source spirit, human hands in command
ComfyUI heartbeat across the land

[Final Chorus]
{hook_block}

[Outro]
Save the audio, write the manifest
Review the keepers, train only the best
{safe_title}, the signal stays warm
SonicForge forever, the sound of the swarm
"""


def mutate_workflow(template: dict, row: dict, index: int) -> tuple[dict, int, str, str]:
    workflow = json.loads(json.dumps(template))
    track_id = slugify(row.get("id") or row.get("title") or f"track-{index:02d}")
    seed_src = f"{RUN_ID}:{track_id}:{index}"
    seed = int(hashlib.sha256(seed_src.encode()).hexdigest()[:8], 16) % 999_999_999
    bpm = int(row.get("target_bpm") or 128)
    tags = make_tags(row)
    lyrics = make_lyrics(row, index)
    workflow["94"]["inputs"].update({
        "tags": tags,
        "lyrics": lyrics,
        "bpm": bpm,
        "duration": DURATION_SECONDS,
        "timesignature": "4",
        "language": "en",
        "keyscale": row.get("keyscale") or "F minor",
        "cfg_scale": 2,
        "temperature": 0.85,
        "top_p": 0.9,
    })
    workflow["98"]["inputs"]["seconds"] = DURATION_SECONDS
    workflow["98"]["inputs"]["batch_size"] = BATCH_SIZE
    workflow["109"]["inputs"]["value"] = seed
    workflow["107"]["inputs"]["filename_prefix"] = f"audio/{index:02d}_{track_id}"
    return workflow, seed, tags, lyrics


def wait_for_history(prompt_id: str, max_wait_s: int = 1800) -> dict:
    start = time.time()
    next_report = 0
    last_error = None
    while time.time() - start < max_wait_s:
        try:
            body, _ctype, _status = http_get(BASE_URL + "/history/" + urllib.parse.quote(prompt_id), timeout=60)
            data = json.loads(body.decode("utf-8", "replace")) if body else {}
            if data and prompt_id in data:
                return data[prompt_id]
        except Exception as e:
            last_error = f"{type(e).__name__}: {str(e)[:160]}"
        if time.time() >= next_report:
            try:
                qbody, _, _ = http_get(BASE_URL + "/queue", timeout=30)
                log("waiting", prompt_id, "queue", qbody.decode("utf-8", "replace")[:250], "last_error", last_error)
            except Exception as qe:
                log("waiting", prompt_id, "queue_error", type(qe).__name__, "last_error", last_error)
            next_report = time.time() + 30
        time.sleep(5)
    raise TimeoutError(f"history timeout for {prompt_id}; last_error={last_error}")


def extract_and_download_outputs(history: dict, track_dir: Path) -> list[Path]:
    outputs = []
    for node_id, node_out in (history.get("outputs") or {}).items():
        for key, vals in (node_out or {}).items():
            if isinstance(vals, list):
                for item in vals:
                    if isinstance(item, dict) and item.get("filename"):
                        outputs.append(item)
    if not outputs:
        raise RuntimeError("no output files in history")
    downloaded = []
    audio_dir = track_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    for item in outputs:
        params = urllib.parse.urlencode({
            "filename": item.get("filename", ""),
            "subfolder": item.get("subfolder", ""),
            "type": item.get("type", "output"),
        })
        url = BASE_URL + "/view?" + params
        local = audio_dir / Path(item["filename"]).name
        blob, ctype, _ = http_get(url, timeout=240)
        local.write_bytes(blob)
        downloaded.append(local)
        log("downloaded", local, len(blob), ctype)
    return downloaded


def write_readme(export_root: Path, rows: list[dict], metadata_rows: list[dict], repo_id: str | None = None):
    generated = dt.datetime.now(dt.timezone.utc).isoformat()
    total = len(metadata_rows)
    readme = f"""---
license: other
task_categories:
- audio-classification
- text-to-audio
tags:
- synthetic-audio
- ace-step
- comfyui
- sonicforge
- dj-vanta
- music-generation
language:
- en
pretty_name: DJ VANTA — No Velvet Rope in the Node Graph
configs:
- config_name: album_tracks
  default: true
  data_files:
  - split: train
    path: metadata.jsonl
---

# DJ VANTA — No Velvet Rope in the Node Graph

Private synthetic audio dataset generated for SonicForge / DJ VANTA album-style LoRA review.

## Status

- Generated UTC: `{generated}`
- Run ID: `{RUN_ID}`
- Track target: `{len(rows)}`
- Generated tracks in this export: `{total}`
- Duration target: `{DURATION_SECONDS}` seconds each
- Format: MP3 from ComfyUI `SaveAudioMP3` workflow
- Source: original synthetic prompts and lyrics written for SonicForge / DJ VANTA
- Training started: **false**
- Public release approved: **false**
- Repo: `{repo_id or 'pending'}`

## Contents

```text
tracks/<track_id>/audio/*.mp3
tracks/<track_id>/<track_id>.lyrics.txt
tracks/<track_id>/<track_id>.settings.json
tracks/<track_id>/<track_id>.prompt.md
metadata.jsonl
album_manifest.json
```

## Safety / provenance

This dataset is composed of newly generated synthetic audio candidates from original prompts/lyrics. It is intended for private review before any model training. It should not be treated as an official release, commercial album, or endorsed collaboration with any referenced tool/person/org.

No secrets, tokens, private media, provider logs, model weights, or training checkpoints are included.
"""
    (export_root / "README.md").write_text(readme)


def copy_for_hf(album_root: Path, export_root: Path):
    if export_root.exists():
        shutil.rmtree(export_root)
    shutil.copytree(album_root, export_root)


def upload_to_hf(export_root: Path) -> dict:
    load_dotenv_safe()
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_HUB_TOKEN")
    if not token:
        return {"uploaded": False, "reason": "missing_hf_token", "repo_id": REPO_ID_DEFAULT}
    try:
        from huggingface_hub import HfApi, create_repo, upload_folder
    except Exception as e:
        return {"uploaded": False, "reason": f"huggingface_hub_import_failed:{type(e).__name__}", "repo_id": REPO_ID_DEFAULT}
    api = HfApi(token=token)
    who = api.whoami(token=token)
    log("hf_auth_ok", who.get("name") or "authenticated")
    repo_id = REPO_ID_DEFAULT
    try:
        create_repo(repo_id=repo_id, repo_type="dataset", private=True, exist_ok=True, token=token)
    except Exception as e:
        # Fallback to authenticated username namespace if org creation is not allowed.
        user = who.get("name") or who.get("fullname") or "user"
        repo_id = f"{user}/{ALBUM_SLUG}-synthetic-audio"
        log("hf_org_repo_create_failed_fallback_user_namespace", type(e).__name__)
        create_repo(repo_id=repo_id, repo_type="dataset", private=True, exist_ok=True, token=token)
    write_readme(export_root, [], [json.loads(l) for l in (export_root / "metadata.jsonl").read_text().splitlines() if l.strip()], repo_id=repo_id)
    upload_folder(
        repo_id=repo_id,
        repo_type="dataset",
        folder_path=str(export_root),
        path_in_repo=".",
        commit_message=f"Upload DJ VANTA synthetic album dataset {RUN_ID}",
        token=token,
    )
    info = api.dataset_info(repo_id, token=token, files_metadata=True)
    files = [s.rfilename for s in (info.siblings or [])]
    return {"uploaded": True, "repo_id": repo_id, "private": getattr(info, "private", None), "file_count": len(files), "url": f"https://huggingface.co/datasets/{repo_id}"}


def main():
    os.chdir(PROJECT_ROOT)
    if not WORKFLOW_PATH.exists():
        raise SystemExit(f"workflow missing: {WORKFLOW_PATH}")
    if not QUEUE_PATH.exists():
        raise SystemExit(f"queue missing: {QUEUE_PATH}")
    if not BASE_URL:
        raise SystemExit("COMFYUI_BASE_URL is not set")
    LOCAL_ALBUM_ROOT.mkdir(parents=True, exist_ok=True)
    (LOCAL_ALBUM_ROOT / "tracks").mkdir(exist_ok=True)
    (LOCAL_ALBUM_ROOT / "logs").mkdir(exist_ok=True)
    rows = [json.loads(l) for l in QUEUE_PATH.read_text().splitlines() if l.strip()]
    template = json.loads(WORKFLOW_PATH.read_text())
    log("start_full_album_generation", "tracks", len(rows), "duration", DURATION_SECONDS, "base", "COMFYUI_BASE_URL", "run", RUN_ID)
    metadata_path = LOCAL_ALBUM_ROOT / "metadata.jsonl"
    existing = {}
    if metadata_path.exists():
        for line in metadata_path.read_text().splitlines():
            if line.strip():
                d = json.loads(line); existing[d["track_id"]] = d
    metadata_rows = list(existing.values())
    for i, row in enumerate(rows, start=1):
        track_id = slugify(row.get("id") or row.get("title") or f"track-{i:02d}")
        if track_id in existing and Path(existing[track_id].get("audio_path", "")).exists():
            log("skip_existing", i, track_id)
            continue
        title = row.get("title") or track_id
        track_dir = LOCAL_ALBUM_ROOT / "tracks" / f"{i:02d}_{track_id}"
        track_dir.mkdir(parents=True, exist_ok=True)
        workflow, seed, tags, lyrics = mutate_workflow(template, row, i)
        (track_dir / f"{track_id}.lyrics.txt").write_text(lyrics)
        (track_dir / f"{track_id}.prompt.md").write_text(f"# {title}\n\n## Tags\n\n{tags}\n\n## Source row\n\n```json\n{json.dumps(row, indent=2)}\n```\n")
        settings = {"track_index": i, "track_id": track_id, "title": title, "seed": seed, "duration_seconds": DURATION_SECONDS, "bpm": row.get("target_bpm"), "keyscale": row.get("keyscale"), "workflow_source": str(WORKFLOW_PATH), "base_url_redacted": "COMFYUI_BASE_URL"}
        (track_dir / f"{track_id}.settings.json").write_text(json.dumps(settings, indent=2))
        payload = {"prompt": workflow, "client_id": f"sonicforge-{RUN_ID}-{track_id}"}
        log("submit", i, track_id, title, "seed", seed)
        resp = http_post_json(BASE_URL + "/prompt", payload, timeout=120)
        prompt_id = resp.get("prompt_id")
        if not prompt_id or resp.get("node_errors"):
            raise RuntimeError(f"prompt submit failed for {track_id}: {json.dumps(resp)[:1000]}")
        (track_dir / "prompt_id.txt").write_text(prompt_id)
        history = wait_for_history(prompt_id)
        (track_dir / f"{track_id}.history.json").write_text(json.dumps(history, indent=2))
        files = extract_and_download_outputs(history, track_dir)
        audio_path = files[0]
        duration = ffprobe_duration(audio_path)
        qa = {"duration_seconds": duration, "duration_target_seconds": DURATION_SECONDS, "duration_ok": (duration is None or abs(duration - DURATION_SECONDS) <= 2.5), "size_bytes": audio_path.stat().st_size, "sha256": sha256_file(audio_path)}
        (track_dir / f"{track_id}.review.json").write_text(json.dumps({"status": "generated_pending_human_listening_review", "qa": qa}, indent=2))
        meta = {"track_index": i, "track_id": track_id, "title": title, "audio": str(audio_path.relative_to(LOCAL_ALBUM_ROOT)), "audio_path": str(audio_path), "lyrics_file": str((track_dir / f"{track_id}.lyrics.txt").relative_to(LOCAL_ALBUM_ROOT)), "prompt_file": str((track_dir / f"{track_id}.prompt.md").relative_to(LOCAL_ALBUM_ROOT)), "settings_file": str((track_dir / f"{track_id}.settings.json").relative_to(LOCAL_ALBUM_ROOT)), "review_file": str((track_dir / f"{track_id}.review.json").relative_to(LOCAL_ALBUM_ROOT)), "prompt_id": prompt_id, "seed": seed, "bpm": row.get("target_bpm"), "keyscale": row.get("keyscale"), "duration_seconds": duration, "duration_target_seconds": DURATION_SECONDS, "format": "mp3", "sha256": qa["sha256"], "status": "generated_pending_human_listening_review", "approved_for_training": False, "source": "synthetic_comfyui_acestep_workflow"}
        existing[track_id] = meta
        metadata_rows = list(existing.values())
        metadata_rows.sort(key=lambda x: x["track_index"])
        metadata_path.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in metadata_rows))
        log("track_complete", i, track_id, "duration", duration, "file", audio_path)
    metadata_rows = [json.loads(l) for l in metadata_path.read_text().splitlines() if l.strip()]
    manifest = {"schema": "sonicforge.synthetic_audio_album.v1", "album_title": "DJ VANTA — No Velvet Rope in the Node Graph", "album_slug": ALBUM_SLUG, "run_id": RUN_ID, "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "status": "generated_pending_human_review_no_training_started", "track_count": len(metadata_rows), "duration_target_seconds": DURATION_SECONDS, "source_queue": str(QUEUE_PATH), "workflow": "ComfyUI ACE-Step 1.5 audio workflow", "closed_gates": ["training_not_started", "public_release_not_approved", "no_secrets_included"], "tracks": metadata_rows}
    (LOCAL_ALBUM_ROOT / "album_manifest.json").write_text(json.dumps(manifest, indent=2))
    write_readme(LOCAL_ALBUM_ROOT, rows, metadata_rows)
    # CSV listening sheet.
    with (LOCAL_ALBUM_ROOT / "LISTENING_REVIEW.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["track_index", "track_id", "title", "duration_seconds", "audio", "musical_score_1_5", "training_value_1_5", "notes", "accept_for_training"])
        w.writeheader()
        for m in metadata_rows:
            w.writerow({k: m.get(k, "") for k in ["track_index", "track_id", "title", "duration_seconds", "audio"]} | {"musical_score_1_5": "", "training_value_1_5": "", "notes": "", "accept_for_training": ""})
    copy_for_hf(LOCAL_ALBUM_ROOT, HF_EXPORT_ROOT)
    upload_result = upload_to_hf(HF_EXPORT_ROOT)
    (LOCAL_ALBUM_ROOT / "hf_upload_result.json").write_text(json.dumps(upload_result, indent=2))
    (HF_EXPORT_ROOT / "hf_upload_result.json").write_text(json.dumps(upload_result, indent=2))
    log("DONE", json.dumps({"local_album_root": str(LOCAL_ALBUM_ROOT), "hf_export_root": str(HF_EXPORT_ROOT), "upload": upload_result}, indent=2))


if __name__ == "__main__":
    main()
