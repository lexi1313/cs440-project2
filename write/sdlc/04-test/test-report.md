Agent Skills Component — Test Report

Project: CS440 Project 2
Component: Skill Router and Trigger Logging
Test Date: November 18, 2026
Status: Component, integration, and live Lab 4 testing completed

1. Overview

This report documents testing of the Agent Skills routing component developed for the mini-coding-agent. The component discovers available skills, evaluates their relevance to user prompts, selects appropriate skills based on similarity scores, and records routing decisions.

Testing focused on verifying the functionality of skill_router.py and its generated skill_trigger.log.

2. Test Environment

* Operating System: macOS
* Programming Language: Python 3
* Test Script: mini-coding-agent/test_skill_router.py
* Component: mini-coding-agent/skill_router.py
* Log File: mini-coding-agent/skill_trigger.log
* Test Skill: isolate/.claude/skills/vacuum-env-debugging/SKILL.md
* Similarity Method: Token-frequency cosine similarity
* Similarity Threshold: 0.3

The router uses Python standard-library functionality for file discovery, text processing, similarity calculations, and logging.

3. Component Test Results

T1: Skill Discovery

Objective: Verify that the router discovers a valid skill in the configured skill directory.

Expected Result: The vacuum-env-debugging skill is discovered without errors.

Actual Result:

* Discovered skills: ['vacuum-env-debugging']
* Errors: []

Status: PASS

T2: Relevant Prompt Matching

Objective: Verify that a relevant prompt triggers the appropriate skill.

Input:

Debug the vacuum robot environment and investigate its state transitions

Expected Result: The router selects vacuum-env-debugging.

Actual Result:

* Similarity score: 0.365148
* Threshold: 0.3
* Selected skill: vacuum-env-debugging

Status: PASS

T3: Unrelated Prompt Rejection

Objective: Verify that an unrelated prompt does not trigger an inappropriate skill.

Input:

Write a poem about the ocean

Expected Result: No skill is selected.

Actual Result:

* Similarity score: 0.235702
* Threshold: 0.3
* Selected skill: None
* Logged outcome: no_match

Status: PASS

An initial test using a threshold of 0.2 incorrectly selected the skill. Increasing the threshold to 0.3 resolved the issue for the tested prompts.

T4: Routing Log Generation

Objective: Verify that routing decisions are recorded.

Expected Result: A log file is created containing the prompt, similarity method, threshold, candidate scores, selected skill, and routing outcome.

Actual Result: The router successfully created skill_trigger.log and recorded the routing decisions as structured JSON records.

The records included timestamps, session identifiers, decision identifiers, candidate paths, similarity scores, selection decisions, and error information.

Status: PASS

T5: Outcome Recording

Objective: Verify that the router can update a routing decision after a skill is reported as loaded and used.

Expected Result: The corresponding log record reflects the supplied outcome.

Actual Result:

* loaded: True
* used: True
* outcome: success

Status: PASS

This test verifies the logging mechanism. Actual skill execution must be verified separately through agent integration testing.

T6: Malformed Skill Handling

Objective: Verify that an invalid SKILL.md does not cause the router to crash.

Test Setup: A temporary skill directory was created containing a SKILL.md file without valid YAML frontmatter.

Expected Result: The router ignores the invalid skill, records an error, and continues.

Actual Result:

* Selected skill: None
* Error recorded: Missing or invalid frontmatter.
* Outcome: no_match

The router completed the routing check without crashing.

Status: PASS

4. Summary of Results

Test ID	Description	Result
T1	Skill discovery	PASS
T2	Relevant prompt matching	PASS
T3	Unrelated prompt rejection	PASS
T4	Routing log generation	PASS
T5	Outcome recording	PASS
T6	Malformed skill handling	PASS

Component Tests Passed: 6/6

5. Integration Testing

Test file: mini-coding-agent/tests/test_skill_integration.py (pytest, uses the upstream FakeModelClient so the exact prompt sent to the model can be inspected).
Command: cd mini-coding-agent && python -m pytest -q tests
Result: 26 passed (19 upstream tests + 7 new integration tests, including the no-ripgrep search fallback). The upstream tests still pass, so existing behavior is unchanged.

I1: Prompt-time delivery — a Lab 4 prompt selects vacuum-env-debugging, and the SKILL.md instructions appear in the first prompt sent to the model. Log record: trigger=user_prompt, loaded=true, used=true, outcome=completed. PASS
I2: Unrelated prompt — "Write a poem about the ocean" produces no Active skills section; log outcome=no_match. PASS
I3: In-turn request — the model calls use_skill(need=...) mid-task; the instructions are absent from the first prompt and present in the second. Log record: trigger=agent_request, with both the original prompt and the need text. PASS
I4: Permissions preserved — with approval=never, a write_file call after the skill loads is still denied and no file is written. PASS
I5: Malformed skill — a broken SKILL.md is recorded in errors while the valid skill is still selected and the agent finishes. PASS
I6: Per-turn reset — a skill loaded for one turn is not carried into an unrelated next turn. PASS

