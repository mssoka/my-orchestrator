#!/bin/bash
# wave-r1.sh — Perkins r1 lens wave for packet-plumber-v2-5.3-pause-anywhere.
# Creates a dedicated tab, splits 7 lens panes (mm-<lens>-r1), launches
# pi --model zai-coding-cn/glm-5.3 in each, dispatches the lens briefs,
# waits for the 7 JSON outputs, validates them. Panes are closed by Perkins
# after the verification pass (not here) so retries can reuse the tab.
set -u
OUT=/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.3-pause-anywhere/r1
WT=/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.3-pause-anywhere-r1
MODEL="zai-coding-cn/glm-5.3"
LENS_NAMES="blind edge acceptance security architecture codebase tests"

TAB_JSON=$(herdr tab create --workspace w1T --cwd "$WT" --label "perkins-5.3-lenses-r1" --no-focus 2>/dev/null)
TAB=$(echo "$TAB_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['tab']['tab_id'])")
SEED=$(echo "$TAB_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['root_pane']['pane_id'])")
if [ -z "$TAB" ] || [ -z "$SEED" ]; then echo "TAB CREATE FAIL"; exit 2; fi
echo "TAB=$TAB SEED=$SEED"

herdr pane rename "$SEED" "mm-blind-r1" >/dev/null 2>&1
LENS_PANES="$SEED"
i=0
for L in edge acceptance security architecture codebase tests; do
  case $i in 0) D=right;; 1) D=down;; 2) D=right;; 3) D=down;; 4) D=right;; *) D=down;; esac
  NEW=$(herdr pane split --pane "$SEED" --direction $D --cwd "$WT" --no-focus 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['pane']['pane_id'])" 2>/dev/null)
  if [ -z "$NEW" ]; then echo "SPLIT FAIL for $L"; exit 2; fi
  herdr pane rename "$NEW" "mm-$L-r1" >/dev/null 2>&1
  LENS_PANES="$LENS_PANES $NEW"
  i=$((i+1))
done
echo "PANES: $LENS_PANES"

k=0
for L in $LENS_NAMES; do
  k=$((k+1)); P=$(echo $LENS_PANES | cut -d' ' -f$k)
  herdr pane run $P "cd $WT && pi --model $MODEL" &
done
wait
echo "launched; waiting for pi readiness"
sleep 20

TASK="LENS TASK: Read the brief file $OUT/prompts/%s.txt COMPLETELY and follow it EXACTLY — it defines your role, your input files, and your output contract. Read only the files the brief names; reading other files invalidates your lens. Write your JSON array to the exact path the brief names, then reply with exactly one line: LENS DONE"
k=0
for L in $LENS_NAMES; do
  k=$((k+1)); P=$(echo $LENS_PANES | cut -d' ' -f$k)
  herdr pane run $P "$(printf "$TASK" $L)" &
done
wait
echo "dispatched; polling for outputs"

MISSING=""
for t in $(seq 1 60); do
  MISSING=""
  for L in $LENS_NAMES; do
    [ -s "$OUT/$L-r1.json" ] || MISSING="$MISSING $L"
  done
  [ -z "$MISSING" ] && break
  sleep 30
done
if [ -n "$MISSING" ]; then
  echo "WAVE TIMEOUT, missing:$MISSING"
else
  echo "WAVE all files present"
fi

for L in $LENS_NAMES; do
  F="$OUT/$L-r1.json"
  [ -s "$F" ] || continue
  python3 - "$F" <<'EOF'
import json, sys
path = sys.argv[1]
raw = open(path).read()
out=[]; in_str=False; esc=False
for ch in raw:
    if in_str:
        if esc: out.append(ch); esc=False; continue
        if ch=='\\': out.append(ch); esc=True; continue
        if ch=='"': in_str=False; out.append(ch); continue
        if ord(ch)<32: out.append('\\n' if ch=='\n' else '\\t' if ch=='\t' else f'\\u{ord(ch):04x}')
        else: out.append(ch)
    else:
        if ch=='"': in_str=True
        out.append(ch)
s="".join(out)
try:
    d=json.loads(s)
    assert isinstance(d, list)
    open(path,"w").write(json.dumps(d, indent=2, ensure_ascii=False))
    print(f"OK {path.split('/')[-1]}: array len {len(d)}")
except Exception as e:
    print(f"INVALID {path.split('/')[-1]}: {e}")
    sys.exit(1)
EOF
  echo "  rc=$?"
done
echo "TAB=$TAB" > /tmp/perkins53_tab.env
echo "PANES=$LENS_PANES" >> /tmp/perkins53_tab.env
echo "WAVE DONE"
