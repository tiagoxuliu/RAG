from unittest.mock import patch
from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

def test_query_endpoint_returns_answer():
    fake_result = {
        "answer": "Resposta de teste.",
        "source_documents": [],
    }
    with patch("app.api.answer_question", return_value=fake_result):
        response = client.post("/query", json={"question": "pergunta de teste"})

    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == "Resposta de teste."
    assert body["sources"] == []

def test_query_endpoint_missing_question_returns_422():
    response = client.post("/query", json={})
    assert response.status_code == 422