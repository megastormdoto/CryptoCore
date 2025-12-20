#!/usr/bin/env python3
"""
Quick CLI test for GCM - Windows compatible version
"""
import os
import sys
import tempfile
import subprocess
import unittest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def get_main_path():
    """Get path to main.py or cryptocore.py"""
    # Check current directory and parent
    possible_paths = [
        'cryptocore.py',
        '../cryptocore.py',
        'src/cryptocore.py',
        os.path.join(os.path.dirname(__file__), '..', 'cryptocore.py'),
        os.path.join(os.path.dirname(__file__), '..', 'src', 'cryptocore.py'),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            print(f"Found: {path}")
            return os.path.abspath(path)

    print("Not found in paths:", possible_paths)
    return None


def run_command(cmd):
    """Run command with proper encoding for Windows"""
    try:
        # For Windows, set UTF-8 encoding
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'  # Ignore encoding errors
        )
        return result
    except Exception as e:
        print(f"Command execution error: {e}")
        return None


class TestGCMCLI(unittest.TestCase):
    """Test GCM via CLI"""

    @classmethod
    def setUpClass(cls):
        """Find cryptocore script"""
        cls.script_path = get_main_path()
        if not cls.script_path:
            raise FileNotFoundError("Could not find cryptocore.py")

    def test_cli_gcm(self):
        """Test GCM via CLI - Windows compatible"""
        print("=" * 60)
        print("Testing GCM CLI...")

        # Create test file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.txt') as f:
            f.write(b"This is a secret message for GCM testing.\nLine 2.\n")
            input_file = f.name

        encrypted_file = tempfile.mktemp(suffix='.bin')
        decrypted_file = tempfile.mktemp(suffix='.txt')

        # FIXED: AAD must be hex string
        key = "00112233445566778899aabbccddeeff"
        aad = "aabbccddeeff00112233445566778899"  # Already hex, good!

        try:
            print(f"Input: {input_file}")
            print(f"Key: {key}")
            print(f"AAD (hex): {aad}")

            # Step 1: Encrypt
            print("\n1. Encrypting...")
            cmd = [
                sys.executable, self.script_path,
                'encrypt',
                '--key', key,
                '--input', input_file,
                '--output', encrypted_file,
                '--mode', 'gcm',
                '--aad', aad
            ]

            print(f"Running: {' '.join(cmd[:5])} ...")  # Show partial command

            result = run_command(cmd)
            self.assertIsNotNone(result, "Command execution failed")

            print(f"Return code: {result.returncode}")
            if result.stdout:
                print(f"stdout: {result.stdout[:200]}")
            if result.stderr:
                print(f"stderr: {result.stderr[:200]}")

            self.assertEqual(result.returncode, 0,
                             f"Encryption failed with code {result.returncode}")

            print(f"SUCCESS: Encryption successful")
            print(f"Encrypted file: {encrypted_file}")

            # Check file exists and has reasonable size
            self.assertTrue(os.path.exists(encrypted_file))
            size = os.path.getsize(encrypted_file)
            print(f"Encrypted size: {size} bytes")

            plaintext_size = os.path.getsize(input_file)
            expected_size = 12 + plaintext_size + 16  # nonce + plaintext + tag
            print(f"Expected size: {expected_size} bytes")

            self.assertGreaterEqual(size, expected_size,
                                    "Encrypted file size too small")

            # Step 2: Decrypt with correct AAD
            print("\n2. Decrypting with correct AAD...")
            cmd = [
                sys.executable, self.script_path,
                'encrypt',
                '--decrypt',
                '--key', key,
                '--input', encrypted_file,
                '--output', decrypted_file,
                '--mode', 'gcm',
                '--aad', aad
            ]

            result = run_command(cmd)
            self.assertIsNotNone(result, "Command execution failed")

            print(f"Return code: {result.returncode}")
            if result.stdout:
                print(f"stdout: {result.stdout[:200]}")
            if result.stderr:
                print(f"stderr: {result.stderr[:200]}")

            self.assertEqual(result.returncode, 0,
                             f"Decryption failed with code {result.returncode}")

            print(f"SUCCESS: Decryption successful")

            # Compare files
            with open(input_file, 'rb') as f:
                original = f.read()
            with open(decrypted_file, 'rb') as f:
                decrypted = f.read()

            self.assertEqual(original, decrypted,
                             "Decrypted content doesn't match original")
            print(f"Original/Decrypted length: {len(original)} bytes")

            # Step 3: Try to decrypt with wrong AAD
            print("\n3. Trying to decrypt with wrong AAD (should fail)...")
            wrong_aad_file = tempfile.mktemp(suffix='.txt')
            wrong_aad = "77616e6721616164313233343536"  # Hex for "wrong!aad123456"

            cmd = [
                sys.executable, self.script_path,
                'encrypt',
                '--decrypt',
                '--key', key,
                '--input', encrypted_file,
                '--output', wrong_aad_file,
                '--mode', 'gcm',
                '--aad', wrong_aad  # Wrong AAD
            ]

            result = run_command(cmd)
            self.assertIsNotNone(result, "Command execution failed")

            # Should fail (non-zero return code)
            self.assertNotEqual(result.returncode, 0,
                                "Should have failed with wrong AAD")

            # Check that output file was NOT created
            self.assertFalse(os.path.exists(wrong_aad_file),
                             "Output file was created despite auth failure")

            print(f"SUCCESS: Correctly failed with wrong AAD (return code: {result.returncode})")

            print("\n" + "=" * 60)
            print("ALL CLI TESTS PASSED!")

        finally:
            # Cleanup
            files_to_clean = [input_file, encrypted_file, decrypted_file]
            for f in files_to_clean:
                if f and os.path.exists(f):
                    try:
                        os.remove(f)
                    except:
                        pass


if __name__ == "__main__":
    # Set console encoding for Windows
    if sys.platform == "win32":
        try:
            # Try to set UTF-8 encoding
            import io

            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='ignore')
        except:
            pass

    unittest.main()