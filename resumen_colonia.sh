#!/data/data/com.termux/files/usr/bin/bash

# Asegurar entorno
cd ~/hormigasais-lab/lbh-node-service

# Nombre del archivo histórico
HISTORIAL="historial_colonia.log"

# Capturar el resumen en una variable temporal
RESUMEN=$(cat <<EOM
--- RESUMEN TÁCTICO $(date) ---
METRICAS: $(curl -s http://localhost:8100/metrics | jq -c .)
BRIDGE_STATS: $(grep -c "✅ Feromona retransmitida" bridge.log) tx, $(grep -c "❌ ALERTA" bridge.log) alerts
STATUS: Main=$(pgrep -f "main" > /dev/null && echo "OK" || echo "DOWN"), Bridge=$(pgrep -f "bridge_centinela" > /dev/null && echo "OK" || echo "DOWN")
------------------------------------
EOM
)

# Mostrar en pantalla
echo "$RESUMEN"

# Escribir en el histórico
echo "$RESUMEN" >> "$HISTORIAL"

echo -e "\n✅ Resumen guardado en $HISTORIAL"
