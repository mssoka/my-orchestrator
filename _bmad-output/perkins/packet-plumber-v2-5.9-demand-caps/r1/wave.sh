#!/bin/bash
# wave.sh — one 7-lens wave for perkins r1 (packet-plumber-v2-5.9-demand-caps; single chunk: lens-diff.patch 1465 lines + golden-manifest.txt)
set -u
OUT=/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.9-demand-caps/r1
WT=/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.9-demand-caps-r1
WS=w1T
LENS_NAMES="blind edge acceptance security architecture codebase tests"

# 1. dedicated tab (no focus steal) -> its first pane becomes mm-blind-r1
TABJSON=$(herdr tab create --workspace $WS --cwd $WT --label "perkins-5.9-r1-lenses" --no-focus)
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
echo "$TAB" > $OUT/lens-tab.id

herdr pane rename $SEED "mm-blind-r1" >/dev/null 2>&1
LENS_PANES="$SEED"
i=0
for L in edge acceptance security architecture codebase tests; do
  case $i in 0) D=right;; 1) D=down;; 2) D=right;; 3) D=down;; 4) D=right;; *) D=down;; esac
  NEW=$(herdr pane split --pane $SEED --direction $D --cwd $WT --no-focus 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['pane']['pane_id'])" 2>/dev/null)
  if [ -z "$NEW" ]; then echo "SPLIT FAIL for $L"; exit 2; fi
  herdr pane rename $NEW "mm-$L-r1" >/dev/null 2>&1
  LENS_PANES="$LENS_PANES $NEW"
  i=$((i+1))
done
echo "panes: $LENS_PANES"
echo "$LENS_PANES" > $OUT/lens-panes.ids

# 2. launch pi in each pane
for P in $LENS_PANES; do
  herdr pane run $P "cd $WT && pi --model zai-coding-cn/glm-5.3" &
done
wait
echo "pi launching; waiting for all panes to report an agent..."
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
  herdr pane run $P "$(printf "$TASK" "$OUT/prompts/$L.md")" &
done
wait
echo "wave dispatched: $LENS_NAMES"
