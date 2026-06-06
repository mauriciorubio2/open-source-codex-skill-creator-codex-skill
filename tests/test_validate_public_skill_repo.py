import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "open-source-codex-skill-creator" / "scripts" / "validate_public_skill_repo.py"


def write_minimal_repo(root: Path, skill_name: str = "sample-skill") -> None:
    for rel_path in (
        "README.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/workflows/test.yml",
    ):
        path = root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("ok\n", encoding="utf-8")
    (root / "LICENSE").write_text("MIT License\n", encoding="utf-8")

    skill = root / "skills" / skill_name
    (skill / "agents").mkdir(parents=True, exist_ok=True)
    (skill / "SKILL.md").write_text(
        f"---\nname: {skill_name}\ndescription: Use when testing public skill validation.\n---\n\n# Sample\n",
        encoding="utf-8",
    )
    (skill / "agents" / "openai.yaml").write_text(
        "interface:\n"
        '  display_name: "Sample Skill"\n'
        '  short_description: "Validate sample public skill"\n'
        f'  default_prompt: "Use ${skill_name} to test validation."\n',
        encoding="utf-8",
    )


class PublicSkillRepoValidatorTests(unittest.TestCase):
    def test_current_repo_validates(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(ROOT)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_minimal_repo_validates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_minimal_repo(root)
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(root)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_license_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_minimal_repo(root)
            (root / "LICENSE").unlink()
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(root)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        self.assertEqual(result.returncode, 2)
        self.assertIn("LICENSE", result.stdout)


if __name__ == "__main__":
    unittest.main()
