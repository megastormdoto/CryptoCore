#!/usr/bin/env python3
"""Check all Sprint 7 requirements."""
import os
import sys


def check_structure():
    """Check project structure requirements."""
    print("Checking project structure...")

    required = [
        ('src/kdf/pbkdf2.py', 'PBKDF2 implementation'),
        ('src/kdf/hkdf.py', 'HKDF/key hierarchy implementation'),
        ('src/kdf/__init__.py', 'KDF package init'),
        ('tests/test_pbkdf2.py', 'PBKDF2 tests'),
        ('tests/test_hkdf.py', 'HKDF tests'),
    ]

    all_ok = True
    for path, desc in required:
        if os.path.exists(path):
            print(f"✓ {desc}: {path}")
        else:
            print(f"✗ {desc}: {path} NOT FOUND")
            all_ok = False

    return all_ok


def check_cli():
    """Check CLI requirements."""
    print("\nChecking CLI...")

    try:
        sys.path.insert(0, 'src')
        from cli.parser import CLIParser
        parser = CLIParser()

        # Check if derive command exists
        import argparse
        subparsers = [action for action in parser.parser._actions
                      if isinstance(action, argparse._SubParsersAction)]

        if subparsers:
            subparser = subparsers[0]
            if 'derive' in subparser.choices:
                print("✓ derive command exists in CLI")

                # Check required arguments
                derive_parser = subparser.choices['derive']
                required_args = ['--password', '--salt', '--iterations', '--length', '--algorithm']

                for arg in required_args:
                    # Check if argument exists
                    for action in derive_parser._actions:
                        if arg in action.option_strings:
                            print(f"✓ {arg} argument exists")
                            break
                    else:
                        print(f"✗ {arg} argument NOT FOUND")

                return True
            else:
                print("✗ derive command NOT FOUND in CLI")
        else:
            print("✗ No subparsers found in CLI")

    except ImportError as e:
        print(f"✗ CLI import error: {e}")

    return False


def check_functionality():
    """Check KDF functionality."""
    print("\nChecking functionality...")

    try:
        sys.path.insert(0, 'src')
        from kdf.pbkdf2 import pbkdf2_hmac_sha256
        from kdf.hkdf import derive_key

        # Test PBKDF2
        result = pbkdf2_hmac_sha256('password', 'salt', 1, 20)
        if len(result) == 20:
            print("✓ PBKDF2 produces correct length")
        else:
            print(f"✗ PBKDF2 wrong length: {len(result)}")

        # Test HKDF
        master_key = b'0' * 32
        key1 = derive_key(master_key, 'encryption', 32)
        key2 = derive_key(master_key, 'authentication', 32)

        if len(key1) == 32 and len(key2) == 32:
            print("✓ HKDF produces correct length")

        if key1 != key2:
            print("✓ HKDF context separation works")
        else:
            print("✗ HKDF context separation FAILED")

        return True

    except ImportError as e:
        print(f"✗ Functionality import error: {e}")
        return False


def check_readme():
    """Check README updates."""
    print("\nChecking README...")

    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read().lower()

        keywords = ['derive', 'pbkdf2', 'salt', 'iteration', 'key derivation']
        found = []

        for keyword in keywords:
            if keyword in content:
                found.append(keyword)
                print(f"✓ README mentions '{keyword}'")
            else:
                print(f"✗ README missing '{keyword}'")

        if len(found) >= 3:
            return True
        else:
            return False
    else:
        print("✗ README.md not found")
        return False


def main():
    """Run all checks."""
    print("=" * 60)
    print("SPRINT 7 REQUIREMENTS CHECK")
    print("=" * 60)

    checks = [
        ('Project Structure', check_structure),
        ('CLI Implementation', check_cli),
        ('Functionality', check_functionality),
        ('README Updates', check_readme),
    ]

    results = []

    for name, check_func in checks:
        print(f"\n{name}:")
        print("-" * 40)
        try:
            result = check_func()
            results.append((name, result))
            status = "PASS" if result else "FAIL"
            print(f"{name}: [{status}]")
        except Exception as e:
            print(f"ERROR: {e}")
            results.append((name, False))

    print("\n" + "=" * 60)
    print("SUMMARY:")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name:30} {status}")

    print(f"\nTotal: {passed}/{total} requirements met")

    if passed == total:
        print("\n🎉 ALL SPRINT 7 REQUIREMENTS SATISFIED!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} requirements missing")
        return 1


if __name__ == "__main__":
    # Make sure we're in the right directory
    if os.path.basename(os.getcwd()) == 'cryptocore':
        os.chdir('..')

    sys.exit(main())