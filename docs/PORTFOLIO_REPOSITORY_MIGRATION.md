# Portfolio repository migration

## Status: completed

The nine MAK'MA projects now live in verified standalone repositories under
`maharshimak/`. Their current `main` branches are the canonical implementation,
documentation, CI and release history.

The former `portfolio-projects/` copies existed only as a migration source. They are
removed from the profile repository to prevent drift and eliminate duplicate sources of
truth.

## Canonical repositories

- `maharshimak/makma-ai-os`
- `maharshimak/agentic-rag-engine`
- `maharshimak/multimodal-ai-studio`
- `maharshimak/knowledge-twin`
- `maharshimak/clinical-document-intelligence`
- `maharshimak/secure-data-copilot`
- `maharshimak/llm-eval-observability`
- `maharshimak/mlops-control-plane`
- `maharshimak/mlops-production-pipeline`

The profile repository is intentionally limited to presentation, portfolio documentation,
security/profile automation and links to those sources. Do not reintroduce copied project
trees here.

Historical migration commits remain in Git history for provenance; deleting the current
mirror does not fabricate or erase that history.
