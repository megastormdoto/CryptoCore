import os


def generate_key():
    return os.urandom(16)


def test_bit_distribution():
    print("📊 TEST-4: Проверка распределения битов")

    total_bits = 0
    total_ones = 0
    num_samples = 1000

    for i in range(num_samples):
        key = generate_key()
        # Считаем биты '1' в ключе
        ones_count = bin(int.from_bytes(key, 'big')).count('1')
        total_ones += ones_count
        total_bits += len(key) * 8

        if (i + 1) % 200 == 0:
            print(f"  Обработано {i + 1} ключей...")

    percentage_ones = (total_ones / total_bits) * 100
    deviation = abs(percentage_ones - 50.0)

    print(f"\n📈 РЕЗУЛЬТАТЫ РАСПРЕДЕЛЕНИЯ:")
    print(f"Проанализировано битов: {total_bits}")
    print(f"Процент единичных битов: {percentage_ones:.4f}%")
    print(f"Отклонение от 50%: {deviation:.4f}%")

    # Критерий успеха: отклонение < 1%
    if deviation < 1.0:
        print("🎉 ТЕСТ ПРОЙДЕН: Распределение битов близко к идеальному")
        return True
    else:
        print("💥 ТЕСТ ПРОВАЛЕН: Смещение в распределении битов")
        return False


if __name__ == "__main__":
    success = test_bit_distribution()
    exit(0 if success else 1)