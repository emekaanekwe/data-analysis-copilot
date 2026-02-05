# Docker Development Guide

This guide will help you run the Streamlit app with **live reloading** in Docker.

> **Note:** This guide uses `docker compose` (V2 syntax). If you have the older version, use `docker compose` instead.

## Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and start the container with live reloading
docker compose up --build

# Or run in detached mode (background)
docker compose up -d

# View logs
docker compose logs -f

# Stop the container
docker compose down
```

### Option 2: Using Docker Run (Manual)

```bash
# Build the image
docker build -t data-analysis-copilot .

# Run with volume mounting for live reloading
docker run -p 8501:8501 \
  -v $(pwd):/data-analysis-copilot \
  --env-file .env \
  data-analysis-copilot
```

## How Live Reloading Works

### Volume Mounting
The key is the `volumes` section in `docker compose.yml`:
```yaml
volumes:
  - .:/data-analysis-copilot  # Maps your local directory to container
```

This means:
- ✅ Changes to `.py` files are reflected immediately
- ✅ No need to rebuild the container
- ✅ Streamlit auto-reloads when files change

### Streamlit Configuration
The command includes these flags:
- `--server.fileWatcherType=poll` - Detects file changes in Docker
- `--server.runOnSave=true` - Auto-reloads on save

## Access Your App

Once running, open your browser:
- **Local:** http://localhost:8501
- **From another machine:** http://YOUR_IP:8501

## Common Commands

```bash
# Rebuild after changing requirements.txt
docker compose up --build

# Stop all containers
docker compose down

# View running containers
docker ps

# Enter the container shell
docker exec -it data-analysis-copilot bash

# View real-time logs
docker compose logs -f streamlit-app

# Restart the container
docker compose restart
```

## Troubleshooting

### Changes Not Showing Up?

1. **Check if volume is mounted:**
   ```bash
   docker exec -it data-analysis-copilot ls -la
   ```

2. **Verify Streamlit is watching files:**
   - Look for "Watching for file changes" in logs
   - Check `docker compose logs -f`

3. **Hard refresh browser:**
   - Press `Ctrl + Shift + R` (Windows/Linux)
   - Press `Cmd + Shift + R` (Mac)

4. **Restart the container:**
   ```bash
   docker compose restart
   ```

### Port Already in Use?

```bash
# Change port in docker compose.yml
ports:
  - "8502:8501"  # Use 8502 instead
```

### Permission Issues?

```bash
# Add user permissions to Dockerfile
USER root
RUN chmod -R 777 /data-analysis-copilot
```

## Development Workflow

1. **Start container once:**
   ```bash
   docker compose up
   ```

2. **Edit files locally** in your IDE (VSCode, PyCharm, etc.)

3. **Save changes** - Streamlit auto-reloads in ~1-2 seconds

4. **Check browser** - Changes appear automatically

## When to Rebuild

You **only** need to rebuild when:
- ❗ Changing `requirements.txt` (adding/removing packages)
- ❗ Changing `Dockerfile` configuration
- ❗ Changing environment variables in `.env`

Rebuild command:
```bash
docker compose down
docker compose up --build
```

## Production vs Development

### Development (Current Setup)
- Uses volume mounting
- Live reloading enabled
- Logs visible
- Easy debugging

### Production (Future)
Remove volume mounting from `docker compose.yml`:
```yaml
# Comment out or remove volumes
# volumes:
#   - .:/data-analysis-copilot
```

Build and deploy:
```bash
docker build -t data-analysis-copilot:prod .
docker run -p 8501:8501 --env-file .env data-analysis-copilot:prod
```
