#!/usr/bin/env python3
"""
Tests for CSPRNG module
"""

import os
import sys

# Add path to import from src
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_path)

# ИСПРАВЛЕННЫЙ ИМПОРТ - используем cspmg вместо csprng
from csprng import generate_random_bytes, generate_key, generate_iv, bytes_to_hex, is_weak_key


def test_generate_random_bytes():
    """Test generating random bytes of various lengths"""
    print("Testing generate_random_bytes...")
    # Test different byte lengths
    for length in [1, 16, 32, 100]:
        result = generate_random_bytes(length)
        assert len(result) == length, f"Expected {length} bytes, got {len(result)}"
        assert isinstance(result, bytes), "Result should be bytes"
        print(f"  ✅ {length} bytes - OK")
    print("✅ generate_random_bytes tests passed")


def test_generate_key():
    """Test AES key generation"""
    print("Testing generate_key...")
    key = generate_key()
    assert len(key) == 16, "AES key should be 16 bytes"
    assert isinstance(key, bytes), "Key should be bytes"
    print(f"  ✅ Generated key: {bytes_to_hex(key)}")
    print("✅ generate_key tests passed")


def test_generate_iv():
    """Test IV generation"""
    print("Testing generate_iv...")
    iv = generate_iv()
    assert len(iv) == 16, "IV should be 16 bytes"
    assert isinstance(iv, bytes), "IV should be bytes"
    print(f"  ✅ Generated IV: {bytes_to_hex(iv)}")
    print("✅ generate_iv tests passed")


def test_bytes_to_hex():
    """Test bytes to hex conversion"""
    print("Testing bytes_to_hex...")
    test_bytes = b'\x00\x11\x22\xff'
    hex_string = bytes_to_hex(test_bytes)
    assert hex_string == '001122ff', f"Expected '001122ff', got '{hex_string}'"
    print("✅ bytes_to_hex tests passed")


def test_key_uniqueness():
    """Test that generated keys are unique"""
    print("Testing key uniqueness...")
    key_set = set()
    num_keys = 10  # Reduced for faster testing

    for i in range(num_keys):
        key = generate_key()
        key_hex = bytes_to_hex(key)

        # Check for uniqueness
        assert key_hex not in key_set, f"Duplicate key found: {key_hex}"
        key_set.add(key_hex)

        if i % 5 == 0:
            print(f"  Generated {i + 1} keys...")

    print(f"✅ Successfully generated {len(key_set)} unique keys")


def test_weak_key_detection():
    """Test weak key detection"""
    print("Testing weak key detection...")

    # Test all zeros (weak)
    weak_key1 = bytes([0] * 16)
    assert is_weak_key(weak_key1), "All zeros should be detected as weak"
    print("  ✅ All zeros detected as weak")

    # Test sequential bytes (weak)
    weak_key2 = bytes(range(16))  # 0, 1, 2, ..., 15
    assert is_weak_key(weak_key2), "Sequential bytes should be detected as weak"
    print("  ✅ Sequential bytes detected as weak")

    # Test repeated pattern (weak)
    weak_key3 = b'\x01\x02' * 8  # Repeated 2-byte pattern
    assert is_weak_key(weak_key3), "Repeated pattern should be detected as weak"
    print("  ✅ Repeated pattern detected as weak")

    # Test strong key (should not be weak)
    strong_key = generate_key()
    assert not is_weak_key(strong_key), "Random key should not be detected as weak"
    print("  ✅ Random key detected as strong")

    print("✅ weak_key_detection tests passed")


def main():
    """Run all tests"""
    print("🚀 Running CSPRNG Tests...")
    print("=" * 50)

    tests = [
        test_generate_random_bytes,
        test_generate_key,
        test_generate_iv,
        test_bytes_to_hex,
        test_key_uniqueness,
        test_weak_key_detection,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            test()
            passed += 1
            print(f"✅ {test.__name__} - PASSED\n")
        except Exception as e:
            print(f"❌ {test.__name__} - FAILED: {e}\n")

    # Final summary
    print("=" * 50)
    print(f"📊 TEST SUMMARY: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())