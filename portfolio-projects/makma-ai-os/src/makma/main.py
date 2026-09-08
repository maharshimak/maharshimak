from collections import defaultdict
from typing import Protocol

from fastapi import FastAPI
from pydantic import BaseModel


class ModelProvider(Protocol):
    async def generate(self, message: str, context: list[dict[str, str]]) -> str: ...


class EchoProvider:
    async def generate(self, message: str, context: list[dict[str, str]]) -> str:
        return f"Mak'ma online. Received: {message}. Context items: {len(context)}."


class Memory:
    def __init__(self) -> None:
        self.sessions: dict[str, list[dict[str, str]]] = defaultdict(list)

    async def load(self, session_id: str) -> list[dict[str, str]]:
        return list(self.sessions[session_id])

    async def append(self, session_id: str, role: str, content: str) -> None:
        self.sessions[session_id].append({"role": role, "content": content})


class Orchestrator:
    def __init__(self, provider: ModelProvider, memory: Memory) -> None:
        self.provider = provider
        self.memory = memory

    async def run(self, message: str, session_id: str) -> str:
        context = await self.memory.load(session_id)
        await self.memory.append(session_id, "user", message)
        response = await self.provider.generate(message, context)
        await self.memory.append(session_id, "assistant", response)
        return response


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


app = FastAPI(title="Mak'ma AI OS", version="0.1.0")
runtime = Orchestrator(EchoProvider(), Memory())


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/chat")
async def chat(request: ChatRequest) -> dict[str, str]:
    return {
        "response": await runtime.run(request.message, request.session_id),
        "session_id": request.session_id,
    }
