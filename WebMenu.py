#WebMenu v.2.2
#https://github.com/afrancoto/WebMenu

#Andrea Franco 27/08/2012
#Thanks to asermax (github.com)
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


from gi.repository import GObject, RB, Peas, Gtk
import webbrowser
import urllib2

from WebMenu_config import WMConfig
from WebMenu_config import WMConfigDialog

services = {}
services_order = []
other_settings = []
shortcuts = {}
refresh_count=0
web_menu_item = '''
  <ui>
    <menubar name="MenuBar">
      	<menu name="WebMenu" action="WebMenuAction">
        	<menuitem name="YTitem" action="search_on_youtube_action"/>
        	<menuitem name="LYitem" action="search_lyrics_action"/>
    		<menu name="AlbumMenu" action="album_menu_action">
       		 	%s
			<separator/>
			<menuitem name="AL_all" action="album_all"/>
    		</menu>
		<menu name="ArtistMenu" action="artist_menu_action">
       		 	%s
			<separator/>
			<menuitem name="AR_all" action="artist_all"/>
		</menu>
		<separator/>
		<menuitem name="Optionsitem" action="options_action"/>
      	</menu>
    </menubar>
  </ui>'''

web_context_part = '''
	<placeholder name="PluginPlaceholder">
		<separator/>
          	<menuitem name="YTitem" action="search_on_youtube_action_cx"/>
        	<menuitem name="LYitem" action="search_lyrics_action"/>
		<menu name="AlbumMenu" action="album_menu_action">
       		 	%s
			<separator/>
			<menuitem name="AL_all" action="album_all_cx"/>
		</menu>
		<menu name="ArtistMenu" action="artist_menu_action">
       		 	%s
			<separator/>
			<menuitem name="AR_all" action="artist_all_cx"/>
		</menu>
      	</placeholder>'''

web_context_item = '''<ui><popup name="QueuePlaylistViewPopup">''' + web_context_part + '''</popup>
    			  <popup name="BrowserSourceViewPopup">''' + web_context_part + '''</popup>
			  <popup name="PlaylistViewPopup">''' + web_context_part + '''</popup>
			  <popup name="PodcastViewPopup">''' + web_context_part + '''</popup></ui>'''


class WebMenuPlugin(GObject.Object, Peas.Activatable):
  __gtype_name__ = 'WebMenuPlugin'
  object = GObject.property(type=GObject.Object)

  def __init__(self):
    super(WebMenuPlugin, self).__init__()

