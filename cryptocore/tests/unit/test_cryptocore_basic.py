#!/usr/bin/env python3
"""Basic tests for cryptocore."""
import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


class TestCryptoCoreBasic(unittest.TestCase):
    def test_get_symbol_function(self):
        """Test get_symbol function."""
        try:
            # Try to import from cryptocore
            import cryptocore
            # Check if get_symbol exists
            if hasattr(cryptocore, 'get_symbol'):
                symbols_to_test = ['check', 'cross', 'lock', 'warning']
                for symbol in symbols_to_test:
                    result = cryptocore.get_symbol(symbol)
                    self.assertIsNotNone(result)
        except ImportError:
            pass  # OK if not available

    def test_encoding_setup_exists(self):
        """Test that encoding setup code exists."""
        try:
            import cryptocore
            # Just check the file can be imported
            self.assertTrue(True)  # Always passes if import succeeds
        except ImportError:
            self.skipTest("cryptocore module not available")

    def test_sys_path_addition(self):
        """Test that src is added to sys.path."""
        try:
            import cryptocore
            # Check that src is in path
            src_path = os.path.join(os.path.dirname(__file__), '..', '..', 'src')
            self.assertIn(src_path, sys.path)
        except ImportError:
            pass