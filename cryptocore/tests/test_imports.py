#!/usr/bin/env python3
"""
Test that all required modules can be imported
"""
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_imports():
    """Test importing all required modules"""
    print("Testing imports...")

    modules_to_test = [
        ('src.core.ciphers', ['AES']),
        ('src.modes.ecb', ['ECB']),
        ('src.modes.cbc', ['CBC']),
        ('src.modes.cfb', ['CFB']),
        ('src.modes.ofb', ['OFB']),
        ('src.modes.ctr', ['CTR']),
        ('src.modes.gcm', ['GCM', 'AuthenticationError']),
        ('src.aead.encrypt_then_mac', ['EncryptThenMAC']),
        ('src.cli.parser', ['CLIParser']),
    ]

    all_ok = True

    for module_name, expected_classes in modules_to_test:
        try:
            module = __import__(module_name, fromlist=expected_classes)
            print(f"✓ {module_name}")

            # Check classes
            for class_name in expected_classes:
                if hasattr(module, class_name):
                    print(f"  ✓ {class_name}")
                else:
                    print(f"  ✗ {class_name} not found in {module_name}")
                    all_ok = False

        except ImportError as e:
            print(f"✗ {module_name}: {e}")
            all_ok = False
        except Exception as e:
            print(f"✗ {module_name}: {type(e).__name__}: {e}")
            all_ok = False

    return all_ok


if __name__ == "__main__":
    if test_imports():
        print("\n✅ All imports successful!")
        sys.exit(0)
    else:
        print("\n❌ Some imports failed")
        sys.exit(1)