"""
Tests for PBKDF2 implementation with SHA256.
"""
import unittest
import time
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from kdf.pbkdf2 import pbkdf2_hmac_sha256, pbkdf2


class TestPBKDF2(unittest.TestCase):
    """Test PBKDF2 implementation with SHA256."""

    def test_sha256_vectors(self):
        """Test PBKDF2-HMAC-SHA256 with correct test vectors."""
        print("\nTesting PBKDF2-HMAC-SHA256 (NOT SHA1 from RFC 6070)")

        # CORRECT test vectors for SHA256 (not SHA1!)
        test_cases = [
            {
                'password': b'password',
                'salt': b'salt',
                'iterations': 1,
                'dklen': 20,
                'expected': '120fb6cffcf8b32c43e7225256c4f837a86548c9'
            },
            {
                'password': b'password',
                'salt': b'salt',
                'iterations': 2,
                'dklen': 20,
                'expected': 'ae4d0c95af6b46d32d0adff928f06dd02a303f8e'
            },
            {
                'password': b'password',
                'salt': b'salt',
                'iterations': 4096,
                'dklen': 20,
                'expected': 'c5e478d59288c841aa530db6845c4c8d962893a0'
            },
            {
                'password': b'passwordPASSWORDpassword',
                'salt': b'saltSALTsaltSALTsaltSALTsaltSALTsalt',
                'iterations': 4096,
                'dklen': 25,
                'expected': '348c89dbcbd32b2f32d814b8116e84cf2b17347ebc1800181c'
            }
        ]

        for i, test in enumerate(test_cases):
            with self.subTest(test_case=i + 1):
                result = pbkdf2_hmac_sha256(
                    test['password'],
                    test['salt'],
                    test['iterations'],
                    test['dklen']
                )
                expected_bytes = bytes.fromhex(test['expected'])
                self.assertEqual(result, expected_bytes,
                                 f"SHA256 test case {i + 1} failed\n"
                                 f"Expected: {test['expected']}\n"
                                 f"Got:      {result.hex()}")
                print(f"✓ SHA256 test case {i + 1} passed")

    def test_string_inputs(self):
        """Test with string inputs."""
        result = pbkdf2_hmac_sha256(
            'password',
            'salt',
            1,
            20
        )
        expected = bytes.fromhex('120fb6cffcf8b32c43e7225256c4f837a86548c9')
        self.assertEqual(result, expected)

    def test_hex_salt(self):
        """Test with hexadecimal salt string."""
        # '73616c74' is hex for 'salt'
        result = pbkdf2_hmac_sha256(
            'password',
            '73616c74',
            1,
            20
        )
        expected = bytes.fromhex('120fb6cffcf8b32c43e7225256c4f837a86548c9')
        self.assertEqual(result, expected)

    def test_various_lengths(self):
        """Test with various key lengths."""
        for length in [1, 16, 32, 64, 100]:
            with self.subTest(length=length):
                result = pbkdf2_hmac_sha256(
                    'password',
                    'salt',
                    1000,
                    length
                )
                self.assertEqual(len(result), length)

    def test_deterministic(self):
        """Test that same inputs produce same output."""
        result1 = pbkdf2_hmac_sha256('test', 'salt', 1000, 32)
        result2 = pbkdf2_hmac_sha256('test', 'salt', 1000, 32)
        self.assertEqual(result1, result2)

    def test_performance(self):
        """Measure performance for different iteration counts."""
        iterations_to_test = [1000, 10000, 100000]

        for iterations in iterations_to_test:
            start_time = time.time()
            pbkdf2_hmac_sha256('password', 'salt', iterations, 32)
            elapsed = time.time() - start_time

            print(f"Iterations: {iterations:,}, Time: {elapsed:.3f}s")
            # Just ensure it completes, no assertion on time

    def test_main_pbkdf2_function(self):
        """Test the main pbkdf2 wrapper function."""
        result = pbkdf2('password', 'salt', iterations=1, dklen=20)
        expected = bytes.fromhex('120fb6cffcf8b32c43e7225256c4f837a86548c9')
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()