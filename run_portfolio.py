#!/usr/bin/env python3
"""
Cybersecurity Portfolio Runner
Quick access to your portfolio automation tools
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Get the current script directory
    script_dir = Path(__file__).parent
    portfolio_dir = script_dir / "Portfolio"
    
    # Check if portfolio directory exists
    if not portfolio_dir.exists():
        print("❌ Portfolio directory not found!")
        print(f"Expected location: {portfolio_dir}")
        print("Please ensure your portfolio is in the correct location.")
        return
    
    # Check if add_document.py exists
    add_document_script = portfolio_dir / "add_document.py"
    if not add_document_script.exists():
        print("❌ Portfolio automation script not found!")
        print(f"Expected location: {add_document_script}")
        print("Please ensure your portfolio is properly set up.")
        return
    
    # Change to portfolio directory and run the automation
    print("🛡️  Cybersecurity Portfolio Manager")
    print("=" * 50)
    print(f"📁 Portfolio location: {portfolio_dir}")
    print("🚀 Starting portfolio automation...")
    print("=" * 50)
    
    try:
        # Change to portfolio directory
        os.chdir(portfolio_dir)
        
        # Run the add_document.py script
        subprocess.run([sys.executable, "add_document.py"])
        
    except KeyboardInterrupt:
        print("\n\n👋 Portfolio manager closed.")
    except Exception as e:
        print(f"\n❌ Error running portfolio manager: {e}")
        print("Please check your portfolio setup.")

if __name__ == "__main__":
    main() 