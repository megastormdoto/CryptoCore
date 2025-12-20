# CryptoCore Development Guide

## Development Environment Setup

### Prerequisites
- Python 3.8 or higher
- Git
- pip

### Initial Setup
```bash
# Clone repository
git clone https://github.com/megastormdoto/CryptoCore
cd CryptoCore

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

## Project Structure

```
CryptoCore/
├── src/                    # Source code
│   └── cryptocore/        # Main package
│       ├── __init__.py
│       ├── aes.py         # AES implementation
│       ├── hash/          # Hash functions
│       │   ├── __init__.py
│       │   ├── sha256.py  # SHA-256
│       │   └── sha3_256.py
│       ├── modes/         # Encryption modes
│       │   ├── __init__.py
│       │   ├── cbc.py     # CBC mode
│       │   ├── gcm.py     # GCM mode
│       │   └── ctr.py     # CTR mode
│       ├── kdf/           # Key derivation
│       │   ├── __init__.py
│       │   ├── pbkdf2.py  # PBKDF2
│       │   └── hkdf.py    # HKDF-like
│       ├── hmac.py        # HMAC
│       ├── padding.py     # PKCS7 padding
│       ├── random.py      # CSPRNG
│       └── cli.py         # CLI interface
├── tests/                  # Test suites
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   ├── vectors/           # Test vectors
│   └── run_tests.py       # Test runner
├── docs/                   # Documentation
├── scripts/               # Utility scripts
├── pyproject.toml         # Project configuration
├── requirements.txt       # Dependencies
└── Makefile              # Build automation
```

## Running Tests

### Test Structure
```
tests/
├── unit/                  # Unit tests for individual components
│   ├── test_aes.py       # AES tests
│   ├── test_gcm.py       # GCM tests
│   ├── test_pbkdf2.py    # PBKDF2 tests
│   ├── test_hmac.py      # HMAC tests
│   └── test_hash.py      # Hash tests
├── integration/          # End-to-end tests
│   ├── test_cli.py       # CLI tests
│   └── test_interop.py   # OpenSSL compatibility
├── vectors/              # Test vectors from standards
│   ├── aes/             # NIST AES vectors
│   ├── gcm/             # NIST GCM vectors
│   ├── sha256/          # SHA-256 vectors
│   ├── hmac/            # HMAC vectors (RFC 4231)
│   └── pbkdf2/          # PBKDF2 vectors (RFC 6070)
└── run_tests.py         # Unified test runner
```

### Running Tests
```bash
# Run all tests
python tests/run_tests.py

# Or use pytest directly
pytest

# Run specific test categories
pytest tests/unit/                     # Unit tests only
pytest tests/integration/              # Integration tests only
pytest tests/unit/test_aes.py          # Single test file
pytest -k "test_encrypt"              # Tests matching pattern

# Run with coverage
pytest --cov=src/cryptocore --cov-report=html

# Performance tests
pytest tests/performance/ -v
```

### Test Runner Script
```python
# tests/run_tests.py
#!/usr/bin/env python3
"""
Unified test runner for CryptoCore.
Usage: python run_tests.py [--unit] [--integration] [--all]
"""

import pytest
import sys

def main():
    args = sys.argv[1:]
    
    if not args or '--all' in args:
        # Run all tests
        return pytest.main(['tests/', '-v'])
    elif '--unit' in args:
        return pytest.main(['tests/unit/', '-v'])
    elif '--integration' in args:
        return pytest.main(['tests/integration/', '-v'])
    else:
        print("Usage: python run_tests.py [--unit|--integration|--all]")
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

## Adding New Features

### 1. Create Implementation
```python
# src/cryptocore/new_feature.py
"""
Implementation of new cryptographic feature.
Follow PEP 8 and add type hints.
"""

def new_crypto_function(param1: bytes, param2: int) -> bytes:
    """
    Brief description of function.
    
    Args:
        param1: Description
        param2: Description
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When invalid input
        
    Example:
        >>> result = new_crypto_function(b'input', 100)
        >>> len(result)
        32
    """
    # Implementation
    pass
```

### 2. Add Unit Tests
```python
# tests/unit/test_new_feature.py
"""
Unit tests for new_feature module.
"""

import pytest
from cryptocore.new_feature import new_crypto_function

def test_basic_functionality():
    """Test basic use case."""
    result = new_crypto_function(b'test', 10)
    assert isinstance(result, bytes)
    assert len(result) > 0

def test_with_test_vectors():
    """Test against known-answer test vectors."""
    # Load test vectors
    with open('tests/vectors/new_feature/vectors.txt') as f:
        for line in f:
            input_data, expected = line.strip().split(',')
            result = new_crypto_function(
                bytes.fromhex(input_data), 
                1000
            )
            assert result.hex() == expected

def test_error_conditions():
    """Test error handling."""
    with pytest.raises(ValueError):
        new_crypto_function(b'', -1)  # Invalid input
```

### 3. Update CLI (if needed)
```python
# In src/cryptocore/cli.py
def add_new_feature_command(subparsers):
    """Add new command to CLI."""
    parser = subparsers.add_parser('newfeature', 
                                   help='New feature command')
    parser.add_argument('--input', required=True)
    parser.add_argument('--output')
    parser.set_defaults(func=handle_new_feature)

def handle_new_feature(args):
    """Handle new feature command."""
    # Implementation
    pass
```

