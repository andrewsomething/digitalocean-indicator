# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

"""Code to add AppIndicator."""

from gi.repository import Gtk, GLib # pylint: disable=E0611
from gi.repository import AppIndicator3 # pylint: disable=E0611
import digitalocean
import os

from digitalocean_indicator_lib.helpers import get_media_file

import gettext
from gettext import gettext as _
gettext.textdomain('digitalocean-indicator')

class Indicator:
    def __init__(self, window):
        self.indicator = AppIndicator3.Indicator.new('digitalocean-indicator',
                         'deluge-panel',
                         AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        #Uncomment and choose an icon for attention state. 
        #self.indicator.set_attention_icon("ICON-NAME")
        
        self.menu = Gtk.Menu()

        # Add items to Menu and connect signals.
        self.add_droplets()

        
        #Adding preferences button 
        #window represents the main Window object of your app
        self.preferences = Gtk.MenuItem("Preferences")
        self.preferences.connect("activate",window.on_mnu_preferences_activate)
        self.preferences.show()
        self.menu.append(self.preferences)

        self.quit = Gtk.MenuItem("Quit")
        self.quit.connect("activate",window.on_mnu_close_activate)
        self.quit.show()
        self.menu.append(self.quit)

        # Add more items here                           

        self.menu.show()
        self.indicator.set_menu(self.menu)

    def add_droplets(self):
        try:
            manager = digitalocean.Manager(client_id=os.environ["DO_CLIENT_ID"],
                                           api_key=os.environ["DO_API_KEY"])
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
            print("Error: " + e.message)
            if "Access Denied" in e.message:
                error_indicator = Gtk.ImageMenuItem.new_with_label(
                    "Error logging in. Please check your credentials.")
                img = Gtk.Image.new_from_icon_name("error", Gtk.IconSize.MENU)
                error_indicator.set_always_show_image(True)
                error_indicator.set_image(img)
                error_indicator.show()
                self.menu.append(error_indicator)

    
def new_application_indicator(window):
    ind = Indicator(window)
    return ind.indicator
