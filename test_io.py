import sys
import os

print("Script started...")


sys.path.append("cryptocore/src")
print("sys.path updated")

try:
    from file_io import FileIO

    print("FileIO imported successfully")
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


def test_file_io():
    print("Testing FileIO...")

    try:

        data = FileIO.read_file("test.txt")
        print(f"Read: {data}")


        FileIO.write_file("test_copy.txt", data)
        print("File written successfully!")


        original = FileIO.read_file("test.txt")
        copy = FileIO.read_file("test_copy.txt")

        if original == copy:
            print("SUCCESS: Files are identical!")
        else:
            print("FAILED: Files are different!")

    except Exception as e:
        print(f"Error during file operations: {e}")


if __name__ == "__main__":
    test_file_io()