# Contributing

Thanks for taking the time to contribute.

This repository is currently the home of Maharshi Patel's GitHub profile and a set of public AI engineering portfolio projects. Contributions should improve correctness, reliability, documentation, testing or developer experience without weakening the safety boundaries of the projects.

## Before opening a change

- Keep changes focused and easy to review.
- Do not include private employer code, proprietary datasets, credentials, secrets or personal data.
- Do not weaken read-only, permission, validation or audit controls just to simplify a demo.
- Preserve the distinction between implemented, experimental and planned features.
- Add or update tests when behavior changes.
- Update documentation when interfaces, configuration or architecture changes.

## Local quality checks

For a Python project under `portfolio-projects/<project>`:

```bash
cd portfolio-projects/<project>
python -m pip install -e ".[dev]"
python -m ruff check .
python -m pytest -q
python -m pip wheel --no-deps . -w dist
```

If the project contains a Dockerfile, also verify:

```bash
docker build -t portfolio-project:local .
```

## Pull requests

A good pull request should explain:

1. the problem being solved;
2. the design or implementation choice;
3. tests or validation performed;
4. security or compatibility implications;
5. any known limitations.

Use conventional-style commit prefixes where practical: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `ci:` and `chore:`.

## Security

Do not report exploitable vulnerabilities in public issues. Follow [SECURITY.md](./SECURITY.md) for responsible disclosure guidance.
