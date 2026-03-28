#!/bin/bash
# HORMIGASAIS · lbh_autostart.sh · v1.0
# Orquestador de Resiliencia del Nodo A16

echo "🐜 Iniciando Protocolo de Resiliencia LBH..."
termux-wake-lock # Evita que Android suspenda el proceso

# 1. Levantar Gitea (Gestión de Código)
if ! pgrep -f "gitea" > /dev/null; then
    echo "🚀 Levantando Gitea..."
    nohup gitea web -c ~/gitea/custom/conf/app.ini > /dev/null 2>&1 &
fi

# 2. Levantar LBH API (Corazón de Datos)
if ! pgrep -f "lbh_api.py" > /dev/null; then
    echo "🚀 Levantando LBH API..."
    cd ~/hormigasais-lab/lbh-node-service
    nohup python3 lbh_api.py > lbh_api.log 2>&1 &
fi

# 3. Levantar Web UI (Monitor Visual)
if ! pgrep -f "http.server 8080" > /dev/null; then
    echo "🚀 Levantando Dashboard Web..."
    nohup python3 -m http.server 8080 --bind 192.168.1.3 --directory ~/hormigasais-lab/lbh-node-service/ > ~/dashboard_web.log 2>&1 &
fi

echo "✅ Nodo A16 Operativo en 192.168.1.3"
