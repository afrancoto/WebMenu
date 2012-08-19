#WebMenu v.0.9
#Andrea Franco 18/08/2012
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


#To add a new service:
#0. Decide a position for the service in the menu and keep it for every next step
#1. Add the "web_menu_item" and the "web_context_menu" entries: the menu name must be AL_servicename/AR_servicename, the action album_servicename/artist_servicename and album_servicename_cx/artist_servicename_cx
#2. Add actions (album and/or artist) in "draw_menu" and "draw_context_menu" (update position numbers!)
#3. Add service name (lowercase) to "org.gnome.rhythmbox.plugins.webmenu.gschema.xml" in "default-*-services" <default> and in "active-*-services" <description>  (order is important)
#4. Add an entry in "ALBUM_LABELS" and "ARTIST_LABELS" in WebMenu_config.py (order is important)
#4. Add the search_on_service function
#5. Add the entry in "search_on_all" function
#6. Launch Rhythmbox, enable the service in WebMenu preferences and test it from both the menubar and the context menu
#7. Add the service name in WebMenu.plugin and README.md

from gi.repository import GObject, RB, Peas, Gtk
import os
import urllib2

from WebMenu_config import WMConfig
from WebMenu_config import WMConfigDialog

web_menu_item = '''
  <ui>
    <menubar name="MenuBar">
      	<menu name="WebMenu" action="WebMenuAction">
        	<menuitem name="YTitem" action="search_on_youtube_action"/>
		<menu name="AlbumMenu" action="album_menu_action">
			<menuitem name="AL_wikipedia" action="album_wikipedia"/>
			<menuitem name="AL_allmusic" action="album_allmusic"/>
			<menuitem name="AL_rateyourmusic" action="album_rateyourmusic"/>
			<menuitem name="AL_allaboutjazz" action="album_allaboutjazz"/>
			<menuitem name="AL_discogs" action="album_discogs"/>
			<menuitem name="AL_facebook" action="album_facebook"/>
			<menuitem name="AL_lastfm" action="album_lastfm"/>
			<separator/>
			<menuitem name="AL_all" action="album_all"/>
			<separator/>
		</menu>
		<menu name="ArtistMenu" action="artist_menu_action">
			<menuitem name="AR_wikipedia" action="artist_wikipedia"/>
			<menuitem name="AR_allmusic" action="artist_allmusic"/>
			<menuitem name="AR_rateyourmusic" action="artist_rateyourmusic"/>
			<menuitem name="AR_discogs" action="artist_discogs"/>
			<menuitem name="AR_official" action="artist_official"/>
			<menuitem name="AR_facebook" action="artist_facebook"/>
			<menuitem name="AR_lastfm" action="artist_lastfm"/>
			<menuitem name="AR_myspace" action="artist_myspace"/>
			<menuitem name="AR_torrentz" action="artist_torrentz"/>
			<separator/>
			<menuitem name="AR_all" action="artist_all"/>
		</menu>
      	</menu>
    </menubar>
  </ui>
'''

