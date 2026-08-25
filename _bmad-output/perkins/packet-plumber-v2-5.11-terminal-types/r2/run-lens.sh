#!/bin/bash
# run-lens.sh <wave> <lens> <model> — runs inside a herdr lens pane (cwd = round worktree)
W=$1; L=$2; M=${3:-zai-coding-cn/glm-5.3}
OUT=/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.11-terminal-types/r2
LOG="$OUT/lens-out/$L-$W.stdout.log"
P="$OUT/prompts/$W-$L.md"
cd /Users/moses/.herdr/worktrees/packet-plumber/perkins-v2-5.11-terminal-types-r2 || exit 9
pi --print --no-session --model "$M" "$(cat "$P")" > "$LOG" 2>&1
rc=$?
echo "LENS-DONE rc=$rc lens=$L wave=$W model=$M"
