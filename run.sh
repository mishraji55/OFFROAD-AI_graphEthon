#!/bin/bash

# Linux/Mac startup script for Offroad AI Web App

echo ""
echo "╔════════════════════════════════════════╗"
echo "║   Offroad AI - Terrain Segmentation     ║"
echo "║          Starting Flask App...          ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed"
        echo "Please install Python from https://www.python.org/"
        exit 1
    fi
else
    python=$(command -v python3)
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "ERROR: requirements.txt not found"
    exit 1
fi

# Check if model file exists
if [ ! -f "terrain_classifier.pth" ]; then
    echo "WARNING: terrain_classifier.pth not found in project root"
    echo "The app will fail when trying to load the model"
    echo ""
fi

# Install/upgrade dependencies
echo "Installing dependencies..."
$python -m pip install -r requirements.txt --quiet

# Run the Flask app
echo ""
echo "✓ Starting Flask server..."
echo ""
echo "🌐 Open your browser and go to: http://localhost:10000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

$python app.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Flask app failed to start"
    exit 1
fi
