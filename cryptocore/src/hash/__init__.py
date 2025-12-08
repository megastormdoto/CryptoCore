#!/usr/bin/env python3
"""
Hash functions module for CryptoCore
"""

from .sha256 import SHA256, sha256
from .sha3_256 import SHA3_256, sha3_256

__all__ = ['SHA256', 'sha256', 'SHA3_256', 'sha3_256']