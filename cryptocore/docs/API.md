Переделываю API.md и USERGUIDE.md под реальную структуру твоего проекта:

---

## `API.md`

# CryptoCore API Documentation

## Overview
CryptoCore provides cryptographic primitives implemented from scratch in Python. This is an educational project demonstrating how cryptographic algorithms work internally.

## Module Structure
```
src/
├── aes.py              # AES block cipher implementation
├── modes/              # Encryption modes
│   ├── cbc.py         # CBC mode
│   ├── ctr.py         # CTR mode
│   ├── gcm.py         # GCM mode (authenticated encryption)
│   └── ...            # Other modes
├── hash/               # Hash functions
│   ├── sha256.py      # SHA-256 implementation
│   └── sha3_256.py    # SHA3-256 (via hashlib)
├── mac/                # Message Authentication Codes
│   └── hmac.py        # HMAC implementation
├── kdf/                # Key Derivation Functions
│   ├── pbkdf2.py      # PBKDF2 implementation
│   └── hkdf.py        # Key hierarchy
└── main.py            # CLI entry point
```

## AES Encryption

### Class: `AES` (from `src/aes.py`)
```python
class AES:
    """AES block cipher implementation (128-bit only)"""
    
    def __init__(self, key: bytes):
        """
        Initialize AES with a 16-byte key.
        
        Args:
            key: 16-byte encryption key
        """
        
    def encrypt_block(self, plaintext: bytes) -> bytes:
        """
        Encrypt a single 16-byte block.
        
        Args:
            plaintext: 16-byte block to encrypt
            
        Returns:
            16-byte encrypted block
        """
        
    def decrypt_block(self, ciphertext: bytes) -> bytes:
        """
        Decrypt a single 16-byte block.
        
        Args:
            ciphertext: 16-byte block to decrypt
            
        Returns:
            16-byte decrypted block
        """
```

**Example:**
```python
from src.aes import AES

# 16-byte key (128-bit AES)
key = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
aes = AES(key)

# Encrypt a single block
plaintext = b'hello world!!!!!'  # Must be exactly 16 bytes
ciphertext = aes.encrypt_block(plaintext)
decrypted = aes.decrypt_block(ciphertext)
assert plaintext == decrypted
```

## Encryption Modes

### CBC Mode (from `src/modes/cbc.py`)
```python
class CBCMode:
    """Cipher Block Chaining mode"""
    
    def __init__(self, aes: AES, iv: bytes):
        """
        Initialize CBC mode.
        
        Args:
            aes: AES instance
            iv: 16-byte initialization vector
        """
        
    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Encrypt data using CBC mode.
        
        Args:
            plaintext: Data to encrypt (any length)
            
        Returns:
            IV + ciphertext
        """
        
    def decrypt(self, data: bytes) -> bytes:
        """
        Decrypt data using CBC mode.
        
        Args:
            data: IV + ciphertext
            
        Returns:
            Plaintext
        """
```

**Example:**
```python
from src.aes import AES
from src.modes.cbc import CBCMode

key = b'0' * 16
iv = b'1' * 16

aes = AES(key)
cbc = CBCMode(aes, iv)

plaintext = b"This is a test message for CBC encryption!"
ciphertext = cbc.encrypt(plaintext)  # Includes IV at beginning
decrypted = cbc.decrypt(ciphertext)
assert plaintext == decrypted
```

### GCM Mode (from `src/modes/gcm.py`)
```python
class GCM:
    """Galois/Counter Mode - Authenticated Encryption"""
    
    def __init__(self, key: bytes, nonce: bytes = None):
        """
        Initialize GCM mode.
        
        Args:
            key: 16-byte AES key
            nonce: 12-byte nonce (generated if None)
        """
        
    def encrypt(self, plaintext: bytes, aad: bytes = b"") -> bytes:
        """
        Encrypt and authenticate data.
        
        Args:
            plaintext: Data to encrypt
            aad: Additional Authenticated Data (not encrypted)
            
        Returns:
            nonce + ciphertext + tag (12 + len(ciphertext) + 16 bytes)
        """
        
    def decrypt(self, data: bytes, aad: bytes = b"") -> bytes:
        """
        Decrypt and verify authentication.
        
        Args:
            data: nonce + ciphertext + tag
            aad: Additional Authenticated Data
            
        Returns:
            Plaintext
            
        Raises:
            AuthenticationError: If authentication fails
        """
```

**Example:**
```python
from src.modes.gcm import GCM

key = b'\x00' * 16
gcm = GCM(key)

plaintext = b"Sensitive data"
aad = b"metadata:user123"  # Authenticated but not encrypted

# Encrypt with authentication
encrypted = gcm.encrypt(plaintext, aad=aad)

# Decrypt and verify
try:
    decrypted = gcm.decrypt(encrypted, aad=aad)
    print("Authentication successful")
except AuthenticationError:
    print("Authentication failed - data may be tampered")
```

## Hash Functions

