# Project 2 Specification: Agent Skills Component

Status: Proposed

## Purpose

Add a skills component to the mini coding agent so it can discover folder-based skills, select a relevant skill for a user request or a need identified during a task, make that skill's instructions available before acting, and record the routing decision.

## Scope

The component covers:

- Discovering skill folders under configured skill roots.
- Reading a SKILL.md file and its name, description, and instructions.
- Comparing the current user prompt and later task context against available skill descriptions.
- Selecting and loading relevant skill instructions into the agent's context.
- Logging the prompt, similarity check, selected or executed skill, and outcome.
- Demonstrating the component on the Lab 4 vacuum robot project using the Lab 5 skill.

The component does not replace the model, the agent loop, or the existing tools and approval policy. A skill provides instructions to the agent; it is not executable code and does not grant new tool permissions.

## Skill format and discovery

Each skill is a folder containing SKILL.md. The file must provide a non-empty name and description in frontmatter followed by the skill instructions. The router must:

1. Search only configured skill roots.
2. Resolve each candidate file beneath one of those roots.
3. Ignore missing, unreadable, or malformed skill files without stopping the agent.
4. Make the skill name, description, source path, and instruction text available to the routing and execution stages.

For the Lab 4 demonstration, the configured roots must include the existing vacuum environment skill folder at isolate/.claude/skills/vacuum-env-debugging/SKILL.md, even when the agent workspace is write/.

## Matching and selection

The router must consider:

- The user's initial prompt.
- A skill need discovered by the agent during execution, before the next relevant action.

For each check, the router records a similarity score for every eligible skill and applies a configurable threshold. It selects the highest-scoring skill only when that score meets the threshold. If no skill meets the threshold, the agent continues without skill instructions. If multiple candidates tie for the highest score, the router must use a documented deterministic tie rule.

The matching method and threshold must be documented and configurable so the team can inspect and tune them. Matching is a relevance aid; the agent must still use the skill only when its instructions fit the task.

## Instruction handling and permissions

When a skill is selected, its instructions must be added to the agent's working context before the agent takes the related action. The agent must retain its normal tool validation, workspace boundaries, and approval behavior. Skill text must not bypass those controls.

A later routing check may select an additional skill if the task changes. The log must distinguish a routing decision from a skill that was actually loaded and used.

## Logging

Append one structured record per routing check to skill_trigger.log. Records must include:

- Timestamp and run/session identifier.
- User prompt or task text being checked.
- Matching method and threshold.
- Candidate skill names, paths, and similarity scores.
- Selected skill, or an explicit no-match value.
- Whether the skill instructions were loaded/used.
- Outcome or error, including malformed or unreadable skill files when relevant.

The Lab 4 run must leave a log record that shows the prompt, similarity check, and skill used.

## Acceptance criteria

- A valid skill folder is discovered from a configured root.
- A relevant Lab 4 prompt can select the existing vacuum environment skill.
- A skill need raised during an ongoing task can be checked before the next related action.
- An unrelated prompt or a score below threshold results in no skill selection.
- Missing or malformed skills do not stop the agent.
- The selected skill instructions reach the model before the related action.
- The log contains the required prompt, candidates and scores, selection, usage status, and outcome.
- The Lab 4 demonstration respects the Write project instructions: no invented transition or reward model, no direct edit to generated reinforcement_learning.py, and no Q-learning implementation unless explicitly requested as a later task.
