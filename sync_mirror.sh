#!/data/data/com.termux/files/usr/bin/bash
echo "🐜 Sincronizando lbh-node-service..."
git push origin main && echo "✅ Gitea OK" || echo "❌ Gitea FAIL"
git push github main && echo "✅ GitHub OK" || echo "❌ GitHub FAIL"
echo "🐜 Sincronización completa"
