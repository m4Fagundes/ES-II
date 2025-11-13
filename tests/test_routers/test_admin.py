"""
Testes para os endpoints de Admin (/admin/planos)
"""
from fastapi.testclient import TestClient
# Agora importamos a 'app' da nova localização
from provedor_api.main import app 

# --- Configuração ---
client = TestClient(app)

ADMIN_TOKEN = "admin-secret-token"
USER_TOKEN = "user-normal-token"
HEADERS_ADMIN = {"X-Token": ADMIN_TOKEN}
HEADERS_USER = {"X-Token": USER_TOKEN}
HEADERS_NO_TOKEN = {}

# --- Testes de Planos (CRUD Admin) ---

def test_admin_cria_plano_sucesso():
    """Testa se o admin pode criar um novo plano com sucesso."""
    response = client.post(
        "/admin/planos/", # Adicionada barra final (do prefixo do router)
        headers=HEADERS_ADMIN,
        json={"nome": "Plano Teste", "velocidade_mbps": 100, "preco_mensal": 79.90}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Plano Teste"
    assert data["velocidade_mbps"] == 100
    assert data["id"] is not None

def test_admin_cria_plano_sem_auth():
    """Testa que um usuário sem token não pode criar planos."""
    response = client.post(
        "/admin/planos/",
        headers=HEADERS_NO_TOKEN,
        json={"nome": "Plano Falha", "velocidade_mbps": 10, "preco_mensal": 10.0}
    )
    assert response.status_code == 422 # Header 'X-Token' ausente

def test_admin_cria_plano_auth_usuario_comum():
    """Testa que um usuário comum (não-admin) não pode criar planos."""
    response = client.post(
        "/admin/planos/",
        headers=HEADERS_USER,
        json={"nome": "Plano Falha", "velocidade_mbps": 10, "preco_mensal": 10.0}
    )
    assert response.status_code == 403 # Forbidden

def test_admin_altera_plano_sucesso():
    """Testa se o admin pode alterar um plano existente (Plano ID 1)."""
    response = client.put(
        "/admin/planos/1",
        headers=HEADERS_ADMIN,
        json={"nome": "Básico Alterado", "preco_mensal": 55.00}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Básico Alterado"
    assert data["preco_mensal"] == 55.00
    assert data["velocidade_mbps"] == 50 # Não foi alterado

def test_admin_altera_plano_nao_encontrado():
    """Testa a alteração de um plano que não existe."""
    response = client.put(
        "/admin/planos/999",
        headers=HEADERS_ADMIN,
        json={"nome": "Plano Fantasma"}
    )
    assert response.status_code == 404

def test_admin_altera_plano_sem_dados():
    """Testa a alteração de um plano sem enviar dados."""
    response = client.put(
        "/admin/planos/1",
        headers=HEADERS_ADMIN,
        json={} # Nenhum dado
    )
    # Na nova lógica, isso retorna 400
    assert response.status_code == 400

def test_admin_deleta_plano_sucesso():
    """Testa se o admin pode deletar um plano (Plano ID 2)."""
    response = client.delete("/admin/planos/2", headers=HEADERS_ADMIN)
    assert response.status_code == 204 # No Content

    # Verifica se foi deletado
    response_get = client.get("/planos/2")
    assert response_get.status_code == 404

def test_admin_deleta_plano_nao_encontrado():
    """Testa a deleção de um plano que não existe."""
    response = client.delete("/admin/planos/999", headers=HEADERS_ADMIN)
    assert response.status_code == 404