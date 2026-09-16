"""Guarded metadata-only repair for Blender5.2 native H264/sRGB exports.

The native encoder writes BT709 transfer=1 although Standard/sRGB output pixels
are sRGB. Retain those pixels and correct transfer=13 in avcC SPS and colr.
No concat, remux, decode, audio edit or re-encode. Runs inside the Blender export
process. Refuse absent/unsupported signalling or any structural size change.
"""

from pathlib import Path
import hashlib, json, struct


class Bits:
    def __init__(self, data):
        self.data = bytearray(data)
        self.pos = 0

    def read(self, n):
        assert self.pos + n <= len(self.data) * 8, "Truncated SPS"
        v = 0
        for _ in range(n):
            v = (v << 1) | ((self.data[self.pos // 8] >> (7 - self.pos % 8)) & 1)
            self.pos += 1
        return v

    def ue(self):
        zeros = 0
        while self.read(1) == 0:
            zeros += 1
            assert zeros < 32, "Invalid Exp-Golomb"
        return (1 << zeros) - 1 + (self.read(zeros) if zeros else 0)

    def se(self):
        v = self.ue()
        return (v + 1) // 2 if v & 1 else -(v // 2)

    def put(self, offset, n, value):
        for i in range(n):
            bit = offset + i
            mask = 1 << (7 - bit % 8)
            self.data[bit // 8] = (self.data[bit // 8] & ~mask) | (
                ((value >> (n - 1 - i)) & 1) << (7 - bit % 8)
            )


def unescape(data):
    out = bytearray()
    zeros = 0
    i = 0
    while i < len(data):
        b = data[i]
        if zeros >= 2 and b == 3:
            assert i + 1 < len(data) and data[i + 1] <= 3, (
                "Invalid emulation prevention"
            )
            zeros = 0
            i += 1
            continue
        out.append(b)
        zeros = zeros + 1 if b == 0 else 0
        i += 1
    return out


def escape(data):
    out = bytearray()
    zeros = 0
    for b in data:
        if zeros >= 2 and b <= 3:
            out.append(3)
            zeros = 0
        out.append(b)
        zeros = zeros + 1 if b == 0 else 0
    return bytes(out)


def patch_sps(nal):
    assert nal and nal[0] & 31 == 7, "Expected SPS"
    b = Bits(unescape(nal[1:]))
    profile = b.read(8)
    b.read(16)
    b.ue()
    if profile in {100, 110, 122, 244, 44, 83, 86, 118, 128, 138, 139, 134, 135}:
        chroma = b.ue()
        if chroma == 3:
            b.read(1)
        b.ue()
        b.ue()
        b.read(1)
        if b.read(1):
            for i in range(8 if chroma != 3 else 12):
                if b.read(1):
                    last = next_scale = 8
                    for _ in range(16 if i < 6 else 64):
                        if next_scale:
                            next_scale = (last + b.se() + 256) % 256
                        last = last if next_scale == 0 else next_scale
    b.ue()
    order = b.ue()
    if order == 0:
        b.ue()
    elif order == 1:
        b.read(1)
        b.se()
        b.se()
        for _ in range(b.ue()):
            b.se()
    elif order != 2:
        raise AssertionError("Unsupported SPS picture order")
    b.ue()
    b.read(1)
    b.ue()
    b.ue()
    if not b.read(1):
        b.read(1)
    b.read(1)
    if b.read(1):
        for _ in range(4):
            b.ue()
    assert b.read(1), "Missing VUI: refuse structural insertion"
    if b.read(1):
        aspect = b.read(8)
        if aspect == 255:
            b.read(32)
    if b.read(1):
        b.read(1)
    assert b.read(1), "Missing video-signal metadata"
    b.read(3)
    full_range = b.read(1)
    assert b.read(1), "Missing colour description"
    primaries = b.read(8)
    transfer_bit = b.pos
    transfer = b.read(8)
    matrix = b.read(8)
    assert primaries == 1 and matrix == 1 and transfer in {1, 13} and full_range == 0, (
        primaries,
        transfer,
        matrix,
        full_range,
    )
    b.put(transfer_bit, 8, 13)
    patched = nal[:1] + escape(b.data)
    assert len(patched) == len(nal), "SPS size changed; refuse any MP4 relocation/remux"
    return patched, {
        "primaries": primaries,
        "matrix": matrix,
        "range_full": bool(full_range),
        "transfer_before": transfer,
        "transfer_after": 13,
        "rbsp_transfer_bit": transfer_bit,
    }


def repair(path, owned_root):
    path = Path(path).resolve()
    assert path.is_relative_to(Path(owned_root).resolve())
    assert path.stat().st_size <= 2 * 1024**3, (
        "Buffered metadata repair limited to2GiB; validate a streaming implementation for larger exports"
    )
    before = path.read_bytes()
    buf = bytearray(before)
    signals = []
    colr_count = 0
    avcc_count = 0
    containers = {b"moov", b"trak", b"mdia", b"minf", b"stbl", b"edts", b"dinf"}

    def walk(start, end):
        nonlocal colr_count, avcc_count
        at = start
        while at < end:
            assert at + 8 <= end, "Truncated atom"
            size, kind = struct.unpack_from(">I4s", buf, at)
            header = 8
            if size == 1:
                size = struct.unpack_from(">Q", buf, at + 8)[0]
                header = 16
            if size == 0:
                size = end - at
            assert size >= header and at + size <= end, (kind, size)
            payload = at + header
            stop = at + size
            if kind in containers:
                walk(payload, stop)
            elif kind == b"stsd":
                walk(payload + 8, stop)
            elif kind == b"avc1":
                walk(payload + 78, stop)
            elif kind == b"avc3":
                raise AssertionError("In-band SPS signalling unsupported")
            elif kind == b"avcC":
                avcc_count += 1
                assert buf[payload] == 1
                pos = payload + 6
                count = buf[payload + 5] & 31
                assert count >= 1
                for _ in range(count):
                    length = struct.unpack_from(">H", buf, pos)[0]
                    pos += 2
                    assert pos + length <= stop
                    fixed, signal = patch_sps(bytes(buf[pos : pos + length]))
                    buf[pos : pos + length] = fixed
                    signals.append(signal)
                    pos += length
            elif kind == b"colr":
                assert bytes(buf[payload : payload + 4]) in {b"nclx", b"nclc"}, (
                    "Unsupported colour atom"
                )
                prim, trc, matrix = struct.unpack_from(">HHH", buf, payload + 4)
                assert prim == 1 and matrix == 1 and trc in {1, 13}, (prim, trc, matrix)
                struct.pack_into(">H", buf, payload + 6, 13)
                colr_count += 1
            at = stop

    walk(0, len(buf))
    assert avcc_count == 1 and signals and colr_count == 1, (
        "Expected one native H264 track and one colour atom"
    )
    assert len(buf) == len(before)
    changes = [
        {"offset": i, "before": a, "after": b}
        for i, (a, b) in enumerate(zip(before, buf))
        if a != b
    ]
    # Only a few signalling bytes may change, never mdat/audio or container layout.
    assert len(changes) <= 4 * (len(signals) + colr_count), changes
    after = bytes(buf)
    if changes:
        tmp = path.with_suffix(path.suffix + ".metadata-tmp")
        assert not tmp.exists()
        tmp.write_bytes(after)
        tmp.replace(path)
    return {
        "method": "In-process native-export metadata repair only; no remux/re-encode",
        "native_sha256_before": hashlib.sha256(before).hexdigest(),
        "sha256_after": hashlib.sha256(after).hexdigest(),
        "bytes_before": len(before),
        "bytes_after": len(after),
        "signals": signals,
        "colr_atoms": colr_count,
        "changed_bytes": changes,
        "audio_and_picture_packet_payloads_unchanged": True,
    }
