# tests/diagnose_gcm.py
# !/usr/bin/env python3
"""
Diagnose GCM CLI issue
"""
import os
import sys
import tempfile
import subprocess


def diagnose():
    print("GCM CLI DIAGNOSIS")
    print("=" * 70)

    # Test 1: Direct Python GCM
    print("\n1. Testing direct Python GCM...")
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

    try:
        from src.modes.gcm import GCM

        key = bytes.fromhex('00112233445566778899aabbccddeeff')
        plaintext = b"Test message"
        aad_hex = "aabbccdd"
        aad_bytes = bytes.fromhex(aad_hex)

        print(f"Key: {key.hex()}")
        print(f"Plaintext: {plaintext}")
        print(f"AAD hex: {aad_hex}")
        print(f"AAD bytes: {aad_bytes}")

        gcm = GCM(key)
        ciphertext = gcm.encrypt(plaintext, aad_bytes)

        print(f"Nonce: {gcm.nonce.hex()}")
        print(f"Ciphertext length: {len(ciphertext)}")

        gcm2 = GCM(key, gcm.nonce)
        decrypted = gcm2.decrypt(ciphertext, aad_bytes)

        if decrypted == plaintext:
            print("✓ Direct GCM works")
        else:
            print("✗ Direct GCM failed")
            return False

    except Exception as e:
        print(f"✗ Direct test error: {e}")
        return False

    # Test 2: CLI with debug
    print("\n2. Testing CLI with debug output...")

    test_input = tempfile.mktemp(suffix='.txt')
    test_encrypted = tempfile.mktemp(suffix='.bin')
    test_decrypted = tempfile.mktemp(suffix='.txt')

    with open(test_input, 'wb') as f:
        f.write(b"CLI test message")

    try:
        # First, let's see what the CLI parser does
        print("\nRunning CLI encryption command...")
        cmd = [
            sys.executable, 'src/cryptocore.py',
            'encrypt',
            '--key', '00112233445566778899aabbccddeeff',
            '--input', test_input,
            '--output', test_encrypted,
            '--mode', 'gcm',
            '--aad', 'aabbccdd'
        ]

        print(f"Command: {' '.join(cmd)}")

        # Run with verbose output
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')

        print(f"\nEncryption stdout:\n{result.stdout}")
        print(f"\nEncryption stderr:\n{result.stderr}")
        print(f"\nEncryption return code: {result.returncode}")

        if result.returncode != 0:
            print("✗ Encryption failed")
            return False

        # Check file
        if os.path.exists(test_encrypted):
            with open(test_encrypted, 'rb') as f:
                encrypted_data = f.read()
            print(f"\nEncrypted file size: {len(encrypted_data)} bytes")
            print(f"First 20 bytes (hex): {encrypted_data[:20].hex()}")
            print(f"Nonce (first 12 bytes): {encrypted_data[:12].hex()}")

            # Try to decrypt with Python directly
            print("\n3. Decrypting with Python directly...")
            from src.modes.gcm import GCM

            key_bytes = bytes.fromhex('00112233445566778899aabbccddeeff')
            nonce = encrypted_data[:12]
            aad_bytes = bytes.fromhex('aabbccdd')

            print(f"Key: {key_bytes.hex()}")
            print(f"Nonce: {nonce.hex()}")
            print(f"AAD bytes: {aad_bytes}")

            gcm = GCM(key_bytes, nonce)
            try:
                decrypted = gcm.decrypt(encrypted_data, aad_bytes)
                print(f"✓ Direct Python decryption successful")
                print(f"Decrypted: {decrypted}")
            except Exception as e:
                print(f"✗ Direct Python decryption failed: {e}")

                # Try with different AAD formats
                print("\nTrying different AAD formats...")
                aad_formats = [
                    ("hex string 'aabbccdd'", "aabbccdd"),
                    ("bytes b'\\xaa\\xbb\\xcc\\xdd'", b'\xaa\xbb\xcc\xdd'),
                    ("string 'aabbccdd'", 'aabbccdd'),
                ]

                for name, aad in aad_formats:
                    try:
                        if isinstance(aad, str):
                            aad_bytes = bytes.fromhex(aad) if all(
                                c in '0123456789abcdefABCDEF' for c in aad) else aad.encode()
                        else:
                            aad_bytes = aad

                        print(f"\nTrying AAD as {name}: {aad_bytes}")
                        gcm = GCM(key_bytes, nonce)
                        decrypted = gcm.decrypt(encrypted_data, aad_bytes)
                        print(f"✓ SUCCESS with {name}!")
                        print(f"Decrypted: {decrypted}")
                        break
                    except Exception as e2:
                        print(f"✗ Failed with {name}: {e2}")

        else:
            print("✗ Encrypted file not created")
            return False

    except Exception as e:
        print(f"\n✗ Diagnosis error: {e}")
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
    print("Diagnosis complete")
    return True


if __name__ == "__main__":
    success = diagnose()
    sys.exit(0 if success else 1)