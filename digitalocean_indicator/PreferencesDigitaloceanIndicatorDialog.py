# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
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
        # Code for other initialization actions should be added here.

