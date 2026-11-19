# Carregamento e validação de configurações/.env
import os
from dataclasses import dataclass
from dotenv import load_dotenv
from src.exceptions import ConfigError

@dataclass
class AppConfig:
    api_url: str
    api_key: str
    model_name: str
    timeout: int = 15

def load_config() -> AppConfig:
    load_dotenv()

    api_url = os.getenv("LLM_API_URL", "").strip()
    api_key = os.getenv("LLM_API_KEY", "").strip()
    model_name = os.getenv("LLM_MODEL_NAME", "").strip()
    timeout_raw = os.getenv("LLM_TIMEOUT", "15").strip()

    if not api_url:
        raise ConfigError("Configuração ausente: defina 'LLM_API_URL' no arquivo .env.")
    
    # Validação de credencial ausente (requisito do P0)
    if not api_key:
        raise ConfigError("Credencial ausente: defina 'LLM_API_KEY' no arquivo .env antes de executar.")

    if not model_name:
        raise ConfigError("Configuração ausente: defina 'LLM_MODEL_NAME' no arquivo .env.")

    try:
        timeout = int(timeout_raw)
        if timeout <= 0:
            raise ValueError
    except ValueError:
        raise ConfigError("Configuração inválida: 'LLM_TIMEOUT' deve ser um número inteiro positivo.")

    return AppConfig(
        api_url=api_url,
        api_key=api_key,
        model_name=model_name,
        timeout=timeout
    )