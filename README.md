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

# 3. Start server
docker-compose up -d

# 4. Verify
curl -I http://localhost:27701/
```

### Configure Anki Clients

**Desktop (Anki):**
1. Tools → Preferences → Syncing
2. Custom sync server: `http://YOUR_IP:27701`
3. Username: `alfredo`
4. Password: `changeme` (change in docker-compose.yml)

**Mobile (AnkiMobile/AnkiDroid):**
1. Settings → Sync → Custom Sync Server
2. URL: `http://YOUR_IP:27701`
3. Same credentials

## 📁 Structure

```
.
├── docker-compose.yml          # Server config
├── scripts/
│   ├── start.sh               # Start server
│   ├── stop.sh                # Stop server
│   ├── status.sh              # Check status
│   ├── install-service.sh     # Install as macOS service
│   └── uninstall-service.sh   # Remove service
├── SKILL.md                   # OpenClaw skill docs
└── README.md                  # This file
```

## 🔧 Service Mode (Always Running)

```bash
# Install as launchd service (auto-start on boot)
./scripts/install-service.sh

# Check status
launchctl list | grep anki

# View logs
tail -f ~/.openclaw/skills/anki-server/logs/anki-server.stderr.log
```

## 🌐 External Access

For access outside your network, use a reverse proxy:

### Nginx Example

```nginx
server {
    listen 443 ssl;
    server_name anki.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:27701;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Tailscale (Easy VPN)

```bash
# Install Tailscale
brew install tailscale

# Connect
tailscale up

# Access from anywhere
# URL: http://your-mac-mini:27701
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

## 📝 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SYNC_USER1` | `alfredo:changeme` | Username:password |
| `SYNC_BASE` | `/data` | Data directory |
| `MAX_SYNC_PAYLOAD_MEGS` | `500` | Max upload size |
| `SYNC_HOST` | `0.0.0.0` | Bind address |
| `SYNC_PORT` | `8080` | Internal port |

## 🔒 Security

- Change default password in `docker-compose.yml`
- Use HTTPS for external access (nginx/Caddy)
- Consider VPN (Tailscale) for remote access
- Backup `data/` directory regularly

## 🔄 Backup

```bash
# Manual backup
cp -r data/ backups/$(date +%Y%m%d)

# Or use script
./scripts/backup.sh
```

## 📄 License

MIT
