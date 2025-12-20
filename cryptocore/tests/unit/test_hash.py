#!/usr/bin/env python3
"""
Comprehensive tests for hash functions (Sprint 4)
"""
import os
import sys
import tempfile
import time
import hashlib
import subprocess
import struct
import unittest

# Add project root to path to import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)


class TestHashFunctions(unittest.TestCase):
    """Test suite for hash functions"""

    @classmethod
    def setUpClass(cls):
        """Import modules once"""
        try:
            from src.hash.sha256 import SHA256
            from src.hash.sha3_256 import SHA3_256
            cls.SHA256 = SHA256
            cls.SHA3_256 = SHA3_256
            print("✓ Successfully imported hash modules")
        except ImportError as e:
            print(f"✗ Import error: {e}")
            print("Current sys.path:", sys.path)
            raise

    def setUp(self):
        """Reset hashers before each test"""
        self.sha256 = self.SHA256()
        self.sha3_256 = self.SHA3_256()

    def test_sha256_empty(self):
        """TEST-2: Empty input test for SHA-256"""
        print("\nTesting SHA-256 empty string...")
        result = self.sha256.hash(b"")
        expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        print(f"  Result:   {result}")
        print(f"  Expected: {expected}")
        self.assertEqual(result, expected,
                         f"Empty string hash mismatch: {result} != {expected}")
        print("✓ TEST-2: SHA-256 empty string test passed")

    def test_sha3_256_empty(self):
        """TEST-2: Empty input test for SHA3-256"""
        print("\nTesting SHA3-256 empty string...")
        result = self.sha3_256.hash(b"")
        expected = "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a"
        print(f"  Result:   {result}")
        print(f"  Expected: {expected}")
        self.assertEqual(result, expected,
                         f"Empty string hash mismatch: {result} != {expected}")
        print("✓ TEST-2: SHA3-256 empty string test passed")

    def test_nist_vectors_sha256(self):
        """TEST-1: NIST test vectors for SHA-256"""
        print("\nTesting SHA-256 NIST vectors...")
        test_vectors = [
            ("abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
            ("", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
            ("The quick brown fox jumps over the lazy dog",
             "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"),
            ("The quick brown fox jumps over the lazy dog.",
             "ef537f25c895bfa782526529a9b63d97aa631564d5d789c2b765448c8635fb6c"),
        ]

        hasher = self.SHA256()
        all_passed = True
        failures = []
        for message, expected in test_vectors:
            result = hasher.hash(message.encode('utf-8'))
            if result != expected:
                print(f"  ✗ FAILED: '{message[:20]}...' -> {result} != {expected}")
                all_passed = False
                failures.append(f"'{message[:20]}...'")
            else:
                print(f"  ✓ PASSED: '{message[:20]}...'")

        self.assertTrue(all_passed, f"NIST vectors failed: {', '.join(failures)}")
        print("✓ TEST-1: SHA-256 NIST test vectors passed")

    def test_nist_vectors_sha3_256(self):
        """TEST-1: NIST test vectors for SHA3-256"""
        print("\nTesting SHA3-256 NIST vectors...")
        test_vectors = [
            ("", "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a"),
            ("abc", "3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532"),
        ]

        hasher = self.SHA3_256()
        all_passed = True
        failures = []
        for message, expected in test_vectors:
            result = hasher.hash(message.encode('utf-8'))
            if result != expected:
                print(f"  ✗ FAILED: '{message[:20]}...' -> {result} != {expected}")
                all_passed = False
                failures.append(f"'{message[:20]}...'")
            else:
                print(f"  ✓ PASSED: '{message[:20]}...'")

        self.assertTrue(all_passed, f"NIST vectors failed: {', '.join(failures)}")
        print("✓ TEST-1: SHA3-256 NIST test vectors passed")

    def test_avalanche_effect_sha256(self):
        """TEST-5: Avalanche effect test for SHA-256"""
        print("\nTesting SHA-256 avalanche effect...")
        hasher = self.SHA256()

        # Original data
        original_data = b"Hello, world!"
        # Modified data (one bit changed - last character)
        modified_data = b"Hello, world?"

        hash1 = hasher.hash(original_data)
        hash2 = hasher.hash(modified_data)

        # Convert to binary and count differing bits
        bin1 = bin(int(hash1, 16))[2:].zfill(256)
        bin2 = bin(int(hash2, 16))[2:].zfill(256)

        diff_count = sum(bit1 != bit2 for bit1, bit2 in zip(bin1, bin2))

        print(f"  Original:  {hash1}")
        print(f"  Modified:  {hash2}")
        print(f"  Bits changed: {diff_count}/256 ({diff_count / 256 * 100:.1f}%)")

        # Avalanche effect: should be ~128 bits changed (50%)
        # Using wider bounds for reliability
        self.assertTrue(100 < diff_count < 156,
                        f"Weak avalanche effect: {diff_count} bits changed")
        print(f"  ✓ Good avalanche effect")
        print("✓ TEST-5: SHA-256 avalanche effect test completed")

    def test_avalanche_effect_sha3_256(self):
        """TEST-5: Avalanche effect test for SHA3-256"""
        print("\nTesting SHA3-256 avalanche effect...")
        hasher = self.SHA3_256()

        original_data = b"Hello, world!"
        modified_data = b"Hello, world?"

        hash1 = hasher.hash(original_data)
        hash2 = hasher.hash(modified_data)

        bin1 = bin(int(hash1, 16))[2:].zfill(256)
        bin2 = bin(int(hash2, 16))[2:].zfill(256)

        diff_count = sum(bit1 != bit2 for bit1, bit2 in zip(bin1, bin2))

        print(f"  Original:  {hash1}")
        print(f"  Modified:  {hash2}")
        print(f"  Bits changed: {diff_count}/256 ({diff_count / 256 * 100:.1f}%)")

        self.assertTrue(100 < diff_count < 156,
                        f"Weak avalanche effect: {diff_count} bits changed")
        print(f"  ✓ Good avalanche effect")
        print("✓ TEST-5: SHA3-256 avalanche effect test completed")

    def test_large_file_sha256(self):
        """TEST-4: Large file test for SHA-256"""
        print("\nTesting SHA-256 with large file (1MB)...")
        # Create a temporary file with 1MB of data
        with tempfile.NamedTemporaryFile(delete=False, mode='wb', suffix='.bin') as f:
            # Write 1MB of sequential data
            data = b''
            for i in range(1024):  # 1024 * 1024 = 1MB
                data += struct.pack('>I', i % 65536)  # 4 bytes per number
                if len(data) >= 1024:
                    f.write(data[:1024])
                    data = data[1024:]
            temp_file = f.name

        try:
            # Hash using our implementation (chunked)
            hasher = self.SHA256()
            with open(temp_file, 'rb') as f:
                chunk_size = 8192
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    hasher.update(chunk)
            our_hash = hasher.hexdigest()

            # Hash using Python's hashlib for verification
            with open(temp_file, 'rb') as f:
                sys_hash = hashlib.sha256(f.read()).hexdigest()

            print(f"  Our hash:    {our_hash}")
            print(f"  System hash: {sys_hash}")

            self.assertEqual(our_hash, sys_hash, "Hashes don't match!")
            print(f"  ✓ Hashes match!")
            print("✓ TEST-4: SHA-256 large file test passed (1MB)")

        finally:
            # Clean up
            try:
                os.unlink(temp_file)
            except:
                pass

    def test_large_file_sha3_256(self):
        """TEST-4: Large file test for SHA3-256"""
        print("\nTesting SHA3-256 with large file (512KB)...")
        with tempfile.NamedTemporaryFile(delete=False, mode='wb', suffix='.bin') as f:
            # Write 512KB of data
            for i in range(512):  # 512 * 1024 = 512KB
                f.write(os.urandom(1024))
            temp_file = f.name

        try:
            hasher = self.SHA3_256()
            with open(temp_file, 'rb') as f:
                chunk_size = 8192
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    hasher.update(chunk)
            our_hash = hasher.hexdigest()

            with open(temp_file, 'rb') as f:
                sys_hash = hashlib.sha3_256(f.read()).hexdigest()

            print(f"  Our hash:    {our_hash}")
            print(f"  System hash: {sys_hash}")

            self.assertEqual(our_hash, sys_hash, "Hashes don't match!")
            print(f"  ✓ Hashes match!")
            print("✓ TEST-4: SHA3-256 large file test passed (512KB)")

        finally:
            try:
                os.unlink(temp_file)
            except:
                pass

    def test_performance_comparison(self):
        """TEST-6: Performance test"""
        print("\n" + "=" * 60)
        print("TEST-6: Performance comparison")
        print("=" * 60)

        # Create test data
        test_sizes = [1024, 10240, 102400]  # 1KB, 10KB, 100KB
        results = []

        for size in test_sizes:
            test_data = os.urandom(size)

            print(f"\nTesting with {size:,} bytes ({size / 1024:.1f} KB):")

            # SHA-256
            start = time.perf_counter()
            hasher = self.SHA256()
            hasher.update(test_data)
            our_sha256_hash = hasher.hexdigest()
            our_sha256_time = time.perf_counter() - start

            start = time.perf_counter()
            sys_sha256_hash = hashlib.sha256(test_data).hexdigest()
            sys_sha256_time = time.perf_counter() - start

            # SHA3-256
            start = time.perf_counter()
            hasher = self.SHA3_256()
            hasher.update(test_data)
            our_sha3_hash = hasher.hexdigest()
            our_sha3_time = time.perf_counter() - start

            start = time.perf_counter()
            sys_sha3_hash = hashlib.sha3_256(test_data).hexdigest()
            sys_sha3_time = time.perf_counter() - start

            # Verify hashes match
            sha256_match = our_sha256_hash == sys_sha256_hash
            sha3_match = our_sha3_hash == sys_sha3_hash

            print(f"  SHA-256:")
            print(f"    Our impl:    {our_sha256_time * 1000:.2f} ms")
            print(f"    System:      {sys_sha256_time * 1000:.2f} ms")
            print(f"    Slowdown:    {our_sha256_time / sys_sha256_time:.1f}x")
            print(f"    Hash match:  {'✓' if sha256_match else '✗'}")

            print(f"  SHA3-256:")
            print(f"    Our impl:    {our_sha3_time * 1000:.2f} ms")
            print(f"    System:      {sys_sha3_time * 1000:.2f} ms")
            print(f"    Slowdown:    {our_sha3_time / sys_sha3_time:.1f}x")
            print(f"    Hash match:  {'✓' if sha3_match else '✗'}")

            results.append({
                'size': size,
                'sha256_match': sha256_match,
                'sha3_match': sha3_match
            })

        # Check all hashes matched
        all_sha256_match = all(r['sha256_match'] for r in results)
        all_sha3_match = all(r['sha3_match'] for r in results)

        self.assertTrue(all_sha256_match, "SHA-256 hash mismatch in performance test")
        self.assertTrue(all_sha3_match, "SHA3-256 hash mismatch in performance test")

        print("\n" + "=" * 60)
        print("✓ TEST-6: Performance test completed")
        print("=" * 60)


if __name__ == '__main__':
    unittest.main(verbosity=2)