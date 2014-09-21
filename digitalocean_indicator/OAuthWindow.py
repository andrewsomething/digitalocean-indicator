from gi.repository import Gtk, Gio
from gi.repository import WebKit
import urlparse

BASE_URL = 'https://cloud.digitalocean.com/v1/oauth/'
CLIENT_ID = 'de161c2041b50695f89a4f5bebfa638d0783eebf0d38309aa2ee892be4a30bf2'
CALLBACK_URL = 'http://andrewsomething.com'


class AuthWin(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "My Dialog", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

        oauth_url = "{0}/authorize?response_type=token&client_id={1}&redirect_uri={2}&scope=read%20write".format(
                    BASE_URL, CLIENT_ID, CALLBACK_URL)
        self.settings = Gio.Settings("com.andrewsomething.digitalocean-indicator")

        box = self.get_content_area()
        self.web = WebKit.WebView()
        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.add(self.web)
        box.pack_start(self.scrolled, True, True, 0)

        self.set_size_request(400, 575)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_title("Authorize")
        self.set_skip_taskbar_hint(True)
        self.set_resizable(False)
        self.set_default_size(400, 575)
        self.web.load_uri(oauth_url)
        self.show_all()
        self.web.connect('navigation-policy-decision-requested',
                         self.navigation_callback)

    def navigation_callback(self, view, frame, request, action, decision):
        url = request.get_uri()
        if "#access_token" in url:
            res = urlparse.parse_qs(url)
            token_type = res['token_type'][0]
            expires_in = res['expires_in'][0]
            access_token = res[CALLBACK_URL + '/#access_token'][0]
            self.settings.set_string("do-api-token", access_token)
            self.hide()