from dataclasses import dataclass
from math import log, sqrt
from collections import Counter


@dataclass(frozen=True)
class Document:
    id: str
    text: str


def tokenize(text: str) -> list[str]:
    return [t.strip(".,!?;:()[]{}").lower() for t in text.split() if t.strip()]


def lexical_score(query: str, doc: Document) -> float:
    q = tokenize(query)
    d = tokenize(doc.text)
    counts = Counter(d)
    if not d:
        return 0.0
    return sum((1 + log(1 + counts[t])) for t in q if counts[t]) / sqrt(len(d))


def hashed_vector(text: str, dims: int = 64) -> list[float]:
    vec = [0.0] * dims
    for token in tokenize(text):
        vec[hash(token) % dims] += 1.0
    norm = sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def semantic_score(query: str, doc: Document) -> float:
    a, b = hashed_vector(query), hashed_vector(doc.text)
    return sum(x * y for x, y in zip(a, b))


def rank(query: str, docs: list[Document], scorer) -> list[tuple[str, float]]:
    return sorted(((d.id, scorer(query, d)) for d in docs), key=lambda x: x[1], reverse=True)


def reciprocal_rank_fusion(rankings: list[list[tuple[str, float]]], k: int = 60) -> list[tuple[str, float]]:
    scores: dict[str, float] = {}
    for ranking in rankings:
        for position, (doc_id, _) in enumerate(ranking, start=1):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + position)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def hybrid_retrieve(query: str, docs: list[Document], top_k: int = 3) -> list[str]:
    fused = reciprocal_rank_fusion([
        rank(query, docs, lexical_score),
        rank(query, docs, semantic_score),
    ])
    return [doc_id for doc_id, _ in fused[:top_k]]


def citation_context(ids: list[str], docs: list[Document]) -> str:
    lookup = {d.id: d.text for d in docs}
    return "\n\n".join(f"[{doc_id}] {lookup[doc_id]}" for doc_id in ids if doc_id in lookup)


def recall_at_k(relevant: set[str], retrieved: list[str], k: int) -> float:
    if not relevant:
        return 1.0
    return len(relevant.intersection(retrieved[:k])) / len(relevant)
