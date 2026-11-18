---
name: vacuum-env-debugging
description: Helps with the Lab 4 vacuum robot project context and environment, including the Write strategy, grid rules, actions, and debugging. Use for Lab 4 setup or environment questions; Q-learning implementation is a later task unless explicitly requested.
---

# Vacuum Environment and Lab 4 Context

Use this skill for the Lab 4 vacuum robot project, especially when preparing its Write-strategy context or investigating environment behavior.

## Before acting

1. Read the relevant project instructions, README, context files, notebook, and tests before proposing or making changes.
2. For the Write project, read write/.claude/CLAUDE.md and write/.claude/context/environment.md. Treat those files as the source of truth for the grid and coordinate mapping.
3. Confirm which project folder and context engineering strategy the task concerns. Keep the Write and Isolate project setups distinct; do not import one strategy's structure into the other unless asked.

## Lab 4 constraints

- The Lab 4 repository currently sets up the project context. Q-learning is planned for a later lab; do not implement it for a context-setup task unless the user explicitly asks.
- The agent does not know the transition model (T) or reward function (R). Do not invent or add a fixed T or R matrix.
- If a later task explicitly requests learning, use a model-free method such as Q-learning; do not substitute value iteration or policy iteration.
- Preserve the exact environment details in the project's environment context. Do not infer or change grid cells, rewards, obstacles, or coordinate mappings.
- Reuse AIMA's QLearningAgent and run_single_trial for a later Q-learning task when appropriate. Do not modify the AIMA reference implementation.
- Treat reinforcement_learning.ipynb as the editable source. Do not edit the generated reinforcement_learning.py directly.

## Environment debugging

When the task is specifically about an environment bug or behavior:

1. Trace the chosen action through the environment update to the resulting state.
2. Check the lab instructions and existing tests for expected behavior.
3. Check action validity, movement, cleaning, boundaries, invalid actions, and termination as relevant.
4. Focus on the reported issue; avoid unrelated refactors.
5. Explain the cause and suggest a focused test. Do not claim a fix or verification unless the relevant checks were run.

## Completion

Summarize the files inspected or changed, the reason for each change, and the checks actually run. Keep project context instructions in their intended files and avoid duplicating or contradicting them.
