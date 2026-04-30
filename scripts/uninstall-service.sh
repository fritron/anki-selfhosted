#!/bin/bash
# Uninstall Anki Sync Server service

set -e

PLIST_NAME="com.fritron.anki-sync-server"
PLIST_PATH="$HOME/Library/LaunchAgents/$PLIST_NAME.plist"

echo "🛑 Desinstalando Anki Sync Server..."

# Unload service
launchctl unload "$PLIST_PATH" 2>/dev/null || true

echo "✅ Servicio detenido"
echo ""
echo "📝 Para eliminar completamente, borra:"
echo "   $PLIST_PATH"
echo "   ~/.openclaw/skills/anki-server/"
