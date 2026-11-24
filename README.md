# p0_intermediario_rev01
Extrator de informação de contato

# Integração com LLM — Nível Intermediário

Aplicação desenvolvida em Python para interação com Modelos de Linguagem (LLMs), evoluída para o **Nível Intermediário** com foco em separação de responsabilidades, tratamento de falhas previsíveis, interface gráfica desktop e testes automatizados.

---

## Arquitetura e Organização do Código

O projeto está estruturado em módulos com responsabilidades bem definidas dentro do diretório `src/`:

* **`src/config.py`**: Carrega as variáveis de ambiente a partir do arquivo `.env` na raiz do projeto e valida a presença e integridade das configurações obrigatórias antes de qualquer chamada externa.
* **`src/exceptions.py`**: Define exceções personalizadas (`AppError`, `ConfigError`, `InputValidationError`, `LLMAuthError`, `LLMConnectionError`, `LLMResponseError`) para traduzir falhas técnicas em mensagens claras e amigáveis ao usuário.
* **`src/llm_client.py`**: Concentra a preparação dos cabeçalhos e do *payload* (`prepare_request`), a execução da requisição HTTP com controle de timeout (`call_model`) e a extração/validação da resposta (`parse_response`).
* **`src/main.py`**: Orquestra o fluxo principal via linha de comando (CLI), realizando a captura e validação da entrada do usuário (`capture_input`), acionando o cliente LLM e apresentando o resultado (`display_result`).
* **`src/gui.py`**: Interface gráfica desktop desenvolvida com `tkinter` que reutiliza os módulos de configuração, cliente LLM e tratamento de exceções para extrair informações de contato (nomes, e-mails, telefones e URLs) de forma visual e assíncrona.
* **`tests/test_errors.py`**: Suíte de testes unitários com simulação (*mocks*) para validar cenários de falha de forma determinística, sem depender de instabilidades reais no servidor ou expor credenciais.

---

## Pré-requisitos e Instalação

1. **Clone o repositório e acesse a pasta do projeto:**
   ```bash
   git clone [https://github.com/AtiDesign/p0_intermediario_rev01.git](https://github.com/AtiDesign/p0_intermediario_rev01.git)
   cd p0_intermediario_rev01