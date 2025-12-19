#!/usr/bin/env python3
"""Integration test for derive command."""
import sys
import os
import subprocess
import tempfile


def test_derive_basic():
    """Test basic derive command."""
    print("Testing derive command...")

    # Test 1: Basic password derivation
    print("\n1. Basic password derivation:")
    cmd = [
        sys.executable, 'main.py', 'derive',
        '--password', 'testpassword',
        '--salt', '73616c74',  # hex for 'salt'
        '--iterations', '1',
        '--length', '20'
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd='..')
        print(f"Command: {' '.join(cmd)}")
        print(f"Output: {result.stdout.strip()}")
        print(f"Return code: {result.returncode}")

        # Parse output
        if result.stdout:
            parts = result.stdout.strip().split()
            if len(parts) >= 1:
                key_hex = parts[0]
                print(f"Derived key: {key_hex}")
                # Should be 40 hex chars for 20 bytes
                assert len(key_hex) == 40, f"Expected 40 hex chars, got {len(key_hex)}"
                print("✓ Basic derivation works")
    except Exception as e:
        print(f"Error: {e}")


def test_derive_with_files():
    """Test derive with file output."""
    print("\n2. Derive with file output:")

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("mysecretpassword\n")
        password_file = f.name

    with tempfile.NamedTemporaryFile(delete=False, suffix='.bin') as f:
        key_file = f.name

    try:
        cmd = [
            sys.executable, 'main.py', 'derive',
            '--password-file', password_file,
            '--salt', 'a1b2c3d4',
            '--iterations', '1000',
            '--length', '32',
            '--output', key_file
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, cwd='..')
        print(f"Command: {' '.join(cmd[2:])}")  # Skip python and main.py
        print(f"Return code: {result.returncode}")

        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                key_data = f.read()
                print(f"Key file size: {len(key_data)} bytes")
                assert len(key_data) == 32, f"Expected 32 bytes, got {len(key_data)}"
                print(f"Key (hex): {key_data.hex()}")
                print("✓ File output works")

    finally:
        # Cleanup
        if os.path.exists(password_file):
            os.remove(password_file)
        if os.path.exists(key_file):
            os.remove(key_file)


def test_key_hierarchy():
    """Test key hierarchy derivation."""
    print("\n3. Key hierarchy derivation:")

    master_key = '0' * 64  # 32 bytes in hex
    cmd = [
        sys.executable, 'main.py', 'derive',
        '--master-key', master_key,
        '--context', 'encryption',
        '--length', '32'
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd='..')
        print(f"Command: {' '.join(cmd[2:])}")
        print(f"Output: {result.stdout.strip()}")
        print(f"Return code: {result.returncode}")

        if result.stdout:
            parts = result.stdout.strip().split()
            if len(parts) >= 1:
                key_hex = parts[0]
                print(f"Derived key: {key_hex}")
                assert len(key_hex) == 64, f"Expected 64 hex chars, got {len(key_hex)}"
                print("✓ Key hierarchy works")
    except Exception as e:
        print(f"Error: {e}")


def test_all():
    """Run all tests."""
    print("=" * 60)
    print("SPRINT 7 INTEGRATION TESTS")
    print("=" * 60)

    tests = [
        test_derive_basic,
        test_derive_with_files,
        test_key_hierarchy
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ Test failed: {e}")
        except Exception as e:
            print(f"✗ Test error: {e}")

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("=" * 60)

    return passed == total


if __name__ == "__main__":
    # Change to project root if needed
    if os.path.basename(os.getcwd()) == 'cryptocore':
        os.chdir('..')

    success = test_all()
    sys.exit(0 if success else 1)