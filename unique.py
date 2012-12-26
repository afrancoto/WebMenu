from gi.repository import GObject, RB, Peas, Gtk
import os
import urllib2 

#Services data are stored in a matrix like this:
# Line 0: SERVICE_LABEL, ALBUM_URL_WITH_KEYWORDS, ARTIST_URL_WITH_KEYWORDS
# Line 1: SERVICE_LABEL, ALBUM_URL_WITH_KEYWORDS, ARTIST_URL_WITH_KEYWORDS
# Line 2: SERVICE_LABEL, ALBUM_URL_WITH_KEYWORDS, ARTIST_URL_WITH_KEYWORDS
# ...

services_array = [''*3]*3

class Person:
  def __init__(self):
	global services_array
	services_array[1]=["AllMusic", "http://www.allmusic.com/search/albums/[ALBUM]+[ARTIST]", "http://www.allmusic.com/search/artists/[ARTIST]"]
	services_array[2]=["Wikipedia", "http://en.wikipedia.org/w/index.php?search=[ALBUM]", "http://en.wikipedia.org/w/index.php?search=[ARTIST]"]
	services_array[0]=["Fail","Fail", "Fail"]
	self.the_unique_function('activate', None, 1, 'allmusic', False) #Simulates click, shell=none because we don't need it in this example, 1=album/2=artist, allmusic/wikipedia=the service in lowercase, False=command sent from Menubar 

##########
#The "the_unique_function" is the one which is called by the menu/context menu actions
##########
  def the_unique_function(self, event, shell, what, service, context=False):
	metadata=self.get_metadata(shell, context) #Calls "get_metadata"
	print "We are looking for",metadata[what],"on",service
	service_line_number=self.search_service_line_number(service) #Gets the service line number
	print "Line number is:", service_line_number
	URL=services_array[service_line_number][what] #Gets the URL with keywords
	print "URL is:", URL
	command="gnome-open \"" + self.replace_keywords(URL, metadata) + "\"" #Replace keywords
	print "command is:", command
	#os.system(command)

##########
#The "search_service_line_number" function search the service in each line and return its line number, or 0 if the service isn't in the matrix
##########
  def search_service_line_number(self, service):
	line_number=0
	for line in services_array:
		if service in line[0].lower(): return line_number
		line_number=line_number+1
	return 0

##########
#The "replace_keywords" function simply replace the keywords with the metadata
##########
  def replace_keywords(self, URL, metadata):
	URL=URL.replace('[ALBUM]', metadata[1])
	URL=URL.replace('[ARTIST]', metadata[2])
	return URL

##########
#WEBMENU FUNCTIONS TO MAKE THE SCRIPT WORK
##########
  def get_metadata(self, shell, context=False):
	result=['mysong', 'myalbum', 'myartist']
	return result

if __name__ == '__main__': Person() 

