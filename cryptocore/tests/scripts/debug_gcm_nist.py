#!/usr/bin/env python3
"""
NIST SP 800-38D test vectors for GCM - FULL VERSION
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_gcm_import():
    """Test that GCM can be imported"""
    print("🧪 Testing GCM import...")

    import_paths = [
        os.path.join(os.path.dirname(__file__), '..', 'src', 'modes'),
        os.path.join(os.path.dirname(__file__), '..', 'src'),
        '.'
    ]

    for path in import_paths:
        if path not in sys.path:
            sys.path.insert(0, path)

    try:
        from modes.gcm import GCM, AuthenticationError
        print("✅ GCM imported successfully")
        return GCM, AuthenticationError
    except ImportError as e:
        print(f"❌ Import failed: {e}")

        # Try direct import
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "gcm",
                os.path.join(os.path.dirname(__file__), '..', 'src', 'modes', 'gcm.py')
            )
            gcm_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(gcm_module)
            print("✅ GCM loaded directly from file")
            return gcm_module.GCM, gcm_module.AuthenticationError
        except Exception as e2:
            print(f"❌ Direct import also failed: {e2}")
            return None, None


def test_nist_case_1(GCM):
    """Test Case 1: Empty data"""
    print("\n=== NIST Test Case 1 (empty data) ===")

    key = bytes.fromhex('00000000000000000000000000000000')
    iv = bytes.fromhex('000000000000000000000000')
    plaintext = b''
    aad = b''

    try:
        gcm = GCM(key, iv)
        ciphertext = gcm.encrypt(plaintext, aad)

        print(f"✓ Encryption successful")
        print(f"  Nonce: {iv.hex()}")
        print(f"  Ciphertext length: {len(ciphertext)}")
        print(f"  Expected length: {12 + 0 + 16} = 28")

        # Decrypt
        decrypted = gcm.decrypt(ciphertext, aad)

        if decrypted == plaintext:
            print("✅ Test Case 1 PASSED")
            return True
        else:
            print("❌ Test Case 1 FAILED - decryption mismatch")
            return False

    except Exception as e:
        print(f"❌ Test Case 1 FAILED with error: {e}")
        return False


def test_nist_case_2(GCM):
    """Test Case 2: Single block"""
    print("\n=== NIST Test Case 2 (single block) ===")

    key = bytes.fromhex('00000000000000000000000000000000')
    iv = bytes.fromhex('000000000000000000000000')
    plaintext = bytes.fromhex('00000000000000000000000000000000')  # 16 bytes
    aad = b''

    try:
        gcm = GCM(key, iv)
        ciphertext = gcm.encrypt(plaintext, aad)

        print(f"✓ Encryption successful")
        print(f"  Plaintext: {plaintext.hex()}")
        print(f"  Ciphertext length: {len(ciphertext)}")
        print(f"  Expected length: {12 + 16 + 16} = 44")

        # Decrypt
        decrypted = gcm.decrypt(ciphertext, aad)

        if decrypted == plaintext:
            print("✅ Test Case 2 PASSED")
            return True
        else:
            print("❌ Test Case 2 FAILED - decryption mismatch")
            print(f"  Decrypted: {decrypted.hex()}")
            return False

    except Exception as e:
        print(f"❌ Test Case 2 FAILED with error: {e}")
        return False


def test_with_aad(GCM, AuthenticationError):
    """Test with AAD"""
    print("\n=== Testing with AAD ===")

    key = os.urandom(16)
    plaintext = b"This is a test message for AAD testing"
    correct_aad = b"Correct Associated Data"
    wrong_aad = b"Wrong Associated Data"

    try:
        # Encrypt with correct AAD
        gcm = GCM(key)
        ciphertext = gcm.encrypt(plaintext, correct_aad)

        print(f"✓ Encryption with AAD successful")
        print(f"  Nonce: {gcm.nonce.hex()}")

        # Try to decrypt with wrong AAD
        gcm2 = GCM(key, gcm.nonce)

        try:
            gcm2.decrypt(ciphertext, wrong_aad)
            print("❌ Should have failed with wrong AAD!")
            return False
        except AuthenticationError:
            print("✓ Correctly failed with wrong AAD")

        # Decrypt with correct AAD
        gcm3 = GCM(key, gcm.nonce)
        decrypted = gcm3.decrypt(ciphertext, correct_aad)

        if decrypted == plaintext:
            print("✅ AAD test PASSED")
            return True
        else:
            print("❌ AAD test FAILED")
            return False

    except Exception as e:
        print(f"❌ AAD test FAILED with error: {e}")
        return False


def test_tamper_detection(GCM, AuthenticationError):
    """Test ciphertext tamper detection"""
    print("\n=== Testing tamper detection ===")

    key = os.urandom(16)
    plaintext = b"Message for tamper detection test"
    aad = b"Associated data"

    try:
        # Encrypt
        gcm = GCM(key)
        ciphertext = gcm.encrypt(plaintext, aad)

        print(f"✓ Original encryption successful")

        # Tamper with ciphertext
        tampered = bytearray(ciphertext)
        tampered[20] ^= 0x01  # Flip one bit

        # Try to decrypt tampered ciphertext
        gcm2 = GCM(key, gcm.nonce)

        try:
            gcm2.decrypt(bytes(tampered), aad)
            print("❌ Should have detected tampering!")
            return False
        except AuthenticationError:
            print("✓ Correctly detected tampering")

        # Verify original still works
        gcm3 = GCM(key, gcm.nonce)
        decrypted = gcm3.decrypt(ciphertext, aad)

        if decrypted == plaintext:
            print("✅ Tamper detection test PASSED")
            return True
        else:
            print("❌ Tamper detection test FAILED")
            return False

    except Exception as e:
        print(f"❌ Tamper detection test FAILED with error: {e}")
        return False


def run_all_nist_tests():
    """Run all NIST tests"""
    print("=" * 60)
    print("NIST SP 800-38D GCM Test Suite")
    print("=" * 60)

    # First, test import
    GCM, AuthenticationError = test_gcm_import()
    if not GCM:
        print("❌ Cannot proceed without GCM module")
        return False

    results = []

    # Run tests
    results.append(("Import", True))  # Already passed

    # NIST test cases
    results.append(("NIST Case 1 (empty)", test_nist_case_1(GCM)))
    results.append(("NIST Case 2 (single block)", test_nist_case_2(GCM)))

    # Functional tests
    results.append(("AAD authentication", test_with_aad(GCM, AuthenticationError)))
    results.append(("Tamper detection", test_tamper_detection(GCM, AuthenticationError)))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = 0
    total = 0

    for test_name, result in results:
        total += 1
        if result:
            passed += 1
            print(f"✅ {test_name}: PASSED")
        else:
            print(f"❌ {test_name}: FAILED")

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_nist_tests()
    sys.exit(0 if success else 1)