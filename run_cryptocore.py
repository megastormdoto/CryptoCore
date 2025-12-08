#!/usr/bin/env python3
"""Wrapper script to run cryptocore"""

import sys
import os

# Add the cryptocore/src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'cryptocore/src'))

# Import and run main
try:
    from cryptocore import main

    sys.exit(main())
except ImportError as e:
    print(f"Import error: {e}")
    print("Trying alternative import...")

    # Alternative import
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "cryptocore",
        os.path.join(os.path.dirname(__file__), 'cryptocore/src/cryptocore.py')
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.exit(module.main())