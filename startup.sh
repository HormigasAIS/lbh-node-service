#!/bin/bash
# HORMIGASAIS · startup.sh v0.4 · LBH v1.1
# Unificado con start_colonia.sh
REPO=/data/data/com.termux/files/home/hormigasais-lab/lbh-node-service
DB=$REPO/lbh_nodo.db
LOGDIR=/data/data/com.termux/files/home/hormigasais-core/logs
mkdir -p $LOGDIR
echo "[STARTUP] HormigasAIS iniciando..."

# Limpiar procesos previos
pkill -f "./main" 2>/dev/null
pkill -f "colony_heartbeat.py" 2>/dev/null
pkill -f "lbh_panel_web.py" 2>/dev/null
pkill -f "lbh_sensor.py" 2>/dev/null
sleep 1

# Compilar si no existe binario
cd $REPO
if [ ! -f main ]; then
    echo "Compilando nodo maestro..."
    go build -o main main.go
fi

# Nodo maestro REST :8100
fuser -k 8100/tcp 2>/dev/null
./main > $LOGDIR/node.log 2>&1 &
echo "REST :8100 PID: $!"

# Sensor daemon
python3 $REPO/lbh_sensor.py > $LOGDIR/sensor.log 2>&1 &
echo "sensor PID: $!"

# Colony Panel :8300
fuser -k 8300/tcp 2>/dev/null
python3 ~/hormigasais-lab/lbh_panel_web.py > $LOGDIR/panel.log 2>&1 &
echo "panel PID: $!"

# Colony Heartbeat
python3 -u ~/hormigasais-lab/colony_heartbeat.py >> $LOGDIR/heartbeat.log 2>&1 &
echo "heartbeat PID: $!"

# Sync nodos remotos
nohup bash -c 'while true; do
    python3 ~/hormigasais-core/nodos/sync_nodos_remotos.py
    python3 ~/hormigasais-core/nodos/registrar_nodo.py A16_CORE
    sleep 30
done' > $LOGDIR/sync.log 2>&1 &
echo "sync PID: $!"

# Alerta nodos inactivos
nohup bash -c 'while true; do
    python3 ~/hormigasais-core/nodos/alerta_nodos_inactivos.py
    sleep 60
done' > $LOGDIR/alerta.log 2>&1 &
echo "alerta PID: $!"

sleep 2
TOTAL=$(sqlite3 $DB 'SELECT COUNT(*) FROM feromonas' 2>/dev/null || echo 0)
echo "--------------------------------------------------"
echo "COLONIA OPERATIVA"
echo "REST:   http://localhost:8100"
echo "PANEL:  http://localhost:8300"
echo "GITEA:  http://localhost:3001"
echo "FEROMONAS: $TOTAL"
echo "--------------------------------------------------"
