# Context engineering strategy #1: Write

This repo sets up Claude Code's context for a vacuum robot that will learn to navigate a 4x4 grid world with Q-learning. The robot doesn't know the transition model (T) or reward function (R), so it has to learn from experience. The code for Q-learning will come later. The write strategy gives Claude persistent memory so the project doesn't have to be re-explained every session.

## Project Structure
```
cs440-write/
├── .claude/
│   ├── CLAUDE.md                 # Project memory - loaded every session
│   └── context/
│       └── environment.md        # Grid details - imported by CLAUDE.md
├── aima/                         # AIMA reference code 
├── reinforcement_learning.ipynb  # Main notebook; Lab 4 work will go here
├── reinforcement_learning.py     # Auto-generated from the notebook; will not be edited
├── bootstrap.ipynb               
├── requirements.txt
└── CONTRIBUTING.md, LICENSE      # From AIMA repo
```

## Memory Levels
1. **Project memory:** `.claude/CLAUDE.md`
    - Contains facts Claude needs in every session: the project overview, the key constraint, environment summary, project structure, and coding standards.
2. **User memory:**  `~/.claude/CLAUDE.md`
    - Contains personal preferences that apply across all projects. They live in the user's home directory, not the repo, so they aren't included here.
3. **Imports:** `.claude/context/environment.md`
    - Contains the detailed grid layout, possible actions, and the mapping to AIMA's coordinate system. CLAUDE.md references it with `@context/environment.md`.

## Design Decisions
- Static import instead of a context-switching script
  - A hook that loads dynamically adds unnecessary complexity, so the import is written directly in `CLAUDE.md`.
- Coordinate mapping explained
  - AIMA's GridMDP uses (x, y) with y increasing upward, but the lab grid uses rows from the top. Without mapping instructions, Claude could easily put terminal states in the wrong location.
- Living cost of -0.04
    - GridMDP skips 0 cells, so standard cells use -0.04.
- Decisions recorded in the notebook
  - Hyperparameters, decisions, and results are written inside markdown cells.
