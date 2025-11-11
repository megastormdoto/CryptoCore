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
            choices=['ecb'],
            help='Mode of operation (only ecb)'
        )

        # Encryption/decryption operation group
        operation_group = self.parser.add_mutually_exclusive_group(required=True)
        operation_group.add_argument('--encrypt', action='store_true', help='Perform encryption')
        operation_group.add_argument('--decrypt', action='store_true', help='Perform decryption')

        self.parser.add_argument(
            '--key',
            required=True,
            help='Key in HEX format (16 bytes for AES-128)'
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

    def parse_args(self):
        """Parse and validate arguments"""
        args = self.parser.parse_args()

        # Key validation
        if not self._is_valid_hex_key(args.key):
            print(f"Error: Key must be a 32-character HEX string (16 bytes)", file=sys.stderr)
            sys.exit(1)

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
    except SystemExit:
        print("CLI test completed")