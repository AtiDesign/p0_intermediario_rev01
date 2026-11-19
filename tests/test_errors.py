# Testes simulados (credencial inválida, timeout, etc.)
import os
import sys
import unittest
from unittest.mock import MagicMock, patch
import requests

# Garante que a pasta src esteja visível para os testes
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from config import AppConfig, load_config
from exceptions import (
    ConfigError,
    LLMAuthError,
    LLMConnectionError,
    LLMResponseError,
)
from llm_client import call_model, parse_response


class TestLLMErrorHandling(unittest.TestCase):

    def setUp(self):
        self.mock_config = AppConfig(
            api_url="https://api.exemplo.com/v1/chat/completions",
            api_key="chave-falsa-para-teste",
            model_name="modelo-teste",
            timeout=5
        )

    @patch.dict(os.environ, {"LLM_API_URL": "https://api.exemplo.com", "LLM_API_KEY": "", "LLM_MODEL_NAME": "gpt"}, clear=True)
    @patch("config.load_dotenv")
    def test_missing_credential(self, _mock_dotenv):
        """Simula credencial ausente no ambiente."""
        with self.assertRaises(ConfigError) as ctx:
            load_config()
        self.assertIn("Credencial ausente", str(ctx.exception))

    @patch("llm_client.requests.post")
    def test_invalid_credential(self, mock_post):
        """Simula retorno HTTP 401 (credencial inválida)."""
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_resp.ok = False
        mock_post.return_value = mock_resp

        with self.assertRaises(LLMAuthError) as ctx:
            call_model({}, {}, self.mock_config)
        self.assertIn("credencial informada é inválida", str(ctx.exception))

    @patch("llm_client.requests.post", side_effect=requests.exceptions.Timeout)
    def test_timeout(self, _mock_post):
        """Simula estouro de tempo limite (Timeout)."""
        with self.assertRaises(LLMConnectionError) as ctx:
            call_model({}, {}, self.mock_config)
        self.assertIn("Timeout", str(ctx.exception))

    @patch("llm_client.requests.post")
    def test_service_unavailable(self, mock_post):
        """Simula indisponibilidade do servidor (HTTP 503)."""
        mock_resp = MagicMock()
        mock_resp.status_code = 503
        mock_resp.ok = False
        mock_post.return_value = mock_resp

        with self.assertRaises(LLMConnectionError) as ctx:
            call_model({}, {}, self.mock_config)
        self.assertIn("indisponível", str(ctx.exception))

    def test_empty_or_malformed_response(self):
        """Simula resposta JSON inesperada."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"unexpected_key": []}

        with self.assertRaises(LLMResponseError) as ctx:
            parse_response(mock_resp)
        self.assertIn("estrutura inesperada", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()