from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock # Importamos MagicMock
from api.main import app 

client = TestClient(app)

MOCK_AI_RESPONSE = {
    "choices": [
        {
            "message": {
                "content": "Olá! Temos planos de 500 Mega."
            }
        }
    ]
}

@patch("api.routers.chatbot.httpx.AsyncClient.post")
def test_chatbot_responde_sucesso(mock_post):
    # CORREÇÃO: A resposta em si (objeto response) é síncrona, apenas a chamada é async.
    # Usamos MagicMock para simular o objeto que o 'await' retorna.
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_AI_RESPONSE
    
    # O método post retorna essa resposta quando aguardado
    mock_post.return_value = mock_response

    payload = {"mensagem": "Quais os planos?"}
    response = client.post("/chat/enviar", json=payload)

    assert response.status_code == 200
    assert response.json()["resposta"] == "Olá! Temos planos de 500 Mega."

@patch("api.routers.chatbot.httpx.AsyncClient.post")
def test_chatbot_erro_api_externa(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    
    mock_post.return_value = mock_response

    payload = {"mensagem": "Oi"}
    response = client.post("/chat/enviar", json=payload)

    assert response.status_code == 502