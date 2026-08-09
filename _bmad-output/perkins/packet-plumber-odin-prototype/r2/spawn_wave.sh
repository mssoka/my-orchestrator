#!/usr/bin/env bash
# spawn_wave.sh <chunk-letter> — ensure a lens tab + holder pane exist, then
# split 7 lens panes off the holder, launch pi, submit the prompt pointer.
set -uo pipefail
L="$1"
R2=/Users/moses/code/_bmad-output/perkins/packet-plumber-odin-prototype/r2

HOLDER=$(herdr pane list --workspace w1T | python3 -c "
import json,sys
for p in json.load(sys.stdin)['result']['panes']:
    if p.get('label') == 'perkins-r2-holder':
        print(p['pane_id']); break" 2>/dev/null)
if [ -z "${HOLDER:-}" ]; then
  HOLDER=$(herdr tab create --workspace w1T --no-focus | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['root_pane']['pane_id'])")
  herdr pane rename "$HOLDER" "perkins-r2-holder" >/dev/null
  echo "holder recreated: $HOLDER"
fi

DIR=down
for lens in blind edge acceptance security architecture codebase tests; do
  pane=$(herdr pane split "$HOLDER" --direction $DIR --no-focus | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['pane']['pane_id'])" 2>/dev/null)
  if [ -z "$pane" ]; then echo "SPLIT-FAIL $lens-$L"; continue; fi
  [ "$DIR" = down ] && DIR=right || DIR=down
  herdr pane rename "$pane" "mm-$lens-$L-r2" >/dev/null
  herdr pane run "$pane" "pi" >/dev/null
  echo "$lens $pane"
done
