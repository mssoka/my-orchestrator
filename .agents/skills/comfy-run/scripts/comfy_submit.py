#!/usr/bin/env python3
"""comfy_submit.py — submit a ComfyUI workflow (frontend OR API format) to a
running ComfyUI server, with surgical input overrides. Stdlib only.

Usage:
    python3 comfy_submit.py WORKFLOW.json \
        [--url http://127.0.0.1:8188] \
        [--set NODE_ID.INPUT_NAME=VALUE ...] \
        [--set-file NODE_ID.INPUT_NAME=@/path/prompt.txt ...] \
        [--add-video NODE_ID.INPUT_NAME=/path/clip.mp4 ...] \
        [--wait] [--timeout 1800] [--download DIR]

--set overrides land AFTER conversion, by API input name — always exact.
--add-video inserts LoadVideo -> GetVideoComponents and wires the IMAGE-frames
output into a ref_videos.* slot (the MiniMax H3 R2V pattern).

Gotchas baked in (learned 2026-08-30, see comfy-run SKILL.md):
- Templates ship in FRONTEND format (nodes+links); POST /prompt needs API format.
- Widget defs shaped [[options...],{meta}] are COMBOs; [[type,{meta}]] too.
- input_order (not dict merge) is the authoritative widget order.
- MarkdownNote nodes are frontend-only — always stripped.
- Linked params store stale widgets: consume-and-discard by position.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request

WIDGET_TYPES = {"INT", "FLOAT", "STRING", "BOOLEAN", "COMBO"}
SKIP_CLASSES = {"MarkdownNote", "Note"}


def is_widget(v):
    if not isinstance(v, list) or not v:
        return False
    t = v[0]
    if isinstance(t, str):
        return t in WIDGET_TYPES
    if isinstance(t, list):
        return True
    return False


def api_get(url, path):
    return json.load(urllib.request.urlopen(url + path, timeout=15))


def convert_frontend(wf, object_info):
    nodes = {n["id"]: n for n in wf["nodes"]}
    links = wf["links"]
    api = {}
    for nid, n in nodes.items():
        ctype = n["type"]
        if ctype in SKIP_CLASSES:
            continue
        info = object_info.get(ctype)
        if not info:
            continue
        inp = info.get("input", {})
        order = info.get("input_order", {})
        names = (order.get("required") or list((inp.get("required") or {}).keys())) + (
            order.get("optional") or list((inp.get("optional") or {}).keys()))
        defs = {}
        for sec in ("required", "optional"):
            for k, v in (inp.get(sec) or {}).items():
                defs[k] = v
        linked = {}
        for i in n.get("inputs", []):
            if i.get("link") is not None:
                l = next(l for l in links if l[0] == i["link"])
                nm = i.get("name")
                if not isinstance(nm, str):
                    nm = nm[0] if isinstance(nm, list) and nm else str(nm)
                linked[nm] = [str(l[1]), l[2]]
        wv = list(n.get("widgets_values") or [])
        inputs = dict(linked)
        wi = 0
        for k in names:
            v = defs.get(k)
            if v is None or not is_widget(v):
                continue
            if k in linked:
                if wi < len(wv):
                    wi += 1
                continue
            if wi < len(wv):
                inputs[k] = wv[wi]
                wi += 1
        api[str(nid)] = {"class_type": ctype, "inputs": inputs,
                         "_meta": {"title": n.get("title", ctype)}}
    return api


def coerce(value):
    for cast in (lambda x: x.lower() == "true" if x.lower() in ("true", "false") else None,
                 int, float):
        try:
            r = cast(value)
            if r is not None:
                return r
        except (ValueError, TypeError):
            continue
    return value


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workflow")
    ap.add_argument("--url", default="http://127.0.0.1:8188")
    ap.add_argument("--set", dest="sets", action="append", default=[])
    ap.add_argument("--set-file", dest="setfiles", action="append", default=[])
    ap.add_argument("--add-video", dest="videos", action="append", default=[])
    ap.add_argument("--wait", action="store_true")
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--download", dest="download_dir")
    args = ap.parse_args()

    wf = json.load(open(args.workflow))
    object_info = api_get(args.url, "/object_info")

    if isinstance(wf, dict) and "nodes" in wf:
        api = convert_frontend(wf, object_info)
    else:
        api = {str(k): v for k, v in wf.items()}
        api = {k: v for k, v in api.items()
               if v.get("class_type") not in SKIP_CLASSES}

    for spec in args.sets:
        target, _, value = spec.partition("=")
        nid, _, field = target.partition(".")
        api[nid]["inputs"][field] = coerce(value)
    for spec in args.setfiles:
        target, _, path = spec.partition("=")
        nid, _, field = target.partition(".")
        api[nid]["inputs"][field] = open(path.lstrip("@")).read().strip()

    next_id = max(int(k) for k in api) + 1
    for spec in args.videos:
        target, _, path = spec.partition("=")
        nid, _, field = target.partition(".")
        lv, gvc = str(next_id), str(next_id + 1)
        next_id += 2
        api[lv] = {"class_type": "LoadVideo", "inputs": {"file": path}, "_meta": {"title": "Load Video"}}
        api[gvc] = {"class_type": "GetVideoComponents", "inputs": {"video": [lv, 0]}, "_meta": {"title": "Get Video Components"}}
        api[nid]["inputs"][field] = [gvc, 0]

    body = json.dumps({"prompt": api}).encode()
    req = urllib.request.Request(args.url + "/prompt", data=body,
                                 headers={"Content-Type": "application/json"})
    try:
        resp = json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode()[:2000], file=sys.stderr)
        sys.exit(1)
    pid = resp["prompt_id"]
    print("QUEUED prompt_id:", pid)

    if not args.wait:
        return
    deadline = time.time() + args.timeout
    while time.time() < deadline:
        time.sleep(10)
        hist = api_get(args.url, "/history/" + pid).get(pid, {})
        status = hist.get("status", {})
        if status.get("completed") or status.get("status_str") == "success":
            outputs = hist.get("outputs", {})
            files = []
            for nid, out in outputs.items():
                for kind in ("videos", "images", "gifs"):
                    for f in out.get(kind, []) or []:
                        files.append(f)
            print("COMPLETED. outputs:", json.dumps(files, indent=1))
            if args.download_dir:
                import os
                os.makedirs(args.download_dir, exist_ok=True)
                for f in files:
                    q = ("?filename=" + f["filename"] + "&subfolder=" + f.get("subfolder", "")
                         + "&type=" + f.get("type", "output"))
                    data = urllib.request.urlopen(args.url + "/view" + q).read()
                    dest = os.path.join(args.download_dir, f["filename"])
                    with open(dest, "wb") as fh:
                        fh.write(data)
                    print("saved:", dest)
            return
        if status.get("status_str") == "error":
            print("FAILED:", json.dumps(hist.get("outputs", {}))[:800], file=sys.stderr)
            sys.exit(2)
    print("TIMEOUT waiting for", pid, file=sys.stderr)
    sys.exit(3)


if __name__ == "__main__":
    main()
