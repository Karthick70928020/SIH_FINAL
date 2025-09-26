#!/usr/bin/env python3
"""
Smart Network Monitor Backend Startup Script

This script provides an easy way to start the backend with proper error handling
and environment setup.
"""

import os
import sys
import subprocess
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import flask_socketio
        import sklearn
        import pandas
        import numpy
        import cryptography
        logger.info("All required Python packages are available")
        return True
    except ImportError as e:
        logger.error(f"Missing required package: {e}")
        logger.info("Please run: pip install -r requirements.txt")
        return False

def check_system_dependencies():
    """Check system-level dependencies"""
    try:
        # Check if tshark/dumpcap is available for packet capture
        result = subprocess.run(['which', 'tshark'], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            logger.info("tshark found - packet capture available")
        else:
            logger.warning("tshark not found - will use demo mode")
            logger.info("To install: sudo apt-get install tshark (Ubuntu) or brew install wireshark (macOS)")
    except Exception as e:
        logger.warning(f"Could not check tshark: {e}")

def main():
    """Main startup function"""
    print("=" * 60)
    print("Smart Network Monitor Backend")
    print("=" * 60)
    
    # Check Python dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check system dependencies
    check_system_dependencies()
    
    # Set environment variables
    os.environ['FLASK_ENV'] = 'development'
    
    print("\nStarting backend server...")
    print("Frontend should connect to: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        # Import and run the main application
        from app import socketio, app
        socketio.run(
            app,
            host='127.0.0.1',
            port=5000,
            debug=True,
            allow_unsafe_werkzeug=True
        )
    except KeyboardInterrupt:
        print("\nShutting down backend server...")
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()