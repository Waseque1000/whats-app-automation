#!/bin/bash
# Convenient runner script for WhatsApp Student Messenger

# Move to script directory
cd "$(dirname "$0")"

# Activate virtual environment if present
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run the desktop application
python3 main.py
