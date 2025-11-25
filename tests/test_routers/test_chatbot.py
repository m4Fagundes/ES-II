from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from api.main import app 

client = TestClient(app)

# Mock da resposta que a API da LongCat/OpenAI retornaria
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
    """
    Testa se o chatbot devolve a resposta da IA corretamente.
    Usamos @patch para NÃO chamar a API real (economiza dinheiro e tempo).
    """
    # Configura o mock para retornar status 200 e o JSON simulado
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_AI_RESPONSE
    mock_post.return_value = mock_response

    payload = {"mensagem": "Quais os planos?"}
    response = client.post("/chat/enviar", json=payload)

    assert response.status_code == 200
    # Verifica se a resposta da nossa API é o texto que estava dentro do JSON simulado
    assert response.json()["resposta"] == "Olá! Temos planos de 500 Mega."

@patch("api.routers.chatbot.httpx.AsyncClient.post")
def test_chatbot_erro_api_externa(mock_post):
    """Testa o comportamento se a API da IA cair (Erro 500)."""
    mock_response = AsyncMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_post.return_value = mock_response

    payload = {"mensagem": "Oi"}
    response = client.post("/chat/enviar", json=payload)

    # Nossa API deve tratar o erro e retornar 502 Bad Gateway
    assert response.status_code == 502