# Captura de entrada, orquestração e exibição do resultado
import sys
from src.config import load_config
from src.exceptions import AppError, InputValidationError
from src.llm_client import call_model, parse_response, prepare_request

def capture_input() -> str:
    """Captura e valida a entrada do usuário."""
    user_input = input("Digite sua pergunta para o modelo: ").strip()
    if not user_input:
        raise InputValidationError("A entrada não pode estar vazia. Digite uma mensagem válida.")
    return user_input

def display_result(result: str) -> None:
    """Apresenta o resultado formatado ao usuário."""
    print("\n--- Resposta do Modelo ---")
    print(result)
    print("--------------------------\n")

def run() -> None:
    try:
        config = load_config()
        prompt = capture_input()
        headers, payload = prepare_request(prompt, config)
        raw_response = call_model(headers, payload, config)
        answer = parse_response(raw_response)
        display_result(answer)

    except AppError as err:
        print(f"\n[Aviso] {err}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[Aviso] Execução interrompida pelo usuário.", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    run()