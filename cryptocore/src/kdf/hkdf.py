"""
Key hierarchy implementation for deriving multiple keys from a master key.
Simplified HKDF-style derivation.
"""
from typing import Union

try:
    from src.mac.hmac import hmac_sha256
except ImportError:
    # Fallback for testing
    import hashlib
    import hmac


    def hmac_sha256(key: bytes, msg: bytes) -> bytes:
        """Fallback HMAC-SHA256."""
        return hmac.new(key, msg, hashlib.sha256).digest()


def derive_key(
        master_key: bytes,
        context: Union[str, bytes],
        length: int = 32
) -> bytes:
    """
    Derive a key from a master key using a deterministic HMAC-based method.

    Args:
        master_key: Master key as bytes
        context: Context string identifying the key's purpose
        length: Desired key length in bytes

    Returns:
        Derived key as bytes
    """
    if len(master_key) < 16:
        raise ValueError("Master key should be at least 16 bytes for security")

    if isinstance(context, str):
        context = context.encode('utf-8')

    derived = b''
    counter = 1

    while len(derived) < length:
        # T_i = HMAC(master_key, context || INT_32_BE(counter))
        block_input = context + counter.to_bytes(4, 'big')
        block = hmac_sha256(master_key, block_input)
        derived += block
        counter += 1

    # Return exactly length bytes
    return derived[:length]


def expand_key(
        master_key: bytes,
        context: Union[str, bytes],
        length: int = 32
) -> bytes:
    """
    Alias for derive_key for compatibility.
    """
    return derive_key(master_key, context, length)