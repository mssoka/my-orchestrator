#!/bin/bash
# Perkins lens wave spawner — bash 3.2 safe (indexed arrays only)
# usage: spawn_wave.sh <chunk-id> <pane1> <lens1> <pane2> <lens2> ...
CHUNK=$1; shift
NP=$(( $# / 2 ))
PANES=(); LENSES=()
while [ $# -gt 0 ]; do PANES+=("$1"); LENSES+=("$2"); shift 2; done
PROMPT_DIR=/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-viscomm-crisis-duck/r1/lens-prompts

echo "== booting $NP lens panes (model pinned glm-5.3, thinking max) =="
i=0
while [ $i -lt $NP ]; do
  p=${PANES[$i]}; l=${LENSES[$i]}
  herdr pane rename "$p" "mm-$l-$CHUNK" >/dev/null 2>&1
  herdr pane run "$p" "pi --model zai-coding-cn/glm-5.3 --thinking max" >/dev/null 2>&1
  i=$((i+1))
done

sleep 12

echo "== waiting idle + handing over =="
i=0
while [ $i -lt $NP ]; do
  p=${PANES[$i]}; l=${LENSES[$i]}
  herdr agent wait "$p" --until idle --timeout 90000 >/dev/null 2>&1
  rc=$?
  if [ $rc -ne 0 ]; then echo "WARN: wait $p rc=$rc (polling anyway)"; fi
  sleep 3
  herdr pane run "$p" "Read $PROMPT_DIR/$l-$CHUNK.md and execute it exactly. Begin." >/dev/null 2>&1
  echo "handed over $p -> mm-$l-$CHUNK"
  i=$((i+1))
done

echo "== verifying handover delivery =="
sleep 20
i=0
while [ $i -lt $NP ]; do
  p=${PANES[$i]}; l=${LENSES[$i]}
  out=$(herdr pane read "$p" 2>/dev/null | grep -c "lens-prompts/$l-$CHUNK.md")
  echo "$p mm-$l-$CHUNK prompt-seen=$out"
  i=$((i+1))
done
