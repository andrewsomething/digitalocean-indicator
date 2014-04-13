# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

# This is your preferences dialog.
#
# Define your preferences in
# data/glib-2.0/schemas/net.launchpad.digitalocean-indicator.gschema.xml
# See http://developer.gnome.org/gio/stable/GSettings.html for more info.

from gi.repository import Gio # pylint: disable=E0611

from locale import gettext as _

import logging
logger = logging.getLogger('digitalocean_indicator')

from digitalocean_indicator_lib.PreferencesDialog import PreferencesDialog

class PreferencesDigitaloceanIndicatorDialog(PreferencesDialog):
    __gtype_name__ = "PreferencesDigitaloceanIndicatorDialog"

    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the preferences dialog"""
        super(PreferencesDigitaloceanIndicatorDialog, self).finish_initializing(builder)

        # Bind each preference widget to gsettings
        settings = Gio.Settings("com.andrewsomething.digitalocean-indicator")
        do_api_key = self.builder.get_object('do_api_key_entry')
        settings.bind("do-api-key", do_api_key, "text", Gio.SettingsBindFlags.DEFAULT)
        do_client_id = self.builder.get_object('do_client_id_entry')
        settings.bind("do-client-id", do_client_id, "text", Gio.SettingsBindFlags.DEFAULT)
        refresh_interval = self.builder.get_object('refresh_interval_spin')
        settings.bind("refresh-interval", refresh_interval, "value", Gio.SettingsBindFlags.DEFAULT)
        # Code for other initialization actions should be added here.

