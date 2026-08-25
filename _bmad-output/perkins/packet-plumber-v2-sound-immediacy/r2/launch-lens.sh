#!/bin/sh
lens="$1"
exec pi --model zai-coding-cn/glm-5.3 --thinking max "$(cat "/Users/moses/code/_bmad-output/perkins/packet-plumber-v2-sound-immediacy/r2/prompt-$lens.txt")"
