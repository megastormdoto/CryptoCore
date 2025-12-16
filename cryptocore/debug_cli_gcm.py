# debug_cli_gcm.py - положи в корень проекта
import os
import sys
import tempfile
import subprocess

print("=== ОТЛАДКА CLI GCM ПРОБЛЕМЫ ===")

# Определяем путь к cryptocore.py
if os.path.exists('src/cryptocore.py'):
    cryptocore_path = 'src/cryptocore.py'
elif os.path.exists('cryptocore.py'):
    cryptocore_path = 'cryptocore.py'
else:
    print("❌ Не могу найти cryptocore.py")
    sys.exit(1)

print(f"Использую: {cryptocore_path}")

# Создаем тестовый файл
test_content = b"Debug test message"
with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.txt') as f:
    f.write(test_content)
    input_file = f.name

encrypted_file = tempfile.mktemp(suffix='.bin')
decrypted_file = tempfile.mktemp(suffix='.txt')

key = "00112233445566778899aabbccddeeff"
aad = "aabbccdd"

try:
    # 1. Шифрование через CLI с максимальной отладкой
    print("\n1. ШИФРОВАНИЕ через CLI:")
    cmd = [
        sys.executable, cryptocore_path,
        'encrypt',
        '--key', key,
        '--input', input_file,
        '--output', encrypted_file,
        '--mode', 'gcm',
        '--aad', aad
    ]

    print(f"Команда: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    print(f"Код возврата: {result.returncode}")

    if result.stdout:
        print(f"Вывод:\n{result.stdout[:500]}...")
    if result.stderr:
        print(f"Ошибки:\n{result.stderr}")

    if result.returncode != 0:
        print("❌ Шифрование не удалось")
    else:
        print("✅ Шифрование успешно")

        # Проверяем зашифрованный файл
        if os.path.exists(encrypted_file):
            with open(encrypted_file, 'rb') as f:
                encrypted_data = f.read()

            print(f"\nЗашифрованный файл: {len(encrypted_data)} байт")
            print(f"Nonce (первые 12 байт): {encrypted_data[:12].hex()}")
            print(f"Тег (последние 16 байт): {encrypted_data[-16:].hex()}")
            print(f"Данные между nonce и тегом: {len(encrypted_data) - 28} байт")

            # 2. Пробуем дешифровать ПРЯМО в Python (без CLI)
            print("\n2. ДЕШИФРОВАНИЕ ПРЯМО в Python:")

            # Добавляем путь к src
            sys.path.insert(0, 'src')
            try:
                from modes.gcm import GCM, AuthenticationError

                print("✅ GCM импортирован")
            except ImportError as e:
                print(f"❌ Ошибка импорта GCM: {e}")
                sys.exit(1)

            key_bytes = bytes.fromhex(key)
            aad_bytes = bytes.fromhex(aad)

            print(f"Key: {key_bytes.hex()}")
            print(f"AAD: {aad_bytes.hex()}")
            print(f"Nonce из файла: {encrypted_data[:12].hex()}")

            # Пробуем дешифровать БЕЗ передачи nonce в конструктор
            print("\nПопытка 1: Дешифрование БЕЗ nonce в конструкторе:")
            gcm1 = GCM(key_bytes, None)
            try:
                decrypted1 = gcm1.decrypt(encrypted_data, aad_bytes)
                print(f"✅ Дешифрование без nonce успешно!")
                print(f"Результат: {decrypted1}")
                if decrypted1 == test_content:
                    print("✅ Данные совпадают!")
                else:
                    print(f"❌ Данные не совпадают!")
            except AuthenticationError as e:
                print(f"❌ Ошибка аутентификации: {e}")

            # Пробуем дешифровать С передачей nonce в конструктор
            print("\nПопытка 2: Дешифрование С nonce в конструкторе:")
            gcm2 = GCM(key_bytes, encrypted_data[:12])
            try:
                decrypted2 = gcm2.decrypt(encrypted_data, aad_bytes)
                print(f"✅ Дешифрование с nonce успешно!")
                print(f"Результат: {decrypted2}")
            except AuthenticationError as e:
                print(f"❌ Ошибка аутентификации: {e}")

            # 3. Дешифрование через CLI
            print("\n3. ДЕШИФРОВАНИЕ через CLI:")
            cmd = [
                sys.executable, cryptocore_path,
                'encrypt',
                '--decrypt',
                '--key', key,
                '--input', encrypted_file,
                '--output', decrypted_file,
                '--mode', 'gcm',
                '--aad', aad
            ]

            print(f"Команда: {' '.join(cmd)}")

            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
            print(f"Код возврата: {result.returncode}")

            if result.stdout:
                print(f"Вывод:\n{result.stdout[:500]}...")
            if result.stderr:
                print(f"Ошибки:\n{result.stderr}")

            if result.returncode == 0:
                # Сравниваем файлы
                if os.path.exists(decrypted_file):
                    with open(input_file, 'rb') as f1, open(decrypted_file, 'rb') as f2:
                        original = f1.read()
                        decrypted_cli = f2.read()

                        if original == decrypted_cli:
                            print("✅ CLI дешифрование успешно!")
                        else:
                            print("❌ CLI дешифрование: файлы не совпадают")
                else:
                    print("❌ CLI не создал выходной файл")
            else:
                print("❌ CLI дешифрование не удалось")
        else:
            print("❌ Зашифрованный файл не создан")

finally:
    # Очистка
    for f in [input_file, encrypted_file, decrypted_file]:
        if f and os.path.exists(f):
            try:
                os.remove(f)
            except:
                pass