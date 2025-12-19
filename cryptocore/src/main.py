#!/usr/bin/env python3
"""
CryptoCore - Main Entry Point
"""
import sys
import os
import tempfile
from pathlib import Path
from getpass import getpass

# Критически важно: добавляем правильные пути для импорта
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# Добавляем текущую директорию и родительскую
sys.path.insert(0, current_dir)  # src directory
sys.path.insert(0, project_root)  # project root

# Также добавляем возможные пути
sys.path.insert(0, os.path.join(current_dir, '..'))

try:
    # Пробуем импортировать из текущей директории (src)
    from cli.parser import CLIParser
    from core.ciphers import AES
    from core.hashing import SHA256, SHA3_256
    from core.mac import HMAC, CMAC
    from modes.ecb import ECB
    from modes.cbc import CBC
    from modes.cfb import CFB
    from modes.ofb import OFB
    from modes.ctr import CTR
    from modes.gcm import GCM, AuthenticationError
    from aead.encrypt_then_mac import EncryptThenMAC
    # KDF imports
    from kdf.pbkdf2 import pbkdf2_hmac_sha256
    from kdf.hkdf import derive_key

except ImportError as e:
    # Если не сработало, пробуем импортировать как модуль src
    try:
        from src.cli.parser import CLIParser
        from src.core.ciphers import AES
        from src.core.hashing import SHA256, SHA3_256
        from src.core.mac import HMAC, CMAC
        from src.modes.ecb import ECB
        from src.modes.cbc import CBC
        from src.modes.cfb import CFB
        from src.modes.ofb import OFB
        from src.modes.ctr import CTR
        from src.modes.gcm import GCM, AuthenticationError
        from src.aead.encrypt_then_mac import EncryptThenMAC
        # KDF imports
        from src.kdf.pbkdf2 import pbkdf2_hmac_sha256
        from src.kdf.hkdf import derive_key

    except ImportError as e2:
        print(f"FATAL: Could not import modules: {e2}", file=sys.stderr)
        sys.exit(1)


