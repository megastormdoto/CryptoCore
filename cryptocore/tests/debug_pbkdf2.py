#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from kdf.pbkdf2 import pbkdf2_hmac_sha256

print("DEBUGGING PBKDF2 IMPLEMENTATION")
print("=" * 60)

# Test vector 1 from RFC 6070
print("\nTest Vector 1:")
print("Password: 'password' (bytes: b'password')")
print("Salt: 'salt' (bytes: b'salt')")
print("Iterations: 1")
print("Length: 20")

result = pbkdf2_hmac_sha256(b'password', b'salt', 1, 20)
expected = bytes.fromhex('0c60c80f961f0e71f3a9b524af6012062fe037a6')

print(f"\nResult:   {result.hex()}")
print(f"Expected: {expected.hex()}")
print(f"Match: {result == expected}")

# Let's debug step by step
print("\n" + "=" * 60)
print("DEBUG STEP-BY-STEP:")

# Check HMAC implementation
try:
    from mac.hmac import hmac_sha256

    print("Using our HMAC implementation")

    # Test HMAC directly
    print("\nTesting HMAC with known test case:")
    # From RFC 4231 test vector 1
    key = b'\x0b' * 20
    data = b'Hi There'
    expected_hmac = bytes.fromhex('b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7')

    hmac_result = hmac_sha256(key, data)
    print(f"HMAC test: {hmac_result.hex() == expected_hmac.hex()}")

except ImportError as e:
    print(f"HMAC import error: {e}")