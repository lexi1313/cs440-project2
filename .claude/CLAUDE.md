# CS440 Lab 4: Vacuum robot using reinforcement learning
Strategy #1: Write

## Project Overview
A vacuum robot learns to navigate a 4x4 grid world using reinforcement
learning. Q-learning will be implemented in a later lab; this repo
currently sets up the project context.

## Key Constraint
The agent does NOT know the transition model (T) or reward function (R).
It must learn from experience, so use model-free methods (Q-learning),
not value iteration or policy iteration.

## Environment Summary
- 4x4 grid, start at top-left
- One obstacle (X) the robot cannot enter
- Penalty cell (-1) and goal cell (+10)
- Full details: @context/environment.md

## Project Structure
- `aima/` – AIMA reference code. Reuse `QLearningAgent` and
  `run_single_trial` from `aima/reinforcement_learning.py`; do not modify.
- `reinforcement_learning.ipynb` – main notebook; edit this under Lab 4 cell, not the .py
- `reinforcement_learning.py` – auto-generated from the notebook; do not edit

## Coding Standards
- Descriptive variable names
- Follow the AIMA pseudocode style (Fig 21.8 for Q-learning)
