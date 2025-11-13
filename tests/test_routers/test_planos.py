"""
Testes para os endpoints Públicos (/planos)
"""
from fastapi.testclient import TestClient
from provedor_api.main import app 

client = TestClient(app)

# --- Testes Públicos (Usuário) ---

def test_listar_planos_publico():
    """Testa se qualquer um (mesmo sem token) pode listar os planos."""
    response = client.get("/planos/") # Adicionada barra final
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_obter_plano_especifico_publico():
    """Testa se qualquer um pode ver um plano específico (Plano ID 1)."""
    # Nota: os testes rodam em ordem não garantida.
    # Vamos testar o ID 1, que deve existir.
    response = client.get("/planos/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_obter_plano_inexistente():
    """Testa a busca por um plano que não existe."""
    response = client.get("/planos/999")
    assert response.status_code == 404