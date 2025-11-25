from fastapi.testclient import TestClient
from api.main import app 

client = TestClient(app)

# Headers de Autenticação
HEADERS_ADMIN = {"X-Token": "admin-secret-token"}
HEADERS_USER = {"X-Token": "user-normal-token"}

def test_admin_deve_criar_plano_com_sucesso():
    """Verifica se o admin consegue criar um plano novo."""
    payload = {
        "nome": "Plano Gamer",
        "velocidade_mbps": 1000,
        "preco_mensal": 199.90
    }
    response = client.post("/admin/planos/", headers=HEADERS_ADMIN, json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Plano Gamer"
    assert data["id"] is not None

def test_usuario_comum_nao_pode_criar_plano():
    """Garante que usuários normais sejam bloqueados (403)."""
    payload = {"nome": "Hacker", "velocidade_mbps": 9999, "preco_mensal": 1.0}
    response = client.post("/admin/planos/", headers=HEADERS_USER, json=payload)
    assert response.status_code == 403

def test_admin_deve_atualizar_plano():
    """Verifica a atualização de um plano existente."""
    # 1. Cria
    criado = client.post("/admin/planos/", headers=HEADERS_ADMIN, json={"nome": "Antigo", "velocidade_mbps": 10, "preco_mensal": 10}).json()
    id_plano = criado["id"]

    # 2. Atualiza
    response = client.put(f"/admin/planos/{id_plano}", headers=HEADERS_ADMIN, json={"nome": "Novo Nome", "preco_mensal": 20})
    assert response.status_code == 200
    assert response.json()["nome"] == "Novo Nome"
    assert response.json()["velocidade_mbps"] == 10 # Não deve ter mudado

def test_admin_deve_deletar_plano():
    """Verifica a remoção de planos."""
    # 1. Cria para deletar
    criado = client.post("/admin/planos/", headers=HEADERS_ADMIN, json={"nome": "Temp", "velocidade_mbps": 5, "preco_mensal": 5}).json()
    id_plano = criado["id"]

    # 2. Deleta
    response = client.delete(f"/admin/planos/{id_plano}", headers=HEADERS_ADMIN)
    assert response.status_code == 204

    # 3. Verifica se sumiu
    check = client.get(f"/planos/{id_plano}")
    assert check.status_code == 404