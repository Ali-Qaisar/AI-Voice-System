import speech_recognition as sr
import logging
import os

logger = logging.getLogger(__name__)

class STT:
    def __init__(self, config):
        self.config = config
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone() if self._has_microphone() else None
        
    def _has_microphone(self):
        try:
            return len(sr.Microphone.list_microphone_names()) > 0
        except:
            return False

    def listen(self):
        """
        Listens to the microphone and returns the transcribed text.
        Uses online speech recognition services.
        """
        if not self.microphone:
            print("[System] No microphone detected. Please type your command:")
            return input(">> ")

        with self.microphone as source:
            logger.info("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source)
            print("[Friday] Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                # Use online speech recognition based on config
                if self.config.SPEECH_ENGINE == "google":
                    print("[Friday] Recognizing (Google Cloud Speech)...")
                    text = self.recognizer.recognize_google_cloud(
                        audio,
                        credentials_json=self.config.GOOGLE_APPLICATION_CREDENTIALS
                    )
                elif self.config.SPEECH_ENGINE == "whisper_api":
                    print("[Friday] Recognizing (OpenAI Whisper API)...")
                    text = self.recognizer.recognize_whisper_api(
                        audio,
                        api_key=self.config.OPENAI_API_KEY
                    )
                else:
                    # Default to Google's free API
                    print("[Friday] Recognizing (Google Web Speech API)...")
                    text = self.recognizer.recognize_google(audio)
                
                logger.info(f"Heard: {text}")
                return text
            except sr.WaitTimeoutError:
                logger.warning("Listening timed out.")
                return ""
            except sr.UnknownValueError:
                logger.warning("Could not understand audio.")
                return ""
            except sr.RequestError as e:
                logger.error(f"Could not request results; {e}")
                return ""
            except Exception as e:
                logger.error(f"Error during listening: {e}")
                return ""
