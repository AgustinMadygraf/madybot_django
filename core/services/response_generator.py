from typing import Optional
from core.logs.config_logger import LoggerConfigurator
from core.services.model_config import ModelConfig
from core.services.llm_impl.gemini_llm import GeminiLLMClient  # Add this import

logger = LoggerConfigurator().configure()

class ResponseGenerator:
    def __init__(self, llm_client=None, logger=None):
        """
        Flexible constructor supporting multiple initialization scenarios.
        """
        self.logger = logger or LoggerConfigurator().configure()
        self.model_config = ModelConfig(logger=self.logger)
        
        # Use the LLM client if provided, otherwise create a new one
        self.model = llm_client or self.model_config.create_llm_client()
        
        # Wrap Gemini client to provide required interface
        if isinstance(self.model, GeminiLLMClient):
            self.model.start_chat = self._gemini_start_chat
        
        self.logger.info("ResponseGenerator initialized")

    def _gemini_start_chat(self):
        """
        Custom method to simulate start_chat for Gemini client
        """
        class ChatSession:
            def __init__(self, model):
                self.model = model
            
            def send_message(self, message):
                response_text = self.model.send_message(message)
                return type('Response', (object,), {'text': response_text})()
        
        return ChatSession(self.model)

    def generate_response(self, message_input: str) -> str:
        """Generate a response from the input message."""
        self.logger.info(f"Generating response for: {message_input}")
        try:
            chat_session = self.model.start_chat()
            response = chat_session.send_message(message_input)
            return response.text
        except Exception as e:
            self.logger.error(f"Response generation error: {e}")
            raise

    def generate_response_streaming(self, message_input: str, chunk_size: int = 30) -> str:
        """Simulate streaming response generation."""
        return self.generate_response(message_input)