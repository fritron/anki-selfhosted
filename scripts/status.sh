#!/bin/bash

if docker ps | grep -q anki-sync-server; then
    echo "✅ Anki Sync Server está corriendo"
    echo "   URL: http://192.168.1.21:27701"
    echo "   Usuario: alfredo"
    echo ""
    echo "📊 Logs recientes:"
    docker logs --tail 20 anki-sync-server 2>&1 || true
else
    echo "❌ Anki Sync Server no está corriendo"
    echo "   Inicia con: ~/.openclaw/skills/anki-server/scripts/start.sh"
fi
