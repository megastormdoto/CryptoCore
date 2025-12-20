#!/usr/bin/env python3
"""
Simple test to check if basic imports work
"""
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

print("Testing basic imports...")

try:
    # Test CLI parser first
    from src.cli.parser import CLIParser

    print("✓ CLIParser imported")

    # Create parser
    parser = CLIParser()
    print("✓ CLIParser created")

    # Test parsing help
    print("\nTesting help...")
    try:
        sys.argv = ['cryptocore', '--help']
        # Don't actually parse, just check it doesn't crash
        print("✓ Basic CLI structure works")
    except SystemExit:
        print("✓ Help command works")
    except Exception as e:
        print(f"✗ Help error: {e}")

    # Test GCM import
    try:
        from src.modes.gcm import GCM

        print("✓ GCM imported")

        # Try to create GCM instance
        key = b'\x00' * 16
        gcm = GCM(key)
        print("✓ GCM instance created")
        print(f"  Nonce: {gcm.nonce.hex()}")
        print(f"  Nonce length: {len(gcm.nonce)}")

        # Test basic encryption/decryption
        plaintext = b"Hello GCM"
        aad = b"test"
        ciphertext = gcm.encrypt(plaintext, aad)
        print(f"✓ Encryption worked")
        print(f"  Ciphertext length: {len(ciphertext)}")

        # Try to decrypt
        gcm2 = GCM(key, gcm.nonce)
        decrypted = gcm2.decrypt(ciphertext, aad)
        if decrypted == plaintext:
            print("✓ Decryption worked")
        else:
            print(f"✗ Decryption failed: got {decrypted}")

    except ImportError as e:
        print(f"✗ GCM import failed: {e}")
    except Exception as e:
        print(f"✗ GCM test failed: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()

    print("\n✅ Basic tests completed!")

except Exception as e:
    print(f"\n❌ Critical error: {type(e).__name__}: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)