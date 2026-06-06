---
name: open-source-codex-skill-creator
description: Create, validate, package, and publish free open source Codex skills as public GitHub repositories; pair with the official skill-creator skill for scaffold and validation. Use when creating or updating skills intended for public distribution, MIT or OSI licensing, repo docs, semantic release tags, changelogs, contribution guidance, CI validation, GitHub Releases, or installation docs from a GitHub repo.
---

# Open Source Codex Skill Creator

## Overview

Use this skill as the opinionated public-release workflow for Codex skills. Treat the official `skill-creator` skill as the low-level scaffold, metadata, and validation layer whenever it is available.

## Coordination

- Announce this skill when using it.
- Also use `skill-creator` when creating or validating skill structure.
- If `skill-creator` is unavailable, still create the expected Codex skill layout and clearly say validation used the best available fallback.
- Public/open-source skill requests are a publish request, not a local-draft request. Creating the public GitHub repository, pushing the code, tagging the version, and creating the release are part of the default deliverable.
- Before creating or pushing a public GitHub repo, confirm the user explicitly requested public/open source publication or ask for confirmation. If the user named this skill, asked for an "open source skill", "free open source skill", "public skill", "GitHub skill", "publish", "release", or referenced an existing open-source Codex plugin/skill precedent, treat that as explicit confirmation and proceed.
- If the user asks only for a local draft, do not publish or create a public repo.
- For a new public skill, create a dedicated repository by default unless the user names an existing target repo or clearly asks for a multi-skill collection.
- Publish new public skill repos under the requestor's authenticated/default GitHub account by default. If the user names an organization, owner, or different account, use that instead; if the authenticated account is unclear, verify it before creating the repo.
- Do not stop after creating files in `/tmp`, `~/Documents`, the current workspace, or any other local-only folder when the request is for an open-source skill. A local checkout is only a staging area for the GitHub repository.

## Standard Repo Shape

Use this layout unless the target repo already has a compatible structure:

```text
repo-root/
+-- .github/
|   +-- PULL_REQUEST_TEMPLATE.md
|   +-- workflows/test.yml
+-- skills/<skill-name>/
|   +-- SKILL.md
|   +-- agents/openai.yaml
|   +-- scripts/ when useful
|   +-- references/ when useful
|   +-- assets/ when useful
+-- tests/
+-- CHANGELOG.md
+-- CONTRIBUTING.md
+-- LICENSE
+-- README.md
```

Use MIT by default unless the user requests another OSI-approved license. A public repository without an explicit license is not open source.

## Workflow

1. Define the skill.
   - Normalize the skill name to lowercase hyphen-case.
   - Identify what should trigger the skill, what procedures it teaches, and what scripts/references/assets are genuinely reusable.
   - Choose a conservative first release: `1.0.0` for a complete public skill, `0.1.0` for an experimental draft.

2. Scaffold with `skill-creator`.
   - Use `scripts/init_skill.py <skill-name> --path <output-directory>`.
   - Create `agents/openai.yaml` with deterministic `display_name`, `short_description`, and `default_prompt`.
   - Add only the resource directories the skill actually needs.
   - Keep README, changelog, install notes, and release process docs at repo root, not inside the skill folder.

3. Write the skill.
   - Keep `SKILL.md` lean and imperative.
   - Put trigger details in the frontmatter `description`.
   - Move long pattern catalogs, schemas, examples, or reference details into one-level `references/` files.
   - Add scripts only when deterministic reliability or repeated code justifies them.

4. Validate the skill.
   - Run the official `skill-creator` quick validator.
   - Run this skill's `scripts/validate_public_skill_repo.py <repo-root>` after repo docs are in place.
   - Run any script tests and `git diff --check`.
   - Forward-test complex skills with fresh prompts when practical.

5. Write public documentation.
   - `README.md`: explain the skill, install commands, examples, resources, privacy/safety notes, development commands, contribution summary, and license.
   - `CONTRIBUTING.md`: require focused changes, tests/docs when relevant, and a short summary explaining what changed and why.
   - `.github/PULL_REQUEST_TEMPLATE.md`: include an "Elevator Pitch / Summary" section.
   - `CHANGELOG.md`: record release dates and user-visible changes.

6. Version and release.
   - Follow semantic versioning at the repository release/tag level.
   - Bump `PATCH` for backwards-compatible fixes.
   - Bump `MINOR` for backwards-compatible features.
   - Bump `MAJOR` for breaking changes.
   - Update `CHANGELOG.md` for every release.
   - Create an annotated tag like `v1.0.0`.
   - Create a GitHub Release with concise notes from the changelog.

7. Publish when requested or implied by this skill.
   - Resolve the GitHub owner from the authenticated/default account, for example with `gh api user --jq .login`, unless the user names a different owner.
   - Create a dedicated public repository named `<skill-name>-codex-skill` unless the user requests another name.
   - Commit the complete skill, push the default branch, create and push the tag, and create the release.
   - Verify repository visibility, detected license, release URL, and CI status.
   - Provide install guidance using the system skill installer:

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo <owner>/<repo> --path skills/<skill-name>
```

Then tell users to restart Codex to pick up the new skill.

## Review Checklist

- Skill folder has `SKILL.md` with valid frontmatter and matching folder/name.
- `agents/openai.yaml` exists and includes a useful default prompt.
- Optional scripts, references, and assets are directly useful and referenced from `SKILL.md`.
- No repo docs are incorrectly placed inside the skill folder.
- README includes install/use/contribution/license guidance.
- CONTRIBUTING and PR template request an elevator pitch or summary.
- License, changelog, tag, and GitHub Release agree.
- Tests and validators pass or any gaps are explained.
