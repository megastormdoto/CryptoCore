import sys

class FileIO:
    @staticmethod
    def read_file(file_path):
        try:
            with open(file_path, 'rb') as file:
                return file.read()
        except IOError as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)

    @staticmethod
    def write_file(file_path, data):
        try:
            with open(file_path, 'wb') as file:
                file.write(data)
        except IOError as e:
            print(f"Error writing file: {e}", file=sys.stderr)
            sys.exit(1)