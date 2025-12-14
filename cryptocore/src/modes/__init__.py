"""
Block cipher modes of operation.
Sprint 6 focuses on GCM mode.
"""

# Импортируем только то, что нужно для Sprint 6
from .gcm import GCM, AuthenticationError

# Определяем другие режимы как заглушки если они нужны
try:
    from .ecb import ECB
except ImportError:
    class ECB:
        pass

try:
    from .cbc import CBC
except ImportError:
    class CBC:
        pass

try:
    from .cfb import CFB
except ImportError:
    class CFB:
        pass

try:
    from .ofb import OFB
except ImportError:
    class OFB:
        pass

try:
    from .ctr import CTR
except ImportError:
    class CTR:
        pass

__all__ = [
    'ECB', 'CBC', 'CFB', 'OFB', 'CTR',
    'GCM', 'AuthenticationError'
]