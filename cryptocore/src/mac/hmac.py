# src/mac/hmac.py
"""
HMAC (Hash-based Message Authentication Code) implementation
Follows RFC 2104 specification
"""


class HMAC:
    """HMAC implementation using SHA-256 or SHA3-256"""

    BLOCK_SIZE = 64  # bytes for SHA-256/SHA3-256

    def __init__(self, key: bytes, hash_class):
        """
        Initialize HMAC with a key

        Args:
            key: The secret key as bytes
            hash_class: Hash class (SHA256 or SHA3_256)
        """
        self.hash_class = hash_class
        self.key = self._process_key(key)

    def _process_key(self, key: bytes) -> bytes:
        """
        Process the key according to RFC 2104:
        - If key is longer than block size: hash it
        - If key is shorter than block size: pad with zeros
        """
        # If key is longer than block size, hash it
        if len(key) > self.BLOCK_SIZE:
            hasher = self.hash_class()
            hasher.update(key)
            key = hasher.digest()

        # If key is shorter than block size, pad with zeros
        if len(key) < self.BLOCK_SIZE:
            key = key + b'\x00' * (self.BLOCK_SIZE - len(key))

        return key

    def _xor_bytes(self, a: bytes, b: bytes) -> bytes:
        """XOR two byte strings of equal length"""
        return bytes(x ^ y for x, y in zip(a, b))

    def compute(self, message: bytes) -> bytes:
        """
        Compute HMAC for the given message

        Args:
            message: Input message as bytes

        Returns:
            HMAC value as bytes
        """
        # Create inner and outer pads
        ipad = self._xor_bytes(self.key, b'\x36' * self.BLOCK_SIZE)
        opad = self._xor_bytes(self.key, b'\x5c' * self.BLOCK_SIZE)

        # Inner hash: H((K ⊕ ipad) ∥ message)
        inner_hasher = self.hash_class()
        inner_hasher.update(ipad)
        inner_hasher.update(message)
        inner_hash = inner_hasher.digest()

        # Outer hash: H((K ⊕ opad) ∥ inner_hash)
        outer_hasher = self.hash_class()
        outer_hasher.update(opad)
        outer_hasher.update(inner_hash)

        return outer_hasher.digest()

    def compute_hex(self, message: bytes) -> str:
        """Compute HMAC and return as hexadecimal string"""
        return self.compute(message).hex()

    def compute_file(self, file_path: str) -> bytes:
        """
        Compute HMAC for a file (processes in chunks for memory efficiency)

        Args:
            file_path: Path to input file

        Returns:
            HMAC value as bytes
        """
        # Create inner and outer pads
        ipad = self._xor_bytes(self.key, b'\x36' * self.BLOCK_SIZE)
        opad = self._xor_bytes(self.key, b'\x5c' * self.BLOCK_SIZE)

        # Inner hash: H((K ⊕ ipad) ∥ message)
        inner_hasher = self.hash_class()
        inner_hasher.update(ipad)

        # Read file in chunks (for memory efficiency with large files)
        chunk_size = 65536  # 64KB chunks
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                inner_hasher.update(chunk)

        inner_hash = inner_hasher.digest()

        # Outer hash: H((K ⊕ opad) ∥ inner_hash)
        outer_hasher = self.hash_class()
        outer_hasher.update(opad)
        outer_hasher.update(inner_hash)

        return outer_hasher.digest()

    def compute_file_hex(self, file_path: str) -> str:
        """Compute HMAC for a file and return as hexadecimal string"""
        return self.compute_file(file_path).hex()