"""
Tests for key hierarchy implementation.
"""
import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from kdf.hkdf import derive_key


class TestHKDF(unittest.TestCase):
    """Test key hierarchy implementation."""

    def test_deterministic(self):
        """Test that same inputs produce same output."""
        master_key = b'0' * 32
        context = 'encryption'

        key1 = derive_key(master_key, context, 32)
        key2 = derive_key(master_key, context, 32)

        self.assertEqual(key1, key2)

    def test_context_separation(self):
        """Test that different contexts produce different keys."""
        master_key = b'0' * 32

        key1 = derive_key(master_key, 'encryption', 32)
        key2 = derive_key(master_key, 'authentication', 32)
        key3 = derive_key(master_key, 'encryption', 32)  # Same as key1

        self.assertNotEqual(key1, key2)
        self.assertEqual(key1, key3)

    def test_various_lengths(self):
        """Test with various key lengths."""
        master_key = b'0' * 32
        context = 'test'

        for length in [1, 16, 32, 64, 100]:
            with self.subTest(length=length):
                key = derive_key(master_key, context, length)
                self.assertEqual(len(key), length)

    def test_string_context(self):
        """Test with string context."""
        master_key = b'0' * 32

        key1 = derive_key(master_key, 'encryption', 32)
        key2 = derive_key(master_key, b'encryption', 32)

        self.assertEqual(key1, key2)

    def test_master_key_validation(self):
        """Test master key length validation."""
        # Should work with 16+ bytes
        derive_key(b'0' * 16, 'test', 32)

        # Should raise error with short key
        with self.assertRaises(ValueError):
            derive_key(b'0' * 15, 'test', 32)


if __name__ == '__main__':
    unittest.main()