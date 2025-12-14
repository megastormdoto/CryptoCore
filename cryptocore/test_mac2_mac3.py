# test_mac2_mac3.py
# !/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

print("Testing MAC-2 and MAC-3 requirements")
print("=" * 60)

# 1. Test with key longer than 64 bytes (MAC-2)
print("\n1. Testing key longer than 64 bytes (MAC-2 requirement)...")
from mac.hmac import HMAC

# Create 100-byte key
long_key = b'\x01' * 100
data = b"Test message"

hmac = HMAC(long_key, 'sha256')

# Check if key was hashed
processed_key = hmac._processed_key
print(f"   Original key length: {len(long_key)} bytes")
print(f"   Processed key length: {len(processed_key)} bytes")

if len(processed_key) == 64:
    print("   ✅ Key correctly processed to 64 bytes")

    # Check if it was hashed (should be SHA256 of original key)
    from hash.sha256 import SHA256

    hasher = SHA256()
    hasher.update(long_key)
    hashed_key = hasher.digest()

    # Hashed key should be 32 bytes, then padded to 64
    expected_processed = hashed_key + b'\x00' * 32

    if processed_key == expected_processed:
        print("   ✅ Key correctly hashed (SHA256) then padded")
    else:
        print("   ❌ Key processing incorrect")
        print(f"   Processed: {processed_key.hex()[:32]}...")
        print(f"   Expected:  {expected_processed.hex()[:32]}...")
else:
    print("   ❌ Processed key should be 64 bytes")

# 2. Compare with Python's hmac library
print("\n2. Comparing with Python's hmac library (MAC-3 requirement)...")
import hashlib
import hmac as py_hmac

# Test different key sizes
test_cases = [
    (b'short', 16, "Short key (16 bytes)"),
    (b'B' * 64, 64, "Block size key (64 bytes)"),
    (b'L' * 100, 100, "Long key (100 bytes)"),
]

all_pass = True
for key, size, description in test_cases:
    print(f"   Testing {description}...")

    # Our implementation
    our_hmac = HMAC(key, 'sha256')
    our_result = our_hmac.compute_hex(data)

    # Python's standard library
    std_result = py_hmac.new(key, data, hashlib.sha256).hexdigest()

    if our_result == std_result:
        print(f"      ✅ Match")
    else:
        print(f"      ❌ MISMATCH!")
        print(f"      Our: {our_result[:32]}...")
        print(f"      Std: {std_result[:32]}...")
        all_pass = False

print("\n" + "=" * 60)
if all_pass:
    print("✅ ALL REQUIREMENTS PASSED!")
    print("   MAC-2: Keys longer than 64 bytes are hashed ✓")
    print("   MAC-3: HMAC formula correct for all key sizes ✓")
else:
    print("❌ SOME REQUIREMENTS FAILED")