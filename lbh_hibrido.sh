#!/bin/bash
# HORMIGASAIS · lbh_hibrido.sh
# Activa Gitea en modo hibrido (LAN + localhost)

echo "LBH :: Activando modo hibrido soberano..."

APP_INI=/data/data/com.termux/files/usr/etc/gitea/app.ini

if [ ! -f "$APP_INI" ]; then
    echo "ERROR: app.ini no encontrado en $APP_INI"
    exit 1
fi

cp "$APP_INI" "$APP_INI.bak"
echo "Backup creado: app.ini.bak"

sed -i "/HTTP_ADDR/d" "$APP_INI"
echo "HTTP_ADDR = 0.0.0.0" >> "$APP_INI"
echo "HTTP_PORT = 3001" >> "$APP_INI"
echo "Modo hibrido activado (LAN + localhost)"

pkill gitea 2>/dev/null
sleep 2
gitea web > ~/hormigasais-lab/gitea.log 2>&1 &
echo "Gitea reiniciado PID: $!"

sleep 2
curl -s http://127.0.0.1:3001 > /dev/null && echo "OK localhost:3001" || echo "WARN localhost no responde"
curl -s http://192.168.1.5:3001 > /dev/null && echo "OK LAN:3001" || echo "WARN LAN no responde"

echo "--------------------------------------------------"
echo "Local: http://127.0.0.1:3001"
echo "LAN:   http://192.168.1.5:3001"
echo "LBH modo hibrido activo"
