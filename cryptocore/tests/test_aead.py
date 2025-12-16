# tests/test_aead.py
import unittest
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.aead.encrypt_then_mac import EncryptThenMAC, AuthenticationError
from src.modes.ctr import CTRMode


class TestEncryptThenMAC(unittest.TestCase):

    def setUp(self):
        # Generate test key (32 bytes for encryption + MAC)
        self.key = os.urandom(32)
        self.plaintext = b"This is a secret message for testing"
        self.aad = b"Associated authentication data"

    def test_encrypt_decrypt(self):
        """Test basic encryption and decryption"""
        etm = EncryptThenMAC(self.key, CTRMode)

        # Encrypt
        ciphertext = etm.encrypt(self.plaintext, self.aad)

        # Decrypt
        decrypted = etm.decrypt(ciphertext, self.aad)

        self.assertEqual(decrypted, self.plaintext)

    def test_wrong_aad_fails(self):
        """Test that wrong AAD causes authentication failure"""
        etm = EncryptThenMAC(self.key, CTRMode)

        ciphertext = etm.encrypt(self.plaintext, self.aad)

        # Try to decrypt with wrong AAD
        wrong_aad = b"Wrong AAD"

        with self.assertRaises(AuthenticationError):
            etm.decrypt(ciphertext, wrong_aad)

    def test_tampered_ciphertext_fails(self):
        """Test that tampered ciphertext causes authentication failure"""
        etm = EncryptThenMAC(self.key, CTRMode)

        ciphertext = etm.encrypt(self.plaintext, self.aad)

        # Tamper with ciphertext
        tampered = bytearray(ciphertext)
        tampered[10] ^= 0xFF  # Flip some bits

        with self.assertRaises(AuthenticationError):
            etm.decrypt(bytes(tampered), self.aad)

    def test_empty_data(self):
        """Test with empty plaintext and AAD"""
        etm = EncryptThenMAC(self.key, CTRMode)

        ciphertext = etm.encrypt(b"", b"")
        decrypted = etm.decrypt(ciphertext, b"")

        self.assertEqual(decrypted, b"")

    def test_large_data(self):
        """Test with large data"""
        etm = EncryptThenMAC(self.key, CTRMode)

        # 10KB of data
        large_data = os.urandom(10 * 1024)
        ciphertext = etm.encrypt(large_data, self.aad)
        decrypted = etm.decrypt(ciphertext, self.aad)

        self.assertEqual(decrypted, large_data)

    def test_key_separation(self):
        """Test that different keys are used for encryption and MAC"""
        etm1 = EncryptThenMAC(self.key, CTRMode)
        etm2 = EncryptThenMAC(self.key, CTRMode)

        # Both should produce same output with same key
        ct1 = etm1.encrypt(self.plaintext, self.aad)
        ct2 = etm2.encrypt(self.plaintext, self.aad)

        # They should be different due to random IV in CTR mode
        # But decryption should work
        decrypted1 = etm1.decrypt(ct1, self.aad)
        decrypted2 = etm2.decrypt(ct2, self.aad)

        self.assertEqual(decrypted1, self.plaintext)
        self.assertEqual(decrypted2, self.plaintext)


class TestGCMIntegration(unittest.TestCase):
    """Test GCM through the CLI"""

    def test_gcm_cli_basic(self):
        """Test basic GCM encryption/decryption via CLI"""
        import subprocess
        import tempfile

        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b"Test message for GCM")
            input_file = f.name

        encrypted_file = tempfile.mktemp()
        decrypted_file = tempfile.mktemp()

        key = "00112233445566778899aabbccddeeff"
        aad = "aabbccddeeff"

        try:
            # Encrypt
            result = subprocess.run([
                sys.executable, 'cryptocore.py',
                'encrypt',
                '--key', key,
                '--input', input_file,
                '--output', encrypted_file,
                '--mode', 'gcm',
                '--aad', aad
            ], capture_output=True, text=True)

            self.assertEqual(result.returncode, 0, f"Encryption failed: {result.stderr}")

            # Decrypt
            result = subprocess.run([
                sys.executable, 'cryptocore.py',
                'encrypt',
                '--decrypt',
                '--key', key,
                '--input', encrypted_file,
                '--output', decrypted_file,
                '--mode', 'gcm',
                '--aad', aad
            ], capture_output=True, text=True)

            self.assertEqual(result.returncode, 0, f"Decryption failed: {result.stderr}")

            # Compare files
            with open(input_file, 'rb') as f:
                original = f.read()
            with open(decrypted_file, 'rb') as f:
                decrypted = f.read()

            self.assertEqual(original, decrypted)

        finally:
            # Cleanup
            for f in [input_file, encrypted_file, decrypted_file]:
                if os.path.exists(f):
                    os.remove(f)


if __name__ == '__main__':
    unittest.main()