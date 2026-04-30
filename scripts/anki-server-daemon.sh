#!/bin/bash
# Anki Sync Server wrapper for launchd

set -e

ANKI_DIR="$HOME/.openclaw/skills/anki-server"
LOG_DIR="$ANKI_DIR/logs"
LOG_FILE="$LOG_DIR/anki-server.log"

mkdir -p "$LOG_DIR"

cd "$ANKI_DIR"

# Check if docker is available
if ! command -v docker &> /dev/null; then
    echo "$(date): Docker no está instalado" >> "$LOG_FILE"
    exit 1
fi

# Check if docker is running
if ! docker info > /dev/null 2>&1; then
    echo "$(date): Docker no está corriendo, intentando iniciar..." >> "$LOG_FILE"
    open -a Docker 2>&1 || true
    sleep 15
fi

# Pull latest image if needed
docker compose pull >> "$LOG_FILE" 2>&1

# Start server
echo "$(date): Iniciando Anki Sync Server..." >> "$LOG_FILE"
docker compose up -d >> "$LOG_FILE" 2>&1

echo "$(date): Servidor iniciado" >> "$LOG_FILE"
