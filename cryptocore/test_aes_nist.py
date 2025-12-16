# test_aes_nist.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ciphers.aes import AES

# NIST Known Answer Test for AES
key = bytes.fromhex('00000000000000000000000000000000')
plaintext = bytes.fromhex('00000000000000000000000000000000')
expected_ciphertext = bytes.fromhex('66e94bd4ef8a2c3b884cfa59ca342b2e')

aes = AES(key)
result = aes.encrypt(plaintext)

print(f"AES Test:")
print(f"Key: {key.hex()}")
print(f"Plaintext: {plaintext.hex()}")
print(f"Result: {result.hex()}")
print(f"Expected: {expected_ciphertext.hex()}")
print(f"Match: {result == expected_ciphertext}")

# Также проверьте AES на J0
j0 = bytes.fromhex('00000000000000000000000000000001')
result2 = aes.encrypt(j0)
print(f"\nAES on J0:")
print(f"J0: {j0.hex()}")
print(f"AES_K(J0): {result2.hex()}")