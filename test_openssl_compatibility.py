#!/usr/bin/env python3
"""
OpenSSL Compatibility Tests for CryptoCore
"""

import os
import subprocess
import sys

# Добавляем путь к OpenSSL в PATH для subprocess
openssl_path = r"C:\Program Files\OpenSSL-Win64\bin"
os.environ['PATH'] = openssl_path + ";" + os.environ['PATH']


def run_command(cmd, description=""):
    """Run command and return success status"""
    if description:
        print(f"\n🔧 {description}")
        print(f"   Command: {cmd}")

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout
        else:
            print(f"   ❌ Failed: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False, str(e)


def test_openssl_compatibility(mode, test_file="test_openssl.txt"):
    """Test interoperability with OpenSSL for a specific mode"""
    print(f"\n🔍 Testing {mode.upper()} mode OpenSSL compatibility...")

    # Create test file
    test_content = f"OpenSSL compatibility test for {mode} mode"
    with open(test_file, "wb") as f:
        f.write(test_content.encode())

    key = "00112233445566778899aabbccddeeff"
    iv = "aabbccddeeff00112233445566778899"

    # 1. Encrypt with CryptoCore, decrypt with OpenSSL
    print("   1. CryptoCore → OpenSSL:")

    # Encrypt with CryptoCore
    crypto_encrypted = f"cryptocore_{mode}.enc"
    success, _ = run_command(
        f'python main.py --algorithm aes --mode {mode} --encrypt '
        f'--key {key} --input {test_file} --output {crypto_encrypted}',
        "Encrypt with CryptoCore"
    )

    if not success:
        return False

    # For modes with IV, handle IV extraction
    if mode != 'ecb':
        # Read the encrypted file to extract IV (first 16 bytes)
        with open(crypto_encrypted, 'rb') as f:
            data = f.read()
            iv_from_file = data[:16].hex()
            ciphertext_only = data[16:]

        # Write ciphertext without IV for OpenSSL
        ciphertext_file = f"ciphertext_{mode}.bin"
        with open(ciphertext_file, 'wb') as f:
            f.write(ciphertext_only)

        # Decrypt with OpenSSL using IV from file
        openssl_decrypted = f"openssl_decrypted_{mode}.txt"
        success, _ = run_command(
            f'openssl enc -aes-128-{mode} -d -K {key} -iv {iv_from_file} '
            f'-in {ciphertext_file} -out {openssl_decrypted}',
            "Decrypt with OpenSSL"
        )
    else:
        # ECB mode - no IV
        openssl_decrypted = f"openssl_decrypted_{mode}.txt"
        success, _ = run_command(
            f'openssl enc -aes-128-{mode} -d -K {key} '
            f'-in {crypto_encrypted} -out {openssl_decrypted}',
            "Decrypt with OpenSSL"
        )

    if success:
        # Compare files
        try:
            with open(test_file, 'rb') as f1, open(openssl_decrypted, 'rb') as f2:
                if f1.read() == f2.read():
                    print("   ✅ CryptoCore → OpenSSL: SUCCESS")
                else:
                    print("   ❌ CryptoCore → OpenSSL: Files differ!")
                    return False
        except FileNotFoundError:
            print("   ❌ Output file not found")
            return False
    else:
        return False

    # 2. Encrypt with OpenSSL, decrypt with CryptoCore
    print("   2. OpenSSL → CryptoCore:")

    # Encrypt with OpenSSL
    openssl_encrypted = f"openssl_{mode}.enc"
    if mode != 'ecb':
        success, _ = run_command(
            f'openssl enc -aes-128-{mode} -K {key} -iv {iv} '
            f'-in {test_file} -out {openssl_encrypted}',
            "Encrypt with OpenSSL"
        )
    else:
        success, _ = run_command(
            f'openssl enc -aes-128-{mode} -K {key} '
            f'-in {test_file} -out {openssl_encrypted}',
            "Encrypt with OpenSSL"
        )

    if not success:
        return False

    # Decrypt with CryptoCore
    cryptocore_decrypted = f"cryptocore_decrypted_{mode}.txt"
    if mode != 'ecb':
        success, _ = run_command(
            f'python main.py --algorithm aes --mode {mode} --decrypt '
            f'--key {key} --iv {iv} --input {openssl_encrypted} --output {cryptocore_decrypted}',
            "Decrypt with CryptoCore"
        )
    else:
        success, _ = run_command(
            f'python main.py --algorithm aes --mode {mode} --decrypt '
            f'--key {key} --input {openssl_encrypted} --output {cryptocore_decrypted}',
            "Decrypt with CryptoCore"
        )

    if success:
        # Compare files
        try:
            with open(test_file, 'rb') as f1, open(cryptocore_decrypted, 'rb') as f2:
                if f1.read() == f2.read():
                    print("   ✅ OpenSSL → CryptoCore: SUCCESS")
                    return True
                else:
                    print("   ❌ OpenSSL → CryptoCore: Files differ!")
                    return False
        except FileNotFoundError:
            print("   ❌ Output file not found")
            return False

    return False


def main():
    print("🚀 Testing OpenSSL Compatibility...")
    print("=" * 50)

    # Check if OpenSSL is installed
    success, version = run_command("openssl version", "Checking OpenSSL installation")
    if not success:
        print("❌ OpenSSL is not installed or not in PATH")
        print("   Please install OpenSSL and try again")
        return

    print(f"   OpenSSL version: {version.strip()}")

    # Test ALL modes
    modes = ['ecb', 'cbc', 'cfb', 'ofb', 'ctr']

    results = {}
    for mode in modes:
        results[mode] = test_openssl_compatibility(mode)

    # Summary
    print("\n" + "=" * 50)
    print("📊 OPENSSL COMPATIBILITY SUMMARY:")
    print("=" * 50)

    success_count = sum(results.values())
    for mode, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{mode.upper():<6}: {status}")

    print(f"\nOpenSSL Compatibility: {success_count}/{len(modes)} modes")

    if success_count == len(modes):
        print("🎉 FULL OPENSSL COMPATIBILITY ACHIEVED!")
        print("   All requirements for Sprint 2 are COMPLETED! 🚀")
    else:
        print("⚠️  Some modes need OpenSSL compatibility fixes")

    # Cleanup - НЕ УДАЛЯЕМ САМ ТЕСТОВЫЙ ФАЙЛ!
    print("\n🧹 Cleaning up TEMPORARY test files...")
    temp_files_to_remove = [
        "test_openssl.txt",  # Удаляем тестовый контент
        "cryptocore_*.enc", "openssl_*.enc",  # Удаляем зашифрованные файлы
        "ciphertext_*.bin",  # Удаляем ciphertext
        "openssl_decrypted_*.txt", "cryptocore_decrypted_*.txt"  # Удаляем расшифрованные
    ]

    for pattern in temp_files_to_remove:
        for file in os.listdir('.'):
            if any(file.startswith(prefix.replace('*', '')) for prefix in [
                "test_openssl", "cryptocore_", "openssl_",
                "ciphertext_", "openssl_decrypted_", "cryptocore_decrypted_"
            ]):
                # НИКОГДА не удаляем сам тестовый скрипт!
                if file != "test_openssl_compatibility.py" and file != "backup_openssl_test.py":
                    try:
                        os.remove(file)
                        print(f"   Removed: {file}")
                    except:
                        pass


if __name__ == "__main__":
    main()