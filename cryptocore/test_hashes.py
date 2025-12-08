#!/usr/bin/env python3
"""
Простой тест хеш-функций для 4-го спринта
"""
import os
import sys

# Добавляем src в путь (мы находимся в cryptocore/cryptocore/)
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

print(f"Текущая директория: {current_dir}")
print(f"Путь к src: {src_path}")
print(f"Python путь: {sys.path}")

print("\n🧪 Тестирование хеш-функций (Спринт 4)")
print("=" * 50)

try:
    # Пробуем импортировать
    print("Пробую импортировать hash.sha256...")
    from hash.sha256 import SHA256

    print("✅ SHA256 импортирован!")

    print("Пробую импортировать hash.sha3_256...")
    from hash.sha3_256 import SHA3_256

    print("✅ SHA3_256 импортирован!")

except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("\nСтруктура проекта:")

    # Проверяем существование файлов
    hash_dir = os.path.join(src_path, 'hash')
    if os.path.exists(hash_dir):
        print(f"Папка hash существует: {hash_dir}")
        print("Содержимое:")
        for item in os.listdir(hash_dir):
            print(f"  - {item}")
    else:
        print(f"Папка hash НЕ существует: {hash_dir}")

    sys.exit(1)


def test_sha256():
    print("\n🔹 Тестирование SHA-256:")

    # Создаем тестовые данные
    test_cases = [
        ("", "Пустая строка"),
        ("abc", "Строка 'abc'"),
        ("hello world", "Строка 'hello world'"),
        ("The quick brown fox jumps over the lazy dog", "Известный тест"),
    ]

    hasher = SHA256()

    for data, description in test_cases:
        if isinstance(data, str):
            data_bytes = data.encode('utf-8')
        else:
            data_bytes = data

        hash_result = hasher.hash(data_bytes)
        print(f"  {description}:")
        print(f"    Хеш: {hash_result}")
        print(f"    Длина: {len(hash_result)} символов")

    # Проверяем известный хеш для пустой строки
    empty_hash = hasher.hash(b"")
    expected_empty = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    if empty_hash == expected_empty:
        print(f"✅ Пустая строка: ПРАВИЛЬНО")
    else:
        print(f"❌ Пустая строка: ОШИБКА")
        print(f"   Ожидалось: {expected_empty}")
        print(f"   Получено:  {empty_hash}")

    return empty_hash == expected_empty


def test_sha3_256():
    print("\n🔹 Тестирование SHA3-256:")

    test_cases = [
        ("", "Пустая строка"),
        ("abc", "Строка 'abc'"),
        ("hello world", "Строка 'hello world'"),
    ]

    hasher = SHA3_256()

    for data, description in test_cases:
        if isinstance(data, str):
            data_bytes = data.encode('utf-8')
        else:
            data_bytes = data

        hash_result = hasher.hash(data_bytes)
        print(f"  {description}:")
        print(f"    Хеш: {hash_result}")
        print(f"    Длина: {len(hash_result)} символов")

    # Проверяем известный хеш для пустой строки
    empty_hash = hasher.hash(b"")
    expected_empty = "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a"

    if empty_hash == expected_empty:
        print(f"✅ Пустая строка: ПРАВИЛЬНО")
    else:
        print(f"❌ Пустая строка: ОШИБКА")
        print(f"   Ожидалось: {expected_empty}")
        print(f"   Получено:  {empty_hash}")

    return empty_hash == expected_empty


def main():
    print("\n" + "=" * 50)
    print("Начало тестирования...")

    results = []

    # Тест 1: SHA-256
    try:
        sha256_ok = test_sha256()
        results.append(("SHA-256", sha256_ok))
    except Exception as e:
        print(f"❌ Ошибка в тесте SHA-256: {e}")
        results.append(("SHA-256", False))

    # Тест 2: SHA3-256
    try:
        sha3_ok = test_sha3_256()
        results.append(("SHA3-256", sha3_ok))
    except Exception as e:
        print(f"❌ Ошибка в тесте SHA3-256: {e}")
        results.append(("SHA3-256", False))

    # Итоги
    print("\n" + "=" * 50)
    print("ИТОГИ ТЕСТИРОВАНИЯ:")
    print("=" * 50)

    all_passed = True
    for name, passed in results:
        status = "✅ ПРОЙДЕН" if passed else "❌ ПРОВАЛЕН"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
    else:
        print("💥 НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛЕНЫ")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)