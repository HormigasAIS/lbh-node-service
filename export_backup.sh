#!/bin/bash
# HORMIGASAIS · export_backup.sh
# Exporta el respaldo a: Almacenamiento interno/Respaldo Gitea

DESTINO="/sdcard/Respaldo Gitea"
ORIGEN="$HOME/hormigasais-lab"

# Buscar el archivo .tar.gz más reciente en el laboratorio
ULTIMO_BACKUP=$(ls -t $ORIGEN/HormigasAIS_Respaldo_*.tar.gz 2>/dev/null | head -n 1)

if [ -z "$ULTIMO_BACKUP" ]; then
    echo "❌ No se encontró ningún archivo de respaldo en $ORIGEN"
    exit 1
fi

echo "🐜 LBH :: Iniciando exportación soberana..."
echo "📦 Archivo: $(basename "$ULTIMO_BACKUP")"

# Copiar a la ruta específica de la memoria interna
cp "$ULTIMO_BACKUP" "$DESTINO/"

if [ $? -eq 0 ]; then
    echo "✅ ÉXITO: Copiado a '$DESTINO'"
    echo "📊 Tamaño detectado: $(du -h "$ULTIMO_BACKUP" | awk '{print $1}')"
    echo "📅 Fecha: $(date '+%d %b %I:%M %p')"
else
    echo "❌ ERROR: No se pudo copiar. Ejecuta 'termux-setup-storage' para dar permisos."
fi
