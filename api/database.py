"""
Camada de Acesso a Dados (Simulação de Repositório).

Em uma aplicação real, este módulo conteria as consultas SQL (com SQLAlchemy)
ou NoSQL (com Motor/Pymongo). Ele abstrai *como* os dados são
armazenados e recuperados.

Para este exemplo, continuamos usando um dicionário em memória,
mas agora encapsulado em funções.
"""
import logging
from typing import Dict, Optional, List
from api import models

logger = logging.getLogger(__name__)

# --- Simulação do Banco de Dados (privado) ---
_db_planos: Dict[int, models.Plano] = {
    1: models.Plano(id=1, nome="Básico", velocidade_mbps=50, preco_mensal=49.90),
    2: models.Plano(id=2, nome="Fibra Max", velocidade_mbps=500, preco_mensal=99.90),
}
_db_assinaturas: Dict[str, models.Assinatura] = {} # Key: user_id
_next_plano_id = 3

# --- Funções de Acesso: Planos (Interface do Repositório) ---

def get_all_planos() -> List[models.Plano]:
    """Retorna todos os planos do banco de dados."""
    return list(_db_planos.values())

def get_plano_by_id(plano_id: int) -> Optional[models.Plano]:
    """Busca um plano pelo ID."""
    return _db_planos.get(plano_id)

def create_novo_plano(plano_data: models.PlanoCreate) -> models.Plano:
    """Cria um novo plano no banco de dados."""
    global _next_plano_id
    
    novo_plano = models.Plano(id=_next_plano_id, **plano_data.model_dump())
    _db_planos[novo_plano.id] = novo_plano
    
    logger.info(f"Plano {novo_plano.id} criado: {novo_plano.nome}")
    _next_plano_id += 1
    return novo_plano

def update_plano_by_id(plano_id: int, plano_data: models.PlanoUpdate) -> Optional[models.Plano]:
    """Atualiza um plano existente no banco de dados."""
    plano_existente = _db_planos.get(plano_id)
    if not plano_existente:
        return None

    update_data = plano_data.model_dump(exclude_unset=True)
    if not update_data:
        # Nenhum dado foi enviado, mas consideramos a operação "bem-sucedida"
        # retornando o plano existente sem alterações.
        return plano_existente
        
    updated_plano = plano_existente.model_copy(update=update_data)
    _db_planos[plano_id] = updated_plano
    logger.info(f"Plano {plano_id} atualizado.")
    return updated_plano

def delete_plano_by_id(plano_id: int) -> bool:
    """Deleta um plano. Retorna True se deletado, False se não encontrado."""
    if plano_id not in _db_planos:
        return False
    
    del _db_planos[plano_id]
    logger.info(f"Plano {plano_id} deletado.")
    return True

# --- Funções de Acesso: Assinaturas ---

def get_assinatura_by_user_id(user_id: str) -> Optional[models.Assinatura]:
    """Busca uma assinatura pelo ID do usuário."""
    return _db_assinaturas.get(user_id)

def create_assinatura(user_id: str, plano_id: int) -> models.Assinatura:
    """Cria ou atualiza uma assinatura para um usuário."""
    assinatura = models.Assinatura(user_id=user_id, plano_id=plano_id)
    _db_assinaturas[user_id] = assinatura
    logger.info(f"Usuário {user_id} assinou/atualizou o plano {plano_id}.")
    return assinatura

_db_users = {
    "admin@admin.com": {"email": "admin@admin.com", "password": "123", "nome": "Administrador", "role": "admin", "id": "admin-secret-token"},
    "user@user.com": {"email": "user@user.com", "password": "123", "nome": "Cliente Teste", "role": "user", "id": "user-normal-token"}
}   

# --- Funções de Auth ---
def get_user_by_email(email: str):
    return _db_users.get(email)

def create_user(user_data: models.UserCreate):
    if user_data.email in _db_users:
        return None
    # Simulando geração de token simples
    fake_token = f"token-{user_data.email}"
    new_user = {
        "email": user_data.email,
        "password": user_data.password, # Em prod, use hash!
        "nome": user_data.nome,
        "role": "user",
        "id": fake_token
    }
    _db_users[user_data.email] = new_user
    return new_user

# --- Função Financeira para o Admin ---
def get_dados_financeiros():
    total_receita = 0.0
    contagem_planos = {}
    
    # Itera sobre todas as assinaturas
    for user_id, assinatura in _db_assinaturas.items():
        if assinatura.status == "ativo":
            plano = _db_planos.get(assinatura.plano_id)
            if plano:
                total_receita += plano.preco_mensal
                
                # Contagem por tipo de plano
                nome = plano.nome
                contagem_planos[nome] = contagem_planos.get(nome, 0) + 1
                
    total_users = len(_db_assinaturas)
    ticket_medio = (total_receita / total_users) if total_users > 0 else 0
    
    return {
        "total_receita_mensal": total_receita,
        "total_assinantes": total_users,
        "ticket_medio": ticket_medio,
        "planos_vendidos": contagem_planos
    }