#!/bin/bash
# HORMIGASAIS · lbh_service.sh · v2.2-stable
DIR="/data/data/com.termux/files/home/hormigasais-lab/lbh-node-service"
API_SCRIPT="$DIR/lbh_api.py"
LOG_FILE="$DIR/lbh_api.log"

case "$1" in
    start)
        pgrep -f "lbh_api.py" > /dev/null && echo "🐜 Ya corre." && exit
        echo "🚀 Iniciando API LBH..."
        nohup python3 "$API_SCRIPT" > "$LOG_FILE" 2>&1 &
        sleep 1
        echo "✅ API en puerto 3002."
        ;;
    stop)
        echo "🛑 Deteniendo API..."
        pkill -f "lbh_api.py" && echo "✅ Detenida." || echo "❌ No activa."
        ;;
    status)
        if pgrep -f "lbh_api.py" > /dev/null; then
            echo "🟢 ACTIVA (Puerto 3002)"
            [ -f "$LOG_FILE" ] && tail -n 2 "$LOG_FILE"
        else
            echo "🔴 INACTIVA"
        fi
        ;;
    *)
        echo "Uso: ./lbh_service.sh {start|stop|status}"
        ;;
esac
