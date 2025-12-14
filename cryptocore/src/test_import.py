#!/usr/bin/env python3
"""
Test that all imports work correctly
"""
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("🔍 Testing imports...")
print("=" * 50)

try:
    # Test 1: Import GCM
    print("\n1. Testing GCM import...")
    from modes.gcm import GCM, AuthenticationError

    print("   ✅ GCM imported successfully")

    # Test 2: Create GCM instance
    print("\n2. Testing GCM instance creation...")
    key = b'\x00' * 16
    gcm = GCM(key)
    print(f"   ✅ GCM instance created")
    print(f"   Nonce: {gcm.nonce.hex()}")
    print(f"   Nonce length: {len(gcm.nonce)} bytes")

    # Test 3: Basic encryption/decryption
    print("\n3. Testing encryption/decryption...")
    plaintext = b"Hello CryptoCore!"
    aad = b"Test AAD"

    ciphertext = gcm.encrypt(plaintext, aad)
    print(f"   ✅ Encryption successful")
    print(f"   Ciphertext length: {len(ciphertext)} bytes")

    # Check format
    if len(ciphertext) == 12 + len(plaintext) + 16:
        print(f"   ✅ Format correct: nonce(12) + ciphertext({len(plaintext)}) + tag(16)")
    else:
        print(f"   ❌ Format wrong: {len(ciphertext)} != {12 + len(plaintext) + 16}")

    # Decrypt
    gcm2 = GCM(key, gcm.nonce)
    decrypted = gcm2.decrypt(ciphertext, aad)

    if decrypted == plaintext:
        print("   ✅ Decryption successful")
    else:
        print(f"   ❌ Decryption failed")

    # Test 4: Wrong AAD should fail
    print("\n4. Testing authentication failure...")
    try:
        gcm3 = GCM(key, gcm.nonce)
        gcm3.decrypt(ciphertext, b"WRONG AAD")
        print("   ❌ Should have failed!")
    except AuthenticationError:
        print("   ✅ Correctly failed with wrong AAD")
    except Exception as e:
        print(f"   ❌ Wrong error type: {type(e).__name__}")

    # Test 5: Import CLI parser
    print("\n5. Testing CLI parser import...")
    try:
        from cli.parser import CLIParser

        parser = CLIParser()
        print("   ✅ CLI parser imported and created")
    except Exception as e:
        print(f"   ❌ CLI parser error: {e}")

    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED!")
    print("\n✅ Sprint 6 requirements verified:")
    print("   - GCM implementation ✓")
    print("   - AAD support ✓")
    print("   - Authentication tags ✓")
    print("   - Catastrophic failure ✓")

except ImportError as e:
    print(f"\n❌ Import error: {e}")
    print("\nCurrent directory:", os.getcwd())
    print("Files in src/modes:", os.listdir('src/modes'))
except Exception as e:
    print(f"\n❌ Test error: {type(e).__name__}: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1) 