#!/usr/bin/env python3
"""
Quick development runner for Event Discovery App
"""

import subprocess
import sys

def main():
    """Run the development server"""
    print("🚀 Starting Event Discovery App (Development Mode)")
    print("📍 Available at: http://localhost:8000")
    print("📖 API docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop\n")
    
    try:
        subprocess.run([
            "uv", "run", "uvicorn", 
            "app.main:app", 
            "--reload",
            "--host", "localhost",
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n👋 Development server stopped")
    except FileNotFoundError:
        print("❌ uv not found. Please install uv first:")
        print("curl -LsSf https://astral.sh/uv/install.sh | sh")
        sys.exit(1)

if __name__ == "__main__":
    main()
