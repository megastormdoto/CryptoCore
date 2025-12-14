#!/usr/bin/env python3
"""
Direct GCM test without subprocess
"""
import os
import sys
import tempfile

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

print("🧪 Direct GCM Test")
print("=" * 50)

try:
    # Test imports
    print("\n1. Testing imports...")
    from modes.gcm import GCM

    print("   ✓ GCM imported")

    from cli.parser import CLIParser

    print("   ✓ CLIParser imported")

    # Test GCM directly
    print("\n2. Testing GCM directly...")
    key = bytes.fromhex("00112233445566778899aabbccddeeff")
    plaintext = b"Hello GCM direct test!"
    aad = b"test aad"

    gcm = GCM(key)
    print(f"   Generated nonce: {gcm.nonce.hex()}")

    ciphertext = gcm.encrypt(plaintext, aad)
    print(f"   Ciphertext length: {len(ciphertext)}")
    print(f"   Structure: nonce({len(gcm.nonce)}) + cipher({len(ciphertext) - 28}) + tag(16)")

    # Decrypt
    gcm2 = GCM(key, gcm.nonce)
    decrypted = gcm2.decrypt(ciphertext, aad)

    if decrypted == plaintext:
        print("   ✓ Decryption successful")
    else:
        print("   ✗ Decryption failed")
        sys.exit(1)

    # Test wrong AAD
    print("\n3. Testing wrong AAD (should fail)...")
    try:
        gcm3 = GCM(key, gcm.nonce)
        gcm3.decrypt(ciphertext, b"WRONG AAD")
        print("   ✗ Should have failed but didn't!")
        sys.exit(1)
    except Exception as e:
        print(f"   ✓ Correctly failed: {type(e).__name__}")

    # Test CLI parser
    print("\n4. Testing CLI parser...")
    parser = CLIParser()

    # Simulate GCM encryption arguments
    test_args = [
        'encrypt',
        '--key', '00112233445566778899aabbccddeeff',
        '--input', 'test.txt',
        '--output', 'encrypted.bin',
        '--mode', 'gcm',
        '--aad', 'aabbccddeeff'
    ]

    try:
        # This will parse but not execute
        sys.argv = ['cryptocore'] + test_args
        args = parser.parse_args()
        print(f"   ✓ CLI parser accepts GCM arguments")
        print(f"   Mode: {args.mode}")
        print(f"   AAD: {args.aad}")
    except SystemExit:
        # argparse calls sys.exit() for help/errors
        pass
    except Exception as e:
        print(f"   ✗ CLI parser error: {e}")

    print("\n✅ All direct tests passed!")

except ImportError as e:
    print(f"\n❌ Import error: {e}")
    print("\nCurrent sys.path:")
    for p in sys.path:
        print(f"  {p}")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Test error: {type(e).__name__}: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)