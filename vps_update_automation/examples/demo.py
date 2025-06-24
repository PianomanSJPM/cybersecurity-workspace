#!/usr/bin/env python3
"""
VPS Update Automation Demo Script
This script demonstrates the main features of the VPS Update Automation system.
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime
import shutil

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from scripts.backup_encryption import BackupEncryption
from scripts.backup_monitor import BackupMonitor

def create_demo_files():
    """Create some demo files for backup testing."""
    demo_dir = Path('demo_files')
    demo_dir.mkdir(exist_ok=True)
    
    # Create a text file
    with open(demo_dir / 'example.txt', 'w') as f:
        f.write('This is a demo file for backup testing.\n')
        f.write(f'Created at: {datetime.now()}\n')
    
    # Create a binary file
    with open(demo_dir / 'example.bin', 'wb') as f:
        f.write(os.urandom(1024))  # 1KB of random data
    
    print("Created demo files in 'demo_files' directory")
    return demo_dir

def demonstrate_backup_encryption():
    """Demonstrate backup encryption features."""
    print("\n=== Backup Encryption Demo ===")
    
    # Initialize encryption
    encryption = BackupEncryption('config/config.example.json')
    
    # Create a demo file
    demo_file = Path('demo.txt')
    with open(demo_file, 'w') as f:
        f.write('This is a test file for encryption demo.\n')
    
    # Encrypt the file
    print(f"\nEncrypting file: {demo_file}")
    encrypted_file = encryption.encrypt_file(demo_file)
    print(f"Encrypted file created: {encrypted_file}")
    
    # Decrypt the file
    print(f"\nDecrypting file: {encrypted_file}")
    decrypted_file = encryption.decrypt_file(encrypted_file)
    print(f"Decrypted file created: {decrypted_file}")
    
    # Clean up
    for f in [demo_file, Path(encrypted_file), Path(decrypted_file)]:
        if f.exists():
            f.unlink()
    
    # Demonstrate directory encryption
    demo_dir = create_demo_files()
    print(f"\nEncrypting directory: {demo_dir}")
    encrypted_dir = encryption.encrypt_directory(demo_dir)
    print(f"Encrypted directory archive created: {encrypted_dir}")
    
    # Decrypt the directory
    print(f"\nDecrypting directory: {encrypted_dir}")
    decrypted_dir = encryption.decrypt_directory(encrypted_dir)
    print(f"Decrypted directory created: {decrypted_dir}")
    
    # Clean up
    for file in demo_dir.glob('*'):
        if file.exists():
            file.unlink()
    if demo_dir.exists():
        demo_dir.rmdir()
    if Path(encrypted_dir).exists():
        Path(encrypted_dir).unlink()
    if Path(decrypted_dir).exists():
        shutil.rmtree(Path(decrypted_dir))

def demonstrate_monitoring():
    """Demonstrate monitoring features."""
    print("\n=== Backup Monitoring Demo ===")
    
    # Initialize monitor
    monitor = BackupMonitor('config/config.example.json')
    
    # Check storage usage
    print("\nChecking storage usage...")
    storage_status = monitor.check_storage_usage()
    print(f"Storage Status:")
    print(f"- Total Space: {storage_status['total_space'] / (1024**3):.2f} GB")
    print(f"- Used Space: {storage_status['used_space'] / (1024**3):.2f} GB")
    print(f"- Free Space: {storage_status['free_space'] / (1024**3):.2f} GB")
    print(f"- Usage: {storage_status['usage_percent']:.1f}%")
    
    # Check backup health
    print("\nChecking backup health...")
    health_status = monitor.check_backup_health()
    print(f"Backup Health Status:")
    print(f"- Overall Status: {health_status['overall_status']}")
    print(f"- Total Backups: {health_status['total_backups']}")
    print(f"- Healthy Backups: {health_status['healthy_backups']}")
    print(f"- Corrupted Backups: {health_status['corrupted_backups']}")
    print(f"- Missing Backups: {health_status['missing_backups']}")
    
    # Send a test alert
    print("\nSending test alert...")
    monitor.send_alert(
        'Test Alert',
        'This is a test alert from the VPS Update Automation system.'
    )

def demonstrate_web_interface():
    """Demonstrate the web interface features."""
    print("\n=== Web Interface Demo ===")
    print("To use the web interface:")
    print("1. Start the web server:")
    print("   python web_server.py")
    print("2. Open your browser and navigate to:")
    print("   http://localhost:5000")
    print("\nThe web interface provides:")
    print("- Real-time system status")
    print("- Backup management")
    print("- Monitoring dashboard")
    print("- Configuration settings")

def main():
    """Run the demonstration."""
    print("VPS Update Automation System Demo")
    print("================================")
    
    try:
        # Demonstrate backup encryption
        demonstrate_backup_encryption()
        
        # Demonstrate monitoring
        demonstrate_monitoring()
        
        # Show web interface information
        demonstrate_web_interface()
        
        print("\nDemo completed successfully!")
        
    except Exception as e:
        print(f"\nError during demo: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 