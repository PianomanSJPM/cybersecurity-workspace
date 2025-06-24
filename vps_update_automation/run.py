#!/usr/bin/env python3
"""
VPS Update Automation System Runner
This script starts the VPS update automation system.
"""

import os
import sys
import logging
import argparse
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent))

from scripts.backup_encryption import BackupEncryption
from scripts.backup_monitor import BackupMonitor
from web.api.websocket import start_server

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/vps_update.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def setup_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        'logs',
        'backups',
        'config',
        'temp'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        logger.info(f"Ensured directory exists: {directory}")

def start_backup_service():
    """Start the backup service."""
    try:
        encryption = BackupEncryption()
        monitor = BackupMonitor()
        
        # Initial health check
        health_status = monitor.check_backup_health()
        logger.info(f"Initial backup health check: {health_status['overall_status']}")
        
        # Initial storage check
        storage_status = monitor.check_storage_usage()
        logger.info(f"Initial storage status: {storage_status['usage_percent']:.1f}% used")
        
        return encryption, monitor
    except Exception as e:
        logger.error(f"Error starting backup service: {e}")
        raise

async def start_web_server():
    """Start the web server and WebSocket server."""
    try:
        # Start WebSocket server
        ws_server = await start_server()
        logger.info("WebSocket server started")
        
        # Start web server (implement your web server here)
        # For example, using aiohttp:
        # app = web.Application()
        # web.run_app(app, host='localhost', port=5000)
        
        return ws_server
    except Exception as e:
        logger.error(f"Error starting web server: {e}")
        raise

async def main():
    """Main function to run the VPS update automation system."""
    parser = argparse.ArgumentParser(description='VPS Update Automation System')
    parser.add_argument('--demo', action='store_true', help='Run in demo mode')
    args = parser.parse_args()
    
    try:
        # Setup
        setup_directories()
        logger.info("Starting VPS Update Automation System")
        
        if args.demo:
            # Run demo
            from examples.demo import main as run_demo
            run_demo()
            return
        
        # Start services
        encryption, monitor = start_backup_service()
        ws_server = await start_web_server()
        
        # Keep the script running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            ws_server.close()
            await ws_server.wait_closed()
            
    except Exception as e:
        logger.error(f"Error in main: {e}")
        sys.exit(1)

if __name__ == '__main__':
    # Run the async main function
    asyncio.run(main()) 