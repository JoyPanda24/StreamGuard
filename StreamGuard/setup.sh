#!/bin/bash

# StreamGuard Setup Script for Linux/Mac
# This script sets up the project for development on Linux and macOS

set -e  # Exit on error

echo "============================================"
echo "StreamGuard Setup - Linux/Mac/Unix"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo ""
    echo "Install Python 3.10+ using:"
    echo ""
    echo "Ubuntu/Debian:"
    echo "  sudo apt update && sudo apt install -y python3 python3-pip python3-venv"
    echo ""
    echo "Fedora/RHEL:"
    echo "  sudo dnf install -y python3 python3-pip"
    echo ""
    echo "Arch Linux:"
    echo "  sudo pacman -S python python-pip"
    echo ""
    echo "macOS:"
    echo "  brew install python3"
    echo ""
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "[OK] Python found: $PYTHON_VERSION"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not available"
    exit 1
fi

echo "[OK] pip3 found"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "[OK] Virtual environment created"
else
    echo "[OK] Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
echo ""
echo "Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "[OK] Dependencies installed"
else
    echo "WARNING: requirements.txt not found in StreamGuard directory"
    echo "Please ensure you're running this script from the StreamGuard directory"
fi

# Create .env if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo ""
    echo "Creating .env file from template..."
    cp backend/.env.example backend/.env
    echo "[OK] Created backend/.env"
fi

# Make app.py executable
chmod +x backend/app.py 2>/dev/null || true
chmod +x backend/test_app.py 2>/dev/null || true

echo ""
echo "============================================"
echo "Setup Complete!"
echo "============================================"
echo ""
echo "To start the development server:"
echo "  1. Run: source .venv/bin/activate"
echo "  2. Run: cd backend"
echo "  3. Run: python app.py"
echo ""
echo "The API will be available at: http://localhost:5000"
echo ""
echo "To run tests:"
echo "  cd backend"
echo "  python test_app.py"
echo ""
echo "To deactivate virtual environment:"
echo "  deactivate"
echo ""
