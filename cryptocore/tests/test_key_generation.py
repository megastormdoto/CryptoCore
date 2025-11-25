#!/usr/bin/env python3
"""
Test key generation functionality
"""

import os
import sys
import subprocess
import tempfile

# Add path to import from src
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.insert(0, os.path.join(current_dir, '..', 'src'))


def run_command(cmd, cwd='..'):
    """Run command and return success status"""
    try:
        result = subprocess.run(cmd, shell=False, capture_output=True, text=True, cwd=cwd)
        if result.returncode == 0:
            return True, result.stdout, result.stderr
        else:
            return False, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def test_encryption_without_key():
    """Test encryption without providing key"""
    print("🔐 Testing encryption without key...")

    # Create test file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("Test content for automatic key generation")
        test_file = f.name

    encrypted_file = test_file + '.enc'
    decrypted_file = test_file + '_decrypted.txt'

    try:
        # Encrypt without key
        cmd = [
            sys.executable, 'cryptocore/main.py',
            '--algorithm', 'aes',
            '--mode', 'cbc',
            '--encrypt',
            '--input', test_file,
            '--output', encrypted_file
        ]

        print(f"Running encryption without key...")
        success, stdout, stderr = run_command(cmd, cwd='..')

        if not success:
            print(f"❌ Encryption failed: {stderr}")
            return False

        # Check if key was generated
        if 'Generated random key:' in stdout:
            print("✅ Key was automatically generated")

            # Extract generated key
            for line in stdout.split('\n'):
                if 'Generated random key:' in line:
                    generated_key = line.split(': ')[1].strip()
                    print(f"✅ Generated key: {generated_key}")

                    # Test decryption with generated key
                    decrypt_cmd = [
                        sys.executable, 'cryptocore/main.py',
                        '--algorithm', 'aes',
                        '--mode', 'cbc',
                        '--decrypt',
                        '--key', generated_key,
                        '--input', encrypted_file,
                        '--output', decrypted_file
                    ]

                    success, stdout, stderr = run_command(decrypt_cmd, cwd='..')
                    if success:
                        # Verify files match
                        with open(test_file, 'r') as f1, open(decrypted_file, 'r') as f2:
                            original = f1.read()
                            decrypted = f2.read()

                            if original == decrypted:
                                print("✅ SUCCESS: Original and decrypted files match!")
                                return True
                            else:
                                print("❌ FAILED: Files don't match!")
                                return False
                    else:
                        print(f"❌ Decryption failed: {stderr}")
                        return False
            return True
        else:
            print("❌ No key generation message found")
            print(f"Output: {stdout}")
            return False

    finally:
        # Cleanup
        for file_path in [test_file, encrypted_file, decrypted_file]:
            if os.path.exists(file_path):
                os.unlink(file_path)


def test_decryption_requires_key():
    """Test that decryption requires key"""
    print("🔒 Testing decryption requires key...")

    # Create dummy encrypted file
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.enc') as f:
        f.write(b'fake encrypted data')
        enc_file = f.name

    try:
        # Try to decrypt without key
        cmd = [
            sys.executable, 'cryptocore/main.py',
            '--algorithm', 'aes',
            '--mode', 'cbc',
            '--decrypt',
            '--input', enc_file,
            '--output', enc_file + '.dec'
        ]

        success, stdout, stderr = run_command(cmd, cwd='..')

        # This should FAIL (return code != 0)
        if not success:
            print("✅ Correctly failed without key")
            return True
        else:
            print("❌ Should have failed without key")
            return False

    finally:
        # Cleanup
        for ext in ['', '.dec']:
            file_path = enc_file + ext
            if os.path.exists(file_path):
                os.unlink(file_path)


def main():
    """Run all tests"""
    print("🚀 Key Generation Tests")
    print("=" * 50)

    tests = [
        test_encryption_without_key,
        test_decryption_requires_key,
    ]

    results = {}

    for test in tests:
        try:
            results[test.__name__] = test()
            print()
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            results[test.__name__] = False

    # Summary
    print("=" * 50)
    print("📊 RESULTS:")
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name}: {status}")

    passed = sum(results.values())
    total = len(results)

    print(f"\nTotal: {passed}/{total}")

    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())