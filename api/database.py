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