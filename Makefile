PLUGIN_PATH=~/.local/share/rhythmbox/plugins/WebMenu
install: upschema
	@echo Installing Rhythmbox Web Menu:
	@mkdir -p $(PLUGIN_PATH)
	@cp * $(PLUGIN_PATH) -Rf
	@echo DONE!
uninstall:
	@echo Removing Rhythmbox Web Menu:
	@rm -Rf $(PLUGIN_PATH) /usr/share/glib-2.0/schemas/org.gnome.rhythmbox.plugins.webmenu.gschema.xml
	@glib-compile-schemas /usr/share/glib-2.0/schemas
	@echo DONE!
upschema:
	@cp org.gnome.rhythmbox.plugins.webmenu.gschema.xml /usr/share/glib-2.0/schemas 
	@glib-compile-schemas /usr/share/glib-2.0/schemas
