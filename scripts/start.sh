#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Check if docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está corriendo. Iniciando Docker Desktop..."
    open -a Docker
    sleep 10
fi

# Pull latest image
echo "📦 Descargando última imagen de Anki Sync Server..."
docker compose pull

# Start server
echo "🚀 Iniciando Anki Sync Server..."
docker compose up -d

# Wait for healthcheck
echo "⏳ Esperando a que el servidor esté listo..."
sleep 5

# Check status
if curl -s http://localhost:27701/ > /dev/null 2>&1; then
    echo "✅ Anki Sync Server corriendo en http://192.168.1.21:27701"
    echo ""
    echo "📱 Configura tus clientes Anki:"
    echo "   URL: http://192.168.1.21:27701"
    echo "   Usuario: alfredo"
    echo "   Contraseña: ${ANKI_PASSWORD:-changeme}"
    echo ""
    echo "💡 Para cambiar la contraseña, edita docker-compose.yml o setea ANKI_PASSWORD"
else
    echo "⚠️  El servidor no respondió. Revisa los logs:"
    echo "   docker logs anki-sync-server"
fi
