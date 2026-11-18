# CS440 Project 2
#### Group 1: Alexa Tchakar, Jacob St Lawrence, Alyssa Bennett
Project 2 adds skill routing to the mini coding agent and uses the Lab 5 skill on Lab 4, logging the prompt, match score, and skill used.

## Structure 
```
cs440-project2/
├── sdlc/
│   ├── 01-plan/
│   │   └── intent.md
│   ├── 02-design/
│   │   └── spec.md
│   ├── 03-build/
│   │   └── plan.md
│   ├── 04-test/
│   │   └── test-report.md
│   ├── 05-deploy/
│   │   └── review.md
│   └── 06-maintain/
│       └── feedback.md
├── mini-coding-agent/
│   ├── mini_coding_agent.py          # Agent entry point
│   └── skill_router.py               # Discovers, matches, and loads skills
├── isolate/
│   └── .claude/
│       └── skills/
│           └── vacuum-env-debugging/
│               └── SKILL.md          # Existing Lab 5 skill instructions
├── write/                            # Lab 4 workspace used for the demo
├── skill_trigger.log                 # Prompts, similarity scores, and skill usage
└── README.md                         # Project setup and demo instructions
```


# CS440 Lab 05
#### Group 1: Alexa Tchakar, Jacob St Lawrence, Alyssa Bennett
This lab uses Claude to solve Lab 04 using hooks, skills, and sub-agents.

## Structure 
```
├── isolate/
  ├── .claude/
  │   ├── CLAUDE.md                 # Project memory - loaded every session
  │   ├── settings.json             # Registers hook with Claude
  │   └── context/    
  │       └── environment.md        # Grid details - imported by CLAUDE.md
  ├── src/                          
  │   └── vacuum_env.py/            # environment for vacuum
  ├── tests/                        # AIMA reference code 
      └── test_env.py/              # tests called by hooks in settings.json
  └── README.md
```

## Hyperparameters
- **Living reward:** Every step costs -.04
- **Discount factor:** 0.9 means future rewards matter, but reaching the goal sooner is preferred
- **Learning rate:** 0.1 means the robot learns from each attempt and doesn't overreact if it makes one bad step
- **Epsilon:** 0.1 means that the robot will move at random 10% of the time 
 
## Hooks
This repo uses a **PostToolUse** hook in `.claude/settings.json`. Each time Claude edits a file, the hook runs `tests/test_env.py` without the need for a command. The test in `test_env.py` checks the hyperparameters set in `src/vacuum_env.py` (living reward, discount factor, learning rate, and epsilon). If the test fails, the hook exits with code 2, and Claude fixes the error; otherwise, Claude sees that the tests pass and continues working. With this format, any mistakes will be identified right away. 

To run the same check manually (from the `isolate` folder): `python3 -B tests/test_env.py`


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
