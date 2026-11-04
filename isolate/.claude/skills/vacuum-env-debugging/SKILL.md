---
name: vacuum-env-debugging
description: Helps debug the vacuum environment lab by tracing agent actions, state changes, cleaning, movement, and termination. Use when investigating a vacuum simulation bug or asking how an action changes the environment.
---

# Vacuum Environment Debugging

When helping with this lab:

1. Read the relevant environment code and tests before proposing a change.
2. Trace the behavior from the chosen action through the environment update to the resulting state.
3. Check the lab instructions and existing tests for the expected behavior.
4. Focus on the specific bug or question; avoid unrelated refactors.
5. Explain the cause and suggest a focused test for the behavior.
6. Don’t claim the issue is fixed or verified unless the relevant checks were run.

## Check

- Whether the action is valid and handled as expected.
- Whether movement and cleaning update the correct state.
- Whether boundaries and invalid actions are handled consistently.
- Whether termination happens at the expected point.
- Whether the change preserves the project’s isolate technique.