web_context_item = '''
  <ui>
    <popup name="QueuePlaylistViewPopup">
	<placeholder name="PluginPlaceholder">
        	<menuitem name="YTitem" action="search_on_youtube_action_cx"/>
		<menu name="AlbumMenu" action="album_menu_action">
			<menuitem name="AL_wikipedia" action="album_wikipedia_cx"/>
			<menuitem name="AL_allmusic" action="album_allmusic_cx"/>
			<menuitem name="AL_rateyourmusic" action="album_rateyourmusic_cx"/>
			<menuitem name="AL_allaboutjazz" action="album_allaboutjazz_cx"/>
			<menuitem name="AL_discogs" action="album_discogs_cx"/>
			<menuitem name="AL_facebook" action="album_facebook_cx"/>
			<menuitem name="AL_lastfm" action="album_lastfm_cx"/>
			<separator/>
			<menuitem name="AL_all" action="album_all_cx"/>
			<separator/>
		</menu>
		<menu name="ArtistMenu" action="artist_menu_action">
			<menuitem name="AR_wikipedia" action="artist_wikipedia_cx"/>
			<menuitem name="AR_allmusic" action="artist_allmusic_cx"/>
			<menuitem name="AR_rateyourmusic" action="artist_rateyourmusic_cx"/>
			<menuitem name="AR_discogs" action="artist_discogs_cx"/>
			<menuitem name="AR_official" action="artist_official_cx"/>
			<menuitem name="AR_facebook" action="artist_facebook_cx"/>
			<menuitem name="AR_lastfm" action="artist_lastfm_cx"/>
			<menuitem name="AR_myspace" action="artist_myspace_cx"/>
			<menuitem name="AR_torrentz" action="artist_torrentz_cx"/>
			<separator/>
			<menuitem name="AR_all" action="artist_all_cx"/>
		</menu>
      	</placeholder>
    </popup>
    
    <popup name="BrowserSourceViewPopup">
	<placeholder name="PluginPlaceholder">
        	<menuitem name="YTitem" action="search_on_youtube_action_cx"/>
		<menu name="AlbumMenu" action="album_menu_action">
			<menuitem name="AL_wikipedia" action="album_wikipedia_cx"/>
			<menuitem name="AL_allmusic" action="album_allmusic_cx"/>
			<menuitem name="AL_rateyourmusic" action="album_rateyourmusic_cx"/>
			<menuitem name="AL_allaboutjazz" action="album_allaboutjazz_cx"/>
			<menuitem name="AL_discogs" action="album_discogs_cx"/>
			<menuitem name="AL_facebook" action="album_facebook_cx"/>
			<menuitem name="AL_lastfm" action="album_lastfm_cx"/>
			<separator/>
			<menuitem name="AL_all" action="album_all_cx"/>
			<separator/>
		</menu>
		<menu name="ArtistMenu" action="artist_menu_action">
			<menuitem name="AR_wikipedia" action="artist_wikipedia_cx"/>
			<menuitem name="AR_allmusic" action="artist_allmusic_cx"/>
			<menuitem name="AR_rateyourmusic" action="artist_rateyourmusic_cx"/>
			<menuitem name="AR_discogs" action="artist_discogs_cx"/>
			<menuitem name="AR_official" action="artist_official_cx"/>
			<menuitem name="AR_facebook" action="artist_facebook_cx"/>
			<menuitem name="AR_lastfm" action="artist_lastfm_cx"/>
			<menuitem name="AR_myspace" action="artist_myspace_cx"/>
			<menuitem name="AR_torrentz" action="artist_torrentz_cx"/>
			<separator/>
			<menuitem name="AR_all" action="artist_all_cx"/>
		</menu>
      	</placeholder>
    </popup>

    <popup name="PlaylistViewPopup">
	<placeholder name="PluginPlaceholder">
        	<menuitem name="YTitem" action="search_on_youtube_action_cx"/>
		<menu name="AlbumMenu" action="album_menu_action">
			<menuitem name="AL_wikipedia" action="album_wikipedia_cx"/>
			<menuitem name="AL_allmusic" action="album_allmusic_cx"/>
			<menuitem name="AL_rateyourmusic" action="album_rateyourmusic_cx"/>
			<menuitem name="AL_allaboutjazz" action="album_allaboutjazz_cx"/>
			<menuitem name="AL_discogs" action="album_discogs_cx"/>
			<menuitem name="AL_facebook" action="album_facebook_cx"/>
			<menuitem name="AL_lastfm" action="album_lastfm_cx"/>
			<separator/>
			<menuitem name="AL_all" action="album_all_cx"/>
			<separator/>
		</menu>
		<menu name="ArtistMenu" action="artist_menu_action">
			<menuitem name="AR_wikipedia" action="artist_wikipedia_cx"/>
			<menuitem name="AR_allmusic" action="artist_allmusic_cx"/>
			<menuitem name="AR_rateyourmusic" action="artist_rateyourmusic_cx"/>
			<menuitem name="AR_discogs" action="artist_discogs_cx"/>
			<menuitem name="AR_official" action="artist_official_cx"/>
			<menuitem name="AR_facebook" action="artist_facebook_cx"/>
			<menuitem name="AR_lastfm" action="artist_lastfm_cx"/>
			<menuitem name="AR_myspace" action="artist_myspace_cx"/>
			<menuitem name="AR_torrentz" action="artist_torrentz_cx"/>
			<separator/>
			<menuitem name="AR_all" action="artist_all_cx"/>
		</menu>
      	</placeholder>
    </popup>

    <popup name="PodcastViewPopup">
	<placeholder name="PluginPlaceholder">
        	<menuitem name="YTitem" action="search_on_youtube_action_cx"/>
		<menu name="AlbumMenu" action="album_menu_action">
			<menuitem name="AL_wikipedia" action="album_wikipedia_cx"/>
			<menuitem name="AL_allmusic" action="album_allmusic_cx"/>
			<menuitem name="AL_rateyourmusic" action="album_rateyourmusic_cx"/>
			<menuitem name="AL_allaboutjazz" action="album_allaboutjazz_cx"/>
			<menuitem name="AL_discogs" action="album_discogs_cx"/>
			<menuitem name="AL_facebook" action="album_facebook_cx"/>
			<menuitem name="AL_lastfm" action="album_lastfm_cx"/>
			<separator/>
			<menuitem name="AL_all" action="album_all_cx"/>
			<separator/>
		</menu>
		<menu name="ArtistMenu" action="artist_menu_action">
			<menuitem name="AR_wikipedia" action="artist_wikipedia_cx"/>
			<menuitem name="AR_allmusic" action="artist_allmusic_cx"/>
			<menuitem name="AR_rateyourmusic" action="artist_rateyourmusic_cx"/>
			<menuitem name="AR_discogs" action="artist_discogs_cx"/>
			<menuitem name="AR_official" action="artist_official_cx"/>
			<menuitem name="AR_facebook" action="artist_facebook_cx"/>
			<menuitem name="AR_lastfm" action="artist_lastfm_cx"/>
			<menuitem name="AR_myspace" action="artist_myspace_cx"/>
			<menuitem name="AR_torrentz" action="artist_torrentz_cx"/>
			<separator/>
			<menuitem name="AR_all" action="artist_all_cx"/>
		</menu>
      	</placeholder>
    </popup>
  </ui>
'''

