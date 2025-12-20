# tests/hex_utils.py
def string_to_hex(s):
    """Convert string to hex"""
    return s.encode('utf-8').hex()

def hex_to_string(h):
    """Convert hex to string"""
    return bytes.fromhex(h).decode('utf-8', errors='ignore')

if __name__ == "__main__":
    # Test conversion
    test_string = "testaad123456"
    hex_string = string_to_hex(test_string)
    print(f"String: '{test_string}'")
    print(f"Hex: {hex_string}")
    print(f"Back to string: '{hex_to_string(hex_string)}'")