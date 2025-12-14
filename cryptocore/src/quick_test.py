# В папке src создайте файл quick_test.py
# !/usr/bin/env python3
import sys
import os

# Мы уже в src, добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing HMAC from within src directory...")

try:
    # Пробуем импортировать
    from mac.hmac import HMAC

    print("✓ HMAC imported successfully!")

    # Тестовые данные
    test_data = b"Hi There"
    test_key = bytes.fromhex("0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b")

    # Создаем HMAC
    hmac = HMAC(test_key, 'sha256')
    result = hmac.compute_hex(test_data)

    print(f"\nComputed HMAC: {result}")
    print(f"Expected:      b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7")

    if result == "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7":
        print("\n✓ SUCCESS! RFC 4231 test passed!")
    else:
        print("\n✗ FAIL: HMAC doesn't match")

except ImportError as e:
    print(f"Import error: {e}")
    print(f"\nTrying different import...")

    # Попробуем другой способ
    try:
        import mac.hmac

        HMAC = mac.hmac.HMAC
        print("✓ Import worked with import mac.hmac")
    except Exception as e2:
        print(f"Still failed: {e2}")

        # Прямой импорт файла
        import importlib.util

        hmac_path = os.path.join(os.path.dirname(__file__), 'mac', 'hmac.py')
        spec = importlib.util.spec_from_file_location("hmac", hmac_path)
        hmac_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(hmac_module)
        HMAC = hmac_module.HMAC
        print("✓ Direct file import worked!")