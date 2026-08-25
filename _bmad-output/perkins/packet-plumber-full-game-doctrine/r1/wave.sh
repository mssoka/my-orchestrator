#!/bin/bash
# wave.sh — one 7-lens wave for packet-plumber-full-game-doctrine perkins r1 (single chunk: diff.patch 427 lines)
set -u
OUT=/Users/moses/code/_bmad-output/perkins/packet-plumber-full-game-doctrine/r1
WT=/Users/moses/.herdr/worktrees/packet-plumber/perkins-full-game-doctrine-r1
WS=w1T
LENS_NAMES="blind edge acceptance security architecture codebase tests"

# 1. dedicated tab (no focus steal) -> its first pane becomes mm-blind-r1
TABJSON=$(herdr tab create --workspace $WS --cwd $WT --label "perkins-fgd-r1-lenses" --no-focus)
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

# 2. launch pi in each lens pane
k=0
for L in $LENS_NAMES; do
  k=$((k+1)); P=$(echo $LENS_PANES | cut -d' ' -f$k)
  herdr pane run $P "cd $WT && pi --model zai-coding-cn/glm-5.3" &
done
wait; sleep 20

# 3. wait for all lens panes to reach idle (pi started)
for t in $(seq 1 30); do
  STATUS=$(herdr pane list --workspace $WS 2>/dev/null | python3 -c "
import json,sys
panes=json.load(sys.stdin)['result']['panes']
tab=[p for p in panes if p['tab_id']=='$TAB']
print(','.join(sorted(set(p.get('agent_status') or 'unknown' for p in tab))))")
  echo "poll $t: $STATUS"
  case "$STATUS" in *working*|*blocked*|*unknown*) sleep 10;; *) break;; esac
done

# 4. dispatch the lens task
TASK='LENS TASK: Read the brief file %s COMPLETELY and follow it EXACTLY — it defines your role, your input files, and your output contract. Read only the files the brief names; reading other files invalidates your lens. Write your JSON array to the exact path the brief names, then reply with exactly one line: LENS DONE'
k=0
for L in $LENS_NAMES; do
  k=$((k+1)); P=$(echo $LENS_PANES | cut -d' ' -f$k)
  herdr pane run $P "$(printf "$TASK" "$OUT/prompts/$L.md")" &
done
wait
echo "wave dispatched — tab=$TAB panes=$LENS_PANES"
