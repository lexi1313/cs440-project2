# Build plan for Agent Skills

**Status** Proposed

Use the [design specification](../02-design/spec.md) as the implementation contract. Its draft uses named sections, so the steps below cite those sections.

## Files that change

Paths in this section are relative to the repository root.

| Path | Planned work |
| --- | --- |
| `mini-coding-agent/skill_router.py` | Discover and validate skills, score task text, and write routing records. |
| `mini-coding-agent/mini_coding_agent.py` | Configure the router and deliver selected instructions in the existing agent loop. |
| `mini-coding-agent/tests/test_skill_router.py` and `test_skill_integration.py` in the same test directory | Cover routing behavior, prompt delivery, and permission preservation. |
| `README.md` | Document setup, the Lab 4 command and prompt, and how to read the log. |
| `write/sdlc/04-test/test-report.md` | Record commands, results, and what the Lab 4 attempt achieved. |
| `skill_trigger.log` | Capture routing evidence from the demonstration. |

## Order of work

1. **Discovery, matching, and logging.** Start with failing tests for valid and malformed skill files, a path escaping its configured root, a relevant prompt, an unrelated prompt, tied scores, and valid log records.
2. **Skill format and discovery.** Add configured roots and parse folder-based `SKILL.md` files. Validate metadata and resolved paths. Capture discovery diagnostics so an invalid file can be reported while other skills remain available.
3. **Matching and selection.** Implement deterministic token cosine similarity over normalized prompt text and skill descriptions. Choose the best score at or above a configurable threshold. Break ties by skill name, then source path. Pick the initial threshold using a small set of representative matches and non-matches and document it with the CLI options.
4. **Instruction handling and permissions.** Route the initial message in `MiniAgent.ask`. Add a structured skill lookup tool so the model can supply a new task description during the turn. Include selected instructions in turn context before the next model call. Keep the stable prompt prefix separate, deduplicate instructions within the turn, and preserve the existing approval and path checks for actions.
5. **Logging.** Append a JSON Lines record for each check. Include a timestamp, session ID, original prompt, evaluated task text, method, threshold, candidate paths and scores, selection, instruction delivery status, and outcome or error. Report whether instructions reached the model using the model-call boundary as evidence. Describe the actual Lab 4 outcome separately in the test report.
6. **Lab 4 demonstration.** Use `write/` as the agent workspace and configure `isolate/.claude/skills/` as a skill root. Ask the agent to inspect a specific vacuum setup or behavior question using the Lab 5 skill. Run relevant Lab 4 checks and save the log and actual outcome, including partial completion if applicable.

## Risks

- Short prompts can produce low or misleading scores. Check paraphrases and unrelated prompts before choosing a threshold.
- The Lab 5 skill lives outside the Write workspace. Check the configured skill root independently and keep ordinary workspace tool boundaries in force.
- A logged match can occur before instruction delivery. Check the exact prompt received by the test model and distinguish selection from delivery.
- Logs contain verbatim prompts. Use non-sensitive inputs in the recorded demonstration and inspect its log before sharing.

## Proof

- Router tests show discovery, score and threshold behavior, stable ties, diagnostics, and parseable JSON Lines output.
- Upstream's `FakeModelClient` captures both prompt-time delivery and in-turn lookup delivery. An unrelated prompt continues normally. A denied write remains denied after a skill loads.
- The live Lab 4 run and its test report identify the command, prompt, matched skill, relevant log record, and the observed task result.