##########
#The "draw_menu" function creates the 'Web' menu and associates every entry to its specific function
##########

  def draw_menu(self, shell):
    global action_group, action_group_submenus
    global ui_id, ui_manager
    global refresh_count

    menu_not_drawn=False #Usually the function is called by apply_settings, so the menu is already drawn

    try: ui_id
    except NameError: menu_not_drawn=True #If the ui_context_id does not exist, the menu is not yet drawn, so it is not deleted

    if not menu_not_drawn :
	ui_manager.remove_ui(ui_id) #Delete a previous drawn menu
	ui_manager.remove_action_group(action_group_submenus)
	del ui_id, action_group_submenus
	ui_manager.ensure_update()	

    #0. Web Menu
    action_group = Gtk.ActionGroup(name='WebMenuActionGroup')
    action_group_submenus= Gtk.ActionGroup(name='WebMenuSubmenusActionGroup_'+str(refresh_count))
    refresh_count+=1
    web_menu_action = Gtk.Action("WebMenuAction", _("Web"), None, None)
    action_group.add_action(web_menu_action)
    #0.1a Song on Youtube
    youtube_action = Gtk.Action ('search_on_youtube_action', _('Song on Youtube'), _('Look for the current playing song on Youtube'), "")
    youtube_action.connect ('activate', self.search_on_youtube, shell)
    action_group.add_action_with_accel (youtube_action, "<alt>Y")
    #0.1b Lyrics on Google
    lyrics_action = Gtk.Action ('search_lyrics_action', _('Look for lyrics'), _('Look for the current playing song\'s lyrics'), "")
    lyrics_action.connect ('activate', self.search_lyrics, shell)
    action_group.add_action_with_accel (lyrics_action, "<alt>L")

    #0.2 Album SubMenu-----------------------------------------------------------------------------------------------------------------------------
    album_menu_action = Gtk.Action("album_menu_action", _("Album"), None, None)
    action_group.add_action(album_menu_action)
    #0.2.X Album SubMenu Items
    ui_album=''
    for service in services_order:
	if services[service][1] is not '':  #If the album URL is empty does not display the option
 		#Add a new submenu item	
        	action_name = 'album_%s' % service
        	ui_album += '<menuitem name="AL_%s" action="%s"/>' % (service, action_name) #ui_album is the Album submenu
        	#Create the action
        	action = Gtk.Action( action_name, service, _('Look for the current album on %s' % service), '' )
        	action.connect( 'activate', self.unique_search_function, shell, 1, service)
		
		shortcut_exist=True #Checks if a shortcut exist	for a service	
		try: shortcuts[service]
		except: shortcut_exist=False

        	if (shortcut_exist) and (shortcuts[service][0] is not ''): #If the shortcut exist and we are in thr right submenu, it's added
			action_group_submenus.add_action_with_accel(action, shortcuts[service][0]) 
			print "Album shortcut: "+service+" -->"+shortcuts[service][0]
		else: action_group_submenus.add_action(action)

    #0.2.n Album -> Every Service
    album_all_action = Gtk.Action ('album_all', _('All'), _('Look for the current album on every service'), "")
    album_all_action.connect ('activate', self.search_on_all, shell, 1) #The last argument "1" stands for "Album"
    action_group.add_action(album_all_action)

    #0.3 Artist SubMenu-----------------------------------------------------------------------------------------------------------------------------
    artist_menu_action = Gtk.Action("artist_menu_action", _("Artist"), None, None)
    action_group.add_action(artist_menu_action)
    #0.3.X Artist SubMenu Items 
    ui_artist=''
    for service in services_order:
	if services[service][2] is not '':  #If the artist URL is empty does not display the option
 		#Add a new submenu item	
        	action_name = 'artist_%s' % service
        	ui_artist += '<menuitem name="AR_%s" action="%s"/>' % (service, action_name) #ui_artist is the Artist submenu
        	#Create the action
        	action = Gtk.Action( action_name, service, _('Look for the current artist on %s' % service), '' )
        	action.connect( 'activate', self.unique_search_function, shell, 2, service)
		
		shortcut_exist=True #Checks if a shortcut exist	for a service	
		try: shortcuts[service]
		except: shortcut_exist=False

        	if (shortcut_exist) and (shortcuts[service][1] is not ''): #If the shortcut exist and we are in thr right submenu, it's added
			action_group_submenus.add_action_with_accel(action, shortcuts[service][1])  
		else: action_group_submenus.add_action(action)

    #0.3.n Artist -> Every Service
    artist_all_action = Gtk.Action ('artist_all', _('All'), _('Look for the current artist on every service'), "")
    artist_all_action.connect ('activate', self.search_on_all, shell, 2) #The last argument "2" stands for "Artist"
    action_group.add_action(artist_all_action)

    #0.4 Options------------------------------------------------------------------------------------------------------------------------------------
    options_action = Gtk.Action ('options_action', _('Options'), _('WebMenu Options'), "")
    options_action.connect ('activate', self.open_options, shell)
    action_group.add_action (options_action)

    ui_manager.insert_action_group(action_group) #Adds the action groups
    ui_manager.insert_action_group(action_group_submenus)
    ui_manager.ensure_update()

    ui = web_menu_item % (ui_album, ui_artist) #Adds ui_album and ui_artist to the webmenu
    ui_id = ui_manager.add_ui_from_string(ui)
    ui_manager.ensure_update()