class WebMenuPlugin(GObject.Object, Peas.Activatable):
  __gtype_name__ = 'WebMenuPlugin'
  object = GObject.property(type=GObject.Object)

  def __init__(self):
    super(WebMenuPlugin, self).__init__()

##########
#The "draw_menu" function creates the 'Web' menu and associates every entry to its specific function
#0.
#  1
#  2.
#    1
#    ...
#    8
#  3.
#    1
#    ...
#    10
##########

  def draw_menu(self, shell, settings): 
    #0. Web Menu
    action_group = Gtk.ActionGroup(name='WebMenuActionGroup')
    web_menu_action = Gtk.Action("WebMenuAction", _("Web"), None, None)
    action_group.add_action(web_menu_action)
    #0.1 Song on Youtube
    youtube_action = Gtk.Action ('search_on_youtube_action', _('Song on Youtube'), _('Look for the current playing song on Youtube'), "")
    youtube_action.connect ('activate', self.search_on_youtube, shell)
    action_group.add_action_with_accel (youtube_action, "<alt>Y")
    #0.2 Album Menu
    album_menu_action = Gtk.Action("album_menu_action", _("Album"), None, None)
    action_group.add_action(album_menu_action)
    #0.2.1 Album -> Wikipedia
    album_wikipedia_action = Gtk.Action ('album_wikipedia', _('Wikipedia'), _('Look for the current album on Wikipedia'), "")
    album_wikipedia_action.connect ('activate', self.search_on_wikipedia, shell, 1)  #The last argument "1" stands for "Album"
    action_group.add_action_with_accel (album_wikipedia_action, "<alt>W")
    #0.2.2 Album -> AllMusic
    album_allmusic_action = Gtk.Action ('album_allmusic', _('AllMusic'), _('Look for the current album on AllMusic'), "")
    album_allmusic_action.connect ('activate', self.search_on_allmusic, shell, 1) #The last argument "1" stands for "Album"
    action_group.add_action(album_allmusic_action)
    #0.2.3 Album -> RateYourMusic
    album_rateyourmusic_action = Gtk.Action ('album_rateyourmusic', _('RateYourMusic'), _('Look for the current album on RateYourMusic'), "")
    album_rateyourmusic_action.connect ('activate', self.search_on_rateyourmusic, shell, 1) #The last argument "1" stands for "Album"
    action_group.add_action(album_rateyourmusic_action)
    #0.2.4 Album -> AllAboutJazz
    album_allaboutjazz_action = Gtk.Action ('album_allaboutjazz', _('AllAboutJazz'), _('Look for the current album on AllAboutJazz'), "")
    album_allaboutjazz_action.connect ('activate', self.search_on_allaboutjazz, shell, 1) #The last argument "1" stands for "Album"
    action_group.add_action(album_allaboutjazz_action)
    #0.2.5 Album -> DiscoGS
    album_discogs_action = Gtk.Action ('album_discogs', _('DiscoGS'), _('Look for the current album on DiscoGS'), "")
    album_discogs_action.connect ('activate', self.search_on_discogs, shell, 1) #The last argument "1" stands for "Album"
    action_group.add_action(album_discogs_action)
    #0.2.6 Album -> Lastfm
    album_lastfm_action = Gtk.Action ('album_lastfm', _('Last.fm'), _('Look for the current album on Last.fm'), "")
    album_lastfm_action.connect ('activate', self.search_on_lastfm, shell, 1) #The last argument "1" stands for "Album"
    action_group.add_action(album_lastfm_action)
    #0.2.7 Album -> Facebook
    album_facebook_action = Gtk.Action ('album_facebook', _('Facebook'), _('Look for the current album on Facebook'), "")
    album_facebook_action.connect ('activate', self.search_on_facebook, shell, 1) #The last argument "1" stands for "Album"
    action_group.add_action(album_facebook_action)
    #0.2.8 Album -> Every Service
    album_all_action = Gtk.Action ('album_all', _('All'), _('Look for the current album on every service'), "")
    album_all_action.connect ('activate', self.search_on_all, shell, settings, 1) #The last argument "1" stands for "Album"
    action_group.add_action(album_all_action)
    #0.3 Artist Menu
    artist_menu_action = Gtk.Action("artist_menu_action", _("Artist"), None, None)
    action_group.add_action(artist_menu_action)
    #0.3.1 Artist -> Wikipedia
    artist_wikipedia_action = Gtk.Action ('artist_wikipedia', _('Wikipedia'), _('Look for the current artist on Wikipedia'), "")
    artist_wikipedia_action.connect ('activate', self.search_on_wikipedia, shell, 2)  #The last argument "2" stands for "Artist"
    action_group.add_action(artist_wikipedia_action)
    #0.3.2 Artist -> AllMusic
    artist_allmusic_action = Gtk.Action ('artist_allmusic', _('AllMusic'), _('Look for the current artist on AllMusic'), "")
    artist_allmusic_action.connect ('activate', self.search_on_allmusic, shell, 2) #The last argument "2" stands for "Artist"
    action_group.add_action_with_accel (artist_allmusic_action, "<alt>A")
    #0.3.3 Artist -> RateYourMusic
    artsit_rateyourmusic_action = Gtk.Action ('artist_rateyourmusic', _('RateYourMusic'), _('Look for the current artsit on RateYourMusic'), "")
    artsit_rateyourmusic_action.connect ('activate', self.search_on_rateyourmusic, shell, 2) #The last argument "2" stands for "Artist"
    action_group.add_action(artsit_rateyourmusic_action)
    #0.3.4 Artist -> DiscoGS
    artist_discogs_action = Gtk.Action ('artist_discogs', _('DiscoGS'), _('Look for the current artist on DiscoGS'), "")
    artist_discogs_action.connect ('activate', self.search_on_discogs, shell, 2) #The last argument "2" stands for "Artist"
    action_group.add_action(artist_discogs_action)
    #0.3.5 Artist -> Official Website
    artist_official_action = Gtk.Action ('artist_official', _('Official Website'), _('Look for the current artist\'s official website'), "")
    artist_official_action.connect ('activate', self.search_on_official, shell) #No need to specify what to search
    action_group.add_action(artist_official_action)
    #0.3.6 Artist -> Lastfm
    artsit_lastfm_action = Gtk.Action ('artist_lastfm', _('Last.fm'), _('Look for the current artsit on Last.fm'), "")
    artsit_lastfm_action.connect ('activate', self.search_on_lastfm, shell, 2) #The last argument "2" stands for "Artist"
    action_group.add_action(artsit_lastfm_action)
    #0.3.7 Artist -> Facebook
    artist_facebook_action = Gtk.Action ('artist_facebook', _('Facebook'), _('Look for the current artist on Facebook'), "")
    artist_facebook_action.connect ('activate', self.search_on_facebook, shell, 2) #The last argument "2" stands for "Artist"
    action_group.add_action(artist_facebook_action)
    #0.3.8 Artist -> Myspace
    artist_myspace_action = Gtk.Action ('artist_myspace', _('Myspace'), _('Look for the current artist on Myspace'), "")
    artist_myspace_action.connect ('activate', self.search_on_myspace, shell) #No need to specify what to search
    action_group.add_action(artist_myspace_action)
    #0.3.9 Artist -> Torrentz
    artist_torrentz_action = Gtk.Action ('artist_torrentz', _('Torrentz'), _('Look for the current artist on Torrentz'), "")
    artist_torrentz_action.connect ('activate', self.search_on_torrentz, shell) #No need to specify what to search
    action_group.add_action_with_accel (artist_torrentz_action, "<alt>T")
    #0.3.10 Artist -> Every Service
    artist_all_action = Gtk.Action ('artist_all', _('All'), _('Look for the current artist on every service'), "")
    artist_all_action.connect ('activate', self.search_on_all, shell, settings, 2) #The last argument "2" stands for "Artist"
    action_group.add_action(artist_all_action)
    ui_manager = shell.props.ui_manager
    ui_manager.insert_action_group(action_group)
    self.ui_id = ui_manager.add_ui_from_string(web_menu_item)
    ui_manager.ensure_update()

