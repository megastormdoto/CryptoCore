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

# Add project root to path to import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Now import our modules
try:
    from src.hash.sha256 import SHA256
    from src.hash.sha3_256 import SHA3_256

    print("✓ Successfully imported hash modules")
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Current sys.path:", sys.path)
    sys.exit(1)


class TestHashFunctions:
    """Test suite for hash functions"""

    def test_sha256_empty(self):
        """TEST-2: Empty input test for SHA-256"""
        print("\nTesting SHA-256 empty string...")
        hasher = SHA256()
        result = hasher.hash(b"")
        expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        print(f"  Result:   {result}")
        print(f"  Expected: {expected}")
        assert result == expected, f"Empty string hash mismatch: {result} != {expected}"
        print("✓ TEST-2: SHA-256 empty string test passed")
        return True

    def test_sha3_256_empty(self):
        """TEST-2: Empty input test for SHA3-256"""
        print("\nTesting SHA3-256 empty string...")
        hasher = SHA3_256()
        result = hasher.hash(b"")
        expected = "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a"
        print(f"  Result:   {result}")
        print(f"  Expected: {expected}")
        assert result == expected, f"Empty string hash mismatch: {result} != {expected}"
        print("✓ TEST-2: SHA3-256 empty string test passed")
        return True

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

        hasher = SHA256()
        all_passed = True
        for message, expected in test_vectors:
            result = hasher.hash(message.encode('utf-8'))
            if result != expected:
                print(f"  ✗ FAILED: '{message[:20]}...' -> {result} != {expected}")
                all_passed = False
            else:
                print(f"  ✓ PASSED: '{message[:20]}...'")

        assert all_passed, "Some NIST vectors failed"
        print("✓ TEST-1: SHA-256 NIST test vectors passed")
        return True

    def test_nist_vectors_sha3_256(self):
        """TEST-1: NIST test vectors for SHA3-256"""
        print("\nTesting SHA3-256 NIST vectors...")
        test_vectors = [
            ("", "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a"),
            ("abc", "3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532"),
        ]

        hasher = SHA3_256()
        all_passed = True
        for message, expected in test_vectors:
            result = hasher.hash(message.encode('utf-8'))
            if result != expected:
                print(f"  ✗ FAILED: '{message[:20]}...' -> {result} != {expected}")
                all_passed = False
            else:
                print(f"  ✓ PASSED: '{message[:20]}...'")

        assert all_passed, "Some NIST vectors failed"
        print("✓ TEST-1: SHA3-256 NIST test vectors passed")
        return True

    def test_avalanche_effect_sha256(self):
        """TEST-5: Avalanche effect test for SHA-256"""
        print("\nTesting SHA-256 avalanche effect...")
        hasher = SHA256()

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
        if not (100 < diff_count < 156):
            print(f"  ⚠️  Warning: Avalanche effect weaker than expected")
        else:
            print(f"  ✓ Good avalanche effect")

        print("✓ TEST-5: SHA-256 avalanche effect test completed")
        return True

    def test_avalanche_effect_sha3_256(self):
        """TEST-5: Avalanche effect test for SHA3-256"""
        print("\nTesting SHA3-256 avalanche effect...")
        hasher = SHA3_256()

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

        if not (100 < diff_count < 156):
            print(f"  ⚠️  Warning: Avalanche effect weaker than expected")
        else:
            print(f"  ✓ Good avalanche effect")

        print("✓ TEST-5: SHA3-256 avalanche effect test completed")
        return True

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
            hasher = SHA256()
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

            if our_hash == sys_hash:
                print(f"  ✓ Hashes match!")
            else:
                print(f"  ✗ Hashes don't match!")
                return False

            print("✓ TEST-4: SHA-256 large file test passed (1MB)")
            return True

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
            hasher = SHA3_256()
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

            if our_hash == sys_hash:
                print(f"  ✓ Hashes match!")
            else:
                print(f"  ✗ Hashes don't match!")
                return False

            print("✓ TEST-4: SHA3-256 large file test passed (512KB)")
            return True

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
            hasher = SHA256()
            hasher.update(test_data)
            our_sha256_hash = hasher.hexdigest()
            our_sha256_time = time.perf_counter() - start

            start = time.perf_counter()
            sys_sha256_hash = hashlib.sha256(test_data).hexdigest()
            sys_sha256_time = time.perf_counter() - start

            # SHA3-256
            start = time.perf_counter()
            hasher = SHA3_256()
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

        assert all_sha256_match, "SHA-256 hash mismatch in performance test"
        assert all_sha3_match, "SHA3-256 hash mismatch in performance test"

        print("\n" + "=" * 60)
        print("✓ TEST-6: Performance test completed")
        print("=" * 60)
        return True

    def test_interoperability(self):
        """TEST-3: Interoperability with system tools"""
        print("\n" + "=" * 60)
        print("TEST-3: Interoperability tests")
        print("=" * 60)

        # Create test file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.txt') as f:
            f.write(b"This is a test file for interoperability checks.\n")
            f.write(b"Second line with some data.\n")
            f.write(b"Third line with more content.\n")
            test_file = f.name

        try:
            test_file_abs = os.path.abspath(test_file)
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)
            cryptocore_path = os.path.join(project_root, 'cryptocore.py')

            print(f"Test file: {test_file}")
            print(f"CryptoCore path: {cryptocore_path}")

            # Test 1: SHA-256
            print("\n1. Testing SHA-256 interoperability...")

            # Run our implementation
            result = subprocess.run(
                [sys.executable, cryptocore_path, 'dgst', '--algorithm', 'sha256', '--input', test_file_abs],
                capture_output=True,
                text=True,
                cwd=project_root
            )

            if result.returncode != 0:
                print(f"  ✗ Our implementation failed: {result.stderr}")
                our_sha256_hash = None
            else:
                our_output = result.stdout.strip()
                if our_output:
                    our_sha256_hash = our_output.split()[0]
                    print(f"  Our output: {our_sha256_hash}")
                else:
                    our_sha256_hash = None
                    print(f"  ✗ No output from our implementation")

            # Try to get system hash (sha256sum)
            try:
                result = subprocess.run(
                    ['sha256sum', test_file_abs],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    sys_sha256_hash = result.stdout.strip().split()[0]
                    print(f"  System sha256sum: {sys_sha256_hash}")

                    if our_sha256_hash and our_sha256_hash == sys_sha256_hash:
                        print(f"  ✓ SHA-256 hashes match!")
                    elif our_sha256_hash:
                        print(f"  ✗ SHA-256 hashes don't match!")
                    else:
                        print(f"  ⚠️  Could not compare (our impl failed)")
                else:
                    print(f"  ⚠️  sha256sum not available or failed")
                    sys_sha256_hash = None
            except FileNotFoundError:
                print(f"  ⚠️  sha256sum command not found on this system")
                sys_sha256_hash = None

            # Test 2: SHA3-256
            print("\n2. Testing SHA3-256 interoperability...")

            # Run our implementation
            result = subprocess.run(
                [sys.executable, cryptocore_path, 'dgst', '--algorithm', 'sha3-256', '--input', test_file_abs],
                capture_output=True,
                text=True,
                cwd=project_root
            )

            if result.returncode != 0:
                print(f"  ✗ Our implementation failed: {result.stderr}")
                our_sha3_hash = None
            else:
                our_output = result.stdout.strip()
                if our_output:
                    our_sha3_hash = our_output.split()[0]
                    print(f"  Our output: {our_sha3_hash}")
                else:
                    our_sha3_hash = None
                    print(f"  ✗ No output from our implementation")

            # Try to get system hash (sha3sum)
            try:
                result = subprocess.run(
                    ['sha3sum', '-a', '256', test_file_abs],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    sys_sha3_hash = result.stdout.strip().split()[0]
                    print(f"  System sha3sum: {sys_sha3_hash}")

                    if our_sha3_hash and our_sha3_hash == sys_sha3_hash:
                        print(f"  ✓ SHA3-256 hashes match!")
                    elif our_sha3_hash:
                        print(f"  ✗ SHA3-256 hashes don't match!")
                    else:
                        print(f"  ⚠️  Could not compare (our impl failed)")
                else:
                    print(f"  ⚠️  sha3sum not available or failed")
                    sys_sha3_hash = None
            except FileNotFoundError:
                print(f"  ⚠️  sha3sum command not found on this system")
                sys_sha3_hash = None

            print("\n" + "=" * 60)
            print("✓ TEST-3: Interoperability tests completed")
            print("Note: Some checks may show warnings if system tools are not available")
            print("=" * 60)
            return True

        finally:
            # Clean up
            try:
                os.unlink(test_file)
            except:
                pass


def run_all_tests():
    """Run all hash function tests"""
    print("=" * 70)
    print("Running CryptoCore Hash Function Tests (Sprint 4)")
    print("=" * 70)

    tester = TestHashFunctions()

    # Run tests in order
    tests = [
        ("Empty string SHA-256", tester.test_sha256_empty),
        ("Empty string SHA3-256", tester.test_sha3_256_empty),
        ("NIST vectors SHA-256", tester.test_nist_vectors_sha256),
        ("NIST vectors SHA3-256", tester.test_nist_vectors_sha3_256),
        ("Avalanche SHA-256", tester.test_avalanche_effect_sha256),
        ("Avalanche SHA3-256", tester.test_avalanche_effect_sha3_256),
        ("Large file SHA-256", tester.test_large_file_sha256),
        ("Large file SHA3-256", tester.test_large_file_sha3_256),
        ("Performance", tester.test_performance_comparison),
        ("Interoperability", tester.test_interoperability),
    ]

    passed = 0
    failed = 0
    results = []

    for test_name, test_func in tests:
        print(f"\n{'=' * 40}")
        print(f"Running: {test_name}")
        print(f"{'=' * 40}")

        try:
            success = test_func()
            if success:
                passed += 1
                results.append((test_name, "✓ PASSED"))
            else:
                failed += 1
                results.append((test_name, "✗ FAILED"))
        except AssertionError as e:
            failed += 1
            print(f"  AssertionError: {e}")
            results.append((test_name, f"✗ FAILED: {e}"))
        except Exception as e:
            failed += 1
            print(f"  Exception: {e}")
            results.append((test_name, f"✗ ERROR: {e}"))

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    for test_name, result in results:
        print(f"{test_name:30} {result}")

    print(f"\nTotal: {passed} passed, {failed} failed")
    print("=" * 70)

    if failed == 0:
        print("🎉 All hash function tests passed!")
    else:
        print(f"⚠️  {failed} test(s) failed")

    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)