#!/usr/bin/env python3
"""
Проверка импортов из src директории
"""

import sys
import os

# Добавляем src в путь
src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')
sys.path.insert(0, src_path)


def test_import_cli_parser():
    """Импорт cli_parser"""
    try:
        import cli_parser
        print("✅ cli_parser импортирован")
        assert hasattr(cli_parser, 'CLIParser')
        print("✅ CLIParser найден")
        return True
    except Exception as e:
        print(f"❌ Ошибка импорта cli_parser: {e}")
        return False


def test_import_file_io():
    """Импорт file_io"""
    try:
        import file_io
        print("✅ file_io импортирован")
        assert hasattr(file_io, 'FileIO')
        print("✅ FileIO найден")
        return True
    except Exception as e:
        print(f"❌ Ошибка импорта file_io: {e}")
        return False


def test_import_csprng():
    """Импорт csprng"""
    try:
        import csprng
        print("✅ csprng импортирован")
        assert hasattr(csprng, 'generate_random_bytes')
        assert hasattr(csprng, 'is_weak_key')
        print("✅ Функции csprng найдены")
        return True
    except Exception as e:
        print(f"❌ Ошибка импорта csprng: {e}")
        return False


def test_import_modes():
    """Импорт режимов шифрования"""
    try:
        # Проверяем существование директории modes
        modes_dir = os.path.join(src_path, 'modes')
        if os.path.exists(modes_dir):
            print("✅ Директория modes существует")

            # Проверяем основные файлы
            mode_files = ['ecb.py', 'cbc.py', 'cfb.py', 'ofb.py', 'ctr.py', 'gcm.py']
            for file in mode_files:
                file_path = os.path.join(modes_dir, file)
                if os.path.exists(file_path):
                    print(f"  ✅ {file} существует")
                else:
                    print(f"  ⚠  {file} не найден")

            return True
        else:
            print("❌ Директория modes не найдена")
            return False
    except Exception as e:
        print(f"❌ Ошибка проверки modes: {e}")
        return False


def test_import_hash():
    """Импорт хэш-функций"""
    try:
        hash_dir = os.path.join(src_path, 'hash')
        if os.path.exists(hash_dir):
            print("✅ Директория hash существует")

            hash_files = ['sha256.py', 'sha3_256.py']
            for file in hash_files:
                file_path = os.path.join(hash_dir, file)
                if os.path.exists(file_path):
                    print(f"  ✅ {file} существует")
                else:
                    print(f"  ⚠  {file} не найден")

            return True
        else:
            print("❌ Директория hash не найдена")
            return False
    except Exception as e:
        print(f"❌ Ошибка проверки hash: {e}")
        return False


def test_import_mac():
    """Импорт MAC функций"""
    try:
        mac_dir = os.path.join(src_path, 'mac')
        if os.path.exists(mac_dir):
            print("✅ Директория mac существует")

            mac_files = ['hmac.py', 'cmac.py']
            for file in mac_files:
                file_path = os.path.join(mac_dir, file)
                if os.path.exists(file_path):
                    print(f"  ✅ {file} существует")
                else:
                    print(f"  ⚠  {file} не найден")

            return True
        else:
            print("❌ Директория mac не найдена")
            return False
    except Exception as e:
        print(f"❌ Ошибка проверки mac: {e}")
        return False


def test_import_kdf():
    """Импорт KDF функций"""
    try:
        kdf_dir = os.path.join(src_path, 'kdf')
        if os.path.exists(kdf_dir):
            print("✅ Директория kdf существует")

            kdf_files = ['pbkdf2.py', 'hkdf.py']
            for file in kdf_files:
                file_path = os.path.join(kdf_dir, file)
                if os.path.exists(file_path):
                    print(f"  ✅ {file} существует")
                else:
                    print(f"  ⚠  {file} не найден")

            return True
        else:
            print("❌ Директория kdf не найдена")
            return False
    except Exception as e:
        print(f"❌ Ошибка проверки kdf: {e}")
        return False


def run_all_import_tests():
    """Запуск всех тестов импортов"""
    print("=" * 60)
    print("ПРОВЕРКА ИМПОРТОВ ИЗ SRC ДИРЕКТОРИИ")
    print("=" * 60)

    tests = [
        ("CLI Parser", test_import_cli_parser),
        ("File IO", test_import_file_io),
        ("CSPRNG", test_import_csprng),
        ("Modes", test_import_modes),
        ("Hash", test_import_hash),
        ("MAC", test_import_mac),
        ("KDF", test_import_kdf),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        print(f"\n📦 Тест: {test_name}")
        try:
            if test_func():
                print(f"   ✅ ПРОЙДЕН")
                passed += 1
            else:
                print(f"   ❌ НЕ ПРОЙДЕН")
                failed += 1
        except Exception as e:
            print(f"   💥 ОШИБКА: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"ИТОГО: {passed} пройдено, {failed} не пройдено")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = run_all_import_tests()
    sys.exit(0 if success else 1)