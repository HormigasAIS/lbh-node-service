#!/bin/bash
# HORMIGASAIS · centinela_v24.sh v1.0
# Vigilancia A20 desde A16 cada 5 min via SSH
LOG=/data/data/com.termux/files/home/hormigasais-lab/centinela.log
echo "[CENTINELA] Vigilancia iniciada. Intervalo: 5 min"
while true; do
    bash ~/hormigasais-lab/lbh-node-service/levantar_a20_remoto.sh
    echo "$(date '+%Y-%m-%d %H:%M:%S') centinela OK" >> $LOG
    sleep 300
done
