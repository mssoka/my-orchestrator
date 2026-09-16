import copy, json, os, struct, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from core import ContractError, load_config, open_job, receipt, save, digest, inspect
from mv import lock, reviewed
from selftest import config, fixture
from srgb_metadata import repair, Bits, escape, unescape


class Contracts(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="native contract spaces ")
        self.work = Path(self.tmp.name)
        self.music = fixture(self.work, 0.317)
        self.c = config(self.work, self.music)
        self.path = self.work / "config.json"
        self.put()

    def tearDown(self):
        self.tmp.cleanup()

    def put(self):
        save(self.path, self.c)

    def test_missing_original(self):
        self.c["music"] = str(self.work / "missing.wav")
        self.put()
        with self.assertRaises(ContractError):
            load_config(self.path)

    def test_bad_fps(self):
        self.c["video"]["fps"] = 23.976
        self.put()
        with self.assertRaises(ContractError):
            load_config(self.path)

    def test_test_only_string_does_not_bypass_review(self):
        self.c["test_only"] = "false"
        self.put()
        with self.assertRaises(ContractError):
            load_config(self.path)

    def test_boolean_fps_is_not_a_frame_rate(self):
        self.c["video"]["fps"] = True
        self.put()
        with self.assertRaises(ContractError):
            load_config(self.path)

    def test_nested_typo_rejected(self):
        self.c["video"]["sampls"] = 32
        self.put()
        with self.assertRaises(ContractError):
            load_config(self.path)

    def test_antiphase_audio_alignment_and_real_skip(self):
        import numpy as np
        from checks import alignment

        x = np.random.default_rng(37).normal(0, 0.1, 12000)
        a = np.column_stack([x, -x])
        self.assertEqual(alignment(a, a, 3000, 3000)["offset_samples"], 0)
        self.assertEqual(
            abs(alignment(a, a[1105:], 3000, 3000)["offset_samples"]), 1105
        )

    def test_bad_loop(self):
        self.c["loop"]["frames"] = 0
        self.put()
        with self.assertRaises(ContractError):
            load_config(self.path)

    def test_unknown_config_key(self):
        self.c["ouput"] = "typo"
        self.put()
        with self.assertRaises(ContractError):
            load_config(self.path)

    def test_no_fabricated_authority(self):
        self.c["approval"]["full_song"] = ""
        self.put()
        with self.assertRaises(ContractError):
            load_config(self.path)

    def test_audio_must_remain_external(self):
        self.c["output"] = str(self.work)
        self.put()
        with self.assertRaises(ContractError):
            load_config(self.path)

    def test_existing_unowned_output(self):
        Path(self.c["output"]).mkdir()
        with self.assertRaises(ContractError):
            open_job(load_config(self.path))

    def test_changed_resume_config(self):
        c = load_config(self.path)
        open_job(c)
        c["title"] = "changed"
        with self.assertRaises(ContractError):
            open_job(c)

    def test_changed_resume_source(self):
        c = load_config(self.path)
        open_job(c)
        self.music.chmod(0o644)
        with self.music.open("ab") as f:
            f.write(b"changed")
        with self.assertRaises(ContractError):
            open_job(c)

    def test_changed_helper_identity(self):
        c = load_config(self.path)
        open_job(c)
        with patch("core.script_identity", return_value="changed"):
            with self.assertRaises(ContractError):
                open_job(c)

    def test_partial_export_is_not_success(self):
        r, job = open_job(load_config(self.path))
        (r / "movie.mp4").write_bytes(b"partial native bytes")
        save(r / "terminal.json", {"state": "FAILED", "returncode": 73})
        with self.assertRaises(ContractError):
            receipt(r, "export")

    def test_changed_completed_artifact(self):
        r, job = open_job(load_config(self.path))
        p = r / "picture.mp4"
        p.write_bytes(b"old")
        save(
            r / "export.json",
            {
                "identity": job["identity"],
                "files": {"picture.mp4": {"sha256": digest(p)}},
            },
        )
        p.write_bytes(b"new")
        with self.assertRaises(ContractError):
            receipt(r, "export")

    def test_live_lock_cannot_be_stolen(self):
        r, job = open_job(load_config(self.path))
        save(r / "worker.lock", {"identity": job["identity"], "pid": os.getpid()})
        with self.assertRaises(ContractError):
            with lock(r, clear=True):
                pass

    def test_missing_actual_review_is_not_approval(self):
        self.c["test_only"] = False
        self.put()
        r, job = open_job(load_config(self.path))
        with self.assertRaises(ContractError):
            reviewed(r, "loop")

    def test_small_partial_repeat_and_external_paths(self):
        c = load_config(self.path)
        facts = inspect(c)
        self.assertEqual(facts["frames"], 8)
        self.assertEqual(facts["partial_frames"], 8)
        self.assertNotEqual(facts["inputs"]["music"]["path"], c["output"])

    def test_broken_metadata_refuses_write(self):
        p = self.work / "bad.mp4"
        p.write_bytes(b"not an MP4")
        before = digest(p)
        with self.assertRaises((AssertionError, struct.error)):
            repair(p, self.work)
        self.assertEqual(before, digest(p))

    def test_metadata_cannot_touch_foreign_path(self):
        with self.assertRaises(AssertionError):
            repair(self.music, self.work / "owned subdirectory")


