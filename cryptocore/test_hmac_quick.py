import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from src.hash.sha256 import SHA256
    from src.mac.hmac import HMAC

    print("Testing HMAC with RFC 4231 test case 1...")

    key = bytes.fromhex('0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b')
    data = b"Hi There"

    hmac = HMAC(key, SHA256)
    result = hmac.compute(data).hex()
    expected = "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7"

    print(f"Key: {key.hex()}")
    print(f"Data: {data}")
    print(f"Expected: {expected}")
    print(f"Got:      {result}")
    print(f"Match: {result == expected}")

    if result == expected:
        print("✓ SUCCESS! HMAC works correctly.")
    else:
        print("✗ FAILED! HMAC doesn't match expected value.")

except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()