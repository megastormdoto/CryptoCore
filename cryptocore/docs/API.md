# CryptoCore Python API Documentation

## Overview
CryptoCore provides cryptographic primitives implemented in Python.

## Table of Contents
- [AES Encryption](#aes-encryption)
- [Encryption Modes](#encryption-modes)
- [Hash Functions](#hash-functions)
- [HMAC](#hmac)
- [GCM Authenticated Encryption](#gcm-authenticated-encryption)
- [Key Derivation Functions](#key-derivation-functions)

## AES Encryption

### `class AES`
```python
class AES:
    """AES block cipher implementation"""
```

**Methods:**
- `__init__(key: bytes)` - Initialize with 16/24/32 byte key
- `encrypt_block(plaintext: bytes) -> bytes` - Encrypt 16-byte block
- `decrypt_block(ciphertext: bytes) -> bytes` - Decrypt 16-byte block

**Example:**
```python
from cryptocore.aes import AES

key = b'0' * 16
aes = AES(key)
ciphertext = aes.encrypt_block(b'hello world!!!!!')
```

## Encryption Modes

### `CBC` Mode
```python
from cryptocore.modes import cbc_encrypt, cbc_decrypt

ciphertext = cbc_encrypt(key, iv, plaintext)
plaintext = cbc_decrypt(key, iv, ciphertext)
```

### `CTR` Mode
```python
from cryptocore.modes import ctr_encrypt, ctr_decrypt
# CTR encryption/decryption use same function
ciphertext = ctr_encrypt(key, nonce, plaintext)
```

### `GCM` Mode
```python
from cryptocore.modes.gcm import GCM

gcm = GCM(key)
ciphertext = gcm.encrypt(plaintext, aad=aad_data)
plaintext = gcm.decrypt(ciphertext, aad=aad_data)  # Raises AuthenticationError on failure
```

## Hash Functions

### `sha256(data: bytes) -> bytes`
```python
from cryptocore.hash import sha256

hash_value = sha256(b"hello world")
# Returns 32 bytes
```

### `sha3_256(data: bytes) -> bytes`
```python
from cryptocore.hash import sha3_256

hash_value = sha3_256(b"hello world")
# Returns 32 bytes
```

## HMAC

### `hmac_sha256(key: bytes, message: bytes) -> bytes`
```python
from cryptocore.hmac import hmac_sha256

mac = hmac_sha256(b"secret_key", b"message")
# Returns 32-byte HMAC
```

## Key Derivation Functions

### `pbkdf2_hmac_sha256(password, salt, iterations, dklen)`
```python
from cryptocore.kdf import pbkdf2_hmac_sha256

# Derive key from password
key = pbkdf2_hmac_sha256(
    password="MyPassword",
    salt=b"saltvalue",
    iterations=100000,
    dklen=32
)
```

### `derive_key(master_key, context, length)`
```python
from cryptocore.kdf import derive_key

# Key hierarchy: derive specific key from master
encryption_key = derive_key(
    master_key=master_key_bytes,
    context="database_encryption",
    length=32
)
```

## Utility Functions

### Random Number Generation
```python
from cryptocore.random import generate_key, generate_nonce, generate_salt

key = generate_key(32)      # 32 random bytes
nonce = generate_nonce(12)  # 12-byte nonce for GCM
salt = generate_salt(16)    # 16-byte salt for PBKDF2
```

### Padding
```python
from cryptocore.padding import pkcs7_pad, pkcs7_unpad

padded = pkcs7_pad(data, block_size=16)
unpadded = pkcs7_unpad(padded)
```

## Error Classes

```python
from cryptocore.exceptions import (
    CryptoError,
    AuthenticationError,  # Raised by GCM on auth failure
    KeyError,
    DecryptionError
)

try:
    plaintext = gcm.decrypt(ciphertext, aad=aad)
except AuthenticationError:
    print("Authentication failed!")
```

## Security Notes

### Critical Warnings:
1. **Never use ECB mode** for real data (educational purposes only)
2. **Always verify authentication** (HMAC/GCM tag) before using data
3. **Use unique nonces** for GCM - never reuse with same key
4. **Minimum 100,000 iterations** for PBKDF2
5. **Store keys securely** - never in source code

### Best Practices:
```python
# ✅ Good: Use GCM with unique nonce
gcm = GCM(key)
ciphertext = gcm.encrypt(data, aad=metadata)

# ✅ Good: Verify before decrypting
try:
    plaintext = gcm.decrypt(ciphertext, aad=metadata)
except AuthenticationError:
    # Handle tampering
    pass

# ❌ Bad: Using ECB
from cryptocore.modes import ecb_encrypt  # DON'T USE FOR REAL DATA
```

## Complete Example

```python
from cryptocore.kdf import pbkdf2_hmac_sha256
from cryptocore.modes.gcm import GCM
from cryptocore.random import generate_salt

# 1. Derive key from password
salt = generate_salt(16)
key = pbkdf2_hmac_sha256(
    password="UserPassword123!",
    salt=salt,
    iterations=150000,
    dklen=32
)

# 2. Encrypt with GCM
gcm = GCM(key)
ciphertext = gcm.encrypt(
    plaintext=sensitive_data,
    aad=b"user_id:123|timestamp:2024"
)

# 3. Decrypt and authenticate
try:
    decrypted = gcm.decrypt(
        ciphertext=ciphertext,
        aad=b"user_id:123|timestamp:2024"
    )
    print("Success! Data authenticated.")
except AuthenticationError:
    print("WARNING: Data tampered or wrong key!")
