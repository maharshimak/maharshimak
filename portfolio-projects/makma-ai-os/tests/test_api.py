from fastapi.testclient import TestClient

from makma.main import app

client = TestClient(app)


def test_health() -> None:
    assert client.get("/health").json() == {"status": "ok"}


def test_chat() -> None:
    response = client.post(
        "/v1/chat",
        json={"message": "hello", "session_id": "demo"},
    )
    assert response.status_code == 200
    assert "Mak'ma online" in response.json()["response"]
