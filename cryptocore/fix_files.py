# fix_files.py
import os


def clean_file(file_path):
    """Remove null bytes from a file"""
    try:
        with open(file_path, 'rb') as f:
            content = f.read()

        # Remove null bytes
        cleaned = content.replace(b'\x00', b'')

        with open(file_path, 'wb') as f:
            f.write(cleaned)

        print(f"Cleaned: {file_path}")
        return True
    except Exception as e:
        print(f"Error cleaning {file_path}: {e}")
        return False


def clean_directory(directory):
    """Clean all Python files in directory"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                clean_file(os.path.join(root, file))


if __name__ == '__main__':
    # Clean test files
    clean_directory('tests')
    # Clean src files
    clean_directory('src')
    print("All files cleaned!")