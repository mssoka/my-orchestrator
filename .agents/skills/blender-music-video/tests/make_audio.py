"""Generate SYNTHETIC MP3 using Blender's native Audaspace writer, no external encoder."""

import aud
import bpy
import hashlib
import json
import sys
import wave
from pathlib import Path

request = json.loads(Path(sys.argv[sys.argv.index("--") + 1]).read_text())
source = Path(request["source"])
target = Path(request["target"])
assert bpy.app.background and not target.exists()
before = hashlib.sha256(source.read_bytes()).hexdigest()
with wave.open(str(source)) as wav:
    rate = wav.getframerate()
sound = aud.Sound(str(source))
sound.write(
    str(target),
    rate,
    aud.CHANNELS_STEREO,
    aud.FORMAT_S16,
    aud.CONTAINER_MP3,
    aud.CODEC_MP3,
    320000,
    4096,
)
assert target.is_file() and target.stat().st_size > 4096
assert hashlib.sha256(source.read_bytes()).hexdigest() == before
target.chmod(0o444)
print(
    json.dumps(
        {
            "state": "NATIVE_SYNTHETIC_MP3_WRITTEN",
            "bytes": target.stat().st_size,
            "sample_rate": rate,
        }
    )
)
