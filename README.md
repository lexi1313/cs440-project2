# CS440 Lab 04

#### Group 1: Alexa Tchakar, Jacob St Lawrence, Alyssa Bennett

This lab explores two context engineering strategies, [Write](https://github.com/alyssakbennett/cs440-lab04/tree/main/write) and 
[Isolate](https://github.com/alyssakbennett/cs440-lab04/tree/main/isolate) using Claude Code to prepare a vacuum robot project for 
reinforcement learning. We will be implementing Q-learning at a later time.

## Write
This strategy uses a `.claude` directory that contains persistent project instructions in `CLAUDE.md` and `environment.md`.
### Structure 
```
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

## Isolate
This strategy uses specialized sub-agents to separate tasks and reduce context confusion. The main agent analyzes tasks and delegates them 
to either the environment or Q-learning agent based on their responsibilities.

- **`.claude/`**
  - `CLAUDE.md`: The Main Agent instructions (tells the orchestrator to delegate).
  - `agents/environment.md`: The Environment Sub-agent (restricted to grid and coordinate mapping).
  - `agents/q-learning.md`: The Q-Learning Sub-agent (restricted to AIMA and notebook setup).
- **`src/`**
  - `vacuum_env.py`: The Python environment setup placeholder.
- **`tests/`**
  - `test_env.py`: Basic environment test placeholder.