##########
#The "draw_context_menu" function creates the entries in the context menu and associates them to their specific function.
##########
  def draw_context_menu(self, shell, settings): 
    #0. Web Menu
    action_group = Gtk.ActionGroup(name='WebMenuContextActionGroup')
    #0.1 Song on Youtube
    youtube_action = Gtk.Action ('search_on_youtube_action_cx', _('Song on Youtube'), _('Look for the current playing song on Youtube'), "")
    youtube_action.connect ('activate', self.search_on_youtube, shell, True) #"True" says that the command is launched from the context menu
    action_group.add_action_with_accel (youtube_action, "<alt>Y")
    #0.2.1 Album -> Wikipedia
    album_wikipedia_action = Gtk.Action ('album_wikipedia_cx', _('Wikipedia'), _('Look for the current album on Wikipedia'), "")
    album_wikipedia_action.connect ('activate', self.search_on_wikipedia, shell, 1, True)  #The last arguments: "1" stands for "Album", "True" says that the command is launched from the context menu
    action_group.add_action_with_accel (album_wikipedia_action, "<alt>W")
    #0.2.2 Album -> AllMusic
    album_allmusic_action = Gtk.Action ('album_allmusic_cx', _('AllMusic'), _('Look for the current album on AllMusic'), "")
    album_allmusic_action.connect ('activate', self.search_on_allmusic, shell, 1, True)  #The last arguments: "1" stands for "Album", "True" says that the command is launched from the context menu
    action_group.add_action(album_allmusic_action)
    #0.2.3 Album -> RateYourMusic
    album_rateyourmusic_action = Gtk.Action ('album_rateyourmusic_cx', _('RateYourMusic'), _('Look for the current album on RateYourMusic'), "")
    album_rateyourmusic_action.connect ('activate', self.search_on_rateyourmusic, shell, 1, True)  #The last arguments: "1" stands for "Album", "True" says that the command is launched from the context menu
    action_group.add_action(album_rateyourmusic_action)
    #0.2.4 Album -> AllAboutJazz
    album_allaboutjazz_action = Gtk.Action ('album_allaboutjazz_cx', _('AllAboutJazz'), _('Look for the current album on AllAboutJazz'), "")
    album_allaboutjazz_action.connect ('activate', self.search_on_allaboutjazz, shell, True)  #No need to specify what to search, "True" says that the command is launched from the context menu"
    action_group.add_action(album_allaboutjazz_action)
    #0.2.5 Album -> DiscoGS
    album_discogs_action = Gtk.Action ('album_discogs_cx', _('DiscoGS'), _('Look for the current album on DiscoGS'), "")
    album_discogs_action.connect ('activate', self.search_on_discogs, shell, 1, True)  #The last arguments: "1" stands for "Album", "True" says that the command is launched from the context menu
    action_group.add_action(album_discogs_action)
    #0.2.6 Album -> Lastfm
    album_lastfm_action = Gtk.Action ('album_lastfm_cx', _('Last.fm'), _('Look for the current album on Last.fm'), "")
    album_lastfm_action.connect ('activate', self.search_on_lastfm, shell, 1, True) #The last arguments: "1" stands for "Album", "True" says that the command is launched from the context menu
    action_group.add_action(album_lastfm_action)
    #0.2.7 Album -> Facebook
    album_facebook_action = Gtk.Action ('album_facebook_cx', _('Facebook'), _('Look for the current album on Facebook'), "")
    album_facebook_action.connect ('activate', self.search_on_facebook, shell, 1, True)  #The last arguments: "1" stands for "Album", "True" says that the command is launched from the context menu
    action_group.add_action(album_facebook_action)
    #0.2.8 Album -> Every Service
    album_all_action = Gtk.Action ('album_all_cx', _('All'), _('Look for the current album on every service'), "")
    album_all_action.connect ('activate', self.search_on_all, shell, settings, 1, True)  #The last arguments: "1" stands for "Album", "True" says that the command is launched from the context menu"
    action_group.add_action(album_all_action)
    #0.3.1 Artist -> Wikipedia
    artist_wikipedia_action = Gtk.Action ('artist_wikipedia_cx', _('Wikipedia'), _('Look for the current artist on Wikipedia'), "")
    artist_wikipedia_action.connect ('activate', self.search_on_wikipedia, shell, 2, True)  #The last argument "2" stands for "Artist", "True" says that the command is launched from the context menu"
    action_group.add_action(artist_wikipedia_action)
    #0.3.2 Artist -> AllMusic
    artist_allmusic_action = Gtk.Action ('artist_allmusic_cx', _('AllMusic'), _('Look for the current artist on AllMusic'), "")
    artist_allmusic_action.connect ('activate', self.search_on_allmusic, shell, 2, True) #The last argument "2" stands for "Artist", "True" says that the command is launched from the context menu"
    action_group.add_action_with_accel (artist_allmusic_action, "<alt>A")
    #0.3.3 Artist -> RateYourMusic
    artsit_rateyourmusic_action = Gtk.Action ('artist_rateyourmusic_cx', _('RateYourMusic'), _('Look for the current artsit on RateYourMusic'), "")
    artsit_rateyourmusic_action.connect ('activate', self.search_on_rateyourmusic, shell, 2, True) #The last argument "2" stands for "Artist", "True" says that the command is launched from the context menu"
    action_group.add_action(artsit_rateyourmusic_action)
    #0.3.4 Artist -> DiscoGS
    artist_discogs_action = Gtk.Action ('artist_discogs_cx', _('DiscoGS'), _('Look for the current artist on DiscoGS'), "")
    artist_discogs_action.connect ('activate', self.search_on_discogs, shell, 2, True) #The last argument "2" stands for "Artist", "True" says that the command is launched from the context menu"
    action_group.add_action(artist_discogs_action)
    #0.3.5 Artist -> Official Website
    artist_official_action = Gtk.Action ('artist_official_cx', _('Official Website'), _('Look for the current artist\'s official website'), "")
    artist_official_action.connect ('activate', self.search_on_official, shell, True) #No need to specify what to search, "True" says that the command is launched from the context menu"
    action_group.add_action(artist_official_action)
    #0.3.6 Artist -> Lastfm
    artsit_lastfm_action = Gtk.Action ('artist_lastfm_cx', _('Last.fm'), _('Look for the current artsit on Last.fm'), "")
    artsit_lastfm_action.connect ('activate', self.search_on_lastfm, shell, 2, True) #The last argument "2" stands for "Artist"
    action_group.add_action(artsit_lastfm_action)
    #0.3.7 Artist -> Facebook
    artist_facebook_action = Gtk.Action ('artist_facebook_cx', _('Facebook'), _('Look for the current artist on Facebook'), "")
    artist_facebook_action.connect ('activate', self.search_on_facebook, shell, 2, True) #The last argument "2" stands for "Artist", "True" says that the command is launched from the context menu"
    action_group.add_action(artist_facebook_action)
    #0.3.8 Artist -> Myspace
    artist_myspace_action = Gtk.Action ('artist_myspace_cx', _('Myspace'), _('Look for the current artist on Myspace'), "")
    artist_myspace_action.connect ('activate', self.search_on_myspace, shell, True) #No need to specify what to search, "True" says that the command is launched from the context menu"
    action_group.add_action(artist_myspace_action)
    #0.3.9 Artist -> Torrentz
    artist_torrentz_action = Gtk.Action ('artist_torrentz_cx', _('Torrentz'), _('Look for the current artist on Torrentz'), "")
    artist_torrentz_action.connect ('activate', self.search_on_torrentz, shell, True) #No need to specify what to search, "True" says that the command is launched from the context menu"
    action_group.add_action_with_accel (artist_torrentz_action, "<alt>T")
    #0.3.10 Artist -> Every Service
    artist_all_action = Gtk.Action ('artist_all_cx', _('All'), _('Look for the current artist on every service'), "")
    artist_all_action.connect ('activate', self.search_on_all, shell, settings, 2, True) #The last argument "2" stands for "Artist", "True" says that the command is launched from the context menu"
    action_group.add_action(artist_all_action)
    ui_manager = shell.props.ui_manager
    ui_manager.insert_action_group(action_group)
    self.ui_context_id = ui_manager.add_ui_from_string(web_context_item)
    ui_manager.ensure_update()

