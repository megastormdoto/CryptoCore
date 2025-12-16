# test_simple_gcm.py - ПРОСТОЙ ТЕСТ ДЛЯ GCM
import os
import sys

# Добавляем путь к src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from modes.gcm import GCM, AuthenticationError

    print("✅ GCM импортирован успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    sys.exit(1)


def test_basic_gcm():
    print("\n=== Тест 1: Базовое шифрование/дешифрование ===")

    key = bytes.fromhex('00112233445566778899aabbccddeeff')
    gcm = GCM(key)

    plaintext = b"Hello GCM World! This is a test message."
    aad = b"MyAuthData"

    print(f"Key: {key.hex()}")
    print(f"Plaintext: {plaintext}")
    print(f"AAD: {aad}")

    # Шифрование
    try:
        ciphertext = gcm.encrypt(plaintext, aad)
        print(f"\n✅ Шифрование успешно")
        print(f"Ciphertext length: {len(ciphertext)} bytes")
        print(f"Nonce (first 12 bytes): {ciphertext[:12].hex()}")
        print(f"Tag (last 16 bytes): {ciphertext[-16:].hex()}")
    except Exception as e:
        print(f"❌ Ошибка шифрования: {e}")
        return False

    # Дешифрование с правильным AAD
    try:
        gcm2 = GCM(key)
        decrypted = gcm2.decrypt(ciphertext, aad)

        if decrypted == plaintext:
            print(f"\n✅ Дешифрование успешно")
            print(f"Decrypted: {decrypted}")
            return True
        else:
            print(f"❌ Ошибка дешифрования: данные не совпадают")
            print(f"Expected: {plaintext}")
            print(f"Got: {decrypted}")
            return False

    except AuthenticationError as e:
        print(f"❌ Ошибка аутентификации: {e}")
        return False
    except Exception as e:
        print(f"❌ Ошибка дешифрования: {e}")
        return False


def test_wrong_aad():
    print("\n=== Тест 2: Неправильный AAD (должен завершиться ошибкой) ===")

    key = bytes.fromhex('00112233445566778899aabbccddeeff')
    gcm = GCM(key)

    plaintext = b"Secret message"
    correct_aad = b"CorrectAAD"
    wrong_aad = b"WrongAAD"

    # Шифруем с правильным AAD
    ciphertext = gcm.encrypt(plaintext, correct_aad)

    # Пытаемся дешифровать с неправильным AAD
    gcm2 = GCM(key)

    try:
        decrypted = gcm2.decrypt(ciphertext, wrong_aad)
        print(f"❌ ОШИБКА: Должен был завершиться с ошибкой аутентификации!")
        print(f"Получили: {decrypted}")
        return False
    except AuthenticationError:
        print("✅ Правильно завершился с ошибкой аутентификации!")
        return True
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return False


def test_nist_vector():
    print("\n=== Тест 3: NIST тестовый вектор (пустые данные) ===")

    # NIST Test Case 1: empty data
    key = bytes.fromhex('00000000000000000000000000000000')
    nonce = bytes.fromhex('000000000000000000000000')

    gcm = GCM(key, nonce)
    plaintext = b""
    aad = b""

    # Шифруем
    ciphertext = gcm.encrypt(plaintext, aad)

    # Ожидаемый тег по NIST: 58e2fccefa7e3061367f1d57a4e7455a
    expected_tag = bytes.fromhex('58e2fccefa7e3061367f1d57a4e7455a')
    actual_tag = ciphertext[-16:]  # Последние 16 байт

    print(f"Expected tag: {expected_tag.hex()}")
    print(f"Actual tag:   {actual_tag.hex()}")

    if actual_tag == expected_tag:
        print("✅ NIST тестовый вектор совпадает!")
        return True
    else:
        print("❌ NIST тестовый вектор не совпадает!")
        return False


def test_cli_compatibility():
    print("\n=== Тест 4: Совместимость с CLI ===")

    import tempfile
    import subprocess

    # Создаем тестовый файл
    test_content = b"CLI test message for GCM\nLine 2\nLine 3"
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.txt') as f:
        f.write(test_content)
        input_file = f.name

    encrypted_file = tempfile.mktemp(suffix='.bin')
    decrypted_file = tempfile.mktemp(suffix='.txt')

    key = "00112233445566778899aabbccddeeff"
    aad = "aabbccdd"

    try:
        # Шифрование через CLI
        print("1. Шифрование через CLI...")
        cmd = [
            sys.executable, 'src/cryptocore.py',
            'encrypt',
            '--key', key,
            '--input', input_file,
            '--output', encrypted_file,
            '--mode', 'gcm',
            '--aad', aad
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ CLI шифрование не удалось: {result.stderr}")
            return False
        print("✅ CLI шифрование успешно")

        # Дешифрование через CLI
        print("2. Дешифрование через CLI...")
        cmd = [
            sys.executable, 'src/cryptocore.py',
            'encrypt',
            '--decrypt',
            '--key', key,
            '--input', encrypted_file,
            '--output', decrypted_file,
            '--mode', 'gcm',
            '--aad', aad
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ CLI дешифрование не удалось: {result.stderr}")
            return False
        print("✅ CLI дешифрование успешно")

        # Сравниваем файлы
        with open(input_file, 'rb') as f1, open(decrypted_file, 'rb') as f2:
            original = f1.read()
            decrypted = f2.read()

            if original == decrypted:
                print("✅ Файлы совпадают!")
                return True
            else:
                print("❌ Файлы не совпадают!")
                return False

    except Exception as e:
        print(f"❌ Ошибка в CLI тесте: {e}")
        return False
    finally:
        # Очистка
        for f in [input_file, encrypted_file, decrypted_file]:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except:
                    pass


def main():
    print("=" * 60)
    print("ПРОСТОЙ ТЕСТ GCM РЕАЛИЗАЦИИ")
    print("=" * 60)

    results = []

    results.append(("Базовое шифрование/дешифрование", test_basic_gcm()))
    results.append(("Неправильный AAD", test_wrong_aad()))
    results.append(("NIST тестовый вектор", test_nist_vector()))
    results.append(("Совместимость с CLI", test_cli_compatibility()))

    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ ТЕСТОВ:")
    print("=" * 60)

    passed = 0
    for test_name, result in results:
        if result:
            print(f"✅ {test_name}: ПРОЙДЕНО")
            passed += 1
        else:
            print(f"❌ {test_name}: НЕ ПРОЙДЕНО")

    print(f"\nИтого: {passed}/{len(results)} тестов пройдено")

    if passed == len(results):
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! GCM работает корректно!")
        return True
    else:
        print(f"\n⚠️  {len(results) - passed} тест(ов) не пройдено")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)