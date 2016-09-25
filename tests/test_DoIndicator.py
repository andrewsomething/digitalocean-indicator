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

from digitalocean_indicator import DoIndicator

sys.path.insert(0, os.path.realpath(os.path.join(
    os.path.dirname(__file__), "..")))


class TestDoIndicator(unittest.TestCase):
    def setUp(self):
        self.DoIndicator_members = [
            'AppIndicator3', 'DoPreferencesDialog', 'GLib', 'Gdk', 'Gio',
            'Gtk', 'Indicator', 'Notify', 'digitalocean', 'get_media_file',
            'gettext', 'gi', 'os', 'time']

    def test_DoIndicator_members(self):
        all_members = dir(DoIndicator)
        public_members = [x for x in all_members if not x.startswith('_')]
        public_members.sort()
        self.assertEqual(self.DoIndicator_members, public_members)


if __name__ == '__main__':
    unittest.main()
