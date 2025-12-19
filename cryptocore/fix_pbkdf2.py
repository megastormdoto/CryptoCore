#!/usr/bin/env python3
"""Fix PBKDF2 implementation."""
import sys
import os

# Добавляем разные пути для импорта
import_paths = [
    os.path.join(os.path.dirname(__file__), 'cryptocore', 'src'),
    os.path.join(os.path.dirname(__file__), 'src'),
    os.path.join(os.path.dirname(__file__), 'cryptocore'),
]

for path in import_paths:
    if os.path.exists(path):
        sys.path.insert(0, path)
        print(f"Added to path: {path}")

print(f"Current sys.path: {sys.path[:3]}")

# Попробуем импортировать
try:
    from kdf.pbkdf2 import pbkdf2_hmac_sha256

    print("✓ Import successful from kdf.pbkdf2")

    # Test
    print("\nTesting PBKDF2...")
    result = pbkdf2_hmac_sha256(b'password', b'salt', 1, 20)
    expected = bytes.fromhex('0c60c80f961f0e71f3a9b524af6012062fe037a6')
    print(f"Result:   {result.hex()}")
    print(f"Expected: {expected.hex()}")
    print(f"Match: {result == expected}")

except ImportError as e:
    print(f"✗ Import error: {e}")

    # Попробуем найти модуль
    import importlib.util

    for path in import_paths:
        pbkdf2_path = os.path.join(path, 'kdf', 'pbkdf2.py')
        if os.path.exists(pbkdf2_path):
            print(f"Found pbkdf2.py at: {pbkdf2_path}")

            # Попробуем импортировать напрямую
            spec = importlib.util.spec_from_file_location("pbkdf2", pbkdf2_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            result = module.pbkdf2_hmac_sha256(b'password', b'salt', 1, 20)
            expected = bytes.fromhex('0c60c80f961f0e71f3a9b524af6012062fe037a6')
            print(f"Direct import result: {result.hex()}")
            print(f"Expected: {expected.hex()}")
            print(f"Match: {result == expected}")
            break