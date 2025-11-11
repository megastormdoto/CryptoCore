#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from cli_parser import CLIParser
from file_io import FileIO

class CryptoCore:
    def __init__(self):
        self.parser = CLIParser()

    def run(self):
        try:
            args = self.parser.parse_args()
            key_bytes = bytes.fromhex(args.key)

            if len(key_bytes) != 16:
                print("Error: Key must be 16 bytes for AES-128", file=sys.stderr)
                sys.exit(1)

            iv = None
            input_data = FileIO.read_file(args.input)

            if args.encrypt:
                if args.mode != 'ecb':
                    iv = os.urandom(16)
            else:
                if args.mode != 'ecb':
                    if args.iv:
                        iv = bytes.fromhex(args.iv)
                    else:
                        if len(input_data) < 16:
                            print("Error: Input file too short to contain IV", file=sys.stderr)
                            sys.exit(1)
                        iv = input_data[:16]
                        input_data = input_data[16:]

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

            if args.encrypt:
                output_data = mode_instance.encrypt(input_data, iv)
                if args.mode != 'ecb' and iv is not None:
                    output_data = iv + output_data
                print(f"File encrypted: {args.input} -> {args.output}")
            else:
                output_data = mode_instance.decrypt(input_data, iv)
                print(f"File decrypted: {args.input} -> {args.output}")

            FileIO.write_file(args.output, output_data)

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

def main():
    cryptocore = CryptoCore()
    cryptocore.run()

if __name__ == '__main__':
    main()