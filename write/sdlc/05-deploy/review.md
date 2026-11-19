# Project 2 Review Record

Status: Implementation and live Lab 4 run complete; awaiting group sign-off

This file is the Deploy-stage review record for the Agent Skills component. Do not mark a check as passed unless its evidence has been reviewed.

## Change under review

- Feature: folder-based skill discovery, similarity routing, instruction loading, and logging.
- Specification: ../02-design/spec.md
- Implementation plan: ../03-build/plan.md
- Demonstration target: Lab 4 vacuum robot project, using the existing Lab 5 skill.

## Review checklist

- [ ] The implementation matches the approved spec and plan.
- [ ] Skill discovery reads only configured skill roots and handles invalid files safely.
- [ ] Similarity scores, threshold behavior, no-match behavior, and tie behavior are clear and repeatable.
- [ ] The selected skill instructions are loaded before the related agent action.
- [ ] Skill instructions do not bypass existing tool permissions, path checks, or approval behavior.
- [ ] The log records the prompt, matching method, threshold, candidates and scores, selected skill, whether it was used, and outcome.
- [ ] The Lab 4 run uses the intended skill and respects the Write project instructions.
- [ ] Tests and the Lab 4 demonstration evidence are linked below.
- [ ] No unrelated Lab 4 files or generated files were changed.

## Findings

Record each finding with severity, file or behavior, evidence, and resolution.

- Low, threshold: the initial 0.2 threshold selected the skill for an unrelated prompt (score 0.236). Resolved by raising it to 0.3, which is now the CLI default (`--skill-threshold`). See the threshold table in the test report.
- Medium, logging: a selected skill whose model call failed stayed `pending` in the log forever. Resolved: `finish_skills` closes the record as `not_delivered:<outcome>` with `loaded=false`.
- Low, prompt text: the rules mention "Active skills", so tests must check for the section header `Active skills:\n` and not just the phrase. Resolved in `test_skill_integration.py`.
- Medium, upstream context reduction: during the live run, the agent re-read `environment.md` 9 times and never acted, because history showed only 900 chars per read (180 once older) and `clip()` dropped the newest steps once over 12,000 chars. Resolved in `history_text`: limits are now 2,500/600 chars, a 20,000-char cap, and the tail is kept. All 25 tests still pass.
- Medium, Lab 4 output: the first live attempt used `GridMDP` without importing it. Caught by running the cell. The accepted run imports it and was executed by both the agent and the reviewer.
- Open, workspace root: `--cwd write` resolves to the git root (`cs440-project2/`) because upstream `WorkspaceContext` uses `git rev-parse --show-toplevel`. Tool path checks are therefore bounded by the repo root, not by `write/`. This is upstream behavior and was left unchanged; the skill instructions point the agent at `write/...` paths.

## Verification evidence

- Tests run: `cd mini-coding-agent && python -m pytest -q tests` -> 25 passed. `python3 test_skill_router.py` -> T1 to T6 pass. See [test-report.md](../04-test/test-report.md).
- Lab 4 demonstration: [lab4-demo-run.txt](../04-test/lab4-demo-run.txt) and test report section 6 (3 attempts, last one accepted and independently re-run).
- Skill routing log: `mini-coding-agent/skill_trigger.log` (JSON Lines, one record per routing check).

## Review decision

Pending review after implementation.

Reviewer(s): TBD
Review date: TBD

## Loop Back (To Maintain Stage)
*If any blocking issues are found, document them here so they can be moved to `06-maintain/feedback.md`.*
- *Pending review.*
