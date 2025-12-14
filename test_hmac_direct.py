#!/usr/bin/env python3
import sys
import os

# Добавляем текущую директорию и src в путь
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')

# Добавляем оба пути
sys.path.insert(0, current_dir)  # Сначала корень
sys.path.insert(0, src_path)  # Затем src

print(f"Current dir: {current_dir}")
print(f"Src path: {src_path}")
print(f"Python path: {sys.path}")

# Создаем тестовое сообщение
test_data = b"Hi There"
test_key = bytes.fromhex("0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b")

print("\nTesting HMAC implementation...")
print(f"Key: {test_key.hex()}")
print(f"Data: {test_data}")

try:
    # Сначала попробуем посмотреть что есть в директориях
    print(f"\nContents of src directory:")
    if os.path.exists(src_path):
        for item in os.listdir(src_path):
            print(f"  {item}")

    print(f"\nContents of src/mac directory:")
    mac_path = os.path.join(src_path, 'mac')
    if os.path.exists(mac_path):
        for item in os.listdir(mac_path):
            print(f"  {item}")

    # Пробуем импортировать
    print("\nTrying imports...")

    # Вариант 1: Абсолютный импорт
    print("Trying: from src.mac.hmac import HMAC")
    try:
        from src.mac.hmac import HMAC

        print("✓ Import successful!")
    except ImportError as e1:
        print(f"✗ Import failed: {e1}")

        # Вариант 2: Относительный импорт из src
        print("\nTrying: import sys; sys.path.append('src'); from mac.hmac import HMAC")
        import sys

        sys.path.append('src')
        from mac.hmac import HMAC

        print("✓ Import successful!")

    # Создаем HMAC объект
    hmac = HMAC(test_key, 'sha256')

    # Вычисляем HMAC
    result = hmac.compute_hex(test_data)

    print(f"\nComputed HMAC: {result}")
    print(f"Expected HMAC: b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7")

    if result == "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7":
        print("\n✓ SUCCESS: HMAC matches RFC 4231 test vector!")
    else:
        print("\n✗ FAIL: HMAC does not match expected value")

except ImportError as e:
    print(f"\nImport error: {e}")
    import traceback

    traceback.print_exc()

except Exception as e:
    print(f"\nError: {e}")
    import traceback

    traceback.print_exc()