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

from gi.repository import GLib, Gio # pylint: disable=E0611

from locale import gettext as _

import logging, os
logger = logging.getLogger('digitalocean_indicator')

from digitalocean_indicator_lib.PreferencesDialog import PreferencesDialog
from digitalocean_indicator_lib.helpers import get_media_file

autostart_dir = os.path.join(GLib.get_user_config_dir(),"autostart/")
autostart_template = "digitalocean-indicator-autostart.desktop"
autostart_file = get_media_file(autostart_template)
autostart_file = autostart_file.replace("file:///", '')
installed_file = os.path.join(autostart_dir, autostart_template)

class DoPreferencesDialog(PreferencesDialog):
    __gtype_name__ = "PreferencesDigitaloceanIndicatorDialog"

    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the preferences dialog"""
        super(DoPreferencesDialog, self).finish_initializing(builder)

        # Bind each preference widget to gsettings
        settings = Gio.Settings("com.andrewsomething.digitalocean-indicator")
        do_api_key = self.builder.get_object('do_api_key_entry')
        settings.bind("do-api-key", do_api_key, "text", Gio.SettingsBindFlags.DEFAULT)
        do_client_id = self.builder.get_object('do_client_id_entry')
        settings.bind("do-client-id", do_client_id, "text", Gio.SettingsBindFlags.DEFAULT)
        refresh_interval = self.builder.get_object('refresh_interval_spin')
        settings.bind("refresh-interval", refresh_interval, "value", Gio.SettingsBindFlags.DEFAULT)

        self.autostart_switch = builder.get_object("autostart_switch")
        if os.path.isfile(installed_file):
            self.autostart_switch.set_active(True)
        self.autostart_switch.connect('notify::active', self.on_autostart_switch_activate)

    def on_autostart_switch_activate(self, widget, data=None):
        if self.autostart_switch.get_active():
            if not os.path.exists(autostart_dir):
                os.mkdir(autostart_dir)
            if os.path.isdir(autostart_dir):
                os.symlink(autostart_file, installed_file)
        else:
            os.unlink(installed_file)
