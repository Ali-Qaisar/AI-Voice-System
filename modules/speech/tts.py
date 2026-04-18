import logging
import os
import tempfile

logger = logging.getLogger(__name__)

class TTS:
    def __init__(self, config):
        self.config = config
        self.engine_type = config.TTS_ENGINE

    def speak(self, text):
        """
        Synthesizes text to speech using online services.
        """
        logger.info(f"Speaking: {text}")
        print(f"[Friday]: {text}")
        
        try:
            if self.engine_type == "google_cloud":
                self._speak_google_cloud(text)
            elif self.engine_type == "elevenlabs":
                self._speak_elevenlabs(text)
            else:
                # Default to gTTS (Google Text-to-Speech - free online API)
                self._speak_gtts(text)
        except Exception as e:
            logger.error(f"TTS Error: {e}")
            print(f"[Error] Could not synthesize speech: {e}")

    def _speak_gtts(self, text):
        """Uses Google Text-to-Speech (free online API)"""
        from gtts import gTTS
        import pygame
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            temp_file = fp.name
        
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(temp_file)
        
        # Use pygame for better audio playback on Windows
        pygame.mixer.init()
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        pygame.mixer.quit()
        os.remove(temp_file)

    def _speak_google_cloud(self, text):
        """Uses Google Cloud Text-to-Speech API (requires API key)"""
        from google.cloud import texttospeech
        import pygame
        
        client = texttospeech.TextToSpeechClient()
        
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Neural2-F",  # Female voice
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            temp_file = fp.name
            fp.write(response.audio_content)
        
        pygame.mixer.init()
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        pygame.mixer.quit()
        os.remove(temp_file)

    def _speak_elevenlabs(self, text):
        """Uses ElevenLabs API (requires API key)"""
        import requests
        import pygame
        
        api_key = self.config.ELEVENLABS_API_KEY
        voice_id = "21m00Tcm4TlvDq8ikWAM"  # Default voice
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            temp_file = fp.name
            fp.write(response.content)
        
        pygame.mixer.init()
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        pygame.mixer.quit()
        os.remove(temp_file)
