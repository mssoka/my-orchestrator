#!/usr/bin/env python3
"""hf_gen.py — submit a Higgsfield generation via the RAW developer API.

The Blender plugin's own submission layer is buggy (4 server-side fails on
2026-08-30); the raw endpoint works when the body is wrapped in a
{"params": {...}} envelope. Stdlib only.

Usage:
    python3 hf_gen.py video --job-type seedance_2_5 \
        --params-file params.json \
        [--image-ref MEDIA_ID ...] [--video-ref MEDIA_ID ...] \
        [--upload /abs/path/file ...] \
        [--wait] [--timeout 1800] [--download /abs/path/out.mp4]

Auth: reads the Blender plugin's session token from
    ~/Library/Application Support/Higgsfield/Blender/auth.json
Workspace: --workspace-id or the plugin's default
    50d577d1-1f9f-407c-a0d7-3d786ca1f2db (header: hf-workspace-id)

Upload flow: POST /developer/v2alpha/medias (multipart) -> media id, then
reference ids in params as image_references / video_references.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time

AUTH_FILE = os.path.expanduser(
    "~/Library/Application Support/Higgsfield/Blender/auth.json")
BASE = "https://fnf-api-gw.higgsfield.ai/fnf-plugin-gateway"
DEFAULT_WS = "50d577d1-1f9f-407c-a0d7-3d786ca1f2db"


def token():
    d = json.load(open(AUTH_FILE))
    return d.get("access_token") or d.get("id_token")


def curl(method, url, headers=None, json_body=None, data_path=None, timeout=120, retries=3):
    """curl transport — Cloudflare 1010-bans python urllib's TLS fingerprint,
    so ALL API traffic goes through the curl binary. Network blips retry."""
    last = ""
    for attempt in range(retries):
        cmd = ["curl", "-sS", "-m", str(timeout), "-X", method, url]
        for k, v in (headers or {}).items():
            cmd += ["-H", k + ": " + v]
        if json_body is not None:
            cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(json_body)]
        if data_path is not None:
            cmd += ["--data-binary", "@" + data_path]
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 30)
        except subprocess.TimeoutExpired:
            last = "timeout-expired"
            time.sleep(15)
            continue
        if out.returncode == 0:
            text = out.stdout
            try:
                return json.loads(text)
            except ValueError:
                return {"_raw": text}
        last = out.stderr[:300]
        time.sleep(15)
    print("curl failed after retries:", last, file=sys.stderr)
    sys.exit(1)


def req(method, path, ws, body=None, put_file=None, extra_headers=None):
    h = {"Authorization": "Bearer " + token(), "hf-workspace-id": ws}
    if extra_headers:
        h.update(extra_headers)
    resp = curl(method, BASE + path, headers=h, json_body=body, data_path=put_file)
    if isinstance(resp, dict) and resp.get("detail") and "error" in str(resp.get("detail")).lower():
        print("API error:", json.dumps(resp)[:800], file=sys.stderr)
        sys.exit(1)
    return resp


def upload(path, ws, kind=None):
    """Slot-pattern upload: create slot -> PUT bytes to presigned URL -> confirm.

    The backend is NOT a multipart endpoint (a multipart POST to /medias gets
    a Cloudflare 1010). Flow per higgsfield.resources.media:
    POST /developer/v2alpha/media?type=K&extension=E -> slot with upload_url;
    PUT bytes to upload_url; POST /media/<id>/confirm?type=K -> media id.
    """
    fname = os.path.basename(path)
    ext = os.path.splitext(fname)[1].lstrip(".").lower() or "png"
    if kind is None:
        kind = "video" if ext in ("mp4", "mov", "webm", "m4v") else (
            "audio" if ext in ("mp3", "wav", "m4a", "aac") else "image")
    slot = req("POST", "/developer/v2alpha/media?type=" + kind + "&extension=" + ext, ws)
    upload_url = slot.get("upload_url")
    ctype = slot.get("content_type") or "application/octet-stream"
    media_id = slot.get("id") or slot.get("media_id")
    curl("PUT", upload_url, headers={"Content-Type": ctype}, data_path=path, timeout=300)
    conf = req("POST", "/developer/v2alpha/media/" + media_id + "/confirm?type=" + kind, ws)
    mid = conf.get("id") or conf.get("media_id") or media_id
    print("uploaded", fname, "->", mid)
    return mid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=["video", "image", "3d", "audio"])
    ap.add_argument("--job-type", required=True)
    ap.add_argument("--params-file")
    ap.add_argument("--prompt")
    ap.add_argument("--image-ref", action="append", default=[])
    ap.add_argument("--video-ref", action="append", default=[])
    ap.add_argument("--upload", action="append", default=[])
    ap.add_argument("--workspace-id", default=DEFAULT_WS)
    ap.add_argument("--wait", action="store_true")
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--download")
    args = ap.parse_args()

    params = {}
    if args.params_file:
        params = json.load(open(args.params_file))
    if args.prompt:
        params["prompt"] = args.prompt

    uploaded = [upload(p, args.workspace_id) for p in args.upload]

    def refs(kind, ids):
        if not ids:
            return
        key = {"image": "image_references", "video": "video_references",
               "audio": "audio_references"}[kind]
        params.setdefault(key, []).extend({"id": i} for i in ids)

    if uploaded:
        if args.kind == "video" and uploaded:
            refs("video", uploaded[:-2] if len(uploaded) > 2 else uploaded)
    refs("image", args.image_ref)
    refs("video", args.video_ref)

    path = "/developer/v2alpha/" + args.kind + "s/" + args.job_type + "/generations"
    resp = req("POST", path, args.workspace_id, body={"params": params})
    jid = resp["id"]
    print("SUBMITTED", jid, "| credits:", resp.get("credits"))

    if not args.wait:
        return
    deadline = time.time() + args.timeout
    while time.time() < deadline:
        time.sleep(15)
        job = req("GET", "/developer/v2alpha/jobs/" + jid, args.workspace_id)
        st = job.get("status")
        if st == "completed":
            url = job.get("result_url")
            print("COMPLETED:", url)
            if args.download and url:
                subprocess.run(["curl", "-sSL", "-m", "300", "-o", args.download, url], check=True)
                print("saved:", args.download, os.path.getsize(args.download), "bytes")
            return
        if st == "failed":
            print("FAILED:", json.dumps(job)[:600], file=sys.stderr)
            sys.exit(2)
    print("TIMEOUT", file=sys.stderr)
    sys.exit(3)


if __name__ == "__main__":
    main()
