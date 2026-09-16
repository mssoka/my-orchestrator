"""FFmpeg is ONLY a decoder/probe here. No external encoding, mux or concat."""

import subprocess, tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps, ImageDraw
from scipy.signal import correlate
from core import require, probe, stream, pcm, save

WIDTH, HEIGHT = 160, 90


def decoded_frames(path):
    with tempfile.TemporaryFile() as err:
        p = subprocess.Popen(
            [
                "ffmpeg",
                "-v",
                "error",
                "-xerror",
                "-i",
                str(path),
                "-map",
                "0:v:0",
                "-vf",
                f"scale={WIDTH}:{HEIGHT}:flags=area",
                "-pix_fmt",
                "rgb24",
                "-f",
                "rawvideo",
                "-",
            ],
            stdout=subprocess.PIPE,
            stderr=err,
        )
        try:
            while True:
                b = p.stdout.read(WIDTH * HEIGHT * 3)
                if not b:
                    break
                require(len(b) == WIDTH * HEIGHT * 3, "Incomplete decoded frame")
                yield (
                    np.frombuffer(b, dtype=np.uint8)
                    .reshape(HEIGHT, WIDTH, 3)
                    .astype(np.float32)
                )
            require(p.wait() == 0, "Full video decode failed")
        finally:
            if p.poll() is None:
                p.terminate()
                p.wait()  # Own QA decoder only; never a renderer.
            p.stdout.close()


