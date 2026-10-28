# CS440 Lab 4: Vacuum Robot using Reinforcement Learning (Isolate Strategy)

This repository implements the **Isolate** strategy for Lab 4. The overall goal of the isolate repo is to prevent Context Confusion and Context Overload by splitting work across specialized sub-agents, rather than making one main agent do everything.

## The Lab Constraints
The vacuum robot navigates a 4x4 grid. The lab explicitly states that the agent does NOT know the transition model (T) or the reward function (R). Q-learning will be implemented in a later lab. 

This repo uses a "Main Agent" (the Orchestrator) that acts as a manager. It reads the prompt and delegates tasks to specialized sub-agents with restricted scopes. The environment agent never has to think about Q-learning math, and the Q-learning agent never has to worry about grid coordinates.

## Project Structure

- **`.claude/`**
  - `CLAUDE.md`: The Main Agent instructions (tells the orchestrator to delegate).
  - `agents/environment.md`: The Environment Sub-agent (restricted to grid and coordinate mapping).
  - `agents/q-learning.md`: The Q-Learning Sub-agent (restricted to AIMA and notebook setup).
- **`src/`**
  - `vacuum_env.py`: The Python environment setup placeholder.
- **`tests/`**
  - `test_env.py`: Basic environment test placeholder.
    
## How the Isolate Sub-Agents Work
When a prompt is submitted, the Main Agent analyzes the task and delegates:
If the task involves grid, wall, setup, or coordinates, it delegates to the environment-agent (who only knows the grid rules).
If the task involves AIMA, Q-learning, or the notebook, it delegates to the q-learning-agent (who only knows the AIMA rules).
This ensures each sub-agent only sees the exact rules it needs to complete its specific task, keeping the Main Agent's context window completely clean.
