# 📋 Manager Bot Commands Reference

## 🚀 Deployment Commands

### `/deploy`
Deploy a new bot from GitHub repository.

**Usage:**
```
/deploy
```

**Interactive steps:**
1. Send bot token
2. Send GitHub repo URL
3. Send GitHub token (or `skip` for public repos)

**Example:**
```
User: /deploy
Bot: Please send the Bot Token...
User: 123456:ABC-DEF123456789
Bot: Now send the GitHub Repository URL...
User: https://github.com/username/my-bot
Bot: If private repo, send GitHub token. If public, send: skip
User: skip
Bot: ✅ Deployment Successful! Bot ID: abc123
```

---

## 🎮 Management Commands

### `/list`
Show all deployed bots with their status.

**Usage:**
```
/list
```

**Output:**
```
🤖 Running Bots:

Bot ID: abc123
Status: 🟢 Running
Repo: https://github.com/user/bot1
Started: 2025-10-04 10:30:00
```

---

### `/stop <bot_id>`
Stop a running bot.

**Usage:**
```
/stop abc123
```

**Result:** Bot process is terminated and removed from storage.

---

### `/restart <bot_id>`
Restart a bot with the same code (no update from GitHub).

**Usage:**
```
/restart abc123
```

**When to use:** 
- Bot crashed or frozen
- After changing environment variables
- To free up memory

---

### `/update <bot_id>`
Pull latest changes from GitHub and restart the bot.

**Usage:**
```
/update abc123
```

**What it does:**
1. Runs `git pull` in bot directory
2. Reinstalls requirements if changed
3. Restarts the bot
4. Shows what changed

**Output:**
```
✅ Bot abc123 updated successfully! Changes:
Updated 3 files:
- bot.py
- plugins/start.py
- requirements.txt
```

---

## 🔄 Auto-Update Commands

### `/autoupdate on [interval]`
Enable automatic update checking.

**Usage:**
```
/autoupdate on           # Check every 5 minutes
/autoupdate on 10        # Check every 10 minutes
```

**How it works:**
- Checks all running bots every N minutes
- Runs `git fetch` to check for updates
- If updates found, automatically runs `/update`
- Logs all actions

**Recommended:** 5-10 minute intervals

---

### `/autoupdate off`
Disable automatic update checking.

**Usage:**
```
/autoupdate off
```

---

## 📊 Monitoring Commands

### `/logs <bot_id>`
View recent logs from a specific bot.

**Usage:**
```
/logs abc123
```

**Output:**
- Last 50 lines of bot logs
- Sent as text (if short)
- Sent as file (if long)

**Use for:**
- Debugging errors
- Checking bot activity
- Verifying successful startup

---

### `/status`
Show system resources and bot statistics.

**Usage:**
```
/status
```

**Output:**
```
📊 System Status

🤖 Bots:
• Running: 3/5

💻 Resources:
• CPU: 15.2%
• RAM: 45.8% (234MB / 512MB)
• Disk: 12.3% (1.2GB / 10GB)

✅ Manager Bot: Online
```

---

## 🆘 Help Commands

### `/start`
Show welcome message and command list.

**Usage:**
```
/start
```

---

## 📝 Usage Examples

### Example 1: Deploy and Manage a Bot
```
# Deploy
/deploy
[Send token, repo, GitHub token]

# Check if running
/list

# View logs
/logs abc123

# Update when you change code
/update abc123
```

---

### Example 2: Enable Auto-Updates
```
# Enable auto-update
/autoupdate on 5

# Deploy a bot
/deploy
[Follow prompts]

# Now bot will auto-update every 5 minutes!
# Just push to GitHub and it updates automatically
```

---

### Example 3: Troubleshooting
```
# Bot not responding?

# 1. Check logs
/logs abc123

# 2. Check system resources
/status

# 3. Try restart
/restart abc123

# 4. If still broken, stop and redeploy
/stop abc123
/deploy
```

---

## ⚡ Quick Tips

**For Manual Updates:**
```bash
# On GitHub
1. Edit your bot code
2. git commit -m "Fixed bug"
3. git push

# On Telegram
/update abc123
```

**For Auto-Updates:**
```bash
# One-time setup
/autoupdate on 10

# Then just push to GitHub
git push

# Bot updates automatically in 10 minutes!
```

**Resource Management:**
```
# Too many bots running?
/status                  # Check resources
/list                    # See all bots
/stop <unuse
