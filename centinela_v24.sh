#!/bin/bash
# HORMIGASAIS · centinela_v24.sh v1.0.1 · LBH v1.1
# Vigilancia A20 desde A16 cada 5 min via SSH · Rutas Reales

REPO=/data/data/com.termux/files/home/lbh-node-service
LOG=$REPO/centinela.log

echo '[CENTINELA] Vigilancia iniciada. Intervalo: 5 min'

while true; do
    # Ejecutar rescate desde la ubicación real
    bash $REPO/levantar_a20_remoto.sh
    
    # Escribir en el log correcto
    echo "$(date '+%Y-%m-%d %H:%M:%S') centinela OK" >> $LOG
    
    sleep 300
done
