import unittest
from unittest.mock import MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.skills.registry import SkillRegistry
from modules.brain.context import ContextManager
from config import Config

class TestSkills(unittest.TestCase):
    def setUp(self):
        self.mock_tts = MagicMock()
        self.config = Config()
        self.context = ContextManager(self.config)
        self.registry = SkillRegistry(self.mock_tts, self.context)

    def test_time_skill(self):
        # execute time skill
        self.registry.execute("time", {})
        # Verify TTS was called
        self.mock_tts.speak.assert_called()
        # Verify call contained "current" or typical time format
        args, _ = self.mock_tts.speak.call_args
        self.assertIn("It is currently", args[0])

    def test_greeting_with_context(self):
        # Set user name
        self.context.update_profile("name", "TestUser")
        
        self.registry.execute("greeting", {})
        
        args, _ = self.mock_tts.speak.call_args
        self.assertIn("Hello TestUser", args[0])

if __name__ == '__main__':
    unittest.main()
