#!/bin/bash
cd /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r3
pi -p --model zai-coding-cn/glm-5.2 --no-session --name "mm-blind-r3" "You are the Blind Hunter code-review lens (Perkins automated review round 3). Read the lens brief at /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r3/lens-briefs/blind.md and follow its instructions EXACTLY. Read ONLY the brief and the single diff file it names; do NOT read any repository file, do NOT cd into the worktree (your isolation depends on this). Write ONLY your JSON array to /Users/moses/code/_bmad-output/perkins/righttenantry-refcheck-rc3-4/r3/blind.json and stop. An empty array is a valid, honest answer when nothing is wrong."
echo "BLIND_DONE_0"
