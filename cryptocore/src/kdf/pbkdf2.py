"""
PBKDF2 implementation from scratch according to RFC 2898.
"""
import struct
import hashlib
from typing import Union

# Try to import our HMAC implementation from Sprint 5
try:
    # Assuming HMAC is in src/mac/hmac.py
    import sys
    import os

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from mac.hmac import hmac_sha256

    print("Using our HMAC implementation")
except ImportError as e:
    print(f"Warning: Using fallback HMAC: {e}")
    # Fallback using Python's built-in HMAC
    import hmac


    def hmac_sha256(key: bytes, msg: bytes) -> bytes:
        """Fallback HMAC-SHA256 using Python's hmac module."""
        return hmac.new(key, msg, hashlib.sha256).digest()


def _is_hex_string(s: str) -> bool:
    """Check if string contains only hexadecimal characters."""
    try:
        # Remove any whitespace and check
        s = s.strip()
        # Check if all characters are hex digits (case insensitive)
        return all(c in '0123456789abcdefABCDEF' for c in s)
    except:
        return False


def pbkdf2_hmac_sha256(
        password: Union[str, bytes],
        salt: Union[str, bytes],
        iterations: int,
        dklen: int
) -> bytes:
    """
    PBKDF2-HMAC-SHA256 implementation from scratch.

    Args:
        password: Password as string or bytes
        salt: Salt as string or bytes (hex string if string contains hex chars)
        iterations: Number of iterations
        dklen: Desired key length in bytes

    Returns:
        Derived key as bytes
    """
    # Convert inputs to bytes if needed
    if isinstance(password, str):
        password = password.encode('utf-8')

    if isinstance(salt, str):
        # Check if string looks like hexadecimal
        if _is_hex_string(salt):
            try:
                salt = bytes.fromhex(salt)
            except ValueError:
                # If it looks like hex but conversion fails, treat as text
                salt = salt.encode('utf-8')
        else:
            salt = salt.encode('utf-8')

    # Calculate number of blocks needed (SHA-256 produces 32-byte hashes)
    hlen = 32  # SHA-256 output size
    blocks_needed = (dklen + hlen - 1) // hlen

    derived_key = b''

    for i in range(1, blocks_needed + 1):
        # U1 = HMAC(password, salt || INT_32_BE(i))
        block_input = salt + struct.pack('>I', i)
        u_current = hmac_sha256(password, block_input)
        block = u_current

        # Compute U2 through Uc
        for _ in range(2, iterations + 1):
            u_current = hmac_sha256(password, u_current)
            # XOR u_current into block
            block = bytes(a ^ b for a, b in zip(block, u_current))

        derived_key += block

    # Return exactly dklen bytes
    return derived_key[:dklen]


def pbkdf2(
        password: Union[str, bytes],
        salt: Union[str, bytes],
        iterations: int = 100000,
        dklen: int = 32,
        hash_name: str = 'sha256'
) -> bytes:
    """
    Main PBKDF2 function supporting different hash algorithms.
    Currently only SHA-256 is implemented.
    """
    if hash_name.lower() != 'sha256':
        raise ValueError(f"Hash algorithm {hash_name} not supported. Only 'sha256' is available.")

    return pbkdf2_hmac_sha256(password, salt, iterations, dklen)


# Simple test to verify implementation
if __name__ == '__main__':
    # Test with RFC 6070 test vector 1
    print("Testing PBKDF2 with RFC 6070 test vector 1...")
    result = pbkdf2_hmac_sha256(
        b'password',
        b'salt',
        1,
        20
    )
    expected = bytes.fromhex('0c60c80f961f0e71f3a9b524af6012062fe037a6')

    if result == expected:
        print("✓ Test vector 1 passed")
    else:
        print(f"✗ Test vector 1 failed")
        print(f"  Expected: {expected.hex()}")
        print(f"  Got:      {result.hex()}")

    # Test with hex salt
    print("\nTesting with hex salt...")
    result = pbkdf2_hmac_sha256(
        'password',
        '73616c74',  # hex for 'salt'
        1,
        20
    )

    if result == expected:
        print("✓ Hex salt test passed")
    else:
        print(f"✗ Hex salt test failed")
        print(f"  Expected: {expected.hex()}")
        print(f"  Got:      {result.hex()}")