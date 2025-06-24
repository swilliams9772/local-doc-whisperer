#!/bin/bash

# Local Doc-Whisperer Quick Start Script
# This script sets up the environment and demonstrates basic usage

echo "🧠 Local Doc-Whisperer Quick Start"
echo "=================================="

# Check if Python 3.8+ is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python $python_version detected"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚙️  Setting up environment file..."
    cp env.example .env
    echo ""
    echo "🔑 IMPORTANT: Please edit .env and add your Anthropic API key!"
    echo "   You can get an API key from: https://docs.anthropic.com/en/docs/get-started"
    echo ""
    echo "   Open .env in your text editor and replace 'your_anthropic_api_key_here'"
    echo "   with your actual API key."
    echo ""
    read -p "   Press Enter when you've added your API key..."
else
    echo "✅ Environment file already exists"
fi

# Check if API key is set
if grep -q "your_anthropic_api_key_here" .env; then
    echo "⚠️  Warning: API key still needs to be set in .env file"
    echo "   The demo will not work until you add a valid Anthropic API key."
else
    echo "✅ API key appears to be configured"
fi

echo ""
echo "🚀 Setup complete! Here's how to use Doc-Whisperer:"
echo ""
echo "1. Process the sample document:"
echo "   python main.py ingest docs_in/sample_document.md"
echo ""
echo "2. Ask questions about it:"
echo "   python main.py ask \"What are the main benefits of AI in education?\""
echo ""
echo "3. Start interactive mode:"
echo "   python main.py interactive"
echo ""
echo "4. List all processed documents:"
echo "   python main.py list-docs"
echo ""
echo "📖 For more information, see README.md"

# Optionally run a test
echo ""
read -p "Would you like to test with the sample document now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧪 Testing with sample document..."
    python main.py ingest docs_in/sample_document.md
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Sample document processed successfully!"
        echo ""
        echo "Try asking: python main.py ask \"What are the challenges of AI in education?\""
    else
        echo "❌ Error processing sample document. Please check your API key in .env"
    fi
fi

echo ""
echo "Happy hacking! 🎉" 