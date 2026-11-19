import json
import math
import re
import uuid

from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


class SkillRouter:
    """
    Discovers available agent skills and selects the most
    relevant skill based on the current task.
    """

    def __init__(self, skill_roots, threshold=0.3,
                 log_path="skill_trigger.log", echo=None):

        self.skill_roots = [Path(root).resolve() for root in skill_roots]
        self.threshold = threshold
        self.log_path = Path(log_path)
        # Optional callable(str) used to show routing decisions live
        # (the CLI passes a stderr printer; tests leave it as None).
        self.echo = echo

        if not 0 <= threshold <= 1:
            raise ValueError("Threshold must be between 0 and 1.")

        self.session_id = str(uuid.uuid4())


    def load_skill(self, path):
        """
        Reads a SKILL.md file and extracts its name,
        description, and instructions.
        """

        path = Path(path).resolve()

        # Ensure the file is inside an allowed skill root.
        if not any(
            path.is_relative_to(root)
            for root in self.skill_roots
        ):
            raise ValueError("Skill is outside configured roots.")

        text = path.read_text(encoding="utf-8")

        # Separate YAML frontmatter from instructions.
        match = re.match(
            r"\A---\s*\n(.*?)\n---\s*\n(.*)",
            text,
            re.DOTALL
        )

        if not match:
            raise ValueError("Missing or invalid frontmatter.")

        frontmatter = match.group(1)
        instructions = match.group(2).strip()

        metadata = {}

        # Parse simple name and description fields.
        for line in frontmatter.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip().strip("\"'")

        name = metadata.get("name")
        description = metadata.get("description")

        if not name or not description:
            raise ValueError("Skill requires a name and description.")

        if not instructions:
            raise ValueError("Skill instructions cannot be empty.")

        return {
            "name": name,
            "description": description,
            "path": str(path),
            "instructions": instructions
        }


    def discover_skills(self):
        """
        Searches configured roots for valid SKILL.md files.

        Invalid or unreadable files are skipped.
        """

        skills = []
        errors = []

        for root in self.skill_roots:

            if not root.is_dir():
                errors.append({
                    "path": str(root),
                    "error": "Skill root does not exist"
                })
                continue

            for path in sorted(root.rglob("SKILL.md")):

                try:
                    skill = self.load_skill(path)
                    skills.append(skill)

                except (OSError, UnicodeError, ValueError) as error:
                    errors.append({
                        "path": str(path),
                        "error": str(error)
                    })

        return skills, errors


    def tokenize(self, text):
        """
        Converts text into lowercase word tokens.
        """

        return re.findall(r"[a-z0-9]+", text.lower())


    def calculate_similarity(self, prompt, description):
        """
        Calculates cosine similarity between the prompt
        and skill description using word frequencies.
        """

        prompt_words = Counter(self.tokenize(prompt))
        description_words = Counter(self.tokenize(description))

        if not prompt_words or not description_words:
            return 0.0

        # Dot product
        dot_product = sum(
            count * description_words.get(word, 0)
            for word, count in prompt_words.items()
        )

        # Vector magnitudes
        prompt_magnitude = math.sqrt(
            sum(count ** 2 for count in prompt_words.values())
        )

        description_magnitude = math.sqrt(
            sum(count ** 2 for count in description_words.values())
        )

        similarity = dot_product / (
            prompt_magnitude * description_magnitude
        )

        return similarity


    def route_skill(self, prompt, task_text=None, trigger="user_prompt"):
        """
        Finds the most relevant skill for a prompt.

        prompt is the user's request for this turn. task_text is the
        text actually scored; it defaults to the prompt, and is set to
        the agent's stated need when the agent asks for a skill during
        execution (trigger="agent_request").

        Returns the selected skill and its instructions,
        or None when no skill meets the threshold.
        """

        task_text = prompt if task_text is None else task_text

        skills, errors = self.discover_skills()

        candidates = []

        for skill in skills:

            score = self.calculate_similarity(
                task_text,
                skill["description"]
            )

            candidates.append({
                "name": skill["name"],
                "path": skill["path"],
                "score": round(score, 6)
            })

        # Highest score first, then name/path for deterministic ties.
        candidates.sort(
            key=lambda candidate: (
                -candidate["score"],
                candidate["name"],
                candidate["path"]
            )
        )

        selected_skill = None

        if candidates:
            best = candidates[0]

            if best["score"] >= self.threshold:
                selected_skill = next(
                    skill for skill in skills
                    if skill["path"] == best["path"]
                )

        decision_id = str(uuid.uuid4())

        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": self.session_id,
            "decision_id": decision_id,
            "trigger": trigger,
            "prompt": prompt,
            "task_text": task_text,
            "method": "token_cosine",
            "threshold": self.threshold,
            "candidates": candidates,
            "selected_skill": (
                selected_skill["name"]
                if selected_skill else None
            ),
            "selected_path": (
                selected_skill["path"]
                if selected_skill else None
            ),
            "loaded": False,
            "used": False,
            "outcome": (
                "pending" if selected_skill else "no_match"
            ),
            "errors": errors
        }

        self.log_routing(record)

        if self.echo:
            scores = ", ".join(
                f"{c['name']}={c['score']:.3f}" for c in candidates
            ) or "no skills found"
            verdict = (
                f"selected {selected_skill['name']}"
                if selected_skill else "no match"
            )
            self.echo(
                f"[skills] {trigger} check: {scores} "
                f"(threshold {self.threshold}) -> {verdict}"
            )

        return {
            "decision_id": decision_id,
            "selected_skill": selected_skill,
            "candidates": candidates
        }


    def log_routing(self, record):
        """
        Appends a structured JSON record to skill_trigger.log.
        """

        self.log_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with self.log_path.open("a", encoding="utf-8") as log:
            log.write(json.dumps(record) + "\n")


    def record_outcome(self, decision_id, loaded=False,
                       used=False, outcome="completed"):
        """
        Updates the existing routing record after the agent
        reports whether it loaded and used the skill.

        Keeps one record per routing check.
        """

        if not self.log_path.exists():
            raise FileNotFoundError("Routing log does not exist.")

        records = []

        found = False

        with self.log_path.open("r", encoding="utf-8") as log:

            for line in log:
                if not line.strip():
                    continue

                record = json.loads(line)

                if record.get("decision_id") == decision_id:

                    record["loaded"] = bool(loaded)
                    record["used"] = bool(used)
                    record["outcome"] = outcome
                    record["updated_at"] = datetime.now(
                        timezone.utc
                    ).isoformat()

                    found = True

                records.append(record)

        if not found:
            raise ValueError("Routing decision not found.")

        # Write updated records to a temporary file.
        temp_path = self.log_path.with_name(
            self.log_path.name + ".tmp"
        )

        with temp_path.open("w", encoding="utf-8") as log:
            for record in records:
                log.write(json.dumps(record) + "\n")

        temp_path.replace(self.log_path)