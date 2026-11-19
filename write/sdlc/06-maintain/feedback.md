# Maintenance feedback for Agent Skills

**Status** Pre-run baseline. Live demonstration results are pending.

## Observed during planning

- The Lab 5 skill is stored under `isolate/.claude/skills/`, while the proposed Lab 4 demonstration targets `write/`. The run command needs to specify both locations so skill discovery and workspace access can be checked independently.
- The skill description emphasizes debugging vacuum actions and state. Generic prompts such as “finish Lab 4” may match weakly. Add a task-specific prompt and a paraphrase to the evaluation set before tuning the threshold.
- Downstream evidence depends on distinguishing a score above the threshold from instructions reaching the model. Record both and use the Lab 4 result to assess whether the instructions helped.

## Signals to track

| Signal | Evidence | Follow-up when observed |
| --- | --- | --- |
| A relevant Lab 4 prompt misses | Prompt, candidate scores, threshold, and expected skill | Add the prompt to the routing tests and review tokenization, skill metadata, and the threshold. |
| An unrelated prompt loads a skill | Prompt, chosen skill, and candidate scores | Add a negative test and identify why the candidate matched before changing the threshold. |
| A selection fails to reach the model | Session ID, selected skill, delivery field, and error | Reproduce with the fake model and check the next model request. |
| Lab 4 work goes outside the requested setup | Agent transcript, resulting diff, and test result | Review how workspace guidance and skill instructions enter the model prompt. Add a check for the observed failure. |

## Close the loop

After the demo, record expected and observed behavior, link the relevant log record and [test report](../04-test/test-report.md), and assign any confirmed follow-up during team review. If a finding changes the project's constraints or desired behavior, update [intent.md](../01-plan/intent.md) before revising the specification and build plan.

## Observed during build

- Short generic prompts such as "Solve Lab 4" still clear the threshold (0.333) because "lab" and "4" appear in the skill description. The margin is thin; a paraphrase without those tokens may miss. Possible follow-ups: score against the skill name as well as the description, or switch to embeddings.
- The `use_skill` tool lets the model recover from a missed match mid-task, so the threshold does not have to catch every phrasing on the first check.

## Run feedback

2026-11-19, Claude backend, 3 attempts. See the test report, section 6.
- Routing worked on every attempt (0.551 to 0.593 vs. 0.3), and the instructions reached the model each time.
- Failure 1: the agent's "verification" printed the cell's source instead of running it. Disposition: prompt asks for execution. Future option: add "run the cell" to the skill's Completion section.
- Failure 2: upstream history truncation caused a re-read loop. Disposition: fixed in `history_text`.
- The agent first tries `.claude/CLAUDE.md` relative to `write/`, but the tool root is the git root, which costs about 2 steps per run. Disposition: open (see review.md).

Previously: Pending the first live Lab 4 run. Record the date, session ID, prompt, expected behavior, observed behavior, evidence, and disposition for each confirmed finding.
