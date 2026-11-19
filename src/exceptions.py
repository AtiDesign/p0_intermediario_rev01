# Exceções personalizadas com mensagens amigáveis
class AppError(Exception):
    """Erro base da aplicação com mensagem amigável ao usuário."""
    pass

class ConfigError(AppError):
    """Erro de configuração ou credenciais ausentes."""
    pass

class InputValidationError(AppError):
    """Erro na entrada fornecida pelo usuário."""
    pass

class LLMAuthError(AppError):
    """Erro de autenticação (credencial inválida ou sem permissão)."""
    pass

class LLMConnectionError(AppError):
    """Erro de rede, timeout ou indisponibilidade do serviço."""
    pass

class LLMResponseError(AppError):
    """Erro quando a resposta vem vazia ou em formato inesperado."""
    pass