#!/bin/bash
# wave-orchestrator.sh — dispatches waves sequentially as each wave's JSONs land (r4)
R4=/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.11-terminal-types/r4
RL=$R4/run-lens.sh
# pane ids exported by the caller (stable lens->pane assignment)
: "${P_blind:?}" "${P_edge:?}" "${P_acceptance:?}" "${P_security:?}" "${P_architecture:?}" "${P_codebase:?}" "${P_tests:?}"

wave_done() { # wave -> 0 if all 7 jsons exist and parse
  local f n=0
  for L in blind edge acceptance security architecture codebase tests; do
    f="$R4/lens-out/$L-$1.json"
    [ -f "$f" ] && python3 -c "import json,sys; a=json.load(open(sys.argv[1])); assert isinstance(a,list)" "$f" 2>/dev/null && n=$((n+1))
  done
  [ $n -eq 7 ]
}

lens_ok() { # lens wave -> 0 if json exists+parses
  [ -f "$R4/lens-out/$1-$2.json" ] && python3 -c "import json,sys; a=json.load(open(sys.argv[1])); assert isinstance(a,list)" "$R4/lens-out/$1-$2.json" 2>/dev/null
}

mark() { touch "$R4/lens-out/.dispatched-$1-$2"; }
was()   { [ -f "$R4/lens-out/.dispatched-$1-$2" ]; }
retry() { [ -f "$R4/lens-out/.retried-$1-$2" ]; }
markretry() { touch "$R4/lens-out/.retried-$1-$2"; }

pane_of() { case $1 in
  blind) echo "$P_blind";; edge) echo "$P_edge";; acceptance) echo "$P_acceptance";;
  security) echo "$P_security";; architecture) echo "$P_architecture";;
  codebase) echo "$P_codebase";; tests) echo "$P_tests";; esac; }

for WAVE in code g1 g2 g3 g4 g5; do
  # wait for previous wave complete (code wave dispatches immediately)
  if [ "$WAVE" != code ]; then
    PREV=code; case $WAVE in g1) PREV=code;; g2) PREV=g1;; g3) PREV=g2;; g4) PREV=g3;; g5) PREV=g4;; esac
    while ! wave_done $PREV; do sleep 20; done
  fi
  # dispatch every lens not yet dispatched
  for L in blind edge acceptance security architecture codebase tests; do
    if ! was $L $WAVE; then
      herdr pane run "$(pane_of $L)" "bash $RL $WAVE $L" >/dev/null 2>&1
      mark $L $WAVE
      echo "$(date +%H:%M:%S) dispatched $L-$WAVE on $(pane_of $L)"
    fi
  done
  # wait for this wave; one retry per failed lens
  while ! wave_done $WAVE; do
    sleep 20
    for L in blind edge acceptance security architecture codebase tests; do
      # only retry a lens whose pane is finished (stdout log carries LENS-DONE) but json missing/invalid
      if ! lens_ok $L $WAVE && ! retry $L $WAVE; then
        if grep -q "LENS-DONE" "$R4/lens-out/$L-$WAVE.stdout.log" 2>/dev/null; then
          echo "$(date +%H:%M:%S) RETRY $L-$WAVE (pane finished, json missing/invalid)"
          herdr pane run "$(pane_of $L)" "bash $RL $WAVE $L" >/dev/null 2>&1
          markretry $L $WAVE
        fi
      fi
    done
  done
  echo "$(date +%H:%M:%S) WAVE $WAVE COMPLETE"
done
echo "$(date +%H:%M:%S) ALL WAVES COMPLETE"
