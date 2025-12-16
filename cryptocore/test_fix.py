import sys
sys.path.insert(0, 'src')

# Тестируем напрямую
from modes.gcm import GCM
from cli_parser import CLIParser

# Создаем тестовые данные
key = bytes.fromhex('00112233445566778899aabbccddeeff')
plaintext = b'Hello from direct test'
aad = b'test'

print('1. Direct test...')
gcm = GCM(key, None)  # Передаем None
ciphertext = gcm.encrypt(plaintext, aad)
print(f'   Nonce in ciphertext: {ciphertext[:12].hex()}')
print(f'   Tag in ciphertext: {ciphertext[-16:].hex()}')

# Пробуем дешифровать
gcm2 = GCM(key, None)  # Тоже None
try:
    decrypted = gcm2.decrypt(ciphertext, aad)
    print(f'   Decrypted: {decrypted}')
    print('   ✅ Direct test PASSED')
except Exception as e:
    print(f'   ❌ Direct test FAILED: {e}')

# Тестируем через CLI эмуляцию
print('\n2. CLI emulation test...')
# Симулируем то, что делает cryptocore.py
with open('simple.txt', 'wb') as f:
    f.write(plaintext)

# Шифрование
gcm3 = GCM(key, None)  # None при шифровании
ct = gcm3.encrypt(plaintext, aad)
with open('cli_encrypted.bin', 'wb') as f:
    f.write(ct)

# Дешифрование  
with open('cli_encrypted.bin', 'rb') as f:
    data = f.read()

gcm4 = GCM(key, None)  # None при дешифровании
try:
    pt = gcm4.decrypt(data, aad)
    print(f'   Decrypted via CLI emulation: {pt}')
    print('   ✅ CLI emulation PASSED' if pt == plaintext else '   ❌ CLI emulation FAILED')
except Exception as e:
    print(f'   ❌ CLI emulation FAILED: {e}')

# Cleanup
import os
for f in ['simple.txt', 'cli_encrypted.bin']:
    if os.path.exists(f):
        os.remove(f)
