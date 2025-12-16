# debug_nist_exact.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from modes.gcm import GCM

print("=" * 70)
print("DEBUG NIST TEST VECTOR 2")
print("=" * 70)

# NIST Test Vector 2
key = bytes.fromhex('00000000000000000000000000000000')
nonce = bytes.fromhex('000000000000000000000000')
plaintext = bytes.fromhex('00000000000000000000000000000000')
aad = b""

print(f"Key: {key.hex()}")
print(f"Nonce: {nonce.hex()}")
print(f"Plaintext: {plaintext.hex()}")
print(f"AAD: {aad.hex() if aad else '(empty)'}")

# Создаем GCM
gcm = GCM(key, nonce)

# 1. Проверяем H
H = gcm.aes.encrypt(b'\x00' * 16)
print(f"\n1. H = AES_K(0^128): {H.hex()}")
print(f"   H as int: {int.from_bytes(H, 'big'):#034x}")

# 2. Вычисляем J0
j0 = nonce + b'\x00\x00\x00\x01'
print(f"\n2. J0 = IV || 0^31 || 1: {j0.hex()}")

# 3. Вычисляем S = AES_K(J0)
s = gcm.aes.encrypt(j0[:16])  # Берем первые 16 байт
s_int = int.from_bytes(s, 'big')
print(f"3. S = AES_K(J0): {s.hex()}")
print(f"   S as int: {s_int:#034x}")

# 4. CTR шифрование
print(f"\n4. CTR Encryption:")
counter = gcm._inc32(j0[:16])
print(f"   Initial counter = inc32(J0): {counter.hex()}")

keystream1 = gcm.aes.encrypt(counter)
print(f"   Keystream block 1: {keystream1.hex()}")

# Plaintext = 16 нулевых байтов
ciphertext = bytes(p ^ k for p, k in zip(plaintext, keystream1))
print(f"   Ciphertext (plaintext XOR keystream): {ciphertext.hex()}")
print(f"   Expected ciphertext: 0388dace60b6a392f328c2b971b2fe78")

# 5. GHASH вычисление
print(f"\n5. GHASH Calculation:")
# AAD пустой, ciphertext = 16 байт
# Согласно NIST: GHASH_H(AAD, C) где:
# - AAD пустой
# - C = ciphertext

ghash = gcm._ghash(aad, ciphertext)
print(f"   GHASH result: {ghash:#034x}")

# 6. Tag вычисление
tag_int = ghash ^ s_int
tag = tag_int.to_bytes(16, 'big')
print(f"\n6. Tag = GHASH XOR S:")
print(f"   Tag int: {tag_int:#034x}")
print(f"   Tag bytes: {tag.hex()}")
print(f"   Expected tag: ab6e47d42cec13bdf53a67b21257bddf")

# 7. Проверяем GF умножение
print(f"\n7. GF Multiplication Test:")
# Тестируем умножение на H
test_block = b'\x00' * 16
test_int = int.from_bytes(test_block, 'big')
result = gcm._gf_mult(test_int ^ 0x1234567890ABCDEF, gcm.H_int)
print(f"   Test GF mult: {result:#034x}")

print("\n" + "=" * 70)
print("COMPLETE ENCRYPTION:")
ct = gcm.encrypt(plaintext, aad)
print(f"Full ciphertext with nonce: {ct.hex()}")
print(f"Nonce (12): {ct[:12].hex()}")
print(f"Ciphertext (16): {ct[12:-16].hex()}")
print(f"Tag (16): {ct[-16:].hex()}")