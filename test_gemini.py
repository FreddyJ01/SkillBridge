#!/usr/bin/env python3
"""
Test Gemini integration for SkillBridge
"""

import os
from ai_provider import AIProvider

def test_gemini_integration():
    """Test the Gemini API integration"""
    print("🧪 Testing Gemini Integration")
    print("=" * 40)
    
    # Check if API key is set
    gemini_key = os.getenv('GEMINI_API_KEY')
    if not gemini_key:
        print("❌ GEMINI_API_KEY not found in environment")
        print()
        print("📋 Setup Instructions:")
        print("1. Get your Gemini API key from: https://aistudio.google.com/app/apikey")
        print("2. Create/edit .env file:")
        print("   echo 'GEMINI_API_KEY=your_key_here' >> .env")
        print("3. Run this test again")
        return False
    
    print("✅ Gemini API key found")
    
    # Create AI provider
    ai = AIProvider()
    print(f"Provider: {ai.get_provider_info()}")
    print()
    
    # Sample test data
    sample_jd = """Software Engineer - Python/AI
We are looking for a talented Software Engineer to join our AI team. 
Requirements:
- 3+ years Python experience
- Machine learning knowledge
- Experience with APIs and databases
"""
    
    sample_resume = """John Smith
Software Developer

EXPERIENCE:
- Developed web applications using Python and Flask
- Worked with databases and API integrations  
- Built data processing systems

SKILLS:
- Python, JavaScript, SQL
- Problem solving and debugging
"""
    
    print("🚀 Testing Gemini response...")
    try:
        response = ai.generate_response(sample_jd, sample_resume)
        
        if response:
            print("✅ SUCCESS! Gemini integration working!")
            print()
            print("📝 Sample Response Preview:")
            print("-" * 50)
            print(response[:300] + "..." if len(response) > 300 else response)
            print("-" * 50)
            
            # Save test result
            with open("gemini_test_result.txt", "w", encoding="utf-8") as f:
                f.write("GEMINI INTEGRATION TEST RESULT\n")
                f.write("=" * 50 + "\n\n")
                f.write("JOB DESCRIPTION:\n")
                f.write(sample_jd + "\n\n")
                f.write("ORIGINAL RESUME:\n")
                f.write(sample_resume + "\n\n")
                f.write("GEMINI TAILORED RESUME:\n")
                f.write(response)
            
            print(f"💾 Full result saved to: gemini_test_result.txt")
            return True
            
        else:
            print("❌ No response received from Gemini")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Gemini: {e}")
        return False

def show_gemini_setup():
    """Show Gemini setup information"""
    print("🤖 Google Gemini Setup Guide")
    print("=" * 40)
    print()
    print("📋 REQUIREMENTS:")
    print("   ✅ Google account")
    print("   ✅ Gemini API access (free tier available)")
    print()
    print("🔑 GET API KEY:")
    print("   1. Go to: https://aistudio.google.com/app/apikey")
    print("   2. Sign in with Google account")
    print("   3. Click 'Create API Key'")
    print("   4. Copy the generated key")
    print()
    print("⚙️  SETUP:")
    print("   1. Create/edit .env file in SkillBridge folder:")
    print("      echo 'GEMINI_API_KEY=your_key_here' >> .env")
    print("   2. Set provider in config.py:")
    print("      AI_PROVIDER = 'gemini'")
    print("   3. Run SkillBridge!")
    print()
    print("💰 PRICING:")
    print("   • Free tier: 15 requests/minute, 1M tokens/day")
    print("   • Pay-as-you-go: Very competitive rates")
    print("   • Perfect for resume tailoring use case")

if __name__ == "__main__":
    show_gemini_setup()
    print()
    test_gemini_integration()