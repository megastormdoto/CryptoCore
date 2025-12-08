#!/usr/bin/env python3
import argparse
import sys


class CLIParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='CryptoCore - Cryptographic Toolkit (AES-128 + Hash Functions + MAC)',
            prog='cryptocore',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  Encryption/Decryption:
    cryptocore encrypt --key 00112233445566778899aabbccddeeff --input file.txt --output encrypted.bin
    cryptocore encrypt --key 00112233445566778899aabbccddeeff --input encrypted.bin --output decrypted.txt --decrypt --mode cbc --iv a1b2c3d4e5f678901234567890abcdef

  Hashing (Sprint 4):
    cryptocore dgst --algorithm sha256 --input document.pdf
    cryptocore dgst --algorithm sha3-256 --input backup.tar --output backup.sha3

  MAC (Sprint 5 - HMAC):
    cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input message.txt
    cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input message.txt --verify hmac.txt
            """
        )

        subparsers = self.parser.add_subparsers(
            dest='command',
            help='Available commands',
            required=True,
            metavar='COMMAND'
        )

        # ==================== ENCRYPTION/DECRYPTION COMMAND ====================
        # (From previous sprints - kept unchanged)
        enc_parser = subparsers.add_parser(
            'encrypt',
            help='Encrypt or decrypt files using AES-128',
            description='Encrypt or decrypt files using AES-128 with various block modes.'
        )

        # Key arguments group
        key_group = enc_parser.add_argument_group('Key options')
        key_group.add_argument(
            '--key',
            required=True,
            help='Encryption/decryption key in hexadecimal format (32 characters, 16 bytes). '
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
            choices=['ecb', 'cbc', 'cfb', 'ofb', 'ctr'],
            default='ecb',
            help='Block cipher mode (default: ecb)'
        )
        mode_group.add_argument(
            '--decrypt',
            action='store_true',
            help='Perform decryption instead of encryption'
        )

        # Advanced options group (from previous sprints)
        adv_group = enc_parser.add_argument_group('Advanced options')
        adv_group.add_argument(
            '--iv',
            help='Initialization vector in hexadecimal format (32 characters). '
                 'Required for CBC/CFB/OFB/CTR modes during decryption if IV was not prepended to the file.'
        )

        # ==================== HASH/MAC COMMAND (SPRINT 4 + 5) ====================
        hash_parser = subparsers.add_parser(
            'dgst',
            help='Compute cryptographic hash or MAC of files',
            description='Compute message digest (hash) or Message Authentication Code (MAC) of files.'
        )

        # Algorithm selection
        hash_parser.add_argument(
            '--algorithm',
            required=True,
            choices=['sha256', 'sha3-256'],
            help='Hash algorithm to use. Choices: sha256, sha3-256'
        )

        # Input file
        hash_parser.add_argument(
            '--input',
            required=True,
            help='Path to input file to hash'
        )

        # Output option
        hash_parser.add_argument(
            '--output',
            help='Optional path to output file for hash/MAC value. '
                 'If not specified, result is printed to stdout.'
        )

        # ========== HMAC/CMAC OPTIONS (SPRINT 5) - ДОБАВЛЯЕМ ==========
        mac_group = hash_parser.add_argument_group('MAC options')

        mac_group.add_argument(
            '--hmac',
            action='store_true',
            help='Enable HMAC mode (requires --key)'
        )

        mac_group.add_argument(
            '--cmac',
            action='store_true',
            help='Enable AES-CMAC mode (bonus, requires --key)'
        )

        mac_group.add_argument(
            '--key', '-k',
            type=str,
            help='Key for HMAC/CMAC as hexadecimal string'
        )

        mac_group.add_argument(
            '--verify',
            type=str,
            help='File containing expected MAC value for verification'
        )

        # Add mutual exclusivity for hash-specific options
        hash_note = hash_parser.add_argument_group('Note')
        hash_note.description = (
            'The dgst command can compute hash values or MAC (Message Authentication Code) values. '
            'For MAC, specify --hmac or --cmac with --key.'
        )

    def parse_args(self):
        """Parse command line arguments with additional validation"""
        args = self.parser.parse_args()

        # Post-parsing validation for encryption command
        if args.command == 'encrypt':
            # Validate key length (should be 32 hex chars = 16 bytes)
            if args.key:
                if len(args.key) != 32:
                    self.parser.error(
                        f"Key must be exactly 32 hexadecimal characters (16 bytes). "
                        f"Got {len(args.key)} characters."
                    )
                try:
                    bytes.fromhex(args.key)
                except ValueError:
                    self.parser.error(
                        f"Invalid key format. Key must contain only hexadecimal characters (0-9, a-f, A-F)."
                    )

            # Validate IV if provided
            if args.iv:
                if len(args.iv) != 32:
                    self.parser.error(
                        f"IV must be exactly 32 hexadecimal characters (16 bytes). "
                        f"Got {len(args.iv)} characters."
                    )
                try:
                    bytes.fromhex(args.iv)
                except ValueError:
                    self.parser.error(
                        f"Invalid IV format. IV must contain only hexadecimal characters (0-9, a-f, A-F)."
                    )

                # Warn if IV is provided but mode is ECB
                if args.mode == 'ecb':
                    print(
                        "Warning: IV is provided but mode is ECB (IV is not used in ECB mode).",
                        file=sys.stderr
                    )

        # Post-parsing validation for hash command (SPRINT 5 - добавляем проверки для HMAC)
        elif args.command == 'dgst':
            # Проверка для HMAC/CMAC
            if args.hmac or args.cmac:
                if not args.key:
                    self.parser.error(
                        "Key must be provided when using --hmac or --cmac"
                    )

                # Проверяем что ключ в hex формате
                try:
                    key_bytes = bytes.fromhex(args.key)
                    if len(key_bytes) == 0:
                        self.parser.error("Key cannot be empty")
                except ValueError:
                    self.parser.error(
                        "Invalid key format. Key must be a hexadecimal string."
                    )

                # Для CMAC проверяем что алгоритм SHA-256 (нужен для ключа)
                if args.cmac and args.algorithm != 'sha256':
                    print(
                        "Warning: CMAC typically uses AES, but algorithm is set to hash. Continuing anyway...",
                        file=sys.stderr
                    )

        return args


if __name__ == '__main__':
    try:
        parser = CLIParser()
        args = parser.parse_args()
        print(f"Command: {args.command}")
        print(f"Arguments: {args}")
    except SystemExit:
        pass  # argparse already printed error
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)