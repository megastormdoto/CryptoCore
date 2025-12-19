"""
Compare our PBKDF2 implementation with OpenSSL.
"""
import subprocess
import tempfile
import os
from kdf.pbkdf2 import pbkdf2_hmac_sha256


def test_with_openssl():
    """Test our implementation against OpenSSL."""
    test_cases = [
        {
            'password': 'password',
            'salt': 'salt',
            'iterations': 1,
            'length': 20
        },
        {
            'password': 'password',
            'salt': '73616c74',  # hex for 'salt'
            'iterations': 2,
            'length': 20
        },
        {
            'password': 'test123',
            'salt': 'a1b2c3d4',
            'iterations': 1000,
            'length': 32
        }
    ]

    for i, test in enumerate(test_cases):
        print(f"\nTest case {i + 1}:")
        print(f"  Password: {test['password']}")
        print(f"  Salt: {test['salt']}")
        print(f"  Iterations: {test['iterations']}")
        print(f"  Length: {test['length']}")

        # Our implementation
        our_result = pbkdf2_hmac_sha256(
            test['password'],
            test['salt'],
            test['iterations'],
            test['length']
        )
        print(f"  Our result: {our_result.hex()}")

        # OpenSSL command
        # Note: OpenSSL expects salt in hex format
        salt_hex = test['salt']
        if not all(c in '0123456789abcdefABCDEF' for c in salt_hex):
            # Convert text salt to hex
            salt_hex = test['salt'].encode('utf-8').hex()

        openssl_cmd = [
            'openssl', 'kdf',
            '-keylen', str(test['length']),
            '-kdfopt', f'pass:{test["password"]}',
            '-kdfopt', f'salt:{salt_hex}',
            '-kdfopt', f'iter:{test["iterations"]}',
            'PBKDF2'
        ]

        try:
            result = subprocess.run(
                openssl_cmd,
                capture_output=True,
                text=True,
                check=True
            )
            openssl_result = bytes.fromhex(result.stdout.strip())
            print(f"  OpenSSL result: {openssl_result.hex()}")

            if our_result == openssl_result:
                print("  ✓ Results match!")
            else:
                print("  ✗ Results DO NOT match!")
                print(f"    Difference: {our_result != openssl_result}")
        except subprocess.CalledProcessError as e:
            print(f"  OpenSSL error: {e}")
            print(f"  stderr: {e.stderr}")
        except FileNotFoundError:
            print("  OpenSSL not found. Skipping comparison.")


if __name__ == '__main__':
    test_with_openssl()