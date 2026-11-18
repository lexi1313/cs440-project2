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

## Run feedback

Pending the first live Lab 4 run. Record the date, session ID, prompt, expected behavior, observed behavior, evidence, and disposition for each confirmed finding.
