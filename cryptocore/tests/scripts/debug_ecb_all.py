# test_ecb_all.py - ВСЁ в одном файле!
from Crypto.Cipher import AES


# Класс ECBMode прямо здесь
class ECBMode:
    def __init__(self, key):
        if len(key) != 16:
            raise ValueError("Key must be 16 bytes")
        self.key = key
        self.block_size = 16

    def encrypt(self, plaintext):
        padded_data = self._pkcs7_pad(plaintext)
        cipher = AES.new(self.key, AES.MODE_ECB)

        encrypted_blocks = []
        for i in range(0, len(padded_data), self.block_size):
            block = padded_data[i:i + self.block_size]
            encrypted_block = cipher.encrypt(block)
            encrypted_blocks.append(encrypted_block)

        return b''.join(encrypted_blocks)

    def decrypt(self, ciphertext):
        if len(ciphertext) % self.block_size != 0:
            raise ValueError("Ciphertext must be multiple of block size")

        cipher = AES.new(self.key, AES.MODE_ECB)

        decrypted_blocks = []
        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]
            decrypted_block = cipher.decrypt(block)
            decrypted_blocks.append(decrypted_block)

        decrypted_data = b''.join(decrypted_blocks)
        return self._pkcs7_unpad(decrypted_data)

    def _pkcs7_pad(self, data):
        padding_length = self.block_size - (len(data) % self.block_size)
        padding = bytes([padding_length] * padding_length)
        return data + padding

    def _pkcs7_unpad(self, data):
        if len(data) == 0:
            return data

        padding_length = data[-1]

        if padding_length < 1 or padding_length > self.block_size:
            raise ValueError("Invalid padding")

        if data[-padding_length:] != bytes([padding_length] * padding_length):
            raise ValueError("Invalid padding")

        return data[:-padding_length]


# Тесты прямо здесь
def test_basic():
    print("Testing basic ECB...")

    key = b'0123456789abcdef'
    test_data = b'Hello, CryptoCore!'

    ecb = ECBMode(key)

    encrypted = ecb.encrypt(test_data)
    print(f"Original: {test_data}")
    print(f"Encrypted: {encrypted.hex()}")

    decrypted = ecb.decrypt(encrypted)
    print(f"Decrypted: {decrypted}")

    if test_data == decrypted:
        print("✅ SUCCESS: Basic test passed!")
        return True
    else:
        print("❌ FAILED: Basic test failed!")
        return False


def test_padding():
    print("Testing padding...")

    key = b'0123456789abcdef'
    ecb = ECBMode(key)

    test_cases = [b'', b'A', b'Hello', b'16bytes!!!!!!']

    for i, data in enumerate(test_cases):
        encrypted = ecb.encrypt(data)
        decrypted = ecb.decrypt(encrypted)

        if data == decrypted:
            print(f"  ✅ Test {i + 1} passed")
        else:
            print(f"  ❌ Test {i + 1} failed")

    print("✅ All padding tests completed!")


if __name__ == "__main__":
    print("=== Testing ECB Mode ===")
    test_basic()
    test_padding()
    print("=== All tests finished ===")