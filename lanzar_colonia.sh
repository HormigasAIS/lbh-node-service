#!/usr/bin/env bash

echo "🐜 [HormigasAIS] Iniciando infraestructura soberana..."

# 1. Liberar puerto 8080 si está ocupado
fuser -k 8080/tcp 2>/dev/null || pkill -f "python3 -m http.server 8080"

# 2. Lanzar Servidor Web (Dashboard)
cd ~/hormigasais-lab/lbh-node-service
python3 -m http.server 8080 > web_server.log 2>&1 &
echo "🚀 Dashboard activo en http://localhost:8080"

# 3. Lanzar Puente de Telemetría en bucle
echo "📡 Activando puente de datos LBH..."
while true; do
  python3 ~/hormigasais-lab/lbh-node-service/generar_demo_state.py
  sleep 3
done
