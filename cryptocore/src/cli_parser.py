import argparse
import sys
import os
import re


class CLIParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='CryptoCore - Cryptographic Core Operations Tool',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        self._setup_arguments()

    def _setup_arguments(self):
        """Setup command line arguments"""
        self.parser.add_argument(
            '--algorithm',
            required=True,
            choices=['aes'],
            help='Encryption algorithm (only aes)'
        )
        self.parser.add_argument(
            '--mode',
            required=True,
            choices=['ecb', 'cbc', 'cfb', 'ofb', 'ctr'],
            help='Mode of operation'
        )

        # Encryption/decryption operation group
        operation_group = self.parser.add_mutually_exclusive_group(required=True)
        operation_group.add_argument('--encrypt', action='store_true', help='Perform encryption')
        operation_group.add_argument('--decrypt', action='store_true', help='Perform decryption')

        # Key is now optional for encryption, required for decryption
        self.parser.add_argument(
            '--key',
            help='Key in HEX format (16 bytes for AES-128). Optional for encryption - will be generated if omitted.'
        )

        self.parser.add_argument(
            '--input',
            required=True,
            help='Input file'
        )
        self.parser.add_argument(
            '--output',
            help='Output file (optional)'
        )
        self.parser.add_argument(
            '--iv',
            help='Initialization Vector in HEX format (for decryption only)'
        )

    def parse_args(self):
        """Parse and validate arguments"""
        args = self.parser.parse_args()

        # Key validation for decryption
        if args.decrypt and not args.key:
            print(f"Error: Key is REQUIRED for decryption operations", file=sys.stderr)
            sys.exit(1)

        # Key validation if provided
        if args.key:
            if not self._is_valid_hex_key(args.key):
                print(f"Error: Key must be a 32-character HEX string (16 bytes)", file=sys.stderr)
                sys.exit(1)

            # Check for weak keys and warn
            self._warn_weak_key(args.key)

        # IV validation (if provided)
        if args.iv and not self._is_valid_hex_iv(args.iv):
            print(f"Error: IV must be a 32-character HEX string (16 bytes)", file=sys.stderr)
            sys.exit(1)

        # Validate IV usage
        if args.encrypt and args.iv:
            print("Warning: IV is generated automatically during encryption. Provided IV will be ignored.", file=sys.stderr)
            args.iv = None  # Ignore IV for encryption

        if args.decrypt and not args.iv:
            print("Info: No IV provided. Will read IV from input file.", file=sys.stderr)

        # Check input file existence
        if not os.path.exists(args.input):
            print(f"Error: Input file does not exist: {args.input}", file=sys.stderr)
            sys.exit(1)

        # Generate default output filename
        if not args.output:
            args.output = self._generate_default_output_filename(args.input, args.encrypt)

        return args

    def _is_valid_hex_key(self, key):
        """Validate HEX key"""
        hex_pattern = re.compile(r'^[0-9a-fA-F]{32}$')
        return bool(hex_pattern.match(key))

    def _is_valid_hex_iv(self, iv):
        """Validate HEX IV"""
        hex_pattern = re.compile(r'^[0-9a-fA-F]{32}$')
        return bool(hex_pattern.match(iv))

    def _generate_default_output_filename(self, input_file, is_encrypt):
        """Generate default output filename"""
        if is_encrypt:
            return input_file + '.enc'
        else:
            # Remove .enc extension if present, otherwise add .dec
            if input_file.endswith('.enc'):
                return input_file[:-4] + '.dec'
            else:
                return input_file + '.dec'

    def _warn_weak_key(self, key_hex):
        """Check for weak keys and print warning"""
        try:
            key_bytes = bytes.fromhex(key_hex)

            # Check for all zeros
            if all(byte == 0 for byte in key_bytes):
                print(f"⚠️  WARNING: The provided key is all zeros (very weak!)", file=sys.stderr)
                print(f"   For better security, use a randomly generated key.", file=sys.stderr)
                return

            # Check for sequential bytes
            sequential_up = all(key_bytes[i] == key_bytes[i - 1] + 1 for i in range(1, len(key_bytes)))
            sequential_down = all(key_bytes[i] == key_bytes[i - 1] - 1 for i in range(1, len(key_bytes)))

            if sequential_up or sequential_down:
                print(f"⚠️  WARNING: The provided key uses sequential bytes (weak!)", file=sys.stderr)
                print(f"   For better security, use a randomly generated key.", file=sys.stderr)
                return

            # Check for repeated patterns
            if len(key_bytes) >= 4:
                # Check if key consists of repeated 2-byte pattern
                if len(key_bytes) % 2 == 0:
                    pattern = key_bytes[:2]
                    repeated = all(key_bytes[i:i + 2] == pattern for i in range(2, len(key_bytes), 2))
                    if repeated:
                        print(f"⚠️  WARNING: The provided key uses repeated patterns (weak!)", file=sys.stderr)
                        print(f"   For better security, use a randomly generated key.", file=sys.stderr)
                        return

        except:
            pass  # If we can't check, don't show warning


if __name__ == "__main__":
    # Test the CLI parser
    parser = CLIParser()
    try:
        args = parser.parse_args()
        print("Parsed arguments:")
        print(f"  Algorithm: {args.algorithm}")
        print(f"  Mode: {args.mode}")
        print(f"  Operation: {'encrypt' if args.encrypt else 'decrypt'}")
        print(f"  Key: {args.key}")
        print(f"  Input: {args.input}")
        print(f"  Output: {args.output}")
        print(f"  IV: {args.iv}")
    except SystemExit:
        print("CLI test completed")