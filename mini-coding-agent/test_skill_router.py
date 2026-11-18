from pathlib import Path
from skill_router import SkillRouter

# Find the project root
project_root = Path(__file__).resolve().parent.parent

# Initialize the router
router = SkillRouter(
    skill_roots=[project_root / "isolate" / ".claude" / "skills"],
    threshold=0.3,
    log_path=project_root / "mini-coding-agent" / "skill_trigger.log"
)

# Test 1: Discover skills
skills, errors = router.discover_skills()

print("TEST 1: Skill Discovery")
print("Skills found:", [skill["name"] for skill in skills])
print("Errors:", errors)
print()

# Test 2: Relevant prompt
print("TEST 2: Relevant Prompt")

result = router.route_skill(
    "Debug the vacuum robot environment and investigate its state transitions"
)

print("Candidates:", result["candidates"])
print("Selected:", result["selected_skill"]["name"] if result["selected_skill"] else None)
print()

# Test 3: Unrelated prompt
print("TEST 3: Unrelated Prompt")

result = router.route_skill(
    "Write a poem about the ocean"
)

print("Candidates:", result["candidates"])
print("Selected:", result["selected_skill"]["name"] if result["selected_skill"] else None)
print()

# Test 4: Verify logging
print("TEST 4: Logging")

log_path = project_root / "mini-coding-agent" / "skill_trigger.log"

if log_path.exists():
    print("Log created successfully:", log_path)
    print("Log contents:")
    print(log_path.read_text())
else:
    print("ERROR: Log was not created")

# Test 5: Outcome recording
print("\nTEST 5: Outcome Recording")

result = router.route_skill(
    "Debug the vacuum robot environment and investigate its state transitions"
)

router.record_outcome(
    decision_id=result["decision_id"],
    loaded=True,
    used=True,
    outcome="success"
)

import json

with log_path.open("r", encoding="utf-8") as log:
    records = [json.loads(line) for line in log if line.strip()]

record = next(
    record for record in records
    if record["decision_id"] == result["decision_id"]
)

print("Loaded:", record["loaded"])
print("Used:", record["used"])
print("Outcome:", record["outcome"])

# Test 6: Malformed skill handling
print("\nTEST 6: Malformed Skill Handling")

import tempfile

with tempfile.TemporaryDirectory() as temp_dir:
    invalid_skill_dir = Path(temp_dir) / "invalid-skill"
    invalid_skill_dir.mkdir()

    invalid_skill_path = invalid_skill_dir / "SKILL.md"
    invalid_skill_path.write_text(
        "This skill has no YAML frontmatter.",
        encoding="utf-8"
    )

    test_router = SkillRouter(
        skill_roots=[Path(temp_dir)],
        threshold=0.3,
        log_path=Path(temp_dir) / "skill_trigger.log"
    )

    result = test_router.route_skill(
        "Debug the vacuum robot environment"
    )

    print("Selected:", result["selected_skill"])

    import json

    with test_router.log_path.open("r", encoding="utf-8") as log:
        record = json.loads(log.readline())

    print("Errors:", record["errors"])
    print("Outcome:", record["outcome"])