# Anki Self-Hosted Sync Server

> Self-hosted Anki sync server with Docker + OpenClaw skill integration.

## 🚀 Quick Start

### Prerequisites

- macOS with Homebrew
- Docker CLI (lightweight via Colima) or Docker Desktop

### Install

```bash
# 1. Install Docker runtime (macOS)
brew install docker docker-compose colima
colima start --cpu 2 --memory 4

# 2. Clone this repo
git clone https://github.com/YOUR_USERNAME/anki-selfhosted.git
cd anki-selfhosted

# 3. Configure environment
cp .env.example .env
# Edit .env and set ANKI_PASSWORD

# 4. Start server
docker-compose up -d

# 5. Verify
curl -I http://localhost:27701/
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file (see `.env.example`):

```env
# Generate a secure password with: openssl rand -base64 24
ANKI_PASSWORD=your_secure_password_here
SYNC_BASE=/data
MAX_SYNC_PAYLOAD_MEGS=500
SYNC_HOST=0.0.0.0
SYNC_PORT=8080
```

### Anki Clients

**Desktop (Anki):**
1. Tools → Preferences → Syncing
2. Custom sync server: `https://anki.aenrione.com` (or your domain)
3. Username: `alfredo`
4. Password: (from your `.env` file)

**Mobile (AnkiMobile/AnkiDroid):**
1. Settings → Sync → Custom Sync Server
2. URL: `https://anki.aenrione.com`
3. Same credentials

## 🌐 External Access

### Option 1: Direct Port (Simplest)

Expose port 27701 directly and point your domain to your public IP:

```yaml
# docker-compose.yml - Direct mode
services:
  anki-sync-server:
    image: maogxer/anki-sync-server:latest
    ports:
      - "27701:8080"
    env_file:
      - .env
    # ... rest of config
```

**Requirements:**
- Port forward 27701 in your router
- DNS A record pointing to your public IP
- SSL via reverse proxy (nginx, Caddy, Cloudflare Tunnel)

### Option 2: Nginx Reverse Proxy (Recommended)

Use nginx to proxy requests and serve a status page:

```yaml
# docker-compose.yml - Nginx mode (default)
services:
  anki-sync-server:
    image: maogxer/anki-sync-server:latest
    expose:
      - "8080"
    env_file:
      - .env
    # ... rest of config

  nginx:
    image: nginx:alpine
    ports:
      - "27701:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - ./status:/usr/share/nginx/html:ro
    depends_on:
      - anki-sync-server
```

### Option 3: Cloudflare Tunnel (Easiest)

For easy HTTPS without opening ports:

```bash
# Install cloudflared
brew install cloudflared

# Authenticate
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create anki-server

# Route domain
cloudflared tunnel route dns anki-server anki.aenrione.com

# Start tunnel
cloudflared tunnel run anki-server
```

## 📁 Structure

```
.
├── docker-compose.yml          # Server configuration
├── .env.example                # Environment variables template
├── nginx/
│   └── nginx.conf             # Reverse proxy config
├── status/
│   └── index.html             # Status page
├── data/                       # Anki collections (gitignored)
├── scripts/
│   ├── start.sh               # Start server
│   ├── stop.sh                # Stop server
│   ├── status.sh              # Check status
│   ├── install-service.sh     # Install as macOS service
│   └── uninstall-service.sh   # Remove service
├── SKILL.md                   # OpenClaw skill docs
└── README.md                  # This file
```

## 🖥️ Service Mode (Always Running)

```bash
# Install as launchd service (auto-start on boot)
./scripts/install-service.sh

# Check status
launchctl list | grep anki

# View logs
tail -f ~/.openclaw/skills/anki-server/logs/anki-server.stderr.log
```

## 🔒 Security

- **Change default password** in `.env` file
- **Use HTTPS** for external access (Cloudflare, nginx + Let's Encrypt)
- **Backup `data/` directory** regularly
- **Don't commit `.env`** — it contains your password

## 🔄 Backup

```bash
# Manual backup
cp -r data/ backups/$(date +%Y%m%d)

# Or use script
./scripts/backup.sh
```

## 🧠 OpenClaw Skill

This repo includes an OpenClaw skill for AI-assisted flashcard creation:

```bash
# Add to OpenClaw skills directory
ln -s $(pwd) ~/.openclaw/skills/anki-server
```

### Usage

```
User: "Anki esto: La capital de Francia es París"
Agent: ✅ Card created in deck "General"

User: "Anki from URL: https://en.wikipedia.org/wiki/Spaced_repetition"
Agent: ✅ 10 cards created from article

User: "Anki stats"
Agent: 📊 342 cards, 87% retention
```

## 📄 License

MIT
