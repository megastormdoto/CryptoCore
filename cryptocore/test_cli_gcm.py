#!/usr/bin/env python3
"""
Quick CLI test for GCM
"""
import os
import sys
import tempfile
import subprocess

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_cli_gcm():
    """Test GCM via CLI"""
    print("🔧 Testing GCM CLI...")

    # Create test file
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.txt') as f:
        f.write(b"This is a secret message for GCM testing.\nLine 2.\n")
        input_file = f.name

    encrypted_file = tempfile.mktemp(suffix='.bin')
    decrypted_file = tempfile.mktemp(suffix='.txt')

    key = "00112233445566778899aabbccddeeff"
    aad = "aabbccddeeff00112233445566778899"

    try:
        print(f"Input: {input_file}")
        print(f"Key: {key}")
        print(f"AAD: {aad}")

        # Step 1: Encrypt
        print("\n1. Encrypting...")
        result = subprocess.run([
            sys.executable, '-m', 'src.main',
            'encrypt',
            '--key', key,
            '--input', input_file,
            '--output', encrypted_file,
            '--mode', 'gcm',
            '--aad', aad
        ], capture_output=True, text=True)

        print(f"   stdout: {result.stdout[:100]}...")
        if result.stderr:
            print(f"   stderr: {result.stderr[:200]}")

        if result.returncode != 0:
            print(f"   ❌ Encryption failed with code {result.returncode}")
            return False

        print(f"   ✅ Encryption successful")
        print(f"   Encrypted file: {encrypted_file}")

        # Check file exists and has reasonable size
        if os.path.exists(encrypted_file):
            size = os.path.getsize(encrypted_file)
            print(f"   Encrypted size: {size} bytes")

            # Should be: 12 (nonce) + plaintext + 16 (tag)
            plaintext_size = os.path.getsize(input_file)
            expected_size = 12 + plaintext_size + 16
            print(f"   Expected size: {expected_size} bytes")

            if size >= expected_size:
                print("   ✅ Size looks correct")
            else:
                print(f"   ⚠️  Size might be wrong")

        # Step 2: Decrypt with correct AAD
        print("\n2. Decrypting with correct AAD...")
        result = subprocess.run([
            sys.executable, '-m', 'src.main',
            'encrypt',
            '--decrypt',
            '--key', key,
            '--input', encrypted_file,
            '--output', decrypted_file,
            '--mode', 'gcm',
            '--aad', aad
        ], capture_output=True, text=True)

        print(f"   stdout: {result.stdout[:100]}...")
        if result.stderr:
            print(f"   stderr: {result.stderr[:200]}")

        if result.returncode != 0:
            print(f"   ❌ Decryption failed with code {result.returncode}")
            return False

        print(f"   ✅ Decryption successful")

        # Compare files
        with open(input_file, 'rb') as f:
            original = f.read()
        with open(decrypted_file, 'rb') as f:
            decrypted = f.read()

        if original == decrypted:
            print(f"   ✅ Decrypted content matches original")
        else:
            print(f"   ❌ Decrypted content does NOT match!")
            print(f"   Original length: {len(original)}")
            print(f"   Decrypted length: {len(decrypted)}")
            return False

        # Step 3: Try to decrypt with wrong AAD
        print("\n3. Trying to decrypt with wrong AAD (should fail)...")
        wrong_aad_file = tempfile.mktemp(suffix='.txt')
        result = subprocess.run([
            sys.executable, '-m', 'src.main',
            'encrypt',
            '--decrypt',
            '--key', key,
            '--input', encrypted_file,
            '--output', wrong_aad_file,
            '--mode', 'gcm',
            '--aad', 'wrongaad1234567890abcdef'  # Wrong AAD
        ], capture_output=True, text=True)

        print(f"   stdout: {result.stdout[:100]}...")
        if result.stderr:
            print(f"   stderr: {result.stderr[:200]}")

        if result.returncode == 0:
            print(f"   ❌ Should have failed but didn't!")
            return False

        print(f"   ✅ Correctly failed with wrong AAD")

        # Check that output file was NOT created
        if os.path.exists(wrong_aad_file):
            print(f"   ❌ Output file was created despite auth failure!")
            os.remove(wrong_aad_file)
            return False
        else:
            print(f"   ✅ Output file was NOT created (as expected)")

        print("\n🎉 All CLI tests passed!")
        return True

    except Exception as e:
        print(f"\n❌ Test error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        for f in [input_file, encrypted_file, decrypted_file]:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except:
                    pass


if __name__ == "__main__":
    print("=" * 60)
    if test_cli_gcm():
        print("\n✅ CLI GCM test PASSED")
        sys.exit(0)
    else:
        print("\n❌ CLI GCM test FAILED")
        sys.exit(1)