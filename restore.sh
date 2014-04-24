#! /bin/sh
# -------------------------------------------------
#  carga las configuraciones correspondientes
# -------------------------------------------------

if [ $1 == "posgre" ]; then
    echo "Cargando configuracion para PosgreSQL"
    cp settings-posgre.py settings.py
    
elif [ $1 == "sqlite" ]; then
    echo "Cargando configuracion para Sqlite"
    cp settings-sqlite.py settings.py
else
    echo "Parametro Invalido: $1"
fi
