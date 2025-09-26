import requests
import json
import os
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI
from config import *
import time

# Load environment variables
load_dotenv()

class AIProvider:
    """Handles AI communication with both Ollama and OpenAI"""
    
    def __init__(self):
        self.provider = AI_PROVIDER.lower()
        
        if self.provider == "openai":
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                print("⚠️  No OpenAI API key found. Switching to Ollama...")
                self.provider = "ollama"
            else:
                self.openai_client = OpenAI(api_key=api_key)
    
    def is_ollama_available(self) -> bool:
        """Check if Ollama is running locally"""
        try:
            response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def ensure_ollama_model(self) -> bool:
        """Ensure the Ollama model is downloaded"""
        try:
            # Check if model exists
            response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [model['name'].split(':')[0] for model in models]
                
                if OLLAMA_MODEL not in model_names:
                    print(f"📥 Downloading {OLLAMA_MODEL} model (this may take a few minutes)...")
                    # Pull the model
                    pull_data = {"name": OLLAMA_MODEL}
                    response = requests.post(f"{OLLAMA_URL}/api/pull", json=pull_data, timeout=600)
                    if response.status_code != 200:
                        return False
                    print(f"✅ {OLLAMA_MODEL} model ready!")
                return True
        except Exception as e:
            print(f"❌ Error setting up Ollama model: {e}")
            return False
    
    def generate_response(self, job_description: str, resume_content: str) -> Optional[str]:
        """Generate tailored resume using the configured AI provider"""
        
        # Prepare the prompt
        user_message = f"""Job Description:
{job_description}

Current Resume:
{resume_content}

Please tailor this resume for the job description above."""

        for attempt in range(MAX_RETRIES):
            try:
                if self.provider == "ollama":
                    return self._generate_ollama_response(user_message)
                else:
                    return self._generate_openai_response(user_message)
            except Exception as e:
                print(f"⚠️  Attempt {attempt + 1} failed: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2)  # Wait before retry
                
        return None
    
    def _generate_ollama_response(self, user_message: str) -> Optional[str]:
        """Generate response using local Ollama"""
        if not self.is_ollama_available():
            raise Exception("Ollama is not running. Please start Ollama first.")
        
        if not self.ensure_ollama_model():
            raise Exception(f"Could not set up {OLLAMA_MODEL} model")
        
        # Prepare request
        data = {
            "model": OLLAMA_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            "stream": False
        }
        
        print("🤖 Processing with local AI...")
        response = requests.post(f"{OLLAMA_URL}/api/chat", json=data, timeout=TIMEOUT_SECONDS)
        
        if response.status_code == 200:
            result = response.json()
            return result['message']['content']
        else:
            raise Exception(f"Ollama request failed: {response.status_code}")
    
    def _generate_openai_response(self, user_message: str) -> Optional[str]:
        """Generate response using OpenAI API"""
        print("🤖 Processing with OpenAI...")
        
        response = self.openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=4000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def get_provider_info(self) -> str:
        """Get information about current AI provider"""
        if self.provider == "ollama":
            if self.is_ollama_available():
                return f"🤖 Using Ollama ({OLLAMA_MODEL}) - Free & Local"
            else:
                return "❌ Ollama not available"
        else:
            return f"🤖 Using OpenAI ({OPENAI_MODEL}) - API"