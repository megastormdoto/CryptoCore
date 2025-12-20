#!/usr/bin/env python3
"""Basic tests for CLI parser."""
import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


class TestCLIParserBasic(unittest.TestCase):
    def test_import(self):
        """Test that CLI parser can be imported."""
        import cli_parser
        self.assertTrue(hasattr(cli_parser, 'CLIParser'))

    def test_parser_creation(self):
        """Test parser creation."""
        from cli_parser import CLIParser

        parser = CLIParser()
        self.assertIsNotNone(parser)
        self.assertIsNotNone(parser.parser)

    def test_parser_attributes(self):
        """Test that parser has expected attributes."""
        from cli_parser import CLIParser

        parser = CLIParser()
        # Check basic attributes
        self.assertTrue(hasattr(parser, 'parser'))
        self.assertTrue(hasattr(parser, 'parse_args'))

    def test_parser_methods(self):
        """Test parser methods."""
        from cli_parser import CLIParser

        parser = CLIParser()
        # Check methods exist
        self.assertTrue(callable(parser.parse_args))