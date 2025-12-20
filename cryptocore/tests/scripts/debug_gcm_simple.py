# tests/test_gcm_simple.py
import os
import sys
import tempfile
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_gcm_simple():
    print("Testing GCM...")

    # Find cryptocore.py
    script = None
    for path in ['cryptocore.py', 'src/cryptocore.py']:
        if os.path.exists(path):
            script = path
            break

    if not script:
        print("ERROR: cryptocore.py not found")
        return False

    # Create test files
    input_file = tempfile.mktemp(suffix='.txt')
    encrypted_file = tempfile.mktemp(suffix='.bin')
    decrypted_file = tempfile.mktemp(suffix='.txt')

    with open(input_file, 'wb') as f:
        f.write(b"Test message for GCM")

    # FIXED: AAD must be hex string
    key = "00112233445566778899aabbccddeeff"
    aad = "74657374616164313233343536"  # Hex for "testaad123456"

    try:
        # Encrypt
        print("1. Encrypting...")
        result = subprocess.run([
            sys.executable, script,
            'encrypt',
            '--key', key,
            '--input', input_file,
            '--output', encrypted_file,
            '--mode', 'gcm',
            '--aad', aad
        ], capture_output=True, text=True, encoding='utf-8', errors='ignore')

        if result.returncode != 0:
            print(f"Encryption failed: {result.stderr}")
            return False

        print(f"Encryption stdout: {result.stdout[:100]}")

        # Check encrypted file exists
        if not os.path.exists(encrypted_file):
            print("ERROR: Encrypted file not created")
            return False

        encrypted_size = os.path.getsize(encrypted_file)
        print(f"Encrypted file size: {encrypted_size} bytes")

        # Decrypt
        print("\n2. Decrypting...")
        result = subprocess.run([
            sys.executable, script,
            'encrypt',
            '--decrypt',
            '--key', key,
            '--input', encrypted_file,
            '--output', decrypted_file,
            '--mode', 'gcm',
            '--aad', aad
        ], capture_output=True, text=True, encoding='utf-8', errors='ignore')

        if result.returncode != 0:
            print(f"Decryption failed: {result.stderr}")
            return False

        print(f"Decryption stdout: {result.stdout[:100]}")

        # Compare
        with open(input_file, 'rb') as f1, open(decrypted_file, 'rb') as f2:
            original = f1.read()
            decrypted = f2.read()

            if original == decrypted:
                print(f"\nSUCCESS: GCM works!")
                print(f"Original: {original}")
                print(f"Decrypted: {decrypted}")
                return True
            else:
                print(f"\nERROR: Files don't match")
                print(f"Original length: {len(original)}, data: {original[:50]}")
                print(f"Decrypted length: {len(decrypted)}, data: {decrypted[:50]}")
                return False

    except Exception as e:
        print(f"Exception: {e}")
        return False
    finally:
        # Cleanup
        for f in [input_file, encrypted_file, decrypted_file]:
            if f and os.path.exists(f):
                try:
                    os.remove(f)
                except:
                    pass


if __name__ == "__main__":
    if test_gcm_simple():
        sys.exit(0)
    else:
        sys.exit(1)