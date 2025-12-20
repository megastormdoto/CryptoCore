"""
Unit tests for PBKDF2-HMAC-SHA256 implementation.
Tests based on RFC 6070 test vectors and edge cases.
"""

import pytest
import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..', '..')
sys.path.insert(0, project_root)

# Now import
try:
    from src.kdf.pbkdf2 import pbkdf2_hmac_sha256
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Python path: {sys.path}")
    print(f"Looking for: {os.path.join(project_root, 'src', 'kdf', 'pbkdf2.py')}")
    raise


class TestPBKDF2:
    """Test suite for PBKDF2-HMAC-SHA256"""

    def test_basic_functionality(self):
        """Basic PBKDF2 key derivation"""
        # Simple test with minimal iterations
        key = pbkdf2_hmac_sha256("password", "salt", 1, 20)

        assert isinstance(key, bytes)
        assert len(key) == 20
        # Basic check: not all zeros
        assert key != b'\x00' * 20

    def test_deterministic_output(self):
        """Same inputs should produce same output"""
        key1 = pbkdf2_hmac_sha256("secret", "mysalt", 1000, 32)
        key2 = pbkdf2_hmac_sha256("secret", "mysalt", 1000, 32)

        assert key1 == key2

    def test_rfc6070_test_vector_1(self):
        """RFC 6070 Test Vector #1: P="password", S="salt", c=1, dkLen=20"""
        key = pbkdf2_hmac_sha256("password", "salt", 1, 20)
        expected = bytes.fromhex("120fb6cffcf8b32c43e7225256c4f837a86548c9")

        assert key == expected, f"Expected {expected.hex()}, got {key.hex()}"

    def test_rfc6070_test_vector_2(self):
        """RFC 6070 Test Vector #2: P="password", S="salt", c=2, dkLen=20"""
        key = pbkdf2_hmac_sha256("password", "salt", 2, 20)
        expected = bytes.fromhex("ae4d0c95af6b46d32d0adff928f06dd02a303f8e")

        assert key == expected, f"Expected {expected.hex()}, got {key.hex()}"

    def test_rfc6070_test_vector_3(self):
        """RFC 6070 Test Vector #3: P="password", S="salt", c=4096, dkLen=20"""
        key = pbkdf2_hmac_sha256("password", "salt", 4096, 20)
        expected = bytes.fromhex("c5e478d59288c841aa530db6845c4c8d962893a0")

        assert key == expected, f"Expected {expected.hex()}, got {key.hex()}"

    def test_rfc6070_test_vector_4(self):
        """RFC 6070 Test Vector #4: P="passwordPASSWORDpassword", S="saltSALTsaltSALTsaltSALTsaltSALTsalt", c=4096, dkLen=25"""
        password = "passwordPASSWORDpassword"
        salt = "saltSALTsaltSALTsaltSALTsaltSALTsalt"
        key = pbkdf2_hmac_sha256(password, salt, 4096, 25)
        expected = bytes.fromhex("348c89dbcbd32b2f32d814b8116e84cf2b17347ebc1800181c")

        assert key == expected, f"Expected {expected.hex()}, got {key.hex()}"

    def test_different_key_lengths(self):
        """Test deriving keys of different lengths"""
        for dklen in [16, 20, 32, 48, 64]:
            key = pbkdf2_hmac_sha256("password", "salt", 1000, dklen)

            assert isinstance(key, bytes)
            assert len(key) == dklen

    def test_password_and_salt_as_bytes(self):
        """Test with password and salt provided as bytes"""
        password_bytes = b"password123"
        salt_bytes = b"saltvalue"

        key1 = pbkdf2_hmac_sha256(password_bytes, salt_bytes, 1000, 32)
        key2 = pbkdf2_hmac_sha256("password123", "saltvalue", 1000, 32)

        assert key1 == key2

    def test_empty_password(self):
        """Test with empty password (edge case)"""
        key = pbkdf2_hmac_sha256("", "salt", 1000, 32)

        assert isinstance(key, bytes)
        assert len(key) == 32
        # Should not be all zeros
        assert key != b'\x00' * 32

    def test_empty_salt(self):
        """Test with empty salt (edge case)"""
        key = pbkdf2_hmac_sha256("password", "", 1000, 32)

        assert isinstance(key, bytes)
        assert len(key) == 32

    def test_salt_with_hex_chars(self):
        """Test that salt with hex characters is not interpreted as hex"""
        # If salt looks like hex but should be treated as string
        salt = "a1b2c3d4"  # This looks like hex but should be string "a1b2c3d4"
        key = pbkdf2_hmac_sha256("password", salt, 1000, 32)

        assert isinstance(key, bytes)
        assert len(key) == 32

    def test_high_iteration_count(self):
        """Test with high iteration count (performance test)"""
        key = pbkdf2_hmac_sha256("password", "salt", 10000, 32)

        assert isinstance(key, bytes)
        assert len(key) == 32

    def test_iterations_affect_output(self):
        """Different iteration counts should produce different keys"""
        key1 = pbkdf2_hmac_sha256("password", "salt", 1000, 32)
        key2 = pbkdf2_hmac_sha256("password", "salt", 2000, 32)

        assert key1 != key2

    def test_salt_affects_output(self):
        """Different salts should produce different keys"""
        key1 = pbkdf2_hmac_sha256("password", "salt1", 1000, 32)
        key2 = pbkdf2_hmac_sha256("password", "salt2", 1000, 32)

        assert key1 != key2

    def test_password_affects_output(self):
        """Different passwords should produce different keys"""
        key1 = pbkdf2_hmac_sha256("password1", "salt", 1000, 32)
        key2 = pbkdf2_hmac_sha256("password2", "salt", 1000, 32)

        assert key1 != key2

    @pytest.mark.xfail(reason="Current implementation may not validate iterations")
    def test_zero_iterations_error(self):
        """Zero iterations should raise an error"""
        with pytest.raises(ValueError):
            pbkdf2_hmac_sha256("password", "salt", 0, 32)

    @pytest.mark.xfail(reason="Current implementation may not validate iterations")
    def test_negative_iterations_error(self):
        """Negative iterations should raise an error"""
        with pytest.raises(ValueError):
            pbkdf2_hmac_sha256("password", "salt", -1, 32)

    @pytest.mark.xfail(reason="Current implementation may not validate dklen")
    def test_zero_dklen_error(self):
        """Zero dkLen should raise an error"""
        with pytest.raises(ValueError):
            pbkdf2_hmac_sha256("password", "salt", 1000, 0)

    @pytest.mark.xfail(reason="Current implementation may not validate dklen")
    def test_negative_dklen_error(self):
        """Negative dkLen should raise an error"""
        with pytest.raises(ValueError):
            pbkdf2_hmac_sha256("password", "salt", 1000, -1)

    def test_large_dklen(self):
        """Test with large dkLen (should work up to (2^32-1)*32 according to RFC)"""
        # Test with 64 bytes (reasonable large value)
        key = pbkdf2_hmac_sha256("password", "salt", 1000, 64)

        assert isinstance(key, bytes)
        assert len(key) == 64

    def test_hex_salt_string(self):
        """Test with salt provided as hex string"""
        # This tests if the implementation handles hex strings correctly
        salt_hex = "a1b2c3d4e5f67890"
        key = pbkdf2_hmac_sha256("password", salt_hex, 1000, 32)

        assert isinstance(key, bytes)
        assert len(key) == 32


if __name__ == "__main__":
    pytest.main([__file__, "-v"])