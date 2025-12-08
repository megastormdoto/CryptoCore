#!/usr/bin/env python3
import sys
import os

# Add src directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from cli_parser import CLIParser
from file_io import FileIO
from csprng import generate_random_bytes, is_weak_key


class CryptoCore:
    def __init__(self):
        self.parser = CLIParser()

    def run(self):
        """Main entry point for CryptoCore"""
        try:
            args = self.parser.parse_args()

            # Dispatch to appropriate handler
            if args.command == 'encrypt':
                self._handle_crypto(args)
            elif args.command == 'dgst':
                self._handle_hash(args)
            else:
                print(f"Error: Unknown command '{args.command}'", file=sys.stderr)
                sys.exit(1)

        except SystemExit:
            raise  # Re-raise system exit exceptions
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    def _handle_crypto(self, args):
        """Handle encryption/decryption operations (Sprints 1-3)"""
        print(f"CryptoCore - {'Decryption' if args.decrypt else 'Encryption'} Mode")
        print(f"Algorithm: AES-128, Mode: {args.mode.upper()}")
        print(f"Input file: {args.input}")
        print(f"Output file: {args.output}")
        print("-" * 50)

        # Convert key from hex to bytes
        try:
            key_bytes = bytes.fromhex(args.key)
        except ValueError as e:
            print(f"Error: Invalid key format - {e}", file=sys.stderr)
            sys.exit(1)

        # Validate key length
        if len(key_bytes) != 16:
            print(f"Error: Key must be 16 bytes (got {len(key_bytes)} bytes)", file=sys.stderr)
            sys.exit(1)

        # Check for weak keys
        if is_weak_key(key_bytes):
            print("WARNING: The provided key may be weak! Consider using a different key.", file=sys.stderr)

        # Read input file
        try:
            input_data = FileIO.read_file(args.input)
        except Exception as e:
            print(f"Error reading input file: {e}", file=sys.stderr)
            sys.exit(1)

        if not input_data:
            print("Warning: Input file is empty", file=sys.stderr)

        # Handle IV based on mode and operation
        iv = None
        if args.mode != 'ecb':
            if args.decrypt:
                # For decryption, IV might be in file or provided via --iv
                if args.iv:
                    # IV provided via command line
                    try:
                        iv = bytes.fromhex(args.iv)
                    except ValueError as e:
                        print(f"Error: Invalid IV format - {e}", file=sys.stderr)
                        sys.exit(1)
                    print(f"Using provided IV: {args.iv}")
                else:
                    # Extract IV from beginning of file
                    if len(input_data) < 16:
                        print("Error: Input file too short to contain IV", file=sys.stderr)
                        sys.exit(1)
                    iv = input_data[:16]
                    input_data = input_data[16:]
                    print(f"Extracted IV from file: {iv.hex()}")
            else:
                # For encryption, generate random IV
                iv = generate_random_bytes(16)
                print(f"Generated random IV: {iv.hex()}")

        # Import and initialize the appropriate mode
        try:
            if args.mode == 'ecb':
                from modes.ecb import ECBMode
                mode_instance = ECBMode(key_bytes)
            elif args.mode == 'cbc':
                from modes.cbc import CBCMode
                mode_instance = CBCMode(key_bytes)
            elif args.mode == 'cfb':
                from modes.cfb import CFBMode
                mode_instance = CFBMode(key_bytes)
            elif args.mode == 'ofb':
                from modes.ofb import OFBMode
                mode_instance = OFBMode(key_bytes)
            elif args.mode == 'ctr':
                from modes.ctr import CTRMode
                mode_instance = CTRMode(key_bytes)
            else:
                raise ValueError(f"Unsupported mode: {args.mode}")
        except ImportError as e:
            print(f"Error: Could not import mode module - {e}", file=sys.stderr)
            sys.exit(1)

        # Perform encryption or decryption
        try:
            if args.decrypt:
                print("Performing decryption...")
                output_data = mode_instance.decrypt(input_data, iv)
                operation = "decrypted"
            else:
                print("Performing encryption...")
                output_data = mode_instance.encrypt(input_data, iv)
                # For encryption in modes other than ECB, prepend IV to output
                if args.mode != 'ecb' and iv is not None:
                    output_data = iv + output_data
                operation = "encrypted"

            # Write output file
            FileIO.write_file(args.output, output_data)

            print(f"✓ File successfully {operation}")
            print(f"  Input size: {len(input_data)} bytes")
            print(f"  Output size: {len(output_data)} bytes")

            # Show key reminder for encryption
            if not args.decrypt:
                print("\n" + "=" * 50)
                print("IMPORTANT: Save your key for decryption!")
                print(f"Key: {args.key}")
                if iv:
                    print(f"IV: {iv.hex()}" if args.mode != 'ecb' else "")
                print("=" * 50)

        except Exception as e:
            print(f"Error during {'decryption' if args.decrypt else 'encryption'}: {e}", file=sys.stderr)
            sys.exit(1)

    def _handle_hash(self, args):
        """Handle hash computation operations (Sprint 4)"""
        print(f"CryptoCore - Hash Computation Mode")
        print(f"Algorithm: {args.algorithm.upper()}")
        print(f"Input file: {args.input}")
        if args.output:
            print(f"Output file: {args.output}")
        print("-" * 50)

        # Import hash algorithm (Sprint 4)
        try:
            if args.algorithm == 'sha256':
                from hash.sha256 import SHA256
                hasher = SHA256()
            elif args.algorithm == 'sha3-256':
                from hash.sha3_256 import SHA3_256
                hasher = SHA3_256()
            else:
                print(f"Error: Unsupported hash algorithm '{args.algorithm}'", file=sys.stderr)
                sys.exit(1)
        except ImportError as e:
            print(f"Error: Could not import hash module - {e}", file=sys.stderr)
            sys.exit(1)

        # Read and hash file in chunks (for memory efficiency with large files)
        try:
            chunk_size = 65536  # 64KB chunks
            total_bytes = 0

            with open(args.input, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    hasher.update(chunk)
                    total_bytes += len(chunk)

                    # Show progress for large files
                    if total_bytes % (10 * 1024 * 1024) == 0:  # Every 10MB
                        print(f"  Processed: {total_bytes / (1024 * 1024):.1f} MB...", end='\r')

            # Get final hash
            hash_value = hasher.hexdigest()

            print(f"✓ Hash computed successfully")
            print(f"  File size: {total_bytes} bytes")
            print(f"  Hash ({args.algorithm}): {hash_value}")

            # Format output as per requirement: HASH_VALUE INPUT_FILE_PATH
            output_line = f"{hash_value}  {args.input}"

            # Write output to file or stdout
            if args.output:
                try:
                    with open(args.output, 'w') as out_f:
                        out_f.write(output_line + '\n')
                    print(f"✓ Hash saved to: {args.output}")
                except Exception as e:
                    print(f"Error writing output file: {e}", file=sys.stderr)
                    sys.exit(1)
            else:
                print("\n" + "=" * 50)
                print("Hash result:")
                print(output_line)

        except FileNotFoundError:
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        except PermissionError:
            print(f"Error: Permission denied accessing file: {args.input}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error during hash computation: {e}", file=sys.stderr)
            sys.exit(1)


def main():
    """Main function - entry point for the application"""
    cryptocore = CryptoCore()
    cryptocore.run()


if __name__ == '__main__':
    main()