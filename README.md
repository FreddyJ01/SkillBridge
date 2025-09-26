# 🌉 SkillBridge - Automated Resume Tailoring

SkillBridge is a "set it and forget it" automation tool that watches a folder and automatically tailors your resume for any job description. Drop in your JD and resume, get a perfectly tailored resume back - no manual work required!

## ✨ Features

- 📁 **Folder Watching**: Automatically detects when you drop JD.docx and CurrentResume.docx files
- 🤖 **AI-Powered**: Uses local AI (Ollama) for free, or OpenAI for premium results  
- 🎨 **100% Format Preservation**: Advanced XML processing maintains **identical** formatting, fonts, spacing, and style
- 🔍 **Deep Document Analysis**: Scans every formatting detail including horizontal lines, borders, and complex layouts
- 🔄 **Cross-Platform**: Works on Windows, Mac, and Linux
- 🚀 **Zero Manual Work**: Completely automated once set up
- 💰 **Free Option**: No API costs with local Ollama AI
- 🛡️ **Robust Fallback**: Multiple formatting preservation methods ensure reliability

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

### **"Python is not recognized"**
- **Windows:** Reinstall Python and check "Add Python to PATH"
- **Mac:** Use `python3` instead of `python`

### **"Ollama not running"**
- **Solution 1:** Run `ollama serve` in a separate terminal window
- **Solution 2:** Switch to OpenAI in [`config.py`](config.py)
- **Solution 3:** Restart the setup script

### **"TypeError: __init__() got an unexpected keyword argument 'proxies'"**
This is a common compatibility issue with OpenAI library versions.

**Quick Fix:**
```bash
pip3 install "httpx<0.25" "urllib3<2.0" openai==1.35.0 --upgrade
```

**What this does:** Installs compatible versions of the networking libraries that work together properly.

### **"Could not extract text"**
- Ensure files are `.docx` format (not `.doc` or `.pdf`)
- Try opening and re-saving the files in Microsoft Word
- Check that files actually contain text

### **"AI failed to respond"**
- **For Ollama:** Make sure `ollama serve` is running
- **For OpenAI:** Check your internet connection and API key
- Try again - AI sometimes has temporary hiccups

### **Files not being detected**
- Make sure files are named exactly `JD.docx` and `CurrentResume.docx`
- Check that SkillBridge is still running (look for the console window)
- Try dropping files one at a time with a few seconds between

### **Need more help?**
- Check the console window for detailed error messages
- Make sure both files are in the correct folder
- Restart SkillBridge if it seems stuck

## 🎯 Tips for Best Results

### Writing Better Job Descriptions
1. **Copy the complete job posting** - don't just use bullet points
2. **Include company information** if available
3. **Keep industry context** - mention the company type/industry

### Preparing Your Resume
1. **Use a complete resume** - include all sections (experience, skills, education)
2. **Any Word formatting supported** - horizontal lines, borders, tables, custom fonts all preserved
3. **Include quantified achievements** - numbers help AI understand impact
4. **Complex layouts welcome** - the XML system handles advanced formatting

### Optimizing the AI Prompt
Edit the `SYSTEM_PROMPT` in [`config.py`](config.py) to:
- Focus on your industry (e.g., "You are a tech resume expert...")
- Emphasize specific skills (e.g., "Always highlight leadership experience...")
- Match your career level (e.g., "Focus on senior-level responsibilities...")

### Advanced Formatting Preservation
SkillBridge uses **three layers** of formatting preservation:

1. **🚀 XML Reconstruction (100% identical)**: Direct manipulation of Word's XML structure
2. **📋 Structure Preservation (95% similar)**: Smart content mapping with format matching  
3. **📄 Fallback Formatting (80% similar)**: Basic professional styling as last resort

**The system automatically tries each method** until one succeeds, ensuring you always get a properly formatted resume.

## 🤝 Contributing

Want to improve SkillBridge? Pull requests welcome!

- Add new AI providers
- Improve document formatting
- Enhance error handling
- Add more configuration options

## 📄 License

This project is licensed under the terms in the LICENSE file.SkillBridge
SkillBridge is a Python-powered automation tool that takes in a job description and your resume, then intelligently tailors your resume to highlight the most relevant skills, experience, and achievements. The goal isn’t just to pass ATS, but to help you present yourself as the right fit, for both you and the organization.
