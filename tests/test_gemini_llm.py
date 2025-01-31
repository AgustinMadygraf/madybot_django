"""
Path: tests/test_gemini_llm.py

"""

from unittest.mock import Mock
from app.components.services.llm_impl.gemini_llm import GeminiLLMClient

def test_send_message():
    " Prueba para enviar un mensaje al cliente"
    mock_genai = Mock()
    mock_genai.send_message.return_value = Mock(text="Simulated Gemini response")

    client = GeminiLLMClient(api_key="fake_key", system_instruction="system_instruction")
    client.chat_session = mock_genai

    response = client.send_message("Test input")
    assert response == "Simulated Gemini response"
    mock_genai.send_message.assert_called_once_with("Test input")
