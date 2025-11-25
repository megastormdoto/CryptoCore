import os


def generate_key():
    """Генерирует 16-байтный AES ключ"""
    return os.urandom(16)


def test_1000_keys():
    print("🔑 TEST-2: Проверка уникальности 1000 ключей")
    print("Генерация 1000 ключей...")

    keys = set()
    duplicates = 0

    for i in range(1000):
        key = generate_key()
        key_hex = key.hex()  # Конвертируем в HEX для проверки

        if key_hex in keys:
            duplicates += 1
            print(f"❌ ДУБЛИКАТ! Ключ #{i}: {key_hex}")
        else:
            keys.add(key_hex)

        if (i + 1) % 100 == 0:
            print(f"  ✅ Сгенерировано {i + 1} ключей...")

    print(f"\n📊 РЕЗУЛЬТАТЫ:")
    print(f"Всего ключей: 1000")
    print(f"Уникальных: {len(keys)}")
    print(f"Дубликатов: {duplicates}")

    if duplicates == 0:
        print("🎉 ТЕСТ ПРОЙДЕН! Все ключи уникальны")
        return True
    else:
        print("💥 ТЕСТ ПРОВАЛЕН! Найдены дубликаты")
        return False


if __name__ == "__main__":
    success = test_1000_keys()
    exit(0 if success else 1)