### 4. Update Documentation
- Update `docs/API.md` with new functions
- Update `docs/USERGUIDE.md` if CLI changes
- Update this file if development process changes

## Code Quality

### Style Guidelines
- Follow PEP 8
- Use Black formatter (88 char line length)
- Use isort for import sorting
- Add type hints for all functions

### Setup Development Tools
```bash
# Install development tools
pip install black isort flake8 mypy pytest bandit

# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Check style
flake8 src/ tests/

# Type checking
mypy src/

# Security check
bandit -r src/
```

### Pre-commit Hook
Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
```

## Building and Distribution

### Building Package
```bash
# Build distribution
python -m build

# Check distribution
twine check dist/*

# Install locally
pip install dist/cryptocore-*.tar.gz
```

### Version Management
Update version in `pyproject.toml`:
```toml
[project]
name = "cryptocore"
version = "1.0.0"
```

## Test Vectors Management

### Adding Test Vectors
1. Download official test vectors from NIST/RFC sources
2. Place in appropriate directory under `tests/vectors/`
3. Create parser/loader in test files

### Example: Loading NIST Vectors
```python
# tests/unit/test_aes_vectors.py
import os

def load_nist_vectors(filename):
    """Load NIST format test vectors."""
    vectors = []
    current = {}
    
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith('KEY ='):
                current['key'] = bytes.fromhex(line.split('=')[1].strip())
            elif line.startswith('PLAINTEXT ='):
                current['plaintext'] = bytes.fromhex(line.split('=')[1].strip())
            elif line.startswith('CIPHERTEXT ='):
                current['ciphertext'] = bytes.fromhex(line.split('=')[1].strip())
                vectors.append(current.copy())
                current = {}
    
    return vectors
```

## Performance Testing

### Benchmark Script
```python
# scripts/benchmark.py
#!/usr/bin/env python3
"""
Performance benchmarks for CryptoCore.
"""

import time
import hashlib
from cryptocore.aes import AES
from cryptocore.kdf import pbkdf2_hmac_sha256

def benchmark_aes():
    """Benchmark AES encryption."""
    aes = AES(b'0' * 16)
    data = b'x' * 1024 * 1024  # 1MB
    
    start = time.time()
    for _ in range(100):
        aes.encrypt_block(data[:16])
    elapsed = time.time() - start
    
    print(f"AES-128 block encryption: {100/elapsed:.1f} ops/sec")

def benchmark_pbkdf2():
    """Benchmark PBKDF2."""
    start = time.time()
    pbkdf2_hmac_sha256("password", "salt", 10000, 32)
    elapsed = time.time() - start
    
    print(f"PBKDF2-HMAC-SHA256 (10k iterations): {elapsed:.2f} seconds")
    print(f"Projected 100k iterations: {elapsed * 10:.2f} seconds")

if __name__ == '__main__':
    benchmark_aes()
    benchmark_pbkdf2()
```

## Debugging

### Common Issues

#### Import Errors
```bash
# Make sure package is installed in development mode
pip install -e .

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

#### Test Failures
1. **Check test vectors**: Verify they match algorithm specifications
2. **Check endianness**: Crypto often uses big-endian
3. **Check padding**: Ensure PKCS7 padding is correct

#### Performance Issues
- Use `cProfile`: `python -m cProfile -o profile.stats script.py`
- Use `memory_profiler` for memory leaks
- Consider optimizing with `numpy` for vectorized operations

## Security Considerations for Development

### Critical Rules
1. **Never log sensitive data** (keys, passwords, plaintext)
2. **Clear memory after use**: Zero out sensitive variables
3. **Use constant-time comparisons** for MAC/authentication
4. **Validate all inputs** (key lengths, IV sizes, etc.)
5. **Never reuse nonces** with same key in GCM

### Security Checklist
- [ ] No secrets in source code
- [ ] Memory cleared after sensitive operations
- [ ] Input validation on all parameters
- [ ] Constant-time string comparison for MACs
- [ ] Proper error messages (no information leakage)
- [ ] Secure random number generation

## Contributing Workflow

### 1. Fork and Clone
```bash
git clone https://github.com/YOUR_USERNAME/CryptoCore
cd CryptoCore
git checkout -b feature/new-algorithm
```

### 2. Make Changes
- Implement feature
- Add tests
- Update documentation

### 3. Test Thoroughly
```bash
# Run full test suite
python tests/run_tests.py --all

# Check code quality
black src/ tests/
flake8 src/ tests/
mypy src/

# Run security checks
bandit -r src/
```

### 4. Submit Pull Request
- Ensure all tests pass
- Update documentation
- Add changelog entry if needed

## Release Process

### 1. Version Bump
```bash
# Update version in pyproject.toml
# Commit: "Bump version to 1.1.0"
```

### 2. Create Release
```bash
# Tag release
git tag -a v1.1.0 -m "Release version 1.1.0"
git push --tags

# Build and upload
python -m build
twine upload dist/*
```

### 3. Update Documentation
- Update `CHANGELOG.md`
- Create release notes on GitHub
- Verify all documentation is current

## Getting Help

- Check existing GitHub issues
- Review test cases for usage examples
- Run in debug mode: `cryptocore --verbose --debug ...`
- Enable detailed logging: `import logging; logging.basicConfig(level=logging.DEBUG)`

---

**Next Steps:**
1. Create `tests/` directory structure
2. Write `tests/run_tests.py`
3. Add test vectors from NIST/RFC
4. Create `Makefile` with common commands