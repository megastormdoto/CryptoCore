# run_tests.py
import sys
import os
import unittest

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def run_all_tests():
    """Run all tests"""
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code
    return 0 if result.wasSuccessful() else 1


def run_hmac_tests():
    """Run only HMAC tests"""
    from tests.test_hmac import TestHMAC

    suite = unittest.TestLoader().loadTestsFromTestCase(TestHMAC)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'hmac':
        sys.exit(run_hmac_tests())
    else:
        sys.exit(run_all_tests())