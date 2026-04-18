"""
Interactive script to configure API keys in .env file
"""

import os
import sys

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def get_gemini_key():
    """Guide user to get Gemini API key"""
    print_header("STEP 1: Get Free Gemini API Key")
    
    print("\n📝 Instructions:")
    print("1. Open your browser and go to:")
    print("   https://makersuite.google.com/app/apikey")
    print("\n2. Sign in with your Google account")
    print("\n3. Click 'Create API Key'")
    print("\n4. Copy the generated API key")
    
    print("\n" + "-" * 60)
    api_key = input("\nPaste your Gemini API key here (or press Enter to skip): ").strip()
    
    if api_key and api_key != "your_gemini_api_key_here":
        return api_key
    return None

def get_optional_keys():
    """Ask if user wants to configure optional API keys"""
    print_header("STEP 2: Optional API Keys")
    
    print("\nDo you want to configure optional premium services?")
    print("(You can skip this and use the free tier)")
    
    response = input("\nConfigure optional keys? (y/n): ").lower().strip()
    
    if response != 'y':
        return {}
    
    optional_keys = {}
    
    # OpenAI
    print("\n" + "-" * 60)
    print("OpenAI API Key (for GPT models or Whisper API)")
    print("Get from: https://platform.openai.com/api-keys")
    key = input("Paste OpenAI API key (or press Enter to skip): ").strip()
    if key:
        optional_keys['OPENAI_API_KEY'] = key
    
    # Anthropic
    print("\n" + "-" * 60)
    print("Anthropic API Key (for Claude models)")
    print("Get from: https://console.anthropic.com/")
    key = input("Paste Anthropic API key (or press Enter to skip): ").strip()
    if key:
        optional_keys['ANTHROPIC_API_KEY'] = key
    
    # ElevenLabs
    print("\n" + "-" * 60)
    print("ElevenLabs API Key (for premium text-to-speech)")
    print("Get from: https://elevenlabs.io/")
    key = input("Paste ElevenLabs API key (or press Enter to skip): ").strip()
    if key:
        optional_keys['ELEVENLABS_API_KEY'] = key
    
    return optional_keys

def update_env_file(gemini_key, optional_keys):
    """Update .env file with API keys"""
    print_header("STEP 3: Updating .env File")
    
    if not os.path.exists('.env'):
        print("✗ .env file not found!")
        print("  Run: copy .env.example .env")
        return False
    
    # Read current .env
    with open('.env', 'r') as f:
        lines = f.readlines()
    
    # Update lines
    updated_lines = []
    for line in lines:
        if gemini_key and line.startswith('GOOGLE_API_KEY='):
            updated_lines.append(f'GOOGLE_API_KEY={gemini_key}\n')
            print(f"✓ Updated GOOGLE_API_KEY")
        elif 'OPENAI_API_KEY' in optional_keys and line.startswith('# OPENAI_API_KEY='):
            updated_lines.append(f'OPENAI_API_KEY={optional_keys["OPENAI_API_KEY"]}\n')
            print(f"✓ Added OPENAI_API_KEY")
        elif 'ANTHROPIC_API_KEY' in optional_keys and line.startswith('# ANTHROPIC_API_KEY='):
            updated_lines.append(f'ANTHROPIC_API_KEY={optional_keys["ANTHROPIC_API_KEY"]}\n')
            print(f"✓ Added ANTHROPIC_API_KEY")
        elif 'ELEVENLABS_API_KEY' in optional_keys and line.startswith('# ELEVENLABS_API_KEY='):
            updated_lines.append(f'ELEVENLABS_API_KEY={optional_keys["ELEVENLABS_API_KEY"]}\n')
            print(f"✓ Added ELEVENLABS_API_KEY")
        else:
            updated_lines.append(line)
    
    # Write updated .env
    with open('.env', 'w') as f:
        f.writelines(updated_lines)
    
    return True

def main():
    """Main configuration flow"""
    print_header("FRIDAY AI ASSISTANT - API KEY CONFIGURATION")
    
    print("\nThis script will help you configure API keys for Friday AI.")
    print("You'll need at least a free Gemini API key to get started.")
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("\n⚠️  .env file not found!")
        print("Creating .env from template...")
        try:
            if os.path.exists('.env.example'):
                import shutil
                shutil.copy('.env.example', '.env')
                print("✓ Created .env file")
            else:
                print("✗ .env.example not found!")
                return 1
        except Exception as e:
            print(f"✗ Error creating .env: {e}")
            return 1
    
    # Get Gemini key (required)
    gemini_key = get_gemini_key()
    
    if not gemini_key:
        print("\n⚠️  No Gemini API key provided.")
        print("You can manually edit .env file later.")
        print("\nTo get a free key:")
        print("  1. Visit: https://makersuite.google.com/app/apikey")
        print("  2. Create an API key")
        print("  3. Add it to .env file")
        return 1
    
    # Get optional keys
    optional_keys = get_optional_keys()
    
    # Update .env file
    if update_env_file(gemini_key, optional_keys):
        print_header("✅ CONFIGURATION COMPLETE!")
        
        print("\nYour .env file has been configured with:")
        print(f"  ✓ Gemini API Key (required)")
        if optional_keys:
            for key in optional_keys:
                print(f"  ✓ {key}")
        
        print("\n" + "=" * 60)
        print("NEXT STEPS")
        print("=" * 60)
        
        print("\n1. Test your configuration:")
        print("   python test_all.py")
        
        print("\n2. Verify all APIs:")
        print("   python verify_apis.py")
        
        print("\n3. Run Friday:")
        print("   python main.py")
        
        print("\n4. Say 'Friday' to activate, then speak your command!")
        
        return 0
    else:
        print("\n✗ Failed to update .env file")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nConfiguration cancelled.")
        sys.exit(1)
