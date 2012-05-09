#!/bin/bash
DATA="/usr/share/lightdm-configurator"
BIN="/usr/bin/"
DESKTOP="/usr/share/applications/"

mkdir -p $DATA
cp -r data $DATA
cp __init__.py $DATA
cp interface_gtk.glade $DATA
cp lightdm-config_gtk3.py $DATA
cp lightdm_reader.py $DATA
cp lightdm-configurator $BIN
cp lightdm-configurator.desktop $DESKTOP

echo "Todo Instalado!!"


