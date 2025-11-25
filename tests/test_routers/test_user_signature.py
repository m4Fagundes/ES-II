from fastapi.testclient import TestClient
from api.main import app 

client = TestClient(app)
HEADERS_USER = {"X-Token": "user-normal-token"}

def test_usuario_assina_plano_com_sucesso():
    """Usuário logado deve conseguir assinar o plano 1."""
    response = client.post("/assinar/1", headers=HEADERS_USER)
    assert response.status_code == 200
    data = response.json()
    assert data["plano_id"] == 1
    assert data["status"] == "ativo"

def test_usuario_ve_sua_assinatura():
    """Após assinar, o endpoint minha-assinatura deve retornar os dados corretos."""
    # Garante assinatura
    client.post("/assinar/2", headers=HEADERS_USER)
    
    response = client.get("/minha-assinatura", headers=HEADERS_USER)
    assert response.status_code == 200
    assert response.json()["plano_id"] == 2

def test_assinar_plano_inexistente_falha():
    """Tentar assinar plano 9999 deve dar 404."""
    response = client.post("/assinar/9999", headers=HEADERS_USER)
    assert response.status_code == 404

def test_acesso_sem_token_falha():
    """Tentar ver assinatura sem token deve dar 401 ou 422."""
    response = client.get("/minha-assinatura")
    assert response.status_code in [401, 422]