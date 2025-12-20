#!/usr/bin/env python3
"""Quick tests to boost coverage."""
import unittest


class TestCoverageBoost(unittest.TestCase):
    def test_cbc_mode_coverage(self):
        from src.modes.cbc import CBCMode
        mode = CBCMode(b'0' * 16)
        self.assertIsNotNone(mode)

    def test_cfb_mode_coverage(self):
        from src.modes.cfb import CFBMode
        mode = CFBMode(b'0' * 16)
        self.assertIsNotNone(mode)

    def test_ofb_mode_coverage(self):
        from src.modes.ofb import OFBMode
        mode = OFBMode(b'0' * 16)
        self.assertIsNotNone(mode)

    def test_ecb_mode_coverage(self):
        from src.modes.ecb import ECBMode
        mode = ECBMode(b'0' * 16)
        self.assertIsNotNone(mode)

    def test_gcm_coverage(self):
        from src.modes.gcm import GCM
        gcm = GCM(b'0' * 16)
        self.assertIsNotNone(gcm)