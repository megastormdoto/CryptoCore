# correct_final_pbkdf2.py
import hmac
import hashlib
import struct


def correct_pbkdf2(password, salt, iterations, dklen):
    """
    Correct PBKDF2-HMAC-SHA256 implementation.
    The issue might be in XOR operation order or byte order.
    """
    if isinstance(password, str):
        password = password.encode('utf-8')
    if isinstance(salt, str):
        try:
            if all(c in '0123456789abcdefABCDEF' for c in salt.strip()):
                salt = bytes.fromhex(salt)
            else:
                salt = salt.encode('utf-8')
        except:
            salt = salt.encode('utf-8')

    hlen = 32
    blocks_needed = (dklen + hlen - 1) // hlen

    derived_key = b''

    for i in range(1, blocks_needed + 1):
        # U1 = HMAC(password, salt || INT_32_BE(i))
        block_input = salt + struct.pack('>I', i)
        u = hmac.new(password, block_input, hashlib.sha256).digest()
        block = u

        # For iterations > 1, XOR with subsequent U values
        for _ in range(2, iterations + 1):
            u = hmac.new(password, u, hashlib.sha256).digest()
            # XOR each byte
            block = bytes(b1 ^ b2 for b1, b2 in zip(block, u))

        derived_key += block

    return derived_key[:dklen]


def test_algorithm():
    """Test the algorithm step by step."""
    print("STEP BY STEP ALGORITHM CHECK")
    print("=" * 60)

    password = b'password'
    salt = b'salt'
    i = 1

    # Step 1: Compute block input
    block_input = salt + struct.pack('>I', i)
    print(f"1. Block input: {block_input.hex()}")

    # Step 2: Compute U1
    u1 = hmac.new(password, block_input, hashlib.sha256).digest()
    print(f"2. U1: {u1.hex()}")
    print(f"   U1 (first 20 bytes): {u1[:20].hex()}")

    # Step 3: For iterations=1, block = U1
    block = u1
    print(f"3. Block after 1 iteration: {block[:20].hex()}")

    # Step 4: Compare with expected
    expected = bytes.fromhex('0c60c80f961f0e71f3a9b524af6012062fe037a6')
    print(f"4. Expected: {expected.hex()}")
    print(f"5. Match: {block[:20] == expected}")

    # Let's check what Python's hashlib gives us
    print("\n" + "=" * 60)
    print("PYTHON HASHLIB PBKDF2_HMAC RESULT:")

    import hashlib
    python_result = hashlib.pbkdf2_hmac('sha256', password, salt, 1, 20)
    print(f"Python hashlib: {python_result.hex()}")
    print(f"Matches expected: {python_result.hex() == '0c60c80f961f0e71f3a9b524af6012062fe037a6'}")

    # Let's also compute U1 ourselves
    print("\n" + "=" * 60)
    print("MANUAL HMAC COMPUTATION:")

    # HMAC key padding
    block_size = 64  # SHA-256 block size

    if len(password) > block_size:
        key = hashlib.sha256(password).digest()
    else:
        key = password + b'\x00' * (block_size - len(password))

    print(f"Key (padded): {key[:16].hex()}...")

    # ipad and opad
    ipad = bytes([0x36] * block_size)
    opad = bytes([0x5C] * block_size)

    k_ipad = bytes(k ^ i for k, i in zip(key, ipad))
    k_opad = bytes(k ^ o for k, o in zip(key, opad))

    print(f"\nComputing HMAC...")
    print(f"inner = SHA256((key XOR ipad) || message)")

    inner_input = k_ipad + block_input
    inner_hash = hashlib.sha256(inner_input).digest()
    print(f"inner hash: {inner_hash.hex()}")

    outer_input = k_opad + inner_hash
    hmac_result = hashlib.sha256(outer_input).digest()
    print(f"HMAC result: {hmac_result.hex()}")
    print(f"First 20 bytes: {hmac_result[:20].hex()}")


if __name__ == "__main__":
    # First test our corrected version
    print("TESTING CORRECTED PBKDF2")
    print("=" * 60)

    result = correct_pbkdf2(b'password', b'salt', 1, 20)
    expected = bytes.fromhex('0c60c80f961f0e71f3a9b524af6012062fe037a6')
    print(f"Result:   {result.hex()}")
    print(f"Expected: {expected.hex()}")
    print(f"Match: {result == expected}")

    # Run algorithm test
    test_algorithm()