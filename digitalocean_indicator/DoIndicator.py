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

import os
import time
import digitalocean

from gi.repository import Gtk, GLib, Gio, Gdk  # pylint: disable=E0611
from gi.repository import AppIndicator3  # pylint: disable=E0611
from gi.repository import Notify

from digitalocean_indicator.DoPreferencesDialog import DoPreferencesDialog
from digitalocean_indicator_lib.helpers import get_media_file

import gettext
from gettext import gettext as _
gettext.textdomain('digitalocean-indicator')


class Indicator:
    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new('digitalocean-indicator',
                         '',
                         AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        icon_uri = get_media_file("digitalocean-indicator.svg")
        icon_path = icon_uri.replace("file:///", '')
        self.indicator.set_icon(icon_path)

        Notify.init('DigitalOcean Indicator')

        self.PreferencesDialog = DoPreferencesDialog
        self.settings = Gio.Settings(
            "com.andrewsomething.digitalocean-indicator")
        self.settings.connect('changed', self.on_preferences_changed)
        self.preferences_dialog = None
        self.preferences_changed = False

        self.do_api_token = self.settings.get_string("do-api-token")

        self.menu = Gtk.Menu()

        # Add items to Menu and connect signals.
        self.build_menu()
        # Refresh menu every 10 min by default
        self.change_timeout = False
        self.interval = self.settings.get_int("refresh-interval")
        GLib.timeout_add_seconds(self.interval*60, self.timeout_set)

    def build_menu(self):
        self.add_droplets()

        self.seperator = Gtk.SeparatorMenuItem.new()
        self.seperator.show()
        self.menu.append(self.seperator)

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
            manager = digitalocean.Manager(token=self.do_api_token)
            my_droplets = manager.get_all_droplets()
            for droplet in my_droplets:
                droplet_item = Gtk.ImageMenuItem.new_with_label(droplet.name)
                droplet_item.set_always_show_image(True)
                if droplet.status == "active":
                    img = Gtk.Image.new_from_icon_name("gtk-ok",
                                                       Gtk.IconSize.MENU)
                    droplet_item.set_image(img)
                else:
                    img = Gtk.Image.new_from_icon_name("gtk-stop",
                                                       Gtk.IconSize.MENU)
                    droplet_item.set_image(img)
                droplet_item.show()
                sub_menu = Gtk.Menu.new()

                ip = Gtk.MenuItem.new()
                ip.set_label(_("IP: ") + str(droplet.ip_address))
                ip.connect('activate', self.on_ip_clicked)
                ip.show()
                sub_menu.append(ip)

                image = droplet.image['name']
                image_id = Gtk.MenuItem.new()
                image_id.set_label(_("Type: ") + image)
                image_id.show()
                sub_menu.append(image_id)

                region = droplet.region['name']
                region_id = Gtk.MenuItem.new()
                region_id.set_label(_("Region: ") + region)
                region_id.show()
                sub_menu.append(region_id)

                size = droplet.size_slug
                size_id = Gtk.MenuItem.new()
                size_id.set_label(_("Size: ") + size)
                size_id.show()
                sub_menu.append(size_id)

                seperator = Gtk.SeparatorMenuItem.new()
                seperator.show()
                sub_menu.append(seperator)

                web = Gtk.MenuItem.new()
                web.set_label(_("View on web..."))
                droplet_url = "https://cloud.digitalocean.com/droplets/%s" % droplet.id
                web.connect('activate', self.open_web_link, droplet_url)
                web.show()
                sub_menu.append(web)

                if droplet.status == "active":
                    power_off = Gtk.ImageMenuItem.new_with_label(
                        _("Power off..."))
                    power_off.set_always_show_image(True)
                    img = Gtk.Image.new_from_icon_name("system-shutdown",
                                                       Gtk.IconSize.MENU)
                    power_off.set_image(img)
                    power_off.connect('activate',
                                      self.on_power_toggled,
                                      droplet,
                                      'off')
                    power_off.show()
                    sub_menu.append(power_off)

                    reboot = Gtk.ImageMenuItem.new_with_label(_("Reboot..."))
                    reboot.set_always_show_image(True)
                    img = Gtk.Image.new_from_icon_name("system-reboot",
                                                       Gtk.IconSize.MENU)
                    reboot.set_image(img)
                    reboot.connect('activate',
                                   self.on_power_toggled,
                                   droplet,
                                   'reboot')
                    reboot.show()
                    sub_menu.append(reboot)

                else:
                    power_on = Gtk.ImageMenuItem.new_with_label(
                        _("Power on..."))
                    power_on.set_always_show_image(True)
                    img = Gtk.Image.new_from_icon_name("gtk-ok",
                                                       Gtk.IconSize.MENU)
                    power_on.set_image(img)
                    power_on.connect('activate',
                                     self.on_power_toggled,
                                     droplet,
                                     'on')
                    power_on.show()
                    sub_menu.append(power_on)

                sub_menu.show()
                droplet_item.set_submenu(sub_menu)
                self.menu.append(droplet_item)
        except Exception, e:
            if e.message:
                print("Error: ", e.message)
            if "Unable to authenticate you." or "No token provied." in e.message:
                error_indicator = Gtk.ImageMenuItem.new_with_label(
                    _("Please connect to your DigitalOcean account."))
            else:
                error_indicator = Gtk.ImageMenuItem.new_with_label(
                    _("No network connection."))
            img = Gtk.Image.new_from_icon_name("error", Gtk.IconSize.MENU)
            error_indicator.set_always_show_image(True)
            error_indicator.set_image(img)
            error_indicator.connect('activate', self.on_preferences_activate)
            error_indicator.show()
            self.menu.append(error_indicator)

    def timeout_set(self):
        self.rebuild_menu()
        if self.change_timeout:
            GLib.timeout_add_seconds(self.interval*60, self.timeout_set)
            return False
        return True

    def on_ip_clicked(self, widget):
        address = widget.get_label().replace("IP: ", '')
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(address, -1)
        message = 'IP address %s copied to clipboard' % address
        notification = Notify.Notification.new(
            'DigitalOcean Indicator',
            message,
            'digitalocean-indicator'
        )
        notification.show()

    def open_web_link(self, widget, url):
        Gtk.show_uri(None, url, Gdk.CURRENT_TIME)

    def on_power_toggled(self, widget, droplet, action):
        if action is "on":
            res = droplet.power_on()
        elif action is "reboot":
            res = droplet.reboot()
        else:
            res = droplet.power_off()
        action = digitalocean.Action(token=self.do_api_token)
        action.id = res['action']['id']
        loading = True
        while loading:
            action.load()
            if action.status == 'in-progress':
                time.sleep(2)
            else:
                loading = False
                break
        self.rebuild_menu()

    def on_preferences_changed(self, settings, key, data=None):
        if key == "refresh-interval":
            self.change_timeout = True
            self.interval = settings.get_int(key)
            GLib.timeout_add_seconds(self.interval*60, self.timeout_set)
        else:
            self.preferences_changed = True

    def on_preferences_activate(self, widget):
        """Display the preferences window for digitalocean-indicator."""
        if self.preferences_dialog is None:
            self.preferences_dialog = self.PreferencesDialog()  # pylint: disable=E1102
            self.preferences_dialog.connect('destroy',
                                            self.on_preferences_dialog_destroyed)
            self.preferences_dialog.show()
        if self.preferences_dialog is not None:
            self.preferences_dialog.present()

    def on_refresh_activate(self, widget):
        self.rebuild_menu()

    def rebuild_menu(self):
        for i in self.menu.get_children():
            self.menu.remove(i)
        self.build_menu()
        return True

    def on_preferences_dialog_destroyed(self, widget, data=None):
        self.preferences_dialog = None
        if self.preferences_changed is True:
            self.do_api_token = self.settings.get_string("do-api-token")
            self.rebuild_menu()
        self.preferences_changed = False

    def on_exit_activate(self, widget):
        self.on_destroy(widget)

    def on_destroy(self, widget, data=None):
        Gtk.main_quit()
