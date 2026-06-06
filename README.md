# Open Source Codex Skill Creator

Create, validate, package, and publish free open source Codex skills as public GitHub repositories.

This skill incorporates the official `skill-creator` workflow as the scaffold and validation layer, then adds the public release discipline used for open source Codex plugin work: a dedicated GitHub repo, MIT license by default, README, changelog, contribution docs, CI, semver tag, and GitHub Release.

## Install

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo mauriciorubio2/open-source-codex-skill-creator --path skills/open-source-codex-skill-creator
```

Restart Codex after installing so the skill is discovered.

## Use

Example prompts:

```text
Use $open-source-codex-skill-creator to create and publish a public MIT-licensed Codex skill for financial chart QA.
```

```text
Use $open-source-codex-skill-creator to turn this local skill into a public GitHub repo with CI, changelog, and a v1.0.0 release.
```

## What It Provides

- A concise public-release workflow in `skills/open-source-codex-skill-creator/SKILL.md`
- A validator script in `scripts/validate_public_skill_repo.py`
- A standard repo shape for public skill projects
- Guidance for pairing with the official `skill-creator` skill

## Development

```bash
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/open-source-codex-skill-creator
python skills/open-source-codex-skill-creator/scripts/validate_public_skill_repo.py .
python -m unittest discover -s tests
git diff --check
```

## License

MIT. See [LICENSE](LICENSE).
