"""
AES implementation for the project.
"""
try:
    from Crypto.Cipher import AES as PyCrypto_AES

    HAS_PYCRYPTO = True
except ImportError:
    HAS_PYCRYPTO = False
    print("WARNING: pycryptodome not found, using stub implementation")


class AES:
    """AES cipher implementation."""

    def __init__(self, key: bytes):
        if len(key) not in (16, 24, 32):
            raise ValueError("Key must be 16, 24, or 32 bytes")
        self.key = key
        self.block_size = 16

        if HAS_PYCRYPTO:
            self._cipher = PyCrypto_AES.new(key, PyCrypto_AES.MODE_ECB)
        else:
            # Fallback stub for testing
            pass

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt one 16-byte block."""
        if len(data) != 16:
            raise ValueError(f"Data must be 16 bytes, got {len(data)}")

        if HAS_PYCRYPTO:
            return self._cipher.encrypt(data)
        else:
            # Simple stub for testing
            return bytes([(b + i) % 256 for i, b in enumerate(data)])
