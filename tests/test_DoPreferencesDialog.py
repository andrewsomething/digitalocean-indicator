#!/usr/bin/python
"""
This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License version 3, as published
by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranties of
MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import os.path
import unittest

from digitalocean_indicator import DoPreferencesDialog

sys.path.insert(0, os.path.realpath(os.path.join(
    os.path.dirname(__file__), "..")))


class TestDoPreferencesDialog(unittest.TestCase):
    def setUp(self):
        self.DoPreferencesDialog_members = [
            'AuthWin', 'DoPreferencesDialog', 'GLib', 'Gio',
            'PreferencesDialog', 'autostart_dir', 'autostart_file',
            'autostart_template', 'get_media_file', 'gi', 'installed_file',
            'logger', 'logging', 'os', 'requests']

    def test_DoPreferencesDialog_members(self):
        all_members = dir(DoPreferencesDialog)
        public_members = [x for x in all_members if not x.startswith('_')]
        public_members.sort()
        self.assertEqual(self.DoPreferencesDialog_members, public_members)


if __name__ == '__main__':
    unittest.main()
