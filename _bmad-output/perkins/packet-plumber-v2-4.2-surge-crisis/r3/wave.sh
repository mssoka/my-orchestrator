#!/usr/bin/env bash
# Wave launcher for Perkins r3 lenses. Usage: wave.sh <chunk>
# Closes panes labeled mm-*-r3-*, creates a fresh tab, launches 7 lens panes,
# hands over the briefs. Panes stay open for the caller to poll.
set -u
CHUNK="$1"
B=/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-4.2-surge-crisis/r3/briefs

# 1. close existing lens panes (any label containing "mm-" and "-r3-")
for P in $(herdr pane list --workspace w1T 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
for p in d['result']['panes']:
    l=p.get('label') or ''
    if 'mm-' in l and '-r3-' in l:
        print(p['pane_id'])"); do
  herdr pane close "$P" >/dev/null 2>&1
done
sleep 2

# 2. new tab
TAB=$(herdr tab create --workspace w1T --label perkins-pp-4.2-r3-$CHUNK --no-focus 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['tab']['tab_id'])")
P1=$(herdr pane list --workspace w1T 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
for p in d['result']['panes']:
    if p['tab_id']=='$TAB': print(p['pane_id']); break")

# 3. label + split
herdr pane rename "$P1" "mm-blind-r3-$CHUNK" >/dev/null
P2=$(herdr pane split "$P1" --direction right --no-focus 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['pane']['pane_id'])")
P3=$(herdr pane split "$P1" --direction down --no-focus 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['pane']['pane_id'])")
P4=$(herdr pane split "$P1" --direction down --no-focus 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['pane']['pane_id'])")
P5=$(herdr pane split "$P1" --direction down --no-focus 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['pane']['pane_id'])")
P6=$(herdr pane split "$P1" --direction down --no-focus 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['pane']['pane_id'])")
P7=$(herdr pane split "$P1" --direction down --no-focus 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['pane']['pane_id'])")
herdr pane rename "$P2" "mm-edge-r3-$CHUNK" >/dev/null
herdr pane rename "$P3" "mm-acceptance-r3-$CHUNK" >/dev/null
herdr pane rename "$P4" "mm-security-r3-$CHUNK" >/dev/null
herdr pane rename "$P5" "mm-architecture-r3-$CHUNK" >/dev/null
herdr pane rename "$P6" "mm-codebase-r3-$CHUNK" >/dev/null
herdr pane rename "$P7" "mm-tests-r3-$CHUNK" >/dev/null

# 4. launch pi in each
for P in "$P1" "$P2" "$P3" "$P4" "$P5" "$P6" "$P7"; do
  herdr pane run "$P" "pi --model deepseek/deepseek-v4-pro"
done

# 5. wait for idle, hand over
sleep 25
herdr pane run "$P1" "Read $B/brief-$CHUNK-blind.md and execute it. Your deliverable is the JSON file named in its FILE-OUTPUT CONTRACT. Do not copy the repo anywhere — work in place, read-only."
herdr pane run "$P2" "Read $B/brief-$CHUNK-edge.md and execute it. Your deliverable is the JSON file named in its FILE-OUTPUT CONTRACT. Do not copy the repo anywhere — work in place, read-only."
herdr pane run "$P3" "Read $B/brief-$CHUNK-acceptance.md and execute it. Your deliverable is the JSON file named in its FILE-OUTPUT CONTRACT. Do not copy the repo anywhere — work in place, read-only."
herdr pane run "$P4" "Read $B/brief-$CHUNK-security.md and execute it. Your deliverable is the JSON file named in its FILE-OUTPUT CONTRACT. Do not copy the repo anywhere — work in place, read-only."
herdr pane run "$P5" "Read $B/brief-$CHUNK-architecture.md and execute it. Your deliverable is the JSON file named in its FILE-OUTPUT CONTRACT. Do not copy the repo anywhere — work in place, read-only."
herdr pane run "$P6" "Read $B/brief-$CHUNK-codebase.md and execute it. Your deliverable is the JSON file named in its FILE-OUTPUT CONTRACT. Do not copy the repo anywhere — work in place, read-only."
herdr pane run "$P7" "Read $B/brief-$CHUNK-tests.md and execute it. Your deliverable is the JSON file named in its FILE-OUTPUT CONTRACT. Do not copy the repo anywhere — work in place, read-only."
echo "wave $CHUNK launched: $P1 $P2 $P3 $P4 $P5 $P6 $P7 (tab $TAB)"
