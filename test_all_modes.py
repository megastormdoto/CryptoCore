#!/usr/bin/env python3
"""
Test script for all encryption modes
"""

import os
import sys
import subprocess

# Добавляем путь к src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def run_command(cmd):
    """Run command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            print(f"Command failed: {cmd}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"Exception running command: {e}")
        return False


def test_mode(mode_name, test_file="test.txt"):
    """Test a specific mode"""
    print(f"\n🔍 Testing {mode_name.upper()} mode...")

    key = "00112233445566778899aabbccddeeff"
    encrypted_file = f"test_{mode_name}.enc"
    decrypted_file = f"test_{mode_name}_decrypted.txt"

    # Encryption
    encrypt_cmd = f"python main.py --algorithm aes --mode {mode_name} --encrypt --key {key} --input {test_file} --output {encrypted_file}"
    print(f"Encrypt: {encrypt_cmd}")

    if not run_command(encrypt_cmd):
        return False

    # Decryption (for modes with IV, read from file)
    if mode_name == 'ecb':
        decrypt_cmd = f"python main.py --algorithm aes --mode {mode_name} --decrypt --key {key} --input {encrypted_file} --output {decrypted_file}"
    else:
        decrypt_cmd = f"python main.py --algorithm aes --mode {mode_name} --decrypt --key {key} --input {encrypted_file} --output {decrypted_file}"

    print(f"Decrypt: {decrypt_cmd}")

    if not run_command(decrypt_cmd):
        return False

    # Verify files are identical
    try:
        with open(test_file, 'rb') as f1, open(decrypted_file, 'rb') as f2:
            original = f1.read()
            decrypted = f2.read()

            if original == decrypted:
                print(f"✅ {mode_name.upper()} SUCCESS: Files match!")
                return True
            else:
                print(f"❌ {mode_name.upper()} FAILED: Files don't match!")
                print(f"Original: {len(original)} bytes")
                print(f"Decrypted: {len(decrypted)} bytes")
                return False
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        return False


def main():
    print("🚀 Testing all CryptoCore modes...")

    # Create test file if it doesn't exist
    test_content = b"Hello CryptoCore! Testing all modes: ECB, CBC, CFB, OFB, CTR."
    with open("test.txt", "wb") as f:
        f.write(test_content)

    # Test all modes
    modes = ['ecb', 'cbc', 'cfb', 'ofb', 'ctr']
    results = {}

    for mode in modes:
        results[mode] = test_mode(mode)

    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY:")
    print("=" * 50)

    success_count = sum(results.values())
    for mode, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{mode.upper():<6}: {status}")

    print(f"\nTotal: {success_count}/{len(modes)} modes working")

    if success_count == len(modes):
        print("🎉 ALL MODES WORKING CORRECTLY!")
    else:
        print("⚠️  Some modes need attention")


if __name__ == "__main__":
    main()