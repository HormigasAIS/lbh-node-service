#!/data/data/com.termux/files/usr/bin/bash

# Asegurar que estamos en el directorio correcto
cd ~/hormigasais-lab/lbh-node-service

echo "🐜 [HormigasAIS] Iniciando protocolo de despliegue soberano v0.3.0..."

# 1. Limpiar procesos residuales (Nodo, Bridge y Heartbeat)
pkill -f "main"
pkill -f "bridge_centinela"
pkill -f "lbh_heartbeat.sh"

echo "🧹 Limpieza de procesos completada."

# 2. Levantar el Nodo Principal
echo "🚀 Levantando Nodo Principal (:8100)..."
./main > nodo.log 2>&1 &
sleep 2

# 3. Levantar el Bridge Centinela
echo "📡 Levantando Bridge Centinela (:9001)..."
go run cmd/bridge_centinela/main.go > bridge.log 2>&1 &
sleep 1

# 4. Lanzar el SISTEMA DE LATIDO (Heartbeat) en segundo plano
echo "💓 Activando Sistema Nervioso Central (Heartbeat)..."
~/hormigasais-lab/LBH-Net/tools/lbh_heartbeat.sh > heartbeat.log 2>&1 &

echo "✅ Colonia HormigasAIS operativa y bajo vigilancia."
echo "   - Logs: nodo.log, bridge.log, heartbeat.log"
echo "   - Estado: ./resumen_colonia.sh"
