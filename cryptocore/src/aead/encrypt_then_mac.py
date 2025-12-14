import os
import hmac
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from src.core.ciphers import AES
from src.modes.ctr import CTR


class AuthenticationError(Exception):
    """Exception raised when authentication fails."""
    pass


class EncryptThenMAC:
    """Encrypt-then-MAC authenticated encryption."""

    def __init__(self, key: bytes, mode_class, mode_args=None):
        """
        Initialize EncryptThenMAC.

        Args:
            key: Master key (will be split into encryption and MAC keys)
            mode_class: Block cipher mode class (e.g., CTR)
            mode_args: Arguments for the mode constructor
        """
        if len(key) < 32:
            # For AES-128, we need 32 bytes (16 for encryption, 16 for MAC)
            raise ValueError("Key must be at least 32 bytes for Encrypt-then-MAC")

        # Derive separate keys using HKDF
        hkdf = HKDF(
            algorithm=SHA256(),
            length=32,
            salt=None,
            info=b'encrypt_then_mac_key_separation'
        )
        derived_key = hkdf.derive(key)

        self.enc_key = derived_key[:16]
        self.mac_key = derived_key[16:]

        # Initialize encryption mode
        mode_args = mode_args or {}
        self.cipher = mode_class(self.enc_key, **mode_args)

    def encrypt(self, plaintext: bytes, aad: bytes = b"") -> bytes:
        """Encrypt then MAC."""
        # Encrypt
        ciphertext = self.cipher.encrypt(plaintext)

        # Compute MAC over ciphertext || AAD
        mac_data = ciphertext + aad
        tag = hmac.new(self.mac_key, mac_data, 'sha256').digest()[:16]

        return ciphertext + tag

    def decrypt(self, data: bytes, aad: bytes = b"") -> bytes:
        """Verify MAC then decrypt."""
        if len(data) < 16:
            raise AuthenticationError("Data too short to contain tag")

        ciphertext = data[:-16]
        received_tag = data[-16:]

        # Verify MAC
        mac_data = ciphertext + aad
        expected_tag = hmac.new(self.mac_key, mac_data, 'sha256').digest()[:16]

        if not hmac.compare_digest(received_tag, expected_tag):
            raise AuthenticationError("Authentication failed: MAC mismatch")

        # Decrypt
        return self.cipher.decrypt(ciphertext)