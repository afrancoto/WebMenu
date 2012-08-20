#WebMenu v.1.0
#Andrea Franco 19/08/2012
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import webbrowser

from gi.repository import Gio
from gi.repository import GObject
from gi.repository import PeasGtk
from gi.repository import Gtk
from gi.repository import RB

DCONF_DIR = 'org.gnome.rhythmbox.plugins.webmenu'
CURRENT_VERSION = '1.0'

class WMConfig(object):
    def __init__(self):
        self.settings = Gio.Settings(DCONF_DIR)

    def get_settings(self):
        return self.settings
     
class WMConfigDialog(GObject.Object, PeasGtk.Configurable):
    __gtype_name__ = 'WebMenuConfigDialog'
    object = GObject.property(type=GObject.Object)

    def __init__(self):
        GObject.Object.__init__(self)
        self.settings = Gio.Settings(DCONF_DIR)

    def do_create_configure_widget(self):
	global services
        dialog = Gtk.VBox()
    	
	vbox=Gtk.VBox(False, 15)
	hbox=Gtk.HBox()

	albumvbox = Gtk.VBox()
	albumlabel = Gtk.Label("<b>Album Submenu:</b>", use_markup=True) #Frome here: 'Album' vertical box    
	albumvbox.pack_start(albumlabel, False, False, 10)
        albumvbox.set_margin_left(15)
	albumvbox.set_margin_right(15)
        for service, data in services.items():
            check = Gtk.CheckButton(service)
            check.set_active(services[service][3])
            check.connect("toggled", self.website_toggled, service, 1)#The last argument, 1, stands for "Album"   
            albumvbox.pack_start(check, False, False, 0)
        
        hbox.pack_start(albumvbox, False, False, 0)

	artistlabel = Gtk.Label("<b>Artist Submenu:</b>", use_markup=True) #Frome here: 'Artist' vertical box      
	artistvbox = Gtk.VBox()
	artistvbox.pack_start(artistlabel, False, False, 10)
        artistvbox.set_margin_left(15)
	artistvbox.set_margin_right(15)
        for service, data in services.items():
            check = Gtk.CheckButton(service)
            check.set_active(services[service][4])
            check.connect("toggled", self.website_toggled, service, 2)#The last argument, 2, stands for "Artist"   
            albumvbox.pack_start(check, False, False, 0)
       
        hbox.pack_start(artistvbox, False, False, 0)
	vbox.pack_start(hbox, False, False, 0)

	ubutton = Gtk.Button("Look for updates (Current Version: "+CURRENT_VERSION+")") #crea il pulsante
	ubutton.connect("clicked", self.update_search)
	vbox.pack_start(ubutton, False, False, 0)

        dialog.pack_start(vbox, False, False, 0)
        dialog.show_all()
        
        return dialog
    
       
    def website_toggled(self, checkbutton, service, what):
	services[service][what+2]=checkbutton.get_active()

    def update_search(self, widget, data=None):
    	webbrowser.open("https://github.com/afrancoto/WebMenu/downloads")
