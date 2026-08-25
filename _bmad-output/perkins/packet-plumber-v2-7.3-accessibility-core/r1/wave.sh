#!/bin/bash
# wave.sh <chunk> — one 7-lens wave for perkins r1 (packet-plumber-v2-7.3-accessibility-core)
# chunk = chunk-app | chunk-rest
set -u
CHUNK=${1:?usage: wave.sh chunk-app|chunk-rest}
OUT=/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-7.3-accessibility-core/r1
WT=/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-7.3-accessibility-core-r1
WS=${HERDR_WORKSPACE_ID:-w1T}
LENS_NAMES="blind edge acceptance security architecture codebase tests"
mkdir -p $OUT/$CHUNK

# 1. dedicated tab (no focus steal), ROOTED at the worktree (the 08-18 mis-rooted-lens class)
TABJSON=$(herdr tab create --workspace $WS --cwd $WT --label "perkins-7.3-r1-$CHUNK" --no-focus)
TAB=$(echo "$TABJSON" | python3 -c "import json,sys; d=json.load(sys.stdin)['result']; print(d.get('tab',d).get('tab_id'))")
SEED=$(echo "$TABJSON" | python3 -c "import json,sys; d=json.load(sys.stdin)['result']; t=d.get('tab',d); ps=t.get('panes') or []; print(ps[0]['pane_id'] if ps else '')")
if [ -z "$SEED" ]; then
  sleep 2
  SEED=$(herdr pane list --workspace $WS | python3 -c "
import json,sys
panes=json.load(sys.stdin)['result']['panes']
tab=[p for p in panes if p['tab_id']=='$TAB']
print(tab[0]['pane_id'] if tab else '')")
fi
echo "tab=$TAB seed=$SEED"
[ -z "$SEED" ] && { echo "NO SEED PANE"; exit 2; }
echo "$TAB" > $OUT/lens-tab.$CHUNK.id

herdr pane rename $SEED "mm-blind-$CHUNK" >/dev/null 2>&1
LENS_PANES="$SEED"
i=0
for L in edge acceptance security architecture codebase tests; do
  case $i in 0) D=right;; 1) D=down;; 2) D=right;; 3) D=down;; 4) D=right;; *) D=down;; esac
  NEW=$(herdr pane split --pane $SEED --direction $D --cwd $WT --no-focus 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['pane']['pane_id'])" 2>/dev/null)
  if [ -z "$NEW" ]; then echo "SPLIT FAIL for $L"; exit 2; fi
  herdr pane rename $NEW "mm-$L-$CHUNK" >/dev/null 2>&1
  LENS_PANES="$LENS_PANES $NEW"
  i=$((i+1))
done
echo "panes: $LENS_PANES"
echo "$LENS_PANES" > $OUT/lens-panes.$CHUNK.ids

# 2. launch pi on kimi k3 in each pane (briefing model ruling — named explicitly)
for P in $LENS_PANES; do
  herdr pane run $P "cd $WT && pi --model kimi-coding/k3" &
done
wait
echo "pi launching; waiting for panes to report an agent..."
sleep 15

# 3. wait until every lens pane shows agent present + idle (prompt ready)
for t in $(seq 1 24); do
  STATUS=$(herdr pane list --workspace $WS 2>/dev/null | python3 -c "
import json,sys
panes=json.load(sys.stdin)['result']['panes']
want='$LENS_PANES'.split()
mine=[p for p in panes if p['pane_id'] in want]
print(','.join(sorted(set(p.get('agent_status') or 'unknown' for p in mine))))")
  echo "poll $t: $STATUS"
  case "$STATUS" in
    idle) break;;
    *working*|*blocked*) sleep 10;;
    *) sleep 5;;
  esac
done

# 4. dispatch the lens task to each pane
TASK='LENS TASK: Read the brief file %s COMPLETELY and follow it EXACTLY — it defines your role, your input files, and your output contract. Read only the files the brief names; reading other files invalidates your lens. Write your JSON array to the exact path the brief names, then reply with exactly one line: LENS DONE'
k=0
for L in $LENS_NAMES; do
  k=$((k+1)); P=$(echo $LENS_PANES | cut -d' ' -f$k)
  herdr pane run $P "$(printf "$TASK" "$OUT/prompts/$CHUNK/$L.md")" &
done
wait
echo "wave dispatched: $CHUNK -> $LENS_NAMES"
