/^diff --git / { if (file) close(file); f=$3; sub(/^a\//,"",f); gsub(/\//,"_",f); file="chunks/_f_" f; print > file }
{ if (file) print > file }
