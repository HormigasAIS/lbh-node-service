#!/bin/bash
# HORMIGASAIS · sync_mirror.sh v1.2 · LBH v1.1
REPO_DIR=/data/data/com.termux/files/home/hormigasais-lab/lbh-node-service
DB=/data/data/com.termux/files/home/hormigasais-lab/lbh-node-service/lbh_nodo.db
cd $REPO_DIR
echo "Sincronizando espejo HormigasAIS..."
echo "Rama: $(git branch --show-current)"
git push origin main
if [ $? -eq 0 ]; then echo "Gitea: OK"; else echo "Gitea: ERROR"; fi
timeout 15s git push github main
if [ $? -eq 0 ]; then echo "GitHub: OK"; else echo "GitHub: ERROR"; fi
echo "Feromonas: $(sqlite3 $DB 'SELECT COUNT(*) FROM feromonas' 2>/dev/null || echo N/A)"
echo "--------------------------------------------------"
