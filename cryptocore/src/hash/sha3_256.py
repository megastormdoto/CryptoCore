#!/usr/bin/env python3
import hashlib


class SHA3_256:
    """SHA3-256 implementation using Python's hashlib"""

    def __init__(self):
        self._hasher = hashlib.sha3_256()

    def update(self, data):
        """Update hash with new data"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        self._hasher.update(data)

    def digest(self):
        """Return final hash digest as bytes"""
        return self._hasher.digest()

    def hexdigest(self):
        """Return final hash as hexadecimal string"""
        return self._hasher.hexdigest()

    def hash(self, data):
        """Convenience method to hash data in one call"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha3_256(data).hexdigest()


# Convenience function
def sha3_256(data):
    """Compute SHA3-256 hash of data"""
    hasher = SHA3_256()
    return hasher.hash(data)


if __name__ == '__main__':
    # Quick test
    hasher = SHA3_256()
    print("Testing SHA3-256 implementation:")

    # Test with empty string
    empty_hash = hasher.hash(b"")
    print(f"Empty string: {empty_hash}")
    expected_empty = "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a"
    print(f"Expected:     {expected_empty}")
    print(f"Match: {empty_hash == expected_empty}")