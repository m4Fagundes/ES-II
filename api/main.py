"""
Ponto de Entrada Principal da Aplicação FastAPI.
Este arquivo é responsável por:
1. Inicializar o objeto FastAPI.
2. Configurar o CORS (para permitir que o frontend se conecte).
3. Incluir os roteadores (endpoints) dos outros arquivos.
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa seus arquivos de rotas
# Assumimos que o roteador de planos (público) também existe
from .routers import planos, usuarios, admin 

# Configuração de logging (boa prática)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Inicialização da Aplicação ---
app = FastAPI(
    title="ProvedorNet API",
    description="API para gerenciamento de planos e assinaturas de internet.",
    version="1.0.0",
)

# --- Configuração CORS ---
origins = [
    "http://127.0.0.1:5500", 
    "http://localhost:5500",
    "http://127.0.0.1:8080", 
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)
# --- Fim Configuração CORS ---


# --- Inclusão dos Routers ---
logger.info("Incluindo router de planos (público)")
# Assumindo que o router de planos públicos não tem prefixo e define rotas como /planos
app.include_router(planos.router, tags=["Planos (Público)"]) 

logger.info("Incluindo router de usuários (assinatura)")
app.include_router(usuarios.router, tags=["Usuários (Assinatura)"])

# INCLUSÃO CORRETA: /admin + /planos (do admin.py) = /admin/planos
logger.info("Incluindo router de admin (gerenciamento)")
app.include_router(admin.router, prefix="/admin", tags=["Admin (Gerenciamento)"])


@app.get("/", tags=["Root"])
async def read_root():
    """Endpoint raiz para verificar se a API está online."""
    logger.info("Acessando endpoint raiz (/)")
    return {"message": "Bem-vindo à API ProvedorNet! Acesse /docs para a documentação."}