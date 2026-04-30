---
name: anki-server
description: Self-hosted Anki sync server for spaced repetition learning. Adds flashcards to Anki decks from any source — URLs, PDFs, text — and syncs them across all devices via a private Anki sync server running on the user's machine.
---

# Anki Server Skill

Self-hosted Anki sync server + flashcard creation assistant.

## Overview

This skill provides:

1. **Anki Sync Server** — Docker container running on the user's Mac mini
2. **Flashcard Creation** — AI-assisted generation of Anki cards from any source
3. **Cross-device Sync** — Anki apps on phone/tablet sync to the private server
4. **OpenClaw Integration** — Add cards via chat, research, or document analysis

## Architecture

```
+-------------+     +------------------+     +-------------+
|  Anki Mobile | --> |  Anki Sync Server | <-- |  Anki Desktop |
|   (iOS/Android) |  |  (Docker on Mac)  |     |  (Mac/PC)     |
+-------------+     +------------------+     +-------------+
                            ^
                            |
                     +-------------+
                     |   OpenClaw  |
                     |   (add cards |
                     |    via chat) |
                     +-------------+
```

## Server Setup

### Docker Compose

```yaml
# ~/.openclaw/skills/anki-server/docker-compose.yml
version: "3.8"

services:
  anki-sync-server:
    image: ghcr.io/ankitects/anki-sync-server:latest
    container_name: anki-sync-server
    restart: unless-stopped
    ports:
      - "27701:8080"
    environment:
      - SYNC_USER1=alfredo:${ANKI_PASSWORD}
      - SYNC_BASE=/data
      - MAX_SYNC_PAYLOAD_MEGS=500
    volumes:
      - ./data:/data
    networks:
      - anki-net

  # Optional: reverse proxy with HTTPS
  caddy:
    image: caddy:2-alpine
    container_name: anki-caddy
    restart: unless-stopped
    ports:
      - "27702:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - ./caddy-data:/data
      - ./caddy-config:/config
    networks:
      - anki-net
    depends_on:
      - anki-sync-server

networks:
  anki-net:
    driver: bridge
```

### Caddyfile (for HTTPS)

```
anki.fritron.local {
    reverse_proxy anki-sync-server:8080
}
```

### Start Server

```bash
cd ~/.openclaw/skills/anki-server
docker-compose up -d
```

## Client Configuration

### Anki Desktop (Mac/PC)

1. Tools → Preferences → Syncing
2. Replace AnkiWeb URL with: `http://192.168.1.21:27701`
3. Enter credentials: `alfredo` / `{password}`

### AnkiMobile (iOS)

1. Settings → Sync → Custom Sync Server
2. URL: `http://192.168.1.21:27701`
3. Credentials: `alfredo` / `{password}`

### AnkiDroid (Android)

1. Settings → Advanced → Custom Sync Server
2. Sync URL: `http://192.168.1.21:27701`
3. Media URL: `http://192.168.1.21:27701/msync`

## OpenClaw Integration

### Add Cards from Chat

```
User: "Anki esto: La capital de Francia es París"
Agent: Creates card "France Capital" -> "París"

User: "Anki from URL: https://en.wikipedia.org/wiki/Spaced_repetition"
Agent: Extracts key facts, generates 5-10 cards

User: "Anki from PDF: ~/documents/paper.pdf"
Agent: Analyzes PDF, generates cards per section
```

### Flashcard Format

```json
{
  "deck": "General::Knowledge",
  "front": "What is the capital of France?",
  "back": "Paris",
  "tags": ["geography", "europe"],
  "source": "user-chat-2026-04-30"
}
```

## Commands

| Command | Description |
|---------|-------------|
| `anki start` | Start the sync server |
| `anki stop` | Stop the sync server |
| `anki status` | Check server status |
| `anki add <text>` | Add a flashcard |
| `anki add-url <url>` | Generate cards from URL |
| `anki add-pdf <path>` | Generate cards from PDF |
| `anki decks` | List decks |
| `anki stats` | Show sync stats |

## Security

- Server runs on local network only (192.168.1.21)
- For external access: Tailscale or VPN required
- HTTPS via Caddy reverse proxy
- Password stored in environment variable

## Files

- `docker-compose.yml` — Server configuration
- `data/` — Anki collections and media
- `scripts/` — Helper scripts for card creation
- `Caddyfile` — Reverse proxy config

## Notes

- Backup: `data/` folder should be backed up regularly
- Updates: `docker-compose pull && docker-compose up -d`
- Logs: `docker logs anki-sync-server`
