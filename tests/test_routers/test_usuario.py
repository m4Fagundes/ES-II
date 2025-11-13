"""
Testes para os endpoints de Usuário (/assinar, /minha-assinatura)
"""
from fastapi.testclient import TestClient
from api.main import app 

client = TestClient(app)

USER_TOKEN = "user-normal-token"
ADMIN_TOKEN = "admin-secret-token" # Admin também é um usuário
HEADERS_USER = {"X-Token": USER_TOKEN}
HEADERS_ADMIN = {"X-Token": ADMIN_TOKEN}

# --- Testes de Assinatura (Usuário) ---

def test_usuario_assina_plano_sucesso():
    """Testa se um usuário comum pode assinar um plano."""
    response = client.post("/assinar/1", headers=HEADERS_USER)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == USER_TOKEN
    assert data["plano_id"] == 1
    assert data["status"] == "ativo"

def test_usuario_ve_minha_assinatura():
    """Testa se o usuário pode ver a assinatura que acabou de fazer."""
    # Primeiro, garante que ele assinou
    client.post("/assinar/1", headers=HEADERS_USER)
    
    # Agora, testa o GET
    response = client.get("/minha-assinatura", headers=HEADERS_USER)
    assert response.status_code == 200
    data = response.json()
    assert data["plano_id"] == 1
    assert data["user_id"] == USER_TOKEN

def test_usuario_assina_plano_inexistente():
    """Testa a assinatura de um plano que não existe."""
    response = client.post("/assinar/999", headers=HEADERS_USER)
    assert response.status_code == 404

def test_usuario_ve_assinatura_sem_ter_assinado():
    """Testa um admin (que ainda não assinou nada) vendo suas assinaturas."""
    # O token de admin é um user_id diferente do USER_TOKEN
    response = client.get("/minha-assinatura", headers=HEADERS_ADMIN)
    assert response.status_code == 404 # Admin ainda não assinou