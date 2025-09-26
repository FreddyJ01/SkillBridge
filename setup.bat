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
pip install -r requirements.txt

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
echo To start SkillBridge:
echo   python skillbridge.py
echo.
echo To use a different folder, edit the WATCH_FOLDER path in config.py
echo.
pause