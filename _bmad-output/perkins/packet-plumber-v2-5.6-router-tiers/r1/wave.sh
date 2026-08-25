#!/bin/bash
# wave.sh <chunk> <seed-pane> — run one 7-lens wave on a diff chunk, validate, close all but seed.
set -u
CHUNK=$1; SEED=$2
OUT=/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.6-router-tiers/r1
WT=/Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.6-router-tiers-r1
LENS_NAMES="blind edge acceptance security architecture codebase tests"
LENS_PANES=""

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

k=0
for L in $LENS_NAMES; do
  k=$((k+1)); P=$(echo $LENS_PANES | cut -d' ' -f$k)
  herdr pane run $P "cd $WT && pi --model deepseek/deepseek-v4-pro" &
done
wait; sleep 15

for t in $(seq 1 20); do
  STATUS=$(herdr pane list --workspace w1T 2>/dev/null | python3 -c "
import json,sys
panes=json.load(sys.stdin)['result']['panes']
tab=[p for p in panes if p['tab_id']=='w1T:tB2']
print(','.join(sorted(set(p['agent_status'] for p in tab))))")
  case "$STATUS" in *working*|*blocked*) sleep 10;; *) break;; esac
done

TASK="LENS TASK: Read the brief file $OUT/prompts/%s-$CHUNK.txt COMPLETELY and follow it EXACTLY — it defines your role, your input files, and your output contract. Read only the files the brief names; reading other files invalidates your lens. Write your JSON array to the exact path the brief names, then reply with exactly one line: LENS DONE"
k=0
for L in $LENS_NAMES; do
  k=$((k+1)); P=$(echo $LENS_PANES | cut -d' ' -f$k)
  herdr pane run $P "$(printf "$TASK" $L)" &
done
wait

MISSING=""
for t in $(seq 1 24); do
  MISSING=""
  for L in $LENS_NAMES; do
    [ -s "$OUT/$L-$CHUNK.json" ] || MISSING="$MISSING $L"
  done
  [ -z "$MISSING" ] && break
  sleep 25
done
if [ -n "$MISSING" ]; then echo "WAVE $CHUNK TIMEOUT, missing:$MISSING"; else echo "WAVE $CHUNK all files present"; fi

for L in $LENS_NAMES; do
  F="$OUT/$L-$CHUNK.json"
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
    open(path,"w").write(json.dumps(d, indent=2, ensure_ascii=False))
    print(f"OK {path.split('/')[-1]}: array len {len(d)}")
except Exception as e:
    print(f"INVALID {path.split('/')[-1]}: {e}")
    sys.exit(1)
EOF
  echo "  rc=$?"
done

sleep 10
k=0
for L in $LENS_NAMES; do
  k=$((k+1)); P=$(echo $LENS_PANES | cut -d' ' -f$k)
  [ "$L" = "blind" ] && continue
  herdr pane close $P >/dev/null 2>&1
done
echo "WAVE $CHUNK DONE, seed=$SEED"
