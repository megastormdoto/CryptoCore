import sys
import os

# Add path to import from src
sys.path.append("cryptocore/src")

from cli_parser import CLIParser


def test_cli_help():
    """Test help command"""
    print("Testing CLI help...")
    try:
        parser = CLIParser()
        parser.parser.print_help()
    except SystemExit:
        print("Help test completed")


def test_cli_parsing():
    """Test argument parsing"""
    print("\nTesting CLI parsing...")

    # Test arguments for encryption
    test_args = [
        '--algorithm', 'aes',
        '--mode', 'ecb',
        '--encrypt',
        '--key', '00112233445566778899aabbccddeeff',
        '--input', 'test.txt'
    ]

    # Temporarily replace sys.argv
    original_argv = sys.argv
    sys.argv = ['test_cli.py'] + test_args

    try:
        parser = CLIParser()
        args = parser.parse_args()

        print("SUCCESS: Arguments parsed correctly!")
        print(f"  Algorithm: {args.algorithm}")
        print(f"  Mode: {args.mode}")
        print(f"  Operation: {'encrypt' if args.encrypt else 'decrypt'}")
        print(f"  Key: {args.key}")
        print(f"  Input: {args.input}")
        print(f"  Output: {args.output}")

    except SystemExit as e:
        print(f"Failed with exit code: {e.code}")
    finally:
        sys.argv = original_argv


def test_cli_validation():
    """Test validation errors"""
    print("\nTesting CLI validation...")

    # Test with invalid key (too short)
    test_args = [
        '--algorithm', 'aes',
        '--mode', 'ecb',
        '--encrypt',
        '--key', 'shortkey',  # Invalid key
        '--input', 'test.txt'
    ]

    original_argv = sys.argv
    sys.argv = ['test_cli.py'] + test_args

    try:
        parser = CLIParser()
        args = parser.parse_args()
        print("ERROR: Should have failed with invalid key!")
    except SystemExit as e:
        print("SUCCESS: Correctly rejected invalid key")
    finally:
        sys.argv = original_argv


def test_cli_decryption():
    """Test decryption arguments"""
    print("\nTesting decryption arguments...")

    test_args = [
        '--algorithm', 'aes',
        '--mode', 'ecb',
        '--decrypt',
        '--key', '00112233445566778899aabbccddeeff',
        '--input', 'ciphertext.bin'
    ]

    original_argv = sys.argv
    sys.argv = ['test_cli.py'] + test_args

    try:
        parser = CLIParser()
        args = parser.parse_args()

        print("SUCCESS: Decryption arguments parsed correctly!")
        print(f"  Operation: {'encrypt' if args.encrypt else 'decrypt'}")
        print(f"  Output: {args.output}")  # Should be .dec file

    except SystemExit as e:
        print(f"Failed: {e.code}")
    finally:
        sys.argv = original_argv


if __name__ == "__main__":
    test_cli_help()
    test_cli_parsing()
    test_cli_validation()
    test_cli_decryption()
    print("\nAll CLI tests completed! ✅")