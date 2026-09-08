from dataclasses import dataclass
import re


@dataclass(frozen=True)
class StudyRecord:
    study_id: str | None
    phase: str | None
    participants: int | None
    intervention: str | None
    primary_endpoint: str | None


def _capture(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, flags=re.I)
    return match.group(1).strip() if match else None


def extract(text: str) -> StudyRecord:
    participants = _capture(r"participants?\s*:\s*(\d+)", text)
    return StudyRecord(
        study_id=_capture(r"study\s*(?:id)?\s*:\s*([A-Z0-9-]+)", text),
        phase=_capture(r"phase\s*:\s*([1-4IVX]+)", text),
        participants=int(participants) if participants else None,
        intervention=_capture(r"intervention\s*:\s*([^\n]+)", text),
        primary_endpoint=_capture(r"primary endpoint\s*:\s*([^\n]+)", text),
    )


def validate(record: StudyRecord) -> list[str]:
    errors: list[str] = []
    if record.participants is not None and record.participants <= 0:
        errors.append("participants must be positive")
    if record.study_id is None:
        errors.append("study_id missing")
    return errors