class CryptoCore:
    def __init__(self):
        self.parser = CLIParser()

    def run(self):
        """Main execution flow"""
        args = self.parser.parse_args()

        if args.command == 'encrypt':
            self.handle_encryption(args)
        elif args.command == 'dgst':
            self.handle_digest(args)
        elif args.command == 'derive':
            self.handle_derive(args)
        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            sys.exit(1)

    def handle_encryption(self, args):
        """Handle encryption/decryption commands"""
        try:
            # Parse key
            key = bytes.fromhex(args.key)

            # Parse AAD (for GCM)
            aad = args.aad if hasattr(args, 'aad') else b""

            # Read input file
            with open(args.input, 'rb') as f:
                input_data = f.read()

            if args.decrypt:
                self.handle_decryption(args, key, input_data, aad)
            else:
                self.handle_encryption_process(args, key, input_data, aad)

        except Exception as e:
            print(f"[ERROR] {str(e)}", file=sys.stderr)
            sys.exit(1)

    def handle_encryption_process(self, args, key, plaintext, aad):
        """Handle encryption"""
        output_data = None

        if args.mode == 'gcm':
            # GCM encryption
            if args.iv:
                # Use provided nonce
                nonce = bytes.fromhex(args.iv)
                gcm = GCM(key, nonce)
            else:
                # Generate random nonce
                gcm = GCM(key)

            # Encrypt with GCM
            ciphertext = gcm.encrypt(plaintext, aad)
            output_data = ciphertext

            # Show nonce info
            print(f"[INFO] GCM nonce: {gcm.nonce.hex()}")
            print(f"[INFO] AAD length: {len(aad)} bytes")

        elif args.mode == 'ecb':
            cipher = AES(key)
            mode = ECB(cipher)
            output_data = mode.encrypt(plaintext)

        elif args.mode == 'cbc':
            cipher = AES(key)
            if args.iv:
                iv = bytes.fromhex(args.iv)
            else:
                iv = os.urandom(16)
            mode = CBC(cipher, iv)
            output_data = iv + mode.encrypt(plaintext)

        elif args.mode == 'cfb':
            cipher = AES(key)
            if args.iv:
                iv = bytes.fromhex(args.iv)
            else:
                iv = os.urandom(16)
            mode = CFB(cipher, iv)
            output_data = iv + mode.encrypt(plaintext)

        elif args.mode == 'ofb':
            cipher = AES(key)
            if args.iv:
                iv = bytes.fromhex(args.iv)
            else:
                iv = os.urandom(16)
            mode = OFB(cipher, iv)
            output_data = iv + mode.encrypt(plaintext)

        elif args.mode == 'ctr':
            cipher = AES(key)
            if args.iv:
                iv = bytes.fromhex(args.iv)
            else:
                iv = os.urandom(16)
            mode = CTR(cipher, iv)
            output_data = iv + mode.encrypt(plaintext)

        else:
            raise ValueError(f"Unsupported mode: {args.mode}")

        # Write output
        with open(args.output, 'wb') as f:
            f.write(output_data)

        print(f"[SUCCESS] Encryption completed successfully")
        print(f"[INFO] Output size: {len(output_data)} bytes")

    def handle_decryption(self, args, key, input_data, aad):
        """Handle decryption with authentication checks"""
        output_data = None

        try:
            if args.mode == 'gcm':
                # GCM decryption
                if args.iv:
                    # Nonce provided separately via --iv/--nonce
                    nonce = bytes.fromhex(args.iv)
                    # input_data должен содержать только ciphertext + tag (без nonce)
                    # Но наш формат всегда сохраняет nonce в файле
                    # Поэтому если указан явный nonce, считаем что в файле его нет
                    gcm = GCM(key, nonce)
                    # input_data уже содержит ciphertext + tag
                    plaintext = gcm.decrypt(nonce + input_data, aad)
                else:
                    # Nonce is prepended (12 bytes) in the file
                    # Format: nonce (12) + ciphertext + tag (16)
                    gcm = GCM(key)
                    plaintext = gcm.decrypt(input_data, aad)

                output_data = plaintext

            elif args.mode == 'ecb':
                cipher = AES(key)
                mode = ECB(cipher)
                output_data = mode.decrypt(input_data)

            elif args.mode == 'cbc':
                cipher = AES(key)
                if args.iv:
                    iv = bytes.fromhex(args.iv)
                    ciphertext = input_data
                else:
                    iv = input_data[:16]
                    ciphertext = input_data[16:]
                mode = CBC(cipher, iv)
                output_data = mode.decrypt(ciphertext)

            elif args.mode == 'cfb':
                cipher = AES(key)
                if args.iv:
                    iv = bytes.fromhex(args.iv)
                    ciphertext = input_data
                else:
                    iv = input_data[:16]
                    ciphertext = input_data[16:]
                mode = CFB(cipher, iv)
                output_data = mode.decrypt(ciphertext)

            elif args.mode == 'ofb':
                cipher = AES(key)
                if args.iv:
                    iv = bytes.fromhex(args.iv)
                    ciphertext = input_data
                else:
                    iv = input_data[:16]
                    ciphertext = input_data[16:]
                mode = OFB(cipher, iv)
                output_data = mode.decrypt(ciphertext)

            elif args.mode == 'ctr':
                cipher = AES(key)
                if args.iv:
                    iv = bytes.fromhex(args.iv)
                    ciphertext = input_data
                else:
                    iv = input_data[:16]
                    ciphertext = input_data[16:]
                mode = CTR(cipher, iv)
                output_data = mode.decrypt(ciphertext)

            else:
                raise ValueError(f"Unsupported mode: {args.mode}")

            # Write output (only if authentication succeeded for GCM)
            with open(args.output, 'wb') as f:
                f.write(output_data)

            print(f"[SUCCESS] Decryption completed successfully")
            print(f"[INFO] Output size: {len(output_data)} bytes")

        except AuthenticationError as e:
            # CRITICAL: Delete output file if authentication failed
            if os.path.exists(args.output):
                os.remove(args.output)
            print(f"[ERROR] Authentication failed: {str(e)}", file=sys.stderr)
            print(f"[SECURITY] No plaintext output - file deleted for security", file=sys.stderr)
            sys.exit(1)

    def handle_digest(self, args):
        """Handle hash/MAC commands"""
        try:
            # Read input file
            with open(args.input, 'rb') as f:
                data = f.read()

            result = None

            if args.hmac:
                # HMAC computation/verification
                key = bytes.fromhex(args.key)
                hmac = HMAC(key, args.algorithm)

                if args.verify:
                    # Verify mode
                    with open(args.verify, 'r') as f:
                        expected_line = f.read().strip()

                    # Parse format: HMAC_VALUE FILENAME
                    parts = expected_line.split()
                    if len(parts) >= 1:
                        expected_hex = parts[0]
                        expected = bytes.fromhex(expected_hex)
                        computed = hmac.compute(data)

                        if hmac.verify(data, expected):
                            print(f"[SUCCESS] HMAC verification passed")
                            sys.exit(0)
                        else:
                            print(f"[ERROR] HMAC verification failed", file=sys.stderr)
                            print(f"Expected: {expected_hex}")
                            print(f"Computed: {computed.hex()}")
                            sys.exit(1)
                    else:
                        print(f"[ERROR] Invalid verification file format", file=sys.stderr)
                        sys.exit(1)
                else:
                    # Compute mode
                    result = hmac.compute(data)

            elif args.cmac:
                # CMAC computation/verification
                key = bytes.fromhex(args.key)
                cmac = CMAC(key)

                if args.verify:
                    with open(args.verify, 'r') as f:
                        expected_hex = f.read().strip()
                    expected = bytes.fromhex(expected_hex)
                    computed = cmac.compute(data)

                    if cmac.verify(data, expected):
                        print(f"[SUCCESS] CMAC verification passed")
                        sys.exit(0)
                    else:
                        print(f"[ERROR] CMAC verification failed", file=sys.stderr)
                        sys.exit(1)
                else:
                    result = cmac.compute(data)

            else:
                # Regular hash
                if args.algorithm == 'sha256':
                    hasher = SHA256()
                elif args.algorithm == 'sha3-256':
                    hasher = SHA3_256()
                else:
                    raise ValueError(f"Unsupported algorithm: {args.algorithm}")

                result = hasher.compute(data)

            # Output result
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(f"{result.hex()} {args.input}\n")
                print(f"[SUCCESS] Result written to {args.output}")
            else:
                print(f"{result.hex()} {args.input}")

        except Exception as e:
            print(f"[ERROR] {str(e)}", file=sys.stderr)
            sys.exit(1)

    def handle_derive(self, args):
        """Handle key derivation commands"""
        try:
            # Get password or master key
            password = None
            master_key = None

            if args.master_key:
                # Key hierarchy mode
                master_key = bytes.fromhex(args.master_key)

                if not args.context:
                    print("[ERROR] Context string required for key hierarchy derivation",
                          file=sys.stderr)
                    sys.exit(1)

                # Perform key hierarchy derivation
                derived_key = derive_key(
                    master_key,
                    args.context,
                    args.length
                )
                salt_hex = ''

            else:
                # Password-based mode
                if args.password:
                    password = args.password
                elif args.password_file:
                    try:
                        with open(args.password_file, 'r', encoding='utf-8') as f:
                            password = f.read().strip()
                    except IOError as e:
                        print(f"[ERROR] Reading password file: {e}", file=sys.stderr)
                        sys.exit(1)
                elif args.password_env:
                    password = os.environ.get(args.password_env)
                    if not password:
                        print(f"[ERROR] Environment variable {args.password_env} not set",
                              file=sys.stderr)
                        sys.exit(1)
                else:
                    # Prompt for password
                    password = getpass("Enter password: ")

                # Get or generate salt
                salt = None
                if args.salt:
                    try:
                        salt = bytes.fromhex(args.salt)
                    except ValueError:
                        # If not valid hex, treat as text
                        salt = args.salt.encode('utf-8')
                elif args.salt_file:
                    try:
                        with open(args.salt_file, 'rb') as f:
                            salt = f.read()
                    except IOError as e:
                        print(f"[ERROR] Reading salt file: {e}", file=sys.stderr)
                        sys.exit(1)
                else:
                    # Generate random salt
                    import secrets
                    salt = secrets.token_bytes(16)
                    salt_hex = salt.hex()

                # Perform PBKDF2 derivation
                print(f"[INFO] Deriving key with {args.iterations} iterations...")
                derived_key = pbkdf2_hmac_sha256(
                    password,
                    salt,
                    args.iterations,
                    args.length
                )

                # Clear password from memory
                if isinstance(password, str):
                    # Overwrite with random data
                    password = ' ' * len(password)
                password = None

            # Output results according to specification
            if args.output:
                # Write binary key to file
                try:
                    with open(args.output, 'wb') as f:
                        f.write(derived_key)
                    print(f"[SUCCESS] Key written to {args.output}")
                except IOError as e:
                    print(f"[ERROR] Writing key file: {e}", file=sys.stderr)
                    sys.exit(1)

            # Always print to stdout in format: KEY_HEX SALT_HEX
            if master_key:
                # For key hierarchy, salt is empty
                print(f"{derived_key.hex()} ")
            else:
                # For PBKDF2, include salt
                salt_output = salt_hex if 'salt_hex' in locals() else args.salt or ''
                print(f"{derived_key.hex()} {salt_output}")

            # Write generated salt to file if specified
            if 'salt_hex' in locals() and salt_hex and args.output_salt:
                try:
                    with open(args.output_salt, 'w') as f:
                        f.write(salt_hex)
                    print(f"[INFO] Salt written to {args.output_salt}")
                except IOError as e:
                    print(f"[ERROR] Writing salt file: {e}", file=sys.stderr)
                    sys.exit(1)

        except Exception as e:
            print(f"[ERROR] Key derivation failed: {str(e)}", file=sys.stderr)
            sys.exit(1)


def main():
    """Main entry point"""
    try:
        app = CryptoCore()
        app.run()
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()