# Contributing

Thanks for taking the time to contribute.

This repository is Maharshi Patel's GitHub **profile/portfolio manifest**. The nine MAK'MA
projects are maintained in their own standalone repositories and are the canonical source
of implementation, tests, CI and releases.

## Before opening a change

- Keep profile changes focused and easy to review.
- Do not include credentials, private employer code, proprietary datasets or personal data.
- Preserve the distinction between implemented, experimental and planned features.
- Keep project links pointed at the canonical `maharshimak/<repository>` repositories.
- Make implementation changes in the corresponding project repository rather than copying
  source back into this profile repository.

## Profile validation

The profile CI verifies that the README links all nine canonical project repositories and
that the retired `portfolio-projects/` mirror does not return.

Each standalone project owns its own install, lint, test, wheel/container and security
workflow. Follow that project's `CONTRIBUTING.md` and README for local commands.

## Pull requests

A good pull request should explain the problem, the change, validation performed, and any
security or compatibility implications. Conventional-style prefixes such as `feat:`,
`fix:`, `docs:`, `test:`, `refactor:`, `ci:` and `chore:` are preferred.

## Security

Do not report exploitable vulnerabilities in public issues. Follow
[SECURITY.md](./SECURITY.md) for responsible disclosure guidance.
