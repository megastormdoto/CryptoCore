#!/usr/bin/env python3
"""
Отладочный тест SHA-256
"""
import sys
import os

sys.path.insert(0, 'src')

from hash.sha256 import SHA256


def test_one_byte():
    """Тестируем один байт"""
    print("Тест 1: Один байт 'a'")
    hasher = SHA256()

    # Байт 'a' = 0x61
    data = b'a'
    result = hasher.hash(data)

    # Ожидаемый хеш для 'a'
    # Можно проверить через python: hashlib.sha256(b'a').hexdigest()
    expected = "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"

    print(f"  Результат: {result}")
    print(f"  Ожидаемый: {expected}")
    print(f"  Совпадает: {result == expected}")

    # Распечатаем промежуточные данные
    print(f"  Данные (hex): {data.hex()}")
    print(f"  Длина: {len(data)} байт")

    return result == expected


def test_abc_step_by_step():
    """Тестируем 'abc' пошагово"""
    print("\nТест 2: 'abc' пошагово")

    # Ожидаемый: ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
    data = b'abc'
    print(f"  Данные: '{data.decode()}'")
    print(f"  HEX: {data.hex()}")
    print(f"  Бинарно: {bin(int.from_bytes(data, 'big'))[2:].zfill(len(data) * 8)}")

    # Посчитаем вручную
    hasher = SHA256()

    # Давай посмотрим на паддинг
    print(f"\n  Длина сообщения: {len(data)} байт = {len(data) * 8} бит")

    # Покажем каждый шаг
    hasher.update(data)
    print(f"  message_length после update: {hasher.message_length}")
    print(f"  unprocessed: {hasher.unprocessed.hex()}")

    digest = hasher.digest()
    result = digest.hex()
    expected = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"

    print(f"\n  Результат: {result}")
    print(f"  Ожидаемый: {expected}")
    print(f"  Совпадает: {result == expected}")

    return result == expected


def test_padding():
    """Тестируем паддинг"""
    print("\nТест 3: Проверка паддинга")

    # Для пустой строки
    hasher = SHA256()
    empty_hash = hasher.hash(b"")
    expected_empty = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    print(f"  Пустая строка: {empty_hash}")
    print(f"  Ожидаемый:     {expected_empty}")
    print(f"  Совпадает: {empty_hash == expected_empty}")

    # Посмотрим паддинг для длины 0
    padding = hasher._sha256_padding(0)
    print(f"\n  Паддинг для длины 0:")
    print(f"    HEX: {padding.hex()}")
    print(f"    Длина паддинга: {len(padding)} байт")
    print(f"    Бит '1': {padding[0:1].hex()} = 0x80")
    print(f"    Нули: {len(padding) - 9} байт")
    print(f"    Длина сообщения (64 бита): {padding[-8:].hex()}")

    return empty_hash == expected_empty


def compare_with_hashlib():
    """Сравнение с hashlib"""
    import hashlib

    print("\nТест 4: Сравнение с hashlib")

    test_cases = [
        b"",
        b"a",
        b"ab",
        b"abc",
        b"abcd",
        b"hello",
    ]

    all_match = True
    for data in test_cases:
        # Наша реализация
        our_hasher = SHA256()
        our_hash = our_hasher.hash(data)

        # hashlib
        lib_hash = hashlib.sha256(data).hexdigest()

        match = our_hash == lib_hash
        all_match = all_match and match

        print(f"  '{data.decode() if data else 'пусто'}': {match}")
        if not match:
            print(f"    Наша:  {our_hash}")
            print(f"    Библиотека: {lib_hash}")
            print(f"    Данные HEX: {data.hex()}")

    return all_match


def main():
    print("🔧 Отладочный тест SHA-256")
    print("=" * 60)

    results = []

    results.append(("Один байт", test_one_byte()))
    results.append(("'abc' пошагово", test_abc_step_by_step()))
    results.append(("Паддинг", test_padding()))
    results.append(("Сравнение с hashlib", compare_with_hashlib()))

    print("\n" + "=" * 60)
    print("ИТОГИ:")
    for name, passed in results:
        status = "✅" if passed else "❌"
        print(f"  {name}: {status}")

    all_passed = all(passed for _, passed in results)

    if all_passed:
        print("\n🎉 Все тесты пройдены!")
    else:
        print("\n🔧 Нужна отладка алгоритма")


if __name__ == "__main__":
    main()