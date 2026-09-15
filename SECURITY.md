# Security Policy

## Scope

This policy applies to the profile repository and the public portfolio projects currently stored under `portfolio-projects/`.

Only the current `main` branch is considered supported. Historical commits may contain superseded implementations and should not be treated as maintained releases.

## Reporting a vulnerability

Please do **not** publish exploitable security details, credentials, private data or working attack payloads in a public issue.

For responsible disclosure, contact the repository owner privately at `pmaharshi999@gmail.com` with a clear subject such as `Security report: <project>`. Include the affected project, impact, reproduction steps and any suggested mitigation. Remove unrelated secrets or personal data from logs and screenshots before sending them.

## Secrets and sensitive data

Never commit API keys, passwords, OAuth tokens, private keys, production credentials, database files containing private data or private user information.

Use environment variables and `.env.example` files with placeholder values only. Local database, key and credential-like artifacts are ignored at repository level.

If a real credential is accidentally committed:

1. revoke or rotate it immediately;
2. remove it from the current tree;
3. inspect Git history and rewrite affected history where necessary;
4. re-run the repository security audit before considering the incident closed.

## Automated safeguards

The repository uses a **Security History Audit** GitHub Actions workflow that checks every reachable Git blob for common credential patterns and sensitive filenames. The workflow runs on pull requests, pushes to `main`, a weekly schedule and manual dispatch.

The scanner is designed not to print matched secret values. A match fails the workflow and reports only the pattern category, blob and path requiring review.

Project CI also validates linting, tests, package builds and container builds where configured.

## AI and tool safety

Projects that introduce agents, tools, SQL execution, model promotion or external actions should document and test:

- what the component can read;
- what it can modify;
- whether explicit user approval is required;
- how inputs and outputs are validated;
- how actions are logged or audited;
- how credentials and permissions are scoped;
- what limits prevent unbounded or destructive execution.

Security controls should not be weakened merely to simplify a demo.

## Portfolio data policy

Public examples should use synthetic, generated or otherwise public-safe data. Employer-confidential code, proprietary datasets, real patient data and private internal architecture do not belong in this repository.
