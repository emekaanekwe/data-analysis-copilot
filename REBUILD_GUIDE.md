# Container Rebuild Guide

## 🚀 Easiest Way - Use the Rebuild Script

```bash
./rebuild.sh
```

Then choose option 1 (Docker Compose) or option 2 (Docker Build).

---

## 📋 Manual Commands

### Method 1: Docker Compose (Recommended)

**Why?** Includes volume mounting for live reloading automatically.

```bash
# Stop and remove old containers
docker compose down

# Rebuild and start
docker compose up --build

# Or run in background
docker compose up --build -d

# View logs
docker compose logs -f
```

**Access:** http://localhost:8501

**Benefits:**
- ✅ Live reloading (changes show up automatically)
- ✅ Easy to manage
- ✅ Single command to start/stop
- ✅ Environment variables auto-loaded

---

### Method 2: Docker Build (Your Current Method)

**Your original command:**
```bash
docker build -t streamlit_app .
```

**To rebuild with live reloading:**

```bash
# 1. Stop existing container
docker stop $(docker ps -aq --filter "ancestor=streamlit_app")
docker rm $(docker ps -aq --filter "ancestor=streamlit_app")

# 2. Rebuild image
docker build -t streamlit_app .

# 3. Run with volume mounting (THIS IS THE KEY!)
docker run -d \
  --name data-analysis-copilot \
  -p 8501:8501 \
  -v $(pwd):/data-analysis-copilot \
  --env-file .env \
  streamlit_app

# 4. View logs
docker logs -f data-analysis-copilot
```

**Access:** http://localhost:8501

**The KEY difference:** The `-v $(pwd):/data-analysis-copilot` flag mounts your local directory into the container, enabling live reloading.

---

## 🔍 Check What's Running

```bash
# List all containers
docker ps -a

# List only running containers
docker ps

# Find your container
docker ps --filter "ancestor=streamlit_app"
docker ps --filter "name=data-analysis-copilot"
```

---

## 🛑 Stop Everything

```bash
# If using Docker Compose
docker compose down

# If using Docker Build
docker stop data-analysis-copilot
docker rm data-analysis-copilot

# Nuclear option (stop ALL containers)
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
```

---

## 🔧 When Do You Need to Rebuild?

### ✅ YES - Rebuild Required:
- Changed `requirements.txt` (added/removed packages)
- Changed `Dockerfile` configuration
- First time running
- Packages not installing correctly

### ❌ NO - Just Edit and Save:
- Changed Python code (`.py` files)
- Changed `.env` variables (restart container only)
- Changed UI/logic

**With live reloading enabled**, Python file changes appear automatically in 1-2 seconds!

---

## 📊 Comparison Table

| Feature | Docker Compose | Docker Build (old) | Docker Build (with volume) |
|---------|----------------|-------------------|---------------------------|
| **Command** | `docker compose up` | `docker run streamlit_app` | `docker run -v $(pwd):...` |
| **Live Reloading** | ✅ Yes | ❌ No | ✅ Yes |
| **Rebuild Needed** | Only for packages | Every change | Only for packages |
| **Env Variables** | Auto-loaded | Manual | Manual |
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 💡 Recommended Workflow

1. **First time setup:**
   ```bash
   docker compose up --build
   ```

2. **Daily development:**
   - Just edit your Python files
   - Save and watch them reload automatically
   - No rebuild needed!

3. **After changing packages:**
   ```bash
   docker compose up --build
   ```

4. **When done:**
   ```bash
   docker compose down
   ```

---

## 🐛 Troubleshooting

### "Container name already in use"
```bash
docker rm -f data-analysis-copilot
```

### "Port 8501 already in use"
```bash
# Find what's using it
sudo lsof -i :8501

# Stop it
docker stop $(docker ps -q --filter "publish=8501")
```

### "Permission denied" on Docker commands
```bash
# Add your user to docker group (one time)
sudo usermod -aG docker $USER

# Then logout and login again
```

### Changes not showing up
1. Verify volume is mounted:
   ```bash
   docker exec -it data-analysis-copilot ls -la
   ```

2. Check Streamlit is watching files:
   ```bash
   docker logs data-analysis-copilot | grep -i watch
   ```

3. Hard refresh browser: `Ctrl + Shift + R`
