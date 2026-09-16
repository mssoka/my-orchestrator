import functools, json, sys, tempfile, threading, unittest, urllib.request, urllib.error
from pathlib import Path
from http.server import ThreadingHTTPServer

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from core import save, digest, ContractError
from serve import Handler, validate_delivery


class LocalServer(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.root = self.base / "delivery"
        self.root.mkdir()
        (self.root / "index.html").write_text("<video controls></video>")
        self.data = bytes(range(256))
        (self.root / "movie.mp4").write_bytes(self.data)
        save(
            self.root / "manifest.json",
            {p.name: {"sha256": digest(p)} for p in self.root.iterdir() if p.is_file()},
        )
        validate_delivery(self.root)

        class QuietHandler(Handler):
            def log_message(self, *args):
                pass

        self.server = ThreadingHTTPServer(
            ("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(self.root))
        )
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self):
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()
        self.tmp.cleanup()

    def request(self, path="/movie.mp4", range=None, method="GET"):
        req = urllib.request.Request(
            self.url + path, headers={"Range": range} if range else {}, method=method
        )
        return urllib.request.urlopen(req)

    def test_full_and_range(self):
        with self.request() as r:
            self.assertEqual(r.read(), self.data)
            self.assertEqual(r.status, 200)
        with self.request(range="bytes=2-9") as r:
            self.assertEqual(r.status, 206)
            self.assertEqual(r.read(), self.data[2:10])
            self.assertEqual(r.headers["Content-Range"], "bytes 2-9/256")

    def test_suffix_and_head(self):
        with self.request(range="bytes=-8") as r:
            self.assertEqual(r.read(), self.data[-8:])
        with self.request(range="bytes=2-9", method="HEAD") as r:
            self.assertEqual(r.read(), b"")
            self.assertEqual(r.headers["Content-Length"], "8")

    def test_invalid_ranges(self):
        for value in ["bytes=9999-", "bytes=0-1,4-5", "bytes=-0"]:
            with self.assertRaises(urllib.error.HTTPError) as cm:
                self.request(range=value)
            self.assertEqual(cm.exception.code, 416)

    def test_no_symlink_escape(self):
        secret = self.base / "secret.txt"
        secret.write_text("not served")
        (self.root / "escape.txt").symlink_to(secret)
        with self.assertRaises(urllib.error.HTTPError) as cm:
            self.request("/escape.txt")
        self.assertEqual(cm.exception.code, 403)

    def test_no_upload_method(self):
        with self.assertRaises(urllib.error.HTTPError) as cm:
            self.request(method="POST")
        self.assertEqual(cm.exception.code, 501)

    def test_tampered_delivery_refused(self):
        (self.root / "movie.mp4").write_bytes(b"changed")
        with self.assertRaises(ContractError):
            validate_delivery(self.root)


if __name__ == "__main__":
    unittest.main()
