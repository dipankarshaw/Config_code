#!/bin/bash

# Configuration Streamlit App - Quick Start

echo "🚀 Starting Network Configuration Streamlit App..."
echo ""
echo "Dependencies check..."

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

echo ""
echo "✨ Launching Streamlit app..."
echo "📱 The app will open in your default browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run streamlit app
streamlit run src/streamlit_app.py --logger.level=warning
