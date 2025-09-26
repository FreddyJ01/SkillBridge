#!/usr/bin/env python3
"""
Quick provider switcher for SkillBridge
"""

import os
import sys

def switch_provider(provider):
    """Switch AI provider in config.py"""
    
    config_file = "config.py"
    
    if not os.path.exists(config_file):
        print("❌ config.py not found")
        return False
    
    # Read current config
    with open(config_file, 'r') as f:
        lines = f.readlines()
    
    # Update the AI_PROVIDER line
    updated_lines = []
    for line in lines:
        if line.startswith('AI_PROVIDER = '):
            updated_lines.append(f'AI_PROVIDER = "{provider}"\n')
            print(f"✅ Changed AI_PROVIDER to: {provider}")
        else:
            updated_lines.append(line)
    
    # Write back
    with open(config_file, 'w') as f:
        f.writelines(updated_lines)
    
    return True

def show_providers():
    """Show available providers"""
    print("🤖 Available AI Providers:")
    print("=" * 40)
    print()
    print("1. gemini - Google Gemini AI")
    print("   ✨ Benefits: Latest Google AI, competitive pricing, fast")
    print("   ⚠️  Requires: Gemini API key")
    print()
    print("2. openai - OpenAI API")
    print("   ✨ Benefits: Fully automated, fast, proven quality")
    print("   ⚠️  Requires: OpenAI API key")
    print()
    print("3. ollama - Local AI")
    print("   ✨ Benefits: Free, private, offline")
    print("   ⚠️  Requires: Ollama installed and running")

def main():
    """Main function"""
    
    if len(sys.argv) < 2:
        print("🔧 SkillBridge Provider Switcher")
        print("=" * 40)
        print()
        show_providers()
        print()
        print("Usage:")
        print("  python switch_provider.py gemini")
        print("  python switch_provider.py openai") 
        print("  python switch_provider.py ollama")
        return
    
    provider = sys.argv[1].lower()
    
    valid_providers = ["gemini", "openai", "ollama"]
    
    if provider not in valid_providers:
        print(f"❌ Invalid provider: {provider}")
        print(f"Valid options: {', '.join(valid_providers)}")
        return
    
    if switch_provider(provider):
        print()
        print("🎯 Provider switched successfully!")
        print()
        
        if provider == "gemini":
            print("🤖 Google Gemini Mode Active")
            print("   � Make sure GEMINI_API_KEY is set in .env")
            print("   🚀 Run: python skillbridge.py")
        elif provider == "openai":
            print("🤖 OpenAI API Mode Active") 
            print("   🔑 Make sure OPENAI_API_KEY is set in .env")
            print("   🚀 Run: python skillbridge.py")
        elif provider == "ollama":
            print("🏠 Local Ollama Mode Active")
            print("   🔄 Make sure Ollama is running")
            print("   🚀 Run: python skillbridge.py")

if __name__ == "__main__":
    main()