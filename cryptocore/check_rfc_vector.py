# check_rfc_vector.py
import hmac
import hashlib

print("CHECKING RFC 6070 TEST VECTOR DIRECTLY")
print("=" * 60)

# Test vector from RFC 6070
password = b'password'
salt = b'salt'
iterations = 1
dklen = 20

print(f"Password: '{password.decode()}'")
print(f"Salt: '{salt.decode()}'")
print(f"Iterations: {iterations}")
print(f"Derived key length: {dklen}")

# Compute using Python
result = hashlib.pbkdf2_hmac('sha256', password, salt, iterations, dklen)
print(f"\nPython hashlib.pbkdf2_hmac result: {result.hex()}")

# Expected from assignment
expected_hex = '0c60c80f961f0e71f3a9b524af6012062fe037a6'
print(f"Expected from RFC 6070: {expected_hex}")
print(f"Match: {result.hex() == expected_hex}")

# Let me check online or compute manually
print("\n" + "=" * 60)
print("LET'S COMPUTE HMAC MANUALLY")

# Compute U1 = HMAC-SHA256(password, salt || INT_32_BE(1))
import struct
block_input = salt + struct.pack('>I', 1)
print(f"Block input (salt || INT_32_BE(1)): {block_input.hex()}")

# Compute HMAC
h = hmac.new(password, block_input, hashlib.sha256)
u1 = h.digest()
print(f"U1 (full): {u1.hex()}")
print(f"U1 (first 20 bytes): {u1[:20].hex()}")

# Check if there's confusion about the test vector
print("\n" + "=" * 60)
print("CHECKING OTHER SOURCES")

# Maybe the test vector is for SHA1, not SHA256?
print("\nTesting with SHA1 (just in case):")
try:
    result_sha1 = hashlib.pbkdf2_hmac('sha1', password, salt, iterations, dklen)
    print(f"SHA1 result: {result_sha1.hex()}")
    print(f"Matches RFC 6070? {result_sha1.hex() == expected_hex}")
except:
    print("SHA1 not available")

# Let me check what OpenSSL gives us
print("\n" + "=" * 60)
print("LET'S CHECK WHAT THE ASSIGNMENT REALLY WANTS")

# Maybe the problem is in how we interpret the test?
# Let me re-read RFC 6070...
print("\nLooking at actual RFC 6070 test vectors...")
print("RFC 6070 test vector 1 for PBKDF2:")
print("  Input:")
print("    P = \"password\"")
print("    S = \"salt\"")
print("    c = 1")
print("    dkLen = 20")
print("  Output:")
print("    DK = 0c60c80f961f0e71f3a9b524af6012062fe037a6")

print("\nBut wait! RFC 6070 uses SHA1 as the PRF!")
print("The assignment might have a typo or you might be using SHA256 instead of SHA1")

# Let's verify
print("\n" + "=" * 60)
print("QUICK CHECK: Is RFC 6070 for SHA1 or SHA256?")

import urllib.request
import json

print("According to RFC 6070 title: 'PKCS #5: Password-Based Key Derivation Function 2 (PBKDF2) Test Vectors'")
print("PBKDF2 can use different PRFs. RFC 6070 examples use HMAC-SHA1.")

print("\n" + "=" * 60)
print("SOLUTION: Use the correct test vectors for SHA256!")

# Let me provide correct SHA256 test vectors
print("\nHere are correct test vectors for PBKDF2-HMAC-SHA256:")

# Test from OpenSSL or other implementations
print("\nTest 1 (from various online sources):")
print("Password: 'password', Salt: 'salt', Iterations: 1, dkLen: 20")
print("Expected: 120fb6cffcf8b32c43e7225256c4f837a86548c9")
print(f"Matches our result: {result.hex() == '120fb6cffcf8b32c43e7225256c4f837a86548c9'}")

print("\nTest 2 (from various online sources):")
print("Password: 'password', Salt: 'salt', Iterations: 2, dkLen: 20")
test2 = hashlib.pbkdf2_hmac('sha256', password, salt, 2, 20)
print(f"Expected: ae4d0c95af6b46d32d0adff928f06dd02a303f8e")
print(f"Matches our result: {test2.hex() == 'ae4d0c95af6b46d32d0adff928f06dd02a303f8e'}")