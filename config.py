import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    def __init__(self):
        # Speech Settings (now using online services)
        self.SPEECH_ENGINE = os.getenv("SPEECH_ENGINE", "google_free") # 'google_free', 'google', 'whisper_api'
        self.TTS_ENGINE = os.getenv("TTS_ENGINE", "gtts")              # 'gtts', 'google_cloud', 'elevenlabs'

        # API Keys
        self.GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        self.ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
        self.ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

        # Brain Settings (now using online models only)
        self.LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")     # 'gemini', 'openai', 'anthropic'
        self.LLM_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-flash") # Model name for the provider

        # System Settings
        self.WAKE_WORD = os.getenv("WAKE_WORD", "friday")
