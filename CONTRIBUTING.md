# Contributing

Thanks for improving this skill.

## Pull Requests

- Keep changes focused and explain the user-facing improvement.
- Include an elevator pitch or short summary in the PR.
- Update `SKILL.md` when the public release workflow changes.
- Update `scripts/validate_public_skill_repo.py` tests when validation behavior changes.
- Run:

```bash
python skills/open-source-codex-skill-creator/scripts/validate_public_skill_repo.py .
python -m unittest discover -s tests
git diff --check
```
