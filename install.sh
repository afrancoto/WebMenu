#!/bin/bash

################################ USAGE #######################################

usage=$(
cat <<EOF
Usage:
$0 [OPTION]
-h                show this message.
-l, --local       install the plugin locally (default).
-g, --global      install the plugin globally.
-u, --uninstall   removes the plugin

EOF
)

########################### OPTIONS PARSING #################################

#parse options
TMP=`getopt --name=$0 -a --longoptions=local,global,uninstall,help -o l,g,u,h -- $@`

if [[ $? == 1 ]]
then
    echo
    echo "$usage"
    exit
fi

eval set -- $TMP

until [[ $1 == -- ]]; do
    case $1 in
        -l|--local)
            LOCAL=true
	    REMOVE_ONLY=false
            ;;
        -g|--global)
            LOCAL=false
	    REMOVE_ONLY=false
            ;;
        -u|--uninstall)
            REMOVE_ONLY=true
            ;;
        -h|--help)
            echo "$usage"
            exit
            ;;
    esac
    shift # move the arg list to the next option or '--'
done
shift # remove the '--', now $1 positioned at first argument if any

#default values
LOCAL=${LOCAL:=true}
REMOVE_ONLY=${REMOVE_ONLY:=false}

echo Local installation: $LOCAL

########################## START INSTALLATION ################################

#define constants
GLIB_SCHEME="org.gnome.rhythmbox.plugins.webmenu.gschema.xml"
GLIB_DIR="/usr/share/glib-2.0/schemas/"
SCRIPT_NAME=`basename "$0"`
SCRIPT_PATH=${0%`basename "$0"`}

#deletes old files
echo "Deleting old files (password needed)"
#sudo rm "${GLIB_DIR}${GLIB_SCHEME}" &>/dev/null
sudo rm -r "/home/${USER}/.local/share/rhythmbox/plugins/WebMenu" &>/dev/null
sudo rm -r "/usr/lib/rhythmbox/plugins/WebMenu" &>/dev/null

if [[ $REMOVE_ONLY == false ]]
then

#install the glib schema
echo "Installing the glib schema (password needed)"
sudo cp "${PLUGIN_PATH}${GLIB_SCHEME}" "$GLIB_DIR"
sudo glib-compile-schemas "$GLIB_DIR"

#install the plugin; the install path depends on the install mode
echo Installing the plugin
if [[ $LOCAL == true ]]
then
    PLUGIN_PATH="/home/${USER}/.local/share/rhythmbox/plugins/WebMenu/"
    echo in $PLUGIN_PATH
    
    #build the dirs
    mkdir -p $PLUGIN_PATH

    #copy the files
    cp -r "${SCRIPT_PATH}"* "$PLUGIN_PATH"

    #remove the install script from the dir (not needed)
    #rm "${PLUGIN_PATH}${SCRIPT_NAME}"
else
    PLUGIN_PATH="/usr/lib/rhythmbox/plugins/WebMenu/"
    echo in $PLUGIN_PATH
    
    #build the dirs
    sudo mkdir -p $PLUGIN_PATH

    #copy the files
    sudo cp -r "${SCRIPT_PATH}"* "$PLUGIN_PATH"

    #remove the install script from the dir (not needed)
    #sudo rm "${PLUGIN_PATH}${SCRIPT_NAME}"
fi

fi
echo "DONE! :D"
