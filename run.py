#!/usr/bin/env python3
"""
Run CryptoCore from project root
"""
import sys
import os

# Get project root
project_root = os.path.dirname(os.path.abspath(__file__))

# Add project root to Python path
sys.path.insert(0, project_root)

# Now we can import from src
try:
    # First check if we can see the modules
    print(f"Project root: {project_root}")
    print(f"Python path: {sys.path}")

    # Try to import
    import src

    # Now run the main application
    from src.cryptocore import main

    main()

except ImportError as e:
    print(f"Import error: {e}")
    print(f"\nChecking directory structure...")

    # Check src directory
    src_dir = os.path.join(project_root, 'src')
    if os.path.exists(src_dir):
        print(f"src directory exists: {src_dir}")
        print("Contents:")
        for item in os.listdir(src_dir):
            print(f"  {item}")
    else:
        print(f"src directory NOT found: {src_dir}")

    sys.exit(1)