# CI and project badges

[![Portfolio CI](https://github.com/maharshimak/maharshimak/actions/workflows/portfolio-ci.yml/badge.svg)](https://github.com/maharshimak/maharshimak/actions/workflows/portfolio-ci.yml)
[![Production AI Labs CI](https://github.com/maharshimak/maharshimak/actions/workflows/production-ai-labs-ci.yml/badge.svg)](https://github.com/maharshimak/maharshimak/actions/workflows/production-ai-labs-ci.yml)
[![Security History Audit](https://github.com/maharshimak/maharshimak/actions/workflows/security-history-audit.yml/badge.svg)](https://github.com/maharshimak/maharshimak/actions/workflows/security-history-audit.yml)

The repository currently validates **nine AI engineering projects** across two CI matrices:

- **Portfolio CI** covers Mak'ma AI OS, Agentic RAG Engine, Multimodal AI Studio, Knowledge Twin, Clinical Document Intelligence and MLOps Production Pipeline.
- **Production AI Labs CI** covers Secure Data Copilot, LLM Eval & Observability and MLOps Control Plane.

Both matrices install the package, run Ruff, execute pytest, build a wheel and build the project's Docker image. The **Security History Audit** independently scans all reachable Git blobs for common credential patterns and sensitive filenames.
