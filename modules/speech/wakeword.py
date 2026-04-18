import speech_recognition as sr
import logging
import time

logger = logging.getLogger(__name__)

class WakeWord:
    def __init__(self, config):
        self.config = config
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone() if self._has_microphone() else None
        self.wake_word = config.WAKE_WORD.lower()

    def _has_microphone(self):
        try:
            return len(sr.Microphone.list_microphone_names()) > 0
        except:
            return False

    def listen(self):
        """
        Listens continuously for the wake word.
        Returns True if wake word detected, False otherwise.
        """
        if not self.microphone:
            print("[System] Press Enter to wake Friday...")
            input()
            return True

        # Use a more stable listening approach
        with self.microphone as source:
            # Calibrate once at start or periodically
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                # listen for a short burst
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=2)
                
                # Use Google for wake word (fast, usually reliable for one word)
                text = self.recognizer.recognize_google(audio).lower()
                
                if self.wake_word in text:
                    return True
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                pass 
            except Exception as e:
                # Log critical errors but don't crash
                if "overflow" not in str(e).lower():
                    logger.debug(f"Wake word listener info: {e}")
        
        return False
