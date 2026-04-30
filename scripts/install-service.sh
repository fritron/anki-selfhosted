#!/bin/bash
# Install Anki Sync Server as a macOS service

set -e

PLIST_NAME="com.fritron.anki-sync-server"
PLIST_PATH="$HOME/Library/LaunchAgents/$PLIST_NAME.plist"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔧 Instalando Anki Sync Server como servicio del sistema..."

# Create logs directory
mkdir -p "$HOME/.openclaw/skills/anki-server/logs"

# Load the service
launchctl unload "$PLIST_PATH" 2>/dev/null || true
launchctl load -w "$PLIST_PATH"

echo "✅ Servicio instalado y cargado"
echo ""
echo "📋 Comandos útiles:"
echo "   launchctl start $PLIST_NAME    # Iniciar manualmente"
echo "   launchctl stop $PLIST_NAME     # Detener"
echo "   launchctl list | grep anki     # Ver estado"
echo ""
echo "📝 Logs:"
echo "   tail -f ~/.openclaw/skills/anki-server/logs/anki-server.stderr.log"
echo ""
echo "💡 El servicio arrancará automáticamente al iniciar sesión"
