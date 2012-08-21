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
#from WebMenu import WebMenuPlugin

from gi.repository import Gio
from gi.repository import GObject
from gi.repository import PeasGtk
from gi.repository import Gtk
#from gi.repository import RB

DCONF_DIR = 'org.gnome.rhythmbox.plugins.webmenu'
CURRENT_VERSION = '1.0'

class WMConfig(object):
    def __init__(self):
	global services, services_order
        self.settings = Gio.Settings(DCONF_DIR)
	services = self.settings['services'] #'services' is a global variable with all the settings in it
	services_order=self.settings['services-order']

    def get_settings(self):
        return self.settings

    def check_services_order(self):
	changed=False #The services order is rewritten only if it is changed by this function
	for service, data in services.items():
		if service not in services_order: 
			services_order.append(service) #If a service is missing from the "service-order" key, it is added at the end
			changed=True
	for service in services_order:
		if service not in services: 
			services_order.remove(service) #If a service is missing from the "services" key, it is also deleted from the "service-order" key
			changed=True
	if changed: self.settings['services-order']=services_order
         
class WMConfigDialog(GObject.Object, PeasGtk.Configurable):
    __gtype_name__ = 'WebMenuConfigDialog'
    object = GObject.property(type=GObject.Object)

    def __init__(self):
        GObject.Object.__init__(self)
        self.settings = Gio.Settings(DCONF_DIR)

    def do_create_configure_widget(self):
        dialog = Gtk.VBox()
    	
	vbox=Gtk.VBox(False, 0)
	vbox.set_margin_left(15)
	vbox.set_margin_right(15)
	hbox=Gtk.HBox()

	albumvbox = Gtk.VBox()
	albumlabel = Gtk.Label("<b>Album Submenu:</b>", use_markup=True) #Frome here: 'Album' vertical box    
	albumvbox.pack_start(albumlabel, False, False, 5)
	albumvbox.set_margin_right(15)
        for service in services_order:
	    if services[service][1] is not '': #If the album URL is empty does not display the option
		    check = Gtk.CheckButton(service)
		    check.set_active(services[service][3])
		    check.connect("toggled", self.website_toggled, service, 1)#The last argument, 1, stands for "Album"   
		    albumvbox.pack_start(check, False, False, 0)
	
	albumhseparator = Gtk.HSeparator()
	albumvbox.pack_start(albumhseparator, False, False, 0)
	check = Gtk.CheckButton("All") #The 'All'-album checkbox
        check.set_active(self.settings['other-settings'][1])
	check.connect("toggled", self.other_settings_toggled, 1) #The last argument, 1, stands for "Album"   
	albumvbox.pack_start(check, False, False, 0)
	
        hbox.pack_start(albumvbox, False, False, 0)

	artistlabel = Gtk.Label("<b>Artist Submenu:</b>", use_markup=True) #Frome here: 'Artist' vertical box      
	artistvbox = Gtk.VBox()
	artistvbox.pack_start(artistlabel, False, False, 5)
        artistvbox.set_margin_left(15)
        for service in services_order:
	    if services[service][2] is not '': #If the artist URL is empty does not display the option
		    check = Gtk.CheckButton(service)
		    check.set_active(services[service][4])
	 	    check.connect("toggled", self.website_toggled, service, 2) #The last argument, 2, stands for "Artist"  
		    artistvbox.pack_start(check, False, False, 0)

	artisthseparator = Gtk.HSeparator()
	artistvbox.pack_start(artisthseparator, False, False, 0)
	check = Gtk.CheckButton("All") #The 'All'-artist checkbox
        check.set_active(self.settings['other-settings'][2])
	check.connect("toggled", self.other_settings_toggled, 2) #The last argument, 2, stands for "Album"   
	artistvbox.pack_start(check, False, False, 0)
       
        hbox.pack_start(artistvbox, False, False, 0)
	vbox.pack_start(hbox, False, False, 0)

	check = Gtk.CheckButton("Show the 'Options' item in the Web Menu") #The 'Options' checkbox
        check.set_active(self.settings['other-settings'][0])
	check.connect("toggled", self.other_settings_toggled, 0) #The last argument, 2, stands for the "Options" item
	vbox.pack_start(check, False, False, 10)

	new_button = Gtk.Button("Add a service") #crea il pulsante
	new_button.connect("clicked", self.new_service_window)
	vbox.pack_start(new_button, False, False, 0)

	update_button = Gtk.Button("Look for updates (Current Version: "+CURRENT_VERSION+")") #crea il pulsante
	update_button.connect("clicked", self.update_search)
	vbox.pack_start(update_button, False, False, 0)

        dialog.pack_start(vbox, False, False, 0)
        dialog.show_all()
        
        return dialog
     
    def website_toggled(self, checkbutton, service, what):
	data = list(services[service])
	data[what+2] = checkbutton.get_active()
	services[service]= tuple(data)
	#after asigning the new data, you should persist the services
	self.settings['services'] = services

    def other_settings_toggled(self, checkbutton, what):
	options_list=self.settings['other-settings']
	options_list[what] = checkbutton.get_active()
	self.settings['other-settings']=options_list

    def update_search(self, widget, data=None):
    	webbrowser.open("https://github.com/afrancoto/WebMenu/downloads")

    def new_service_window(self, widget, data=None):
	self.window = Gtk.Window()

	vbox=Gtk.VBox(False, 0)
	vbox.set_margin_left(15)
	vbox.set_margin_right(15)
	main_label = Gtk.Label("<b>Add a new service:</b>", use_markup=True) #Main label 
	vbox.pack_start(main_label, False, False, 10)
	description_label = Gtk.Label("Make a search on the website you want to add, copy here the URL and replace your query\n"
				      "with the keywords: <b>[ALBUM]</b> and/or <b>[ARTIST]</b>\n"
				      "<i>(If you want the service to show up in only one menu, simply leave the other URL empty.)</i>", use_markup=True) #Description label  
	vbox.pack_start(description_label, False, False, 10)	

	hbox=Gtk.HBox(False, 5)
	
	vbox_labels=Gtk.VBox(False, 7)
 	name_label = Gtk.Label("<b>Service Name:</b>", use_markup=True)
	vbox_labels.pack_start(name_label, True, True, 0)

 	album_url_label = Gtk.Label("<b>Album URL:</b>", use_markup=True)
	vbox_labels.pack_start(album_url_label, True, True, 0)

 	artist_url_label = Gtk.Label("<b>Artist URL</b>", use_markup=True)
	vbox_labels.pack_start(artist_url_label, True, True, 0)
	hbox.pack_start(vbox_labels, False, False, 0)	

	vbox_entries=Gtk.VBox(False, 7)
 	name_entry = Gtk.Entry()
	name_entry.set_width_chars(52)
	name_entry.set_max_length(30)
	name_entry.set_text('')
	vbox_entries.pack_start(name_entry, True, True, 0)

 	album_url_entry = Gtk.Entry()
	album_url_entry.set_max_length(300)
	album_url_entry.set_text('')
	vbox_entries.pack_start(album_url_entry, True, True, 0)

 	artist_url_entry = Gtk.Entry()
	artist_url_entry.set_max_length(300)
	artist_url_entry.set_text('')
	vbox_entries.pack_start(artist_url_entry, True, True, 0)
	hbox.pack_start(vbox_entries, False, False, 0)	
	vbox.pack_start(hbox, False, False, 10)

	create_button = Gtk.Button("Add the service") #crea il pulsante
	create_button.connect("clicked", self.new_service_add, name_entry, 
	                                                       album_url_entry, 
	                                                       artist_url_entry)
	vbox.pack_start(create_button, False, False, 10)

        self.window.add(vbox)
	self.window.show_all()
	return

    def new_service_add(self, widget, name, album, artist):
        #TODO: dinamically add the items on the menu and context AND the checkboxs
        #on the active configuration dialog
        service=name.get_text()
	if service is not '':
        	services[service] = ('', album.get_text(), artist.get_text(), True, True) #Gets the new service
		services_order.append(service)
	
	        self.settings['services'] = services #Writes the new service in dconf
        	self.settings['services-order']=services_order

        self.window.destroy()
