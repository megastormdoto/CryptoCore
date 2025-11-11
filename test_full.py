# test_full.py - тест полной функциональности
import sys
import os

# Добавляем правильный путь
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "cryptocore", "src")
sys.path.insert(0, src_path)

print(f"Python path: {sys.path}")

try:
    from cryptocore import CryptoCore

    print("✅ CryptoCore imported successfully!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def test_encryption():
    print("Testing full encryption...")

    # Create test file
    with open("test_plain.txt", "wb") as f:
        f.write(b"This is a test file for CryptoCore!")

    # Simulate encryption command
    test_args = [
        '--algorithm', 'aes',
        '--mode', 'ecb',
        '--encrypt',
        '--key', '00112233445566778899aabbccddeeff',
        '--input', 'test_plain.txt',
        '--output', 'test_encrypted.bin'
    ]

    original_argv = sys.argv
    sys.argv = ['test_full.py'] + test_args

    try:
        cryptocore = CryptoCore()
        cryptocore.run()
        print("✅ Encryption successful!")
    except SystemExit:
        print("✅ Encryption completed!")
    except Exception as e:
        print(f"❌ Encryption failed: {e}")
    finally:
        sys.argv = original_argv


def test_decryption():
    print("Testing full decryption...")

    # Simulate decryption command
    test_args = [
        '--algorithm', 'aes',
        '--mode', 'ecb',
        '--decrypt',
        '--key', '00112233445566778899aabbccddeeff',
        '--input', 'test_encrypted.bin',
        '--output', 'test_decrypted.txt'
    ]

    original_argv = sys.argv
    sys.argv = ['test_full.py'] + test_args

    try:
        cryptocore = CryptoCore()
        cryptocore.run()
        print("✅ Decryption successful!")
    except SystemExit:
        print("✅ Decryption completed!")
    except Exception as e:
        print(f"❌ Decryption failed: {e}")
    finally:
        sys.argv = original_argv


if __name__ == "__main__":
    test_encryption()
    test_decryption()

    # Verify files are identical
    try:
        with open("test_plain.txt", "rb") as f1, open("test_decrypted.txt", "rb") as f2:
            if f1.read() == f2.read():
                print("🎉 SUCCESS: Round-trip test passed!")
            else:
                print("❌ FAILED: Files are different!")
    except FileNotFoundError:
        print("❌ Test files not found - something went wrong")