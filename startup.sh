#!/data/data/com.termux/files/usr/bin/bash

# Asegurar que estamos en el directorio correcto
cd ~/hormigasais-lab/lbh-node-service

echo "🐜 [HormigasAIS] Iniciando protocolo de despliegue soberano..."

# Limpiar procesos residuales de la Colonia para evitar conflictos
pkill -f "main"
pkill -f "bridge_centinela"

echo "🧹 Limpieza de procesos completada."

# Levantar el Nodo Principal
echo "🚀 Levantando Nodo Principal (:8100)..."
./main > nodo.log 2>&1 &
sleep 2

# Levantar el Bridge Centinela
echo "📡 Levantando Bridge Centinela (:9001)..."
go run cmd/bridge_centinela/main.go > bridge.log 2>&1 &

echo "✅ Colonia HormigasAIS v0.2.0 operativa."
echo "   - Logs: nodo.log, bridge.log"
echo "   - Estado: curl http://localhost:8100/metrics"
