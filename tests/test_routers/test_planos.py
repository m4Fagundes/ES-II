"""
Testes para os endpoints públicos de Planos (/planos)
"""
from fastapi.testclient import TestClient
# Importa a instância da aplicação principal
from api.main import app 

# --- Configuração ---
client = TestClient(app)

# --- Testes de Planos (Público) ---

def test_listar_planos_publico():
    """Testa se a lista de planos é retornada com sucesso e contém os itens iniciais."""
    response = client.get("/planos/")
    
    # Deve retornar sucesso (200 OK)
    assert response.status_code == 200
    
    data = response.json()
    # Deve retornar uma lista
    assert isinstance(data, list)
    # Deve conter os 2 planos iniciais do DB mock
    assert len(data) >= 2 
    # Verifica a estrutura básica de um plano
    assert "nome" in data[0]
    assert "id" in data[0]


def test_obter_plano_existente():
    """Testa a obtenção de um plano pelo ID que existe (ID 1)."""
    # Plano 1 é o "Básico" no DB mock
    response = client.get("/planos/1")
    
    # Deve retornar sucesso (200 OK)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == 1
    assert data["nome"] == "Básico"
    assert data["preco_mensal"] == 49.90


def test_obter_plano_inexistente():
    """Testa a obtenção de um plano com um ID que não existe."""
    # Um ID que certamente não está no DB mock (que só tem 1 e 2 no início)
    response = client.get("/planos/9999") 
    
    # Deve retornar 404 Not Found
    assert response.status_code == 404
    
    data = response.json()
    # Verifica a mensagem de detalhe exata da HTTPException
    assert data["detail"] == "Plano não encontrado"