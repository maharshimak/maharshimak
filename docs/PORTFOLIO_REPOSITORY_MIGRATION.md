# Portfolio Repository Migration

This repository currently contains multiple independent engineering projects under `portfolio-projects/`. The goal of this migration is to turn each project into a first-class standalone GitHub repository while preserving project-specific commit history.

## Target repositories

1. `maharshimak/makma-ai-os`
2. `maharshimak/agentic-rag-engine`
3. `maharshimak/multimodal-ai-studio`
4. `maharshimak/knowledge-twin`
5. `maharshimak/clinical-document-intelligence`
6. `maharshimak/secure-data-copilot`
7. `maharshimak/llm-eval-observability`
8. `maharshimak/mlops-control-plane`
9. `maharshimak/mlops-production-pipeline`

## Why split them

The profile repository should function as the portfolio landing page. Keeping substantial projects nested inside it hides them from the GitHub repository list, makes pinning impossible, weakens repository-level discovery, and mixes unrelated CI/dependency concerns.

Standalone repositories provide each project with its own:

- repository card and pinned-profile visibility;
- description, homepage and topics;
- issue tracker and roadmap;
- CI workflow and dependency management;
- releases and version history;
- security/contribution documentation;
- stars, forks and project-specific activity;
- clean clone/install experience.

## Automated split

The PowerShell migration script is:

```text
scripts/split-portfolio-repos.ps1
```

It is intentionally conservative. It:

1. verifies that `git` and GitHub CLI (`gh`) are available;
2. verifies GitHub authentication;
3. refuses to run from a dirty working tree;
4. creates a public standalone repository when it does not exist;
5. accepts an already-created repository only when it is empty;
6. refuses to overwrite a non-empty repository;
7. uses `git subtree split` so each project keeps the commits that affected its directory;
8. pushes that split history as the new repository's `main` branch;
9. configures portfolio homepage and project-specific GitHub topics;
10. leaves the original monorepo folders untouched until validation is complete.

## Windows execution

From a clean local clone of `maharshimak/maharshimak`:

```powershell
git checkout main
git pull
pwsh -File .\scripts\split-portfolio-repos.ps1 -DryRun
pwsh -File .\scripts\split-portfolio-repos.ps1
```

If PowerShell 7 (`pwsh`) is not available, Windows PowerShell can run the script with:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\split-portfolio-repos.ps1
```

## Required tools

```powershell
git --version
gh --version
gh auth status
```

If GitHub CLI is installed but not authenticated:

```powershell
gh auth login
```

Use the GitHub.com account `maharshimak` and grant repository permissions when prompted.

## Validation after the split

Do **not** remove the original folders immediately. Validate every new repository first:

- README renders correctly from the repository root;
- relative documentation/image links still work;
- package/import paths do not depend on the old monorepo location;
- tests pass from a fresh clone;
- linting passes;
- Docker builds where applicable;
- CI runs successfully;
- no credentials, `.env` files, private employer code, confidential data or generated local state are present;
- repository description, homepage and topics are correct.

## Follow-up work

After all nine repositories are healthy:

1. add dedicated per-repository GitHub Actions workflows;
2. add/update `.gitignore`, `.env.example`, security and contribution files;
3. improve project READMEs with architecture, setup, API examples and roadmap;
4. add screenshots/demo media where useful;
5. update the profile `README.md` links to the standalone repositories;
6. pin the strongest six repositories on the GitHub profile;
7. remove `portfolio-projects/*` from the profile repository in a separate cleanup PR;
8. simplify profile-repository CI/Dependabot so it only manages profile-specific content.

## Recommended pinned repositories

The initial six should be:

1. `makma-ai-os`
2. `agentic-rag-engine`
3. `multimodal-ai-studio`
4. `knowledge-twin`
5. `secure-data-copilot`
6. `llm-eval-observability`

The remaining repositories still provide valuable depth but should not crowd the first recruiter-facing view.

## Rollback safety

The migration script does not delete source folders or rewrite the profile repository's history. If a new repository needs to be rebuilt, delete/recreate that standalone repository or fix it independently while the original project remains available here.
