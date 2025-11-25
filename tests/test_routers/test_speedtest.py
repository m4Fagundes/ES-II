from fastapi.testclient import TestClient
from api.main import app 

client = TestClient(app)

def test_download_retorna_headers_corretos():
    """
    Testa se o endpoint de download retorna o Content-Length correto
    e os headers de controle de cache.
    """
    # Usamos stream=True para não baixar os 25MB na memória do teste
    with client.stream("GET", "/speedtest/download") as response:
        assert response.status_code == 200
        # Verifica se o tamanho declarado é 25MB
        expected_size = 25 * 1024 * 1024
        assert response.headers["content-length"] == str(expected_size)
        assert "no-store" in response.headers["cache-control"]

def test_upload_recebe_dados():
    """
    Testa o envio de dados para o endpoint de upload.
    """
    # Cria 1MB de dados fake
    dados_fake = b'\0' * (1024 * 1024) 
    
    # Envia como arquivo/corpo
    response = client.post("/speedtest/upload", content=dados_fake)
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Upload OK"
    # Verifica se o servidor contou os bytes corretamente
    assert data["received_bytes"] == 1024 * 1024