def picture(movie, loop, frames, folder):
    reference = list(decoded_frames(loop))
    require(len(reference) > 1, "Empty/still loop")
    mad = []
    bad = []
    joins = []
    previous = None
    minimum = float("inf")
    samples = []
    for i, f in enumerate(decoded_frames(movie)):
        j = i % len(reference)
        values = [
            float(np.abs(f - reference[(j + k) % len(reference)]).mean())
            for k in [-1, 0, 1]
        ]
        mad.append(values[1])
        if values[1] > 4 or values[1] > min(values[0], values[2]) + 0.05:
            bad.append(i)
        if previous is not None:
            delta = float(np.abs(f - previous).mean())
            minimum = min(minimum, delta)
            if j == 0:
                joins.append({"frame_index": i, "mad": delta})
        if i in {0, len(reference) - 1, len(reference), frames // 2, frames - 1}:
            samples.append((i, Image.fromarray(f.astype("uint8")).resize((480, 270))))
        previous = f
    require(len(mad) == frames, f"Expected{frames} frames, got{len(mad)}")
    require(not bad, f"Unexpected phase/colour at frames{bad[:12]}")
    require(minimum > 0.01, "Duplicate/stalled adjacent pictures")
    sheet = Image.new("RGB", (480 * len(samples), 298), "#111111")
    draw = ImageDraw.Draw(sheet)
    for k, (index, img) in enumerate(samples):
        sheet.paste(img, (k * 480, 28))
        draw.text((k * 480 + 8, 8), f"Frame {index + 1}", fill="white")
    sheet.save(folder / "picture-check.jpg")
    return {
        "frames": frames,
        "all_expected_phases_checked": True,
        "max_mad": max(mad),
        "mean_mad": float(np.mean(mad)),
        "minimum_adjacent_mad": minimum,
        "joins": joins,
        "comparison_resolution": [WIDTH, HEIGHT],
        "calibrated_display_certification": False,
    }


def alignment(a, b, start, length, radius=2048):
    channel = int(np.argmax(np.sum(a[start : start + length] ** 2, axis=0)))
    x = a[start : start + length, channel]
    lo = max(0, start - radius)
    hi = min(len(b), start + length + radius)
    y = b[lo:hi, channel]
    if np.sqrt(np.mean(x * x)) < 1e-6:
        return {"start_sample": start, "state": "UNMEASURABLE_SILENCE"}
    scores = correlate(y, x, mode="valid", method="fft")
    energy = np.concatenate(([0.0], np.cumsum(y * y)))
    energy = energy[length:] - energy[:-length]
    scores /= np.sqrt(np.maximum(energy, 1e-30) * np.sum(x * x))
    offset = int(np.argmax(scores)) + lo - start
    return {
        "start_sample": start,
        "channel": channel,
        "offset_samples": offset,
        "normalised_score": float(np.max(scores)),
    }


def audio(movie, original, rate, expected_frames, fps, full):
    a = pcm(original).astype(np.float64)
    b = pcm(movie).astype(np.float64)
    nominal = round(expected_frames * rate / fps)
    # Native AAC can round to an encoder packet; distinguish that from the frame-grid tail.
    require(
        nominal - 2 <= len(b) <= nominal + 1024,
        "Unexpected decoded audio duration/encoder padding",
    )
    if full:
        require(len(b) >= len(a), "Missing original ending")
    count = min(len(a), len(b), nominal)
    win = min(rate, count)
    starts = sorted({0, max(0, count // 2 - win // 2), max(0, count - win)})
    windows = [alignment(a, b, k, win) for k in starts]
    measured = [x for x in windows if "offset_samples" in x]
    require(measured, "No measurable soundtrack in native diagnostic")
    require(
        all(
            abs(x["offset_samples"]) <= 2 and x["normalised_score"] > 0.98
            for x in measured
        ),
        f"Audio alignment failure:{windows}",
    )
    aa = a[:count]
    bb = b[:count]
    corr = []
    gain = []
    for ch in range(2):
        if np.std(aa[:, ch]) < 1e-7:
            require(
                float(np.sqrt(np.mean(bb[:, ch] ** 2))) < 1e-4,
                "Silent source channel gained signal",
            )
            corr.append(None)
            gain.append(None)
        else:
            corr.append(float(np.corrcoef(aa[:, ch], bb[:, ch])[0, 1]))
            gain.append(
                float(np.dot(aa[:, ch], bb[:, ch]) / np.dot(aa[:, ch], aa[:, ch]))
            )
    peak = float(np.abs(b).max())
    require(
        all(x is None or x > 0.98 for x in corr)
        and all(x is None or 0.98 < x < 1.02 for x in gain)
        and peak < 1,
        f"Correlation/gain/clipping failure:{corr},{gain},{peak}",
    )
    return {
        "original_samples": len(a),
        "decoded_samples": len(b),
        "compared_samples": count,
        "nominal_frame_grid_samples": nominal,
        "aac_packet_padding_samples": len(b) - nominal,
        "original_ending_checked": full,
        "alignment": windows,
        "whole_compared_correlation": corr,
        "gain": gain,
        "peak": peak,
        "listened": False,
        "method": "decoded PCM; energy-normalised correlation, not listening",
    }


def video_check(movie, loop, c, facts, frames, folder, full):
    p = probe(movie)
    v = stream(p, "video")
    a = stream(p, "audio")
    require(
        len(p["streams"]) == 2
        and v["codec_name"] == "h264"
        and a["codec_name"] == "aac",
        "Expected only native H264/AAC streams",
    )
    require(
        [v["width"], v["height"]] == [c["video"]["width"], c["video"]["height"]],
        "Output dimensions changed",
    )
    require(
        (
            v.get("color_transfer"),
            v.get("color_primaries"),
            v.get("color_space"),
            v.get("color_range"),
        )
        == ("iec61966-2-1", "bt709", "bt709", "tv"),
        "Colour signalling mismatch",
    )
    from fractions import Fraction

    require(
        Fraction(v["avg_frame_rate"]) == c["video"]["fps"]
        and int(v["nb_read_frames"]) == frames,
        "fps/frame count mismatch",
    )
    require(
        a["channels"] == 2 and int(a["sample_rate"]) == facts["audio_rate"],
        "Output audio layout/rate mismatch",
    )
    result = {
        "picture": picture(movie, loop, frames, folder),
        "audio": audio(
            movie, c["music"], facts["audio_rate"], frames, c["video"]["fps"], full
        ),
        "probe": p,
    }
    save(folder / "measurements.json", result)
    return result


def loop_check(movie, folder):
    frames = list(decoded_frames(movie))
    deltas = [float(np.abs(a - b).mean()) for a, b in zip(frames, frames[1:])]
    require(min(deltas) > 0.01, "Frozen/duplicate loop frame")
    require(
        len({f.tobytes() for f in frames}) == len(frames), "Repeated sub-period in loop"
    )
    a = np.asarray(Image.open(folder / "start.png").convert("RGB"), dtype=np.float32)
    b = np.asarray(Image.open(folder / "endpoint.png").convert("RGB"), dtype=np.float32)
    endpoint = float(np.abs(a - b).mean())
    seam = float(np.abs(frames[-1] - frames[0]).mean())
    require(endpoint < 1, "Native endpoint does not close")
    require(seam <= max(deltas) * 1.3, "Disproportionate cycle seam")
    result = {
        "unique_frames": len(frames),
        "endpoint_mad": endpoint,
        "seam_mad": seam,
        "adjacent_min": min(deltas),
        "adjacent_max": max(deltas),
        "needs_actual_motion_review": True,
    }
    save(folder / "loop-check.json", result)
    return result
