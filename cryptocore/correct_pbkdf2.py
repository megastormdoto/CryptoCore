# Создайте файл correct_pbkdf2.py в корне
import hmac
import hashlib
import struct


def correct_pbkdf2_hmac_sha256(password, salt, iterations, dklen):
    """
    Correct PBKDF2-HMAC-SHA256 implementation.

    Args:
        password: bytes or str
        salt: bytes or str
        iterations: int
        dklen: int
    Returns:
        bytes
    """
    # Convert to bytes if needed
    if isinstance(password, str):
        password = password.encode('utf-8')

    if isinstance(salt, str):
        # Try hex first, then text
        try:
            # Check if it's hex
            if all(c in '0123456789abcdefABCDEF' for c in salt.strip()):
                salt = bytes.fromhex(salt)
            else:
                salt = salt.encode('utf-8')
        except:
            salt = salt.encode('utf-8')

    def prf(key, data):
        """HMAC-SHA256 PRF."""
        return hmac.new(key, data, hashlib.sha256).digest()

    hlen = 32  # SHA-256 output size
    blocks_needed = (dklen + hlen - 1) // hlen

    derived_key = b''

    for i in range(1, blocks_needed + 1):
        # U1 = PRF(P, S || INT_32_BE(i))
        block_input = salt + struct.pack('>I', i)
        u_prev = prf(password, block_input)
        block = u_prev

        # U2 through Uc
        for j in range(2, iterations + 1):
            u_curr = prf(password, u_prev)
            # XOR with block
            block = bytes(a ^ b for a, b in zip(block, u_curr))
            u_prev = u_curr

        derived_key += block

    return derived_key[:dklen]


# Test
if __name__ == "__main__":
    print("Testing correct PBKDF2 implementation...")

    # Test vector 1
    result = correct_pbkdf2_hmac_sha256(b'password', b'salt', 1, 20)
    expected = bytes.fromhex('0c60c80f961f0e71f3a9b524af6012062fe037a6')
    print(f"Test 1: {result.hex() == expected.hex()}")
    print(f"  Result:   {result.hex()}")
    print(f"  Expected: {expected.hex()}")

    # Test vector 2
    result = correct_pbkdf2_hmac_sha256(b'password', b'salt', 2, 20)
    expected = bytes.fromhex('ea6c014dc72d6f8ccd1ed92ace1d41f0d8de8957')
    print(f"\nTest 2: {result.hex() == expected.hex()}")
    print(f"  Result:   {result.hex()}")
    print(f"  Expected: {expected.hex()}")

    # Test hex salt
    result = correct_pbkdf2_hmac_sha256('password', '73616c74', 1, 20)
    expected = bytes.fromhex('0c60c80f961f0e71f3a9b524af6012062fe037a6')
    print(f"\nTest 3 (hex salt): {result.hex() == expected.hex()}")
    print(f"  Result:   {result.hex()}")
    print(f"  Expected: {expected.hex()}")