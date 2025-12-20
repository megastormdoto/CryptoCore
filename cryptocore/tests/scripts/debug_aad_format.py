# tests/test_aad_format.py
# !/usr/bin/env python3
"""
Test AAD format issue
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


# Mock the args to see what's happening
class MockArgs:
    def __init__(self):
        self.command = 'encrypt'
        self.key = '00112233445566778899aabbccddeeff'
        self.input = 'test.txt'
        self.output = 'test.bin'
        self.mode = 'gcm'
        self.decrypt = False
        self.aad = 'aabbccdd'  # This is what CLI receives


args = MockArgs()

print("Testing AAD parsing...")
print(f"args.aad type: {type(args.aad)}")
print(f"args.aad value: {args.aad}")

# Simulate what cryptocore.py does
if hasattr(args, 'aad') and args.aad:
    print(f"\n1. args.aad exists: {args.aad}")

    # Try different conversions
    print("\n2. Trying different conversions:")

    # Option 1: Assume it's hex string
    try:
        aad_bytes1 = bytes.fromhex(args.aad)
        print(f"   bytes.fromhex('{args.aad}'): {aad_bytes1}")
    except Exception as e:
        print(f"   bytes.fromhex failed: {e}")

    # Option 2: Assume it's already bytes
    if isinstance(args.aad, bytes):
        print(f"   args.aad is already bytes: {args.aad}")

    # Option 3: Assume it's string, encode to bytes
    aad_bytes3 = args.aad.encode('utf-8')
    print(f"   args.aad.encode('utf-8'): {aad_bytes3}")

    # Option 4: If it's hex string representation like "b'\\xaa\\xbb\\xcc\\xdd'"
    if args.aad.startswith("b'") and args.aad.endswith("'"):
        print(f"   It looks like a bytes representation: {args.aad}")
        # This would need eval(), which is dangerous

print("\n" + "=" * 50)
print("Now let's check what cli_parser actually returns...")

# Try to import and test cli_parser
try:
    from cli_parser import CLIParser
    import argparse

    # Create a test parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--aad', help='AAD')

    # Test parsing
    test_args = parser.parse_args(['--aad', 'aabbccdd'])
    print(f"\nargparse.parse_args(['--aad', 'aabbccdd']).aad:")
    print(f"  Type: {type(test_args.aad)}")
    print(f"  Value: {test_args.aad}")

    # Now test with actual CLIParser
    print("\nTesting actual CLIParser...")
    cli = CLIParser()

    # We can't easily test parse_args without command line args
    # But let's see the setup
    print("CLIParser setup complete")

except ImportError as e:
    print(f"Could not import cli_parser: {e}")
except Exception as e:
    print(f"Error: {e}")