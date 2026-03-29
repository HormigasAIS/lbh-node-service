#!/data/data/com.termux/files/usr/bin/bash

# HORMIGASAIS · lbh_autostart.sh · v2.0 (Resiliencia Industrial)
echo "🐜 [HormigasAIS] Iniciando protocolo de recuperación de Soberanía..."

# 1. Asegurar persistencia en Android
termux-wake-lock

# 2. Módulo de Soberanía (Gitea)
if ! pgrep -f "gitea web" > /dev/null; then
    echo "🚀 Levantando Gitea en Puerto 3001..."

    # Limpieza agresiva de puerto
    fuser -k 3001/tcp > /dev/null 2>&1

    # Arranque controlado
    nohup gitea web -p 3001 > ~/gitea_autostart.log 2>&1 &
    GITEA_PID=$!

    # Validación activa (clave para el Nodo A16)
    echo "📡 Esperando respuesta del Nodo Local..."
    for i in {1..7}; do
        if curl -s -o /dev/null -I http://127.0.0.1:3001; then
            echo "✅ Soberanía validada: Gitea activo en PID $GITEA_PID"
            break
        fi
        [ $i -eq 7 ] && echo "⚠️ Nodo no respondió, revisar ~/gitea_autostart.log"
        sleep 1
    done
fi

# 3. Módulo de Visualización (Dashboard)
if ! pgrep -f "http.server 8080" > /dev/null; then
    echo "📊 Iniciando Monitor Visual en puerto 8080..."
    cd ~/hormigasais-lab/lbh-node-service
    nohup python3 -m http.server 8080 > ~/dashboard_web.log 2>&1 &
fi

echo "✅ Nodo A16 Operativo y Autosanado."
