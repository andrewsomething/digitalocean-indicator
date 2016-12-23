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
import responses

from digitalocean import Droplet, baseapi
from digitalocean_indicator import DoIndicator
from requests.exceptions import ConnectionError

sys.path.insert(0, os.path.realpath(os.path.join(
    os.path.dirname(__file__), "..")))


class TestDoIndicator(unittest.TestCase):
    def setUp(self):
        self.do_api_token = 'aspecialsecret'
        self.base_url = "https://api.digitalocean.com/v2/"

        self.DoIndicator_members = [
            'AppIndicator3', 'ConnectionError', 'DoPreferencesDialog', 'GLib',
            'Gdk', 'Gio', 'Gtk', 'Indicator', 'IndicatorError', 'Notify',
            'digitalocean', 'get_media_file', 'gettext', 'gi', 'os', 'time']

    def _load_from_file(self, json_file):
        cwd = os.path.dirname(__file__)
        with open(os.path.join(cwd, 'fixtures/%s' % json_file), 'r') as f:
            return f.read()

    def test_DoIndicator_members(self):
        all_members = dir(DoIndicator)
        public_members = [x for x in all_members if not x.startswith('_')]
        public_members.sort()

        self.assertEqual(self.DoIndicator_members, public_members)

    def test_build_droplet_details_active(self):
        droplet = Droplet(name="test", image={'name': 'Ubuntu'},
                          status="active", ip_address="192.0.2.0",
                          size_slug="1gb", region={'name': 'nyc3'},
                          tags=['foo', 'bar'])
        indicator = DoIndicator.Indicator()
        sub_menu = indicator.build_droplet_details(droplet)

        ip = sub_menu.get_children()[0]
        image = sub_menu.get_children()[1]
        region = sub_menu.get_children()[2]
        size = sub_menu.get_children()[3]
        tags = sub_menu.get_children()[4]
        view = sub_menu.get_children()[6]
        power = sub_menu.get_children()[7]
        reboot = sub_menu.get_children()[8]

        self.assertEqual(len(sub_menu), 9)
        self.assertEqual(ip.get_label(), "IP: 192.0.2.0")
        self.assertEqual(region.get_label(), "Region: nyc3")
        self.assertEqual(image.get_label(), "Type: Ubuntu")
        self.assertEqual(size.get_label(), "Size: 1gb")
        self.assertEqual(tags.get_label(), "Tags: foo, bar")
        self.assertEqual(view.get_label(), "View on web...")
        self.assertEqual(power.get_label(), "Power off...")
        self.assertEqual(reboot.get_label(), "Reboot...")

    def test_build_droplet_details_inactive(self):
        droplet = Droplet(name="test", image={'name': 'Ubuntu'},
                          status="inactive", ip_address="192.0.2.0",
                          size_slug="1gb", region={'name': 'nyc3'})
        indicator = DoIndicator.Indicator()
        sub_menu = indicator.build_droplet_details(droplet)

        power = sub_menu.get_children()[6]

        self.assertEqual(power.get_label(), "Power on...")

    @responses.activate
    def test_get_droplets(self):
        data = self._load_from_file('droplet.json')

        url = self.base_url + 'droplets/'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        indicator = DoIndicator.Indicator(self.do_api_token)
        droplets = indicator.get_droplets()
        d = droplets[0]

        self.assertEqual(len(droplets), 1)
        self.assertEqual(d.name, "example.com")

    @responses.activate
    def test_build_menu(self):
        data = self._load_from_file('droplet.json')

        url = self.base_url + 'droplets/'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        indicator = DoIndicator.Indicator(self.do_api_token)
        indicator.build_menu()

        name = indicator.menu.get_children()[0]
        prefs = indicator.menu.get_children()[-3]
        refresh = indicator.menu.get_children()[-2]
        quit = indicator.menu.get_children()[-1]

        self.assertEqual(len(indicator.menu), 10)
        self.assertEqual(name.get_label(), "example.com")
        self.assertEqual(refresh.get_label(), "Refresh")
        self.assertEqual(prefs.get_label(), "Preferences")
        self.assertEqual(quit.get_label(), "Quit")

    @responses.activate
    def test_build_menu_connection_error(self):
        exception = ConnectionError('Internet is down')
        url = self.base_url + 'droplets/'
        responses.add(responses.GET, url,
                      body=exception)

        indicator = DoIndicator.Indicator(self.do_api_token)
        indicator.build_menu()

        error = indicator.menu.get_children()[0]

        self.assertEqual(len(indicator.menu), 10)
        self.assertEqual(error.get_label(), "No network connection.")

    def test_build_menu_no_token(self):
        indicator = DoIndicator.Indicator()
        indicator.build_menu()

        error = indicator.menu.get_children()[0]

        self.assertEqual(len(indicator.menu), 10)
        self.assertEqual(error.get_label(),
                         "Please connect to your DigitalOcean account.")

    @responses.activate
    def test_build_menu_bad_token(self):
        url = self.base_url + 'droplets/'
        responses.add(responses.GET, url,
                      body='{"id":"unauthorized","message":"Unable to authenticate you."}',
                      status=401)

        indicator = DoIndicator.Indicator(self.do_api_token)
        indicator.build_menu()

        error = indicator.menu.get_children()[0]

        self.assertEqual(len(indicator.menu), 10)
        self.assertEqual(error.get_label(),
                         "Please connect to your DigitalOcean account.")


if __name__ == '__main__':
    unittest.main()
