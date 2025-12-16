# tests/test_aead_etm.py
import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.modes.aead import AEADEncryptThenMAC, AuthenticationError


class TestAEADEncryptThenMAC(unittest.TestCase):
    """Test Encrypt-then-MAC AEAD implementation"""

    def test_key_derivation(self):
        """Test that keys are properly derived"""
        master_key = os.urandom(16)
        aead = AEADEncryptThenMAC(master_key)

        # Keys should be different
        self.assertNotEqual(aead.k_enc, aead.k_mac)
        # Key lengths should be correct
        self.assertEqual(len(aead.k_enc), 16)  # AES-128 key
        self.assertEqual(len(aead.k_mac), 32)  # HMAC-SHA256 key

    def test_basic_encryption_decryption(self):
        """Test basic encrypt/decrypt"""
        master_key = os.urandom(16)
        plaintext = b"Hello AEAD World!"
        aad = b"Authentication Data"

        aead = AEADEncryptThenMAC(master_key)

        # Encrypt
        ciphertext = aead.encrypt(plaintext, aad)

        # Should contain nonce(12) + ciphertext + tag(16)
        self.assertGreaterEqual(len(ciphertext), 12 + 16)

        # Decrypt
        decrypted = aead.decrypt(ciphertext, aad)
        self.assertEqual(decrypted, plaintext)

    def test_authentication_failure_tampered_ciphertext(self):
        """Test tampering detection"""
        master_key = os.urandom(16)
        plaintext = b"Secret message"
        aad = b"Auth data"

        aead = AEADEncryptThenMAC(master_key)
        ciphertext = aead.encrypt(plaintext, aad)

        # Tamper with ciphertext
        tampered = bytearray(ciphertext)
        if len(tampered) > 28:
            tampered[20] ^= 0x01

        with self.assertRaises(AuthenticationError):
            aead.decrypt(bytes(tampered), aad)

    def test_authentication_failure_wrong_aad(self):
        """Test wrong AAD detection"""
        master_key = os.urandom(16)
        plaintext = b"Secret message"
        aad_correct = b"correct aad"
        aad_wrong = b"wrong aad"

        aead = AEADEncryptThenMAC(master_key)
        ciphertext = aead.encrypt(plaintext, aad_correct)

        with self.assertRaises(AuthenticationError):
            aead.decrypt(ciphertext, aad_wrong)

    def test_empty_data(self):
        """Test with empty plaintext"""
        master_key = os.urandom(16)
        plaintext = b""
        aad = b""

        aead = AEADEncryptThenMAC(master_key)
        ciphertext = aead.encrypt(plaintext, aad)

        # Should be nonce + tag only
        self.assertEqual(len(ciphertext), 12 + 16)

        decrypted = aead.decrypt(ciphertext, aad)
        self.assertEqual(decrypted, plaintext)


if __name__ == '__main__':
    unittest.main()