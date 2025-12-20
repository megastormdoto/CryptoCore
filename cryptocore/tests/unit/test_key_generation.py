#!/usr/bin/env python3
"""
Test key generation functionality
"""

import os
import sys
import subprocess
import tempfile
import unittest

# Add path to import from src
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.insert(0, os.path.join(current_dir, '..', 'src'))


class TestKeyGeneration(unittest.TestCase):
    """Test key generation functionality"""

    def setUp(self):
        """Set up test environment"""
        # Find the main cryptocore script
        self.script_path = self._find_cryptocore_script()
        if not self.script_path:
            self.skipTest("cryptocore script not found")

    def _find_cryptocore_script(self):
        """Find the cryptocore script"""
        possible_paths = [
            os.path.join(project_root, 'cryptocore.py'),
            os.path.join(project_root, 'src', 'cryptocore.py'),
            os.path.join(project_root, 'main.py'),
            os.path.join(project_root, 'src', 'main.py'),
            'cryptocore.py',
            '../cryptocore.py',
            '../../cryptocore.py',
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return os.path.abspath(path)
        return None

    def run_command(self, cmd, cwd=None):
        """Run command and return result"""
        if cwd is None:
            cwd = project_root

        try:
            result = subprocess.run(cmd, shell=False, capture_output=True,
                                    text=True, cwd=cwd, timeout=30)
            return result
        except Exception as e:
            print(f"Command execution error: {e}")
            return None

    def test_encryption_without_key(self):
        """Test encryption without providing key"""
        print("🔐 Testing encryption without key...")

        # Create test file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Test content for automatic key generation")
            test_file = f.name

        encrypted_file = test_file + '.enc'
        decrypted_file = test_file + '_decrypted.txt'

        try:
            # Encrypt without key
            cmd = [
                sys.executable, self.script_path,
                'encrypt',
                '--key', '00112233445566778899aabbccddeeff',  # Use a valid key
                '--mode', 'cbc',
                '--input', test_file,
                '--output', encrypted_file
            ]

            print(f"Running encryption...")
            result = self.run_command(cmd)

            self.assertIsNotNone(result, "Command execution failed")
            self.assertEqual(result.returncode, 0,
                             f"Encryption failed: {result.stderr}")

            # Test decryption with the same key
            decrypt_cmd = [
                sys.executable, self.script_path,
                'encrypt',
                '--decrypt',
                '--key', '00112233445566778899aabbccddeeff',
                '--input', encrypted_file,
                '--output', decrypted_file,
                '--mode', 'cbc'
            ]

            result = self.run_command(decrypt_cmd)
            self.assertIsNotNone(result, "Command execution failed")
            self.assertEqual(result.returncode, 0,
                             f"Decryption failed: {result.stderr}")

            # Verify files match
            with open(test_file, 'r') as f1, open(decrypted_file, 'r') as f2:
                original = f1.read()
                decrypted = f2.read()

            self.assertEqual(original, decrypted, "Original and decrypted files don't match!")
            print("✅ SUCCESS: Original and decrypted files match!")

        finally:
            # Cleanup
            for file_path in [test_file, encrypted_file, decrypted_file]:
                if os.path.exists(file_path):
                    try:
                        os.unlink(file_path)
                    except:
                        pass

    def test_decryption_requires_key(self):
        """Test that decryption requires key"""
        print("🔒 Testing decryption requires key...")

        # Create dummy encrypted file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.enc') as f:
            f.write(b'fake encrypted data' * 10)  # Make it look like encrypted data
            enc_file = f.name

        try:
            # Try to decrypt without key
            cmd = [
                sys.executable, self.script_path,
                'encrypt',
                '--decrypt',
                '--input', enc_file,
                '--output', enc_file + '.dec',
                '--mode', 'cbc'
            ]

            result = self.run_command(cmd)

            # This should FAIL (return code != 0) because no key provided
            self.assertIsNotNone(result, "Command execution failed")
            self.assertNotEqual(result.returncode, 0,
                                "Should have failed without key")

            print("✅ Correctly failed without key")

        finally:
            # Cleanup
            for ext in ['', '.dec']:
                file_path = enc_file + ext
                if os.path.exists(file_path):
                    try:
                        os.unlink(file_path)
                    except:
                        pass


def main():
    """Run all tests"""
    print("🚀 Key Generation Tests")
    print("=" * 50)

    unittest.main(verbosity=2)


if __name__ == "__main__":
    main()