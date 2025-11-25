from fastapi import APIRouter, HTTPException
from api import models, database
import httpx
import logging

# --- Configurações da API LLM (Baseado na sua imagem) ---
LLM_API_URL = "https://api.longcat.chat/openai/v1/chat/completions"
# Nota de Segurança: Em produção, use variáveis de ambiente (os.getenv)
LLM_API_KEY = "Bearer ak_1H91k98qz9gB74R3m60Fd3OU7F72Y"
LLM_MODEL = "LongCat-Flash-Chat"

router = APIRouter(prefix="/chat", tags=["Chatbot IA"])
logger = logging.getLogger(__name__)

def gerar_prompt_sistema():
    """
    Constrói o contexto da IA. Injeta os dados reais do banco de dados
    para que a IA responda com precisão sobre os produtos.
    """
    # Busca planos atualizados
    planos = database.get_all_planos()
    lista_planos = "\n".join([f"- {p.nome}: {p.velocidade_mbps} Mega por R$ {p.preco_mensal:.2f}/mês" for p in planos])

    return f"""
    Você é o Assistente Virtual da ProvedorNet, um provedor de internet fibra óptica.
    
    SUA MISSÃO:
    Atuar como um atendente comercial e de suporte nível 1. Seja breve, cordial e direto.
    
    REGRAS DE OURO (Contexto do Negócio):
    1. Responda APENAS sobre internet, wifi, roteadores e planos da ProvedorNet.
    2. Se perguntarem sobre outros assuntos (ex: política, futebol), diga: "Desculpe, só posso ajudar com sua conexão de internet."
    3. Use APENAS os planos listados abaixo. Não invente preços ou velocidades.
    4. Para problemas técnicos complexos, peça para ligar no 0800-123-4567.

    NOSSOS PLANOS DISPONÍVEIS AGORA:
    {lista_planos}

    INFORMAÇÕES GERAIS:
    - Instalação: Gratuita (fidelidade 12 meses).
    - Tecnologia: 100% Fibra Óptica até dentro de casa.
    """

@router.post("/enviar", response_model=models.ChatResposta)
async def conversar(dados: models.ChatMensagem):
    """
    Endpoint que recebe a mensagem do usuário e consulta a LLM.
    """
    prompt_sistema = gerar_prompt_sistema()

    # Payload no formato padrão OpenAI (compatível com LongCat)
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": dados.mensagem}
        ],
        "max_tokens": 500,
        "temperature": 0.3, # Baixa temperatura para respostas mais factuais
        "stream": False
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": LLM_API_KEY
    }

    try:
        # Requisição assíncrona para não travar o servidor
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(LLM_API_URL, json=payload, headers=headers)
            
            if response.status_code != 200:
                logger.error(f"Erro na API externa: {response.text}")
                raise HTTPException(status_code=502, detail="Erro ao processar inteligência artificial.")

            dados_resp = response.json()
            # Extrai a resposta de texto
            texto_ia = dados_resp["choices"][0]["message"]["content"]
            
            return models.ChatResposta(resposta=texto_ia)

    except httpx.RequestError as e:
        logger.error(f"Falha de conexão LLM: {e}")
        return models.ChatResposta(resposta="No momento estou em manutenção. Por favor, tente novamente mais tarde.")