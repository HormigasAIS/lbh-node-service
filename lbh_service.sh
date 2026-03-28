#!/bin/bash
# HORMIGASAIS · lbh_service.sh
# Control del Micro-Servicio API LBH

API_SCRIPT="/data/data/com.termux/files/home/hormigasais-lab/lbh-node-service/lbh_api.py"
LOG_FILE="/data/data/com.termux/files/home/hormigasais-lab/lbh_api.log"

case "" in
    start)
        if pgrep -f "lbh_api.py" > /dev/null; then
            echo "🐜 LBH API ya está corriendo."
        else
            echo "🚀 Iniciando API LBH en segundo plano..."
            nohup python3 "" > "" 2>&1 &
            echo "✅ API activa (Puerto 3002)."
        fi
        ;;
    stop)
        echo "🛑 Deteniendo API LBH..."
        pkill -f "lbh_api.py" && echo "✅ Servicio detenido." || echo "❌ No hay servicio activo."
        ;;
    status)
        if pgrep -f "lbh_api.py" > /dev/null; then
            PID=
            echo "🟢 API LBH ACTIVA (PID: )"
            tail -n 3 ""
        else
            echo "🔴 API LBH INACTIVA"
        fi
        ;;
    *)
        echo "Uso: ./lbh_service.sh {start|stop|status}"
        ;;
esac
