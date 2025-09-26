#!/bin/bash

# SkillBridge Setup Script for macOS/Linux
echo "🌉 Setting up SkillBridge..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 from https://python.org"
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama not found. Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
else
    echo "✅ Ollama is already installed"
fi

# Start Ollama service
echo "🚀 Starting Ollama..."
ollama serve &

# Give Ollama time to start
sleep 3

# Pull the default model
echo "📥 Downloading AI model (this may take a few minutes)..."
ollama pull llama3.1

# Create the watch folder
echo "📁 Creating watch folder..."
mkdir -p ./TailorResumeInbox

echo ""
echo "🎉 SkillBridge setup complete!"
echo ""
echo "To start SkillBridge:"
echo "  python3 skillbridge.py"
echo ""
echo "To use a different folder, edit the WATCH_FOLDER path in config.py"
echo ""