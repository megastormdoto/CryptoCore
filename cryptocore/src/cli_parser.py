#!/usr/bin/env python3
import argparse
import sys


class CLIParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='CryptoCore - Cryptographic Toolkit (AES + Hash + MAC + GCM + KDF)',
            prog='cryptocore',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""\n
Examples:
  Encryption/Decryption:
    # GCM Encryption with hex AAD
    cryptocore encrypt --key 00112233445566778899aabbccddeeff --input plaintext.txt --output encrypted.bin --mode gcm --aad aabbccddeeff
    # GCM Decryption with AAD
    cryptocore encrypt --decrypt --key 00112233445566778899aabbccddeeff --input encrypted.bin --output decrypted.txt --mode gcm --aad aabbccddeeff

  Hashing:
    cryptocore dgst --algorithm sha256 --input document.pdf
    cryptocore dgst --algorithm sha3-256 --input backup.tar --output backup.sha3

  HMAC:
    cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input message.txt
    cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input message.txt --verify expected_hmac.txt

  Key Derivation:
    # Basic PBKDF2 with password and salt
    cryptocore derive --password "MySecurePassword" --salt a1b2c3d4e5f601234567890123456789
    # Auto-generate salt
    cryptocore derive --password "AnotherPassword" --iterations 500000 --length 16
    # Save to file
    cryptocore derive --password "app_key" --salt fixedappsalt --iterations 10000 --length 32 --output key.bin
    # Key hierarchy from master key
    cryptocore derive --master-key 00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff --context "encryption"
    # Read password from file
    cryptocore derive --password-file pass.txt --salt 1234...
            """
        )

        subparsers = self.parser.add_subparsers(
            dest='command',
            help='Available commands',
            required=True,
            metavar='COMMAND'
        )

        # ==================== ENCRYPTION/DECRYPTION COMMAND ====================
        self._setup_encrypt_parser(subparsers)

        # ==================== HASH/MAC COMMAND ====================
        self._setup_dgst_parser(subparsers)

        # ==================== KEY DERIVATION COMMAND ====================
        self._setup_derive_parser(subparsers)

    def _setup_encrypt_parser(self, subparsers):
        """Setup encryption/decryption command parser."""
        enc_parser = subparsers.add_parser(
            'encrypt',
            help='Encrypt or decrypt files using AES',
            description='Encrypt or decrypt files using AES with various block modes including GCM.'
        )

        # Key arguments group
        key_group = enc_parser.add_argument_group('Key options')
        key_group.add_argument(
            '--key',
            required=True,
            help='Encryption/decryption key in hexadecimal format (32 chars for AES-128). '
                 'Example: 00112233445566778899aabbccddeeff'
        )

        # File I/O group
        io_group = enc_parser.add_argument_group('File input/output')
        io_group.add_argument(
            '--input',
            required=True,
            help='Path to input file'
        )
        io_group.add_argument(
            '--output',
            required=True,
            help='Path to output file'
        )

        # Operation mode group
        mode_group = enc_parser.add_argument_group('Operation mode')
        mode_group.add_argument(
            '--mode',
            choices=['ecb', 'cbc', 'cfb', 'ofb', 'ctr', 'gcm'],
            default='ecb',
            help='Block cipher mode (default: ecb). '
                 'Note: GCM requires 12-byte nonce and supports AAD.'
        )
        mode_group.add_argument(
            '--decrypt',
            action='store_true',
            help='Perform decryption instead of encryption'
        )

        # Advanced options group
        adv_group = enc_parser.add_argument_group('Advanced options')
        adv_group.add_argument(
            '--iv',
            help='Initialization vector/nonce in hexadecimal format. '
                 'Required for CBC/CFB/OFB/CTR modes during decryption if IV was not prepended to the file. '
                 'For GCM: 12-byte nonce (24 hex chars).'
        )

        # GCM-specific options (SPRINT 6)
        gcm_group = enc_parser.add_argument_group('GCM/AEAD options (Sprint 6)')
        gcm_group.add_argument(
            '--aad',
            type=str,
            default='',
            help='Additional Authenticated Data (AAD) for GCM mode. '
                 'Can be hex string (e.g., "aabbccdd") or text string (e.g., "MyAuthData"). '
                 'Optional, treated as empty if not provided.'
        )

        gcm_group.add_argument(
            '--nonce',
            type=str,
            help='Nonce for GCM mode (12 bytes, 24 hex chars). '
                 'Alias for --iv, provided for consistency. If not provided during encryption, random nonce is generated.'
        )

    def _setup_dgst_parser(self, subparsers):
        """Setup hash/MAC command parser."""
        hash_parser = subparsers.add_parser(
            'dgst',
            help='Compute cryptographic hash or MAC of files',
            description='Compute message digest (hash) or Message Authentication Code (MAC) of files.'
        )

        hash_parser.add_argument(
            '--algorithm',
            required=True,
            choices=['sha256', 'sha3-256'],
            help='Hash algorithm to use'
        )

        hash_parser.add_argument(
            '--input',
            required=True,
            help='Path to input file to hash'
        )

        hash_parser.add_argument(
            '--output',
            help='Optional path to output file for hash/MAC value'
        )

        mac_group = hash_parser.add_argument_group('MAC options')
        mac_group.add_argument(
            '--hmac',
            action='store_true',
            help='Enable HMAC mode (requires --key)'
        )
        mac_group.add_argument(
            '--key',
            type=str,
            help='Key for HMAC as hexadecimal string'
        )
        mac_group.add_argument(
            '--verify',
            type=str,
            help='File containing expected HMAC value for verification'
        )
        mac_group.add_argument(
            '--cmac',
            action='store_true',
            help='[BONUS] Enable AES-CMAC mode'
        )

    def _setup_derive_parser(self, subparsers):
        """Setup key derivation command parser."""
        derive_parser = subparsers.add_parser(
            'derive',
            help='Derive cryptographic keys from passwords or other keys',
            description='Derive cryptographic keys using PBKDF2 (password-based) or key hierarchy (master key-based).'
        )

        # Password/Master Key input group (mutually exclusive)
        key_input_group = derive_parser.add_argument_group('Key source options')
        password_group = key_input_group.add_mutually_exclusive_group()

        password_group.add_argument(
            '--password', '-p',
            help='Password string (use quotes for special characters)'
        )
        password_group.add_argument(
            '--password-file', '-P',
            help='Read password from file (more secure)'
        )
        password_group.add_argument(
            '--password-env', '-E',
            help='Read password from environment variable'
        )
        password_group.add_argument(
            '--master-key', '-k',
            help='Master key for key hierarchy derivation (hex string, 32+ hex chars recommended)'
        )

        # Context for key hierarchy
        derive_parser.add_argument(
            '--context', '-c',
            help='Context string for key hierarchy derivation (e.g., "encryption", "authentication"). '
                 'Required when using --master-key.'
        )

        # Salt options
        salt_group = derive_parser.add_mutually_exclusive_group()
        salt_group.add_argument(
            '--salt', '-s',
            help='Salt as hexadecimal string (for PBKDF2). If not provided, random 16-byte salt is generated.'
        )
        salt_group.add_argument(
            '--salt-file',
            help='Read salt from file (raw bytes)'
        )

        # Algorithm and parameters
        params_group = derive_parser.add_argument_group('Derivation parameters')
        params_group.add_argument(
            '--algorithm', '-a',
            choices=['pbkdf2'],
            default='pbkdf2',
            help='Key derivation algorithm (default: pbkdf2)'
        )
        params_group.add_argument(
            '--iterations', '-i',
            type=int,
            default=100000,
            help='Number of iterations for PBKDF2 (default: 100000)'
        )
        params_group.add_argument(
            '--length', '-l',
            type=int,
            default=32,
            help='Desired key length in bytes (default: 32)'
        )

        # Output options
        output_group = derive_parser.add_argument_group('Output options')
        output_group.add_argument(
            '--output', '-o',
            help='Output file for derived key (binary format)'
        )
        output_group.add_argument(
            '--output-salt',
            help='Output file for generated salt (if salt was auto-generated)'
        )

        # Optional: format output
        output_group.add_argument(
            '--format',
            choices=['hex', 'binary'],
            default='hex',
            help='Output format for stdout (default: hex)'
        )

    def parse_args(self):
        """Parse command line arguments with additional validation"""
        args = self.parser.parse_args()

        if args.command == 'encrypt':
            self._validate_encrypt_args(args)
        elif args.command == 'dgst':
            self._validate_dgst_args(args)
        elif args.command == 'derive':
            self._validate_derive_args(args)

        return args

    def _validate_encrypt_args(self, args):
        """Validate encryption command arguments."""
        # Validate key
        if args.key:
            try:
                key_bytes = bytes.fromhex(args.key)
                if len(key_bytes) not in [16, 24, 32]:
                    print(
                        f"Warning: Key is {len(key_bytes)} bytes. "
                        f"AES supports 16 (128-bit), 24 (192-bit), or 32 (256-bit) bytes.",
                        file=sys.stderr
                    )
            except ValueError:
                self.parser.error(
                    "Invalid key format. Must be hexadecimal string."
                )

        # Handle nonce/iv for GCM
        if args.mode == 'gcm':
            # Если указан --nonce, используем его, иначе --iv
            if args.nonce and args.iv:
                self.parser.error(
                    "Cannot specify both --nonce and --iv. Use one for GCM."
                )
            elif args.nonce:
                args.iv = args.nonce

            # Для GCM decryption: если IV не указан, он будет прочитан из файла
            if args.iv:
                try:
                    iv_bytes = bytes.fromhex(args.iv)
                    if len(iv_bytes) != 12:
                        print(
                            f"Warning: GCM recommends 12-byte nonce (got {len(iv_bytes)} bytes).",
                            file=sys.stderr
                        )
                except ValueError:
                    self.parser.error(
                        "Invalid nonce format. Must be hexadecimal string."
                    )
        else:
            # For non-GCM modes, validate IV length
            if args.iv:
                try:
                    iv_bytes = bytes.fromhex(args.iv)
                    if len(iv_bytes) != 16:
                        print(
                            f"Warning: Non-GCM modes typically use 16-byte IV (got {len(iv_bytes)} bytes).",
                            file=sys.stderr
                        )
                except ValueError:
                    self.parser.error(
                        "Invalid IV format. Must be hexadecimal string."
                    )
            elif args.decrypt and args.mode in ['cbc', 'cfb', 'ofb', 'ctr']:
                print(
                    "Warning: IV not specified for decryption. "
                    "Assuming IV is prepended to the input file.",
                    file=sys.stderr
                )

        # Validate AAD for GCM - FIXED: Support both hex and text AAD
        if hasattr(args, 'aad'):
            if args.aad == '':
                args.aad = b""  # Empty bytes
            else:
                try:
                    # First try to parse as hex
                    args.aad = bytes.fromhex(args.aad)
                except ValueError:
                    # If not valid hex, treat as text string
                    args.aad = args.aad.encode('utf-8')
        else:
            args.aad = b""  # Empty bytes

    def _validate_dgst_args(self, args):
        """Validate hash/MAC command arguments."""
        # HMAC validation
        if args.hmac:
            if not args.key:
                self.parser.error(
                    "Error: --key is REQUIRED when using --hmac"
                )
            try:
                bytes.fromhex(args.key)
            except ValueError:
                self.parser.error(
                    "Invalid key format. Must be hexadecimal string."
                )

        # CMAC validation
        if args.cmac:
            if not args.key:
                self.parser.error(
                    "Error: --key is REQUIRED when using --cmac"
                )
            try:
                key_bytes = bytes.fromhex(args.key)
                if len(key_bytes) != 16:
                    self.parser.error(
                        "AES-CMAC requires 16-byte key (32 hex chars)."
                    )
            except ValueError:
                self.parser.error(
                    "Invalid key format for CMAC."
                )

        if args.hmac and args.cmac:
            self.parser.error(
                "Cannot use both --hmac and --cmac simultaneously."
            )

        if args.verify:
            if not args.key:
                self.parser.error(
                    "Error: --key is REQUIRED when using --verify"
                )
            if not (args.hmac or args.cmac):
                self.parser.error(
                    "Error: --verify requires --hmac or --cmac"
                )

    def _validate_derive_args(self, args):
        """Validate key derivation command arguments."""
        # Validate that we have either password (or related) or master key
        password_sources = ['password', 'password_file', 'password_env']
        has_password_source = any(getattr(args, source, None) for source in password_sources)

        if not has_password_source and not args.master_key:
            self.parser.error(
                "Error: Must specify either --password/--password-file/--password-env or --master-key"
            )

        if args.master_key and has_password_source:
            self.parser.error(
                "Error: Cannot specify both password source (--password/--password-file/--password-env) and --master-key"
            )

        # Validate master key
        if args.master_key:
            try:
                master_key_bytes = bytes.fromhex(args.master_key)
                if len(master_key_bytes) < 16:
                    print(
                        f"Warning: Master key is only {len(master_key_bytes)} bytes. "
                        f"Recommend at least 16 bytes for security.",
                        file=sys.stderr
                    )
            except ValueError:
                self.parser.error(
                    "Invalid master key format. Must be hexadecimal string."
                )

            # Context is required for key hierarchy
            if not args.context:
                self.parser.error(
                    "Error: --context is REQUIRED when using --master-key"
                )

        # Validate salt (only relevant for password-based derivation)
        if has_password_source:
            if args.salt:
                try:
                    bytes.fromhex(args.salt)
                except ValueError:
                    self.parser.error(
                        "Invalid salt format. Must be hexadecimal string."
                    )

        # Validate iterations
        if args.iterations < 1:
            self.parser.error(
                "Error: --iterations must be at least 1"
            )

        # Validate length
        if args.length < 1:
            self.parser.error(
                "Error: --length must be at least 1"
            )

        # Validate algorithm
        if args.algorithm not in ['pbkdf2']:
            self.parser.error(
                f"Error: Algorithm '{args.algorithm}' not supported"
            )

        # Validate context string if provided
        if args.context and not args.master_key:
            print(
                "Warning: --context ignored when not using --master-key",
                file=sys.stderr
            )


if __name__ == '__main__':
    try:
        parser = CLIParser()
        args = parser.parse_args()
        print(f"Command: {args.command}")
        print(f"Arguments: {args}")
    except SystemExit:
        pass
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)