##########
#The "apply_settings" function is called when Rhythmbox is loaded and whenever the settings are changed
##########
  def apply_settings(self, settings, key, shell, config):  
    self.settings = config.get_settings()
    paths=["/MenuBar/WebMenu", "/QueuePlaylistViewPopup/PluginPlaceholder", "/BrowserSourceViewPopup/PluginPlaceholder", "/PlaylistViewPopup/PluginPlaceholder", "/PodcastViewPopup/PluginPlaceholder"] #Settings must be applied to the Web Menu and to every context menu
    for path in paths:
     for website in self.settings["default-album-services"]: #Hides the non-active options in the "Album" submenu
	menu_option=path+"/AlbumMenu/AL_"+website
	if (website not in self.settings["active-album-services"]):
		shell.props.ui_manager.get_widget(menu_option).hide()
	else:
		shell.props.ui_manager.get_widget(menu_option).show()

     for website in self.settings["default-artist-services"]: #Hides the non-active options in the "Artist" submenu
	menu_option=path+"/ArtistMenu/AR_"+website
	if (website not in self.settings["active-artist-services"]):
		shell.props.ui_manager.get_widget(menu_option).hide()
	else:
		shell.props.ui_manager.get_widget(menu_option).show()

##########
#The "do_activate" function is called when Rhythmbox is loaded
##########
  def do_activate(self):
    shell = self.object
    config = WMConfig()
    self.settings = config.get_settings()

    self.draw_menu(shell, self.settings) #Calls "draw_menu"
    self.draw_context_menu(shell, self.settings) #Calls "draw_context_menu"
    self.apply_settings('oldsettings', None , shell, config) #Calls "apply_settings"
    self.settings.connect('changed', self.apply_settings, shell, config) #Connects a change in the settings menus to "apply_settings"

    sp=shell.props.shell_player #Connects play/stop events to "song_changed")
    sp.connect ('playing-changed', self.song_changed, shell.props, config.get_settings())
    self.song_changed('start', '', shell.props, config.get_settings())

