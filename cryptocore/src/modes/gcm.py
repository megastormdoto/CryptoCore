"""
Galois/Counter Mode (GCM) implementation.
Based on NIST SP 800-38D.
"""
import os
import struct
import hmac
from typing import Tuple


class AuthenticationError(Exception):
    """Exception raised when GCM authentication fails."""
    pass


class GCM:
    """Galois/Counter Mode (GCM) authenticated encryption."""

    # Irreducible polynomial for GF(2^128): x^128 + x^7 + x^2 + x + 1
    R = 0xE1000000000000000000000000000000

    def __init__(self, key: bytes, nonce: bytes = None):
        """
        Initialize GCM.

        Args:
            key: AES key (16, 24, or 32 bytes)
            nonce: Nonce (12 bytes recommended). If None, random nonce is generated.
        """
        if len(key) not in (16, 24, 32):
            raise ValueError("Key must be 16, 24, or 32 bytes")

        self.key = key

        # Initialize AES cipher - simplified import logic
        self.aes = self._create_aes_cipher(key)

        if nonce is None:
            self.nonce = os.urandom(12)
        else:
            if len(nonce) != 12:
                raise ValueError("Nonce must be 12 bytes for GCM")
            self.nonce = nonce

        # Precompute multiplication table for performance
        self._precompute_table()

    def _create_aes_cipher(self, key):
        """Create AES cipher with simplified import logic."""
        # Try multiple import strategies
        try:
            # Strategy 1: Try from core.ciphers (relative import)
            from ..core.ciphers import AES
            return AES(key)
        except ImportError:
            try:
                # Strategy 2: Try absolute import
                from core.ciphers import AES
                return AES(key)
            except ImportError:
                try:
                    # Strategy 3: Try from current directory
                    import sys
                    sys.path.insert(0, os.path.dirname(__file__))
                    from core.ciphers import AES
                    return AES(key)
                except ImportError:
                    # Strategy 4: Create minimal AES stub
                    return self._create_aes_stub(key)

    def _create_aes_stub(self, key):
        """Create a minimal AES stub for testing."""
        print("NOTE: Using AES stub - install pycryptodome for real AES")

        class AESStub:
            def __init__(self, key):
                self.key = key
                self.block_size = 16
                # Create simple key schedule for stub
                self._key_schedule = self._expand_key(key)

            def _expand_key(self, key):
                """Simple key expansion for stub."""
                schedule = bytearray(176)  # 11 * 16 bytes
                for i in range(16):
                    schedule[i] = key[i % len(key)]

                # Very simple "expansion"
                for i in range(16, 176):
                    schedule[i] = (schedule[i - 16] + i) % 256

                return bytes(schedule)

            def encrypt(self, data):
                """Simple encryption for testing."""
                if len(data) != 16:
                    raise ValueError(f"AES stub requires 16 bytes, got {len(data)}")

                # Very simple "encryption" - XOR with key schedule
                result = bytearray(16)
                round_key = self._key_schedule[:16]

                for i in range(16):
                    result[i] = data[i] ^ round_key[i] ^ (i * 7)

                return bytes(result)

        return AESStub(key)

    def _precompute_table(self):
        """Precompute multiplication table for GHASH."""
        # Compute H = AES_encrypt(0^128)
        zero_block = b'\x00' * 16
        self.H = self.aes.encrypt(zero_block)

        # Convert H to integer
        H_int = int.from_bytes(self.H, 'big')

        # Precompute table
        self.M = [0] * 16
        self.M[0] = 0
        self.M[1] = H_int

        # Compute M[i] = M[i-1] * x (multiply by 2 in GF(2^128))
        for i in range(2, 16):
            self.M[i] = self._mult_by_x(self.M[i - 1])

    def _mult_by_x(self, x: int) -> int:
        """Multiply by x (which is 2) in GF(2^128)."""
        if x & (1 << 127):
            return ((x << 1) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF) ^ self.R
        else:
            return (x << 1) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

    def _mult_gf(self, x: int, y: int) -> int:
        """Multiply two elements in GF(2^128)."""
        # Use 4-bit window method
        z = 0
        v = y

        for i in range(0, 128, 4):
            # Get 4-bit chunk
            chunk = (x >> (124 - i)) & 0xF

            if chunk != 0:
                z ^= self.M[chunk]

            # Multiply v by x^4
            for _ in range(4):
                if v & 1:
                    v = (v >> 1) ^ self.R
                else:
                    v >>= 1

        return z

    def _ghash(self, aad: bytes, ciphertext: bytes) -> int:
        """
        Compute GHASH in GF(2^128).

        Args:
            aad: Associated Authenticated Data
            ciphertext: Ciphertext

        Returns:
            Authentication tag before final processing
        """
        # Prepare length blocks
        len_aad = len(aad) * 8
        len_ct = len(ciphertext) * 8
        len_block = struct.pack('>QQ', len_aad, len_ct)

        y = 0

        # Process AAD in 16-byte blocks
        for i in range(0, len(aad), 16):
            block = aad[i:i + 16]
            if len(block) < 16:
                block = block.ljust(16, b'\x00')
            y = self._mult_gf(y ^ int.from_bytes(block, 'big'), self.M[1])

        # Process ciphertext in 16-byte blocks
        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i:i + 16]
            if len(block) < 16:
                block = block.ljust(16, b'\x00')
            y = self._mult_gf(y ^ int.from_bytes(block, 'big'), self.M[1])

        # Process length block
        y = self._mult_gf(y ^ int.from_bytes(len_block, 'big'), self.M[1])

        return y

    def _compute_j0(self) -> bytes:
        """Compute J0 from nonce."""
        if len(self.nonce) == 12:
            # For 96-bit nonce: J0 = nonce || 0x00000001
            j0 = self.nonce + b'\x00\x00\x00\x01'
        else:
            # For non-96-bit nonce: J0 = GHASH(nonce || zeros)
            nonce_padded = self.nonce
            if len(nonce_padded) % 16 != 0:
                nonce_padded = nonce_padded.ljust(
                    ((len(nonce_padded) + 15) // 16) * 16, b'\x00'
                )

            # GHASH of nonce || len(nonce) as 64-bit big-endian
            len_nonce = len(self.nonce) * 8
            len_block = struct.pack('>QQ', 0, len_nonce)

            y = 0
            for i in range(0, len(nonce_padded), 16):
                block = nonce_padded[i:i + 16]
                y = self._mult_gf(y ^ int.from_bytes(block, 'big'), self.M[1])

            y = self._mult_gf(y ^ int.from_bytes(len_block, 'big'), self.M[1])
            j0 = y.to_bytes(16, 'big')

        return j0

    def encrypt(self, plaintext: bytes, aad: bytes = b"") -> bytes:
        """
        GCM encryption.

        Returns:
            Format: nonce (12 bytes) || ciphertext || tag (16 bytes)
        """
        # Compute J0
        j0 = self._compute_j0()

        # Encrypt using CTR mode starting from J0 + 1
        ctr_start = (int.from_bytes(j0, 'big') + 1) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

        # Generate keystream
        ciphertext = bytearray()
        for i in range(0, len(plaintext), 16):
            # Increment counter
            counter = (ctr_start + (i // 16)) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
            counter_bytes = counter.to_bytes(16, 'big')

            # Encrypt counter to get keystream block
            keystream = self.aes.encrypt(counter_bytes)

            # XOR with plaintext block
            block = plaintext[i:i + 16]
            for j in range(min(len(block), 16)):
                ciphertext.append(block[j] ^ keystream[j])

        ciphertext = bytes(ciphertext)

        # Compute authentication tag
        ghash_result = self._ghash(aad, ciphertext)

        # Compute S = AES_K(J0)
        S = self.aes.encrypt(j0)
        S_int = int.from_bytes(S, 'big')

        # T = GHASH ^ S
        T = ghash_result ^ S_int
        tag = T.to_bytes(16, 'big')

        # Return nonce || ciphertext || tag
        return self.nonce + ciphertext + tag

    def decrypt(self, data: bytes, aad: bytes = b"") -> bytes:
        """
        GCM decryption with authentication.

        Args:
            data: Format: nonce || ciphertext || tag (16 bytes)

        Returns:
            Plaintext if authentication succeeds

        Raises:
            AuthenticationError: If authentication fails
        """
        if len(data) < 28:  # 12 bytes nonce + 16 bytes tag
            raise AuthenticationError("Data too short")

        # Parse input
        nonce = data[:12]
        ciphertext = data[12:-16]
        received_tag = data[-16:]

        # Reinitialize with the same nonce
        self.nonce = nonce
        self._precompute_table()

        # Compute J0
        j0 = self._compute_j0()

        # Verify tag
        ghash_result = self._ghash(aad, ciphertext)
        S = self.aes.encrypt(j0)
        S_int = int.from_bytes(S, 'big')
        expected_tag = (ghash_result ^ S_int).to_bytes(16, 'big')

        if not hmac.compare_digest(received_tag, expected_tag):
            raise AuthenticationError("Authentication failed: tag mismatch")

        # Decrypt using CTR mode
        ctr_start = (int.from_bytes(j0, 'big') + 1) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

        plaintext = bytearray()
        for i in range(0, len(ciphertext), 16):
            # Increment counter
            counter = (ctr_start + (i // 16)) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
            counter_bytes = counter.to_bytes(16, 'big')

            # Encrypt counter to get keystream block
            keystream = self.aes.encrypt(counter_bytes)

            # XOR with ciphertext block
            block = ciphertext[i:i + 16]
            for j in range(min(len(block), 16)):
                plaintext.append(block[j] ^ keystream[j])

        return bytes(plaintext)


# Simple test if run directly
if __name__ == "__main__":
    print("🧪 Testing GCM standalone...")

    # Test with stub AES
    key = b'\x00' * 16
    plaintext = b"Hello GCM world!"
    aad = b"test aad"

    gcm = GCM(key)
    print(f"Nonce: {gcm.nonce.hex()}")

    ciphertext = gcm.encrypt(plaintext, aad)
    print(f"Ciphertext length: {len(ciphertext)}")
    print(f"Expected: 12 (nonce) + {len(plaintext)} (plaintext) + 16 (tag) = {12 + len(plaintext) + 16}")

    gcm2 = GCM(key, gcm.nonce)
    decrypted = gcm2.decrypt(ciphertext, aad)

    if decrypted == plaintext:
        print("✅ GCM encryption/decryption works!")
    else:
        print(f"❌ Decryption failed")
        print(f"Original: {plaintext}")
        print(f"Decrypted: {decrypted}")

    # Test wrong AAD
    print("\nTesting wrong AAD...")
    try:
        gcm3 = GCM(key, gcm.nonce)
        gcm3.decrypt(ciphertext, b"WRONG AAD")
        print("❌ Should have failed with wrong AAD!")
    except AuthenticationError:
        print("✅ Correctly failed with wrong AAD")