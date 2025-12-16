# tests/test_gcm.py (исправленная версия для Windows)
# !/usr/bin/env python3
"""
Quick CLI test for GCM - Windows compatible version
"""
import os
import sys
import tempfile
import subprocess

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def get_main_path():
    """Get path to main.py or cryptocore.py"""
    # Check current directory and parent
    possible_paths = [
        'cryptocore.py',
        '../cryptocore.py',
        'src/cryptocore.py',
        os.path.join(os.path.dirname(__file__), '..', 'cryptocore.py'),
        os.path.join(os.path.dirname(__file__), '..', 'src', 'cryptocore.py'),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            print(f"Found: {path}")
            return os.path.abspath(path)

    print("Not found in paths:", possible_paths)
    return None


def run_command(cmd):
    """Run command with proper encoding for Windows"""
    try:
        # For Windows, set UTF-8 encoding
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'  # Ignore encoding errors
        )
        return result
    except Exception as e:
        print(f"Command execution error: {e}")
        return None


def test_cli_gcm():
    """Test GCM via CLI - Windows compatible"""
    print("=" * 60)
    print("Testing GCM CLI...")

    main_path = get_main_path()
    if not main_path:
        print("ERROR: Could not find cryptocore.py")
        return False

    print(f"Using cryptocore.py at: {main_path}")

    # Create test file
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.txt') as f:
        f.write(b"This is a secret message for GCM testing.\nLine 2.\n")
        input_file = f.name

    encrypted_file = tempfile.mktemp(suffix='.bin')
    decrypted_file = tempfile.mktemp(suffix='.txt')

    # FIXED: AAD must be hex string
    key = "00112233445566778899aabbccddeeff"
    aad = "aabbccddeeff00112233445566778899"  # Already hex, good!

    try:
        print(f"Input: {input_file}")
        print(f"Key: {key}")
        print(f"AAD (hex): {aad}")

        # Step 1: Encrypt
        print("\n1. Encrypting...")
        cmd = [
            sys.executable, main_path,
            'encrypt',
            '--key', key,
            '--input', input_file,
            '--output', encrypted_file,
            '--mode', 'gcm',
            '--aad', aad
        ]

        print(f"Running: {' '.join(cmd[:5])} ...")  # Show partial command

        result = run_command(cmd)
        if not result:
            return False

        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"stdout: {result.stdout[:200]}")
        if result.stderr:
            print(f"stderr: {result.stderr[:200]}")

        if result.returncode != 0:
            print(f"ERROR: Encryption failed with code {result.returncode}")
            return False

        print(f"SUCCESS: Encryption successful")
        print(f"Encrypted file: {encrypted_file}")

        # Check file exists and has reasonable size
        if os.path.exists(encrypted_file):
            size = os.path.getsize(encrypted_file)
            print(f"Encrypted size: {size} bytes")

            plaintext_size = os.path.getsize(input_file)
            expected_size = 12 + plaintext_size + 16
            print(f"Expected size: {expected_size} bytes")

            if size >= expected_size:
                print("SUCCESS: Size looks correct")
            else:
                print(f"WARNING: Size might be wrong")

        # Step 2: Decrypt with correct AAD
        print("\n2. Decrypting with correct AAD...")
        cmd = [
            sys.executable, main_path,
            'encrypt',
            '--decrypt',
            '--key', key,
            '--input', encrypted_file,
            '--output', decrypted_file,
            '--mode', 'gcm',
            '--aad', aad
        ]

        result = run_command(cmd)
        if not result:
            return False

        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"stdout: {result.stdout[:200]}")
        if result.stderr:
            print(f"stderr: {result.stderr[:200]}")

        if result.returncode != 0:
            print(f"ERROR: Decryption failed with code {result.returncode}")
            return False

        print(f"SUCCESS: Decryption successful")

        # Compare files
        with open(input_file, 'rb') as f:
            original = f.read()
        with open(decrypted_file, 'rb') as f:
            decrypted = f.read()

        if original == decrypted:
            print(f"SUCCESS: Decrypted content matches original")
            print(f"Original/Decrypted length: {len(original)} bytes")
        else:
            print(f"ERROR: Decrypted content does NOT match!")
            print(f"Original length: {len(original)}")
            print(f"Decrypted length: {len(decrypted)}")
            return False

        # Step 3: Try to decrypt with wrong AAD
        print("\n3. Trying to decrypt with wrong AAD (should fail)...")
        wrong_aad_file = tempfile.mktemp(suffix='.txt')
        # FIXED: Wrong AAD must also be hex
        wrong_aad = "77616e6721616164313233343536"  # Hex for "wrong!aad123456"

        cmd = [
            sys.executable, main_path,
            'encrypt',
            '--decrypt',
            '--key', key,
            '--input', encrypted_file,
            '--output', wrong_aad_file,
            '--mode', 'gcm',
            '--aad', wrong_aad  # Wrong AAD
        ]

        result = run_command(cmd)

        if result.returncode == 0:
            print(f"ERROR: Should have failed but didn't!")
            print(f"stdout: {result.stdout}")
            return False

        print(f"SUCCESS: Correctly failed with wrong AAD (return code: {result.returncode})")

        # Check that output file was NOT created
        if os.path.exists(wrong_aad_file):
            print(f"ERROR: Output file was created despite auth failure!")
            os.remove(wrong_aad_file)
            return False
        else:
            print(f"SUCCESS: Output file was NOT created (as expected)")

        print("\n" + "=" * 60)
        print("ALL CLI TESTS PASSED!")
        return True

    except Exception as e:
        print(f"\nERROR: Test error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        files_to_clean = [input_file, encrypted_file, decrypted_file]
        for f in files_to_clean:
            if f and os.path.exists(f):
                try:
                    os.remove(f)
                except:
                    pass


if __name__ == "__main__":
    # Set console encoding for Windows
    if sys.platform == "win32":
        try:
            # Try to set UTF-8 encoding
            import io

            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='ignore')
        except:
            pass

    if test_cli_gcm():
        print("\nSUCCESS: CLI GCM test PASSED")
        sys.exit(0)
    else:
        print("\nERROR: CLI GCM test FAILED")
        sys.exit(1)