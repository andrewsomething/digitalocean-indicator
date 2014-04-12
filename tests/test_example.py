#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import sys
import os.path
import unittest
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))

from digitalocean_indicator import AboutDigitaloceanIndicatorDialog

class TestExample(unittest.TestCase):
    def setUp(self):
        self.AboutDigitaloceanIndicatorDialog_members = [
        'AboutDialog', 'AboutDigitaloceanIndicatorDialog', 'gettext', 'logger', 'logging']

    def test_AboutDigitaloceanIndicatorDialog_members(self):
        all_members = dir(AboutDigitaloceanIndicatorDialog)
        public_members = [x for x in all_members if not x.startswith('_')]
        public_members.sort()
        self.assertEqual(self.AboutDigitaloceanIndicatorDialog_members, public_members)

if __name__ == '__main__':    
    unittest.main()
