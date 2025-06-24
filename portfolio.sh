#!/bin/bash
# Cybersecurity Portfolio Quick Access Script

echo "🛡️  Cybersecurity Portfolio Manager"
echo "=================================================="
echo "📁 Quick access to your portfolio automation"
echo "=================================================="

# Check if we're in the right directory
if [ ! -d "Portfolio" ]; then
    echo "❌ Portfolio directory not found!"
    echo "Please run this script from the Cybersecurity folder."
    exit 1
fi

# Change to portfolio directory and run the automation
cd Portfolio

if [ ! -f "add_document.py" ]; then
    echo "❌ Portfolio automation script not found!"
    echo "Please ensure your portfolio is properly set up."
    exit 1
fi

echo "🚀 Starting portfolio automation..."
echo "=================================================="

# Run the Python script
python3 add_document.py 