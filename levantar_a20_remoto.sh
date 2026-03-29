#!/bin/bash
# HORMIGASAIS · levantar_a20_remoto.sh v0.2
# Rescue remoto via SSH desde A16 → A20
A20_IP=192.168.1.7
A20_PORT=8022
echo "[RESCUE] Inspeccionando A20 ($A20_IP)..."
if ping -c 1 -W 2 $A20_IP > /dev/null 2>&1; then
    echo "A20 en linea. Verificando bridge..."
    CHECK=$(ssh -p $A20_PORT -o ConnectTimeout=5 $A20_IP "pgrep -f bridge_a20.py" 2>/dev/null)
    if [ -z "$CHECK" ]; then
        echo "Bridge caido. Reanimando..."
        ssh -p $A20_PORT -o ConnectTimeout=5 $A20_IP             "nohup bash ~/hormigasais-lab/levantar_a20.sh > /dev/null 2>&1 &"
        echo "Comando enviado."
        python3 ~/hormigasais-lab/lbh-node-service/hormiga_slack_fiscal.py             A20-AirCity BRIDGE_DOWN RESCUE 2>/dev/null
    else
        echo "Bridge OK (PID: $CHECK)"
    fi
else
    echo "A20 inalcanzable. Verifica WiFi o bateria."
fi
