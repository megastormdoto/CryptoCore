#!/usr/bin/env python3
import argparse
import sys


class CLIParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='CryptoCore - Cryptographic Toolkit (AES-128 + Hash Functions + MAC + GCM)',
            prog='cryptocore',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""\n
Examples:
  Encryption/Decryption:
    # GCM Encryption with AAD
    cryptocore encrypt --key 00112233445566778899aabbccddeeff --input plaintext.txt --output encrypted.bin --mode gcm --aad aabbccddeeff
    # GCM Decryption with AAD
    cryptocore encrypt --decrypt --key 00112233445566778899aabbccddeeff --input encrypted.bin --output decrypted.txt --mode gcm --aad aabbccddeeff
    # Traditional modes
    cryptocore encrypt --key 00112233445566778899aabbccddeeff --input file.txt --output encrypted.bin
    cryptocore encrypt --decrypt --key 00112233445566778899aabbccddeeff --input encrypted.bin --output decrypted.txt --mode cbc --iv a1b2c3d4e5f678901234567890abcdef

  Hashing:
    cryptocore dgst --algorithm sha256 --input document.pdf
    cryptocore dgst --algorithm sha3-256 --input backup.tar --output backup.sha3

  HMAC:
    cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input message.txt
    cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input message.txt --verify expected_hmac.txt
            """
        )

        subparsers = self.parser.add_subparsers(
            dest='command',
            help='Available commands',
            required=True,
            metavar='COMMAND'
        )

        # ==================== ENCRYPTION/DECRYPTION COMMAND ====================
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
            help='Additional Authenticated Data (AAD) for GCM mode as hexadecimal string. '
                 'Optional, treated as empty if not provided.'
        )

        gcm_group.add_argument(
            '--nonce',
            type=str,
            help='Nonce for GCM mode (12 bytes, 24 hex chars). '
                 'Alias for --iv, provided for consistency. If not provided during encryption, random nonce is generated.'
        )

        # ==================== HASH/MAC COMMAND ====================
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

    def parse_args(self):
        """Parse command line arguments with additional validation"""
        args = self.parser.parse_args()

        if args.command == 'encrypt':
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

            # Validate AAD for GCM
            if args.aad:
                try:
                    args.aad = bytes.fromhex(args.aad)
                except ValueError:
                    self.parser.error(
                        "AAD must be a valid hexadecimal string."
                    )
            else:
                args.aad = b""

        elif args.command == 'dgst':
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

        return args


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