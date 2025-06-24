#!/usr/bin/env python3
"""
Quick Demo: Visual Assets Capture
Run this script to start capturing screenshots and GIFs for your Doc-Whisperer
"""

import subprocess
import sys
from pathlib import Path

def main():
    print("🎨 Doc-Whisperer Visual Assets Capture Demo")
    print("=" * 50)
    
    # Check if server is running
    print("\n📋 Pre-flight Checklist:")
    print("✅ Make sure your web server is running: python web_app.py")
    print("✅ Ensure you have documents ingested for better visuals")
    print("✅ Close unnecessary browser tabs for clean captures")
    
    input("\n🚀 Press Enter when ready to start the capture session...")
    
    # Run the capture script
    script_path = Path("scripts/capture_assets.py")
    
    if script_path.exists():
        try:
            subprocess.run([sys.executable, str(script_path)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running capture script: {e}")
        except KeyboardInterrupt:
            print("\n👋 Capture session cancelled by user")
    else:
        print(f"❌ Capture script not found at: {script_path}")
        print("Please make sure you're running this from the project root directory")

if __name__ == "__main__":
    main() 