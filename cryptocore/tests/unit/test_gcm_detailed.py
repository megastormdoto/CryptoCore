# tests/unit/test_gcm_detailed.py
# !/usr/bin/env python3
"""Detailed tests for GCM."""
import unittest
from src.modes.gcm import GCM


class TestGCMDetailed(unittest.TestCase):
    def test_gcm_basic(self):
        key = b'0' * 16
        gcm = GCM(key)
        plaintext = b'test message'
        ciphertext = gcm.encrypt(plaintext)

        gcm2 = GCM(key, gcm.nonce)
        decrypted = gcm2.decrypt(ciphertext)
        self.assertEqual(decrypted, plaintext)

    def test_gcm_with_aad(self):
        key = b'0' * 16
        gcm = GCM(key)
        plaintext = b'test message'
        aad = b'additional data'
        ciphertext = gcm.encrypt(plaintext, aad)

        gcm2 = GCM(key, gcm.nonce)
        decrypted = gcm2.decrypt(ciphertext, aad)
        self.assertEqual(decrypted, plaintext)

    def test_gcm_authentication_failure(self):
        key = b'0' * 16
        gcm = GCM(key)
        plaintext = b'test message'
        ciphertext = gcm.encrypt(plaintext)

        # Tamper with ciphertext
        tampered = bytearray(ciphertext)
        tampered[10] ^= 0xFF

        gcm2 = GCM(key, gcm.nonce)
        with self.assertRaises(Exception):  # AuthenticationError
            gcm2.decrypt(bytes(tampered))