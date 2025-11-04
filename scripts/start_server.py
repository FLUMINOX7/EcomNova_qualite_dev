#!/usr/bin/env python3
"""
Script to start the EcomNova API server
Checks Python version compatibility before starting
"""
import sys
import os

# Check Python version
if sys.version_info >= (3, 13):
    print("❌ Error: Python 3.13+ is not compatible with FastAPI 0.95.2/Pydantic 1.10.7")
    print("   Please use Python 3.11 or 3.12")
    print("\n💡 Solution:")
    print("   1. Install Python 3.11: pyenv install 3.11.10")
    print("   2. Set local version: pyenv local 3.11.10")
    print("   3. Recreate venv: rm -rf .venv && python -m venv .venv")
    print("   4. Reinstall deps: source .venv/bin/activate && pip install -r requirements.txt")
    sys.exit(1)

if sys.version_info < (3, 9):
    print("❌ Error: Python 3.9+ is required")
    sys.exit(1)

print(f"✅ Python version OK: {sys.version}")

# Set environment variables if .env exists
env_file = os.path.join(os.path.dirname(__file__), "backend", ".env")
if os.path.exists(env_file):
    print(f"📁 Loading environment from {env_file}")
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip().strip('"').strip("'")

# Start the server
print("\n🚀 Starting EcomNova API...")
print("   Access API at: http://localhost:8000")
print("   Access docs at: http://localhost:8000/docs")
print("   Press Ctrl+C to stop\n")

import uvicorn
uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
