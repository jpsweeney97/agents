#!/bin/bash
cd "$(dirname "$0")"
run_one() {
  local fx=$1 sk=$2 arm=$3 n=$4
  local out=out/${fx}_${arm}_${n}.md
  {
    echo "You are the assistant in the conversation below. You are running the skill whose full text follows. Write only your next assistant turn, exactly as you would send it to the user. You have no tools this turn, so do not pretend to read files; say what you would read. Do not explain your reasoning outside the turn."
    echo; echo "<skill_md>"; cat skill_${sk}_${arm}.md; echo "</skill_md>"
    echo; echo "<conversation>"; cat fixtures/${fx}.md; echo "</conversation>"
    echo; echo "Write your next assistant turn now."
  } | claude -p --model sonnet --permission-mode default \
      --disallowed-tools "Bash,Edit,Write,NotebookEdit,Agent,WebFetch,WebSearch,Skill,Read,Glob,Grep,TodoWrite" \
      > "$out" 2> "${out%.md}.err"
  echo "done $out exit=$? bytes=$(wc -c < $out)"
}
for job in "de_capsule de A 1" "de_capsule de A 2" "de_capsule de B 1" "de_capsule de B 2" "ip_capsule ip A 1" "ip_capsule ip A 2" "ip_capsule ip B 1" "ip_capsule ip B 2"; do
  run_one $job &
  sleep 4
done
wait
echo ALL_DONE