CLI smoke test (no Ollama installed): the router printed "[skills] user_prompt check: vacuum-env-debugging=0.655 (threshold 0.3) -> selected vacuum-env-debugging", the model call failed, and the record was closed with outcome=not_delivered:error, loaded=false. This confirms the log separates selection from delivery.

Threshold check (token cosine against the skill description):

| Prompt | Score | Selected at 0.3 |
| --- | --- | --- |
| Help with the Lab 4 vacuum robot environment setup: check the grid rules, actions, and coordinate mapping in the Write project context | 0.655 | yes |
| Set up the Lab 4 vacuum robot environment in the notebook using the Write strategy context | 0.523 | yes |
| Finish the Lab 4 setup for the vacuum robot | 0.522 | yes |
| Debug why the vacuum robot environment lets the robot move into the obstacle | 0.346 | yes |
| Solve Lab 4 | 0.333 | yes |
| Write a poem about the ocean | 0.236 | no |
| Fix the README typo in the setup section | 0.228 | no |
| Add a binary search function with tests | 0.109 | no |

6. Lab 4 Demonstration

Date: November 19, 2026. Backend: `claude -p` (Sonnet) via `--backend claude`, because Ollama was not installed on the demo machine. Approval: auto (non-interactive run). Full terminal output: [lab4-demo-run.txt](lab4-demo-run.txt).

Command (from the repository root):

python3 mini-coding-agent/mini_coding_agent.py --backend claude --model sonnet --cwd . --skills-dir isolate/.claude/skills --approval auto --max-steps 20 --max-new-tokens 4096 "Solve Lab 4 for the vacuum robot: set up the 4x4 grid environment in the Lab 4 cell of write/reinforcement_learning.ipynb using the Write project context (grid rules, actions, coordinate mapping). Do not implement Q-learning. Verify the cell actually runs by executing its code with python3 from the write folder."

| Attempt | Result | Cause / action |
| --- | --- | --- |
| 1 (14 steps) | Skill selected (0.593). Cell written, but it used `GridMDP` without importing it; the notebook never imports `GridMDP`, so it would fail in Jupyter. Hit the step limit while re-checking. | Notebook reverted. Prompt now asks for execution-based verification, which the skill also requires. |
| 2 (20 steps) | Skill selected (0.551). Re-read the same files 9 times and never wrote. | Upstream history compression cut each read to 900 chars (180 once older). History limits raised; transcript clipping now keeps the newest steps. |
| 3 (20 steps) | Skill selected (0.551). Followed the skill's "Before acting" steps, read AIMA `mdp.py`, wrote the Lab 4 cell (with `from aima.mdp import GridMDP`), executed it (exit 0), and returned a final summary. | Accepted, but it took 19 steps. |
| 4 (`--cwd .`, 7 steps) | Skill selected (0.551). Read CLAUDE.md and environment.md, found the Lab 4 cell, patched it, executed it (exit 0), and returned a final summary. No failed tool calls. | **Final run.** A run from a regular terminal with `--cwd write` showed two more causes of wasted steps: tool paths resolve from the git root, and with no `rg` installed, the fallback `search` treated regex patterns as literal text. The fallback now uses regex (new test), and the demo uses `--cwd .`. Transcript: [lab4-demo-run.txt](lab4-demo-run.txt). |

Independent verification of the final run (attempt 4; attempt 3 checked the same way) (not relying on the agent's report):
- The notebook still parses (56 cells, nbformat 4). Only cell 55 changed.
- Running cell 55 after the notebook's own import cell prints init (0, 3), terminals [(1, 0), (3, 0)], obstacle (1, 2) excluded, 15 states, R(penalty) = -1, R(goal) = 10. All of these match write/.claude/context/environment.md.
- reinforcement_learning.py and aima/ are unchanged. No Q-learning code was added. No T or R matrix was invented.
- Log record (last line of skill_trigger.log): trigger=user_prompt, score 0.551246, threshold 0.3, selected_skill=vacuum-env-debugging, loaded=true, used=true, outcome=completed.

7. Known Limitations

The routing component uses token-frequency cosine similarity rather than semantic embeddings. Consequently, matching depends on word overlap between prompts and skill descriptions.

The initial threshold of 0.2 produced an incorrect selection for an unrelated prompt. A threshold of 0.3 correctly separated the two tested prompts, but additional prompts and skills should be evaluated before considering this threshold broadly reliable.

The outcome-recording test confirms that the router can store supplied usage statuses. It does not independently verify whether an agent actually followed the skill instructions.

8. Conclusion

All six standalone component tests passed.

The results demonstrate that the router can discover valid skills, calculate similarity scores, select or reject skills according to a configured threshold, generate routing logs, update outcome records, and handle malformed skills without crashing.

The component is ready for integration testing. Final acceptance depends on successful integration with the mini-coding-agent and completion of the required Lab 4 demonstration.