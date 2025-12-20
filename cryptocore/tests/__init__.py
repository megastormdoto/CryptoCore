"""
Test suite for CryptoCore.
"""

import os
import sys

# Add src directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_path = os.path.join(project_root, 'src')

if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Also add project root for relative imports
if project_root not in sys.path:
    sys.path.insert(0, project_root)

print(f"[DEBUG] Tests __init__ loaded")
print(f"[DEBUG] Current dir: {current_dir}")
print(f"[DEBUG] Project root: {project_root}")
print(f"[DEBUG] Src path: {src_path}")
print(f"[DEBUG] Python path: {sys.path}")