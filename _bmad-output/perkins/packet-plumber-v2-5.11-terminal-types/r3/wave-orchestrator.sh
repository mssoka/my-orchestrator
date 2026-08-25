#!/bin/bash
# wave-orchestrator.sh — dispatches waves g2..g6 per-pane as the current wave's JSON lands
R3=/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.11-terminal-types/r3
RL=$R3/run-lens.sh
declare_panes() { :; }
# pane assignment (same lens per pane all round)
P_blind=w1T:p25N; P_edge=w1T:p25P; P_acc=w1T:p25Q; P_sec=w1T:p25R
P_arch=w1T:p25S; P_cb=w1T:p25T; P_tests=w1T:p25V

wave_done() { # lens wave -> 0 if json exists and parses
  local f="$R3/lens-out/$1-$2.json"
  [ -f "$f" ] && python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$f" 2>/dev/null
}

mark_dispatched() { # lens wave
  touch "$R3/lens-out/.dispatched-$1-$3"
}

was_dispatched() { [ -f "$R3/lens-out/.dispatched-$1-$2" ]; }

for WAVE in g2 g3 g4 g5 g6; do
  # wait until all 7 lenses of the PREVIOUS wave have landed
  PREV=g1; case $WAVE in g3) PREV=g2;; g4) PREV=g3;; g5) PREV=g4;; g6) PREV=g5;; esac
  while true; do
    n=0
    for L in blind edge acceptance security architecture codebase tests; do
      wave_done $L $PREV && n=$((n+1))
    done
    [ $n -eq 7 ] && break
    sleep 20
  done
  for L in blind edge acceptance security architecture codebase tests; do
    if ! was_dispatched $L $WAVE; then
      case $L in
        blind)        P=$P_blind;;
        edge)         P=$P_edge;;
        acceptance)   P=$P_acc;;
        security)     P=$P_sec;;
        architecture) P=$P_arch;;
        codebase)     P=$P_cb;;
        tests)        P=$P_tests;;
      esac
      herdr pane run "$P" "bash $RL $WAVE $L" >/dev/null 2>&1
      mark_dispatched $L $WAVE
      echo "$(date +%H:%M:%S) dispatched $L-$WAVE on $P"
    fi
  done
done
echo "$(date +%H:%M:%S) ALL WAVES DISPATCHED"
