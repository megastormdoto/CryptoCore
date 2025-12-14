#!/usr/bin/env python3
"""
Complete Sprint 6 test
"""
import os
import sys
import tempfile
import subprocess

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("🚀 SPRINT 6 FINAL TEST")
print("=" * 70)


def test_requirement(name, description, test_func):
    """Test a single requirement."""
    print(f"\n{name}: {description}")
    print("-" * 50)

    try:
        if test_func():
            print("✅ PASS")
            return True
        else:
            print("❌ FAIL")
            return False
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
        return False


def test_gcm_implementation():
    """Test GCM implementation."""
    from modes.gcm import GCM, AuthenticationError

    # Test with different key sizes
    for key_size in [16, 24, 32]:
        key = b'\x00' * key_size
        plaintext = b"Test message"
        aad = b"AAD data"

        # Encrypt
        gcm = GCM(key)
        ciphertext = gcm.encrypt(plaintext, aad)

        # Check format
        if len(ciphertext) != 12 + len(plaintext) + 16:
            print(f"  Wrong format for key size {key_size}")
            return False

        # Decrypt
        gcm2 = GCM(key, gcm.nonce)
        decrypted = gcm2.decrypt(ciphertext, aad)

        if decrypted != plaintext:
            print(f"  Decryption failed for key size {key_size}")
            return False

    print("  All key sizes work correctly")
    return True


def test_aad_support():
    """Test AAD support."""
    from modes.gcm import GCM, AuthenticationError

    key = b'\x00' * 16

    # Test different AAD lengths
    test_cases = [
        b"",  # Empty AAD
        b"A",  # 1 byte
        b"A" * 16,  # 16 bytes
        b"A" * 64,  # 64 bytes
        b"A" * 1000,  # 1000 bytes
    ]

    for aad in test_cases:
        gcm = GCM(key)
        plaintext = b"Test message"
        ciphertext = gcm.encrypt(plaintext, aad)

        # Decrypt with correct AAD
        gcm2 = GCM(key, gcm.nonce)
        decrypted = gcm2.decrypt(ciphertext, aad)

        if decrypted != plaintext:
            print(f"  Failed with AAD length {len(aad)}")
            return False

        # Try with wrong AAD
        try:
            gcm3 = GCM(key, gcm.nonce)
            gcm3.decrypt(ciphertext, b"WRONG" + aad)
            print(f"  Should have failed with wrong AAD (len={len(aad)})")
            return False
        except AuthenticationError:
            pass

    print("  All AAD lengths work correctly")
    return True


def test_cli_gcm():
    """Test CLI GCM support."""
    try:
        from cli.parser import CLIParser

        # Create parser
        parser = CLIParser()

        # Test that parser accepts GCM arguments
        test_args = [
            'encrypt',
            '--key', '00112233445566778899aabbccddeeff',
            '--input', 'test.txt',
            '--output', 'out.bin',
            '--mode', 'gcm',
            '--aad', 'aabbccddeeff'
        ]

        # Temporarily replace sys.argv
        old_argv = sys.argv
        sys.argv = ['cryptocore'] + test_args

        try:
            args = parser.parse_args()
            if args.mode == 'gcm' and args.aad == b'\xaa\xbb\xcc\xdd\xee\xff':
                print("  CLI parser accepts GCM arguments")
                return True
            else:
                print(f"  Wrong args: mode={args.mode}, aad={args.aad}")
                return False
        finally:
            sys.argv = old_argv

    except Exception as e:
        print(f"  CLI test error: {e}")
        return False


def test_file_format():
    """Test file format (nonce + ciphertext + tag)."""
    from modes.gcm import GCM

    key = b'\x00' * 16

    # Test different plaintext lengths
    lengths = [0, 1, 15, 16, 17, 32, 100, 1000]

    for length in lengths:
        plaintext = b"X" * length
        gcm = GCM(key)
        ciphertext = gcm.encrypt(plaintext, b"")

        # Parse components
        nonce = ciphertext[:12]
        tag = ciphertext[-16:]
        actual_ciphertext = ciphertext[12:-16]

        if len(nonce) != 12:
            print(f"  Wrong nonce length: {len(nonce)}")
            return False

        if len(tag) != 16:
            print(f"  Wrong tag length: {len(tag)}")
            return False

        if len(actual_ciphertext) != length:
            print(f"  Wrong ciphertext length: {len(actual_ciphertext)} != {length}")
            return False

    print("  All file formats correct")
    return True


def test_security():
    """Test security properties."""
    from modes.gcm import GCM, AuthenticationError

    key = b'\x00' * 16
    plaintext = b"Secret message"
    aad = b"Auth data"

    # Encrypt
    gcm = GCM(key)
    ciphertext = gcm.encrypt(plaintext, aad)

    # Test 1: Tamper with ciphertext
    tampered = bytearray(ciphertext)
    if len(tampered) > 20:
        tampered[15] ^= 0x01  # Flip one bit

        try:
            gcm2 = GCM(key, gcm.nonce)
            gcm2.decrypt(bytes(tampered), aad)
            print("  Should have failed with tampered ciphertext")
            return False
        except AuthenticationError:
            pass

    # Test 2: Tamper with tag
    tampered_tag = bytearray(ciphertext)
    tampered_tag[-1] ^= 0x01  # Flip last bit of tag

    try:
        gcm3 = GCM(key, gcm.nonce)
        gcm3.decrypt(bytes(tampered_tag), aad)
        print("  Should have failed with tampered tag")
        return False
    except AuthenticationError:
        pass

    print("  Security properties verified")
    return True


def main():
    """Run all tests."""
    tests = [
        ("STR-2", "GCM implementation", test_gcm_implementation),
        ("AEAD-4", "AAD support", test_aad_support),
        ("CLI-1", "CLI GCM support", test_cli_gcm),
        ("IO-1", "File format", test_file_format),
        ("AEAD-6", "Security properties", test_security),
    ]

    passed = 0
    total = len(tests)

    for req_id, description, test_func in tests:
        if test_requirement(req_id, description, test_func):
            passed += 1

    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Total tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")

    if passed == total:
        print("\n🎉 SPRINT 6 COMPLETED SUCCESSFULLY!")
        print("\n✅ All requirements met:")
        print("   - GCM mode implemented from scratch")
        print("   - AAD support for authenticated encryption")
        print("   - 16-byte authentication tags")
        print("   - Catastrophic failure on authentication error")
        print("   - CLI integration with --mode gcm and --aad")
        print("   - Proper file format: nonce(12) + ciphertext + tag(16)")
        print("\n🚀 Ready for submission!")
        return True
    else:
        print(f"\n⚠️  {total - passed} tests failed")
        print("Check the errors above")
        return False


if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        sys.exit(1)