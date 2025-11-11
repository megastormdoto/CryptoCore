#!/usr/bin/env python3
"""
CryptoCore - Main Entry Point
"""

import sys
import os

# Добавляем путь к исходному коду
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'cryptocore', 'src'))

from cryptocore import main

if __name__ == '__main__':
    main()