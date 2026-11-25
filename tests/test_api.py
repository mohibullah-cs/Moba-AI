from fastapi.testclient import TestClient

from app.main import app, conversations
import app.main as main_module

client = TestClient(app)


def setup_function():
    conversations.clear()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["app"] == "Moba"


def test_chat_returns_ai_reply(monkeypatch):
    def fake_reply(messages):
        assert messages[0]["role"] == "system"
        assert messages[-1]["content"] == "Hello Moba"
        return "Hello! How can I help?"

    monkeypatch.setattr(main_module, "get_ai_reply", fake_reply)

    response = client.post(
        "/api/chat",
        json={"conversation_id": "test-chat", "message": "Hello Moba"},
    )

    assert response.status_code == 200
    assert response.json()["reply"] == "Hello! How can I help?"
    assert len(conversations["test-chat"]) == 3


def test_chat_rejects_empty_message():
    response = client.post(
        "/api/chat",
        json={"conversation_id": "test-chat", "message": ""},
    )
    assert response.status_code == 422


def test_ai_error_is_returned_as_service_unavailable(monkeypatch):
    from app.ai_service import AIServiceError

    def fail_reply(messages):
        raise AIServiceError("API key is missing.")

    monkeypatch.setattr(main_module, "get_ai_reply", fail_reply)

    response = client.post(
        "/api/chat",
        json={"conversation_id": "error-chat", "message": "Hi"},
    )

    assert response.status_code == 503
    assert response.json()["detail"] == "API key is missing."
    assert conversations["error-chat"] == [main_module.SYSTEM_MESSAGE]
