# Portfolio repository migration

The nine projects are currently retained under `portfolio-projects/`. Public source
cleanup must wait for verified standalone repositories and successful Actions.

## Preparation and publication

`scripts/split-portfolio-repos.py` replaces the initial command-string PowerShell
implementation. The PowerShell entry point now delegates using an argument array.

Requirements: a full clean clone on `main`, Python 3.12+, Git, `git-filter-repo`,
and Docker. Publishing additionally requires GitHub CLI authenticated as the target
owner with repository creation/push permissions. Never paste credentials into files.

```bash
python -m pip install git-filter-repo
python scripts/split-portfolio-repos.py --dry-run
python scripts/split-portfolio-repos.py --output ../portfolio-verified
```

The default operation prepares isolated repositories and validates them. To prepare,
validate and then publish in one invocation, choose a fresh output directory:

```bash
python scripts/split-portfolio-repos.py --output ../portfolio-publish --publish
```

For PowerShell:

```powershell
./scripts/split-portfolio-repos.ps1 -DryRun
./scripts/split-portfolio-repos.ps1 -Output ../portfolio-publish -Publish
```

`--dry-run` is read-only and lists the plan; it does not claim any validation ran.
The output directory must not exist. A stopped run preserves its local artifacts.
The script never deletes/recreates remote repositories or force-pushes. If publication
stops partway, inspect the verified local splits and existing destinations before
resuming manually; a blind rerun will intentionally refuse non-empty destinations.

## Safety and verification

1. Check source identity, clean tree, full history and main commit.
2. Clone each project into an isolated repository using `git-filter-repo`.
3. Compare the split root tree with the exact source subtree hash.
4. Inspect every reachable blob for common credential patterns and sensitive filenames.
5. Install each package in a separate virtual environment; run lint and tests.
6. Build a distributable wheel and a real Docker image.
7. Only after all nine pass, create or inspect each public destination.
8. Refuse any destination with existing refs, regardless of repository size.
9. Push without force, verify remote main SHA, and configure metadata.

The credential scan is heuristic, not proof that code is free of all confidential
information. Manually review source and fixtures before publication. A suspected
secret blocks publication; remediate the affected history and repeat validation.
Authentic author dates/messages are retained when filtering; commit IDs change
because project paths and ancestry change. No historical contributions are fabricated.

Descriptions and topics are in [portfolio-repositories.json](portfolio-repositories.json).

## Cleanup gate

For every standalone repository verify public visibility, main branch, expected
files/history, readable README, working links, installation, lint/tests, Docker and
successful Actions. Confirm description, homepage, topics and MIT license.

Then create a separate profile cleanup PR to replace project links, remove only the
verified migrated folders, remove the two monorepo CI workflows and migrate/remove
monorepo Dependabot configuration. Keep the profile snake workflow and useful migration
documentation. Merge only after profile links and remaining workflows are healthy.

Never replace working links with links to repositories that do not yet exist.

Recommended pins: Mak'ma AI OS, Agentic RAG Engine, Multimodal AI Studio, Knowledge Twin,
Secure Data Copilot, LLM Eval & Observability. Pinning is a separate profile UI action.
