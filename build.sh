#!/bin/bash

case $1 in
	"-s")
		echo 'Installing... sudo is required'
		sudo apt-get install python3 python3-pip
		sudo apt-get install vlc browser-plugin-vlc python3-dbus
		sudo apt-get install python3-tk
		pip3 install python-vlc
		pip3 install vk
	;;
	*)
		echo 'Defatult launch'
esac

killall -9 python3
python3 main.py
