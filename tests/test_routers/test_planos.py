from fastapi.testclient import TestClient
from api.main import app 

client = TestClient(app)

def test_listar_planos_publico():
    """Qualquer um deve poder listar os planos."""
    response = client.get("/planos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Deve haver pelo menos os planos padrão do banco simulado
    assert len(response.json()) >= 1 

def test_obter_plano_por_id_existente():
    """Busca um plano específico (ID 1 sempre existe no mock DB)."""
    response = client.get("/planos/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_obter_plano_inexistente_retorna_404():
    """Busca por ID que não existe."""
    response = client.get("/planos/99999")
    assert response.status_code == 404