from dataclasses import asdict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from data_copilot.executor import DataCopilot
from data_copilot.safety import UnsafeQueryError

app = FastAPI(
    title="Secure Data Copilot",
    version="0.1.0",
    description="Read-only analytics copilot with explicit SQL policy enforcement.",
)


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    database_path: str = Field(min_length=1)
    max_rows: int = Field(default=200, ge=1, le=1000)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/ask")
def ask(request: AskRequest) -> dict[str, object]:
    try:
        result = DataCopilot(
            database_path=request.database_path,
            max_rows=request.max_rows,
        ).ask(request.question)
        return asdict(result)
    except (ValueError, UnsafeQueryError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