##########
#The "draw_context_menu" function creates the entries in the context menu and associates them to their specific function.
##########
  def draw_context_menu(self, shell):
    global context_action_group
    global ui_context_id

    menu_not_drawn=False #Usually the function is called by apply_settings, so the menu is already drawn

    try: ui_context_id
    except NameError: menu_not_drawn=True #If the ui_context_id does not exist, the menu is not yet drawn, so it is not deleted

    if not menu_not_drawn :  
	ui_manager.remove_ui(ui_context_id) #Delete a previous drawn menu
	del ui_context_id
	ui_manager.ensure_update()

    #0. Web Context Menu
    context_action_group = Gtk.ActionGroup(name='WebMenuContextActionGroup')
    #0.1a Song on Youtube
    youtube_action = Gtk.Action ('search_on_youtube_action_cx', _('Song on Youtube'), _('Look for the selected song on Youtube'), "")
    youtube_action.connect ('activate', self.search_on_youtube, shell, True) #"True" says that the command is launched from the context menu
    context_action_group.add_action_with_accel (youtube_action, "<alt>Y")
    #0.1b Lyrics
    lyrics_action = Gtk.Action ('search_lyrics_action_cx', _('Look for lyrics'), _('Look for the selected song\'s Lyrics'), "")
    lyrics_action.connect ('activate', self.search_lyrics, shell, True) #"True" says that the command is launched from the context menu
    context_action_group.add_action_with_accel (lyrics_action, "<alt>L")
    #0.2.X Album SubMenu
    ui_album=''
    for service in services_order:
	if services[service][1] is not '':  #If the album URL is empty does not display the option
 		#Add a new submenu item	
        	action_name = 'album_%s_cx' % service
        	ui_album += '<menuitem name="AL_%s" action="%s"/>' % (service, action_name) #ui_album is the Album submenu
	        #Create the action
       		action = Gtk.Action( action_name, service, _('Look for the selected album on %s' % service), '' )
        	action.connect( 'activate', self.unique_search_function, shell, 1, service, True )
        	context_action_group.add_action( action )
    #0.2.n Album -> Every Service
    album_all_action = Gtk.Action ('album_all_cx', _('All'), _('Look for the current album on every service'), "")
    album_all_action.connect ('activate', self.search_on_all, shell, 1, True) #The last argument "1" stands for "Album"
    context_action_group.add_action(album_all_action)

    #0.3.X Artist SubMenu
    ui_artist=''
    for service in services_order:
	if services[service][2] is not '':  #If the artist URL is empty does not display the option
 		#Add a new submenu item	
        	action_name = 'artist_%s_cx' % service
        	ui_artist += '<menuitem name="AR_%s" action="%s"/>' % (service, action_name) #ui_artist is the Artist submenu
        	#Create the action
       		action = Gtk.Action( action_name, service, _('Look for the selected artist on %s' % service), '' )
        	action.connect( 'activate', self.unique_search_function, shell, 2, service, True )
       		context_action_group.add_action( action )
    #0.3.n Artist -> Every Service
    artist_all_action = Gtk.Action ('artist_all_cx', _('All'), _('Look for the current artist on every service'), "")
    artist_all_action.connect ('activate', self.search_on_all, shell, 2, True) #The last argument "2" stands for "Artist"
    context_action_group.add_action(artist_all_action)

    ui = web_context_item % ((ui_album, ui_artist)*4) #Adds ui_album and ui_artist to the web context menu
    ui_manager.insert_action_group(context_action_group)
    ui_context_id = ui_manager.add_ui_from_string(ui)
    ui_manager.ensure_update()

