# 🔭 LLM Eval & Observability

A compact evaluation and observability platform for **LLM/RAG regressions**.

## Implemented

- typed experiment cases
- latency and cost tracking
- lexical answer relevance
- citation coverage
- forbidden-phrase detection
- token/cost estimation
- experiment aggregation
- regression quality gates
- JSONL trace store
- FastAPI evaluation endpoint
- tests
- Docker

## Why this project matters

AI systems can regress without throwing exceptions. A deployment may still return HTTP 200 while becoming slower, more expensive, less grounded or less relevant.

This project treats model quality as an engineering signal.

```text
test cases
   ↓
candidate system
   ↓
traces
   ↓
metrics
   ↓
quality gate
   ↓
PASS / BLOCK RELEASE
```

## Metrics

- relevance score
- citation coverage
- forbidden-output rate
- latency p95
- average estimated cost
- pass rate

## Example

```python
from llm_eval.models import EvalCase, ModelOutput
from llm_eval.runner import ExperimentRunner
from llm_eval.gates import regression_gate

cases = [
    EvalCase(
        id="rag-1",
        prompt="What is RAG?",
        expected_terms={"retrieval", "generation"},
        expected_citations={"doc-1"},
    )
]

def candidate(case):
    return ModelOutput(
        text="Retrieval augmented generation combines retrieval and generation.",
        citations=["doc-1"],
        latency_ms=180,
        input_tokens=100,
        output_tokens=28,
    )

summary = ExperimentRunner().run("candidate-v1", cases, candidate)
decision = regression_gate(summary)
print(decision)
```

## Roadmap

- provider adapters
- prompt/version registry
- RAG faithfulness evaluator
- pairwise model comparison
- dataset versioning
- OpenTelemetry exporter
- dashboard
- CI deployment gate