##########
#The "do_deactivate" function removes the 'Web' Menu and the context menu
##########
  def do_deactivate(self):
    shell = self.object
    ui_manager = shell.props.ui_manager
    ui_manager.remove_ui(self.ui_id) 
    del self.ui_id
    ui_manager.remove_ui(self.ui_context_id)
    del self.ui_context_id

##########
#The "get_metadata" function gets and returns, in order, TITLE, ALBUM and ARTIST of the current playing song as elements of an array (0,1,2)
##########
  def get_metadata(self, shell, context=False):
    if context:
	page = shell.props.selected_page
	if not hasattr(page, "get_entry_view"): return
	selected = page.get_entry_view().get_selected_entries()
	if selected != []:
		playing_title = selected[0].get_string(RB.RhythmDBPropType.TITLE)
		playing_album = selected[0].get_string(RB.RhythmDBPropType.ALBUM)
		playing_artist = selected[0].get_string(RB.RhythmDBPropType.ARTIST)	   
    else:
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
    command="gnome-open http://www.youtube.com/results?search_query=\"" + urllib2.quote(metadata[0]) + "\"+\"" + urllib2.quote(metadata[2]) + "\""
    os.system(command)

##########
#The "search_on_wikipedia" function search the artist OR the album on wikipedia; "what" argument: 0=title (not used), 1=album, 2=artist
##########
  def search_on_wikipedia(self, event, shell, what, context=False):
    metadata=self.get_metadata(shell, context) #Calls "get_metadata"
    command="gnome-open http://en.wikipedia.org/w/index.php?search=\"" + urllib2.quote(metadata[what]) + "\""
    os.system(command)