##########
#The "apply_settings" function is called when Rhythmbox is loaded and whenever the settings are changed
##########
  def apply_settings(self, settings, key, shell, config):
    global services, services_order, other_settings, shortcuts

    #The global variables are updated if changed
    if (key is not 'all') and (key is not 'firsttime'): 
	services = self.settings['services']
	services_order = self.settings['services-order']
    	other_settings = self.settings['other-settings']
    	shortcuts = self.settings['shortcuts']

    config.check_services_order() #Checks settings integrity
    
    self.draw_menu(shell)#Redraws the menus
    self.draw_context_menu(shell)

    paths=["/MenuBar/WebMenu", "/QueuePlaylistViewPopup/PluginPlaceholder", "/BrowserSourceViewPopup/PluginPlaceholder", "/PlaylistViewPopup/PluginPlaceholder", "/PodcastViewPopup/PluginPlaceholder"] #Settings must be applied to the Web Menu and to every context menu
    for path in paths:
	for service, data in services.items():
		menu_option=path+"/AlbumMenu/AL_"+service  #Hides the non-active options in the "Album" submenu
		menu_option_widget=ui_manager.get_widget(menu_option)
		if (services[service][1] is not ''):# and (menu_option_widget is not None):
			if services[service][3]: shell.props.ui_manager.get_widget(menu_option).show()
			else: ui_manager.get_widget(menu_option).hide()

		menu_option=path+"/ArtistMenu/AR_"+service  #Hides the non-active options in the "Artist" submenu
		if (services[service][2] is not ''):# and (menu_option_widget is not None):
			if services[service][4]:  shell.props.ui_manager.get_widget(menu_option).show()
			else: ui_manager.get_widget(menu_option).hide()


	menu_option=path+"/AlbumMenu/AL_all"  #Hides/shows the 'All' option in the "Album" submenu	
	if other_settings[1]: ui_manager.get_widget(menu_option).show()
	else: ui_manager.get_widget(menu_option).hide()

	menu_option=path+"/ArtistMenu/AR_all"  #Hides/shows the 'All' option in the "Artist" submenu	
	if other_settings[2]: ui_manager.get_widget(menu_option).show()
	else: ui_manager.get_widget(menu_option).hide()

    if other_settings[0]: ui_manager.get_widget("/MenuBar/WebMenu/Optionsitem").show()
    else: ui_manager.get_widget("/MenuBar/WebMenu/Optionsitem").hide()

    if other_settings[3]: ui_manager.get_widget("/MenuBar/WebMenu/LYitem").show()
    else: ui_manager.get_widget("/MenuBar/WebMenu/LYitem").hide()

    ui_manager.ensure_update()
    
    self.song_changed('start', '', shell.props)#deactivate menus if needed

##########
#The "do_activate" function is called when Rhythmbox is loaded
##########
  def do_activate(self):

    #Services data are stored in a dict like this:
    #     STRING            0:STRING          1:STRING          2:STRING               3:BOOLEAN                  4:BOOLEAN
    # 'service_name' : ('song_engine_url','album_engine_url','artist_engine_url', enabled_in_album_submenu, enabled_in_artist_submenu)

    global services, services_order, other_settings, shortcuts
    global ui_manager

    shell = self.object
    ui_manager = shell.props.ui_manager
    config = WMConfig()

    config.check_services_order() #Checks settings integrity

    self.settings = config.get_settings()
    services = self.settings['services'] #'services' is a global variable with all the settings in it
    services_order = self.settings['services-order'] #'services-order' is a global variable that keeps the right order for the menu items
    other_settings = self.settings['other-settings'] #'other-settings' is an array of booleans: ['Options' item, 'All' item in album menu, 'All' item in artist menu, 'Look for Lyrics' item]
    shortcuts = self.settings['shortcuts'] #'shortcuts' is a global variables with album and artist shortcuts

    self.draw_menu(shell) #Calls "draw_menu"
    self.draw_context_menu(shell) #Calls "draw_context_menu"

    self.apply_settings('oldsettings', 'all' , shell, config) #Calls "apply_settings"
    self.settings.connect('changed', self.apply_settings, shell, config) #Connects a change in the settings menus to "apply_settings"

    sp=shell.props.shell_player #Connects play/stop events to "song_changed")
    sp.connect ('playing-changed', self.song_changed, shell.props)
    self.song_changed('start', '', shell.props)

##########
#The "do_deactivate" function removes the 'Web' Menu and the context menu
##########
  def do_deactivate(self):
    global ui_id, ui_context_id
    global action_group, action_group_submenus, context_action_group

    shell = self.object
    ui_manager.remove_ui(ui_id)
    ui_manager.remove_action_group(action_group)
    ui_manager.remove_action_group(action_group_submenus)
    del ui_id, action_group, action_group_submenus
    ui_manager.remove_ui(ui_context_id)
    ui_manager.remove_action_group(context_action_group)
    del ui_context_id, context_action_group

