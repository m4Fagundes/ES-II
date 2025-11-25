from fastapi.testclient import TestClient
from api.main import app 

client = TestClient(app)

HEADERS_ADMIN = {"X-Token": "admin-secret-token"}
HEADERS_USER = {"X-Token": "user-normal-token"}

def test_admin_deve_criar_plano_com_sucesso():
    payload = {
        "nome": "Plano Gamer",
        "velocidade_mbps": 1000,
        "preco_mensal": 199.90
    }
    # Nota: O prefixo no router é /admin/planos. 
    # O FastAPI redireciona /admin/planos/ para /admin/planos geralmente, 
    # mas vamos ser exatos.
    response = client.post("/admin/planos/", headers=HEADERS_ADMIN, json=payload)
    
    # Se der 404 aqui, verifique se o api/main.py não está duplicando o prefixo
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Plano Gamer"
    assert data["id"] is not None

def test_usuario_comum_nao_pode_criar_plano():
    payload = {"nome": "Hacker", "velocidade_mbps": 9999, "preco_mensal": 1.0}
    response = client.post("/admin/planos/", headers=HEADERS_USER, json=payload)
    assert response.status_code == 403

def test_admin_deve_atualizar_plano():
    # 1. Cria
    criado = client.post("/admin/planos/", headers=HEADERS_ADMIN, json={"nome": "Antigo", "velocidade_mbps": 10, "preco_mensal": 10}).json()
    
    # Proteção caso a criação falhe no teste anterior
    assert "id" in criado, f"Falha ao criar plano: {criado}"
    id_plano = criado["id"]

    # 2. Atualiza
    response = client.put(f"/admin/planos/{id_plano}", headers=HEADERS_ADMIN, json={"nome": "Novo Nome", "preco_mensal": 20})
    assert response.status_code == 200
    assert response.json()["nome"] == "Novo Nome"

def test_admin_deve_deletar_plano():
    # 1. Cria para deletar
    criado = client.post("/admin/planos/", headers=HEADERS_ADMIN, json={"nome": "Temp", "velocidade_mbps": 5, "preco_mensal": 5}).json()
    
    assert "id" in criado
    id_plano = criado["id"]

    # 2. Deleta
    response = client.delete(f"/admin/planos/{id_plano}", headers=HEADERS_ADMIN)
    assert response.status_code == 204

    # 3. Verifica se sumiu
    check = client.get(f"/planos/{id_plano}")
    assert check.status_code == 404