"""Loopback-only, single-range local review server; no writes/uploads."""

from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from functools import partial
import json, os, re


class Handler(SimpleHTTPRequestHandler):
    def send_head(self):
        root = Path(self.directory).resolve()
        path = Path(self.translate_path(self.path)).resolve()
        if not path.is_relative_to(root):
            self.send_error(403)
            return
        if path.is_dir():
            path = path / "index.html"
        if not path.is_file():
            self.send_error(404)
            return
        size = path.stat().st_size
        start, end = 0, size - 1
        status = 200
        value = self.headers.get("Range")
        if value:
            match = re.fullmatch(r"bytes=(\d*)-(\d*)", value)
            try:
                if not match:
                    raise ValueError()
                a, b = match.groups()
                if not a:
                    start = max(0, size - int(b))
                    end = size - 1
                    assert int(b) > 0
                else:
                    start = int(a)
                    end = min(size - 1, int(b)) if b else size - 1
                assert 0 <= start <= end < size
                status = 206
            except (ValueError, AssertionError):
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{size}")
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
        f = path.open("rb")
        f.seek(start)
        self.remaining = end - start + 1
        self.send_response(status)
        self.send_header("Content-Type", self.guess_type(str(path)))
        self.send_header("Content-Length", str(self.remaining))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "no-cache")
        if status == 206:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        return f

    def copyfile(self, source, outputfile):
        try:
            while self.remaining:
                data = source.read(min(1024 * 1024, self.remaining))
                if not data:
                    break
                outputfile.write(data)
                self.remaining -= len(data)
        except (BrokenPipeError, ConnectionResetError):
            pass


def validate_delivery(root):
    from core import read, digest, require

    root = Path(root).resolve()
    manifest = read(root / "manifest.json")
    for name, info in manifest.items():
        path = (root / name).resolve()
        require(
            path.is_relative_to(root) and path.is_file(),
            "Missing/escaping delivery file",
        )
        require(digest(path) == info["sha256"], "Delivery payload changed")
    require((root / "index.html").is_file(), "No local player")
    if (root / "owner-review.json").exists():
        require(
            read(root / "owner-review.json")["payload_manifest_sha256"]
            == digest(root / "manifest.json"),
            "Owner review is stale",
        )
    return root


def serve(root, port=0):
    root = validate_delivery(root)
    server = ThreadingHTTPServer(
        ("127.0.0.1", port), partial(Handler, directory=str(root))
    )
    print(
        json.dumps(
            {
                "state": "LISTENING",
                "pid": os.getpid(),
                "root": str(root),
                "url": f"http://127.0.0.1:{server.server_port}/index.html",
            }
        ),
        flush=True,
    )
    try:
        server.serve_forever()
    finally:
        server.server_close()
