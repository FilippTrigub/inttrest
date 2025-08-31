#!/usr/bin/env python3
"""
Setup and run script for the Event Discovery App
"""

import os
import sys
import subprocess
from pathlib import Path


def check_uv_installed():
    """Check if uv is installed"""
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
        print("✅ uv is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ uv is not installed")
        print("Please install uv first:")
        print("curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False


def setup_environment():
    """Set up the Python environment and install dependencies"""
    print("🔧 Setting up Python environment...")
    
    try:
        # Create virtual environment and install dependencies
        subprocess.run(["uv", "sync"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def create_env_file():
    """Create .env file from .env.example if it doesn't exist"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print("📄 Creating .env file from template...")
        with env_example.open() as src, env_file.open("w") as dst:
            dst.write(src.read())
        print("✅ .env file created")
        print("⚠️  Please edit .env file to add your API keys")
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("⚠️  No .env.example file found")


def run_application():
    """Run the FastAPI application"""
    print("🚀 Starting the Event Discovery App...")
    print("📍 Application will be available at: http://localhost:8000")
    print("🗺️  Map interface: http://localhost:8000")
    print("📖 API docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the application\n")
    
    try:
        subprocess.run([
            "uv", "run", "uvicorn", 
            "app.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start application: {e}")


def main():
    """Main setup and run function"""
    print("🎯 Event Discovery App Setup")
    print("=" * 40)
    
    # Check if uv is installed
    if not check_uv_installed():
        sys.exit(1)
    
    # Set up environment
    if not setup_environment():
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Ask user if they want to run the app
    response = input("\n🎯 Do you want to start the application now? (y/n): ").lower()
    if response in ['y', 'yes']:
        run_application()
    else:
        print("\n📝 To start the application later, run:")
        print("   uv run uvicorn app.main:app --reload")
        print("\n📖 Or use the development script:")
        print("   python run_dev.py")


if __name__ == "__main__":
    main()