##########
#The "search_on_allmusic" function search the artist OR the album on allmusic; "what" argument: 0=title (not used), 1=album, 2=artist
##########
  def search_on_allmusic(self, event, shell, what, context=False):
    metadata=self.get_metadata(shell, context) #Calls "get_metadata"
    what_text=['songs', 'albums', 'artists'] #Allmusic uses differt search engines for Songs, Albums and Artists
    command="gnome-open http://www.allmusic.com/search/"+what_text[what]+"/\"" + urllib2.quote(metadata[what]) + "\""
    if what==1: command=command + "+\"" + urllib2.quote(metadata[2]) + "\"" #If you're looking for the album, the artist is added to get better results
    os.system(command)

##########
#The "search_on_rateyourmusic" function search the artist OR the album on rateyourmuisc; "what" argument: 0=title (not used), 1=album, 2=artist
##########
  def search_on_rateyourmusic(self, event, shell, what, context=False):
    metadata=self.get_metadata(shell, context) #Calls "get_metadata"
    what_text=['', 'l', 'a'] #rateyourmusic uses differt search engines for Songs, Albums and Artists
    command="gnome-open \"http://rateyourmusic.com/search?searchterm=" + urllib2.quote(metadata[what]) + "&searchtype=" + what_text[what] + "\""
    os.system(command)

##########
#The "search_on_allaboutjazz" function search the album on allaboutjazz
##########
  def search_on_allaboutjazz(self, event, shell, context=False):
    metadata=self.get_metadata(shell, context) #Calls "get_metadata"
    command="gnome-open \"http://www.allaboutjazz.com/googlesearch.php?cx=005595936876858408448%3Ahfhqnzuknl8&cof=FORID%3A11&q=" + urllib2.quote(metadata[2] + " " + metadata[1] + " review") + "\""  #If you're looking for the album, the artist is added to get better results
    os.system(command)

##########
#The "search_on_discogs" function search the artist OR the album on facebook; "what" argument: 0=title (not used), 1=album, 2=artist
##########
  def search_on_discogs(self, event, shell, what, context=False):
    metadata=self.get_metadata(shell, context) #Calls "get_metadata"
    what_text=['track', 'release_title', 'artist'] #Allmusic uses differt search engines for Songs, Albums and Artists
    command="gnome-open \"http://www.discogs.com/advanced_search?" + what_text[what] + "=" + urllib2.quote(metadata[what]) + "\""
    if what==1: command=command + "\"&artist=" + urllib2.quote(metadata[2]) + "\"" #If you're looking for the album, the artist is added to get better results
    os.system(command)

