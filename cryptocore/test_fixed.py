#!/usr/bin/env python3
"""
Исправленный тест хеш-функций
"""
import os
import sys

# Добавляем src в путь
sys.path.insert(0, 'src')

from hash.sha256 import SHA256
from hash.sha3_256 import SHA3_256

print("🧪 Тестирование ИСПРАВЛЕННЫХ хеш-функций")
print("=" * 50)


def test_sha256_correct():
    print("\n🔹 Тестирование SHA-256 (исправленный):")

    test_cases = [
        (b"", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "Пустая строка"),
        (b"abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad", "Строка 'abc'"),
        (b"hello world", "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9", "Строка 'hello world'"),
        (b"The quick brown fox jumps over the lazy dog",
         "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592",
         "Известный тест"),
        (b"The quick brown fox jumps over the lazy dog.",
         "ef537f25c895bfa782526529a9b63d97aa631564d5d789c2b765448c8635fb6c",
         "Известный тест с точкой"),
    ]

    all_passed = True
    for data, expected, description in test_cases:
        hasher = SHA256()
        result = hasher.hash(data)

        if result == expected:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            print(f"     Ожидалось: {expected}")
            print(f"     Получено:  {result}")
            all_passed = False

    return all_passed


def test_sha3_256_correct():
    print("\n🔹 Тестирование SHA3-256:")

    test_cases = [
        (b"", "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a", "Пустая строка"),
        (b"abc", "3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532", "Строка 'abc'"),
        (b"hello world", "644bcc7e564373040999aac89e7622f3ca71fba1d972fd94a31c3bfbf24e3938", "Строка 'hello world'"),
    ]

    all_passed = True
    for data, expected, description in test_cases:
        hasher = SHA3_256()
        result = hasher.hash(data)

        if result == expected:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            print(f"     Ожидалось: {expected}")
            print(f"     Получено:  {result}")
            all_passed = False

    return all_passed


def test_multiple_calls():
    print("\n🔹 Тестирование множественных вызовов:")

    hasher = SHA256()

    # Тест 1: Два отдельных вызова
    hash1 = hasher.hash(b"hello")
    hash2 = hasher.hash(b"world")

    print(f"  hash('hello'): {hash1}")
    print(f"  hash('world'): {hash2}")

    # Проверяем, что они разные
    if hash1 != hash2:
        print("  ✅ Разные вызовы дают разные результаты")
    else:
        print("  ❌ ОШИБКА: Разные входы дают одинаковый хеш!")
        return False

    # Тест 2: Инкрементальное vs одним вызовом
    hasher2 = SHA256()
    hasher2.update(b"hello")
    hasher2.update(b" ")
    hasher2.update(b"world")
    incremental_hash = hasher2.hexdigest()

    one_shot_hash = hasher.hash(b"hello world")

    print(f"  Инкрементальный: {incremental_hash}")
    print(f"  Одним вызовом:   {one_shot_hash}")

    if incremental_hash == one_shot_hash:
        print("  ✅ Инкрементальный и одним вызовом совпадают")
    else:
        print("  ❌ ОШИБКА: Не совпадают!")
        return False

    return True


def main():
    print("\n" + "=" * 50)
    print("Начало тестирования...")

    results = []

    # Тест 1: SHA-256
    try:
        sha256_ok = test_sha256_correct()
        results.append(("SHA-256 correctness", sha256_ok))
    except Exception as e:
        print(f"❌ Ошибка в тесте SHA-256: {e}")
        results.append(("SHA-256 correctness", False))

    # Тест 2: SHA3-256
    try:
        sha3_ok = test_sha3_256_correct()
        results.append(("SHA3-256 correctness", sha3_ok))
    except Exception as e:
        print(f"❌ Ошибка в тесте SHA3-256: {e}")
        results.append(("SHA3-256 correctness", False))

    # Тест 3: Множественные вызовы
    try:
        multi_ok = test_multiple_calls()
        results.append(("Multiple calls", multi_ok))
    except Exception as e:
        print(f"❌ Ошибка в тесте множественных вызовов: {e}")
        results.append(("Multiple calls", False))

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