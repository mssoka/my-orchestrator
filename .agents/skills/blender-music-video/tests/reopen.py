"""Read-only Blender reopen check for the relocated integration fixture kit."""

import bpy, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import native
from core import save, require

request = json.loads(Path(sys.argv[sys.argv.index("--") + 1]).read_text())
job = json.loads(Path(request["job"]).read_text())
native.FACTS = job["facts"]
scene = bpy.data.scenes[request["scene"]]
result = native.inspect_edit(scene, job["config"], Path(request["loop"]))
require(
    all(Path(x).resolve() == Path(request["loop"]).resolve() for x in result["links"]),
    "Relocated picture escaped kit",
)
require(
    any(getattr(w, "sequencer_scene", None) == scene for w in bpy.data.workspaces),
    "Missing native sequencer workspace binding",
)
save(request["report"], {"state": "RELOCATED_NATIVE_REOPEN_PASSED", **result})
