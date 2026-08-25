#!/bin/bash
# recover-stdout.sh — watch for lens stdout logs that parse as JSON but whose
# .json file is missing (the architecture-lens file-write flake, r2/r3-precedent),
# and recover them. Runs until all 7*6 json files exist or 90 min elapse.
R4=/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-5.11-terminal-types/r4
LO=$R4/lens-out
END=$(( $(date +%s) + 5400 ))
while [ "$(date +%s)" -lt "$END" ]; do
  for w in code g1 g2 g3 g4 g5; do
    for l in blind edge acceptance security architecture codebase tests; do
      j="$LO/$l-$w.json"; s="$LO/$l-$w.stdout.log"
      [ -f "$j" ] && continue
      [ -f "$s" ] || continue
      if python3 -c "import json,sys; a=json.load(open(sys.argv[1])); assert isinstance(a,list)" "$s" 2>/dev/null; then
        python3 -c "import json; json.dump(json.load(open('$s')), open('$j','w'), indent=2)" 2>/dev/null \
          && echo "$(date +%H:%M:%S) RECOVERED $l-$w.json from stdout (len $(python3 -c "import json;print(len(json.load(open('$j'))))" 2>/dev/null))"
      fi
    done
  done
  sleep 30
done
echo "$(date +%H:%M:%S) recovery watcher finished"
