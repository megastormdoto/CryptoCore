import sys
import os

print("=== CHECKING IMPORTS ===")
print(f"Current dir: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Add src to path
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, src_path)
print(f"\nAdded to path: {src_path}")

print("\n=== TRYING TO IMPORT MODULES ===")

try:
    from hash.sha256 import SHA256

    print("✓ Imported SHA256")

    from hash.sha3_256 import SHA3_256

    print("✓ Imported SHA3_256")

    from mac.hmac import HMAC

    print("✓ Imported HMAC")

    # Test instantiation
    print("\n=== TESTING INSTANTIATION ===")
    key = b'testkey'
    hmac = HMAC(key, SHA256)
    print(f"✓ Created HMAC instance: {hmac}")

    # Test computation
    result = hmac.compute(b"test").hex()
    print(f"✓ Computed HMAC: {result[:16]}...")

    print("\n✅ ALL IMPORTS WORKING!")

except ImportError as e:
    print(f"\n❌ IMPORT ERROR: {e}")
    import traceback

    traceback.print_exc()

    # Show directory structure
    print("\n=== DIRECTORY STRUCTURE ===")
    for root, dirs, files in os.walk('.'):
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            if file.endswith('.py'):
                print(f"{subindent}{file}")