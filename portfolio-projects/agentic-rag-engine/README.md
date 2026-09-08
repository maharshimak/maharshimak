# 🧠 Agentic RAG Engine

A compact retrieval engine demonstrating **lexical + semantic-style scoring, reciprocal-rank fusion, citation-ready context assembly and evaluation hooks**.

## Implemented

- document chunk model
- BM25-inspired lexical scorer
- deterministic embedding-like scorer for offline tests
- reciprocal rank fusion
- citation formatter
- retrieval metrics
- unit tests

## Architecture

```mermaid
flowchart LR
Q[Query] --> L[Lexical Retriever]
Q --> S[Semantic Retriever]
L --> F[Rank Fusion]
S --> F
F --> C[Citation Context]
C --> A[Agent / LLM]
```

The semantic scorer is intentionally deterministic and dependency-light for the public starter. Swap it with a real embedding backend through the same interface.
