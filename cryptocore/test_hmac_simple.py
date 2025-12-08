# test_hmac_simple.py (сохрани в cryptocore/cryptocore/)
import os
import sys
import shutil

# Добавляем src в путь
sys.path.insert(0, 'src')

from mac.hmac import HMAC
from hash.sha256 import SHA256


def test_rfc_4231():
    """Test HMAC with RFC 4231 test vectors"""
    print("Testing RFC 4231 test cases...")

    test_cases = [
        {
            'key': '0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b',
            'data': b'Hi There',
            'expected': 'b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7'
        },
        {
            'key': '4a656665',
            'data': b'what do ya want for nothing?',
            'expected': '5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843'
        }
    ]

    for i, test in enumerate(test_cases):
        key = bytes.fromhex(test['key'])
        data = test['data']

        hmac = HMAC(key, SHA256)
        result = hmac.compute(data).hex()

        if result == test['expected']:
            print(f"✓ RFC 4231 test case {i + 1} passed")
        else:
            print(f"✗ RFC 4231 test case {i + 1} failed")
            print(f"  Expected: {test['expected']}")
            print(f"  Got:      {result}")
            return False

    return True


def test_key_sizes():
    """Test various key sizes"""
    print("\nTesting key sizes...")

    data = b'Test message'

    # Short key (16 bytes)
    short_key = b'shortkey12345678'
    hmac1 = HMAC(short_key, SHA256)
    result1 = hmac1.compute(data)

    # Block size key (64 bytes)
    block_key = b'x' * 64
    hmac2 = HMAC(block_key, SHA256)
    result2 = hmac2.compute(data)

    # Long key (100 bytes)
    long_key = b'x' * 100
    hmac3 = HMAC(long_key, SHA256)
    result3 = hmac3.compute(data)

    print(f"✓ Short key (16 bytes): {len(result1)} bytes")
    print(f"✓ Block size key (64 bytes): {len(result2)} bytes")
    print(f"✓ Long key (100 bytes): {len(result3)} bytes")

    return True


def test_tamper_detection():
    """Test that HMAC detects tampered messages"""
    print("\nTesting tamper detection...")

    key = b'secretkey'
    original_data = b"Original message"
    tampered_data = b"Tampered message"

    hmac = HMAC(key, SHA256)
    original_hash = hmac.compute(original_data)
    tampered_hash = hmac.compute(tampered_data)

    if original_hash != tampered_hash:
        print("✓ Tamper detection works")
        return True
    else:
        print("✗ Tamper detection failed")
        return False


def test_wrong_key():
    """Test that wrong key produces different HMAC"""
    print("\nTesting wrong key detection...")

    correct_key = b'correctkey'
    wrong_key = b'wrongkey123'
    data = b"Test message"

    hmac1 = HMAC(correct_key, SHA256)
    hmac2 = HMAC(wrong_key, SHA256)

    result1 = hmac1.compute(data)
    result2 = hmac2.compute(data)

    if result1 != result2:
        print("✓ Wrong key detection works")
        return True
    else:
        print("✗ Wrong key detection failed")
        return False


def test_empty_message():
    """Test HMAC with empty message"""
    print("\nTesting empty message...")

    key = bytes.fromhex('0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b')
    data = b""

    hmac = HMAC(key, SHA256)
    result = hmac.compute(data)

    if len(result) == 32:  # 32 bytes for SHA-256
        print(f"✓ Empty message: {result.hex()[:16]}...")
        return True
    else:
        print(f"✗ Empty message failed: {len(result)} bytes")
        return False


def test_file_hmac():
    """Test file-based HMAC computation"""
    print("\nTesting file HMAC...")

    # Create test file
    test_content = b"This is a test file for HMAC computation."
    with open('test_file.txt', 'wb') as f:
        f.write(test_content)

    key = b'testkey123'
    hmac = HMAC(key, SHA256)

    # Compute directly from bytes
    direct_result = hmac.compute(test_content)

    # Compute from file
    file_result = hmac.compute_file('test_file.txt')

    # Clean up
    os.remove('test_file.txt')

    if direct_result == file_result:
        print("✓ File HMAC works correctly")
        return True
    else:
        print("✗ File HMAC failed")
        print(f"  Direct: {direct_result.hex()[:16]}...")
        print(f"  File:   {file_result.hex()[:16]}...")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("HMAC Implementation Tests")
    print("=" * 60)

    tests = [
        test_rfc_4231,
        test_key_sizes,
        test_tamper_detection,
        test_wrong_key,
        test_empty_message,
        test_file_hmac
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Error in test: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("✓ All HMAC tests passed!")
        return 0
    else:
        print("✗ Some HMAC tests failed")
        return 1


if __name__ == '__main__':
    exit(main())