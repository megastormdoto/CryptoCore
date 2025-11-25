#!/usr/bin/env python3
"""
Debug imports to find the problem
"""

import os
import sys

print("🔧 Debugging imports...")

# Add path to import from src
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_path)

print(f"Python path: {sys.path}")
print(f"Current dir: {current_dir}")
print(f"Src path: {src_path}")

# List files in src directory
try:
    src_files = os.listdir(src_path)
    print(f"Files in src: {src_files}")
except FileNotFoundError:
    print(f"❌ src directory not found at: {src_path}")
    sys.exit(1)

try:
    # Try to import
    from csprng import generate_random_bytes

    print("✅ SUCCESS: Imported generate_random_bytes")

    # Test the function
    data = generate_random_bytes(16)
    print(f"✅ Generated {len(data)} random bytes")

except ImportError as e:
    print(f"❌ IMPORT FAILED: {e}")

    # Try alternative
    try:
        import csprng

        print(f"✅ Alternative import worked. Functions: {[f for f in dir(csprng) if not f.startswith('_')]}")
    except ImportError as e2:
        print(f"❌ Alternative import also failed: {e2}")

except Exception as e:
    print(f"❌ OTHER ERROR: {e}")