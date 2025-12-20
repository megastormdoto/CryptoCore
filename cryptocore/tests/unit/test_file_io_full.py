#!/usr/bin/env python3
"""Full tests for file_io."""
import unittest
import tempfile
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


class TestFileIOFull(unittest.TestCase):
    def setUp(self):
        """Create temp files."""
        self.temp_files = []

    def tearDown(self):
        """Clean up temp files."""
        for f in self.temp_files:
            if os.path.exists(f):
                try:
                    os.unlink(f)
                except:
                    pass

    def create_temp_file(self, content=b""):
        """Create temporary file with content."""
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as f:
            if content:
                f.write(content)
            temp_file = f.name
            self.temp_files.append(temp_file)
        return temp_file

    def test_read_file_exists(self):
        """Test that FileIO class exists."""
        import file_io
        self.assertTrue(hasattr(file_io, 'FileIO'))

    def test_read_write_basic(self):
        """Basic read/write test."""
        from file_io import FileIO

        test_data = b"Hello, World!"
        temp_file = self.create_temp_file()

        # Write
        FileIO.write_file(temp_file, test_data)

        # Read
        result = FileIO.read_file(temp_file)
        self.assertEqual(result, test_data)

    def test_read_empty_file(self):
        """Test reading empty file."""
        from file_io import FileIO

        temp_file = self.create_temp_file(b"")
        result = FileIO.read_file(temp_file)
        self.assertEqual(result, b"")

    def test_write_large_file(self):
        """Test writing large file."""
        from file_io import FileIO

        # 10KB of data
        test_data = b"X" * 10240
        temp_file = self.create_temp_file()

        FileIO.write_file(temp_file, test_data)

        # Verify size
        with open(temp_file, 'rb') as f:
            result = f.read()
        self.assertEqual(len(result), 10240)

    def test_read_nonexistent_file_raises(self):
        """Test reading non-existent file raises error."""
        from file_io import FileIO

        # This should raise SystemExit (because file_io calls sys.exit)
        with self.assertRaises(SystemExit):
            FileIO.read_file("/nonexistent/path/file.txt")

    def test_write_to_directory_raises(self):
        """Test writing to directory path raises error."""
        from file_io import FileIO

        # Try to write to a directory (should raise SystemExit)
        # Use a real directory that exists
        import tempfile
        temp_dir = tempfile.gettempdir()

        with self.assertRaises(SystemExit):
            FileIO.write_file(temp_dir, b"test")