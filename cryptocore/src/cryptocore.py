#!/usr/bin/env python3

import sys
import os

# Добавляем текущую папку в путь
sys.path.insert(0, os.path.dirname(__file__))

from cli_parser import CLIParser
from file_io import FileIO

# Класс ECBMode прямо здесь (чтобы избежать проблем с импортом)
from Crypto.Cipher import AES


class ECBMode:
    def __init__(self, key):
        if len(key) != 16:
            raise ValueError("Key must be 16 bytes")
        self.key = key
        self.block_size = 16

    def encrypt(self, plaintext):
        padded_data = self._pkcs7_pad(plaintext)
        cipher = AES.new(self.key, AES.MODE_ECB)

        encrypted_blocks = []
        for i in range(0, len(padded_data), self.block_size):
            block = padded_data[i:i + self.block_size]
            encrypted_block = cipher.encrypt(block)
            encrypted_blocks.append(encrypted_block)

        return b''.join(encrypted_blocks)

    def decrypt(self, ciphertext):
        if len(ciphertext) % self.block_size != 0:
            raise ValueError("Ciphertext must be multiple of block size")

        cipher = AES.new(self.key, AES.MODE_ECB)

        decrypted_blocks = []
        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]
            decrypted_block = cipher.decrypt(block)
            decrypted_blocks.append(decrypted_block)

        decrypted_data = b''.join(decrypted_blocks)
        return self._pkcs7_unpad(decrypted_data)

    def _pkcs7_pad(self, data):
        padding_length = self.block_size - (len(data) % self.block_size)
        padding = bytes([padding_length] * padding_length)
        return data + padding

    def _pkcs7_unpad(self, data):
        if len(data) == 0:
            return data

        padding_length = data[-1]

        if padding_length < 1 or padding_length > self.block_size:
            raise ValueError("Invalid padding")

        if data[-padding_length:] != bytes([padding_length] * padding_length):
            raise ValueError("Invalid padding")

        return data[:-padding_length]


class CryptoCore:
    def __init__(self):
        self.parser = CLIParser()

    def run(self):
        """Main application method"""
        try:
            # Parse command line arguments
            args = self.parser.parse_args()

            # Convert key from HEX to bytes
            key_bytes = bytes.fromhex(args.key)

            # Verify key size
            if len(key_bytes) != 16:
                print("Error: Key must be 16 bytes for AES-128", file=sys.stderr)
                sys.exit(1)

            # Read input file
            input_data = FileIO.read_file(args.input)

            # Perform operation
            if args.algorithm == 'aes' and args.mode == 'ecb':
                ecb = ECBMode(key_bytes)

                if args.encrypt:
                    output_data = ecb.encrypt(input_data)
                    print(f"File encrypted: {args.input} -> {args.output}")
                else:
                    output_data = ecb.decrypt(input_data)
                    print(f"File decrypted: {args.input} -> {args.output}")

                # Write output file
                FileIO.write_file(args.output, output_data)

            else:
                print("Error: Unsupported algorithm/mode", file=sys.stderr)
                sys.exit(1)

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


def main():
    """Application entry point"""
    cryptocore = CryptoCore()
    cryptocore.run()


if __name__ == '__main__':
    main()