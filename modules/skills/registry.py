import datetime
import logging
import sys
from modules.skills.weather import WeatherSkill

logger = logging.getLogger(__name__)

class SkillRegistry:
    def __init__(self, tts, context_manager):
        self.tts = tts
        self.context_manager = context_manager
        self.weather_skill = WeatherSkill()
        
        self.skills = {
            "greeting": self.handle_greeting,
            "goodbye": self.handle_goodbye,
            "time": self.handle_time,
            "date": self.handle_date,
            "date": self.handle_date,
            "weather": self.handle_weather,
            "who_are_you": self.handle_intro,
            "llm_query": self.handle_llm,
            "unknown": self.handle_unknown
        }
    
    def execute(self, intent, entities):
        handler = self.skills.get(intent, self.handle_unknown)
        handler(entities)

    def handle_greeting(self, entities):
        name = self.context_manager.get_profile("name")
        response = f"Hello {name}! I am Friday. How can I assist you today?"
        self.tts.speak(response)

    def handle_goodbye(self, entities):
        response = "Goodbye! Shutting down systems."
        self.tts.speak(response)
        sys.exit(0)

    def handle_time(self, entities):
        now = datetime.datetime.now().strftime("%I:%M %p")
        response = f"It is currently {now}."
        self.tts.speak(response)

    def handle_date(self, entities):
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        response = f"Today is {today}."
        self.tts.speak(response)
        
    def handle_weather(self, entities):
        # Check if city entity exists, else use profile default
        city = entities.get("city")
        if not city:
            city = self.context_manager.get_profile("city")
            
        logger.info(f"Checking weather for {city}")
        self.tts.speak(f"Checking weather for {city}...")
        report = self.weather_skill.get_weather(city)
        self.tts.speak(report)

    def handle_intro(self, entities):
        response = "I am Friday, an advanced autonomous AI system designed to assist you."
        self.tts.speak(response)

    def handle_llm(self, entities):
        query = entities.get("query")
        # Get context from manager
        history = self.context_manager.get_context()
        # We need access to the LLM module. 
        # For simplicity, we'll import and instantiate it here if it wasn't passed.
        # Ideally, main.py should pass it. 
        from modules.brain.llm_brain import LLMBrain
        from config import Config
        llm = LLMBrain(Config())
        
        self.tts.speak("Thinking...")
        response = llm.generate_response(query, history)
        self.tts.speak(response)

    def handle_unknown(self, entities):
        # Fallback to LLM if unknown, effectively same as llm_query but for safety
        self.handle_llm({"query": "I didn't understand that."})
