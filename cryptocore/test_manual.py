#!/usr/bin/env python3
"""
Manual test for key generation
"""

import os
import sys

# Add src to path
sys.path.insert(0, 'src')

from csprng import generate_key, bytes_to_hex
from cryptocore import CryptoCore


def test_direct():
    """Test CSPRNG directly"""
    print("🔐 Testing CSPRNG directly...")
    key = generate_key()
    print(f"✅ Generated key: {bytes_to_hex(key)}")
    return True


def test_integration():
    """Test integration with CryptoCore"""
    print("\n🔧 Testing CryptoCore integration...")

    # Create test file
    with open('test_input.txt', 'w') as f:
        f.write("Hello CryptoCore! Testing automatic key generation.")

    try:
        # Simulate command line arguments for encryption without key
        print("Testing encryption without key...")

        # We'll test this by calling the internal methods directly
        from cli_parser import CLIParser
        from file_io import FileIO

        # Test that CLI parser accepts missing key for encryption
        test_args = [
            '--algorithm', 'aes',
            '--mode', 'cbc',
            '--encrypt',
            '--input', 'test_input.txt',
            '--output', 'test_encrypted.bin'
        ]

        # Save original argv
        original_argv = sys.argv
        sys.argv = ['test'] + test_args

        try:
            parser = CLIParser()
            args = parser.parse_args()
            print(f"✅ CLI parsing: encrypt={args.encrypt}, key={args.key}")

            if args.encrypt and args.key is None:
                print("✅ CLI correctly allows missing key for encryption")
                return True
            else:
                print("❌ CLI should allow missing key for encryption")
                return False

        except SystemExit as e:
            print(f"❌ CLI parsing failed: {e}")
            return False
        finally:
            sys.argv = original_argv

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False
    finally:
        # Cleanup
        for file in ['test_input.txt', 'test_encrypted.bin']:
            if os.path.exists(file):
                os.unlink(file)


def main():
    print("🚀 Manual Key Generation Tests")
    print("=" * 50)

    test1 = test_direct()
    test2 = test_integration()

    print("\n" + "=" * 50)
    print("📊 RESULTS:")
    print(f"  Direct CSPRNG test: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"  Integration test: {'✅ PASS' if test2 else '❌ FAIL'}")

    if test1 and test2:
        print("🎉 All manual tests passed!")
        return 0
    else:
        print("⚠️ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())