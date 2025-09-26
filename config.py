# Configuration for SkillBridge
# You can modify these settings to customize the behavior

# FOLDER SETTINGS
# Default watch folder (change this path if you want to watch a different location)
WATCH_FOLDER = "./TailorResumeInbox"

# OUTPUT SETTINGS
OUTPUT_FILENAME = "TailoredResume.docx"
ERROR_FILENAME = "Error.docx"

# AI PROVIDER SETTINGS
# Options: "ollama" (free, local) or "openai" (requires API key)
AI_PROVIDER = "ollama"

# OLLAMA SETTINGS (for local AI)
OLLAMA_MODEL = "llama3.1"  # Options: llama3.1, mistral, phi3
OLLAMA_URL = "http://localhost:11434"

# OPENAI SETTINGS (optional, for premium experience)
# Create a .env file and add: OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL = "gpt-4"

# RESUME TAILORING PROMPT
# This is the core instruction for the AI - modify this to improve results
SYSTEM_PROMPT = """You are an expert resume tailoring specialist. Your job is to take a job description and a resume, then rewrite the resume to be perfectly tailored for that specific job while maintaining 100% truthfulness.

Your goals:
1. Match keywords from the job description naturally
2. Emphasize relevant experience and skills
3. Reorder and rewrite bullet points to highlight job-relevant achievements
4. Use action verbs and quantified results where possible
5. Ensure ATS compatibility
6. Make the resume compelling to human recruiters

Rules:
- Never fabricate experience, skills, or achievements
- Keep the same overall structure and formatting intent
- Return ONLY the tailored resume text, no explanations
- Maintain professional tone throughout
- Focus on relevance and impact

Input format: You'll receive the job description first, then the current resume.
Output: Return only the tailored resume content."""

# PROCESSING SETTINGS
MAX_RETRIES = 3
TIMEOUT_SECONDS = 300  # 5 minutes max per AI request