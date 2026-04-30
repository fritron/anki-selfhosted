---
name: anki-server
description: Self-hosted Anki sync server + AI-powered flashcard creation via OpenClaw. Create, manage, and sync flashcards across all devices. Generate cards from text, URLs, and PDFs using AI. Auto-sync after every operation.
---

# 🧠 Anki Server Skill

Complete Anki flashcard management through OpenClaw chat interface.

## Features

- ✅ **Create cards** from chat
- ✅ **Auto-sync** after every operation
- ✅ **Generate cards** from text/URLs/PDFs using AI
- ✅ **List, search, delete** cards
- ✅ **Cross-device sync** via self-hosted server
- ✅ **No manual sync needed** — everything syncs automatically

## Architecture

```
WhatsApp → OpenClaw → AnkiConnect → Anki Desktop
                                     ↓ Auto-sync
                                  Sync Server
                                     ↓
                               Mobile (AnkiDroid/iOS)
```

## Setup

### 1. Start Sync Server
```bash
anki start
```

### 2. Install AnkiConnect (Anki Desktop)
- Anki → Tools → Add-ons → Get Add-ons → Code: `2055492159`
- Restart Anki
- Keep Anki Desktop open while using OpenClaw

### 3. Configure Anki Mobile
- Settings → Sync → Custom Sync Server
- URL: `https://anki.aenrione.com`
- Credentials: `alfredo` / password from `.env`

## Commands

### Create Cards (Auto-sync)
```
"Anki crear: PREGUNTA = RESPUESTA"
→ Card creada + sync automático al servidor

"Anki crear: Capital de Italia = Roma [deck: Geografía]"
→ Card en deck específico + sync automático

"Anki crear deck: Ciencias"
→ Nuevo deck + sync automático
```

### Generate from Content (Auto-sync)
```
"Anki desde texto: El Sol es una estrella amarilla enana..."
→ Genera N cards + sync automático

"Anki desde URL: https://es.wikipedia.org/wiki/Sol"
→ Extrae contenido + genera cards + sync

"Anki desde PDF: ~/documents/fisica.pdf"
→ Analiza PDF + genera cards + sync
```

### Manage
```
"Anki listar decks"
"Anki buscar: Sol"
"Anki eliminar: ID o texto"
→ Todas con sync automático después

"Anki stats"
"Anki sync"
```

## Auto-Sync Behavior

| Operation | Auto-sync? |
|-----------|-----------|
| Create card | ✅ Yes |
| Create deck | ✅ Yes |
| Delete card | ✅ Yes |
| List decks | ❌ No (read-only) |
| Search | ❌ No (read-only) |
| Stats | ❌ No (read-only) |

## Files

- `scripts/anki-connect.py` — AnkiConnect client with auto-sync
- `scripts/anki-manager.py` — Standalone card generator
- `docker-compose.yml` — Sync server
- `nginx/nginx.conf` — Reverse proxy
