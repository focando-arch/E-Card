#!/usr/bin/env python3
"""
E-Card Flask Setup Script
This script helps you set up and run the E-Card game server.
"""

import os
import sys
import subprocess
import time

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🎮 E-Card Flask Setup")
    print("=" * 40)
    
    # Check if Python 3 is available
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        return
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("\n❌ Failed to install dependencies. Please check your Python/pip installation.")
        return
    
    # Create data directory
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"✅ Created data directory: {data_dir}")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the Flask server: python app.py")
    print("2. Open your browser to: http://localhost:5000")
    print("3. Sign up or sign in to start playing!")
    
    # Ask if user wants to start the server
    response = input("\n🚀 Start the Flask server now? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        print("\n🔥 Starting Flask server...")
        print("📱 Server will be available at: http://localhost:5000")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        try:
            subprocess.run([sys.executable, "app.py"], check=True)
        except KeyboardInterrupt:
            print("\n👋 Server stopped. Goodbye!")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Failed to start server: {e}")

if __name__ == "__main__":
    main() 