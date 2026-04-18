import os
import sys
import logging
from config import Config
from modules.speech.stt import STT
from modules.speech.tts import TTS
from modules.speech.wakeword import WakeWord
from modules.brain.nlp import Brain
from modules.brain.context import ContextManager
from modules.skills.registry import SkillRegistry

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Friday:
    def __init__(self):
        self.config = Config()
        logger.info("Initializing Friday...")
        
        # Initialize Modules
        self.tts = TTS(self.config)
        self.stt = STT(self.config)
        self.brain = Brain(self.config)
        self.wake_word = WakeWord(self.config)
        self.context = ContextManager(self.config)
        self.skills = SkillRegistry(self.tts, self.context)
        
        logger.info("Jarvis Initialized.")

    def start(self):
        logger.info("Friday is starting up...")
        self.tts.speak("Friday is online and listening.")
        # We block here now for standalone voice loop.
        self.run_loop() 

    def process_command(self, text):
        """
        Process a text command from API or Voice.
        """
        self.context.add_turn("user", text)
        intent, entities = self.brain.process(text)
        self.skills.execute(intent, entities)
        return intent

    def run_loop(self):
        logger.info("Entering main interaction loop. Press Ctrl+C to exit.")
        while True:
            # 0. Wait for Wake Word
            print(f"[Friday] >>> Listening for '{self.config.WAKE_WORD}'...", end="\r")
            if not self.wake_word.listen():
                continue
                
            print(f"\n[Friday] Wake word detected!")
            self.tts.speak("Yes?") # Acknowledge

            # 1. Listen (STT)
            print("[Friday] Listening for command...")
            user_input = self.stt.listen()
            
            if not user_input:
                self.tts.speak("I'm sorry, I didn't catch that. Could you please repeat?")
                continue

            # 2. Process
            self.process_command(user_input)
            
            # (Ideally we'd add the system response to memory too, but SkillRegistry handles TTS directly right now)
            
    def shutdown(self):
        logger.info("Shutting down Friday...")
        self.tts.speak("Shutting down.")
        sys.exit(0)

if __name__ == "__main__":
    friday = Friday()
    friday.start()
