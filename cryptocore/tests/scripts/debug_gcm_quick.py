# test_gcm_quick.py
# !/usr/bin/env python3
import os
import sys
import tempfile
import subprocess


def test_gcm():
    print("=== Quick GCM Test ===")

    # Создаем тестовый файл
    test_content = b"This is a test message for GCM\nLine 2\nLine 3"
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.txt') as f:
        f.write(test_content)
        input_file = f.name

    encrypted_file = tempfile.mktemp(suffix='.bin')
    decrypted_file = tempfile.mktemp(suffix='.txt')

    key = "00112233445566778899aabbccddeeff"
    correct_aad = "aabbccdd"
    wrong_aad = "ffffffff"

    try:
        # 1. Шифрование
        print("\n1. Encrypting...")
        cmd = [
            sys.executable, 'src/cryptocore.py',
            'encrypt',
            '--key', key,
            '--input', input_file,
            '--output', encrypted_file,
            '--mode', 'gcm',
            '--aad', correct_aad
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Encryption failed: {result.stderr}")
            return False
        print("✓ Encryption successful")

        # Проверяем размер зашифрованного файла
        encrypted_size = os.path.getsize(encrypted_file)
        expected_size = 12 + len(test_content) + 16  # nonce + data + tag
        print(f"  Encrypted size: {encrypted_size} bytes (expected: {expected_size})")

        # 2. Дешифрование с правильным AAD
        print("\n2. Decrypting with correct AAD...")
        cmd = [
            sys.executable, 'src/cryptocore.py',
            'encrypt',
            '--decrypt',
            '--key', key,
            '--input', encrypted_file,
            '--output', decrypted_file,
            '--mode', 'gcm',
            '--aad', correct_aad
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Decryption failed: {result.stderr}")
            return False

        # Проверяем содержимое
        with open(decrypted_file, 'rb') as f:
            decrypted = f.read()

        if decrypted == test_content:
            print("✓ Decryption successful (content matches)")
        else:
            print(f"✗ Decryption failed (content mismatch)")
            print(f"  Original: {test_content}")
            print(f"  Decrypted: {decrypted}")
            return False

        # 3. Дешифрование с неправильным AAD (должно завершиться ошибкой)
        print("\n3. Decrypting with wrong AAD (should fail)...")
        wrong_output = tempfile.mktemp(suffix='.txt')
        cmd = [
            sys.executable, 'src/cryptocore.py',
            'encrypt',
            '--decrypt',
            '--key', key,
            '--input', encrypted_file,
            '--output', wrong_output,
            '--mode', 'gcm',
            '--aad', wrong_aad
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        # Должен вернуть ненулевой код возврата
        if result.returncode == 0:
            print("✗ Should have failed with wrong AAD!")
            return False
        else:
            print("✓ Correctly failed with wrong AAD")

        # Проверяем, что выходной файл не создан
        if os.path.exists(wrong_output):
            print("✗ Output file was created (should have been deleted)")
            os.remove(wrong_output)
            return False
        else:
            print("✓ Output file was not created (correct)")

        print("\n=== All tests passed! ===")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        # Удаляем временные файлы
        for f in [input_file, encrypted_file, decrypted_file]:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except:
                    pass


if __name__ == "__main__":
    if test_gcm():
        sys.exit(0)
    else:
        sys.exit(1)