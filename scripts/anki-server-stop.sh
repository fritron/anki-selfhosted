#!/bin/bash
# Anki Sync Server stop script for launchd

ANKI_DIR="$HOME/.openclaw/skills/anki-server"
cd "$ANKI_DIR"

docker compose down >> "$ANKI_DIR/logs/anki-server.log" 2>&1
