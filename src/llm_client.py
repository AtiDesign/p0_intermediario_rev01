# Preparação da requisição, chamada HTTP e tratamento
import requests
from src.config import AppConfig
from src.exceptions import (
    LLMAuthError,
    LLMConnectionError,
    LLMResponseError,
)

def prepare_request(prompt: str, config: AppConfig) -> tuple[dict, dict]:
    """Prepara cabeçalhos e corpo da solicitação sem expor segredos nos logs."""
    headers = {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": config.model_name,
        "messages": [{"role": "user", "content": prompt}],
    }
    return headers, payload

def call_model(headers: dict, payload: dict, config: AppConfig) -> requests.Response:
    """Executa a chamada HTTP e trata falhas de rede, timeout e status HTTP."""
    try:
        response = requests.post(
            config.api_url,
            headers=headers,
            json=payload,
            timeout=config.timeout
        )
    except requests.exceptions.Timeout:
        raise LLMConnectionError(
            f"O serviço demorou mais de {config.timeout}s para responder (Timeout). Tente novamente mais tarde."
        )
    except requests.exceptions.ConnectionError:
        raise LLMConnectionError(
            "Não foi possível conectar ao serviço de LLM. Verifique sua rede ou a disponibilidade do servidor."
        )
    except requests.exceptions.RequestException:
        raise LLMConnectionError(
            "Ocorreu uma falha inesperada na comunicação com o serviço de LLM."
        )

    if response.status_code in (401, 403):
        raise LLMAuthError(
            "Falha de autenticação: a credencial informada é inválida ou não possui permissão."
        )
    
    if response.status_code >= 500:
        raise LLMConnectionError(
            f"O serviço de LLM está temporariamente indisponível (Erro {response.status_code}). "
            "Caso utilize infraestrutura institucional, aguarde a recuperação pela equipe técnica."
        )

    if not response.ok:
        raise LLMResponseError(
            f"O serviço recusou a solicitação (Código HTTP {response.status_code}). Verifique os parâmetros do modelo."
        )

    return response

def parse_response(response: requests.Response) -> str:
    """Valida e extrai o texto da resposta do modelo."""
    try:
        data = response.json()
    except ValueError:
        raise LLMResponseError("O serviço retornou uma resposta em formato inválido (não é JSON).")

    try:
        # Ajuste o caminho abaixo caso use Google Gemini nativo ou Ollama /api/generate
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise LLMResponseError("A resposta do modelo veio em uma estrutura inesperada.")

    if not content or not str(content).strip():
        raise LLMResponseError("O modelo retornou uma resposta vazia.")

    return str(content).strip()