# 🤖 Telegram Bot Manager - Koyeb Multi-Bot Hosting

Deploy and manage multiple Telegram bots from GitHub repositories on a single Koyeb instance!

## 📋 Features

- ✅ Deploy multiple bots from GitHub (public & private repos)
- ✅ Automatic repository cloning and requirements installation
- ✅ Process management (start, stop, restart)
- ✅ Real-time logs viewing
- ✅ System status monitoring
- ✅ Full error handling and deployment notifications
- ✅ Runs on Koyeb free tier (1 service limit)

## 🚀 Prerequisites

Before deploying, you need:

1. **Telegram API Credentials**
   - Get `API_ID` and `API_HASH` from https://my.telegram.org
   
2. **Manager Bot Token**
   - Create a bot via [@BotFather](https://t.me/botfather)
   - Get the bot token (this will be your Manager Bot)

3. **Your Telegram User ID**
   - Get your ID from [@userinfobot](https://t.me/userinfobot)

4. **Koyeb Account**
   - Sign up at https://koyeb.com (free tier available)

5. **GitHub Account** (for repos to deploy)
   - Personal Access Token (for private repos)

## 📦 Installation

### Method 1: Deploy to Koyeb (Recommended)

1. **Fork this repository** to your GitHub account

2. **Go to Koyeb Dashboard**
   - Click "Create App"
   - Select "GitHub" as deployment method
   - Connect your GitHub account
   - Select this forked repository

3. **Configure Environment Variables** in Koyeb:
   ```
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_manager_bot_token
   ADMIN_IDS=your_telegram_user_id
   ```
   
   Example:
   ```
   API_ID=12345678
   API_HASH=abcdef1234567890abcdef1234567890
   BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ADMIN_IDS=987654321
   ```

4. **Deploy Settings**:
   - **Instance Type**: Free (Nano)
   - **Region**: Choose closest to you
   - **Builder**: Dockerfile
   - **Port**: Leave default (or set to 8000)
   - **Run Command**: `python bot.py` (or leave empty, Procfile will handle it)
   - **Health Check**: Disabled

5. **Click "Deploy"** and wait for deployment to complete (2-5 minutes)

### Method 2: Local Testing

```bash
# Clone repository
git clone https://github.com/yourusername/bot-manager.git
cd bot-manager

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export API_ID="your_api_id"
export API_HASH="your_api_hash"
export BOT_TOKEN="your_manager_bot_token"
export ADMIN_IDS="your_telegram_user_id"

# Run the bot
python bot.py
```

## 📖 Usage Guide

### Step 1: Start the Manager Bot

Send `/start` to your Manager Bot on Telegram.

### Step 2: Deploy a Bot

1. Send `/deploy` command
2. **Send Bot Token** - The token for the bot you want to deploy
3. **Send GitHub Repo URL** - Example: `https://github.com/username/my-bot`
4. **Send GitHub Token** - If private repo, send your GitHub Personal Access Token. If public, send `skip`
5. **Wait for deployment** - The bot will clone, install requirements, and start your bot

### Step 3: Manage Your Bots

Available commands:

- `/list` - Show all running bots
- `/stop <bot_id>` - Stop a specific bot
- `/restart <bot_id>` - Restart a bot (keeps same code)
- `/update <bot_id>` - **Pull latest changes from GitHub and restart**
- `/logs <bot_id>` - View recent logs
- `/status` - Check system resources

### Step 4: Update Deployed Bots

When you edit your deployed bot's code on GitHub:

**Option 1: Manual Update (Recommended)**
1. Push changes to GitHub
2. Send `/update <bot_id>` to Manager Bot
3. Bot will:
   - Pull latest code (`git pull`)
   - Reinstall requirements if changed
   - Restart with new code
   - Notify you of changes

**Option 2: Auto-Update (Experimental)**
Enable automatic update checking:
```
/autoupdate on        # Check every 5 minutes
/autoupdate on 10     # Check every 10 minutes
/autoupdate off       # Disable auto-update
```

**How it works:**
- Manager Bot checks GitHub every N minutes
- If changes detected, automatically pulls and restarts
- No manual intervention needed
- Good for continuous deployment

**Note:** Auto-update uses system resources. Recommended interval: 5-10 minutes.

## 🔐 GitHub Personal Access Token

For **private repositories**, you need a GitHub token:

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (Full control of private repositories)
4. Generate and copy the token
5. Use this token when deploying private repos

## 📝 Bot Repository Requirements

Your bot repository can have any of these startup methods (checked in order):

### ✅ Supported Startup Methods:

1. **Shell Scripts** (priority):
   - `start.sh`
   - `run.sh`
   - `startup.sh`

2. **Python Files**:
   - `bot.py`
   - `main.py`
   - `app.py`
   - `__main__.py`
   - `run.py`

3. **Python Package**:
   - `__init__.py` (runs as module)

4. **Procfile** (Heroku-style):
   ```
   worker: python bot.py
   bot: python main.py
   ```

5. **Auto-detection**:
   - Searches subdirectories for files with "bot" or "main" in name

### 🤖 Works with Popular Bot Types:

✅ **Autofilter Bots** (TG-File-Store, Autofilter-V3, etc.)
✅ **Music Bots** (VCPlayerBot, MusicBot, etc.)
✅ **Mirror Bots** (Telegram-Mirror-Bot, etc.)
✅ **Custom Bots** (any structure)

### 📁 Example Bot Structure (Autofilter):

```
autofilter-bot/
├── bot.py              # Main bot file
├── database/           # Database module
├── plugins/            # Plugin files
├── requirements.txt    # Dependencies
├── config.py          # Configuration
└── start.sh           # Optional startup script
```

**Environment Variable Support:**

Your bot should read `BOT_TOKEN` from environment:
```python
import os
BOT_TOKEN = os.getenv("BOT_TOKEN")
```

For autofilter bots with multiple env vars, you can also pass them during deployment (coming soon) or hardcode non-sensitive ones.

## 🛠️ Troubleshooting

### Bot fails to deploy

**Error: "No valid startup file found"**
- Ensure your repo has one of: `bot.py`, `main.py`, `start.sh`, `Procfile`, or Python package structure
- For autofilter bots, make sure the main bot file exists
- Check if the bot requires specific environment variables

**Error: "Requirements installation failed"**
- Check your `requirements.txt` for invalid packages
- Ensure all packages are available on PyPI
- Some packages may require system dependencies

**Error: "Bot process died immediately"**
- Check bot logs with `/logs <bot_id>`
- Verify bot token is correct
- Ensure all required environment variables are set
- Check for syntax errors in bot code
- Verify database connections (if bot uses database)

### Bot stops running

- Check system resources with `/status`
- Restart the bot with `/restart <bot_id>`
- Check logs for errors

### Koyeb deployment issues

**Error: "no command to run your application"**
- Make sure `Procfile` is in your repository
- Or set Run Command in Koyeb: `python bot.py`
- Ensure Dockerfile is present

**Error: "Application exited with code 1"**
- Check if all environment variables are set correctly
- Verify BOT_TOKEN, API_ID, API_HASH, ADMIN_IDS are all set
- Check Koyeb logs for specific error messages
- Make sure the bot token is valid

- Verify all environment variables are set correctly
- Ensure your Manager Bot token is valid
- Check Koyeb logs in the dashboard
- Try redeploying the service

## ⚠️ Important Notes

1. **Free Tier Limits**: Koyeb free tier has resource limits. Don't deploy too many heavy bots.

2. **Bot Token Security**: Never commit bot tokens to GitHub. Always use environment variables.

3. **GitHub Token**: Keep your GitHub token secure. It has access to your repositories.

4. **Process Management**: If Koyeb restarts, all deployed bots will need to be redeployed.

5. **Logs**: Logs are stored in memory. They will be lost on restart.

## 🔄 Updating the Manager Bot

If you update the manager bot code:

1. Push changes to GitHub
2. Koyeb will auto-deploy (if enabled)
3. Or manually redeploy from Koyeb dashboard

## 📊 System Requirements

- **RAM**: 512MB minimum (free tier provides 512MB)
- **CPU**: 0.1 vCPU (free tier sufficient)
- **Storage**: Ephemeral (temporary, but bots auto-restore on restart)

## 💾 Data Persistence

The bot uses **JSON file storage** (`bots_data.json`) to save:
- Bot tokens
- GitHub repository URLs
- Bot directories
- Deployment timestamps

**Benefits:**
- ✅ Auto-restart bots after Manager Bot restart
- ✅ No MongoDB needed
- ✅ Simple and lightweight
- ✅ Works on Koyeb free tier

**Note:** Koyeb free tier uses ephemeral storage. If the instance is fully recreated, you'll need to redeploy bots. But normal restarts preserve bot data.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

This project is open source and available under the MIT License.

## 💬 Support

For issues and questions:
1. Check this README
2. Review error logs with `/logs`
3. Check Koyeb dashboard logs
4. Open an issue on GitHub

## 🎯 Roadmap

- [ ] Persistent storage for bot data
- [ ] Auto-restart on crash
- [ ] Resource usage per bot
- [ ] Web dashboard
- [ ] Multiple admin support
- [ ] Bot templates

---

Made with ❤️ for the Telegram bot community

**Happy Bot Hosting! 🚀**
