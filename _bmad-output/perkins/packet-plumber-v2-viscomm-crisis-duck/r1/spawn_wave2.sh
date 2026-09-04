#!/bin/bash
# Wave 2: exit stale pi, boot fresh (fresh context per lens), hand over c2
PANES=(w85:p13 w85:p16 w85:p18 w85:p15 w85:p17 w85:p19 w85:p14)
LENSES=(blind edge acceptance security architecture codebase tests)
CHUNK=c2
PROMPT_DIR=/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-viscomm-crisis-duck/r1/lens-prompts

echo "== exiting stale pi sessions =="
i=0
while [ $i -lt 7 ]; do
  herdr pane run "${PANES[$i]}" "/exit" >/dev/null 2>&1
  i=$((i+1))
done
sleep 8

echo "== booting fresh pi (glm-5.3, thinking max) =="
i=0
while [ $i -lt 7 ]; do
  herdr pane rename "${PANES[$i]}" "mm-${LENSES[$i]}-$CHUNK" >/dev/null 2>&1
  herdr pane run "${PANES[$i]}" "pi --model zai-coding-cn/glm-5.3 --thinking max" >/dev/null 2>&1
  i=$((i+1))
done
sleep 14

echo "== wait idle + hand over =="
i=0
while [ $i -lt 7 ]; do
  p=${PANES[$i]}; l=${LENSES[$i]}
  herdr agent wait "$p" --until idle --timeout 120000 >/dev/null 2>&1
  rc=$?
  [ $rc -ne 0 ] && echo "WARN: wait $p rc=$rc"
  sleep 3
  herdr pane run "$p" "Read $PROMPT_DIR/$l-$CHUNK.md and execute it exactly. Begin." >/dev/null 2>&1
  echo "handed over $p -> mm-$l-$CHUNK"
  i=$((i+1))
done

echo "== delivery check =="
sleep 20
i=0
while [ $i -lt 7 ]; do
  p=${PANES[$i]}; l=${LENSES[$i]}
  out=$(herdr pane read "$p" 2>/dev/null | grep -c "lens-prompts/$l-$CHUNK.md")
  echo "$p mm-$l-$CHUNK prompt-seen=$out"
  i=$((i+1))
done
