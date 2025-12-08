import unittest
import sys
import os

# Add src directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mac.hmac import HMAC
from hash.sha256 import SHA256
from hash.sha3_256 import SHA3_256


class TestHMAC(unittest.TestCase):
    """Test cases for HMAC implementation"""

    def test_rfc_4231_test_case_1(self):
        """RFC 4231 Test Case 1 - HMAC-SHA256"""
        key = bytes.fromhex('0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b')
        data = b"Hi There"
        expected = "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7"

        hmac = HMAC(key, SHA256)
        result = hmac.compute(data).hex()
        self.assertEqual(result, expected)
        print(f"✓ Test 1 passed")

    def test_rfc_4231_test_case_2(self):
        """RFC 4231 Test Case 2 - HMAC-SHA256"""
        key = bytes.fromhex('4a656665')
        data = b"what do ya want for nothing?"
        expected = "5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843"

        hmac = HMAC(key, SHA256)
        result = hmac.compute(data).hex()
        self.assertEqual(result, expected)
        print(f"✓ Test 2 passed")

    def test_rfc_4231_test_case_3(self):
        """RFC 4231 Test Case 3 - HMAC-SHA256"""
        key = bytes.fromhex('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        data = b'\xdd' * 50
        expected = "773ea91e36800e46854db8ebd09181a72959098b3ef8c122d9635514ced565fe"

        hmac = HMAC(key, SHA256)
        result = hmac.compute(data).hex()
        self.assertEqual(result, expected)
        print(f"✓ Test 3 passed")

    def test_rfc_4231_test_case_4(self):
        """RFC 4231 Test Case 4 - HMAC-SHA256"""
        key = bytes.fromhex('0102030405060708090a0b0c0d0e0f10111213141516171819')
        data = b'\xcd' * 50
        expected = "82558a389a443c0ea4cc819899f2083a85f0faa3e578f8077a2e3ff46729665b"

        hmac = HMAC(key, SHA256)
        result = hmac.compute(data).hex()
        self.assertEqual(result, expected)
        print(f"✓ Test 4 passed")

    def test_key_shorter_than_block_size(self):
        """Test with key shorter than block size (16 bytes)"""
        key = b'shortkey12345678'  # 16 bytes
        data = b"Test message"

        hmac = HMAC(key, SHA256)
        result1 = hmac.compute(data).hex()

        # Should be deterministic
        hmac2 = HMAC(key, SHA256)
        result2 = hmac2.compute(data).hex()

        self.assertEqual(result1, result2)
        print(f"✓ Short key test passed")

    def test_key_equal_to_block_size(self):
        """Test with key equal to block size (64 bytes)"""
        key = b'x' * 64  # Exactly block size
        data = b"Test message"

        hmac = HMAC(key, SHA256)
        result = hmac.compute(data).hex()
        # Just check it computes without error
        self.assertEqual(len(result), 64)  # 32 bytes = 64 hex chars
        print(f"✓ Block-size key test passed")

    def test_key_longer_than_block_size(self):
        """Test with key longer than block size (100 bytes)"""
        key = b'x' * 100  # Longer than block size
        data = b"Test message"

        hmac = HMAC(key, SHA256)
        result = hmac.compute(data).hex()
        # Just check it computes without error
        self.assertEqual(len(result), 64)
        print(f"✓ Long key test passed")

    def test_empty_message(self):
        """Test HMAC with empty message"""
        key = bytes.fromhex('0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b')
        data = b""

        hmac = HMAC(key, SHA256)
        result = hmac.compute(data).hex()
        # Just check it computes without error
        self.assertEqual(len(result), 64)
        print(f"✓ Empty message test passed")

    def test_tamper_detection(self):
        """Test that HMAC detects tampered messages"""
        key = b'secretkey'
        original_data = b"Original message"
        tampered_data = b"Tampered message"

        hmac = HMAC(key, SHA256)
        original_hash = hmac.compute(original_data)
        tampered_hash = hmac.compute(tampered_data)

        self.assertNotEqual(original_hash, tampered_hash)
        print(f"✓ Tamper detection test passed")

    def test_wrong_key_detection(self):
        """Test that HMAC with wrong key produces different result"""
        original_key = b'correctkey'
        wrong_key = b'wrongkey123'
        data = b"Test message"

        hmac1 = HMAC(original_key, SHA256)
        hmac2 = HMAC(wrong_key, SHA256)

        result1 = hmac1.compute(data)
        result2 = hmac2.compute(data)

        self.assertNotEqual(result1, result2)
        print(f"✓ Wrong key detection test passed")

    def test_hmac_with_sha3_256(self):
        """Test HMAC with SHA3-256 (bonus)"""
        key = bytes.fromhex('0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b')
        data = b"Hi There"

        # Note: SHA3-256 will produce different result than SHA-256
        hmac = HMAC(key, SHA3_256)
        result = hmac.compute(data).hex()

        # Just check it computes without error
        self.assertEqual(len(result), 64)
        print(f"✓ SHA3-256 test passed")


if __name__ == '__main__':
    unittest.main(verbosity=2)