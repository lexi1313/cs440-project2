# CS440 Project 2
#### Group 1: Alexa Tchakar, Jacob St Lawrence, Alyssa Bennett
Project 2 adds skill routing to the mini coding agent and uses the Lab 5 skill on Lab 4, logging the prompt, match score, and skill used.

## Structure 
```
cs440-project2/
├── mini-coding-agent/
│   ├── mini_coding_agent.py          # Agent entry point (skills = component 7)
│   ├── skill_router.py               # Discovers, matches, and loads skills
│   ├── skill_trigger.log             # Prompts, similarity scores, and skill usage
│   ├── test_skill_router.py          # Standalone router checks (T1–T6)
│   └── tests/
│       ├── test_mini_coding_agent.py # Upstream tests
│       └── test_skill_integration.py # Skill routing inside the agent loop
├── isolate/
│   └── .claude/
│       └── skills/
│           └── vacuum-env-debugging/
│               └── SKILL.md          # Existing Lab 5 skill instructions
├── write/                            # Lab 4 workspace used for the demo
│   ├── sdlc/
│     ├── 01-plan/
│     │   └── intent.md
│     ├── 02-design/
│     │   └── spec.md
│     ├── 03-build/
│     │   └── plan.md
│     ├── 04-test/
│     │   └── test-report.md
│     ├── 05-deploy/
│     │   └── review.md
│     └── 06-maintain/
│         └── feedback.md
└── README.md                         # Project setup and demo instructions
```
### intent.md
- Defines why Project 2 adds skills to the mini coding agent and what success looks like. The goal is to use the existing Lab 5 skill on a Lab 4 task and show why the agent selected it.

### spec.md
- Describes how the agent discovers skills, checks for a match, and loads the selected `SKILL.md`. It also defines what the agent logs for each routing decision.

### plan.md
- Outlines the steps for building skill discovery, matching, instruction loading, and logging. It also explains how to test the component and verify that the Lab 5 skill is used during the Lab 4 demo.

### test-report.md
- Records the checks run against the skills component and their results. It captures what happened during the Lab 4 demo and links to the relevant log evidence.

### review.md
- Records whether the skills component meets the spec, preserves the agent’s approval checks, and produces the required logs. It captures reviewer findings, links to test and demo evidence, and records the review decision.

### feedback
- Records observations from planning and provides a place to capture results from the Lab 4 demo. It tracks missed matches, incorrect selections, and follow-up fixes.

### mini_coding_agent.py
- Runs the agent’s main loop and connects it to the skill router. When a skill matches, the agent adds its instructions to the model’s context before the next action.

### skill_router.py
- Discovers SKILL.md files and scores how closely each skill matches the task. It selects a skill when the score meets the threshold and records the routing decision.


## How it works
1. **Prompt check.** On every user turn, `MiniAgent.ask` sends the prompt to `SkillRouter.route_skill`. The router finds every `<root>/<skill-name>/SKILL.md`, scores the prompt against each skill's `description` using token cosine similarity, and selects the top score if it is ≥ the threshold (default 0.3). Ties are broken by name, then path.
2. **Mid-task check.** When a router is configured, the agent has a `use_skill(need)` tool. The model can call it partway through a task to run a new similarity check on its stated need.
3. **Execution.** The selected skill's instructions go into an `Active skills:` section of the prompt, after the stable prefix and before the transcript, so the model sees them before its next action. Skills give the model instructions only. All tool validation, workspace path checks, and approval prompts still apply.
4. **Logging.** Each check appends one JSON line to `mini-coding-agent/skill_trigger.log`. The record holds `trigger` (`user_prompt` or `agent_request`), `prompt`, `task_text`, `method`, `threshold`, every candidate's `score`, `selected_skill`, `loaded` (the instructions were in a prompt the model received), `used` (the turn finished with them active), and `outcome`. A `[skills] ...` summary line is also printed to the terminal.

## How to run
Requirements: Python 3.10+ and a model backend:
- **Ollama** (upstream default): `ollama serve` with a model pulled (default `qwen3.5:4b`).
- **Claude CLI** (`--backend claude`, default model `sonnet`): uses the local `claude -p` with all of its own tools, MCP servers, and settings disabled. It returns text only, and every action still goes through the mini agent's tools and approvals. The recorded Lab 4 run used this backend: [write/sdlc/04-test/lab4-demo-run.txt](write/sdlc/04-test/lab4-demo-run.txt).
- AIMA's `mdp.py` needs `numpy` (`pip install -r write/requirements.txt`) so the agent can execute the Lab 4 cell.

```bash
ollama serve &              # if it isn't already running
ollama pull qwen3.5:4b

# Lab 4 demo: Write workspace + Lab 5 skill (run from the repository root)
python3 mini-coding-agent/mini_coding_agent.py \
  --cwd . \
  --skills-dir isolate/.claude/skills \
  --approval ask \
  "Help with the Lab 4 vacuum robot environment setup: check the grid rules, actions, and coordinate mapping in write/.claude/context/environment.md"

# Same demo with the Claude CLI backend (what produced lab4-demo-run.txt)
python3 mini-coding-agent/mini_coding_agent.py --backend claude --cwd . \
  --skills-dir isolate/.claude/skills --approval ask --max-steps 20 --max-new-tokens 4096 \
  "Solve Lab 4 for the vacuum robot: set up the 4x4 grid environment in the Lab 4 cell of write/reinforcement_learning.ipynb using the Write project context (grid rules, actions, coordinate mapping). Do not implement Q-learning. Verify the cell actually runs by executing its code with python3 from the write folder."

# View the log (latest record)
tail -n 1 mini-coding-agent/skill_trigger.log | python3 -m json.tool
```

| Flag | Default | Purpose |
| --- | --- | --- |
| `--skills-dir` | `.claude/skills` and `skills` in the workspace | Skill folder to search (repeatable) |
| `--skill-threshold` | `0.3` | Minimum similarity needed to load a skill |
| `--skill-log` | `mini-coding-agent/skill_trigger.log` | Where routing records are written |
| `--no-skills` | off | Run the original agent without skills |
| `--backend` | `ollama` | `ollama` or `claude` |
| `--quiet` | off | Hide the per-step `[step N]` trace |

Use `--cwd .` (the repo root). The agent's file tools resolve paths from the git root, and the skill refers to `write/...` paths. With `--cwd write`, the model sees `write` as its cwd and wastes steps on paths that don't resolve.

Tests (no Ollama needed):
```bash
cd mini-coding-agent
python3 -m pytest -q tests     # 26 tests: 19 upstream + 7 skill integration
python3 test_skill_router.py   # standalone router checks
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
