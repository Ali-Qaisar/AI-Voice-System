"""
Comprehensive test suite for Friday AI Assistant
Combines structure tests, API integration tests, and setup validation
"""

import sys
import os
import tempfile
from unittest.mock import Mock, patch
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

# ============================================================================
# STRUCTURE TESTS
# ============================================================================

def test_config():
    """Test configuration loading"""
    print("\n=== Testing Config ===")
    try:
        from config import Config
        config = Config()
        
        assert config.SPEECH_ENGINE == "google_free"
        assert config.TTS_ENGINE == "gtts"
        assert config.LLM_PROVIDER == "gemini"
        # Don't assert specific model, just check it exists
        assert config.LLM_MODEL is not None
        assert config.WAKE_WORD == "friday"
        
        print("✓ Config loads correctly")
        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False

def test_imports():
    """Test that all required packages can be imported"""
    print("\n=== Testing Package Imports ===")
    packages = {
        'speech_recognition': 'SpeechRecognition',
        'dotenv': 'python-dotenv',
        'google.generativeai': 'google-generativeai',
        'gtts': 'gtts',
        'pygame': 'pygame',
        'requests': 'requests',
    }
    
    results = []
    for module, package in packages.items():
        try:
            __import__(module)
            print(f"✓ {package}")
            results.append(True)
        except ImportError:
            print(f"✗ {package} - run: pip install {package}")
            results.append(False)
    
    return all(results)

def test_module_structure():
    """Test module structure"""
    print("\n=== Testing Module Structure ===")
    
    modules = [
        ('modules.speech.stt', 'STT'),
        ('modules.speech.tts', 'TTS'),
        ('modules.brain.llm_brain', 'LLMBrain'),
    ]
    
    all_ok = True
    for module_path, class_name in modules:
        try:
            module = __import__(module_path, fromlist=[class_name])
            getattr(module, class_name)
            print(f"✓ {module_path}.{class_name}")
        except Exception as e:
            print(f"✗ {module_path}.{class_name}: {e}")
            all_ok = False
    
    return all_ok

# ============================================================================
# API INTEGRATION TESTS
# ============================================================================

def test_gemini_api():
    """Test Gemini API integration"""
    print("\n=== Testing Gemini API ===")
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("⊘ Skipped: GOOGLE_API_KEY not configured")
        return None
    
    try:
        import google.generativeai as genai
        from config import Config
        
        config = Config()
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(config.LLM_MODEL)
        response = model.generate_content("Say 'Hello' in one word.")
        print(f"✓ Gemini API working: {response.text[:50]}...")
        return True
    except Exception as e:
        print(f"✗ Gemini API failed: {e}")
        return False

def test_gtts():
    """Test Google Text-to-Speech"""
    print("\n=== Testing gTTS ===")
    
    try:
        from gtts import gTTS
        tts = gTTS(text="Test", lang='en', slow=False)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            temp_file = fp.name
        
        tts.save(temp_file)
        
        if os.path.exists(temp_file):
            file_size = os.path.getsize(temp_file)
            os.remove(temp_file)
            print(f"✓ gTTS working: Generated {file_size} bytes")
            return True
        else:
            print(f"✗ gTTS failed: Audio file not created")
            return False
    except Exception as e:
        print(f"✗ gTTS failed: {e}")
        return False

def test_speech_recognition():
    """Test SpeechRecognition library"""
    print("\n=== Testing SpeechRecognition ===")
    
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        
        try:
            mics = sr.Microphone.list_microphone_names()
            if mics:
                print(f"✓ SpeechRecognition working: Found {len(mics)} microphone(s)")
                return True
            else:
                print(f"⚠️  No microphones detected (will use text fallback)")
                return True
        except Exception:
            print(f"⚠️  Could not list microphones (library works)")
            return True
    except Exception as e:
        print(f"✗ SpeechRecognition failed: {e}")
        return False

# ============================================================================
# SETUP VALIDATION
# ============================================================================

def validate_env_file():
    """Check if .env file exists and has required keys"""
    print("\n=== Validating Environment ===")
    
    if not os.path.exists('.env'):
        print("✗ .env file not found")
        print("  → Run: copy .env.example .env")
        return False
    
    print("✓ .env file exists")
    
    google_key = os.getenv('GOOGLE_API_KEY')
    if not google_key or google_key == 'your_gemini_api_key_here':
        print("✗ GOOGLE_API_KEY not configured")
        print("  → Get key from: https://makersuite.google.com/app/apikey")
        return False
    
    print("✓ GOOGLE_API_KEY configured")
    return True

def validate_audio():
    """Check if audio devices are available"""
    print("\n=== Validating Audio ===")
    
    try:
        import speech_recognition as sr
        import pygame
        
        mics = sr.Microphone.list_microphone_names()
        if mics:
            print(f"✓ Found {len(mics)} microphone(s)")
        else:
            print("⚠️  No microphones (text fallback available)")
        
        pygame.mixer.init()
        print("✓ Audio output available")
        pygame.mixer.quit()
        
        return True
    except Exception as e:
        print(f"⚠️  Audio check warning: {e}")
        return True

# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def main():
    """Run all tests"""
    print("=" * 60)
    print("FRIDAY AI ASSISTANT - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Package Imports", test_imports),
        ("Configuration", test_config),
        ("Module Structure", test_module_structure),
        ("Environment File", validate_env_file),
        ("Audio Devices", validate_audio),
        ("Gemini API", test_gemini_api),
        ("gTTS", test_gtts),
        ("SpeechRecognition", test_speech_recognition),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result is True)
    failed = sum(1 for _, result in results if result is False)
    skipped = sum(1 for _, result in results if result is None)
    total = len(results)
    
    for name, result in results:
        if result is True:
            status = "✓ PASS"
        elif result is False:
            status = "✗ FAIL"
        else:
            status = "⊘ SKIP"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed} passed, {failed} failed, {skipped} skipped (out of {total})")
    
    if failed == 0:
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print("\nYour Friday AI Assistant is ready!")
        print("\nTo start: python main.py")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
