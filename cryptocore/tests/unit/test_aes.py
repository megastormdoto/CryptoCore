#!/usr/bin/env python3
"""Tests for AES implementation."""
import unittest
from src.ciphers.aes import AES


class TestAES(unittest.TestCase):
    def test_encrypt(self):
        """Test AES encryption."""
        key = b'0' * 16
        plaintext = b'hello world!!!!!'  # 16 bytes
        aes = AES(key)

        # Проверим что encrypt работает
        ciphertext = aes.encrypt(plaintext)
        self.assertEqual(len(ciphertext), 16)
        self.assertNotEqual(ciphertext, plaintext)

    def test_key_expansion(self):
        key = b'0' * 16
        aes = AES(key)
        # Проверим что round_keys созданы
        self.assertTrue(hasattr(aes, 'round_keys'))
        self.assertGreater(len(aes.round_keys), 0)

    def test_invalid_key_length(self):
        with self.assertRaises(ValueError):
            AES(b'short')

    def test_different_key_sizes(self):
        # AES-128
        aes128 = AES(b'0' * 16)
        self.assertIsNotNone(aes128)

        # AES-192
        aes192 = AES(b'0' * 24)
        self.assertIsNotNone(aes192)

        # AES-256
        aes256 = AES(b'0' * 32)
        self.assertIsNotNone(aes256)