from math import ceil
from typing import Callable

from llm_eval.metrics import citation_coverage, contains_forbidden, estimated_cost, relevance
from llm_eval.models import CaseMetrics, EvalCase, ExperimentSummary, ModelOutput


Candidate = Callable[[EvalCase], ModelOutput]


def percentile(values: list[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, ceil(fraction * len(ordered)) - 1))
    return ordered[index]


class ExperimentRunner:
    def __init__(
        self,
        min_relevance: float = 0.7,
        min_citation_coverage: float = 0.8,
        max_latency_ms: float = 5000.0,
        input_per_million: float = 0.0,
        output_per_million: float = 0.0,
    ) -> None:
        self.min_relevance = min_relevance
        self.min_citation_coverage = min_citation_coverage
        self.max_latency_ms = max_latency_ms
        self.input_per_million = input_per_million
        self.output_per_million = output_per_million

    def run(
        self,
        name: str,
        cases: list[EvalCase],
        candidate: Candidate,
    ) -> ExperimentSummary:
        evaluated: list[CaseMetrics] = []

        for case in cases:
            output = candidate(case)
            rel = relevance(case, output)
            citations = citation_coverage(case, output)
            forbidden = contains_forbidden(case, output)
            cost = estimated_cost(
                output,
                self.input_per_million,
                self.output_per_million,
            )
            passed = (
                rel >= self.min_relevance
                and citations >= self.min_citation_coverage
                and not forbidden
                and output.latency_ms <= self.max_latency_ms
            )

            evaluated.append(
                CaseMetrics(
                    case_id=case.id,
                    relevance=rel,
                    citation_coverage=citations,
                    forbidden_hit=forbidden,
                    latency_ms=output.latency_ms,
                    estimated_cost_usd=cost,
                    passed=passed,
                )
            )

        count = len(evaluated) or 1
        return ExperimentSummary(
            name=name,
            pass_rate=sum(item.passed for item in evaluated) / count,
            mean_relevance=sum(item.relevance for item in evaluated) / count,
            mean_citation_coverage=sum(
                item.citation_coverage for item in evaluated
            ) / count,
            latency_p95_ms=percentile(
                [item.latency_ms for item in evaluated],
                0.95,
            ),
            mean_cost_usd=sum(item.estimated_cost_usd for item in evaluated) / count,
            cases=evaluated,
        )
