#!/bin/bash

# FreshCart AI Customer Support - Quick Start Script

echo "🛒 FreshCart AI Customer Support Automation"
echo "==========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version detected"
echo ""

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo "✓ Dependencies installed"
echo ""

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  Please edit .env and add your OpenAI API key"
    echo "   Or enter it directly in the app when it starts"
    echo ""
fi

# Start the app
echo "🚀 Starting FreshCart AI Support Assistant..."
echo ""
echo "The app will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the application"
echo ""

streamlit run app.py
