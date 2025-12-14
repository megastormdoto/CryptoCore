"""
Authenticated Encryption with Associated Data (AEAD)
"""
from .encrypt_then_mac import EncryptThenMAC, AuthenticationError

__all__ = ['EncryptThenMAC', 'AuthenticationError']