import logging
import spacy
from modules.brain.llm_brain import LLMBrain

logger = logging.getLogger(__name__)

class Brain:
    def __init__(self, config):
        self.config = config
        self.llm = LLMBrain(config)
        
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            logger.warning("spaCy model not found. Run 'python -m spacy download en_core_web_sm'")
            self.nlp = None

        # detailed intent patterns
        self.intents = {
            "greeting": ["hello", "hi", "hey", "good morning", "good evening"],
            "goodbye": ["bye", "goodbye", "exit", "quit", "shutdown"],
            "time": ["what time is it", "current time", "tell me the time"],
            "date": ["what is the date", "what's the date", "today's date"],
            "weather": ["what's the weather", "how is the weather", "weather forecast"],
            "who_are_you": ["who are you", "what is your name", "introduce yourself"]
        }

    def process(self, text):
        """
        Process the user input and return the identified intent and entities.
        If no intent matches, return "llm_query" intent and the full text as entity.
        """
        text = text.strip() # Don't lower yet, spaCy needs case
        logger.info(f"Processing text: {text}")

        # spaCy Entity Extraction
        entities = {}
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                # Map spaCy labels to our internal keys if needed
                if ent.label_ == "GPE": # Geopolitical Entity (City/Country)
                    entities["city"] = ent.text
                elif ent.label_ == "PERSON":
                    entities["person"] = ent.text
        
        text_lower = text.lower()
        for intent, patterns in self.intents.items():
            for pattern in patterns:
                if pattern in text_lower:
                    return intent, entities 
        
        # Fallback to LLM
        return "llm_query", {"query": text, "spacy_entities": entities}
