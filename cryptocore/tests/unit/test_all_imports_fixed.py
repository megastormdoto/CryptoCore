#!/usr/bin/env python3
"""
Проверка импортов всех модулей проекта
"""

import sys
import os
import importlib.util

# Добавляем src в путь
src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')
sys.path.insert(0, src_path)


def import_module(module_name, file_path):
    """Импортирует модуль из файла"""
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        return e


def test_basic_imports():
    """Тест импорта основных модулей"""
    print("=" * 60)
    print("ТЕСТ ИМПОРТОВ ОСНОВНЫХ МОДУЛЕЙ")
    print("=" * 60)

    basic_modules = [
        ('cryptocore', 'cryptocore.py'),
        ('cli_parser', 'cli_parser.py'),
        ('file_io', 'file_io.py'),
        ('csprng', 'csprng.py'),
        ('main', 'main.py'),
    ]

    passed = 0
    failed = 0

    for module_name, file_name in basic_modules:
        file_path = os.path.join(src_path, file_name)

        if not os.path.exists(file_path):
            print(f"❌ {module_name}: файл {file_name} не найден")
            failed += 1
            continue

        result = import_module(module_name, file_path)

        if isinstance(result, Exception):
            print(f"❌ {module_name}: ошибка импорта - {result}")
            failed += 1
        else:
            print(f"✅ {module_name}: успешно импортирован")
            passed += 1

    return passed, failed


def test_ciphers_imports():
    """Тест импорта шифров"""
    print("\n" + "=" * 60)
    print("ТЕСТ ИМПОРТОВ ШИФРОВ")
    print("=" * 60)

    ciphers_dir = os.path.join(src_path, 'ciphers')

    if not os.path.exists(ciphers_dir):
        print("❌ Директория ciphers не найдена")
        return 0, 1

    ciphers_modules = [
        ('aes', 'aes.py'),
    ]

    passed = 0
    failed = 0

    for module_name, file_name in ciphers_modules:
        file_path = os.path.join(ciphers_dir, file_name)

        if not os.path.exists(file_path):
            print(f"❌ {module_name}: файл {file_name} не найден")
            failed += 1
            continue

        result = import_module(module_name, file_path)

        if isinstance(result, Exception):
            print(f"❌ {module_name}: ошибка импорта - {result}")
            failed += 1
        else:
            print(f"✅ {module_name}: успешно импортирован")
            passed += 1

    return passed, failed


def test_hash_imports():
    """Тест импорта хэш-функций"""
    print("\n" + "=" * 60)
    print("ТЕСТ ИМПОРТОВ ХЭШ-ФУНКЦИЙ")
    print("=" * 60)

    hash_dir = os.path.join(src_path, 'hash')

    if not os.path.exists(hash_dir):
        print("❌ Директория hash не найдена")
        return 0, 1

    hash_modules = [
        ('sha256', 'sha256.py'),
        ('sha3_256', 'sha3_256.py'),
    ]

    passed = 0
    failed = 0

    for module_name, file_name in hash_modules:
        file_path = os.path.join(hash_dir, file_name)

        if not os.path.exists(file_path):
            print(f"❌ {module_name}: файл {file_name} не найден")
            failed += 1
            continue

        result = import_module(module_name, file_path)

        if isinstance(result, Exception):
            print(f"❌ {module_name}: ошибка импорта - {result}")
            failed += 1
        else:
            print(f"✅ {module_name}: успешно импортирован")
            passed += 1

    return passed, failed


