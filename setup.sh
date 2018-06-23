#!/bin/bash

echo -e "\n";
echo " *****************************************************************";
echo "      ___       ______      __    __   __   __           ___      ";
echo "     /   \     /  __  \    |  |  |  | |  | |  |         /   \     ";
echo "    /  ^  \   |  |  |  |   |  |  |  | |  | |  |        /  ^  \    ";
echo "   /  /_\  \  |  |  |  |   |  |  |  | |  | |  |       /  /_\  \   ";
echo "  /  _____  \ |  '--'  '--.|  '--'  | |  | |  '----. /  _____  \  ";
echo " /__/     \__\ \_____\_____\\______/  |__| |_______|/__/     \__\ ";
echo " *****************************************************************";
echo "	Installation And Update Script v0.1								";
echo " *****************************************************************";
echo -e "\n";

# ------- Functions ----------

command_exists() {
    which $@ > /dev/null 2>&1
}

# 1 - program name, 2 - description, 3 - RPM package name
prog_exists() {
    command_exists $1
    if [ "$?" != 0 ] ; then
        echo " [ERR] $1 is not installed or not in PATH."
        exit 2
    fi
}

err() {
	echo " [ERR] $1"
}

# --------- MAIN ---------

USER=`whoami`
AQUILA_HOME="/var/www/Aquila/"

# Check for root
if [[ $USER != 'root' ]] ; then
    err "Please run Aquila install script as root"
    exit 1;
fi

# Check for required programs
prog_exists python3
prog_exists pip
prog_exists uwsgi
prog_exists psql
prog_exists git

# sudo uwsgi --ini /var/www/Aquila/configs/uwsgi.ini --daemonize /var/www/Aquila/aquila/var/log/uwsgi.log