##########
#The "search_on_official" function opens the first result on Google for the query "ARTIST official website"
##########
  def search_on_official(self, event, shell, context=False):
    metadata=self.get_metadata(shell, context) #Calls "get_metadata"
    command="gnome-open \"http://www.google.com/search?q=" + urllib2.quote(metadata[2]+" official website") + "\"" #add btnI=I%27m+Feeling+Lucky& before the 'q=' to open the first result
    os.system(command)

##########
#The "search_on_lastfm" function search the artist OR the album on lastfm; "what" argument: 0=title (not used), 1=album, 2=artist
##########
  def search_on_lastfm(self, event, shell, what, context=False):
    metadata=self.get_metadata(shell, context) #Calls "get_metadata"
    what_text=['track', 'album', 'artist'] #Lastfm uses differt search engines for Songs, Albums and Artists
    command="gnome-open \"http://www.last.fm/search?type=" + what_text[what] + "&q=" + urllib2.quote(metadata[what]) + "\""
    os.system(command)

##########
#The "search_on_facebook" function search the artist OR the album on facebook; "what" argument: 0=title (not used), 1=album, 2=artist
##########
  def search_on_facebook(self, event, shell, what, context=False):
    metadata=self.get_metadata(shell, context) #Calls "get_metadata"
    command="gnome-open \"https://www.facebook.com/search/results.php?type=pages&q=" + urllib2.quote(metadata[what]) + "\""
    os.system(command)

##########
#The "search_on_myspace" function search ARTIST on myspace
##########
  def search_on_myspace(self, event, shell, context=False):
    metadata=self.get_metadata(shell, context) #Calls "get_metadata"
    command="gnome-open http://www.myspace.com/search/Music?q=\"" + urllib2.quote(metadata[2]) + "\""
    os.system(command)

##########
#The "search_on_torrentz" function search ARTIST on torrentz
##########
  def search_on_torrentz(self, event, shell, context=False):
    metadata=self.get_metadata(shell, context) #Calls "get_metadata"
    command="gnome-open http://torrentz.com/search?f=\"" + urllib2.quote(metadata[2]) + "\""
    os.system(command)

##########
#The "search_on_all" function search the artist OR the album on every service which is activ; "what" argument: 0=title (not used), 1=album, 2=artist
##########
  def search_on_all(self, event, shell, settings, what, context=False):
    what_in_letters=['active-album-services', 'active-artist-services']

    if 'wikipedia' in settings[what_in_letters[what-1]]: self.search_on_wikipedia('activate', shell, what, context)
    if 'allmusic' in settings[what_in_letters[what-1]]: self.search_on_allmusic('activate', shell, what, context)
    if 'rateyourmusic' in settings[what_in_letters[what-1]]: self.search_on_rateyourmusic('activate', shell, what, context)
    if 'allaboutjazz' in settings[what_in_letters[what-1]]: self.search_on_allaboutjazz('activate', shell, context)
    if 'discogs' in settings[what_in_letters[what-1]]: self.search_on_discogs('activate', shell, what, context)
    if 'official' in settings[what_in_letters[what-1]]: self.search_on_official('activate', shell, context)
    if 'lastfm' in settings[what_in_letters[what-1]]: self.search_on_facebook('activate', shell, what, context)
    if 'facebook' in settings[what_in_letters[what-1]]: self.search_on_lastfm('activate', shell, what, context)
    if 'myspace' in settings[what_in_letters[what-1]]: self.search_on_myspace('activate', shell, context)
    if 'torrentz' in settings[what_in_letters[what-1]]:  self.search_on_torrentz('activate', shell, context)

##########
#The "song_changed" function controls if no song is playing. If it is so, the 'Web' menu options are disabled.
##########
  def song_changed(self, playing, user_data, s_props, settings):
    self.playing_entry = s_props.shell_player.get_playing_entry() 
    now_is_playing=self.playing_entry is not None #current playing song==None --> False

    s_props.ui_manager.get_widget("/MenuBar/WebMenu/YTitem").set_sensitive(now_is_playing)  #Disable the YouTube Option
    for website in settings["default-album-services"]: #Disable all the options in the "Album" submenu
	menu_option="/MenuBar/WebMenu/AlbumMenu/AL_"+website
        s_props.ui_manager.get_widget(menu_option).set_sensitive(now_is_playing)
    for website in settings["default-artist-services"]: #Enable all the options in the "Album" submenu
	menu_option="/MenuBar/WebMenu/ArtistMenu/AR_"+website
        s_props.ui_manager.get_widget(menu_option).set_sensitive(now_is_playing)

