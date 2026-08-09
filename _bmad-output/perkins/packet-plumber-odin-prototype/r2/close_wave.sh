#!/usr/bin/env bash
# close_wave.sh <chunk-letter> — close the wave's lens panes, NEVER the holder.
set -uo pipefail
L="$1"
herdr pane list --workspace w1T | python3 -c "
import json,sys
for p in json.load(sys.stdin)['result']['panes']:
    if p.get('label','').endswith('-$L-r2') and p.get('label','').startswith('mm-'):
        print(p['pane_id'])" | while read -r p; do
  herdr pane close "$p" >/dev/null 2>&1 && echo "closed $p"
done
