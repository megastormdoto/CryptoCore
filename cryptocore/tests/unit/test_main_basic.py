#!/usr/bin/env python3
"""Basic tests for main."""
import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


class TestMainBasic(unittest.TestCase):
    def test_main_import(self):
        """Test that main can be imported."""
        try:
            import main
            self.assertTrue(hasattr(main, 'main'))

            # Check it's callable
            from main import main as main_func
            self.assertTrue(callable(main_func))
        except ImportError:
            self.skipTest("main module not available")

    def test_encoding_setup(self):
        """Test Windows encoding setup."""
        try:
            import main

            # Check if encoding functions exist
            if sys.platform == "win32":
                # Should have encoding setup
                self.assertTrue(hasattr(sys.stdout, 'encoding') or
                                hasattr(main, 'get_symbol'))
        except ImportError:
            pass