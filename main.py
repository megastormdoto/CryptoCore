#!/usr/bin/env python3
"""
Main entry point for CryptoCore - run from project root.
"""
import sys
import os

# Add src directory to path
src_dir = os.path.join(os.path.dirname(__file__), 'src')
if os.path.exists(src_dir):
    sys.path.insert(0, src_dir)

try:
    from cryptocore import main
    main()
except ImportError as e:
    print(f"Error: Could not import cryptocore. Make sure you're in the project root directory.")
    print(f"Current directory: {os.getcwd()}")
    print(f"Error details: {e}")
    sys.exit(1)