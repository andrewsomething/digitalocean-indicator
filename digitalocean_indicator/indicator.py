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

"""Code to add AppIndicator."""

from gi.repository import Gtk, GLib, Gio # pylint: disable=E0611
from gi.repository import AppIndicator3 # pylint: disable=E0611
import digitalocean
import os

from digitalocean_indicator.AboutDigitaloceanIndicatorDialog import AboutDigitaloceanIndicatorDialog
from digitalocean_indicator.PreferencesDigitaloceanIndicatorDialog import PreferencesDigitaloceanIndicatorDialog

import gettext
from gettext import gettext as _
gettext.textdomain('digitalocean-indicator')

class Indicator:
    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new('digitalocean-indicator',
                         'deluge-panel',
                         AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        self.PreferencesDialog = PreferencesDigitaloceanIndicatorDialog
        self.settings = Gio.Settings("com.andrewsomething.digitalocean-indicator")
        self.settings.connect('changed', self.on_preferences_changed)
        self.preferences_dialog = None
        self.preferences_changed  = False

        # If the key/id aren't set, take them from the environment.
        self.do_api_key = self.settings.get_string("do-api-key")
        if not self.do_api_key:
            try:
                self.settings.set_string("do-api-key", os.environ["DO_API_KEY"])
            except KeyError:
                pass

        self.do_client_id = self.settings.get_string("do-client-id")
        if not self.do_client_id:
            try:
                self.settings.set_string("do-client-id", os.environ["DO_CLIENT_ID"])
            except KeyError:
                pass

        self.menu = Gtk.Menu()

        # Add items to Menu and connect signals.
        self.build_menu()
        # Refresh menu every 10 min
        GLib.timeout_add_seconds(60 * 10, self.rebuild_menu)

    def build_menu(self):
        self.add_droplets()
        #Adding preferences button
        self.preferences = Gtk.MenuItem("Preferences")
        self.preferences.connect("activate", self.on_preferences_activate)
        self.preferences.show()
        self.menu.append(self.preferences)

        self.quit = Gtk.MenuItem("Refresh")
        self.quit.connect("activate", self.on_refresh_activate)
        self.quit.show()
        self.menu.append(self.quit)

        self.quit = Gtk.MenuItem("Quit")
        self.quit.connect("activate", self.on_exit_activate)
        self.quit.show()
        self.menu.append(self.quit)

        self.menu.show()
        self.indicator.set_menu(self.menu)

    def add_droplets(self):
        try:
            manager = digitalocean.Manager(client_id=self.do_client_id,
                                           api_key=self.do_api_key)
            my_droplets = manager.get_all_droplets()
            for droplet in my_droplets:
                droplet_item = Gtk.ImageMenuItem.new_with_label(droplet.name)
                droplet_item.set_always_show_image(True)
                if droplet.status == "active":
                    img = Gtk.Image.new_from_icon_name("gtk-ok", Gtk.IconSize.MENU)
                    droplet_item.set_image(img)
                else:
                    img = Gtk.Image.new_from_icon_name("gtk-stop", Gtk.IconSize.MENU)
                    droplet_item.set_image(img)
                droplet_item.show()
                self.menu.append(droplet_item)
        except Exception, e:
            if e.message:
                print("Error: ", e.message)
            if "Access Denied" in e.message:
                error_indicator = Gtk.ImageMenuItem.new_with_label(
                    _("Error logging in. Please check your credentials."))
            else:
                error_indicator = Gtk.ImageMenuItem.new_with_label(
                    _("No network connection."))
            img = Gtk.Image.new_from_icon_name("error", Gtk.IconSize.MENU)
            error_indicator.set_always_show_image(True)
            error_indicator.set_image(img)
            error_indicator.show()
            self.menu.append(error_indicator)

    def on_preferences_changed(self, settings, key, data=None):
        self.preferences_changed = True

    def on_preferences_activate(self, widget):
        """Display the preferences window for digitalocean-indicator."""
        if self.preferences_dialog is None:
            self.preferences_dialog = self.PreferencesDialog() # pylint: disable=E1102
            self.preferences_dialog.connect('destroy', self.on_preferences_dialog_destroyed)
            self.preferences_dialog.show()
        if self.preferences_dialog is not None:
            self.preferences_dialog.present()

    def on_refresh_activate(self, widget):
        self.rebuild_menu()

    def rebuild_menu(self):
        for i in self.menu.get_children():
            self.menu.remove(i)
        self.build_menu()
        print("Rebuilding....")
        return True

    def on_preferences_dialog_destroyed(self, widget, data=None):
        self.preferences_dialog = None
        if self.preferences_changed is True:
            self.do_api_key = self.settings.get_string("do-api-key")
            self.do_client_id = self.settings.get_string("do-client-id")
            self.rebuild_menu()
        self.preferences_changed  = False

    def on_exit_activate(self, widget):
        self.on_destroy(widget)

    def on_destroy(self, widget, data=None):
        Gtk.main_quit()
