# tests/debug_gcm.py
# !/usr/bin/env python3
"""
Debug GCM implementation
"""
import os
import sys
import tempfile

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def debug_gcm():
    print("DEBUG GCM IMPLEMENTATION")
    print("=" * 70)

    # Try to import GCM
    try:
        from src.modes.gcm import GCM, AuthenticationError
        print("SUCCESS: Imported GCM")
    except ImportError as e:
        print(f"ERROR: Could not import GCM: {e}")
        print("Trying alternative import...")
        try:
            # Try direct import
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "gcm",
                os.path.join(os.path.dirname(__file__), '..', 'src', 'modes', 'gcm.py')
            )
            gcm_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(gcm_module)
            GCM = gcm_module.GCM
            AuthenticationError = gcm_module.AuthenticationError
            print("SUCCESS: Loaded GCM directly")
        except Exception as e2:
            print(f"ERROR: Could not load GCM: {e2}")
            return False

    # Test basic GCM
    print("\n--- Testing basic GCM ---")
    try:
        key = bytes.fromhex('00112233445566778899aabbccddeeff')
        plaintext = b"Hello GCM World"
        aad = b"test"

        print(f"Key: {key.hex()}")
        print(f"Plaintext: {plaintext}")
        print(f"AAD: {aad}")

        # Encrypt
        gcm = GCM(key)
        print(f"\nEncrypting with nonce: {gcm.nonce.hex()}")
        ciphertext = gcm.encrypt(plaintext, aad)

        print(f"Ciphertext length: {len(ciphertext)}")
        print(f"Expected: 12 (nonce) + {len(plaintext)} + 16 (tag) = {12 + len(plaintext) + 16}")
        print(f"Ciphertext structure:")
        print(f"  Nonce (12 bytes): {ciphertext[:12].hex()}")
        print(f"  Encrypted data ({len(ciphertext) - 28} bytes): ...")
        print(f"  Tag (16 bytes): {ciphertext[-16:].hex()}")

        # Decrypt
        gcm2 = GCM(key, gcm.nonce)
        print(f"\nDecrypting with same nonce: {gcm2.nonce.hex()}")
        decrypted = gcm2.decrypt(ciphertext, aad)

        print(f"Decrypted: {decrypted}")

        if decrypted == plaintext:
            print("\nSUCCESS: Basic GCM works!")
        else:
            print(f"\nERROR: Decryption mismatch!")
            print(f"Expected: {plaintext}")
            print(f"Got: {decrypted}")
            return False

    except Exception as e:
        print(f"\nERROR in basic test: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Test with CLI
    print("\n" + "=" * 70)
    print("Testing GCM through CLI...")

    # Create test file
    test_input = tempfile.mktemp(suffix='.txt')
    test_encrypted = tempfile.mktemp(suffix='.bin')
    test_decrypted = tempfile.mktemp(suffix='.txt')

    with open(test_input, 'wb') as f:
        f.write(b"CLI test message for GCM")

    key = "00112233445566778899aabbccddeeff"
    aad = "aabbccdd"

    try:
        # Encrypt via CLI
        print(f"\nEncrypting: {test_input}")
        import subprocess
        cmd = [
            sys.executable, 'src/cryptocore.py',
            'encrypt',
            '--key', key,
            '--input', test_input,
            '--output', test_encrypted,
            '--mode', 'gcm',
            '--aad', aad
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        print(f"Encryption return code: {result.returncode}")
        if result.stdout:
            print(f"Encryption stdout:\n{result.stdout[:300]}")
        if result.stderr:
            print(f"Encryption stderr:\n{result.stderr}")

        if result.returncode != 0:
            print("ERROR: Encryption via CLI failed")
            return False

        # Check encrypted file
        if not os.path.exists(test_encrypted):
            print("ERROR: Encrypted file not created")
            return False

        encrypted_size = os.path.getsize(test_encrypted)
        print(f"Encrypted file size: {encrypted_size} bytes")

        # Decrypt via CLI
        print(f"\nDecrypting: {test_encrypted}")
        cmd = [
            sys.executable, 'src/cryptocore.py',
            'encrypt',
            '--decrypt',
            '--key', key,
            '--input', test_encrypted,
            '--output', test_decrypted,
            '--mode', 'gcm',
            '--aad', aad
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        print(f"Decryption return code: {result.returncode}")
        if result.stdout:
            print(f"Decryption stdout:\n{result.stdout[:300]}")
        if result.stderr:
            print(f"Decryption stderr:\n{result.stderr}")

        if result.returncode != 0:
            print("ERROR: Decryption via CLI failed")
            return False

        # Compare files
        with open(test_input, 'rb') as f1, open(test_decrypted, 'rb') as f2:
            original = f1.read()
            decrypted = f2.read()

            if original == decrypted:
                print("\nSUCCESS: CLI GCM works!")
                print(f"Original: {original}")
                print(f"Decrypted: {decrypted}")
            else:
                print("\nERROR: CLI files don't match!")
                return False

    except Exception as e:
        print(f"\nERROR in CLI test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        for f in [test_input, test_encrypted, test_decrypted]:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except:
                    pass

    print("\n" + "=" * 70)
    print("DEBUG COMPLETE: GCM seems to work!")
    return True


if __name__ == "__main__":
    if debug_gcm():
        print("\nAll tests passed!")
        sys.exit(0)
    else:
        print("\nSome tests failed")
        sys.exit(1)