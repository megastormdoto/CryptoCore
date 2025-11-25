import os
import collections


def generate_random_bytes(size):
    return os.urandom(size)


def test_basic_statistics():
    print("📊 TEST-3: Базовая статистическая проверка")
    print("Генерация 1 МБ данных для анализа...")

    # Генерируем 1 МБ данных
    data_size = 1024 * 1024  # 1 MB
    test_data = generate_random_bytes(data_size)

    print("🔍 Анализ статистических свойств...")

    # 1. Распределение байтов
    byte_counts = collections.Counter(test_data)
    byte_entropy = len(byte_counts) / 256.0  # Доля уникальных байтов

    # 2. Частота битов
    ones_count = sum(bin(byte).count('1') for byte in test_data)
    total_bits = len(test_data) * 8
    ones_percentage = (ones_count / total_bits) * 100

    # 3. Проверка на последовательности
    consecutive_zeros = 0
    consecutive_ones = 0
    max_consecutive_zeros = 0
    max_consecutive_ones = 0

    for byte in test_data:
        binary = format(byte, '08b')
        for bit in binary:
            if bit == '0':
                consecutive_zeros += 1
                consecutive_ones = 0
                max_consecutive_zeros = max(max_consecutive_zeros, consecutive_zeros)
            else:
                consecutive_ones += 1
                consecutive_zeros = 0
                max_consecutive_ones = max(max_consecutive_ones, consecutive_ones)

    print(f"\n📈 РЕЗУЛЬТАТЫ СТАТИСТИЧЕСКОГО АНАЛИЗА:")
    print(f"Объем данных: {len(test_data)} байт ({len(test_data) / 1024 / 1024:.2f} MB)")
    print(f"Уникальных байтов: {len(byte_counts)}/256 ({byte_entropy * 100:.1f}%)")
    print(f"Процент единичных битов: {ones_percentage:.4f}%")
    print(f"Макс. последовательных нулей: {max_consecutive_zeros}")
    print(f"Макс. последовательных единиц: {max_consecutive_ones}")

    # Критерии успеха
    success = True
    criteria = []

    # Критерий 1: Процент единиц близок к 50%
    if 49.0 <= ones_percentage <= 51.0:
        criteria.append("✅ Распределение битов близко к 50%")
    else:
        criteria.append("❌ Смещение в распределении битов")
        success = False

    # Критерий 2: Высокая энтропия байтов
    if byte_entropy > 0.6:  # Более 60% уникальных байтов
        criteria.append("✅ Высокая энтропия байтов")
    else:
        criteria.append("❌ Низкая энтропия байтов")
        success = False

    # Критерий 3: Нет очень длинных последовательностей
    if max_consecutive_zeros < 50 and max_consecutive_ones < 50:
        criteria.append("✅ Нет длинных последовательностей")
    else:
        criteria.append("❌ Обнаружены длинные последовательности")
        success = False

    print(f"\n📋 КРИТЕРИИ КАЧЕСТВА:")
    for criterion in criteria:
        print(f"  {criterion}")

    if success:
        print("\n🎉 ТЕСТ ПРОЙДЕН: Данные проходят базовые статистические проверки")
    else:
        print("\n💥 ТЕСТ ПРОВАЛЕН: Обнаружены статистические аномалии")

    return success


if __name__ == "__main__":
    success = test_basic_statistics()
    exit(0 if success else 1)