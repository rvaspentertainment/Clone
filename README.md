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
   - **Port**: Leave default
   - **Health Check**: Disabled

5. **Click "Deploy"** and wait for deployment to complete

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
- `/restart <bot_id>` - Restart a bot
- `/logs <bot_id>` - View recent logs
- `/status` - Check system resources

## 🔐 GitHub Personal Access Token

For **private repositories**, you need a GitHub token:

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (Full control of private repositories)
4. Generate and copy the token
5. Use this token when deploying private repos

## 📝 Bot Repository Requirements

Your bot repository must have:

1. **Main file** named one of:
   - `bot.py`
   - `main.py`
   - `app.py`
   - `__main__.py`

2. **requirements.txt** (optional but recommended)

3. **Environment variable support**:
   - Your bot should read `BOT_TOKEN` from environment:
   ```python
   import os
   BOT_TOKEN = os.getenv("BOT_TOKEN")
   ```

### Example Bot Structure

```
my-bot/
├── bot.py              # Main bot file
├── requirements.txt    # Dependencies
└── config.py          # Optional config
```

**bot.py example:**
```python
import os
from pyrogram import Client, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Hello! I'm running on Koyeb!")

app.run()
```

## 🛠️ Troubleshooting

### Bot fails to deploy

**Error: "No main bot file found"**
- Ensure your repo has `bot.py`, `main.py`, or `app.py`

**Error: "Requirements installation failed"**
- Check your `requirements.txt` for invalid packages
- Ensure all packages are available on PyPI

**Error: "Bot process died immediately"**
- Check bot logs with `/logs <bot_id>`
- Verify bot token is correct
- Ensure bot code has no syntax errors

### Bot stops running

- Check system resources with `/status`
- Restart the bot with `/restart <bot_id>`
- Check logs for errors

### Koyeb deployment issues

- Verify all environment variables are set correctly
- Ensure your Manager Bot token is valid
- Check Koyeb logs in the dashboard

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
- **Storage**: Temporary (ephemeral)

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
