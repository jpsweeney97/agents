#!/bin/bash
cd "$(dirname "$0")"
run_one() {
  local fx=$1 arm=$2 n=$3
  local out=out/${fx%.md}_${arm}_${n}.md
  {
    echo "You are the assistant in the conversation below. You are running the skill whose full text follows, plus its examples file. Write only your next assistant turn, exactly as you would send it to the user. Do not use tools. Do not explain your reasoning outside the turn."
    echo; echo "<skill_md>"; cat skill_${arm}.md; echo "</skill_md>"
    echo; echo "<examples_md>"; cat examples_${arm}.md; echo "</examples_md>"
    echo; echo "<conversation>"; cat fixtures/$fx; echo "</conversation>"
    echo; echo "Write your next assistant turn now."
  } | claude -p --model sonnet --permission-mode default \
      --disallowed-tools "Bash,Edit,Write,NotebookEdit,Agent,WebFetch,WebSearch,Skill,Read,Glob,Grep,TodoWrite" \
      > "$out" 2> "${out%.md}.err"
  echo "done $out exit=$? bytes=$(wc -c < $out)"
}
jobs_list=()
for fx in $(ls fixtures); do for arm in A B; do for n in 1 2; do jobs_list+=("$fx $arm $n"); done; done; done
i=0
for j in "${jobs_list[@]}"; do
  run_one $j &
  i=$((i+1))
  sleep 4
  if (( i % 4 == 0 )); then wait; fi
done
wait
echo ALL_DONE
