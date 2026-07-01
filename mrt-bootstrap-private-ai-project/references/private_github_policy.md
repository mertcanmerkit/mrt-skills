# Private GitHub Policy

Default all GitHub publishing to private.

## Rules

- Use `--private` on every new `gh repo create` call unless the user explicitly says public.
- Treat ambiguous phrases like "publish it", "push it", or "put it on GitHub" as private publishing.
- Verify privacy after creation:

```bash
gh repo view OWNER/REPO --json isPrivate,url,nameWithOwner
```

- Do not push secrets, API keys, tokens, private credentials, browser cookies, local env files, or unrelated user files.
- If an existing remote is public and the user did not explicitly ask for public, stop and ask before pushing.
- If the working tree contains unrelated files, stage explicit project paths only.
- If a remote already exists, verify the remote repo's privacy before pushing.
- Record the private repo URL in `docs/02_session_handoff_prompt.md` when it becomes available.
- Run `python3 scripts/ai_project_check.py` inside generated projects before pushing or handing off when the checker exists.
- Treat checker failures for public remotes, unverifiable required privacy, stale memory, or possible secrets as blockers until resolved or explicitly waived by the user.

## New Repo Flow

```bash
git init
git add -A
git commit -m "Initialize private AI project"
gh repo create OWNER/REPO --private --source=. --remote=origin --push
gh repo view OWNER/REPO --json isPrivate,url,nameWithOwner
python3 scripts/ai_project_check.py
```

## Existing Repo Flow

```bash
git remote -v
gh repo view OWNER/REPO --json isPrivate,url,nameWithOwner
git status --short --branch
python3 scripts/ai_project_check.py
git add <intended-files>
git commit -m "<clear message>"
git push
gh repo view OWNER/REPO --json isPrivate,url,nameWithOwner
```

## Automated Checks

Generated projects include `scripts/ai_project_check.py`.

The checker should verify:

- Required memory and adapter files exist, including `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/project.mdc`, `.github/copilot-instructions.md`, `ai-project.yaml`, and `docs/06_memory_freshness.md`.
- `ai-project.yaml` preserves `public_allowed: false` and `require_private_remote_verification: true`.
- GitHub remotes are private by calling `gh repo view OWNER/REPO --json isPrivate,url,nameWithOwner` when a GitHub remote exists.
- Public GitHub remotes are blocked unless the user explicitly requested public visibility.
- Common secret patterns are scanned before push.
- Memory freshness has not exceeded `ai-project.yaml:freshness.stale_after_days`.
