# Security Policy

## Secrets

Never commit API keys, passwords, OAuth tokens, private keys, production credentials, or private user data.

Use environment variables and `.env.example` files with placeholder values only.

## AI tool safety

Projects that introduce agents or tools should document:

- what the tool can read;
- what it can modify;
- whether user confirmation is required;
- how actions are logged;
- how credentials are scoped.

## Vulnerabilities

Please avoid publishing exploitable security details in public issues. Contact the repository owner privately for responsible disclosure.
