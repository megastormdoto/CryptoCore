# test_gcm_logic.py
import os
import sys
sys.path.insert(0, 'src')

from modes.gcm import GCM

print("=== Тестируем логику GCM ===")

key = bytes.fromhex('00112233445566778899aabbccddeeff')

# 1. Шифруем
print("\n1. Шифрование:")
gcm1 = GCM(key, None)
plaintext = b"Test message"
aad = b"aabbccdd"
ciphertext = gcm1.encrypt(plaintext, aad)
print(f"   Ciphertext: {len(ciphertext)} bytes")
print(f"   Nonce в данных: {ciphertext[:12].hex()}")

# 2. Дешифруем ВСЕ данные
print("\n2. Дешифрование (передаем ВСЕ данные):")
gcm2 = GCM(key, None)  # None - ок
decrypted = gcm2.decrypt(ciphertext, aad)  # Передаем ВСЕ данные
print(f"   Результат: {decrypted}")
print(f"   Совпадает? {decrypted == plaintext}")

# 3. Симулируем ошибку CLI (удаляем nonce из данных)
print("\n3. Симулируем ошибку CLI (удалили nonce):")
ciphertext_without_nonce = ciphertext[12:]  # Без nonce
try:
    gcm3 = GCM(key, ciphertext[:12])  # Передаем nonce в конструктор
    decrypted_wrong = gcm3.decrypt(ciphertext_without_nonce, aad)
    print(f"   ❌ ОШИБКА: Должен был упасть!")
except Exception as e:
    print(f"   ✅ Правильно упал: {e}")

print("\n=== Вывод: GCM.decrypt() ожидает ВСЕ данные, включая nonce! ===")
