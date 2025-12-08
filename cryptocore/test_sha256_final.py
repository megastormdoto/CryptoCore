#!/usr/bin/env python3
"""
Финальный тест SHA-256
"""
import sys
import os
import hashlib

sys.path.insert(0, 'src')

# Попробуй импортировать исправленную версию
try:
    from hash.sha256 import SHA256

    print("✅ Исправленная SHA256 импортирована")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    sys.exit(1)


def test_basic():
    print("\n🔹 Базовые тесты:")

    hasher = SHA256()

    # Тест 1: Пустая строка
    empty_hash = hasher.hash(b"")
    expected_empty = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    print(f"  Пустая строка: {empty_hash == expected_empty}")
    if not empty_hash == expected_empty:
        print(f"    Наша: {empty_hash}")
        print(f"    Ожидалось: {expected_empty}")

    # Тест 2: 'abc'
    abc_hash = hasher.hash(b"abc")
    expected_abc = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"

    print(f"  'abc': {abc_hash == expected_abc}")
    if not abc_hash == expected_abc:
        print(f"    Наша: {abc_hash}")
        print(f"    Ожидалось: {expected_abc}")

    # Тест 3: 'hello world'
    hw_hash = hasher.hash(b"hello world")
    expected_hw = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"

    print(f"  'hello world': {hw_hash == expected_hw}")

    return all([
        empty_hash == expected_empty,
        abc_hash == expected_abc,
        hw_hash == expected_hw
    ])


def test_with_hashlib():
    print("\n🔹 Сравнение с hashlib:")

    test_strings = [
        "",
        "a",
        "ab",
        "abc",
        "abcd",
        "abcde",
        "hello",
        "hello world",
        "The quick brown fox",
        "The quick brown fox jumps over the lazy dog",
    ]

    all_match = True
    for s in test_strings:
        data = s.encode('utf-8')

        # Наша реализация
        hasher = SHA256()
        our_hash = hasher.hash(data)

        # hashlib
        lib_hash = hashlib.sha256(data).hexdigest()

        match = our_hash == lib_hash
        all_match = all_match and match

        status = "✅" if match else "❌"
        print(f"  {status} '{s[:20]}{'...' if len(s) > 20 else ''}': {match}")

        if not match:
            print(f"    Наша:  {our_hash}")
            print(f"    Библиотека: {lib_hash}")

    return all_match


def test_incremental():
    print("\n🔹 Инкрементальное хеширование:")

    # Тест 1: 'hello' + ' ' + 'world' должно быть равно 'hello world'
    hasher1 = SHA256()
    hasher1.update(b"hello")
    hasher1.update(b" ")
    hasher1.update(b"world")
    incremental_hash = hasher1.hexdigest()

    hasher2 = SHA256()
    one_shot_hash = hasher2.hash(b"hello world")

    match1 = incremental_hash == one_shot_hash
    print(f"  'hello' + ' ' + 'world' == 'hello world': {match1}")

    # Тест 2: 'a' + 'b' + 'c' должно быть равно 'abc'
    hasher3 = SHA256()
    hasher3.update(b"a")
    hasher3.update(b"b")
    hasher3.update(b"c")
    incremental_abc = hasher3.hexdigest()

    one_shot_abc = hasher2.hash(b"abc")

    match2 = incremental_abc == one_shot_abc
    print(f"  'a' + 'b' + 'c' == 'abc': {match2}")

    return match1 and match2


def test_nist_vectors():
    print("\n🔹 NIST тест-векторы:")

    # Source: https://www.di-mgt.com.au/sha_testvectors.html
    test_cases = [
        (b"",
         "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),

        (b"abc",
         "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),

        (b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",
         "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"),
    ]

    all_pass = True
    for data, expected in test_cases:
        hasher = SHA256()
        result = hasher.hash(data)

        match = result == expected
        all_pass = all_pass and match

        status = "✅" if match else "❌"
        desc = f"{len(data)} байт" if data else "пустая строка"
        print(f"  {status} {desc}: {match}")

        if not match:
            print(f"    Ожидалось: {expected}")
            print(f"    Получено:  {result}")

    return all_pass


def main():
    print("🧪 ФИНАЛЬНЫЙ ТЕСТ SHA-256")
    print("=" * 60)

    results = []

    try:
        results.append(("Базовые тесты", test_basic()))
        results.append(("Сравнение с hashlib", test_with_hashlib()))
        results.append(("Инкрементальное", test_incremental()))
        results.append(("NIST векторы", test_nist_vectors()))
    except Exception as e:
        print(f"\n❌ Ошибка во время тестирования: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\n" + "=" * 60)
    print("ИТОГИ:")
    print("=" * 60)

    all_passed = True
    for name, passed in results:
        status = "✅ ПРОЙДЕН" if passed else "❌ ПРОВАЛЕН"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! SHA-256 работает корректно!")
    else:
        print("💥 НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛЕНЫ")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)