#!/usr/bin/env python3
"""
Unified test runner for CryptoCore.
Usage: python tests/run_tests.py [--unit] [--integration] [--all] [--coverage]
"""

import sys
import os
import argparse


def setup_paths():
    """Set up Python paths for imports."""
    # Get the project root directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Add src to Python path
    src_path = os.path.join(project_root, 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    # Also add the project root
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    return project_root


def run_tests(test_type, coverage=False):
    """Run tests with specified options."""
    setup_paths()

    import pytest

    pytest_args = ['-v', '--tb=short']

    if coverage:
        pytest_args.extend([
            '--cov=src',
            '--cov-report=term',
            '--cov-report=html:coverage_html'
        ])

    # Determine which tests to run
    test_path = ''
    if test_type == 'all':
        test_path = 'tests'
    elif test_type == 'unit':
        test_path = 'tests/unit'
    elif test_type == 'integration':
        test_path = 'tests/integration'
    elif test_type == 'vectors':
        test_path = 'tests/vectors'
    elif test_type == 'scripts':
        test_path = 'tests/scripts'

    pytest_args.append(test_path)

    print(f"Running {test_type} tests from: {test_path}")
    print(f"Python path: {sys.path}")

    # Run pytest
    result = pytest.main(pytest_args)
    return result


def main():
    """Main entry point for test runner."""
    parser = argparse.ArgumentParser(
        description='CryptoCore Test Runner',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--unit',
        action='store_true',
        help='Run only unit tests'
    )

    parser.add_argument(
        '--integration',
        action='store_true',
        help='Run only integration tests'
    )

    parser.add_argument(
        '--vectors',
        action='store_true',
        help='Run vector tests'
    )

    parser.add_argument(
        '--scripts',
        action='store_true',
        help='Run script tests'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Run all tests (default)'
    )

    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Generate coverage report'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    # Determine test type
    test_types = ['unit', 'integration', 'vectors', 'scripts', 'all']
    selected_types = [t for t in test_types if getattr(args, t)]

    if len(selected_types) == 0:
        test_type = 'all'
    elif len(selected_types) == 1:
        test_type = selected_types[0]
    else:
        print("Error: Can only specify one test type at a time")
        return 1

    # Run tests
    return run_tests(test_type, args.coverage)


if __name__ == '__main__':
    sys.exit(main())