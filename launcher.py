#!/usr/bin/env python3
"""
Launcher for CryptoCore - handles import issues
"""
import sys
import os

# Путь к проекту - папка cryptocore внутри текущей директории
project_root = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(project_root, 'cryptocore')  # <-- ДОБАВЬТЕ ЭТО
src_dir = os.path.join(project_dir, 'src')  # <-- ИЗМЕНИТЕ НА ЭТО

# Проверяем что мы в правильном месте
print(f"Project root: {project_root}")
print(f"Project directory: {project_dir}")
print(f"Source directory: {src_dir}")

if not os.path.exists(project_dir):
    print(f"ERROR: Project directory not found at {project_dir}")
    print(f"Current directory contents:")
    for item in os.listdir(project_root):
        print(f"  {item}")
    sys.exit(1)

if not os.path.exists(src_dir):
    print(f"ERROR: src directory not found at {src_dir}")
    print(f"Contents of {project_dir}:")
    for item in os.listdir(project_dir):
        print(f"  {item}")
    sys.exit(1)

# Добавляем project_dir и src_dir в путь
sys.path.insert(0, project_dir)
sys.path.insert(0, src_dir)

print(f"\nPython path: {sys.path}")

# Теперь импортируем и запускаем
try:
    # Проверим можем ли импортировать hmac напрямую
    print("\nTrying to import HMAC...")

    # Пробуем несколько способов
    try:
        from mac.hmac import HMAC

        print("✓ Import successful with: from mac.hmac import HMAC")
    except ImportError:
        try:
            from src.mac.hmac import HMAC

            print("✓ Import successful with: from src.mac.hmac import HMAC")
        except ImportError:
            # Прямой импорт
            import sys

            sys.path.insert(0, os.path.join(src_dir, 'mac'))
            from hmac import HMAC

            print("✓ Import successful with direct import")

    # Протестируем сразу
    test_key = bytes.fromhex("0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b")
    test_data = b"Hi There"

    hmac = HMAC(test_key, 'sha256')
    result = hmac.compute_hex(test_data)

    print(f"\nTest HMAC result: {result}")
    print(f"Expected:         b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7")

    if result == "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7":
        print("\n✓ HMAC implementation is CORRECT!")
    else:
        print("\n✗ HMAC implementation is INCORRECT!")
        print(f"Difference: {result == 'b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7'}")

    # Теперь запустим основной интерфейс
    print("\n" + "=" * 60)
    print("Starting CryptoCore CLI...")
    print("=" * 60)

    # Пробуем импортировать cryptocore
    try:
        from cryptocore import main

        main()
    except ImportError as e:
        print(f"Could not import cryptocore: {e}")
        print("Trying to run command directly...")

        # Запустим тестовую команду напрямую
        import subprocess

        cmd = [sys.executable, os.path.join(project_dir, 'src', 'cryptocore.py'),
               'dgst', '--algorithm', 'sha256', '--hmac',
               '--key', '0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b',
               '--input', os.path.join(project_root, 'rfc_test.txt')]

        print(f"\nRunning: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"Return code: {result.returncode}")
        print(f"Stdout:\n{result.stdout}")
        if result.stderr:
            print(f"Stderr:\n{result.stderr}")

except ImportError as e:
    print(f"\nImport error: {e}")
    import traceback

    traceback.print_exc()

    # Покажем что есть в src
    print(f"\nContents of src directory:")
    for item in os.listdir(src_dir):
        item_path = os.path.join(src_dir, item)
        if os.path.isdir(item_path):
            print(f"  [DIR] {item}/")
        else:
            print(f"  [FILE] {item}")

    sys.exit(1)
except Exception as e:
    print(f"\nError: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)