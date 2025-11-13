"""
Ponto de Entrada Principal da Aplicação FastAPI.
Este arquivo é responsável por:
1. Inicializar o objeto FastAPI.
2. Configurar o CORS (para permitir que o frontend se conecte).
3. Incluir os roteadores (endpoints) dos outros arquivos.
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <--- 1. IMPORTAÇÃO ADICIONADA

# Importa seus arquivos de rotas
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

# --- [INÍCIO DA CORREÇÃO CORS] ---
# Define as "origens" (seu frontend) que podem acessar esta API.
# O Live Server do VS Code geralmente usa a porta 5500.
origins = [
    "http://127.0.0.1:5500",  # Porta padrão do Live Server
    "http://localhost:5500",
    "http://127.0.0.1:8080",  # Outra porta comum
    "http://localhost:8080",
    # Você também pode abrir o index.html como um arquivo (file://)
    # Nesse caso, para testes locais, "*" pode ser necessário
    # se as portas acima não funcionarem.
    # "*" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Permite as origens da lista
    allow_credentials=True,    # Permite envio de credenciais (como cookies ou tokens)
    allow_methods=["*"],         # Permite todos os métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],         # Permite todos os cabeçalhos (incluindo o nosso 'X-Token')
)
# --- [FIM DA CORREÇÃO CORS] ---


# --- Inclusão dos Routers ---
# Adiciona os endpoints que estão nos outros arquivos
logger.info("Incluindo router de planos (público)")
app.include_router(planos.router, tags=["Planos (Público)"])

logger.info("Incluindo router de usuários (assinatura)")
app.include_router(usuarios.router, tags=["Usuários (Assinatura)"])

logger.info("Incluindo router de admin (gerenciamento)")
app.include_router(admin.router, prefix="/admin", tags=["Admin (Gerenciamento)"])


@app.get("/", tags=["Root"])
async def read_root():
    """Endpoint raiz para verificar se a API está online."""
    logger.info("Acessando endpoint raiz (/)")
    return {"message": "Bem-vindo à API ProvedorNet! Acesse /docs para a documentação."}