##########
#The "get_metadata" function gets and returns, in order, TITLE, ALBUM and ARTIST of the current playing song as elements of an array (0,1,2)
##########
  def get_metadata(self, shell, context=False):
    if context: #If the command is sent from the context menu, it returns the selected track, album, artist
	page = shell.props.selected_page
	if not hasattr(page, "get_entry_view"): return
	selected = page.get_entry_view().get_selected_entries()
	if selected != []:
		playing_title = selected[0].get_string(RB.RhythmDBPropType.TITLE)
		playing_album = selected[0].get_string(RB.RhythmDBPropType.ALBUM)
		playing_artist = selected[0].get_string(RB.RhythmDBPropType.ARTIST)	   
    else:  #If the command is sent from the menubar, it returns the playing track, album, artist
	self.playing_entry = shell.props.shell_player.get_playing_entry()
	playing_title = self.playing_entry.get_string(RB.RhythmDBPropType.TITLE)
	playing_album = self.playing_entry.get_string(RB.RhythmDBPropType.ALBUM)
	playing_artist = self.playing_entry.get_string(RB.RhythmDBPropType.ARTIST)

    result=[playing_title, playing_album, playing_artist]
    return result

##########
#The "search_on_youtube" function search TITLE + ARTIST on youtube
##########
  def search_on_youtube(self, event, shell, context=False):
    metadata=self.get_metadata(shell, context) #Calls "get_metadata"
    final_url="http://www.youtube.com/results?search_query=\"" + urllib2.quote(metadata[0]) + "\"+\"" + urllib2.quote(metadata[2]) + "\""
    webbrowser.open(final_url)

##########
#The "search_lyrics" function search lyrics + TITLE + ARTIST on Google
##########
  def search_lyrics(self, event, shell, context=False):
    metadata=self.get_metadata(shell, context) #Calls "get_metadata"
    final_url="https://www.google.com/webhp?q=search#hl=en&q=\"lyrics\"+\"" + urllib2.quote(metadata[0]) + "\"+\"" + urllib2.quote(metadata[2]) + "\""
    webbrowser.open(final_url)

##########
#The "unique_search_function" is the one which is called by the menu/context menu actions
##########
  def unique_search_function(self, event, shell, what, service, context=False):
    metadata=self.get_metadata(shell, context) #Calls "get_metadata"
    base_url = services[service][what] #Gets the URL with keywords
    final_url=self.replace_keywords(base_url, metadata) #Replace keywords
    webbrowser.open(final_url)

##########
#The "replace_keywords" function simply replace the keywords with the metadata
##########
  def replace_keywords(self, URL, metadata):
    URL=URL.replace('[ALBUM]', urllib2.quote(metadata[1]))
    URL=URL.replace('[ARTIST]', urllib2.quote(metadata[2]))
    return URL

##########
#The "search_on_all" function search the artist OR the album on every service which is activ; "what" argument: 0=title (not used), 1=album, 2=artist
##########
  def search_on_all(self, event, shell, what, context=False):
    for service in services_order: 
	if services[service][what+2] and (services[service][what] is not ''): 
		self.unique_search_function('searchonall', shell, what, service, context)

##########
#The "open_options" function opens teh configuration window
##########
  def open_options(self, event, shell):
	config_dialog = WMConfigDialog()
	WMConfigDialog.manager_window_called_from_options(config_dialog, None)

##########
#The "song_changed" function controls if no song is playing. If it is so, the 'Web' menu options are disabled.
##########
  def song_changed(self, playing, user_data, s_props):
    self.playing_entry = s_props.shell_player.get_playing_entry() 
    now_is_playing=self.playing_entry is not None #current playing song==None --> False

    ui_manager.get_widget("/MenuBar/WebMenu/YTitem").set_sensitive(now_is_playing)  #Disable the YouTube item
    ui_manager.get_widget("/MenuBar/WebMenu/LYitem").set_sensitive(now_is_playing)  #Disable the YouTube item
    for service, data in services.items():
	if services[service][1] is not '':
		menu_option="/MenuBar/WebMenu/AlbumMenu/AL_"+service  #Disable all the options in the "Album" submenu
		ui_manager.get_widget(menu_option).set_sensitive(now_is_playing)
	if services[service][2] is not '':
		menu_option="/MenuBar/WebMenu/ArtistMenu/AR_"+service #Disable all the options in the "Artist" submenu
		ui_manager.get_widget(menu_option).set_sensitive(now_is_playing)
    ui_manager.get_widget("/MenuBar/WebMenu/AlbumMenu/AL_all").set_sensitive(now_is_playing)  #Disable the Album/All item
    ui_manager.get_widget("/MenuBar/WebMenu/ArtistMenu/AR_all").set_sensitive(now_is_playing)  #Disable the Artist/All item
