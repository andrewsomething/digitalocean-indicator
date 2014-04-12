# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from locale import gettext as _

from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('digitalocean_indicator')

from digitalocean_indicator_lib import Window
from digitalocean_indicator.AboutDigitaloceanIndicatorDialog import AboutDigitaloceanIndicatorDialog
from digitalocean_indicator.PreferencesDigitaloceanIndicatorDialog import PreferencesDigitaloceanIndicatorDialog

# See digitalocean_indicator_lib.Window.py for more details about how this class works
class DigitaloceanIndicatorWindow(Window):
    __gtype_name__ = "DigitaloceanIndicatorWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(DigitaloceanIndicatorWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutDigitaloceanIndicatorDialog
        self.PreferencesDialog = PreferencesDigitaloceanIndicatorDialog

        # Code for other initialization actions should be added here.