### SHA-256 (from `src/hash/sha256.py`)
```python
def sha256(data: bytes) -> bytes:
    """
    Compute SHA-256 hash of data.
    
    Args:
        data: Input data
        
    Returns:
        32-byte hash value
    """
```

**Example:**
```python
from src.hash.sha256 import sha256

data = b"hello world"
hash_value = sha256(data)
print(f"SHA-256: {hash_value.hex()}")
# Output: b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9
```

### SHA3-256 (from `src/hash/sha3_256.py`)
```python
def sha3_256(data: bytes) -> bytes:
    """
    Compute SHA3-256 hash of data (via hashlib).
    
    Args:
        data: Input data
        
    Returns:
        32-byte hash value
    """
```

## HMAC (from `src/mac/hmac.py`)
```python
def hmac_sha256(key: bytes, message: bytes) -> bytes:
    """
    Compute HMAC-SHA256 of message.
    
    Args:
        key: Secret key
        message: Message to authenticate
        
    Returns:
        32-byte HMAC value
    """
```

**Example:**
```python
from src.mac.hmac import hmac_sha256

key = b"secret_key"
message = b"important message"

mac = hmac_sha256(key, message)
print(f"HMAC: {mac.hex()}")
```

## Key Derivation Functions

### PBKDF2 (from `src/kdf/pbkdf2.py`)
```python
def pbkdf2_hmac_sha256(password: Union[str, bytes], 
                       salt: Union[str, bytes], 
                       iterations: int, 
                       dklen: int) -> bytes:
    """
    Derive key using PBKDF2-HMAC-SHA256.
    
    Args:
        password: Password string or bytes
        salt: Salt string or bytes
        iterations: Number of iterations (recommended: 100,000+)
        dklen: Desired key length in bytes
        
    Returns:
        Derived key
    """
```

**Example:**
```python
from src.kdf.pbkdf2 import pbkdf2_hmac_sha256

password = "MySecurePassword123!"
salt = b"unique_salt_value"
iterations = 100000
dklen = 32  # 256-bit key

derived_key = pbkdf2_hmac_sha256(password, salt, iterations, dklen)
print(f"Derived key: {derived_key.hex()}")
```

### Key Hierarchy (from `src/kdf/hkdf.py`)
```python
def derive_key(master_key: bytes, context: str, length: int = 32) -> bytes:
    """
    Derive specific key from master key using HMAC.
    
    Args:
        master_key: Master key bytes
        context: Unique context string (e.g., "encryption", "authentication")
        length: Desired key length
        
    Returns:
        Derived key
    """
```

**Example:**
```python
from src.kdf.hkdf import derive_key

master_key = b'\x00' * 32  # 256-bit master key

# Derive different keys for different purposes
encryption_key = derive_key(master_key, "encryption", 32)
auth_key = derive_key(master_key, "authentication", 32)
```

## Random Number Generation (from `src/csprng.py`)
```python
def get_random_bytes(size: int) -> bytes:
    """
    Get cryptographically secure random bytes.
    
    Args:
        size: Number of bytes to generate
        
    Returns:
        Random bytes
    """
```

## Error Classes
```python
from src.modes.gcm import AuthenticationError

try:
    data = gcm.decrypt(ciphertext, aad=aad)
except AuthenticationError:
    print("Authentication failed - possible tampering")
```

## Security Notes

### Critical Warnings:
1. **Never reuse nonces in GCM** - reusing nonce with same key breaks security
2. **Always verify authentication** before using decrypted data
3. **Use strong keys** - at least 128 bits of entropy
4. **Minimum 100,000 iterations for PBKDF2** for modern systems

### Best Practices:
```python
# ✅ Good practice
gcm = GCM(key)
ciphertext = gcm.encrypt(data, aad=metadata)
try:
    decrypted = gcm.decrypt(ciphertext, aad=metadata)
except AuthenticationError:
    # Handle authentication failure
    pass

# ❌ Bad practice (don't do this)
# - Using ECB mode for real data
# - Reusing nonces in GCM
# - Hardcoding keys in source code
```

## Complete Example
```python
from src.kdf.pbkdf2 import pbkdf2_hmac_sha256
from src.modes.gcm import GCM
import os

# 1. Derive key from password
salt = os.urandom(16)
key = pbkdf2_hmac_sha256(
    password="UserPassword123!",
    salt=salt,
    iterations=150000,
    dklen=32
)

# 2. Encrypt sensitive data
gcm = GCM(key[:16])  # Use first 16 bytes for AES-128
sensitive_data = b"Credit card: 1234-5678-9012-3456"
metadata = b"user_id:123|timestamp:2024-01-15"

ciphertext = gcm.encrypt(sensitive_data, aad=metadata)

# 3. Decrypt and verify
try:
    decrypted = gcm.decrypt(ciphertext, aad=metadata)
    print(f"Decrypted: {decrypted.decode()}")
except AuthenticationError:
    print("Security alert: Authentication failed!")
```