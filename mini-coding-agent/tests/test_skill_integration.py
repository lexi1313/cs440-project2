"""Integration tests for component 7 (Agent Skills) inside the MiniAgent loop.

These use FakeModelClient so we can inspect the exact prompts the model received
and prove when SKILL.md instructions reached it.
"""

import json
from pathlib import Path

from mini_coding_agent import FakeModelClient, MiniAgent, SessionStore, WorkspaceContext
from skill_router import SkillRouter

LAB5_SKILLS = Path(__file__).resolve().parents[2] / "isolate" / ".claude" / "skills"
SKILL_MARKER = "Vacuum Environment and Lab 4 Context"  # heading inside the Lab 5 SKILL.md
LAB4_PROMPT = "Help with the Lab 4 vacuum robot environment setup: check the grid rules and actions"


def build(tmp_path, outputs, roots=(LAB5_SKILLS,), **kwargs):
    (tmp_path / "README.md").write_text("demo\n", encoding="utf-8")
    workspace = WorkspaceContext.build(tmp_path)
    router = SkillRouter(skill_roots=list(roots), threshold=0.3, log_path=tmp_path / "skill_trigger.log")
    model = FakeModelClient(outputs)
    agent = MiniAgent(
        model_client=model,
        workspace=workspace,
        session_store=SessionStore(tmp_path / ".mini-coding-agent" / "sessions"),
        approval_policy=kwargs.pop("approval_policy", "auto"),
        skill_router=router,
        **kwargs,
    )
    return agent, model, router


def read_log(router):
    return [json.loads(line) for line in router.log_path.read_text().splitlines() if line.strip()]


def test_relevant_prompt_delivers_skill_before_first_model_call(tmp_path):
    agent, model, router = build(tmp_path, ["<final>Checked the grid.</final>"])

    assert agent.ask(LAB4_PROMPT) == "Checked the grid."

    assert SKILL_MARKER in model.prompts[0]
    [record] = read_log(router)
    assert record["trigger"] == "user_prompt"
    assert record["prompt"] == LAB4_PROMPT
    assert record["selected_skill"] == "vacuum-env-debugging"
    assert record["candidates"][0]["score"] >= 0.3
    assert record["loaded"] is True and record["used"] is True
    assert record["outcome"] == "completed"


def test_unrelated_prompt_runs_without_skill(tmp_path):
    agent, model, router = build(tmp_path, ["<final>Done.</final>"])

    agent.ask("Write a poem about the ocean")

    assert "Active skills:\n" not in model.prompts[0]
    [record] = read_log(router)
    assert record["selected_skill"] is None
    assert record["outcome"] == "no_match"
    assert record["loaded"] is False


def test_agent_can_request_skill_mid_task(tmp_path):
    agent, model, router = build(
        tmp_path,
        [
            '<tool>{"name":"use_skill","args":{"need":"debug vacuum robot environment grid actions"}}</tool>',
            "<final>Used the skill.</final>",
        ],
    )

    agent.ask("Look around this repository")

    assert SKILL_MARKER not in model.prompts[0]
    assert SKILL_MARKER in model.prompts[1]
    first, second = read_log(router)
    assert first["outcome"] == "no_match"
    assert second["trigger"] == "agent_request"
    assert second["prompt"] == "Look around this repository"
    assert second["task_text"] == "debug vacuum robot environment grid actions"
    assert second["selected_skill"] == "vacuum-env-debugging"
    assert second["used"] is True and second["outcome"] == "completed"


def test_skill_does_not_bypass_approval(tmp_path):
    agent, model, router = build(
        tmp_path,
        [
            '<tool>{"name":"write_file","args":{"path":"x.py","content":"print(1)"}}</tool>',
            "<final>Could not write.</final>",
        ],
        approval_policy="never",
    )

    agent.ask(LAB4_PROMPT)

    assert SKILL_MARKER in model.prompts[0]
    assert not (tmp_path / "x.py").exists()
    tool_event = next(item for item in agent.session["history"] if item["role"] == "tool")
    assert tool_event["content"] == "error: approval denied for write_file"


def test_malformed_skill_is_logged_and_agent_continues(tmp_path):
    bad_root = tmp_path / "skills"
    (bad_root / "broken").mkdir(parents=True)
    (bad_root / "broken" / "SKILL.md").write_text("no frontmatter here", encoding="utf-8")
    agent, model, router = build(tmp_path, ["<final>ok</final>"], roots=(bad_root, LAB5_SKILLS))

    assert agent.ask(LAB4_PROMPT) == "ok"

    [record] = read_log(router)
    assert record["selected_skill"] == "vacuum-env-debugging"
    assert any("frontmatter" in error["error"] for error in record["errors"])


def test_skills_reset_between_turns(tmp_path):
    agent, model, router = build(tmp_path, ["<final>a</final>", "<final>b</final>"])

    agent.ask(LAB4_PROMPT)
    agent.ask("Write a poem about the ocean")

    assert SKILL_MARKER in model.prompts[0]
    assert "Active skills:\n" not in model.prompts[1]


def test_search_fallback_supports_regex_without_rg(tmp_path, monkeypatch):
    # The demo machine had no ripgrep, and the model's regex patterns used to match nothing.
    import mini_coding_agent

    monkeypatch.setattr(mini_coding_agent.shutil, "which", lambda name: None)
    agent, _, _ = build(tmp_path, [])
    (tmp_path / "nb.ipynb").write_text('"# Lab 4 - Reinforcement Learning"\n', encoding="utf-8")

    assert "nb.ipynb:1:" in agent.tool_search({"pattern": "Lab|lab", "path": "."})
    assert agent.tool_search({"pattern": "Lab 4 (", "path": "."}) == "(no matches)"  # invalid regex falls back to literal
