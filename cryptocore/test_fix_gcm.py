# test_fix_gcm.py
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from modes.gcm import GCM, AuthenticationError

print("=== Тестируем исправленную версию GCM ===")

# Тест 1: Простой round-trip
print("\n1. Round-trip тест:")
key = bytes.fromhex('00112233445566778899aabbccddeeff')
gcm = GCM(key)

plaintext = b"Hello World"
aad = b"auth"

ct = gcm.encrypt(plaintext, aad)
print(f"  Nonce: {ct[:12].hex()}")
print(f"  Tag: {ct[-16:].hex()}")

try:
    pt = gcm.decrypt(ct, aad)
    if pt == plaintext:
        print("  ✅ Round-trip прошел!")
    else:
        print(f"  ❌ Ошибка: {pt} != {plaintext}")
except AuthenticationError as e:
    print(f"  ❌ Auth error: {e}")

# Тест 2: Проверка что тот же самый GCM объект не работает дважды
print("\n2. Разные объекты GCM:")
gcm1 = GCM(key)
ct1 = gcm1.encrypt(plaintext, aad)

gcm2 = GCM(key)
try:
    pt2 = gcm2.decrypt(ct1, aad)
    print("  ✅ Разные объекты работают!")
except AuthenticationError as e:
    print(f"  ❌ Разные объекты не работают: {e}")

# Тест 3: NIST вектор (нужно узнать nonce)
print("\n3. NIST тестовый вектор (нужен nonce):")
nist_key = bytes.fromhex('00000000000000000000000000000000')
nist_nonce = bytes.fromhex('000000000000000000000000')
nist_plaintext = bytes.fromhex('00000000000000000000000000000000')

gcm_nist = GCM(nist_key, nist_nonce)
ct_nist = gcm_nist.encrypt(nist_plaintext, b"")
print(f"  Nonce: {ct_nist[:12].hex()}")
print(f"  Ciphertext: {ct_nist[12:-16].hex()}")
print(f"  Tag: {ct_nist[-16:].hex()}")
print(f"  Expected tag: 58e2fccefa7e3061367f1d57a4e7455a")