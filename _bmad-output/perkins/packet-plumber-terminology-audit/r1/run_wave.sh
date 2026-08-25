#!/usr/bin/env bash
# Perkins r1 wave runner — one chunk's 7-lens wave. Usage: SPAWNER=<pane> run_wave.sh <chunk>
set -uo pipefail
CHUNK="$1"
R="/Users/moses/code/_bmad-output/perkins/packet-plumber-terminology-audit/r1"
WT="/Users/moses/.herdr/worktrees/packet-plumber/perkins-pp-terminology-audit-r1"
LENSES="blind edge acceptance security architecture codebase tests"
MODEL="${MODEL:-deepseek/deepseek-v4-flash}"
MAP="/tmp/pp-r1-wave-$CHUNK.panes"
: > "$MAP"

jid() { python3 -c "import sys,json;print(json.load(sys.stdin)$1)"; }
pane_of() { grep "^$1 " "$MAP" | cut -d' ' -f2; }

i=0
for lens in $LENSES; do
  dir=$([ $((i % 2)) -eq 0 ] && echo right || echo down)
  pid=$(herdr pane split "$SPAWNER" --direction "$dir" --no-focus --cwd "$WT" | jid '["result"]["pane"]["pane_id"]')
  herdr pane rename "$pid" "mm-${lens}-${CHUNK}-r1" >/dev/null
  herdr pane run "$pid" "pi --model $MODEL" >/dev/null
  echo "$lens $pid" >> "$MAP"
  i=$((i+1))
done
echo "spawned: $(cat "$MAP" | tr '\n' ' ')"

wait_status() { # $1 pane, $2 timeout_s, $3 statuses(comma)
  local deadline=$(( $(date +%s) + $2 )) st
  while [ "$(date +%s)" -lt "$deadline" ]; do
    st=$(herdr pane get "$1" | jid '["result"]["pane"]["agent_status"]' 2>/dev/null)
    case ",$3," in *",$st,"*) echo "$st"; return 0;; esac
    sleep 4
  done
  echo "timeout"; return 1
}

for lens in $LENSES; do
  s=$(wait_status "$(pane_of $lens)" 120 "idle,working,blocked")
  [ "$s" = "timeout" ] && echo "BOOT-TIMEOUT $lens"
done
for lens in $LENSES; do
  herdr pane run "$(pane_of $lens)" "Read $R/prompts/${lens}-${CHUNK}.md and follow it exactly." >/dev/null
done
echo "dispatched all 7"

for lens in $LENSES; do
  s=$(wait_status "$(pane_of $lens)" 900 "done,idle,blocked")
  echo "lens $lens -> $s"
done

for lens in $LENSES; do
  f="$R/${lens}-${CHUNK}.json"
  if [ ! -f "$f" ]; then echo "MISSING $lens"; continue; fi
  python3 -c "import json;d=json.load(open('$f'));assert isinstance(d,list);print('OK $lens',len(d),'findings')" 2>/dev/null || echo "BADJSON $lens"
done

for lens in $LENSES; do herdr pane close "$(pane_of $lens)" >/dev/null 2>&1; done
echo "wave $CHUNK closed"
