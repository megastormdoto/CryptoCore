# tests/unit/test_basic_imports.py
# !/usr/bin/env python3
"""Basic import tests for coverage."""
import unittest


class TestBasicImports(unittest.TestCase):
    def test_import_aes(self):
        from src.ciphers.aes import AES
        self.assertTrue(hasattr(AES, 'encrypt'))

    def test_import_hash(self):
        from src.hash.sha256 import SHA256
        from src.hash.sha3_256 import SHA3_256
        self.assertTrue(hasattr(SHA256, 'hash'))
        self.assertTrue(hasattr(SHA3_256, 'hash'))

    def test_import_hmac(self):
        from src.mac.hmac import HMAC
        self.assertTrue(hasattr(HMAC, 'compute'))

    def test_import_modes(self):
        from src.modes.cbc import CBCMode
        from src.modes.ecb import ECBMode
        from src.modes.gcm import GCM
        self.assertTrue(hasattr(CBCMode, '__init__'))
        self.assertTrue(hasattr(ECBMode, '__init__'))
        self.assertTrue(hasattr(GCM, '__init__'))

    def test_import_csprng(self):
        from src.csprng import generate_random_bytes
        self.assertTrue(callable(generate_random_bytes))