@unittest.skipUnless(
    os.environ.get("MV_TEST_MP4"),
    "Native metadata fixture supplied after smoke via MV_TEST_MP4",
)
class NativeMetadata(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.path = self.root / "native.mp4"
        self.path.write_bytes(Path(os.environ["MV_TEST_MP4"]).read_bytes())

    def tearDown(self):
        self.tmp.cleanup()

    def test_idempotent(self):
        before = digest(self.path)
        r = repair(self.path, self.root)
        self.assertEqual(r["changed_bytes"], [])
        self.assertEqual(before, digest(self.path))

    def test_wrong_colr_is_not_a_colour_conversion(self):
        b = bytearray(self.path.read_bytes())
        at = b.index(b"nclx")
        struct.pack_into(">H", b, at + 6, 16)
        self.path.write_bytes(b)
        before = digest(self.path)
        with self.assertRaises(AssertionError):
            repair(self.path, self.root)
        self.assertEqual(before, digest(self.path))

    def test_missing_colr_refuses(self):
        self.path.write_bytes(self.path.read_bytes().replace(b"colr", b"free"))
        before = digest(self.path)
        with self.assertRaises(AssertionError):
            repair(self.path, self.root)
        self.assertEqual(before, digest(self.path))

    def test_inband_sps_refuses(self):
        self.path.write_bytes(self.path.read_bytes().replace(b"avc1", b"avc3"))
        with self.assertRaises(AssertionError):
            repair(self.path, self.root)

    def test_repair_bounded_and_payload_unchanged(self):
        b = bytearray(self.path.read_bytes())
        colr = b.index(b"nclx")
        struct.pack_into(">H", b, colr + 6, 1)
        avcc = b.index(b"avcC") + 4
        at = avcc + 6
        size = struct.unpack_from(">H", b, at)[0]
        at += 2
        nal = bytes(b[at : at + size])
        from srgb_metadata import patch_sps

        _, info = patch_sps(nal)
        bits = Bits(unescape(nal[1:]))
        bits.put(info["rbsp_transfer_bit"], 8, 1)
        replacement = nal[:1] + escape(bits.data)
        self.assertEqual(len(replacement), size)
        b[at : at + size] = replacement
        self.path.write_bytes(b)
        before = bytes(b)
        r = repair(self.path, self.root)
        after = self.path.read_bytes()
        self.assertEqual(len(before), len(after))
        self.assertGreaterEqual(len(r["changed_bytes"]), 2)
        self.assertTrue(
            all(
                at <= x["offset"] < at + size or colr + 6 <= x["offset"] < colr + 8
                for x in r["changed_bytes"]
            )
        )


if __name__ == "__main__":
    unittest.main()
