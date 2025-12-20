#!/usr/bin/env python3
"""
Simple test for CSPRNG
"""

import os
import sys


def main():
    print("🧪 Simple CSPRNG Test")

    # Add path to import from src
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(current_dir, '..', 'src')
    sys.path.insert(0, src_path)

    print(f"Looking for csprng in: {src_path}")

    try:
        # Check if file exists
        csprng_path = os.path.join(src_path, 'csprng.py')
        if os.path.exists(csprng_path):
            print(f"✅ csprng.py exists at: {csprng_path}")
        else:
            print(f"❌ csprng.py NOT found at: {csprng_path}")
            return False

        # Try to import
        from csprng import generate_key, bytes_to_hex

        print("✅ Import successful!")

        # Test basic functionality
        key = generate_key()
        print(f"✅ Key generated: {bytes_to_hex(key)}")

        return True

    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = main()

    if success:
        print("🎉 Test passed!")
        sys.exit(0)
    else:
        print("💥 Test failed!")
        sys.exit(1)