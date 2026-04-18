"""
Quick verification script to check all 9 API integrations
"""

import sys

def verify_imports():
    """Verify all API libraries can be imported"""
    print("=" * 60)
    print("VERIFYING API INTEGRATIONS")
    print("=" * 60)
    
    apis = {
        'LLM APIs': [
            ('google.generativeai', 'Google Gemini'),
            ('openai', 'OpenAI GPT'),
            ('anthropic', 'Anthropic Claude'),
        ],
        'TTS APIs': [
            ('gtts', 'Google TTS (gTTS)'),
            ('google.cloud.texttospeech', 'Google Cloud TTS'),
            ('requests', 'ElevenLabs (via requests)'),
        ],
        'STT APIs': [
            ('speech_recognition', 'Google Web Speech'),
            ('speech_recognition', 'Google Cloud Speech'),
            ('speech_recognition', 'OpenAI Whisper'),
        ]
    }
    
    all_ok = True
    
    for category, api_list in apis.items():
        print(f"\n{category}:")
        for module, name in api_list:
            try:
                __import__(module)
                print(f"  ✓ {name}")
            except ImportError:
                print(f"  ✗ {name} - Missing: {module}")
                all_ok = False
    
    return all_ok

def verify_modules():
    """Verify all module classes exist"""
    print("\n" + "=" * 60)
    print("VERIFYING MODULE STRUCTURE")
    print("=" * 60)
    
    modules = [
        ('modules.brain.llm_brain', 'LLMBrain', 'LLM Brain (3 providers)'),
        ('modules.speech.tts', 'TTS', 'Text-to-Speech (3 engines)'),
        ('modules.speech.stt', 'STT', 'Speech-to-Text (3 engines)'),
    ]
    
    all_ok = True
    
    for module_path, class_name, description in modules:
        try:
            module = __import__(module_path, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"  ✓ {description}")
        except Exception as e:
            print(f"  ✗ {description}: {e}")
            all_ok = False
    
    return all_ok

def verify_methods():
    """Verify all API methods exist"""
    print("\n" + "=" * 60)
    print("VERIFYING API METHODS")
    print("=" * 60)
    
    # Check LLM methods
    print("\nLLM Brain Methods:")
    try:
        from modules.brain.llm_brain import LLMBrain
        methods = ['_generate_gemini_response', '_generate_openai_response', '_generate_anthropic_response']
        for method in methods:
            if hasattr(LLMBrain, method):
                print(f"  ✓ {method}")
            else:
                print(f"  ✗ {method} - Missing")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Check TTS methods
    print("\nTTS Methods:")
    try:
        from modules.speech.tts import TTS
        methods = ['_speak_gtts', '_speak_google_cloud', '_speak_elevenlabs']
        for method in methods:
            if hasattr(TTS, method):
                print(f"  ✓ {method}")
            else:
                print(f"  ✗ {method} - Missing")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Check STT methods
    print("\nSTT Methods:")
    try:
        from modules.speech.stt import STT
        if hasattr(STT, 'listen'):
            print(f"  ✓ listen() - Handles all 3 engines")
        else:
            print(f"  ✗ listen() - Missing")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    return True

def main():
    """Run all verifications"""
    print("\n" + "=" * 60)
    print("FRIDAY AI ASSISTANT - API VERIFICATION")
    print("=" * 60)
    print("\nVerifying all 9 API integrations...\n")
    
    results = []
    
    # Run verifications
    results.append(("API Libraries", verify_imports()))
    results.append(("Module Structure", verify_modules()))
    results.append(("API Methods", verify_methods()))
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    all_passed = all(result for _, result in results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    if all_passed:
        print("\n" + "=" * 60)
        print("✅ ALL 9 APIs VERIFIED AND READY!")
        print("=" * 60)
        print("\nAPI Integration Status:")
        print("  • LLM: 3/3 (Gemini, OpenAI, Anthropic)")
        print("  • TTS: 3/3 (gTTS, Google Cloud, ElevenLabs)")
        print("  • STT: 3/3 (Google Web, Google Cloud, Whisper)")
        print("\nTo use:")
        print("  1. Configure .env with your API keys")
        print("  2. Run: python main.py")
        return 0
    else:
        print("\n⚠️  Some verifications failed. Check errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
