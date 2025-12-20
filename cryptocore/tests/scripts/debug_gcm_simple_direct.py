#!/usr/bin/env python3
"""
Simple direct GCM test
"""
import os
import sys

print("🧪 Simple GCM Direct Test")
print("=" * 50)

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(__file__))

# Проверим что есть в директории
print("Files in directory:")
for f in os.listdir('../../src'):
    print(f"  {f}")

print("\nChecking for modes directory...")
if os.path.exists('../../src/modes'):
    print("✓ modes directory exists")
    print("Files in modes:")
    for f in os.listdir('../../src/modes'):
        print(f"  {f}")
else:
    print("✗ modes directory not found")
    sys.exit(1)

# Пробуем импортировать
try:
    print("\nTrying to import GCM...")
    from modes.gcm import GCM, AuthenticationError

    print("✓ GCM imported successfully!")

    # Простой тест
    print("\nRunning simple GCM test...")
    key = b'\x00' * 16
    plaintext = b"Hello GCM world!"
    aad = b"test aad"

    # Шифрование
    gcm = GCM(key)
    print(f"Nonce generated: {gcm.nonce.hex()}")

    ciphertext = gcm.encrypt(plaintext, aad)
    print(f"Ciphertext length: {len(ciphertext)} bytes")
    print(f"Structure: nonce(12) + ciphertext({len(ciphertext) - 28}) + tag(16)")

    # Дешифрование
    gcm2 = GCM(key, gcm.nonce)
    decrypted = gcm2.decrypt(ciphertext, aad)

    if decrypted == plaintext:
        print("✓ Decryption successful!")
    else:
        print("✗ Decryption failed")
        sys.exit(1)

    # Тест неправильного AAD
    print("\nTesting wrong AAD (should fail)...")
    try:
        gcm3 = GCM(key, gcm.nonce)
        gcm3.decrypt(ciphertext, b"WRONG AAD")
        print("✗ Should have failed but didn't!")
        sys.exit(1)
    except AuthenticationError:
        print("✓ Correctly failed with wrong AAD")

    print("\n" + "=" * 50)
    print("🎉 GCM implementation is working correctly!")
    print("\n✅ Sprint 6 requirements met:")
    print("  - GCM encryption/decryption ✓")
    print("  - Authentication tag ✓")
    print("  - AAD support ✓")
    print("  - Catastrophic failure on auth error ✓")

except ImportError as e:
    print(f"\n❌ Import error: {e}")
    print("\nLet's debug the import...")

    # Попробуем импортировать напрямую
    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "gcm",
            os.path.join('../../src/modes', 'gcm.py')
        )
        gcm_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gcm_module)
        print("✓ Loaded gcm.py directly")

        # Тест
        gcm = gcm_module.GCM(b'\x00' * 16)
        print(f"✓ Created GCM instance, nonce: {gcm.nonce.hex()}")

    except Exception as e2:
        print(f"✗ Direct load failed: {e2}")

except Exception as e:
    print(f"\n❌ Test error: {type(e).__name__}: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)