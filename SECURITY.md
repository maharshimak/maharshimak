# Security Policy

## Scope

This policy applies to this GitHub profile/portfolio manifest. Each linked MAK'MA project
is maintained in its own canonical standalone repository and carries its own
`SECURITY.md`, CI and dependency configuration.

Only current `main` branches are considered supported. Historical commits may contain
superseded implementations and should not be treated as maintained releases.

## Reporting a vulnerability

Do **not** publish exploitable security details, credentials, private data or working
attack payloads in a public issue.

For responsible disclosure, contact the repository owner privately at
`pmaharshi999@gmail.com` with a clear subject such as `Security report: <project>`.
Include the affected repository, impact, reproduction steps and suggested mitigation.
Remove unrelated secrets or personal data from logs and screenshots.

## Secrets and sensitive data

Never commit API keys, passwords, OAuth tokens, private keys, production credentials,
private databases or private user information. Use environment variables and example
configuration containing placeholders only.

If a real credential is accidentally committed:

1. revoke or rotate it immediately;
2. remove it from the current tree;
3. inspect reachable Git history and rewrite affected history where necessary;
4. re-run the relevant repository security checks.

## Automated safeguards

The profile repository runs its security history audit over reachable Git blobs and a
profile-contract workflow over canonical repository links. Each standalone MAK'MA
repository independently gates its implementation with linting, tests, package builds and
container/browser checks where applicable.

## AI and tool safety

Projects that introduce agents, tools, SQL execution, model promotion or external actions
should document and test what can be read or modified, approval requirements, validation,
auditability, credential scope and limits that prevent unbounded or destructive execution.

Public examples should use synthetic, generated or otherwise public-safe data. Employer
confidential code, proprietary datasets and private internal architecture do not belong in
the profile or project repositories.
