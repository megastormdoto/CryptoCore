# tests/test_sprint6_full.py
# !/usr/bin/env python3
"""
Complete Sprint 6 GCM/AEAD Test Suite
"""
import os
import sys
import tempfile
import subprocess
import unittest

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestSprint6GCM(unittest.TestCase):
    """Comprehensive Sprint 6 GCM/AEAD tests"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        print("\n" + "=" * 70)
        print("Sprint 6: GCM/AEAD Test Suite")
        print("=" * 70)

        # Find cryptocore.py
        cls.script_path = cls._find_cryptocore()
        if not cls.script_path:
            raise FileNotFoundError("cryptocore.py not found")

        print(f"Using script: {cls.script_path}")

    @staticmethod
    def _find_cryptocore():
        """Find cryptocore.py script"""
        paths = [
            'cryptocore.py',
            '../cryptocore.py',
            os.path.join(os.path.dirname(__file__), '..', 'cryptocore.py'),
            os.path.join(os.path.dirname(__file__), '..', 'src', 'cryptocore.py'),
        ]

        for path in paths:
            if os.path.exists(path):
                return os.path.abspath(path)

        return None

    def test_01_cli_gcm_help(self):
        """Test that GCM mode is available in CLI help"""
        print("\n[Test 1] Checking CLI help for GCM...")

        result = subprocess.run(
            [sys.executable, self.script_path, 'encrypt', '--help'],
            capture_output=True,
            text=True
        )

        self.assertIn('--mode', result.stdout)
        self.assertIn('gcm', result.stdout.lower())
        self.assertIn('--aad', result.stdout)
        print("✅ GCM mode is available in CLI")

    def test_02_gcm_encrypt_decrypt(self):
        """Test basic GCM encryption and decryption"""
        print("\n[Test 2] Basic GCM encryption/decryption...")

        # Create test file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.txt') as f:
            f.write(b"This is a test message for GCM.\nSecond line.\n")
            input_file = f.name

        encrypted_file = tempfile.mktemp(suffix='.bin')
        decrypted_file = tempfile.mktemp(suffix='.txt')

        key = "00112233445566778899aabbccddeeff"
        aad = "aabbccddeeff001122334455"

        try:
            # Encrypt
            result = subprocess.run([
                sys.executable, self.script_path,
                'encrypt',
                '--key', key,
                '--input', input_file,
                '--output', encrypted_file,
                '--mode', 'gcm',
                '--aad', aad
            ], capture_output=True, text=True)

            self.assertEqual(result.returncode, 0,
                             f"Encryption failed: {result.stderr}")

            # Check output file exists and has correct size
            self.assertTrue(os.path.exists(encrypted_file))
            encrypted_size = os.path.getsize(encrypted_file)
            input_size = os.path.getsize(input_file)
            self.assertGreaterEqual(encrypted_size, input_size + 28)  # nonce + tag

            # Decrypt
            result = subprocess.run([
                sys.executable, self.script_path,
                'encrypt',
                '--decrypt',
                '--key', key,
                '--input', encrypted_file,
                '--output', decrypted_file,
                '--mode', 'gcm',
                '--aad', aad
            ], capture_output=True, text=True)

            self.assertEqual(result.returncode, 0,
                             f"Decryption failed: {result.stderr}")

            # Compare files
            with open(input_file, 'rb') as f:
                original = f.read()
            with open(decrypted_file, 'rb') as f:
                decrypted = f.read()

            self.assertEqual(original, decrypted, "Decrypted content doesn't match original")
            print("✅ Basic GCM encryption/decryption works")

        finally:
            # Cleanup
            for f in [input_file, encrypted_file, decrypted_file]:
                if os.path.exists(f):
                    os.remove(f)

    def test_03_gcm_wrong_aad_fails(self):
        """Test that wrong AAD causes authentication failure"""
        print("\n[Test 3] Testing wrong AAD detection...")

        # Create test file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.txt') as f:
            f.write(b"Message for AAD test")
            input_file = f.name

        encrypted_file = tempfile.mktemp(suffix='.bin')
        wrong_output = tempfile.mktemp(suffix='.txt')

        key = "00112233445566778899aabbccddeeff"
        correct_aad = "correctaad1234567890abcdef"
        wrong_aad = "wrongaad1234567890abcdef"

        try:
            # Encrypt with correct AAD
            result = subprocess.run([
                sys.executable, self.script_path,
                'encrypt',
                '--key', key,
                '--input', input_file,
                '--output', encrypted_file,
                '--mode', 'gcm',
                '--aad', correct_aad
            ], capture_output=True, text=True)

            self.assertEqual(result.returncode, 0)

            # Try to decrypt with wrong AAD
            result = subprocess.run([
                sys.executable, self.script_path,
                'encrypt',
                '--decrypt',
                '--key', key,
                '--input', encrypted_file,
                '--output', wrong_output,
                '--mode', 'gcm',
                '--aad', wrong_aad
            ], capture_output=True, text=True)

            # Should fail
            self.assertNotEqual(result.returncode, 0,
                                "Should have failed with wrong AAD")

            # Output file should not exist
            self.assertFalse(os.path.exists(wrong_output),
                             "Output file should not exist after auth failure")

            print("✅ Wrong AAD correctly causes authentication failure")

        finally:
            # Cleanup
            for f in [input_file, encrypted_file, wrong_output]:
                if os.path.exists(f):
                    os.remove(f)

    def test_04_gcm_tamper_detection(self):
        """Test that tampered ciphertext is detected"""
        print("\n[Test 4] Testing tamper detection...")

        # Create test file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.txt') as f:
            f.write(b"Tamper detection test message")
            input_file = f.name

        encrypted_file = tempfile.mktemp(suffix='.bin')
        tampered_file = tempfile.mktemp(suffix='.bin')
        wrong_output = tempfile.mktemp(suffix='.txt')

        key = "00112233445566778899aabbccddeeff"
        aad = "testaad123456"

        try:
            # Encrypt
            result = subprocess.run([
                sys.executable, self.script_path,
                'encrypt',
                '--key', key,
                '--input', input_file,
                '--output', encrypted_file,
                '--mode', 'gcm',
                '--aad', aad
            ], capture_output=True, text=True)

            self.assertEqual(result.returncode, 0)

            # Tamper with the ciphertext
            with open(encrypted_file, 'rb') as f:
                data = bytearray(f.read())

            # Flip some bits in the middle of ciphertext (after nonce)
            if len(data) > 20:
                data[20] ^= 0xFF

            with open(tampered_file, 'wb') as f:
                f.write(data)

            # Try to decrypt tampered file
            result = subprocess.run([
                sys.executable, self.script_path,
                'encrypt',
                '--decrypt',
                '--key', key,
                '--input', tampered_file,
                '--output', wrong_output,
                '--mode', 'gcm',
                '--aad', aad
            ], capture_output=True, text=True)

            # Should fail
            self.assertNotEqual(result.returncode, 0,
                                "Should have detected tampering")

            # Output file should not exist
            self.assertFalse(os.path.exists(wrong_output),
                             "Output file should not exist after tamper detection")

            print("✅ Tamper detection works correctly")

        finally:
            # Cleanup
            for f in [input_file, encrypted_file, tampered_file, wrong_output]:
                if os.path.exists(f):
                    os.remove(f)

    def test_05_gcm_empty_aad(self):
        """Test GCM with empty AAD"""
        print("\n[Test 5] Testing GCM with empty AAD...")

        # Create test file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.txt') as f:
            f.write(b"Test with empty AAD")
            input_file = f.name

        encrypted_file = tempfile.mktemp(suffix='.bin')
        decrypted_file = tempfile.mktemp(suffix='.txt')

        key = "00112233445566778899aabbccddeeff"

        try:
            # Encrypt with empty AAD (not providing --aad at all)
            result = subprocess.run([
                sys.executable, self.script_path,
                'encrypt',
                '--key', key,
                '--input', input_file,
                '--output', encrypted_file,
                '--mode', 'gcm'
            ], capture_output=True, text=True)

            self.assertEqual(result.returncode, 0)

            # Decrypt with empty AAD
            result = subprocess.run([
                sys.executable, self.script_path,
                'encrypt',
                '--decrypt',
                '--key', key,
                '--input', encrypted_file,
                '--output', decrypted_file,
                '--mode', 'gcm'
            ], capture_output=True, text=True)

            self.assertEqual(result.returncode, 0)

            # Compare files
            with open(input_file, 'rb') as f:
                original = f.read()
            with open(decrypted_file, 'rb') as f:
                decrypted = f.read()

            self.assertEqual(original, decrypted)
            print("✅ GCM works with empty AAD")

        finally:
            # Cleanup
            for f in [input_file, encrypted_file, decrypted_file]:
                if os.path.exists(f):
                    os.remove(f)


def run_tests():
    """Run all tests with nice formatting"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSprint6GCM)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print("\n🎉 ALL SPRINT 6 TESTS PASSED!")
        return True
    else:
        print("\n❌ Some tests failed")
        return False


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)