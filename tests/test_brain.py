import unittest
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Config
from modules.brain.nlp import Brain

class TestBrain(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.brain = Brain(self.config)

    def test_greeting_intent(self):
        input_text = "Hello Friday"
        intent, entities = self.brain.process(input_text)
        self.assertEqual(intent, "greeting")

    def test_time_intent(self):
        input_text = "What time is it?"
        intent, entities = self.brain.process(input_text)
        self.assertEqual(intent, "time")

    def test_weather_intent(self):
        input_text = "What's the weather like?"
        intent, entities = self.brain.process(input_text)
        self.assertEqual(intent, "weather")

    def test_unknown_intent(self):
        input_text = "Blah blah blah"
        intent, entities = self.brain.process(input_text)
        self.assertEqual(intent, "llm_query")

if __name__ == '__main__':
    unittest.main()
