# 🌉 SkillBridge - Automated Resume Tailoring

SkillBridge is a "set it and forget it" automation tool that watches a folder and automatically tailors your resume for any job description. Drop in your JD and resume, get a perfectly tailored resume back - no manual work required!

## ✨ Features

- 📁 **Folder Watching**: Automatically detects when you drop JD.docx and CurrentResume.docx files
- 🤖 **AI-Powered**: Uses local AI (Ollama) for free, or OpenAI for premium results  
- 📝 **Format Preservation**: Maintains your original resume's formatting, fonts, and style
- 🔄 **Cross-Platform**: Works on Windows, Mac, and Linux
- 🚀 **Zero Manual Work**: Completely automated once set up
- 💰 **Free Option**: No API costs with local Ollama AI

## 🚀 Quick Start

### Option 1: Automatic Setup (Recommended)

**Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
python3 skillbridge.py
```

**Windows:**
```cmd
setup.bat
python skillbridge.py
```

### Option 2: Manual Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Ollama (for free AI):**
   - Download from [ollama.ai](https://ollama.ai)
   - Run: `ollama serve`
   - Download model: `ollama pull llama3.1`

3. **Start SkillBridge:**
   ```bash
   python skillbridge.py
   ```

## 📋 How to Use

1. **Start SkillBridge** - Run the main script
2. **Save your job description** as `JD.docx`
3. **Save your resume** as `CurrentResume.docx`  
4. **Drop both files** into the `TailorResumeInbox` folder
5. **Wait 30-60 seconds** for `TailoredResume.docx` to appear!

## ⚙️ Configuration

Edit `config.py` to customize:

- **Watch Folder**: Change `WATCH_FOLDER` to any path you want
- **AI Provider**: Switch between `"ollama"` (free) or `"openai"` (premium)
- **AI Model**: Choose different Ollama models or OpenAI models
- **Custom Prompt**: Modify `SYSTEM_PROMPT` to improve AI results

## 🤖 AI Options

### Free Option: Ollama (Local AI)
- ✅ Completely free forever
- ✅ Works offline after setup  
- ✅ Private (nothing sent to internet)
- ⚠️ Requires decent computer (8GB+ RAM recommended)
- ⚠️ Slower than cloud AI (30-60 seconds)

### Premium Option: OpenAI API
- ✅ Fastest results (5-10 seconds)
- ✅ Highest quality output
- ✅ Works on any computer
- ❌ Costs ~$0.01-0.03 per resume
- ❌ Requires API key

To use OpenAI:
1. Get API key from [platform.openai.com](https://platform.openai.com)
2. Create `.env` file: `OPENAI_API_KEY=your_key_here`
3. Set `AI_PROVIDER = "openai"` in `config.py`

## 📁 Folder Structure

```
SkillBridge/
├── skillbridge.py          # Main application
├── config.py              # Settings & prompts
├── ai_provider.py         # AI integration
├── document_processor.py  # Word document handling
├── requirements.txt       # Dependencies
├── setup.sh/.bat         # Auto setup scripts
└── TailorResumeInbox/    # Watch folder
    ├── JD.docx           # Drop job description here
    ├── CurrentResume.docx # Drop your resume here
    └── TailoredResume.docx # Output appears here!
```

## 🛠️ Troubleshooting

**"Ollama not running":**
- Run `ollama serve` in terminal
- Or switch to OpenAI in config.py

**"Could not extract text":**
- Ensure files are valid .docx Word documents
- Try opening and re-saving the files

**"AI failed to respond":**
- Check internet connection (for OpenAI)
- Ensure Ollama is running (for local AI)
- Try again - AI sometimes has hiccups

**Need help?** Check the console output for detailed error messages.

## 🎯 Tips for Best Results

1. **Clear Job Descriptions**: Copy the full JD text, not just bullet points
2. **Complete Resumes**: Include all sections (experience, skills, education)
3. **Good Prompts**: Customize `SYSTEM_PROMPT` in config.py for your industry
4. **Consistent Formatting**: Use standard Word formatting in your base resume

## 🤝 Contributing

Want to improve SkillBridge? Pull requests welcome!

- Add new AI providers
- Improve document formatting
- Enhance error handling
- Add more configuration options

## 📄 License

This project is licensed under the terms in the LICENSE file.SkillBridge
SkillBridge is a Python-powered automation tool that takes in a job description and your resume, then intelligently tailors your resume to highlight the most relevant skills, experience, and achievements. The goal isn’t just to pass ATS, but to help you present yourself as the right fit, for both you and the organization.
