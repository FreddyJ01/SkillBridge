@echo off
REM SkillBridge Setup Script for Windows
echo 🌉 Setting up SkillBridge...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3 is required but not installed.
    echo Please install Python 3 from https://python.org
    pause
    exit /b 1
)

REM Install Python dependencies
echo 📦 Installing Python dependencies...
echo    - Installing core packages...
pip install -r requirements.txt

echo    - Verifying advanced XML processing...
python -c "import lxml; print('✅ Advanced XML processing ready')" >nul 2>&1 || (
    echo ⚠️  Installing additional XML dependencies...
    pip install lxml>=4.6.0
)

REM Check if Ollama is installed
ollama --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Ollama not found. Please install Ollama manually:
    echo 1. Go to https://ollama.ai
    echo 2. Download and install Ollama for Windows
    echo 3. Run this setup script again
    pause
    exit /b 1
) else (
    echo ✅ Ollama is already installed
)

REM Start Ollama service
echo 🚀 Starting Ollama...
start /B ollama serve

REM Give Ollama time to start
timeout /t 5 /nobreak >nul

REM Pull the default model
echo 📥 Downloading AI model (this may take a few minutes)...
ollama pull llama3.1

REM Create the watch folder
echo 📁 Creating watch folder...
if not exist "TailorResumeInbox" mkdir TailorResumeInbox

echo.
echo 🎉 SkillBridge setup complete!
echo.
echo ✅ Features installed:
echo    📁 Folder watching
echo    🤖 AI integration (Ollama + OpenAI)  
echo    🎨 100%% formatting preservation (XML processing)
echo    🔄 Cross-platform compatibility
echo.
echo 🚀 To start SkillBridge:
echo    python skillbridge.py
echo.
echo ⚙️  To customize settings:
echo    Edit config.py (AI provider, watch folder, etc.)
echo.
echo 📖 For help:
echo    Check README.md for complete instructions
echo.
pause