def test_modes_imports():
    """Тест импорта режимов шифрования"""
    print("\n" + "=" * 60)
    print("ТЕСТ ИМПОРТОВ РЕЖИМОВ ШИФРОВАНИЯ")
    print("=" * 60)

    modes_dir = os.path.join(src_path, 'modes')

    if not os.path.exists(modes_dir):
        print("❌ Директория modes не найдена")
        return 0, 1

    modes_modules = [
        ('ecb', 'ecb.py'),
        ('cbc', 'cbc.py'),
        ('cfb', 'cfb.py'),
        ('ofb', 'ofb.py'),
        ('ctr', 'ctr.py'),
        ('gcm', 'gcm.py'),
        ('aead', 'aead.py'),
        ('base', 'base.py'),
    ]

    passed = 0
    failed = 0

    for module_name, file_name in modes_modules:
        file_path = os.path.join(modes_dir, file_name)

        if not os.path.exists(file_path):
            print(f"⚠  {module_name}: файл {file_name} не найден")
            continue

        result = import_module(module_name, file_path)

        if isinstance(result, Exception):
            print(f"❌ {module_name}: ошибка импорта - {result}")
            failed += 1
        else:
            print(f"✅ {module_name}: успешно импортирован")
            passed += 1

    return passed, failed


def test_mac_imports():
    """Тест импорта MAC функций"""
    print("\n" + "=" * 60)
    print("ТЕСТ ИМПОРТОВ MAC ФУНКЦИЙ")
    print("=" * 60)

    mac_dir = os.path.join(src_path, 'mac')

    if not os.path.exists(mac_dir):
        print("❌ Директория mac не найдена")
        return 0, 1

    mac_modules = [
        ('hmac', 'hmac.py'),
        ('cmac', 'cmac.py'),
    ]

    passed = 0
    failed = 0

    for module_name, file_name in mac_modules:
        file_path = os.path.join(mac_dir, file_name)

        if not os.path.exists(file_path):
            print(f"⚠  {module_name}: файл {file_name} не найден")
            continue

        result = import_module(module_name, file_path)

        if isinstance(result, Exception):
            print(f"❌ {module_name}: ошибка импорта - {result}")
            failed += 1
        else:
            print(f"✅ {module_name}: успешно импортирован")
            passed += 1

    return passed, failed


def test_kdf_imports():
    """Тест импорта KDF функций"""
    print("\n" + "=" * 60)
    print("ТЕСТ ИМПОРТОВ KDF ФУНКЦИЙ")
    print("=" * 60)

    kdf_dir = os.path.join(src_path, 'kdf')

    if not os.path.exists(kdf_dir):
        print("❌ Директория kdf не найдена")
        return 0, 1

    kdf_modules = [
        ('pbkdf2', 'pbkdf2.py'),
        ('hkdf', 'hkdf.py'),
    ]

    passed = 0
    failed = 0

    for module_name, file_name in kdf_modules:
        file_path = os.path.join(kdf_dir, file_name)

        if not os.path.exists(file_path):
            print(f"⚠  {module_name}: файл {file_name} не найден")
            continue

        result = import_module(module_name, file_path)

        if isinstance(result, Exception):
            print(f"❌ {module_name}: ошибка импорта - {result}")
            failed += 1
        else:
            print(f"✅ {module_name}: успешно импортирован")
            passed += 1

    return passed, failed


def main():
    """Основная функция"""
    print("🚀 ПОЛНАЯ ПРОВЕРКА ИМПОРТОВ ПРОЕКТА")

    total_passed = 0
    total_failed = 0

    # Запускаем все тесты импортов
    test_functions = [
        test_basic_imports,
        test_ciphers_imports,
        test_hash_imports,
        test_modes_imports,
        test_mac_imports,
        test_kdf_imports,
    ]

    for test_func in test_functions:
        passed, failed = test_func()
        total_passed += passed
        total_failed += failed

    print("\n" + "=" * 60)
    print("ИТОГИ:")
    print("=" * 60)
    print(f"Всего успешных импортов: {total_passed}")
    print(f"Всего неудачных импортов: {total_failed}")
    print(f"Общее количество: {total_passed + total_failed}")

    if total_failed == 0:
        print("\n🎉 ВСЕ ИМПОРТЫ УСПЕШНЫ!")
    else:
        print(f"\n⚠  Есть проблемы с {total_failed} импортами")

    return total_failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)