#!/usr/bin/env python3
import struct
import binascii


class SHA256:
    """SHA-256 implementation from scratch following NIST FIPS 180-4"""

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset the hasher to initial state"""
        # Initialize hash values (first 32 bits of fractional parts of square roots of first 8 primes)
        self.h = [
            0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
            0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
        ]

        # Initialize round constants (first 32 bits of fractional parts of cube roots of first 64 primes)
        self.k = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]

        self.unprocessed = b''  # Unprocessed bytes
        self.message_length = 0  # Total message length in bits
        self._finalized = False

    @staticmethod
    def _right_rotate(x, n):
        """Right rotate a 32-bit integer"""
        return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

    @staticmethod
    def _right_shift(x, n):
        """Right shift a 32-bit integer"""
        return (x >> n) & 0xFFFFFFFF

    def _sha256_padding(self, message_length):
        """Implement SHA-256 padding scheme"""
        # Calculate total message length in bits
        message_length_bits = message_length * 8

        # Append bit '1' (0x80 = 10000000 in binary)
        padding = b'\x80'

        # Calculate how many zeros we need
        # We need: (message_length_bits + 1 + k) ≡ 448 mod 512
        # So: k = (448 - (message_length_bits + 1)) mod 512
        # But we work in bytes, so: zeros_needed_bytes = (448 - (message_length_bits + 1)) // 8 mod 64

        # Current length in bits after adding '1'
        current_bits = message_length_bits + 8  # +8 for the 0x80 byte

        # Calculate padding zeros (in bits)
        zeros_needed_bits = (448 - (current_bits % 512)) % 512
        if zeros_needed_bits < 0:
            zeros_needed_bits += 512

        # Convert to bytes
        zeros_needed_bytes = zeros_needed_bits // 8

        padding += b'\x00' * zeros_needed_bytes

        # Append 64-bit message length (big-endian)
        padding += struct.pack('>Q', message_length_bits)

        return padding

    def _process_block(self, block):
        """Process one 512-bit block"""
        # Prepare message schedule
        w = [0] * 64

        # Copy block into first 16 words (big-endian)
        for i in range(16):
            w[i] = struct.unpack('>I', block[i * 4:(i + 1) * 4])[0]

        # Extend the schedule
        for i in range(16, 64):
            s0 = self._right_rotate(w[i - 15], 7) ^ self._right_rotate(w[i - 15], 18) ^ self._right_shift(w[i - 15], 3)
            s1 = self._right_rotate(w[i - 2], 17) ^ self._right_rotate(w[i - 2], 19) ^ self._right_shift(w[i - 2], 10)
            w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & 0xFFFFFFFF

        # Initialize working variables with current hash values
        a, b, c, d, e, f, g, h = self.h

        # Compression function main loop
        for i in range(64):
            s1 = self._right_rotate(e, 6) ^ self._right_rotate(e, 11) ^ self._right_rotate(e, 25)
            ch = (e & f) ^ ((~e) & g)
            temp1 = (h + s1 + ch + self.k[i] + w[i]) & 0xFFFFFFFF

            s0 = self._right_rotate(a, 2) ^ self._right_rotate(a, 13) ^ self._right_rotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (s0 + maj) & 0xFFFFFFFF

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF

        # Add compressed chunk to current hash value
        self.h[0] = (self.h[0] + a) & 0xFFFFFFFF
        self.h[1] = (self.h[1] + b) & 0xFFFFFFFF
        self.h[2] = (self.h[2] + c) & 0xFFFFFFFF
        self.h[3] = (self.h[3] + d) & 0xFFFFFFFF
        self.h[4] = (self.h[4] + e) & 0xFFFFFFFF
        self.h[5] = (self.h[5] + f) & 0xFFFFFFFF
        self.h[6] = (self.h[6] + g) & 0xFFFFFFFF
        self.h[7] = (self.h[7] + h) & 0xFFFFFFFF

    def update(self, data):
        """Update hash with new data"""
        if self._finalized:
            raise RuntimeError("Cannot update after digest")

        if isinstance(data, str):
            data = data.encode('utf-8')

        # Update message length
        self.message_length += len(data)

        # Combine with any unprocessed data from previous update
        data = self.unprocessed + data

        # Process complete 64-byte blocks
        num_blocks = len(data) // 64
        for i in range(num_blocks):
            block = data[i * 64:(i + 1) * 64]
            self._process_block(block)

        # Save unprocessed bytes for next update
        self.unprocessed = data[num_blocks * 64:]

    def digest(self):
        """Return final hash digest as bytes"""
        if self._finalized:
            return self._digest_cache

        # Make a copy of current state
        h_final = self.h.copy()
        unprocessed_final = self.unprocessed
        length_final = self.message_length

        # Apply padding
        padding = self._sha256_padding(length_final)
        padded_data = unprocessed_final + padding

        # Process padded data
        num_blocks = len(padded_data) // 64
        for i in range(num_blocks):
            block = padded_data[i * 64:(i + 1) * 64]

            # Process this block
            self._process_block(block)

        # Get final hash
        digest_bytes = b''.join(struct.pack('>I', h) for h in self.h)

        # Restore state (for potential additional operations)
        self.h = h_final
        self.unprocessed = unprocessed_final
        self.message_length = length_final
        self._finalized = True
        self._digest_cache = digest_bytes

        return digest_bytes

    def hexdigest(self):
        """Return final hash as hexadecimal string"""
        return self.digest().hex()

    def hash(self, data):
        """Convenience method to hash data in one call"""
        self.reset()
        self.update(data)
        return self.hexdigest()


# Convenience function
def sha256(data):
    """Compute SHA-256 hash of data"""
    hasher = SHA256()
    return hasher.hash(data)


if __name__ == '__main__':
    # Comprehensive test
    import hashlib

    print("🧪 Комплексный тест SHA-256")
    print("=" * 60)

    test_cases = [
        (b"", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "Пустая строка"),
        (b"a", "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb", "Буква 'a'"),
        (b"ab", "fb8e20fc2e4c3f248c60c39bd652f3c1347298bb977b8b4d5903b85055620603", "Строка 'ab'"),
        (b"abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad", "Строка 'abc'"),
        (b"abcd", "88d4266fd4e6338d13b845fcf289579d209c897823b9217da3e161936f031589", "Строка 'abcd'"),
        (b"hello", "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824", "Строка 'hello'"),
        (b"hello world", "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9", "Строка 'hello world'"),
        (b"The quick brown fox jumps over the lazy dog",
         "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592",
         "Известный тест"),
    ]

    all_pass = True
    for data, expected, description in test_cases:
        hasher = SHA256()
        result = hasher.hash(data)

        # Also compare with hashlib
        lib_hash = hashlib.sha256(data).hexdigest()

        match = (result == expected) and (result == lib_hash)
        all_pass = all_pass and match

        status = "✅" if match else "❌"
        print(f"{status} {description}")

        if not match:
            print(f"   Ожидалось: {expected}")
            print(f"   Получено:  {result}")
            print(f"   hashlib:   {lib_hash}")
            print(f"   Совпадает с ожидаемым: {result == expected}")
            print(f"   Совпадает с hashlib: {result == lib_hash}")

    print("\n" + "=" * 60)
    if all_pass:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
    else:
        print("💥 Есть ошибки!")