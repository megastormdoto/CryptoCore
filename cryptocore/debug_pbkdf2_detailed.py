#!/usr/bin/env python3
"""Detailed debug of PBKDF2."""
import hmac
import hashlib
import struct


def debug_step_by_step(password, salt, iterations, dklen):
    """Debug PBKDF2 step by step."""
    print("=" * 60)
    print("DEBUG PBKDF2 STEP BY STEP")
    print("=" * 60)

    # Convert to bytes if needed
    if isinstance(password, str):
        password = password.encode('utf-8')
    if isinstance(salt, str):
        salt = salt.encode('utf-8')

    print(f"Password: {password} ({password.hex()})")
    print(f"Salt: {salt} ({salt.hex()})")
    print(f"Iterations: {iterations}")
    print(f"Desired length: {dklen}")

    # PRF function
    def prf(key, data):
        result = hmac.new(key, data, hashlib.sha256).digest()
        print(f"  PRF(key={key[:8].hex()}..., data={data[:8].hex()}...) = {result[:8].hex()}...")
        return result

    hlen = 32  # SHA-256 output size
    blocks_needed = (dklen + hlen - 1) // hlen
    print(f"\nBlocks needed: {blocks_needed}")

    derived_key = b''

    for i in range(1, blocks_needed + 1):
        print(f"\n--- Processing block {i} ---")

        # U1 = PRF(P, S || INT_32_BE(i))
        block_input = salt + struct.pack('>I', i)
        print(f"Block input (salt || INT_32_BE({i})): {block_input.hex()}")

        u_current = prf(password, block_input)
        block = u_current
        print(f"U1 = {u_current.hex()}")
        print(f"Block after U1: {block.hex()}")

        # XOR U2 through Uc
        for j in range(2, iterations + 1):
            u_current = prf(password, u_current)
            print(f"U{j} = {u_current.hex()}")

            # XOR operation
            block = bytes(x ^ y for x, y in zip(block, u_current))
            print(f"Block after XOR with U{j}: {block.hex()}")

        derived_key += block
        print(f"Block {i} final: {block.hex()}")

    result = derived_key[:dklen]
    print(f"\nFinal result: {result.hex()}")
    print(f"Expected (RFC 6070): 0c60c80f961f0e71f3a9b524af6012062fe037a6")

    return result


def debug_known_test():
    """Debug with known test values."""
    print("\n" + "=" * 60)
    print("DEBUG WITH RFC 6070 TEST VECTOR 1")
    print("=" * 60)

    # Let's compute what SHOULD happen according to RFC
    # For PBKDF2 with HMAC-SHA256:
    # U1 = HMAC-SHA256(password, salt || INT_32_BE(1))

    password = b'password'
    salt = b'salt'

    print(f"\n1. First, compute U1:")
    print(f"   password = 'password' = {password.hex()}")
    print(f"   salt = 'salt' = {salt.hex()}")
    print(f"   INT_32_BE(1) = {struct.pack('>I', 1).hex()}")

    block_input = salt + struct.pack('>I', 1)
    print(f"   salt || INT_32_BE(1) = {block_input.hex()}")

    # Compute HMAC manually
    import hmac
    import hashlib

    h = hmac.new(password, block_input, hashlib.sha256)
    u1 = h.digest()
    print(f"   U1 = HMAC-SHA256(password, salt || INT_32_BE(1))")
    print(f"   U1 = {u1.hex()}")

    # For iterations=1, result is just U1 truncated to 20 bytes
    expected_first_20 = u1[:20]
    print(f"\n2. For iterations=1, result is U1 truncated to 20 bytes:")
    print(f"   Result = U1[:20] = {expected_first_20.hex()}")
    print(f"   Expected from RFC: 0c60c80f961f0e71f3a9b524af6012062fe037a6")

    # Let's check what we actually get
    print(f"\n3. Computing full HMAC...")
    h_full = hmac.new(password, block_input, hashlib.sha256).digest()
    print(f"   Full HMAC: {h_full.hex()}")
    print(f"   First 20 bytes: {h_full[:20].hex()}")

    # Let's check Python's built-in PBKDF2
    print(f"\n4. Checking with Python's hashlib.pbkdf2_hmac...")
    try:
        import hashlib as hl
        python_result = hl.pbkdf2_hmac('sha256', password, salt, 1, 20)
        print(f"   Python hashlib result: {python_result.hex()}")
        print(f"   Match expected: {python_result.hex() == '0c60c80f961f0e71f3a9b524af6012062fe037a6'}")
    except:
        print("   hashlib.pbkdf2_hmac not available")

    return expected_first_20


def test_with_builtin():
    """Test using Python's built-in PBKDF2."""
    print("\n" + "=" * 60)
    print("USING PYTHON'S BUILT-IN PBKDF2 FOR COMPARISON")
    print("=" * 60)

    import hashlib

    test_cases = [
        (b'password', b'salt', 1, 20, '0c60c80f961f0e71f3a9b524af6012062fe037a6'),
        (b'password', b'salt', 2, 20, 'ea6c014dc72d6f8ccd1ed92ace1d41f0d8de8957'),
    ]

    for i, (pwd, salt, iters, dklen, expected) in enumerate(test_cases, 1):
        result = hashlib.pbkdf2_hmac('sha256', pwd, salt, iters, dklen)
        print(f"\nTest {i}:")
        print(f"  Result:   {result.hex()}")
        print(f"  Expected: {expected}")
        print(f"  Match: {result.hex() == expected}")


if __name__ == "__main__":
    # First debug
    result = debug_step_by_step(b'password', b'salt', 1, 20)

    # Debug known test
    debug_known_test()

    # Test with builtin
    test_with_builtin()