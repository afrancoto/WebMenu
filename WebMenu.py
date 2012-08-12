from gi.repository import GObject, RB, Peas, Gtk
import os
import urllib2

web_menu_item = '''
  <ui>
    <menubar name="MenuBar">
      <menu name="WebMenu" action="WebMenuAction">
        <menuitem name="SearchonYTitem" action="SearchOnYT"/>
	<menuitem name="SearchonWPitem" action="SearchOnWP"/>
      </menu>
    </menubar>
  </ui>
'''

class WebMenuPlugin(GObject.Object, Peas.Activatable):
  #__gtype_name__ = 'SearchOnYTPlugin'
  object = GObject.property(type=GObject.Object)

  def __init__(self):
    super(WebMenuPlugin, self).__init__()

  def do_activate(self):
    shell = self.object
    #Web Menu
    action_group = Gtk.ActionGroup(name='WebMenuActionGroup')
    menu_action = Gtk.Action("WebMenuAction", _("Web"), None, None)
    action_group.add_action(menu_action)
    #Search on Youtube
    YTaction = Gtk.Action ('SearchOnYT', _('Search Song on Youtube'), _('Look for the current playing song on Youtube'), "")
    YTaction.connect ('activate', self.search_on_youtube, shell)
    action_group.add_action_with_accel (YTaction, "<alt>Y")
    action_group.add_action(YTaction)
    #Search on Wikipedia
    WPaction = Gtk.Action ('SearchOnWP', _('Search Album on Wikipedia'), _('Look for the current album on Wikipedia'), "")
    WPaction.connect ('activate', self.search_on_wikipedia, shell)
    action_group.add_action_with_accel (WPaction, "<alt>W")
    action_group.add_action(WPaction)

    ui_manager = shell.props.ui_manager
    ui_manager.insert_action_group(action_group)
    self.ui_id = ui_manager.add_ui_from_string(web_menu_item)

  def do_deactivate(self):
    print 'Deactivating Search On YT Plugin'
    shell = self.object
    ui_manager = shell.props.ui_manager
    ui_manager.remove_ui(self.ui_id)

  def search_on_youtube(self, event, shell):
    self.playing_entry = shell.props.shell_player.get_playing_entry()
    playing_entry = self.playing_entry
    playing_artist = self.playing_entry.get_string(RB.RhythmDBPropType.ARTIST)
    playing_title = self.playing_entry.get_string(RB.RhythmDBPropType.TITLE)
    #playing_album = self.playing_entry.get_string(RB.RhythmDBPropType.ALBUM)

    command="gnome-open http://www.youtube.com/results?search_query=\"" + urllib2.quote(playing_title) + "\"+\"" + urllib2.quote(playing_artist) + "\""
    os.system(command)

  def search_on_wikipedia(self, event, shell):
    self.playing_entry = shell.props.shell_player.get_playing_entry()
    playing_entry = self.playing_entry
    #playing_artist = self.playing_entry.get_string(RB.RhythmDBPropType.ARTIST)
    #playing_title = self.playing_entry.get_string(RB.RhythmDBPropType.TITLE)
    playing_album = self.playing_entry.get_string(RB.RhythmDBPropType.ALBUM)

    command="gnome-open http://en.wikipedia.org/w/index.php?search=\"" + urllib2.quote(playing_album) + "\""
    os.system(command)
