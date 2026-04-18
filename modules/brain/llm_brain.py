import logging
import os
import google.generativeai as genai

logger = logging.getLogger(__name__)

class LLMBrain:
    def __init__(self, config):
        self.config = config
        self.provider = getattr(config, 'LLM_PROVIDER', 'gemini')
        self.model_name = config.LLM_MODEL

        if self.provider == 'gemini':
            api_key = getattr(config, 'GOOGLE_API_KEY', None)
            if not api_key:
                logger.error("GOOGLE_API_KEY not found in config. LLM will fail.")
                raise ValueError("GOOGLE_API_KEY is required for Gemini")
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(self.model_name)
        elif self.provider == 'openai':
            api_key = getattr(config, 'OPENAI_API_KEY', None)
            if not api_key:
                logger.error("OPENAI_API_KEY not found in config. LLM will fail.")
                raise ValueError("OPENAI_API_KEY is required for OpenAI")
            from openai import OpenAI
            self.model = OpenAI(api_key=api_key)
        elif self.provider == 'anthropic':
            api_key = getattr(config, 'ANTHROPIC_API_KEY', None)
            if not api_key:
                logger.error("ANTHROPIC_API_KEY not found in config. LLM will fail.")
                raise ValueError("ANTHROPIC_API_KEY is required for Anthropic")
            from anthropic import Anthropic
            self.model = Anthropic(api_key=api_key)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}. Use 'gemini', 'openai', or 'anthropic'")

    def generate_response(self, text, context_history=None):
        """
        Generates a response from the selected online LLM provider.
        """
        if self.provider == 'gemini':
            return self._generate_gemini_response(text, context_history)
        elif self.provider == 'openai':
            return self._generate_openai_response(text, context_history)
        elif self.provider == 'anthropic':
            return self._generate_anthropic_response(text, context_history)

    def _generate_gemini_response(self, text, context_history=None):
        try:
            logger.info(f"Sending to Gemini ({self.model_name})...")
            
            system_prompt = "You are Friday, a highly advanced and helpful AI assistant. You are intelligent, capable, and polite. Keep responses concise and conversational."
            
            messages = [{"role": "user", "parts": [system_prompt]}]
            if context_history:
                for turn in context_history:
                    role = "user" if turn['role'] == 'user' else "model"
                    messages.append({"role": role, "parts": [turn['content']]})
            
            messages.append({"role": "user", "parts": [text]})
            
            response = self.model.generate_content(messages)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API Error: {e}")
            return f"I encountered an error with my online brain: {e}. Please check your API key and connection."

    def _generate_openai_response(self, text, context_history=None):
        try:
            logger.info(f"Sending to OpenAI ({self.model_name})...")
            
            messages = [
                {"role": "system", "content": "You are Friday, a highly advanced and helpful AI assistant. You are intelligent, capable, and polite. Keep responses concise and conversational."}
            ]
            
            if context_history:
                messages.extend(context_history)
            
            messages.append({"role": "user", "content": text})
            
            response = self.model.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API Error: {e}")
            return f"I encountered an error with OpenAI: {e}. Please check your API key and connection."

    def _generate_anthropic_response(self, text, context_history=None):
        try:
            logger.info(f"Sending to Anthropic ({self.model_name})...")
            
            system_prompt = "You are Friday, a highly advanced and helpful AI assistant. You are intelligent, capable, and polite. Keep responses concise and conversational."
            
            messages = []
            if context_history:
                messages.extend(context_history)
            
            messages.append({"role": "user", "content": text})
            
            response = self.model.messages.create(
                model=self.model_name,
                max_tokens=1024,
                system=system_prompt,
                messages=messages
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API Error: {e}")
            return f"I encountered an error with Anthropic: {e}. Please check your API key and connection."
