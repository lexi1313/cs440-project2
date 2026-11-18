# Intent for Agent Skills

**Status** Draft for Group 1 review

## Problem

The upstream mini coding agent has no dedicated way to discover reusable skill instructions and bring them into a task when they become relevant. Group 1 already has a Lab 5 skill for debugging the vacuum environment. Today, the mini agent cannot automatically select it or show why it was selected.

## Proposed outcome

The mini agent discovers folder-based skills and loads a relevant skill when a user prompt or a need raised during a turn calls for it. Group 1 can run a Lab 4 setup or debugging task against the Write workspace using the existing Lab 5 skill. The instructor can inspect a log that shows the text checked, similarity scores, the routing decision, and which instructions reached the model.

## Affected users and systems

- Group 1 members building, testing, and demonstrating Project 2.
- The instructor team evaluating the implementation and demonstration.
- The upstream mini coding agent, the Lab 4 Write workspace, and the Lab 5 skill at `isolate/.claude/skills/vacuum-env-debugging/SKILL.md`.

## Constraints

- Preserve the mini agent's workspace boundaries, validation, and approval policy.
- Use the existing Lab 5 skill for the Lab 4 attempt.
- Respect Lab 4's model-free setup. Leave explicit transition and reward models and Q-learning implementation outside this task. Make any required notebook edits in the source notebook.
- Keep the implementation focused on discovery, routing, instruction delivery, and evidence.

## Open questions

- Which Lab 4 setup or debugging prompt best exercises the skill while keeping the recorded demonstration under three minutes?
- What threshold separates relevant Lab 4 prompts from unrelated ones across the team's evaluation examples?
