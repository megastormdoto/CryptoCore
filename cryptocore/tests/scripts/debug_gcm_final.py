# tests/test_gcm_final.py
# !/usr/bin/env python3
"""
Final GCM test - Windows compatible
"""
import os
import sys
import tempfile
import subprocess


def clean_output(text):
    """Clean Unicode characters for Windows"""
    if not text:
        return text
    # Replace common Unicode symbols
    replacements = {
        '✓': '[OK]',
        '✗': '[ERROR]',
        '🔧': '[TEST]',
        '🧪': '[TEST]',
        '🎉': '[SUCCESS]',
        '⚠️': '[WARNING]',
        '🔑': '[KEY]',
        '📁': '[FILE]',
        '🔒': '[LOCK]',
        '🔓': '[UNLOCK]',
        '–': '-',
        '—': '-',
        '…': '...',
    }
    for uni, ascii in replacements.items():
        text = text.replace(uni, ascii)
    return text


def run_test():
    print("=" * 70)
    print("GCM FINAL TEST - Windows Edition")
    print("=" * 70)

    # Find cryptocore.py
    script = 'src/cryptocore.py'
    if not os.path.exists(script):
        print(f"ERROR: {script} not found")
        return False

    print(f"Using: {os.path.abspath(script)}")

    # Create test files
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.txt') as f:
        f.write(b"This is a test message for GCM.\nWith multiple lines.\n")
        input_file = f.name

    encrypted_file = tempfile.mktemp(suffix='.bin')
    decrypted_file = tempfile.mktemp(suffix='.txt')

    # Test data
    key = "00112233445566778899aabbccddeeff"
    aad = "aabbccdd"
    wrong_aad = "ffffffff"

    all_passed = True

    try:
        # TEST 1: Encryption
        print("\n" + "-" * 70)
        print("TEST 1: GCM Encryption")
        print("-" * 70)

        cmd = [
            sys.executable, script,
            'encrypt',
            '--key', key,
            '--input', input_file,
            '--output', encrypted_file,
            '--mode', 'gcm',
            '--aad', aad
        ]

        print(f"Command: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        print(f"Return code: {result.returncode}")

        if result.stdout:
            cleaned = clean_output(result.stdout)
            print(f"Output:\n{cleaned[:500]}")

        if result.returncode != 0:
            print(f"ERROR: Encryption failed")
            if result.stderr:
                print(f"Stderr: {clean_output(result.stderr)}")
            all_passed = False
        else:
            print("SUCCESS: Encryption passed")

            # Check file size
            if os.path.exists(encrypted_file):
                size = os.path.getsize(encrypted_file)
                input_size = os.path.getsize(input_file)
                print(f"Input size: {input_size} bytes")
                print(f"Encrypted size: {size} bytes")
                print(f"Expected min size: {12 + input_size + 16} = {12 + input_size + 16} bytes")

        # TEST 2: Decryption with correct AAD
        if all_passed and os.path.exists(encrypted_file):
            print("\n" + "-" * 70)
            print("TEST 2: GCM Decryption with correct AAD")
            print("-" * 70)

            cmd = [
                sys.executable, script,
                'encrypt',
                '--decrypt',
                '--key', key,
                '--input', encrypted_file,
                '--output', decrypted_file,
                '--mode', 'gcm',
                '--aad', aad
            ]

            print(f"Command: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )

            print(f"Return code: {result.returncode}")

            if result.stdout:
                cleaned = clean_output(result.stdout)
                print(f"Output:\n{cleaned[:500]}")

            if result.returncode != 0:
                print(f"ERROR: Decryption failed")
                if result.stderr:
                    print(f"Stderr: {clean_output(result.stderr)}")
                all_passed = False
            else:
                print("SUCCESS: Decryption passed")

                # Compare files
                with open(input_file, 'rb') as f1, open(decrypted_file, 'rb') as f2:
                    original = f1.read()
                    decrypted = f2.read()

                    if original == decrypted:
                        print(f"SUCCESS: Decrypted content matches original")
                        print(f"Content: {original[:50]}...")
                    else:
                        print(f"ERROR: Content mismatch!")
                        all_passed = False

        # TEST 3: Decryption with wrong AAD (should fail)
        if all_passed and os.path.exists(encrypted_file):
            print("\n" + "-" * 70)
            print("TEST 3: GCM Decryption with WRONG AAD (should fail)")
            print("-" * 70)

            wrong_output = tempfile.mktemp(suffix='.txt')

            cmd = [
                sys.executable, script,
                'encrypt',
                '--decrypt',
                '--key', key,
                '--input', encrypted_file,
                '--output', wrong_output,
                '--mode', 'gcm',
                '--aad', wrong_aad
            ]

            print(f"Command: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )

            print(f"Return code: {result.returncode}")

            # For this test, non-zero return code is SUCCESS
            if result.returncode == 0:
                print(f"ERROR: Should have failed with wrong AAD but didn't!")
                all_passed = False
            else:
                print(f"SUCCESS: Correctly failed with wrong AAD")

                # Check that output file was NOT created
                if os.path.exists(wrong_output):
                    print(f"WARNING: Output file was created despite auth failure")
                    os.remove(wrong_output)
                else:
                    print(f"SUCCESS: Output file was not created (as expected)")

            # Clean up
            if os.path.exists(wrong_output):
                os.remove(wrong_output)

        # TEST 4: Decryption with wrong key (should fail)
        if all_passed and os.path.exists(encrypted_file):
            print("\n" + "-" * 70)
            print("TEST 4: GCM Decryption with WRONG KEY (should fail)")
            print("-" * 70)

            wrong_key_output = tempfile.mktemp(suffix='.txt')
            wrong_key = "ffffffffffffffffffffffffffffffff"

            cmd = [
                sys.executable, script,
                'encrypt',
                '--decrypt',
                '--key', wrong_key,
                '--input', encrypted_file,
                '--output', wrong_key_output,
                '--mode', 'gcm',
                '--aad', aad
            ]

            print(f"Command: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )

            print(f"Return code: {result.returncode}")

            # Should fail
            if result.returncode == 0:
                print(f"ERROR: Should have failed with wrong key but didn't!")
                all_passed = False
            else:
                print(f"SUCCESS: Correctly failed with wrong key")

            # Clean up
            if os.path.exists(wrong_key_output):
                os.remove(wrong_key_output)

    except Exception as e:
        print(f"\nEXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        all_passed = False
    finally:
        # Cleanup
        for f in [input_file, encrypted_file, decrypted_file]:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except:
                    pass

    # Final result
    print("\n" + "=" * 70)
    print("FINAL RESULT")
    print("=" * 70)

    if all_passed:
        print("[SUCCESS] ALL GCM TESTS PASSED!")
        print("\nGCM implementation correctly:")
        print("1. Encrypts data")
        print("2. Decrypts with correct key/AAD")
        print("3. Fails with wrong AAD")
        print("4. Fails with wrong key")
        print("\nThis meets Sprint 6 requirements for AEAD!")
        return True
    else:
        print("[ERROR] Some tests failed")
        return False


if __name__ == "__main__":
    # Fix encoding for Windows
    if sys.platform == "win32":
        try:
            import io

            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        except:
            pass

    success = run_test()
    sys.exit(0 if success else 1)