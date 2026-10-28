# CS440 Lab 4: Vacuum robot using reinforcement learning

## Project Overview
A vacuum robot learns to navigate a 4x4 grid using reinforcement learning.

## Key Constraint
The agent does NOT know T and R. Use model-free methods later. Do not write a static T/R matrix.

## Orchestrator Rules (Main Agent)
You are the Main Agent. Do NOT try to do all the work yourself. 
Delegate tasks to your specialized sub-agents using the `Task` tool:
- If the task involves the grid, walls, or coordinates, delegate to the `environment-agent`.
- If the task involves AIMA setup, the notebook, or Q-learning, delegate to the `q-learning-agent`.

## Context Filter
When delegating to a sub-agent, act as the Context Filter. 
- Do NOT pass your full conversation history or unrelated setup rules to the sub-agent. 
- Pass ONLY the specific prompt and the restricted scope required for their task.
